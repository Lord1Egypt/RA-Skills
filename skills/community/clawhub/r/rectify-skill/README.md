# Rectify

An OpenClaw skill that connects your agents to [Rectify](https://www.rectify.so) — an all-in-one SaaS operations platform — for task management and document creation directly from your agents.

## What is Rectify?

Rectify is an all-in-one SaaS operations platform providing:

- **Bug Reporting** — Annotated screenshots, Loom recordings, console logs, and network requests captured in one click
- **AI-Powered Session Replays** — Watch exactly what users experienced; AI surfaces rage clicks, errors, and drop-off patterns
- **Uptime Monitoring** — HTTP/HTTPS, TCP, DNS, ICMP monitoring with Slack/Discord/email alerts and branded status pages
- **Code Scanning** — On-demand static analysis with A-E ratings for bugs, security vulnerabilities, and code smells
- **Roadmap** — Public/private boards for feature requests and community voting
- **Changelogs** — AI-generated release notes via Quanta (Rectify's built-in AI assistant)
- **Documents** — Full document management with markdown, sub-pages, and archiving
- **AgentPulse** — AI agent management layer built on OpenClaw: task boards, agent coordination, cron jobs, skill permissions, and cost tracking

## What This Skill Does

Gives your OpenClaw agents full CRUD access to:

### Task Board
- List, create, update, move, assign, delete, and search tasks
- Create and delete columns
- Assign tasks to OpenClaw agents or Rectify project members

### Documents
- List, get, search, create, update, archive, restore, and delete documents
- Create sub-pages with `parentDocument`
- Full markdown content support

## Installation

Install via ClawHub:

```bash
clawhub install rectify-agentpulse
```

## Setup

1. Create a Rectify account at https://www.rectify.so
2. Create a project and open AgentPulse
3. Pair your OpenClaw gateway with your Rectify project
4. The skill is automatically deployed to your agents during pairing — no additional configuration needed

## Authentication

Uses your existing `$RECTIFY_PROJECT_TOKEN` — the token established during the Rectify setup process. No extra API keys required.

## Usage Examples

Ask your agent:

```
Create a task "Fix login bug" with high priority in the To Do column
```

```
List all tasks assigned to me
```

```
Move task abc123 to the In Progress column
```

```
Create a document titled "API Reference" with the full endpoint documentation
```

```
Search documents for "onboarding"
```

## License

MIT
