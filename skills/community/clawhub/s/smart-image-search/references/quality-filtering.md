# Quality filtering

Filter weak images before final sending.

## Reject hard
Reject when any of these are true:
- obvious site asset or logo
- very small file size
- tiny dimensions
- content-type is not an image
- repeated duplicate of an already selected image

## Soft penalties
Lower confidence or score when:
- URL contains `thumb`, `thumbnail`, `sprite`, `icon`, `logo`
- dimensions are small-ish but still usable
- source looks like a noisy gallery page

## Practical thresholds
Use these as default heuristics:
- minimum width: 220
- minimum height: 220
- minimum file size: 12 KB
- square-ish images are acceptable for avatar intent
- wider images are preferred for wallpaper intent

## Intent-aware quality
- `wallpaper`: prefer larger images, penalize small or square crops
- `avatar`: square is okay
- `meme`: allow lower quality if semantic match is strong, but still reject obvious site assets
- `official` / `portrait`: prefer cleaner medium-to-large images
