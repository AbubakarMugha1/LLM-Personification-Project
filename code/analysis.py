"""Reproduces the numbers in the paper from data/labels.csv.
RQ3 (where ads were served) also needs the dataset's videos_dataset.csv (access on request from its authors):
    python code/analysis.py [path/to/videos_dataset.csv]"""
import sys, json, hashlib, itertools, re
import numpy as np, pandas as pd
from scipy.stats import ttest_1samp, fisher_exact

THEMES = {"romance/sexual": r"romant|sexual|kiss|intimate|suggestive|sensual",
          "clothing/skin": r"cloth|revealing|skin|bikini|swim|lingerie|dress|attire|modest",
          "violence/weapons": r"violen|weapon|gun|fight|blood", "alcohol": r"alcohol|beer|wine|liquor",
          "profanity": r"profan|swear|curse|vulgar", "smoking/drugs": r"smok|tobacco|cigar|vap|drug|cannabis|marijuana",
          "gambling": r"gambl|casino|betting|lotter", "scary/horror": r"scar|fright|horror|creep|disturb|gore|terrif",
          "dangerous acts": r"danger|stunt|unsafe|imitat|reckless",
          "religion/occult": r"relig|spiritual|occult|magic|supernatural|witch|demon",
          "politics": r"politic|propaganda|war\b|military", "death/crime": r"death|dead|murder|kill|crime|criminal"}
COSI = {"Saudi Arabia": "A", "Sweden": "A", "Japan": "A", "United States": "A", "Germany": "A", "South Korea": "A",
        "Turkey": "B", "Indonesia": "B", "France": "B", "Pakistan": "B", "United Arab Emirates": "B", "Belgium": "B",
        "Iran": "C", "Finland": "C", "Ukraine": "C", "Bahrain": "C", "Morocco": "C", "Austria": "C",
        "Algeria": "D", "Jordan": "D", "Sri Lanka": "D", "Bulgaria": "D", "Bangladesh": "D", "Ghana": "D"}
rng = np.random.default_rng(11)

def holm(ps):
    ps = np.asarray(ps); o = np.argsort(ps); m = len(ps); adj = np.empty(m); run = 0
    for k, i in enumerate(o): run = max(run, (m - k) * ps[i]); adj[i] = min(1, run)
    return adj

L = pd.read_csv("data/labels.csv")
concerns = L.concerns.apply(lambda s: " ".join(json.loads(s)).lower())
for t, rx in THEMES.items(): L[t] = concerns.str.contains(rx).astype(float)
L["Inappropriate"] = L.label.eq("Inappropriate").astype(float)
Y = ["Inappropriate"] + list(THEMES)
MM = set(L.loc[L.muslim_majority, "country"])
print("labels:", len(L), "| per run:", L.groupby("run").size().to_dict())

# RQ1/RQ2: MM vs other personas, countries as the unit (permutation of the MM label), Holm over 13 measures
rate = L.groupby("country")[Y].mean() * 100
lab = rate.index.isin(MM); B = 200_000
perms = np.array([rng.permutation(lab) for _ in range(B)])
rows = []
for y in Y:
    v = rate[y].values; obs = v[lab].mean() - v[~lab].mean()
    null = (perms * v).sum(1) / lab.sum() - ((~perms) * v).sum(1) / (~lab).sum()
    rows.append((y, v[lab].mean(), v[~lab].mean(), (np.sum(np.abs(null) >= abs(obs) - 1e-12) + 1) / (B + 1)))
T = pd.DataFrame(rows, columns=["measure", "MM_%", "other_%", "p"]); T["p_holm"] = holm(T.p)
print("\nTable 1 (MM vs other, %, three runs pooled):\n", T.round(4).to_string(index=False))
print("\n% labelled Inappropriate per country:\n", rate.Inappropriate.round(1).sort_values().to_string())
for r in sorted(L.run.unique()):
    rr = L[L.run == r].groupby("country").Inappropriate.mean() * 100
    print(f"run {r}: MM gap {rr[rr.index.isin(MM)].mean() - rr[~rr.index.isin(MM)].mean():.2f} pp")
R = pd.DataFrame({r: L[L.run == r].groupby("country").Inappropriate.mean() for r in sorted(L.run.unique())})
print("run-to-run correlation of country shares:\n", R.corr().round(2))
for b in (1, 2):
    c = rate[rate.index.isin(L.loc[L.batch == b, "country"].unique())].Inappropriate; m = c.index.isin(MM)
    print(f"batch {b}: MM gap {c[m].mean() - c[~m].mean():.2f} pp")
c = rate[rate.index.isin(L.loc[L.batch == 2, "country"].unique())].Inappropriate; mm2 = list(c.index[c.index.isin(MM)])
obs = c[mm2].mean() - c.drop(mm2).mean(); splits = list(itertools.combinations(c.index, len(mm2)))
print(f"batch 2 alone: one-sided p = {np.mean([c[list(s)].mean() - c.drop(list(s)).mean() >= obs - 1e-12 for s in splits]):.3f} ({len(splits)} splits)")
qs = np.array([COSI[x] for x in rate.index], dtype=object)
stat = lambda q: pd.Series(rate.Inappropriate.values).groupby(q).mean().var()
o = stat(qs); print("COSI quartiles: p =", round((sum(stat(rng.permutation(qs)) >= o - 1e-12 for _ in range(10000)) + 1) / 10001, 3))

# each country vs the other 23: paired t-test over ads, Holm over all tests
A = L.groupby(["ad", "country"])[Y].mean(); out = []
for y in Y:
    g = A[y].unstack()
    for k in g.columns:
        d = (g[k] - g.drop(columns=k).mean(axis=1)).dropna().to_numpy(); out.append((y, k, d.mean() * 100, ttest_1samp(d, 0).pvalue))
C = pd.DataFrame(out, columns=["measure", "country", "diff_pp", "p"]); C["p_holm"] = holm(C.p)
S = C[C.p_holm < 0.05]
print(f"\ncountry vs other 23: {len(S)} of {len(C)} significant; measures {sorted(S.measure.unique())}")
print("stricter:", sorted(S[S.diff_pp > 0].country.unique()), "| more lenient:", sorted(S[S.diff_pp < 0].country.unique()))

# ads cited for romantic/sexual content only by MM personas (any run, no other persona in any run)
L["mm"] = L.country.isin(MM)
rom = L.groupby(["ad", "mm"])["romance/sexual"].sum().unstack(fill_value=0)
ONLY = set(rom[(rom[True] > 0) & (rom[False] == 0)].index)
print(f"\nads cited for romance/sexual content only by MM personas: {len(ONLY)}")

# RQ3: where these ads were served (needs the dataset's impression table)
if len(sys.argv) > 1:
    V = pd.read_csv(sys.argv[1], dtype=str)
    V["ad"] = V.ad_id_clean.str.strip().map(lambda a: hashlib.sha256(a.encode()).hexdigest()[:16])
    V["country"] = V.Country.str.strip().replace({"UAE": "United Arab Emirates"})
    V = V[V.ad.isin(set(L.ad))]; mm_ds = MM & set(V.country)
    served_mm = set(V[V.country.isin(mm_ds)].ad); rest = set(L.ad) - ONLY
    a, c = len(ONLY & served_mm), len(rest & served_mm)
    print(f"MM countries in the impression data: {sorted(mm_ds)}")
    print(f"served in an MM country: {a}/{len(ONLY)} vs {c}/{len(rest)}; Fisher p = {fisher_exact([[a, len(ONLY) - a], [c, len(rest) - c]])[1]:.2g}")
    V["mm"] = V.country.isin(mm_ds); V["g"] = V.ad.isin(ONLY)
    print("share of impressions in MM countries:", (V.groupby("g").mm.mean() * 100).round(0).to_dict())
    cite = L[L.mm & L["romance/sexual"].eq(1)].groupby("ad").country.apply(set)
    own = [x for x in ONLY if set(V[V.ad == x].country) & cite.get(x, set())]
    print("served in a country whose own persona cited them:", len(own))
