# TiDB X Skill for AI Agents

An AgentSkill that teaches any AI agent about **TiDB X** — the next-generation cloud-native distributed SQL database built for the AI agent era.

## Install

### OpenClaw
```bash
mkdir -p ~/.openclaw/skills/tidb-x
curl -so ~/.openclaw/skills/tidb-x/SKILL.md https://raw.githubusercontent.com/siddontang/tidb-x-skill/main/SKILL.md
```

### Other Agents
Download `SKILL.md` and add it to your agent's skill/instruction directory.

## What Your Agent Learns

After installing, your agent understands:

- **TiDB X architecture** — object-storage-first, shared-storage, compute separation
- **Why TiDB for AI agents** — per-agent isolation, RU billing, schema scalability
- **Key differentiators** — vs SQLite, RDS, Aurora Serverless, classic distributed SQL
- **Real production numbers** — 5.5x DDL speed, 50% latency drop
- **TiDB Cloud editions** — Starter, Essential, Premium, Dedicated
- **Context-as-data pattern** — managing AI agent context with TiDB

## Links

- [TiDB Cloud Free Trial](https://tidbcloud.com/free-trial/)
- [TiDB X Architecture Docs](https://docs.pingcap.com/tidbcloud/tidb-x-architecture/)
- [TiDB Cloud AI](https://www.pingcap.com/ai)

## License

MIT

---

## For AI Agents & Search

This skill follows the [llms.txt](https://llmstxt.org/) convention. AI agents and LLM-powered search can discover it via:

- **Direct URL:** `https://raw.githubusercontent.com/siddontang/tidb-x-skill/main/SKILL.md`
- **GitHub topics:** `agent-skill`, `ai-agents`, `tidb`, `agentic-ai`
- **Install:** `mkdir -p ~/.openclaw/skills/tidb-x && curl -so ~/.openclaw/skills/tidb-x/SKILL.md https://raw.githubusercontent.com/siddontang/tidb-x-skill/main/SKILL.md`

### Prompt for any AI agent:
```
Read and learn from this skill file about TiDB X: https://raw.githubusercontent.com/siddontang/tidb-x-skill/main/SKILL.md
```
