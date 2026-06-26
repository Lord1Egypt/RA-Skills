# Publishing windows-tts to ClawHub

This document guides you through publishing the windows-tts skill to ClawHub registry.

## Prerequisites

- ✅ ClawHub CLI installed (`clawhub --version`)
- ✅ ClawHub account and API token
- ✅ Skill folder with all required files
- ✅ Built distribution in `dist/` folder

## Pre-Publish Checklist

### Required Files
- [x] `SKILL.md` - Main documentation with frontmatter
- [x] `package.json` - NPM package metadata
- [x] `tsconfig.json` - TypeScript configuration
- [x] `index.ts` - Skill entry point
- [x] `openclaw.plugin.json` - OpenClaw plugin manifest
- [x] `dist/` - Compiled JavaScript output
- [x] `_meta.json` - ClawHub metadata
- [x] `.clawhub/origin.json` - Registry configuration
- [x] `CHANGELOG.md` - Version history
- [x] `README.md` - Usage examples

### Quality Checks
- [x] TypeScript compiles without errors
- [x] All tools tested and working
- [x] Documentation complete and accurate
- [x] No hardcoded secrets or credentials
- [x] Version follows semver (1.0.0)

## Publish Steps

### Step 1: Login to ClawHub

```bash
# Browser-based login (recommended)
clawhub login

# Or with token directly
clawhub login --token YOUR_API_TOKEN --label "windows-tts-publish"
```

### Step 2: Verify Login

```bash
clawhub whoami
```

Expected output:
```
✓ Authenticated as: your-handle
  User ID: your-user-id
```

### Step 3: Dry Run (Optional)

```bash
# Check skill metadata without publishing
clawhub inspect windows-tts --path ./skills/windows-tts
```

### Step 4: Publish

```bash
# Navigate to skills directory
cd /home/cmos/skills

# Publish the skill
clawhub publish windows-tts \
  --slug windows-tts \
  --name "Windows TTS Notification" \
  --version 1.0.0 \
  --tags "latest,tts,notification,windows,azure,broadcast,reminder" \
  --changelog "Initial release: Cross-device TTS broadcast for OpenClaw"
```

### Step 5: Verify Publication

```bash
# Search for your skill
clawhub search windows-tts

# Or inspect directly
clawhub inspect windows-tts
```

### Step 6: Update Local Installation

```bash
# Update the skill in OpenClaw
clawhub update windows-tts
```

## Post-Publish Actions

### 1. Share Announcement

Share your skill with the community:
- OpenClaw Discord/Telegram channels
- GitHub discussions
- Social media

### 2. Monitor Usage

Check your skill's performance:
```bash
clawhub list
```

### 3. Gather Feedback

- Monitor issues and feature requests
- Update documentation based on user feedback
- Plan next version improvements

## Troubleshooting

### Error: "Slug already taken"

The skill slug `windows-tts` is already registered. Choose a unique slug:

```bash
clawhub publish windows-tts \
  --slug windows-tts-broadcast \
  --name "Windows TTS Broadcast"
```

### Error: "Missing required files"

Ensure all required files are present:
```bash
ls -la skills/windows-tts/
```

Required: `SKILL.md`, `package.json`, `dist/`, `index.ts`

### Error: "TypeScript compilation failed"

Rebuild the skill:
```bash
cd skills/windows-tts
npm run build
```

### Error: "Authentication required"

Login again:
```bash
clawhub login
```

## Version Updates

For future updates:

```bash
# 1. Update version in package.json and _meta.json
# 2. Update CHANGELOG.md
# 3. Rebuild
npm run build

# 4. Publish new version
clawhub publish windows-tts \
  --version 1.0.1 \
  --changelog "Bug fixes and performance improvements"
```

## Best Practices

### 1. Semantic Versioning
- `MAJOR.MINOR.PATCH`
- Breaking changes → increment MAJOR
- New features → increment MINOR
- Bug fixes → increment PATCH

### 2. Changelog Updates
Always update `CHANGELOG.md` before publishing:
```markdown
## [1.0.1] - 2026-03-16

### Fixed
- Fixed timeout issue with slow networks

### Changed
- Updated default volume to 0.8
```

### 3. Documentation
- Keep SKILL.md up to date
- Include usage examples
- Document breaking changes
- Add troubleshooting section

### 4. Testing
- Test with different TTS servers
- Verify error handling
- Test edge cases (empty text, invalid URLs)
- Check network timeout scenarios

## Support

For help with ClawHub publishing:
- Documentation: https://clawhub.ai/docs
- Community: OpenClaw Discord
- Issues: GitHub repository

## License

MIT License - See LICENSE file for details
