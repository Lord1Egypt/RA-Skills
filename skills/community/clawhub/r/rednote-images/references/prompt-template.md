# Prompt Template

Build the prompt card by card:

```markdown
[one-sentence topic for this card]

Create a RedNote image card about: <card topic>.
Series role: <cover | content | ending>.
Target audience: <target audience>.

Layout: <layout>.
Visual focus: <main visual focus for this card>.
Aspect ratio: <aspect>.

Style direction: <style>.
Language: <zh|en|ja|ko>.

Series reference:
- reference image: <references/series-reference.png | none>
- priority rule: treat the series reference as the canonical source of truth for palette, recurring subject, typography feel, and layout rhythm

Series anchors:
- overall palette: <shared palette>
- recurring subject / mascot / product: <shared recurring subject>
- layout rhythm: <shared framing, spacing, and card structure>

Card continuity:
- previous card recap: <what the previous card established>
- current transition: <how this card continues the same series>
- next card hook: <what should naturally carry into the next card>

Key points to show:
- <point 1>
- <point 2>
- <point 3>

Text treatment: <none | title-only | text-rich>.
If text is used, keep it bold, sparse, readable, and native to the target language.

Avoid: cluttered layout, too many tiny words, unreadable typography, weak hierarchy, watermark, distorted anatomy.
```

Additional rules:

- A cover card should prioritize the hook and main theme instead of packing in too much information.
- Each content card should usually carry only 1 to 3 main points.
- If image text is required, explicitly state `Language: <zh|en|ja|ko>`.
- If the user provides a title, add a line such as `Title to place: "<title>"`.
- Prefer the reference-first strategy by default: create one canonical series reference first, then reuse it for every card.
