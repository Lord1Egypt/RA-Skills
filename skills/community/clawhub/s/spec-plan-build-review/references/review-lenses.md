# Review Lenses

Use these lenses during the review step.

## Code Reviewer

- Does the implementation match the existing architecture?
- Are edge cases handled without broad rewrites?
- Is the public API or CLI behavior stable?

## Test Engineer

- Is the changed behavior covered?
- Are failure modes reproducible?
- Did local and remote checks run against the intended commit?

## Security Reviewer

- Did the change expand permissions, network access, or write scope?
- Could it expose private data or local secrets?
- Are release artifacts and package metadata consistent?

Findings should cite files, commands, or CI runs.
