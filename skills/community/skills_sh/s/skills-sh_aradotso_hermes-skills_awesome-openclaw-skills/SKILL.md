---
name: awesome-openclaw-skills
description: Browse and discover 5,200+ curated OpenClaw agent skills from the official skills registry, organized by category
triggers:
  - "find OpenClaw skills for *"
  - "search ClawHub registry"
  - "what OpenClaw skills are available for *"
  - "show me agent skills for *"
  - "browse OpenClaw skills by category"
  - "install a ClawHub skill"
  - "find skills for my Clawdbot"
  - "search awesome-openclaw-skills"
---

# awesome-openclaw-skills

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

A curated collection of 5,200+ OpenClaw agent skills filtered from the official ClawHub registry (13,729+ total). Skills are categorized by function (Git & GitHub, DevOps, AI & LLMs, Browser Automation, etc.) and vetted to exclude spam, duplicates, and low-quality entries.

## What is OpenClaw?

OpenClaw is a locally-running AI assistant that operates directly on your machine. **Skills** extend its capabilities, allowing it to interact with external services, automate workflows, and perform specialized tasks.

This collection helps you:
- **Discover** skills by category (Git, DevOps, Marketing, etc.)
- **Filter** out spam, duplicates, and malicious skills
- **Install** via ClawHub CLI or manual setup
- **Inspect** security reports via VirusTotal integration

## Installation

### Browse the Collection

Visit the repository to explore categorized skills:

```bash
# Clone the repository
git clone https://github.com/VoltAgent/awesome-openclaw-skills.git
cd awesome-openclaw-skills

# Browse by category in README.md
cat README.md | grep "## Table of Contents" -A 50
```

Or visit online: [clawskills.sh](https://clawskills.sh/)

### Install a Skill

#### Option 1: ClawHub CLI (Recommended)

```bash
# Install the ClawHub CLI
npm install -g @openclaw/clawhub-cli

# Search for a skill
clawhub search "github automation"

# Install by slug
clawhub install steipete/slack

# Install with specific version
clawhub install steipete/slack@1.2.3

# List installed skills
clawhub list

# Update a skill
clawhub update steipete/slack

# Uninstall
clawhub uninstall steipete/slack
```

#### Option 2: Manual Installation

```bash
# 1. Find the skill's GitHub URL from awesome-openclaw-skills
# 2. Clone or download the skill folder
# 3. Copy to one of these locations:

# Global (available to all projects)
mkdir -p ~/.openclaw/skills/
cp -r skill-folder ~/.openclaw/skills/

# Workspace (project-specific)
mkdir -p ./skills/
cp -r skill-folder ./skills/

# Priority: Workspace > Global > Bundled
```

#### Option 3: Paste GitHub Link in Chat

Simply paste the skill's GitHub repository URL into your OpenClaw assistant chat:

```
https://github.com/openclaw/skills/tree/main/skills/steipete/slack
```

The assistant will handle installation automatically.

## Key Categories

The collection is organized into **40+ categories**:

| Category | Count | Examples |
|----------|-------|----------|
| **Coding Agents & IDEs** | 1,184 | Code review, refactoring, IDE automation |
| **Web & Frontend Development** | 919 | React/Vue/Svelte tooling, CSS frameworks |
| **DevOps & Cloud** | 393 | Docker, Kubernetes, AWS, GCP, Terraform |
| **Browser & Automation** | 323 | Playwright, Puppeteer, web scraping |
| **Search & Research** | 345 | arXiv, Google Scholar, academic databases |
| **Productivity & Tasks** | 205 | Task management, note-taking, calendars |
| **AI & LLMs** | 176 | Model providers, RAG, embeddings |
| **Image & Video Generation** | 170 | DALL·E, Midjourney, video editing |
| **Git & GitHub** | 167 | PR automation, CI/CD, code review |
| **Communication** | 146 | Slack, Discord, email, SMS |
| **CLI Utilities** | 180 | File ops, text processing, shell scripts |

**Full list:** See [Table of Contents](#table-of-contents) in README.md

## Usage Patterns

### Finding Skills by Use Case

```bash
# 1. Clone the repo
git clone https://github.com/VoltAgent/awesome-openclaw-skills.git
cd awesome-openclaw-skills

# 2. Search by keyword
grep -i "docker" README.md

# 3. Browse by category
# Navigate to the category heading in README.md
# Each skill includes:
#   - Name and ClawHub URL
#   - One-line description
#   - GitHub source link
```

### Evaluating a Skill Before Install

1. **Check ClawHub page** for VirusTotal report:
   ```
   https://clawskills.sh/skills/<author>/<skill-name>
   ```

2. **Review source code** on GitHub:
   ```
   https://github.com/openclaw/skills/tree/main/skills/<author>/<skill-name>
   ```

3. **Check for:**
   - Recent updates (skill may be abandoned if >1 year old)
   - Security flags in VirusTotal report
   - Permissions requested (file access, network, API keys)
   - Clear documentation and examples

### Example: Installing a GitHub Automation Skill

```bash
# 1. Find skill in awesome-openclaw-skills
# Category: Git & GitHub
# Skill: auto-pr-merger by autogame-17

# 2. Check ClawHub page
open https://clawskills.sh/skills/autogame-17/auto-pr-merger

# 3. Install via CLI
clawhub install autogame-17/auto-pr-merger

# 4. Configure (if needed)
# Most skills use environment variables:
export GITHUB_TOKEN="ghp_your_token_here"

# 5. Use in OpenClaw chat
# "Auto-merge all approved PRs in my repo"
```

## Configuration

### Skill Locations (Priority Order)

OpenClaw searches for skills in this order:

1. **Workspace** (highest priority): `<project>/skills/`
2. **Global**: `~/.openclaw/skills/`
3. **Bundled**: Built-in OpenClaw skills

**Example directory structure:**

```
~/.openclaw/skills/
├── steipete/
│   └── slack/
│       ├── skill.yaml
│       ├── index.js
│       └── README.md
└── autogame-17/
    └── auto-pr-merger/
        ├── skill.yaml
        └── main.py

./my-project/skills/  # Overrides global
├── custom-skill/
│   └── skill.yaml
```

### Environment Variables

Most skills require API keys or tokens. **Never hardcode secrets** — use environment variables:

```bash
# GitHub
export GITHUB_TOKEN="ghp_..."

# Slack
export SLACK_BOT_TOKEN="xoxb-..."
export SLACK_SIGNING_SECRET="..."

# AWS
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."

# OpenAI (for AI-powered skills)
export OPENAI_API_KEY="sk-..."
```

Or use a `.env` file (ensure it's in `.gitignore`):

```bash
# .env
GITHUB_TOKEN=ghp_your_token
SLACK_BOT_TOKEN=xoxb_your_token

# Load in shell
source .env

# Or use dotenv in code (Node.js example)
require('dotenv').config();
```

## Code Examples

### Programmatic Skill Discovery

**Node.js: Parse README.md and extract skills by category**

```javascript
const fs = require('fs');

// Read the awesome-openclaw-skills README
const readme = fs.readFileSync('README.md', 'utf-8');

// Extract skills from a category
function extractSkills(category) {
  const regex = new RegExp(
    `<summary><h3[^>]*>${category}</h3></summary>([\\s\\S]*?)</details>`,
    'i'
  );
  const match = readme.match(regex);
  if (!match) return [];

  const skillRegex = /- \[(.*?)\]\((https:\/\/clawskills\.sh\/skills\/.*?)\) - (.*)/g;
  const skills = [];
  let skillMatch;

  while ((skillMatch = skillRegex.exec(match[1])) !== null) {
    skills.push({
      name: skillMatch[1],
      url: skillMatch[2],
      description: skillMatch[3],
      slug: skillMatch[2].replace('https://clawskills.sh/skills/', '')
    });
  }

  return skills;
}

// Example: Get all Git & GitHub skills
const gitSkills = extractSkills('Git & GitHub');
console.log(`Found ${gitSkills.length} Git & GitHub skills:`);
gitSkills.slice(0, 5).forEach(skill => {
  console.log(`- ${skill.name}: ${skill.description}`);
});
```

### Python: Install Top Skills from a Category

```python
import re
import subprocess

def get_skills_from_category(readme_path, category):
    with open(readme_path, 'r') as f:
        content = f.read()
    
    # Find category section
    pattern = rf'<summary><h3[^>]*>{re.escape(category)}</h3></summary>(.*?)</details>'
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if not match:
        return []
    
    # Extract skills
    skill_pattern = r'- \[(.*?)\]\(https://clawskills\.sh/skills/(.*?)\) - (.*)'
    skills = []
    for m in re.finditer(skill_pattern, match.group(1)):
        skills.append({
            'name': m.group(1),
            'slug': m.group(2),
            'description': m.group(3)
        })
    return skills

# Install top 3 DevOps skills
devops_skills = get_skills_from_category('README.md', 'DevOps & Cloud')
for skill in devops_skills[:3]:
    print(f"Installing {skill['name']}...")
    subprocess.run(['clawhub', 'install', skill['slug']], check=True)
```

### Bash: Bulk Install Skills from a List

```bash
#!/bin/bash

# skills.txt contains one skill slug per line:
# steipete/slack
# autogame-17/auto-pr-merger
# pals-software/azure-devops

while IFS= read -r slug; do
  echo "Installing $slug..."
  clawhub install "$slug"
  if [ $? -eq 0 ]; then
    echo "✓ $slug installed"
  else
    echo "✗ $slug failed"
  fi
done < skills.txt
```

## Security & Best Practices

### Before Installing ANY Skill

1. **Review the source code:**
   ```bash
   # Clone the official skills repo
   git clone https://github.com/openclaw/skills.git
   cd skills/skills/<author>/<skill-name>
   
   # Read the code
   cat skill.yaml index.js README.md
   ```

2. **Check VirusTotal report** on ClawHub:
   - Green = No flags
   - Yellow = Low-confidence flags (may be false positives)
   - Red = Multiple engines flagged as malicious

3. **Look for red flags:**
   - Obfuscated code (base64, eval, exec)
   - Unexpected network requests
   - File system access outside project directory
   - Requests for unnecessary permissions

### Recommended Security Tools

```bash
# Snyk Skill Security Scanner
npm install -g @snyk/agent-scan
agent-scan ~/.openclaw/skills/steipete/slack

# Agent Trust Hub (Norton/GenDigital)
# Visit: https://ai.gendigital.com/agent-trust-hub
# Upload skill.yaml for analysis
```

### Permissions Model

Skills declare required permissions in `skill.yaml`:

```yaml
name: github-pr-automation
permissions:
  - network: ["github.com", "api.github.com"]
  - filesystem: ["read", "write"]  # Limit to project dir
  - env: ["GITHUB_TOKEN"]
```

**Always verify permissions match the skill's stated functionality.**

## Common Patterns

### Pattern 1: Find and Install a Domain-Specific Skill

```bash
# Use case: "I need a skill for Kubernetes deployments"

# 1. Search locally
grep -i "kubernetes" awesome-openclaw-skills/README.md

# 2. Or search ClawHub
clawhub search "kubernetes deployment"

# 3. Review top results
open https://clawskills.sh/skills/cloudops/k8s-deploy

# 4. Check source
open https://github.com/openclaw/skills/tree/main/skills/cloudops/k8s-deploy

# 5. Install
clawhub install cloudops/k8s-deploy

# 6. Configure
export KUBECONFIG="~/.kube/config"

# 7. Use in chat
# "Deploy my app to the production cluster using k8s-deploy"
```

### Pattern 2: Build a Custom Skill Collection

```bash
# Create a workspace-specific skills directory
mkdir -p ./skills

# Install project-relevant skills locally
cd skills
clawhub install steipete/slack --target ./
clawhub install pals-software/azure-devops --target ./
clawhub install docker-compose-runner --target ./

# Commit to version control
git add skills/
git commit -m "Add project-specific OpenClaw skills"

# Team members get skills automatically
git clone <repo>
# OpenClaw will auto-discover ./skills/
```

### Pattern 3: Monitor Skill Updates

```bash
# List installed skills with versions
clawhub list --verbose

# Check for updates
clawhub outdated

# Update all
clawhub update --all

# Update specific skill
clawhub update steipete/slack
```

## Troubleshooting

### Skill Not Found in ClawHub

**Problem:** `clawhub install author/skill` returns "Not found"

**Solutions:**
1. Verify slug on [clawskills.sh](https://clawskills.sh/)
2. Check if skill was removed from registry (happens with abandoned/malicious skills)
3. Try manual installation from GitHub:
   ```bash
   git clone https://github.com/openclaw/skills.git
   cp -r skills/skills/author/skill ~/.openclaw/skills/
   ```

### Skill Installed but Not Available

**Problem:** OpenClaw doesn't recognize the skill

**Solutions:**
1. Check installation path:
   ```bash
   ls ~/.openclaw/skills/
   ls ./skills/  # Workspace overrides global
   ```

2. Verify `skill.yaml` exists:
   ```bash
   cat ~/.openclaw/skills/author/skill/skill.yaml
   ```

3. Restart OpenClaw:
   ```bash
   openclaw restart
   ```

4. Check logs:
   ```bash
   openclaw logs | grep -i "skill"
   ```

### Permission Errors

**Problem:** Skill fails with "Permission denied"

**Solutions:**
1. Grant required permissions in OpenClaw settings
2. Check environment variables:
   ```bash
   echo $GITHUB_TOKEN  # Should not be empty
   ```
3. Verify API token scopes match skill requirements

### Skill Conflicts

**Problem:** Two skills with similar triggers interfere

**Solutions:**
1. Disable one skill:
   ```bash
   clawhub disable author/skill
   ```

2. Use workspace skills to override global:
   ```bash
   # Install preferred version in ./skills/
   clawhub install author/skill --target ./skills/
   ```

3. Rename skill triggers in `skill.yaml` (advanced)

### Outdated or Abandoned Skills

**Problem:** Skill hasn't been updated in 1+ years

**Solutions:**
1. Check for forks/alternatives:
   ```bash
   clawhub search "slack automation"
   ```

2. Contact author via GitHub (link in ClawHub page)

3. Fork and maintain yourself:
   ```bash
   git clone https://github.com/openclaw/skills.git
   cd skills/skills/author/old-skill
   # Make updates
   # Submit PR to openclaw/skills
   ```

## Contributing

This list only includes skills **already published** in `github.com/openclaw/skills`.

### To Add a Skill

1. **Publish to ClawHub first:**
   ```bash
   cd my-skill
   clawhub publish
   ```

2. **Open PR to awesome-openclaw-skills:**
   - Include ClawHub URL: `https://clawskills.sh/author/skill`
   - Include GitHub URL: `https://github.com/openclaw/skills/tree/main/skills/author/skill`
   - Follow format in existing categories

See [CONTRIBUTING.md](https://github.com/VoltAgent/awesome-openclaw-skills/blob/main/CONTRIBUTING.md)

### Reporting Security Issues

If a skill is malicious or has a security flaw:

1. **Do not install it**
2. Open an issue: [github.com/VoltAgent/awesome-openclaw-skills/issues](https://github.com/VoltAgent/awesome-openclaw-skills/issues)
3. Include:
   - Skill slug
   - VirusTotal report link
   - Description of the issue

## Resources

- **ClawHub Registry:** [clawskills.sh](https://clawskills.sh/)
- **Official Skills Repo:** [github.com/openclaw/skills](https://github.com/openclaw/skills)
- **OpenClaw Docs:** [docs.openclaw.dev](https://docs.openclaw.dev)
- **Security Tools:**
  - [Snyk Agent Scanner](https://github.com/snyk/agent-scan)
  - [Agent Trust Hub](https://ai.gendigital.com/agent-trust-hub)
- **VoltAgent Ecosystem:**
  - [awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)
  - [awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)
  - [awesome-ai-agent-papers](https://github.com/VoltAgent/awesome-ai-agent-papers)

## Related Skills

- **agent-skill-discovery** – Auto-suggest skills based on project dependencies
- **clawhub-curator** – Bulk install/update skills from curated lists
- **skill-security-audit** – Run automated security checks on installed skills

---

**License:** MIT  
**Maintained by:** VoltAgent ([voltagent.dev](https://voltagent.dev))  
**Last Updated:** May 16, 2026  
**Skill Count:** 5,211 (filtered from 13,729)
