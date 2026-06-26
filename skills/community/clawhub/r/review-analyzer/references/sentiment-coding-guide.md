# Sentiment Coding Guide

The goal of coding is *reproducibility*: a second analyst given the same review should land on the same label and aspects. Code from the **text**, not the star rating, and write down your decisions so the next run is comparable.

## Overall vs aspect-based sentiment

- **Overall sentiment** is the reviewer's net attitude toward the product. Use it for the rating-distribution sanity check and to catch star-vs-text mismatches.
- **Aspect-based sentiment** is the attitude toward a *specific feature* (zipper, sizing, battery, shipping). This is what drives the action list, because "people are mildly happy overall" tells you nothing actionable, but "55% negative on zippers, worsening" does.
- A single review usually carries **multiple aspect labels with different polarities**: "Love the fabric (positive: quality) but it runs two sizes small (negative: sizing)." Code each aspect separately. Never collapse a multi-aspect review into one label.

## The 4-label rubric

Apply per aspect (and once overall):

- **Positive** — clear approval, no material reservation. *"Battery lasts all day, exactly as described."*
- **Negative** — clear dissatisfaction or a defect. *"Stopped charging after two weeks."*
- **Neutral** — factual, no evaluative charge, or a question. *"Comes in a brown box. Cable is USB-C."*
- **Mixed** — genuine positive AND negative about the same aspect, or balanced overall. *"Sound is great for the price but the bass rattles at high volume."*

Decision rules:
- If approval is hedged by a real reservation, it's **mixed**, not positive. *"Great little lamp, just wish the cord were longer"* = mixed (and a feature request).
- A complaint about something outside your control (slow third-party courier, buyer ordered the wrong size on purpose) is still coded by content but **tagged out-of-scope** so it doesn't pollute product/copy routing.
- Recommendation intent ("would buy again," "returning it") is a strong tiebreaker between positive and negative.

## Handling sarcasm

Sarcasm flips surface polarity. Cues: exaggerated praise next to a failure, scare quotes, "just what I wanted...", emoji eye-rolls, all-caps "GREAT."
- *"Oh fantastic, it broke on day one. Worth every penny."* -> **negative** (quality/durability).
- *"'Waterproof.' Sure."* -> **negative** (accuracy vs listing).
When in doubt, weight the concrete outcome (it broke, it leaked) over the adjective. If genuinely ambiguous, code **mixed** and flag for human review rather than guessing.

## Handling negation

Negation reverses polarity and is the #1 source of automated-coding errors.
- *"Not bad at all"* / *"can't complain"* -> **positive.**
- *"Doesn't fall apart like the cheap ones"* -> **positive** (durability).
- *"Not as durable as I hoped"* -> **negative** (durability).
- Watch double negation and scope: *"no issues with the zipper, but the strap frayed"* = zipper positive, strap negative.
Automated passes should test negation explicitly; always hand-check a sample of "not"/"no"/"never"/"hardly" reviews.

## Handling comparative statements

Comparisons reveal differentiators and competitive weaknesses — capture both the direction and the referent.
- *"Better seal than the BrandX one I returned"* -> quality **positive**; log "switched from BrandX (+)".
- *"Thinner material than my old pair"* -> quality **negative** (and an accuracy signal if photos implied thickness).
- *"Same as the $20 version but costs $40"* -> value **negative.**
- Self-comparisons over time matter: *"my second unit is flimsier than the first"* is a strong **worsening-trend / supplier-change** signal — note the purchase date.

## Star-rating vs text mismatch

Mismatches are signal, not noise.
1. When stars and text disagree, **recode to the text** for sentiment.
2. **Log every mismatch** and report the overall mismatch rate.
3. Common patterns and what they mean:
   - **High stars, negative text** ("5 stars but it arrived cracked") — often habit/politeness or a review left before a problem appeared. Inflates your rating; a real defect is hiding.
   - **Low stars, positive text** ("love it!! ⭐") — usually a mis-click or a shipping/seller gripe unrelated to the product; verify before treating as a product negative.
   - **3-star reviews** are the richest: their text is almost always more negative than the star implies. Read them closely.

## Incentivized / fake review red flags

Flag, quantify, exclude from sentiment math, and report separately — do not silently delete.

- **Burst timing:** a cluster of 5-star reviews posted on the same day or within hours, especially right after launch or a rating dip.
- **Generic template language:** "Great product, fast shipping, highly recommend!!" with no product-specific detail, repeated near-verbatim across reviewers.
- **Incentive disclosure:** "received free/discounted in exchange for my honest review," gift-card mentions, "the seller asked me to..."
- **Reviewer pattern:** brand-new accounts, reviewers who post dozens of 5-stars across unrelated products the same week.
- **Mismatched specifics:** describes a different color/model than purchased, or praises a feature the product lacks.
- **Off-platform tells:** identical photos across listings, or text referencing a different product name.
Report the flagged rate; a sudden spike often coincides with — and masks — a real product problem.

## Inter-rater consistency tips

- **Write a codebook** with one anchor example per label per aspect before coding; update it when you hit a new edge case.
- **Calibrate first:** two coders independently code the same 20-30 reviews, compare, and reconcile rules before doing the full set.
- **Spot-check automation:** hand-verify a random 10-15% sample of any automated coding; if disagreement exceeds ~10%, tighten the rubric and re-run.
- **One aspect taxonomy:** lock the aspect list (use the pain-point taxonomy) so coders tag consistently.
- **Log ambiguous cases** with the decision made, so the same call is reused next time.
- **Code blind to the star** when feasible — reveal the star only at the mismatch-logging step — to avoid anchoring on it.
