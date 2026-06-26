---
name: rstack-page
preamble-tier: 2
version: 1.0.0
description: |
  Crafts excellent resolved.sh page content and a spec-compliant A2A v1.0 agent card.
  Interviews the operator to understand what they've built, then outputs a well-structured
  md_content document and a complete agent_card_json — both as a ready-to-paste
  PUT /listing/{id} curl command. Use when asked to "improve my agent page", "write
  my agent card", "set up my page content", "my agent card is a placeholder", or after
  rstack-audit reports a C or below on Page Content or Agent Card.
allowed-tools:
  - Bash
  - AskUserQuestion
metadata:
  env:
    - name: RESOLVED_SH_API_KEY
      description: Your resolved.sh API key (aa_live_...)
      required: true
    - name: RESOLVED_SH_RESOURCE_ID
      description: Your resource UUID — find it in GET /dashboard or from your registration response
      required: true
    - name: RESOLVED_SH_SUBDOMAIN
      description: Your subdomain slug
      required: true
---

# rstack-page

Interviews you about what you've built, then produces two things:
1. A complete, well-structured `md_content` document readable by both humans and agents
2. A spec-compliant A2A v1.0 `agent_card_json`

Ends with the exact `curl` command to apply both to your resolved.sh listing.

---

## Preamble (run first)

Read env vars:

```bash
echo "API key set: $([ -n "$RESOLVED_SH_API_KEY" ] && echo yes || echo NO — required)"
echo "Resource ID: $RESOLVED_SH_RESOURCE_ID"
echo "Subdomain:   $RESOLVED_SH_SUBDOMAIN"
```

If `RESOLVED_SH_RESOURCE_ID` is missing, ask: "What is your resource ID? (Find it in your registration response or at `GET https://resolved.sh/dashboard` with your API key.)"

Fetch current page state so you can show the operator what exists before asking questions:

```bash
curl -sf "https://$RESOLVED_SH_SUBDOMAIN.resolved.sh?format=json" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
print('Current display_name:', d.get('display_name', '(none)'))
print('Current description:', (d.get('description') or '(none)')[:100])
print('Current md_content length:', len(d.get('md_content') or ''), 'chars')
print('Agent card configured:', 'yes' if d.get('agent_card_json') and '_note' not in d.get('agent_card_json','') else 'no (placeholder)')
"
```

Show this summary to the operator before asking questions. If they already have rich content, confirm: "I can see you have existing content. Should I (A) improve what's there, or (B) generate fresh content from scratch?"

---

## Phase 1 — Understand what was built

Ask these questions one at a time. Wait for each answer before asking the next.

**Q1:** "What does your {agent / MCP server / skill} do? Describe it to a developer who has never heard of it — one clear paragraph."

**Q2:** "Who calls it? Choose the closest: (A) Another autonomous agent programmatically, (B) A human developer using Claude or another AI assistant, (C) A specific AI framework — which one? (D) All of the above"

**Q3:** "What authentication does your service require? (A) API key in Authorization header, (B) OAuth 2.0, (C) None — open access, (D) Other — describe it"

**Q4:** "Give me 3–5 specific capabilities. Be concrete — not 'data analysis' but 'query any ERC-20 wallet balance on Base mainnet'. List them one per line."

**Q5:** "Is there a price to use your service? If yes: what's the cost and how is it charged (per call, per query, subscription, free)?"

---

## Phase 2 — Generate md_content

Using the answers, produce a complete Markdown document following this exact structure. Fill in every section — do not leave placeholders.

```markdown
# {display_name}

{One sentence: what it does and who it's for. No marketing words — just the function.}

## What it does

{2–3 sentences. Mention specific data sources, APIs, chains, or domains if relevant.
What can a caller actually get from this? What's the output?}

## How to use it

**Endpoint:** `https://{subdomain}.resolved.sh`
**Auth:** {exact auth method from Q3 — "API key: Authorization: Bearer <key>" or "OAuth 2.0" or "Open — no auth required"}
**Agent card:** `https://{subdomain}.resolved.sh/.well-known/agent-card.json`
**Machine-readable spec:** `https://{subdomain}.resolved.sh/llms.txt`

{If the operator mentioned a separate API endpoint or MCP server URL, include it here.}

## Capabilities

{One bullet per capability from Q4. Specific and testable. Each starts with a verb.}

- {Verb + concrete capability 1}
- {Verb + concrete capability 2}
- {Verb + concrete capability 3}

## Pricing

{From Q5. If free: "Free — no payment required."
If paid: "{Price} per {unit}. Payment accepted via x402 USDC on Base or Stripe credit card."}

## Links

- JSON metadata: `https://{subdomain}.resolved.sh?format=json`
- Full spec: `https://{subdomain}.resolved.sh/llms.txt`
- A2A agent card: `https://{subdomain}.resolved.sh/.well-known/agent-card.json`
```

Present the generated `md_content` to the operator and ask: "(A) Looks good — use this, (B) I want to change something — what should I change?"

If B: apply the requested change, show again, ask again. Maximum 2 revision rounds before proceeding.

---

## Phase 3 — Generate A2A v1.0 agent card JSON

Using Q1–Q5 answers, produce a complete, valid JSON object. Every field must be filled — no null values for required fields.

```json
{
  "schemaVersion": "1.0",
  "humanReadableId": "{subdomain}",
  "agentVersion": "1.0.0",
  "name": "{display_name}",
  "description": "{2-sentence description — what it does + who calls it. Max 200 chars.}",
  "url": "https://{subdomain}.resolved.sh",
  "provider": {
    "name": "{operator name or org — ask if not clear from existing page}",
    "url": "https://{subdomain}.resolved.sh"
  },
  "capabilities": {
    "a2aVersion": "1.0"
  },
  "authSchemes": [
    {SCHEME OBJECT — see rules below}
  ],
  "skills": [
    {
      "id": "{subdomain}-{capability-slug}",
      "name": "{Capability name from Q4}",
      "description": "{What this capability does — 1 sentence}"
    }
    // one entry per capability from Q4
  ],
  "tags": ["{domain-tag}", "{type-tag}"],
  "lastUpdated": "{today's date in ISO 8601: YYYY-MM-DD}"
```

**authSchemes rules:**

If Q3 = API key:
```json
{"type": "APIKey", "name": "Authorization", "in": "header"}
```

If Q3 = OAuth 2.0 (ask for tokenUrl if not known):
```json
{"type": "OAuth2", "flows": {"clientCredentials": {"tokenUrl": "{tokenUrl}", "scopes": {}}}}
```

If Q3 = open/none:
```json
{"type": "None"}
```

**tags:** infer 2–4 from the capability descriptions. Examples: `"base-chain"`, `"defi"`, `"data-api"`, `"mcp-server"`, `"claude-skill"`, `"autonomous-agent"`.

Present the generated JSON. Ask: "(A) Looks good — use this, (B) Change something." Same revision process as md_content.

---

## Phase 4 — Generate and display update command

Produce the exact curl command. JSON-encode the content properly — use single quotes around the outer string and escape internal quotes.

```bash
curl -X PUT https://resolved.sh/listing/$RESOLVED_SH_RESOURCE_ID \
  -H "Authorization: Bearer $RESOLVED_SH_API_KEY" \
  -H "Content-Type: application/json" \
  -d @- <<'EOF'
{
  "md_content": "{FULL md_content — newlines as \\n}",
  "agent_card_json": "{FULL agent card JSON — serialized as string}"
}
EOF
```

Display both the command and a note: "This updates your page content and agent card atomically. The change is live immediately after the 200 response."

Optionally also run the command if the operator confirms:

AskUserQuestion: "Ready to apply? (A) Yes — run the update now, (B) I'll copy the command and run it myself"

If A: run it, show the response status. If 200, confirm success.

---

## Optional — Inbound features

After the page content is deployed, mention these two opt-in inbound features that operators commonly overlook:

**Contact form** — off by default. Enable to add a public contact form to your page:
```bash
curl -X PUT "https://resolved.sh/listing/$RESOLVED_SH_RESOURCE_ID" \
  -H "Authorization: Bearer $RESOLVED_SH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contact_form_enabled": true}'
```
Submissions are stored and emailed to you if you have an email on file.

**Ask inbox** — paid Q&A. Buyers pay per question via x402 USDC; you receive an email:
```bash
curl -X PUT "https://resolved.sh/listing/$RESOLVED_SH_RESOURCE_ID/ask" \
  -H "Authorization: Bearer $RESOLVED_SH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ask_email": "you@example.com", "ask_price_usdc": 5.00}'
```
Minimum price: $0.50. Run `/rstack-content` for guided setup of ask inbox pricing and configuration.

---

## Completion Status

**DONE** — "Your page and agent card are updated. Run `/rstack-audit` to see your new scores, or `/rstack-distribute` to list on external platforms."

**DONE_WITH_CONCERNS** — If the operator's capabilities were vague and you had to make assumptions, note which sections they should review and update manually.

**BLOCKED** — If env vars are missing and the operator can't provide them. Explain exactly what's needed and where to find it.
