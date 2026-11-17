
**Never publish without completing this process.**

## Create Publish Folder

Work in a SEPARATE folder, never modify originals:
```
/tmp/publish-[slug]/
├── SKILL.md
├── FILES.txt
└── [auxiliaries]
```

## Verification Message

Before publishing, send user a verification with:

### Required Information
- **Slug:** exact slug to use
- **Name:** exact display name
- **Version:** version number
- **Description:** exact description text
- **Files:** complete list of files to publish

### Content Summary
- Brief summary of what the skill does
- Key sections/topics covered
- Any notable inclusions or exclusions

### Sanitization Confirmation
- "Checked for personal data: ✓"
- "Checked for credentials: ✓"
- "Checked for model-specific references: ✓"
- Note any items that were removed/genericized

## Wait for Approval

**Do not proceed without explicit approval.**

User should confirm:
- Slug is correct
- Name is correct
- Description is correct
- Content looks right
- Ready to publish

## Publish Command

Only after approval:
```bash
clawhub publish <folder> \
  --slug "<slug>" \
  --name "<name>" \
  --version "<version>"
```

## Post-Publish Verification

After publishing:
1. Confirm success message
2. Optionally install to verify: `clawhub install <slug> --dir /tmp/verify`
3. Report to user: "Published [slug]@[version]"

## If Something Goes Wrong

- Wrong slug? Use ClawHub Edit page → "Rename slug" (old slugs stay as redirects). Then publish a new version with the corrected content if needed.
- Wrong content? Publish new version with fix.
- Exposed private data? Publish sanitized version ASAP, rename or delete the old listing, contact support if needed.

## Version Guidelines

- `1.0.0` — First publish
- `1.0.1` — Small fixes (typos, clarifications)
- `1.1.0` — New content/features
- `2.0.0` — Major restructure
