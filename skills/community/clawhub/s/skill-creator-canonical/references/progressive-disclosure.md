# Progressive Disclosure

Use this reference when `SKILL.md` is getting long, when a skill supports multiple variants, or when detailed material would distract from the execution path.

## Loading layers
1. Metadata: `name` and `description`.
2. `SKILL.md`: core workflow and navigation.
3. `references/`: detailed material loaded only when needed.
4. `scripts/`: deterministic operations that can run without loading long prose.

## Split rules
- Keep only the core workflow and selection rules in `SKILL.md`.
- Move detailed examples, schemas, and variant-specific guidance into `references/`.
- Move repeated deterministic logic into `scripts/`.
- Keep references one level deep from `SKILL.md`.

## Patterns
### Pattern 1 — Variants
Use one reference file per provider, framework, or domain.
Example: `references/aws.md`, `references/gcp.md`, `references/azure.md`.

### Pattern 2 — Deep features
Keep the simple path in `SKILL.md`.
Move advanced details to a focused reference file.

### Pattern 3 — Large examples
Keep one short example in `SKILL.md`.
Move long examples to `references/`.

## Navigation rule
Whenever a reference is important, link it from `SKILL.md` with:
`Read [filename] when [condition]. Purpose: [verb + noun].`
