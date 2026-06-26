# YumFu v1.7.6 - Scene-Bound Storybook HTML 📖

## What changed

This release improves YumFu storybook delivery rules based on live user feedback during a Telegram group play session.

### ✅ Storybook format rules clarified
- HTML is now the **canonical** storybook export format
- PDF is now treated as **secondary** and should only be shipped when the layout is visually confirmed acceptable
- Storybooks must use **scene-bound layout**:
  - one image
  - the matching scene/dialogue text directly attached to that image block
- Avoid detached image galleries with separate prose dumps

### ✅ Skill guidance updated
- Added explicit scene-binding rules into `SKILL.md`
- Updated storybook generation instructions to prefer HTML-first delivery
- Clarified that chat-delivered storybooks should optimize for readability, not print-first layout

## Why this release

User feedback was clear: the HTML storybook worked, but the PDF layout did not, and the text should stay embedded with the image paragraph/scene instead of being separated.

This release bakes that preference directly into YumFu so future exports default to the better format.

## Result

Future YumFu storybooks should now:
- read more like an illustrated book / visual novel
- preserve image-text pairing per scene
- avoid splitting art and narration into different sections
