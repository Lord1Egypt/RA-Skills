# Workflow

## Goal
Convert a TikTok cooking link into a structured recipe that is actually usable and worth storing.

## Extraction order
1. Resolve the final TikTok URL.
2. Extract description text.
3. Look for recipe clues in page metadata.
4. Look for cover image / preview image.
5. Use any structured text that can help reconstruct ingredients or steps.

## Reconstruction fields
Build these when possible:
- title
- description
- ingredients
- instructions
- prep/cook/total time if inferable
- servings if inferable
- category/tags

## Reconstruction rules
- Keep the recipe cookable.
- Avoid fake precision.
- If some fields are uncertain, keep the wording usable and honest.
- Prefer natural cooking language over literal noisy extraction.

## Import threshold
Import only if:
- the title is coherent
- ingredients are reasonably usable
- steps are reasonably usable
- the result is not mostly guesswork

Do not import if the result is mostly guesswork.

## Image handling
If a cover image exists:
- download it
- upload it after recipe creation

If no image exists:
- do not block the recipe import just for that

## Final verification
Before returning the final link, verify:
- the recipe exists
- the title is sane
- the ingredients are not empty
- the instructions are not empty
- the final recipe matches the intended language
