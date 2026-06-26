# Commercial Voice A/B Patterns

## Why this skill has real commercial value

Most teams test spoken ads badly:

- they change the script and the voice at the same time
- they compare assets with very different lengths
- they cannot tell whether the win came from copy or voice

This skill fixes that by holding the voice constant and varying only the copy angle.

## Strong use cases

### Short-video hook testing

Keep the same voice and test:

- trust-first
- benefit-first
- urgency-first
- concise-direct

### Private-domain voice-note conversion

For Feishu, WeChat, or sales follow-up:

- one soft recommendation version
- one stronger CTA version
- one warmer relationship version

### Regional wording experiments

This skill supports wording styles such as:

- `neutral`
- `north_direct`
- `south_gentle`
- `taiwan_soft`

Important:
- this is wording adaptation, not guaranteed dialect voice synthesis
- it is still commercially useful because many campaigns only need a regional “feel”

### Same-person voice, multiple copy variants

If you have a cloned voice or exclusive brand voice, pass the same cloned `voice_id` into batch synthesis.

That makes the comparison much cleaner:

- one voice
- many scripts
- faster screening

## Recommended evaluation dimensions

- first 3-second hook strength
- clarity of benefit
- CTA sharpness
- warmth vs pressure
- whether the audience feels “this is speaking to me”

## Suggested production loop

1. Build 4 to 8 variants from one brief
2. Use one fixed voice
3. Screen internally
4. Launch 2 to 3 finalists
5. Track:
   - play rate
   - completion rate
   - click-through
   - conversion
