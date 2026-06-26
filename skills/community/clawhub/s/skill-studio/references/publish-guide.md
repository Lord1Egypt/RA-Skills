# Publishing to ClawHub Guide

Step-by-step guide for publishing your skill to ClawHub.

## Prerequisites

### 1. ClawHub Account

Create account at: https://clawhub.ai

### 2. Install ClawHub CLI

```bash
npm install -g clawhub
```

Verify installation:
```bash
clawhub --version
```

### 3. Login

**Desktop (with browser):**
```bash
clawhub login
```
This opens browser for GitHub OAuth.

**Server/Headless (token-based):**
1. Go to https://clawhub.ai/settings/tokens
2. Generate new token
3. Use: `clawhub auth login --token YOUR_TOKEN`

## Publishing Steps

### Step 1: Validate Your Skill

```bash
cd /path/to/your-skill
# Run validation (skill-studio does this automatically)
```

### Step 2: Publish

```bash
clawhub publish /path/to/your-skill \
  --slug your-skill-name \
  --version 1.0.0 \
  --changelog "Initial release: Brief description"
```

### Step 3: Verify

```bash
clawhub inspect your-skill-name
```

Your skill should appear at: `https://clawhub.ai/@your-username/your-skill-name`

## Version Updates

When updating your skill:

```bash
# Patch version (bug fixes)
clawhub publish . --slug skill-name --version 1.0.1 --changelog "Fix bug..."

# Minor version (new features)
clawhub publish . --slug skill-name --version 1.1.0 --changelog "Add feature..."

# Major version (breaking changes)
clawhub publish . --slug skill-name --version 2.0.0 --changelog "Major rewrite..."
```

## Security Scan

After publishing, ClawHub runs automatic security scan:

- **VirusTotal** - File scanning
- **OpenClaw** - Metadata validation

If flagged:
1. Check the scan report
2. Fix any issues
3. Publish new version

## Common Issues

### "Version already exists"

You need to bump the version number:
```bash
clawhub publish . --slug skill-name --version 1.0.1 ...
```

### "Not logged in"

```bash
clawhub login
```

### "Skill slug already taken"

Choose a different slug or use your username prefix:
```bash
--slug yourusername-skill-name
```

### Server Environment (No Browser)

Option 1: Use token
```bash
clawhub auth login --token YOUR_TOKEN
```

Option 2: Publish from local machine
1. Copy skill directory to local machine
2. Login and publish from there

## Best Practices

1. **Test locally first** - Ensure skill works before publishing
2. **Clear description** - Helps users find your skill
3. **Semantic versioning** - Use proper version numbers
4. **Changelog** - Describe what changed
5. **Security** - Follow validation rules

## After Publishing

Share your skill:
- Post in OpenClaw Discord
- Tweet with #OpenClaw #ClawHub
- Add to awesome-openclaw-skills list

Your skill URL:
```
https://clawhub.ai/@username/skill-name
```

Install command for users:
```bash
clawhub install skill-name
```
