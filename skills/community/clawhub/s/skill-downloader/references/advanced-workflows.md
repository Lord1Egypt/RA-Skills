# Advanced Workflows

Use this reference only when implementing or reviewing the detailed workflow. Keep the main `SKILL.md` focused on policy and high-level process.

## Trusted sources

Primary sources:
- ClawHub
- GitHub `anthropics/skills`
- skills.sh

## Preferred workflow

1. Search trusted sources
2. Inspect the selected candidate
3. Disclose information completeness
4. Ask for explicit approval before installation or update
5. Review downloaded source material before writing files
6. Install into the user-requested target directory
7. Preserve unrelated user data during updates

## Notes for implementation

- Prefer official registry tooling when available
- Use a temporary review location for fallback file-based workflows
- Avoid symlinks for installed skill contents
- Keep update workflows conservative and preserve existing user data
- Treat rate limits and missing metadata as partial-information situations

## Source-specific details

### ClawHub
Use the official inspect/install/update workflow when available.

### GitHub
Use repository metadata and raw file access for inspection when needed.

### skills.sh
Use it for discovery; when installation requires more control, follow the review-first fallback workflow.
