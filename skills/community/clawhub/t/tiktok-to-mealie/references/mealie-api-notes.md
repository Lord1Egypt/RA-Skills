# Mealie API notes

Use these as implementation hints, not hardcoded assumptions.

## Typical useful endpoints
- recipe creation endpoint
- recipe update endpoint
- recipe image upload endpoint
- recipe fetch endpoint for verification

## Preferred pattern
1. Create recipe from structured HTML/JSON recipe data when supported.
2. Fetch created recipe.
3. Upload image if available.
4. Re-fetch if needed to verify state.

## Verification checklist
- slug exists
- title is correct
- ingredient list is not empty
- instruction list is not empty

## Response rule
If the workflow succeeds, return the final recipe link.
If the workflow fails, return a short reason.
