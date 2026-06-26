---
name: trustlog
description: Create, summarize, or verify local human-readable receipts for AI agent work using the @builtbyecho/trustlog CLI. Use when a user asks for proof of what an agent did, audit receipts, command/change summaries, safe handoffs, receipt verification, or local-first evidence before sharing work in PRs, tickets, or chat.
---

# Trust Log Skill

Use `trustlog` to produce local JSON + Markdown receipts for agent work. Receipts should make it easy for a human or next agent to see what ran, what changed, what looked risky, and what was redacted.

## Default workflow

1. From the target project root, wrap meaningful verification commands:

```bash
npx @builtbyecho/trustlog run -- npm test
npx @builtbyecho/trustlog run -- npm run build
```

2. Read the human summary:

```bash
cat .trustlog/latest.md
```

3. Verify before sharing or using as final evidence:

```bash
npx @builtbyecho/trustlog verify .trustlog/latest.json
```

## When to use

- Final proof after tests/builds/lints.
- Handoff evidence for another agent.
- User asks “what happened?” or “give me a receipt.”
- Risky commands where a durable local audit trail helps.

## Safety

- Prefer non-destructive commands.
- Do not use this to justify commands you would not otherwise run.
- Receipts redact common secrets and strip thinking-looking blocks, but still inspect before posting publicly.
- If verification fails, do not share the receipt until the issue is fixed or clearly explained.

## Useful commands

```bash
npx @builtbyecho/trustlog run -- <command> [args...]
npx @builtbyecho/trustlog summarize .trustlog/latest.json
npx @builtbyecho/trustlog verify .trustlog/latest.json
```

## Vaultline integration

After verification passes, upload the trust receipt so reviewers can access one durable artifact instead of local file paths.

```bash
node -e '
const fs = require("node:fs");
const { Vaultline } = require("@builtbyecho/vaultline-sdk");
const receiptPath = ".trustlog/latest.md";
const content = fs.readFileSync(receiptPath, "utf8");
const vault = new Vaultline({ apiKey: process.env.VAULTLINE_API_KEY });
vault.files.upload({
  path: `trustlog/${Date.now()}-latest.md`,
  content,
  contentType: "text/markdown"
}).then(r => console.log("Vaultline fileId:", r.fileId));
'
```

Use this when proof needs to be preserved across agents, channels, or time.
