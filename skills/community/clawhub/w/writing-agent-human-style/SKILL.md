---
name: writing-agent-human-style
description: "Writing Agent - Human Style: Draft on-brand text and Markdown copy from a compact request plus one optional JSON `context` object. Use when an agent needs writing agent human style, writing agent human style, draft up to 10 on brand social media replies in a single request, write original social posts from a topic and a few notes, turn an outline and source material into a short markdown blog post up to 12, 000 characters, draft large blog post, topic through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/writing-agent-human-style
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/writing-agent-human-style"}}
---
# Writing Agent - Human Style

## Freshness
Last updated: `2026-06-09`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Writing Agent is an AI writing assistant that drafts on-brand social media replies, original social posts, short-form blog posts up to 12,000 characters, and larger blog posts up to 30,000 characters — in your voice, ready to review and publish. Give it a topic, your brand voice, and any notes you want it to use, and get back polished, human-sounding copy that respects your requested character limit. Generate up to ten tailored replies in a single request, spin up original posts from a topic, turn an outline and a few notes into a clean Markdown short blog draft, or create a larger long-form Markdown article. Because it writes only from the facts you provide — never inventing claims, stats, or links — every draft stays accurate and on-message.

## Product Instructions
### Writing Agent

Generate polished, on-brand text and Markdown drafts — social media replies, original social posts, short-form blog posts, and larger blog posts. Send a compact request plus one optional `context` object, and the tool returns ready-to-review copy that respects your requested character limit.

#### Actions

##### draft_social_responses

Generate one short reply for each social post you supply.

Required:
- `posts`: 1 to 10 posts, each with `content`; optional `post_id` for your own mapping
- `max_characters_per_response`: 1 to 500 characters per reply

Optional:
- `context`: JSON object with shared writing guidance

##### draft_social_post

Generate one original social media post.

Required:
- `topic`
- `max_characters`: 1 to 5,000 characters

Optional:
- `context`: JSON object with writing guidance and source material

##### draft_short_blog_post

Generate one short-form blog post in Markdown.

Required:
- `topic`
- `max_characters`: 100 to 12,000 characters

Optional:
- `context`: JSON object with outline, writing guidance, and source material

##### draft_large_blog_post

Generate one larger blog post in Markdown.

Required:
- `topic`
- `max_characters`: 100 to 30,000 characters

Optional:
- `context`: JSON object with outline, writing guidance, and source material

#### Context Field

Put all writing guidance and source material in the single `context` object instead of separate fields. `context` must be a JSON object that serializes to no more than 40,000 characters, and the combined `topic`, `posts` content, and `context` are limited to 85,000 characters per request. Keep it concise and include only material the draft should actually use.

Useful context fields:
- `voice`: tone, style, and brand voice guidance
- `goal`: what the draft should accomplish
- `audience`: who the content is for
- `instructions`: specific writing instructions
- `outline`: requested structure for blog posts or longer drafts
- `source_material`: facts, product details, campaign notes, or excerpts to use
- `brand_context`: positioning, vocabulary, claims to use or avoid
- `examples`: example outputs or style references
- `constraints`: words, claims, formats, or topics to avoid
- `desired_structure`: requested sections, bullets, or formatting

#### Output

The tool returns finished writing inline as text or Markdown in `content`. Social response calls also return a `responses` array with one item per input post.

If a draft exceeds the requested character limit, the tool trims it to fit and includes `OUTPUT_TRUNCATED_TO_CHARACTER_LIMIT` in `warnings`.

The agent writes only from the facts and material you provide — it will not invent claims, statistics, URLs, or offers — so every draft stays accurate and on-message.

#### Notes

This tool drafts copy only. It does not publish content, browse the web, retrieve URLs, or accept files, images, audio, or video.

## When To Use
- Use this skill for `Writing Agent - Human Style` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: writing agent   human style, writing agent human style, draft up to 10 on brand social media replies in a single request, write original social posts from a topic and a few notes, turn an outline and source material into a short markdown blog post up to 12, 000 characters, draft large blog post, topic.
- Supported action names: `draft_large_blog_post`, `draft_short_blog_post`, `draft_social_post`, `draft_social_responses`.

## Use Cases
- Draft up to 10 on-brand social media replies in a single request
- Write original social posts from a topic and a few notes
- Turn an outline and source material into a short Markdown blog post up to 12
- 000 characters
- Draft larger long-form Markdown blog posts up to 30
- 000 characters
- Keep every draft within an exact character limit
- Maintain a consistent brand voice across your whole team
- Turn campaign briefs and brand notes into ready-to-review copy
- Reply to customer and community posts in your tone at scale
- Produce accurate drafts that stick to the facts you provide
- Speed up content review workflows with publish-ready text
- Scale social and blog content creation without losing your voice

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `4`.
x402 action routes are enabled and listed in `./schema.md`.

- `draft_large_blog_post` (action slug: `draft-large-blog-post`): Generate one larger blog post in Markdown from a topic, character limit, and optional JSON context. Provide max_characters from 100 to 30,000. Price: `50` credits. Parameters: `context`, `max_characters`, `topic`.
- `draft_short_blog_post` (action slug: `draft-short-blog-post`): Generate one short-form blog post in Markdown from a topic, character limit, and optional JSON context. Provide max_characters from 100 to 12,000. Price: `30` credits. Parameters: `context`, `max_characters`, `topic`.
- `draft_social_post` (action slug: `draft-social-post`): Generate one original social media post from a topic, character limit, and optional JSON context. Price: `10` credits. Parameters: `context`, `max_characters`, `topic`.
- `draft_social_responses` (action slug: `draft-social-responses`): Generate one short brand-appropriate social media response for each supplied post, up to ten posts per request. Price: `20` credits. Parameters: `context`, `max_characters_per_response`, `posts`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "writing-agent-human-style"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "writing-agent-human-style"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "writing-agent-human-style"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "writing-agent-human-style"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "writing-agent-human-style"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "writing-agent-human-style"
  }
}
```

## Call This Tool
Product slug: `writing-agent-human-style`

Marketplace page: https://www.agentpmt.com/marketplace/writing-agent-human-style

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- No-account x402 route: first use `../agentpmt-no-account-agentaddress-x402` to create an AgentAddress and prepare the x402 payment flow.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`
- No-account AgentAddress/x402 setup: ../agentpmt-no-account-agentaddress-x402
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402
  - OpenClaw install: `openclaw skills install agentpmt-no-account-agentaddress-x402`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-no-account-agentaddress-x402`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
npx skills add AgentPMT/agent-skills --skill agentpmt-no-account-agentaddress-x402
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Writing-Agent---Human-Style",
    "arguments": {
      "action": "draft_large_blog_post",
      "context": {},
      "max_characters": 100,
      "topic": "example topic"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "writing-agent-human-style",
  "parameters": {
    "action": "draft_large_blog_post",
    "context": {},
    "max_characters": 100,
    "topic": "example topic"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

x402 action path: `POST https://www.agentpmt.com/api/external/tools/writing-agent-human-style/actions/draft-large-blog-post/invoke`.

x402 wallet scope:

- Direct x402 calls are scoped to the payer wallet that signs the payment authorization.
- Files created through File Manager during x402 calls are owned by that wallet scope.
- Reuse the same payer wallet for later x402 calls when listing, fetching, downloading, or passing those files between AgentPMT tools.
- File Manager files normally expire after the retention window, up to 7 days, unless the file action returns a shorter expiration.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `draft_large_blog_post` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- No-account AgentAddress/x402 setup: ../agentpmt-no-account-agentaddress-x402 (ClawHub: `agentpmt-no-account-agentaddress-x402`, page: https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-no-account-agentaddress-x402`)
- Marketplace product: https://www.agentpmt.com/marketplace/writing-agent-human-style
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
