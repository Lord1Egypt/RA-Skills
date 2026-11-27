# Text pack
Layer 1:
- `scripts/ai_tone_lint.py` for lexical tells (zh: 不是…而是…, 值得注意的是, 总而言之, 在…的今天, 赋能/助力/打造, 三连排比, 破折号/粗体密度; en: Wikipedia "Signs of AI writing": delve, tapestry, testament, not X but Y, em-dash density, bold labels, chat leftovers). Vale rules can replace this when a style guide exists.
- Facts: extract every number, date, proper noun, quote. Each cited URL must open; each number/period in a "verified" claim must appear in the quoted source text, else mark UNVERIFIED.
- Rewrite fidelity: `scripts/claims_diff.py before after`; any lost or changed claim is a blocker.
Judge dimensions:
- Structural AI tone (lint tools miss this; independent tests show humanizer skills leave it intact): every section ends in a lesson, tidy closing line, uniform paragraph length/shape, no concrete detail or first-hand judgement.
- Audience fit: answers the actual question, tone matches reader, no filler.
- Source quality (L3): two independent sources per key claim; check retractions and attribution.
