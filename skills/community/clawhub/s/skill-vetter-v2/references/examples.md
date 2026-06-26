# Examples

## Example verdict: safe

A formatting skill that only reads local markdown files and rewrites output style.

- install risk: low
- runtime risk: low
- trust dependency: none
- verdict: safe

## Example verdict: caution

A deployment helper that writes config files, installs a package, and calls a documented API.

- install risk: medium
- runtime risk: medium
- trust dependency: transparent
- verdict: caution

## Example verdict: unsafe

A skill that requests credentials, reads memory files without explanation, and sends prompts to an opaque external service.

- install risk: high
- runtime risk: extreme
- trust dependency: opaque
- verdict: unsafe

## Verification example

After local review, define a deterministic verification spec such as:
- all required report fields present
- verdict supported by listed warnings
- prohibited data absent

Only verify the structured report payload.
