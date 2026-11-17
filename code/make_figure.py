"""Figure 1: share labelled Inappropriate and share citing romance, sex or clothing per country (three runs pooled)."""
import json, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
RXR = r"romant|sexual|kiss|intimate|suggestive|sensual"; RXC = r"cloth|revealing|skin|bikini|swim|lingerie|dress|attire|modest"
L = pd.read_csv("data/labels.csv"); c = L.concerns.apply(lambda s: " ".join(json.loads(s)).lower())
L["inap"] = L.label.eq("Inappropriate"); L["mod"] = c.str.contains(RXR) | c.str.contains(RXC)
D = (L.groupby(["country", "muslim_majority"])[["inap", "mod"]].mean() * 100).reset_index().sort_values("inap").reset_index(drop=True)
BLUE, ORANGE, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#1f1f1f", "#6b6b6b", "#e2e2de"
plt.rcParams.update({"font.family": "serif", "font.size": 7, "axes.linewidth": 0.6, "axes.edgecolor": MUTED})
fig, (a1, a2) = plt.subplots(1, 2, figsize=(3.33, 2.6), sharey=True)
for ax, col in [(a1, "inap"), (a2, "mod")]:
    for i, r in D.iterrows():
        ax.scatter(r[col], i, s=15, marker="^" if r.muslim_majority else "o", color=ORANGE if r.muslim_majority else BLUE, zorder=3)
    ax.grid(axis="x", color=GRID, lw=0.5); ax.set_axisbelow(True)
    for sp in ["top", "right"]: ax.spines[sp].set_visible(False)
a1.set_yticks(range(len(D))); a1.set_yticklabels(D.country.replace({"United Arab Emirates": "UAE", "United States": "US"}))
for t, m in zip(a1.get_yticklabels(), D.muslim_majority): t.set_color(ORANGE if m else INK)
a1.set_xlabel("% labelled inappropriate"); a2.set_xlabel("% citing romance, sex\nor clothing"); a2.set_xlim(3, 16.5)
leg = a2.legend(handles=[Line2D([], [], marker="^", ls="", color=ORANGE, ms=4, label="Muslim-majority"),
                         Line2D([], [], marker="o", ls="", color=BLUE, ms=4, label="other countries")],
                loc="lower right", fontsize=6.2, frameon=True, fancybox=False, edgecolor=MUTED, bbox_to_anchor=(1.08, 0.04))
fig.tight_layout(pad=0.3); fig.savefig("figures/fig_countries.pdf", bbox_inches="tight", pad_inches=0.02)
