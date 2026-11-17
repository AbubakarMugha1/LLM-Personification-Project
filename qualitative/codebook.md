# Qualitative review: codebook and procedure

## Sample
The 11 ads that, in the first run, were cited for romantic or sexual content by at least three Muslim-majority (MM)
personas and by no other persona (`reviewed_ads.csv`; row numbers match Table 2 of the paper).
- **B units:** the 49 first-run rationales in which an MM persona labelled one of these ads Inappropriate.
- **C units:** the 143 rationales of the 13 other personas for the same ads (13 × 11), all labelled Irrelevant.

The codebook below was derived from a thematic reading of all rationales for these ads.

## Codes
Coding units: A and D per ad; B per MM rationale that flags the ad; C per other persona's rationale.

**A. Ad content** (coded from the video before reading any model output)
- A-format: music video / product ad / other
- A-content (any that apply): A1 revealing clothing; A2 posing, dancing or camera focused on the body; A3 kissing or
  intimate contact; A4 nightlife or party setting; A5 romantic theme only (lyrics or story); A6 none of these
- A-intensity: mild (outfits common in mainstream media) / moderate (repeated emphasis on the body) / strong
  (near-nudity or sexual activity)

**B. MM rationale that flags the ad**
- B-focus (any): B1 clothing or exposure; B2 body-focused posing, dancing or camera; B3 kissing or intimacy;
  B4 adult setting (nightlife, party); B5 the romantic theme itself
- B-frame (any): B6 sexualising terms; B7 audience mismatch ("adult-oriented"); B8 names the country or its culture;
  B9 religion
- B-accuracy (one, judged against A): accurate / overstated / misdescribed

**C. Other persona's rationale**
- C-mention (one, judged against A): C1 names the content and accepts it ("revealing but non-explicit");
  C2 describes it in neutral terms ("fashionable", "glamorous"); C3 does not mention it
- C4 (yes/no): uses explicitness as the threshold (e.g. "no explicit content", "not overtly sexual", "no nudity")

**D. Guidelines (per ad):** D1 the category in YouTube's Made for Kids ad guidelines that names this content
(romantic content / significant skin exposure / adult or sexually suggestive / none / unsure)

## Procedure
1. Watch each ad (twice, with sound) and code A before reading any rationale.
2. Code B for the MM rationales, then C for the other personas' rationales.
3. Memo anything that does not fit; a new code is added only if it applies to at least two ads, and then all ads are
   re-checked.

`codes.csv` holds every code (one row per ad, B rationale or C rationale); `unit = C_mm_not_flagged` rows are an
optional comparison set that was not coded.
