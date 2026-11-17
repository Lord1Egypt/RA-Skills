---
name: saasthinktank-research
description: Find dated, source-linked evidence on code export, GitHub sync, backend connections and databases for Bubble, Lovable, Base44 and Replit.
metadata:
  openclaw:
    emoji: "🔎"
    homepage: https://saasthinktank.com/ct/no-code-ai-app-builders/
---

# SaaS Think Tank research

Use this skill when someone asks what Bubble, Lovable, Base44 or Replit can do with source-code export, GitHub sync, an external backend or a built-in database. SaaS Think Tank is a software research publication across categories. Its existing [No-code AI app builders guide](https://saasthinktank.com/ct/no-code-ai-app-builders/) introduces all four products. This skill covers 16 dated findings for those products and four questions.

## Connect the evidence service

The public, read-only MCP service is `https://saasthinktank.com/mcp`. It needs no account, API key or payment. In a current OpenClaw installation, connect it once through **Settings → MCP → Add server** with Streamable HTTP. If the Gateway is stopped, this CLI command is another option:

```sh
openclaw mcp add saasthinktank --url https://saasthinktank.com/mcp --transport streamable-http
openclaw mcp doctor saasthinktank --probe
```

The skill does not set up the connection by itself. If the MCP tools are unavailable, explain the one-time connection step; do not invent findings. The tool responses state this edition's coverage and limits and include source links for individual findings.

## Answer a question

1. Read the `saasthinktank://evidence/coverage` resource when the client exposes MCP resources. Otherwise, inspect the `coverage` and `limitations` fields in the first tool response.
2. Use `search_findings` for a natural-language question. Its required `query` is the user's covered product question; optional `products` narrows the results and `limit` can be 1–16.
3. Use `compare_products` for two to four distinct covered products. Omit `capability_ids` to see all four questions, or use only IDs returned by the coverage resource or a tool response.
4. Use `get_finding` only with a `record_id` returned by an earlier tool call. Never construct a record ID.
5. Give the answer with each finding's `status`, original `checked_at` date, relevant `conditions` and `limitations`, and its `article_url` or source links. Cite the dataset when reusing its findings.

`unknown` means the published evidence does not establish yes or no. The dataset release date is not a new product check. Code export does not prove that saved data or sign-in services move with an app. GitHub sync does not prove that an existing repository can be imported. This service does not answer price questions, rank products, or check vendors live. For an unsupported question, say what is outside this edition and point to the broader publication if useful.

If the service is unavailable or rate limited, report that and wait to retry. Do not replace a failed call with remembered or guessed findings. Do not send private project data to this public service; a short product question is enough.
