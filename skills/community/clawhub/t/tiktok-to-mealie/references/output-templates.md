# Output templates

## Success
Return only the final recipe link when the user clearly wants execution.

## Weak extraction
Use a short failure message:
- TikTok text too sparse to reconstruct a reliable recipe.
- I could not recover enough ingredients/steps to import something clean.
- The available text is too incomplete, so I stopped before creating junk.

## Confirmation case
Ask for confirmation only if the reconstruction is partial but salvageable.
Use one short question, not a long explanation.

## Recipe quality summary
When a summary is needed, keep it to:
1. title
2. why the reconstruction seems reliable or uncertain
3. next step
