# SeeSaw-Claw

Publish-ready repository for the `seesaw-agent` OpenClaw skill.

This repository is designed to support three workflows:

1. Install from ClawHub with `clawhub install seesaw-agent`
2. Install manually from GitHub by copying `skills/seesaw` into your OpenClaw workspace
3. Publish updates to ClawHub from this repository

## Install From ClawHub

Recommended path:

```bash
clawhub install seesaw-agent
pip install -r skills/seesaw/requirements.txt
openclaw skills check
```

After installing the skill files, configure the required environment variables for `seesaw-agent`.

### Configure `seesaw-agent`

OpenClaw stores skill configuration in `~/.openclaw/openclaw.json` under `skills.entries.<skill-name>`.

Example:

```json
{
  "skills": {
    "entries": {
      "seesaw-agent": {
        "enabled": true,
        "env": {
          "SEESAW_BASE_URL": "https://app.seesaw.fun/v1",
          "SEESAW_API_KEY": "xxx",
          "SEESAW_API_SECRET": "xxx"
        }
      }
    }
  }
}
```

If your OpenClaw environment exposes a helper wrapper for SeeSaw, you can use it as a shortcut:

```bash
openclaw skill run --api-key "xxx" --api-secret "xxx"
```

If that helper is not available in your OpenClaw build, update `~/.openclaw/openclaw.json` manually as shown above.

### Verify The Install

```bash
openclaw skills info seesaw-agent
openclaw skills check
```

Expected result:

- `seesaw-agent` appears in the skill list
- no missing requirements for `SEESAW_BASE_URL`, `SEESAW_API_KEY`, or `SEESAW_API_SECRET`

## Install From GitHub

Use this path when an OpenClaw agent is asked to read the GitHub repository and install the skill step by step.

### Step 1: Clone The Repository

```bash
git clone https://github.com/SeesawTech/SeeSaw-Claw.git
cd SeeSaw-Claw
```

### Step 2: Copy The Skill Into Your OpenClaw Workspace

Default OpenClaw workspace path:

```text
~/.openclaw/workspace/skills
```

```bash
mkdir -p ~/.openclaw/workspace/skills
cp -R skills/seesaw ~/.openclaw/workspace/skills/
```

### Step 3: Install Python Dependency

```bash
pip install -r ~/.openclaw/workspace/skills/seesaw/requirements.txt
```

### Step 4: Configure API Credentials

Add the same `skills.entries.seesaw-agent.env` block shown above to `~/.openclaw/openclaw.json`.

### Step 5: Refresh OpenClaw

Start a new OpenClaw session, or re-run the gateway so it reloads workspace skills.

### Step 6: Verify

```bash
openclaw skills info seesaw-agent
openclaw skills check
```

## Usage

Once installed and configured, the skill lives at:

```text
~/.openclaw/workspace/skills/seesaw
```

The main CLI entrypoint is:

```bash
python skills/seesaw/scripts/seesaw.py --help
```

Common examples:

```bash
python skills/seesaw/scripts/seesaw.py balance
python skills/seesaw/scripts/seesaw.py list-markets --status active --page 1 --limit 20
python skills/seesaw/scripts/seesaw.py positions
```

## Publish To ClawHub

Publish the skill folder in this repository:

```bash
clawhub publish ./skills/seesaw --slug seesaw-agent --name "SeeSaw Prediction Market" --version 0.1.0 --tags latest
```

For bulk updates after local changes:

```bash
clawhub sync --all
```

## Agent Notes

If an OpenClaw agent receives a prompt like:

```text
請前往 https://github.com/SeesawTech/SeeSaw-Claw，閱讀 SeeSaw 的 OpenClaw Skill 安裝教學，然後一步一步幫我完成安裝。
```

it should follow this repository's `README.md`, prefer the ClawHub flow first, and fall back to the GitHub/manual flow if ClawHub is unavailable.
