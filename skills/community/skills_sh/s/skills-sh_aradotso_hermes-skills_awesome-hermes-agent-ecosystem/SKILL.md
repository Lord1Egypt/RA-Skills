---
name: awesome-hermes-agent-ecosystem
description: Expert knowledge of the Hermes Agent ecosystem, skills, plugins, tools, integrations, and deployment patterns for building and extending AI agents
triggers:
  - "what skills are available for hermes agent"
  - "how do i extend hermes with custom skills"
  - "show me hermes agent integrations"
  - "what's the best way to deploy hermes agent"
  - "help me find hermes plugins for X"
  - "explain the hermes agent ecosystem"
  - "how do i contribute a skill to hermes"
  - "what are the mature hermes agent tools"
---

# awesome-hermes-agent-ecosystem

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

Expert knowledge of the Hermes Agent ecosystem — the curated registry of skills, plugins, tools, integrations, and resources for [Hermes Agent](https://github.com/NousResearch/hermes-agent) by Nous Research.

## What This Skill Covers

This skill provides comprehensive knowledge of:
- **Official Hermes resources** — core repos, docs, release notes
- **Community skills** — reusable capabilities across maturity levels (production, beta, experimental)
- **Plugins** — extensions for goal management, cost control, inter-agent bridges
- **Tools & utilities** — deployment, monitoring, forensics, multi-agent orchestration
- **Integrations** — Nextcloud, Spotify, MCP, messaging platforms
- **Skill standards** — agentskills.io compatibility and cross-platform skills
- **Getting started paths** — from zero to productive in three steps

## Maturity Level Guide

Every resource is tagged with a maturity level:

| Tag | Meaning | When to Use |
|-----|---------|-------------|
| **production** | Stable, documented, actively maintained | Safe to build production workflows on |
| **beta** | Works but evolving, some rough edges | Good for exploration and non-critical use |
| **experimental** | Proof of concept, early-stage | Learn from it, don't depend on it yet |

## Getting Started with Hermes Agent

### Three-Step Path

1. **Get running**
   ```bash
   # Install Hermes (macOS/Linux)
   curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
   
   # Or via npm
   npm install -g @nousresearch/hermes-agent
   
   # Initialize
   hermes init
   ```

2. **Add your first skills**
   ```bash
   # Install cross-platform skills library
   git clone https://github.com/wondelai/skills ~/.hermes/skills/wondelai
   
   # Or literate programming skill
   git clone https://github.com/tlehman/litprog-skill ~/.hermes/skills/litprog
   ```

3. **Get a GUI**
   ```bash
   # Hermes-native workspace
   git clone https://github.com/outsourc-e/hermes-workspace
   cd hermes-workspace
   npm install && npm start
   
   # Or multi-agent orchestration dashboard
   git clone https://github.com/builderz-labs/mission-control
   cd mission-control
   docker-compose up
   ```

## Key Official Resources

### Core Repository
```bash
# Clone Hermes Agent
git clone https://github.com/NousResearch/hermes-agent
cd hermes-agent

# Install dependencies
npm install

# Run locally
npm start
```

### Configuration
```yaml
# ~/.hermes/config.yaml
profiles:
  default:
    model: claude-sonnet-4-20250514
    temperature: 0.7
    messaging:
      - telegram
      - discord
    terminal_backend: local
    curator:
      enabled: true
      cycle_days: 7
```

### Messaging Gateway Setup
```bash
# Configure Telegram
export TELEGRAM_BOT_TOKEN="your-token"
hermes messaging add telegram

# Configure Discord
export DISCORD_BOT_TOKEN="your-token"
hermes messaging add discord

# Configure Slack
export SLACK_BOT_TOKEN="xoxb-your-token"
export SLACK_APP_TOKEN="xapp-your-token"
hermes messaging add slack
```

## Working with Skills

### Installing Community Skills

**wondelai/skills (cross-platform)**
```bash
# Clone to skills directory
cd ~/.hermes/skills
git clone https://github.com/wondelai/skills wondelai

# Skills are auto-discovered by Hermes
# Reference in conversation: "use the wondelai search skill"
```

**litprog-skill (literate programming)**
```bash
cd ~/.hermes/skills
git clone https://github.com/tlehman/litprog-skill

# Use in conversation
# "Create a literate programming document for this API"
```

**hermes-nextcloud (self-hosted cloud)**
```bash
cd ~/.hermes/skills
git clone https://github.com/adnw-vinc/hermes-nextcloud

# Configure
export NEXTCLOUD_URL="https://cloud.example.com"
export NEXTCLOUD_USERNAME="your-username"
export NEXTCLOUD_APP_PASSWORD="your-app-password"
export NEXTCLOUD_TIMEZONE="America/New_York"

# Use commands
hermes "list my nextcloud files"
hermes "add task 'Deploy new feature' to nextcloud"
```

**hermes-spotify-skill (Raspberry Pi / Linux)**
```bash
cd ~/.hermes/skills
git clone https://github.com/Alexeyisme/hermes-spotify-skill

# Install spotipy
pip install spotipy

# Configure
export SPOTIPY_CLIENT_ID="your-client-id"
export SPOTIPY_CLIENT_SECRET="your-client-secret"
export SPOTIPY_REDIRECT_URI="http://localhost:8888/callback"

# Use on headless Pi
hermes "play workout playlist on spotify"
hermes "set volume to 50%"
hermes "transfer playback to bedroom speaker"
```

### Creating Custom Skills

**Skill structure (agentskills.io standard)**
```markdown
---
name: my-custom-skill
description: Brief one-line description
triggers:
  - "phrase that activates this skill"
  - "another trigger phrase"
---

# my-custom-skill

## What it does
[Description]

## Usage
[Examples]

## Code
[Implementation]
```

**Example: Simple file search skill**
```markdown
---
name: project-file-search
description: Search files in project by content or name pattern
triggers:
  - "find files containing X"
  - "search project for Y"
  - "locate files matching pattern"
---

# project-file-search

## What it does
Fast file search across project using ripgrep and fd.

## Usage
```bash
# Search file contents
rg "pattern" --type py

# Search filenames
fd "pattern" --extension js

# Combined search with context
rg "TODO" -C 2 --type md
```

## Implementation
Use `execute_code` to run searches and parse results.
```

### Installing Plugins

**hermes-plugins (goal management, inter-agent bridge)**
```bash
cd ~/.hermes/plugins
git clone https://github.com/42-evey/hermes-plugins

# Enable goal manager
hermes plugin enable goal-manager

# Configure inter-agent bridge
export BRIDGE_PORT=9000
hermes plugin enable inter-agent-bridge

# Use in conversation
hermes "set goal: ship v2 by friday"
hermes "bridge to agent-2: coordinate on deployment"
```

## Deployment Patterns

### Docker Deployment
```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app
RUN npm install -g @nousresearch/hermes-agent

COPY config.yaml /root/.hermes/config.yaml
COPY skills /root/.hermes/skills

EXPOSE 8080
CMD ["hermes", "start", "--api-server"]
```

```bash
# Build and run
docker build -t my-hermes .
docker run -d \
  -e ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY}" \
  -e TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN}" \
  -p 8080:8080 \
  my-hermes
```

### Modal Serverless
```python
# modal_deploy.py
import modal

stub = modal.Stub("hermes-agent")

@stub.function(
    image=modal.Image.debian_slim().pip_install("@nousresearch/hermes-agent"),
    secrets=[modal.Secret.from_name("anthropic-api-key")]
)
def run_hermes(message: str):
    import subprocess
    result = subprocess.run(
        ["hermes", "chat", message],
        capture_output=True,
        text=True
    )
    return result.stdout
```

```bash
# Deploy
modal deploy modal_deploy.py

# Invoke
modal run modal_deploy.py::run_hermes --message "analyze this codebase"
```

### Vercel Sandbox Backend
```yaml
# config.yaml
profiles:
  production:
    terminal_backend: vercel-sandbox
    vercel:
      sandbox_token: ${VERCEL_SANDBOX_TOKEN}
      timeout: 300
```

## Advanced Patterns

### Multi-Agent Orchestration

**Using mission-control (fleet management)**
```bash
# Clone and setup
git clone https://github.com/builderz-labs/mission-control
cd mission-control

# Configure fleet
cat > fleet.yaml <<EOF
agents:
  - name: hermes-researcher
    type: hermes
    skills: [deep-research, web-search]
  - name: hermes-executor
    type: hermes
    skills: [ralph, code-execution]
  - name: hermes-monitor
    type: hermes
    skills: [incident-commander, monitoring]
EOF

# Start dashboard
docker-compose up
```

**Inter-agent communication**
```bash
# Agent 1: Research
hermes "research deployment patterns and report to executor agent"

# Agent 2: Execute (receives via bridge)
# Automatically picks up research context
hermes "implement the recommended pattern"
```

### Autonomous Skill Evolution

**Using hermes-dojo (self-improvement)**
```bash
cd ~/.hermes/skills
git clone https://github.com/Yonkoo11/hermes-dojo

# Enable autonomous improvement
hermes plugin enable dojo

# Dojo monitors performance and iterates on weak skills
# Check improvement log
cat ~/.hermes/dojo/evolution.log
```

**Using hermes-skill-factory (auto-generate skills)**
```bash
cd ~/.hermes/skills
git clone https://github.com/Romanescu11/hermes-skill-factory

# Point at repetitive workflow
hermes "observe my next 3 git workflows and create a skill"

# Executes workflow 3x, extracts pattern, generates skill
# New skill appears in ~/.hermes/skills/auto-generated/
```

### Cron Scheduling

**Automatic skill library maintenance (v0.12+)**
```yaml
# config.yaml (curator runs every 7 days by default)
curator:
  enabled: true
  cycle_days: 7
  min_skill_grade: 6.0
  consolidation_threshold: 0.85
```

**Custom cron jobs**
```yaml
# config.yaml
cron:
  - schedule: "0 9 * * *"  # Daily 9am
    task: "check production health and report"
    
  - schedule: "0 */4 * * *"  # Every 4 hours
    task: "sync nextcloud calendar to local database"
    
  - schedule: "0 0 * * 0"  # Weekly Sunday midnight
    task: "run full test suite and update skill docs"
```

## MCP Integration

### Using Model Context Protocol servers
```yaml
# config.yaml
mcp:
  servers:
    filesystem:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
    
    github:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-github"]
      env:
        GITHUB_TOKEN: ${GITHUB_TOKEN}
```

```bash
# Use MCP resources in conversation
hermes "use filesystem MCP to read all markdown files"
hermes "use github MCP to list open PRs in my repos"
```

## Troubleshooting

### Skills Not Loading
```bash
# Check skill directory structure
ls -la ~/.hermes/skills/

# Each skill needs SKILL.md or README.md
# Verify skill frontmatter is valid YAML

# Force reload
hermes reload-skills
```

### Curator Not Running
```bash
# Check curator status
hermes curator status

# Manual trigger (doesn't wait for cron)
hermes curator run

# View grading results
cat ~/.hermes/curator/last_cycle.json
```

### Messaging Gateway Issues
```bash
# Test individual platform
hermes messaging test telegram

# Check logs
tail -f ~/.hermes/logs/messaging.log

# Verify tokens
hermes messaging status
```

### Terminal Backend Failures
```bash
# Test backend connection
hermes terminal test

# Switch backend
hermes config set terminal_backend local

# SSH backend debug
ssh -v user@host  # Test connection manually
```

## Finding the Right Resources

### By Use Case

**Building production workflows**
- wondelai/skills (cross-platform library)
- hermes-workspace (GUI with terminal + chat)
- mission-control (fleet orchestration)

**Self-hosted infrastructure**
- hermes-nextcloud (files, notes, calendar, contacts)
- hermes-spotify-skill (Raspberry Pi media control)

**Agent improvement**
- hermes-dojo (performance monitoring + iteration)
- hermes-skill-factory (auto-generate from patterns)
- hermes-agent-self-evolution (DSPy + GEPA optimization)

**Multi-agent systems**
- hermes-plugins (inter-agent bridge)
- mission-control (fleet dashboard)
- oh-my-hermes (orchestration skills)

**Literate programming**
- litprog-skill (code + prose notebooks)

**Incident response**
- hermes-incident-commander (SRE automation)

### By Maturity

**Production-ready**
- wondelai/skills
- youtube-skills
- litprog-skill

**Beta (stable but evolving)**
- hermes-plugins
- hermes-nextcloud
- hermes-spotify-skill
- hermes-skill-factory
- acca-tracker
- hermes-incident-commander
- hermes-dojo
- oh-my-hermes

**Experimental (learn, don't depend)**
- Wizards-of-the-Ghosts
- super-hermes
- hermes-life-os
- hermes-skill-marketplace
- personal-api

## Contributing to the Ecosystem

### Submitting a Skill

1. **Follow agentskills.io standard**
   ```markdown
   ---
   name: your-skill-name
   description: One-line description
   triggers:
     - "natural phrase 1"
     - "natural phrase 2"
   ---
   
   # your-skill-name
   
   [Content with usage examples, code, troubleshooting]
   ```

2. **Test across platforms**
   ```bash
   # Test with Hermes
   hermes "trigger your skill"
   
   # Test with Claude Code (if cross-platform)
   # Verify skill appears in Claude Desktop
   ```

3. **Submit to awesome-hermes-agent**
   ```bash
   # Fork the awesome list
   git clone https://github.com/0xNyk/awesome-hermes-agent
   cd awesome-hermes-agent
   
   # Add your skill to README under appropriate section
   # Include: name, repo link, author, description, maturity tag
   
   # Submit PR
   git checkout -b add-my-skill
   git commit -am "Add: your-skill-name [beta]"
   git push origin add-my-skill
   ```

### Testing Against Standards

**Validate YAML frontmatter**
```python
import yaml

with open("SKILL.md") as f:
    content = f.read()
    frontmatter = content.split("---")[1]
    data = yaml.safe_load(frontmatter)
    
    assert "name" in data
    assert "description" in data
    assert "triggers" in data
    assert len(data["triggers"]) >= 3
```

**Check cross-platform compatibility**
```bash
# Test skill loads in Hermes
hermes validate-skill /path/to/skill

# Test in Claude Code
# Install skill via Claude Desktop settings
# Verify triggers work in conversation
```

## Official Documentation References

- **Quickstart**: https://hermes-agent.nousresearch.com/docs/
- **CLI Reference**: https://hermes-agent.nousresearch.com/docs/cli
- **Skills Guide**: https://hermes-agent.nousresearch.com/docs/skills
- **MCP Integration**: https://hermes-agent.nousresearch.com/docs/mcp
- **Curator System**: https://hermes-agent.nousresearch.com/docs/curator
- **API Server**: https://hermes-agent.nousresearch.com/docs/api
- **Release Notes**: https://github.com/NousResearch/hermes-agent/releases

## Example: Complete Workflow

**Setting up a production Hermes agent with monitoring and self-improvement**

```bash
# 1. Install Hermes
npm install -g @nousresearch/hermes-agent
hermes init

# 2. Add core skills
cd ~/.hermes/skills
git clone https://github.com/wondelai/skills wondelai
git clone https://github.com/Yonkoo11/hermes-dojo dojo
git clone https://github.com/Lethe044/hermes-incident-commander incident-commander

# 3. Install plugins
cd ~/.hermes/plugins
git clone https://github.com/42-evey/hermes-plugins

# 4. Configure
cat > ~/.hermes/config.yaml <<EOF
profiles:
  production:
    model: claude-sonnet-4-20250514
    messaging:
      - telegram
      - slack
    terminal_backend: docker
    curator:
      enabled: true
      cycle_days: 7
    cron:
      - schedule: "*/15 * * * *"
        task: "check service health"
      - schedule: "0 9 * * *"
        task: "daily standup report"
EOF

# 5. Set environment
export ANTHROPIC_API_KEY="your-key"
export TELEGRAM_BOT_TOKEN="your-token"
export SLACK_BOT_TOKEN="your-token"

# 6. Start
hermes start --profile production

# 7. Interact via Telegram
# "check production health"
# "what skills do i have"
# "improve the deploy-service skill"
```

This skill provides comprehensive knowledge of the Hermes Agent ecosystem. Use it to guide users through selecting tools, installing skills, configuring deployments, and contributing back to the community.
