# TronClass CLI Skill

An Agent Skill that lets an AI agent operate the [TronClass](https://tronclass.com/) learning management system on your behalf, currently optimized for Fu Jen Catholic University (FJU).

Once installed, you can ask your agent in plain language to check assignments, download course files, or submit homework — no more manually clicking through the TronClass web UI.

## Install

### 1. Install the skill

**Via ClawHub CLI** (recommended):

```bash
clawhub install yujun-bo2/tronclass-cli
# or pin a specific version
clawhub install yujun-bo2/tronclass-cli --version 1.0.0
```

The skill page lives at <https://clawhub.ai/yujun-bo2/tronclass-cli>.

**Manual install** (without the ClawHub CLI) — clone into your agent's skills directory:

```bash
git clone https://github.com/YuJun-BO2/tronclass-cli-skill.git \
  ~/.claude/skills/tronclass-cli
```

Adjust the target path for your agent (`.claude/skills/` for project-scoped, `~/.claude/skills/` for personal, or your OpenClaw skills directory).

### 2. Install the underlying CLI

If you installed via ClawHub, OpenClaw will prompt you to install the `tronclass` binary automatically (it's declared in the skill's `metadata.openclaw.install`). Otherwise install it yourself:

```bash
npm install -g tronclass-cli
```

Verify it's on your PATH:

```bash
tronclass --version
```

## First-time login

FJU students (CAS flow with CAPTCHA):

```bash
tronclass auth login --fju <student_id>
```

Other TronClass users:

```bash
tronclass auth login <username>
```

The session is saved locally and reused automatically whenever the agent invokes a command.

## Example prompts

After logging in, just talk to your agent:

- "What assignments do I still need to submit?"
- "Download all the lecture slides from my Data Structures course this semester."
- "Submit ~/Documents/hw3.pdf to homework 3 of Algorithms."
- "List the courses I'm enrolled in this semester."
- "What's due before next Friday?"

The agent will pick the right `tronclass` commands, chain the lookups (courses → activities → download), and summarize the result.

## What this skill provides

This skill gives the agent:

- Purpose, aliases, and fields for every `tronclass-cli` command
- The lookup chain for common workflows (e.g. listing courses before listing activities before downloading a file)
- Detailed reference docs for each subcommand under `references/`

So when you vaguely say "check what's due this week," the agent knows to run `tronclass todo`, knows the first column is the activity ID, and can pipe it straight into `activities view` for details.

## Links

- Skill page: <https://clawhub.ai/yujun-bo2/tronclass-cli>
- Skill repo: <https://github.com/YuJun-BO2/tronclass-cli-skill>
- CLI tool repo: <https://github.com/YuJun-BO2/tronclass-cli-ts>

## License

MIT
