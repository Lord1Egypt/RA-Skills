# Design principles

These are practitioner heuristics for legibility and clarity. They are not measured guarantees of CTR; no numbers here are statistics. Test on the user's own audience.

## The one-second test

At feed size (about 360 px wide) and mobile size (about 170 px) a viewer should get: the subject, the emotion, and the hook in one second. If you must explain it, simplify. `thumb_check.py --preview` renders both sizes on dark and light backgrounds.

## Composition

- One focal point. One main subject (face, object or scene), not three.
- Rule of thirds: subject on one third, text on the other. Leave breathing room around text.
- Large subject, tight crop. Faces and objects should fill a large share of the frame; small details vanish at feed size.
- Keep the bottom-right corner clear: the duration badge covers it. Keep about 3% margin from every edge.
- Directional cues (a gaze, arrow, pointing hand) should lead to the subject or the text, not off the canvas.
- Separate subject from background: outline, rim light, blur or darkening. A thin white outline plus shadow is a safe default for cutouts.

## Text

- 1 to 4 words, often 3 or fewer. Add what the title does not say (a number, a contrast, a reaction); do not repeat the title.
- Heavy condensed sans-serif (Anton, Impact, Bebas, Montserrat Black), uppercase, thick dark stroke, slight shadow. Highlight one word with an accent colour.
- Two lines at most; line breaks at natural phrases.
- Text must read at 170 px width. `thumb_check.py` warns when the rendered height at feed size is too small.
- Avoid small subtitles, URLs and sentences.

## Colour

- High contrast between subject, background and text. Check luminance contrast, not just hue.
- Saturated accent against a calmer base works well: one dominant colour, one accent, black/white for text.
- Common associations (loose, culture-dependent): red for urgency or warning, yellow for attention, green for money or growth or "good", blue for trust or calm or tech, orange for energy, purple for premium or mystery. Choose for the video's mood, and keep the palette consistent with the brand.
- Look at what the niche already uses and either fit in clearly or stand out deliberately; dark thumbnails vanish on dark theme, pale ones on white.
- Colour-blind safety: do not rely on red vs green alone.

## Faces and emotion

- Expressions that match the video's feeling (surprise, concern, joy, disbelief) read faster than neutral ones. The expression must be honest to the content.
- Eyes sharp and visible; a face large enough that the expression survives at 170 px.
- Use the creator's own photos. Shoot expressions in advance: neutral, shocked, laughing, worried, pointing. Light from the front or the side, not flat.
- Not every video needs a face. Objects, before/after, diagrams, maps or a single striking scene often work better for tutorials, finance, history or tech.

## Concept families (use different ones across the 3 to 5 concepts)

1. **Face + reaction + 2-word text.** Best for personal, opinion, reaction, story.
2. **Object hero.** One large object with a number or a label, plain background. Best for products, tools, tests.
3. **Contrast / before-after.** Split frame or two states, with an arrow or a "vs". Best for comparisons and transformations. Must be real.
4. **Curiosity gap.** A striking image of the unexplained thing (blurred, circled, partly hidden), little text. Must pay off in the video.
5. **Bold text-led.** Large 2 to 3 word statement on a strong colour field with one icon. Best for lists, tips, explainers.

## Shorts covers

Shorts covers are 9:16. YouTube's help says Shorts thumbnails can only be added in YouTube Studio on a computer. Keep text in the middle band, away from the interface overlay at the bottom and right. In the feed a Short is mostly shown as its video, so treat the cover as secondary and keep it simple. A 16:9 custom thumbnail on a vertical video is replaced by an auto-generated 4:5 crop on some surfaces (per YouTube Help).

## Brand consistency

Keep 1 to 2 fonts, 2 to 3 colours, one outline/shadow style, consistent subject position and a small logo or colour band across a series, so viewers recognise the channel, while the subject and text change per video. Do not make every thumbnail identical: viewers still need a reason to click each one.

## Testing

- If YouTube Studio offers a thumbnail test feature to the user's channel, use it (not verified in this session; check Studio). Otherwise compare after publishing: change one thing at a time, wait for enough impressions, compare click-through rate and also watch time (a misleading thumbnail raises clicks and hurts retention).
- Judge a winner by a margin that is bigger than normal day-to-day variation; small differences on small numbers are noise.
- Keep a log of concept, text, colour and result to learn what works for this channel.

## Common mistakes

Too much text; text copied from the title; small subject; busy background; low contrast; a face with a neutral expression and a clickbait promise the video does not keep; important content under the duration badge; stretched or soft low-resolution photos; AI text with typos; inconsistent edges after background removal; a design that works only on one theme.
