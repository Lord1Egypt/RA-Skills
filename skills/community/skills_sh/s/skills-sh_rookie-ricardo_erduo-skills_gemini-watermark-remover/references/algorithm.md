# Gemini watermark removal algorithm

## Reverse alpha blending

Gemini visible watermark uses alpha compositing:

watermarked = α * logo + (1 - α) * original

Solve for original:

original = (watermarked - α * logo) / (1 - α)

Logo value is white (255). Alpha values come from pre-captured watermark maps.

## Alpha map construction

Compute alpha per pixel by taking the max RGB channel of the captured watermark image
and normalizing to [0, 1].

## Detection rules

If image width > 1024 AND height > 1024:
- logo size: 96x96
- margin right: 64px
- margin bottom: 64px

Otherwise:
- logo size: 48x48
- margin right: 32px
- margin bottom: 32px

## Limits

- Only removes the visible Gemini watermark in the bottom-right corner.
- Does not remove invisible/steganographic watermarks.
- Works on images that match the current watermark pattern.
