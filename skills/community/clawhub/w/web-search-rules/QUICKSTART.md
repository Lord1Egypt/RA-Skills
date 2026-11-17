# Quickstart / 快速开始

## Install / 安装

```bash
openclaw skills install web-search-rules
```

or / 或

```bash
clawhub install web-search-rules
```

## Try it in 30 seconds / 30 秒验证

Say this to your agent / 对 agent 说这句话：

```text
帮我查一下 XX 的最新政策，把能引用的来源存下来
```

You should get / 你应该得到：

- a short list of findings, each with **source URL + date + quote**;
- a note saying which sources were actually opened versus only seen as snippets;
- **nothing written into your knowledge base until you confirm.**

If you got a wall of claims with no URLs, the skill did not run — check that
`web-search-rules` is in your installed skills list.

## The three things it does / 它只做三件事

1. **Search** and deduplicate results.
2. **Open** sources before trusting them. A snippet, an AI overview, or a
   file's embedded metadata does not count as an opened source.
3. **Stage** findings for your review, then archive only what you approve.

## Minimum useful path / 最小可用路径

Ask one question, review the staged list, approve what you want kept.

That is it. You do **not** need to configure source allow/deny rules, audit
logs, or platform adapters (Obsidian, NotebookLM, IMA, Feishu Docs, Tencent
Docs) to get value on day one — those only matter once you are archiving
regularly.

## Privacy and safety / 隐私与安全

- Runs locally. Writes only into the knowledge base you point it at.
- Stores no API keys, tokens, passwords or credentials.
- Archiving, bulk operations and destructive actions require your explicit
  confirmation first.
- A source is never treated as trustworthy just because its domain is allowed.

## Next / 下一步

Full workflow and configuration contract: `SKILL.md`.
