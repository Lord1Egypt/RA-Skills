# rules

## P0 lint categories

### duplicates
Flag when multiple core context files express the same stable rule, preference, or boundary with only minor wording changes.

### overweight
Flag when a file or section looks too procedural, too long, or too detailed for always-loaded context.

### misplaced
Flag when content appears in the wrong core file role, such as environment-specific details outside `TOOLS.md` or temporary facts inside `MEMORY.md`.

## Severity guidance
- high: likely to create execution ambiguity or long-term drift
- medium: increases maintenance cost or context weight noticeably
- low: cleanup opportunity with limited short-term impact

## First-version limits
- Do not auto-edit files.
- Do not attempt deep semantic clustering.
- Focus on core files first; treat memory expansion as optional.
