---
name: tiktok-to-mealie
description: Extract recipe information from TikTok links, reconstruct a clean recipe, localize it to the user's language when needed, and import it into Mealie. Use when a user sends a TikTok recipe link, asks to convert TikTok cooking content into a structured recipe, or wants a TikTok recipe turned into a usable Mealie entry.
---

# TikTok to Mealie

Use this skill when the user wants to turn TikTok cooking content into a real recipe.

Read as needed:
- `references/workflow.md` for the full extraction/import flow
- `references/mealie-api-notes.md` for Mealie-side behavior
- `references/localization.md` for translation/localization rules
- `references/failure-modes.md` for when to stop instead of importing junk
- `references/output-templates.md` for minimal reply behavior
- `references/configuration.md` for Mealie URL/token configuration

## Core behavior

- Treat TikTok recipe extraction as reconstruction, not perfect scraping.
- Prefer a clean, usable recipe over a literal but messy transcription.
- Prefer execution over commentary when the user clearly wants import.
- Keep user-facing output short.
- If quality is too weak, fail cleanly instead of polluting Mealie.

## Trigger patterns

Use this skill when the user:
- sends a TikTok recipe link
- asks to import a TikTok recipe into Mealie
- asks to convert a short-form cooking video into a structured recipe
- wants recipe extraction from TikTok cooking content

If a message is only a TikTok cooking link and the surrounding context suggests recipe import, treat it as an execution request.

## Default flow

1. Resolve the final TikTok URL.
2. Extract as much useful text as possible from description, metadata, and visible structured clues.
3. Reconstruct:
   - title
   - description
   - ingredients
   - steps
   - times if reasonably inferable
   - servings if reasonably inferable
   - category/tags if useful
4. Recover a cover image if available.
5. Localize the recipe to the user's language if needed.
6. Check import quality threshold.
7. If good enough, create the recipe in Mealie.
8. Upload image if available.
9. Verify the created recipe before returning the final link.

## Quality rules

- Do not import vague junk just because a TikTok link exists.
- Normalize ingredients and steps into an actually cookable recipe.
- If some quantities are missing, use reasonable uncertainty wording instead of fake precision.
- Prefer a coherent recipe with a few explicit assumptions over a broken half-parse.
- If the user language is clear, localize the final recipe consistently.
- Do not keep title, ingredients, and steps in mixed languages unless the user wants that.

## Import threshold

Import only if:
- the title is coherent
- the ingredient list is reasonably usable
- the instruction list is reasonably usable
- the result is more reconstruction than guesswork

If these are not true, stop and explain briefly.

## Mealie behavior

Before import, make sure a Mealie base URL and API token are configured. See `references/configuration.md`.

- Prefer structured recipe creation endpoints when available.
- Add source URL when possible.
- Upload cover image when available.
- Verify final recipe state before replying.
- Return the final recipe link on success.
- Do not assume user-specific hostnames, domains, or secret paths.

## Output behavior

Use the minimal templates in `references/output-templates.md`.

Default rule:
- success -> return the recipe link
- weak extraction -> return a short failure reason
- partial but salvageable extraction -> ask one short confirmation question only if necessary

## Style

- practical
- concise
- execution-focused
- avoid overexplaining
- optimize for a recipe someone can actually cook
