# Install yanbaoke Skill

Follow these steps to install the yanbaoke skill for yourself. After installation, you will be able to search and download research reports from pc.yanbaoke.cn — giving you access to millions of industry reports from 5000+ institutions.

## Prerequisites

You need Node.js 18+ (already present if OpenClaw is installed).

**Search is free** - No API Key required for searching reports.

**Download requires API Key** - If you want to download reports, you need a valid `YANBAOKE_API_KEY`. Obtain one from https://pc.yanbaoke.cn/openclaw

## Steps

### 1. Create directories

```bash
mkdir -p ~/.openclaw/skills/yanbaoke/scripts
```

### 2. Download skill definition

```bash
curl -fSL https://app.quzili.cn/skills/yanbaoke/SKILL.md -o ~/.openclaw/skills/yanbaoke/SKILL.md
```

### 3. Download tool scripts

```bash
curl -fSL https://app.quzili.cn/skills/yanbaoke/scripts/search.mjs -o ~/.openclaw/skills/yanbaoke/scripts/search.mjs
curl -fSL https://app.quzili.cn/skills/yanbaoke/scripts/download.mjs -o ~/.openclaw/skills/yanbaoke/scripts/download.mjs
```

### 4. Set YANBAOKE_API_KEY (Optional - for downloads only)

If you want to download reports, write the key to `~/.bashrc` (or `~/.zshrc` if the user's shell is zsh) so it persists across sessions. Replace `<YOUR_API_KEY>` with the actual key from https://pc.yanbaoke.cn/openclaw

```bash
echo 'export YANBAOKE_API_KEY="<YOUR_API_KEY>"' >> ~/.bashrc
source ~/.bashrc
```

**Skip this step if you only need search functionality.**

### 5. Verify

Run all checks below. Every line must pass.

```bash
test -f ~/.openclaw/skills/yanbaoke/SKILL.md && echo "SKILL.md OK" || echo "SKILL.md MISSING"
test -f ~/.openclaw/skills/yanbaoke/scripts/search.mjs && echo "search.mjs OK" || echo "search.mjs MISSING"
test -f ~/.openclaw/skills/yanbaoke/scripts/download.mjs && echo "download.mjs OK" || echo "download.mjs MISSING"
node ~/.openclaw/skills/yanbaoke/scripts/search.mjs "人工智能" -n 3
```

The search command should return a list of research reports. If all checks pass, the installation is complete — you now have the yanbaoke skill and can search/download reports as described in SKILL.md.
