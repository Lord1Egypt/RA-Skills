# Review Checklist

Use this after coding or polishing a UI.

## Style-fit check
- Does the final UI still match the chosen direction?
- If someone only saw the page, would they describe it with the intended style words?
- Did implementation drift into generic AI UI?

## Layout check
- Is the section order clear and purposeful?
- Is there one strong visual hierarchy?
- Is the page overbuilt with unnecessary sections?

## Component consistency check
- Do buttons feel like the same product?
- Do cards belong to the same visual family?
- Are spacing, radius, borders, and shadows coherent?

## UX check
- Is the main CTA obvious?
- Are interactions understandable without guessing?
- Are text contrast and readability good enough?
- Are focus states visible?
- Does the page still work on mobile widths?

## Motion/effects check
- Are effects helping the page or just showing off?
- Is blur/glass/noise/glow used with restraint?
- Does `prefers-reduced-motion` have a sane fallback when relevant?

## Final judgment
If the answer is “mostly yes” but the page still feels bland, refine:
- typography hierarchy
- CTA prominence
- whitespace rhythm
- token consistency
- one or two signature effects

Do not add random flair if the real problem is weak hierarchy.
