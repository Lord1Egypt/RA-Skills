---
name: rstack-distribute
preamble-tier: 2
version: 1.0.0
description: |
  Generates listing artifacts for every relevant distribution channel after resolved.sh
  registration. Determines resource type (MCP server, skill, autonomous agent), then
  outputs ready-to-submit content for each applicable platform: Smithery, mcp.so,
  skills.sh, Glama, and community lists like awesome-a2a. Ends with a maintenance
  checklist. Use when asked to "list my agent", "distribute my MCP server", "get
  discovered", "where should I list this", or after rstack-audit reports distribution gaps.
allowed-tools:
  - Bash
  - WebSearch
  - AskUserQuestion
metadata:
  env:
    - name: RESOLVED_SH_SUBDOMAIN
      description: Your resolved.sh subdomain slug
      required: true
    - name: GITHUB_REPO
      description: Your GitHub repo URL (e.g. https://github.com/user/repo) — needed for Smithery and skills.sh
      required: false
---

# rstack-distribute

You're registered on resolved.sh. Now get discovered on the platforms where agents
and developers are actively searching for tools. This skill figures out which channels
apply to your resource and generates the exact content for each.

---

## Preamble (run first)

```bash
# Fetch page details
curl -sf "https://$RESOLVED_SH_SUBDOMAIN.resolved.sh?format=json" \
  -o /tmp/rstack_dist_page.json

python3 -c "
import sys, json
d = json.load(open('/tmp/rstack_dist_page.json'))
print('Display name:', d.get('display_name', '(none)'))
print('Description:', (d.get('description') or '(none)')[:120])
print('Registration:', d.get('registration_status', 'unknown'))
print('Has agent card:', 'yes' if d.get('agent_card_json') and '_note' not in str(d.get('agent_card_json','')) else 'placeholder')
print('Data files:', len(d.get('data_marketplace', {}).get('files', [])))
"
```

If `registration_status` is not `active` or `expiring`: "Your registration is not active. External platforms expect live, stable URLs. Register or renew first, then re-run `/rstack-distribute`." End with BLOCKED.

---

## Phase 1 — Classify the resource

AskUserQuestion: "What type of resource is this? Pick the closest match:

(A) **MCP server** — exposes tools via the Model Context Protocol that AI assistants can call
(B) **Claude skill / agent skill** — a SKILL.md-based capability installable via `claude skills add`
(C) **Autonomous agent** — runs independently, accepts tasks, has its own API endpoint
(D) **Data product** — primarily sells datasets (CSV, JSONL) via resolved.sh marketplace
(E) **Multiple** — tell me which combination"

Based on answer, build the channel list:

| Resource type | Applicable channels |
|---------------|-------------------|
| MCP server | Smithery, mcp.so, Glama |
| Claude skill | skills.sh |
| Autonomous agent | awesome-a2a, A2A discovery registries |
| Data product | resolved.sh marketplace (already done), HuggingFace cross-listing |
| All types | resolved.sh ✓ (already done) |

Show the operator which channels apply: "Based on your resource type, here are the platforms to target: {list}. I'll generate the listing content for each."

---

## Phase 2 — Get GitHub repo

If `$GITHUB_REPO` is not set and any channel in the list requires it (Smithery and skills.sh both need a GitHub repo):

AskUserQuestion: "Smithery and skills.sh both require a public GitHub repository. What's yours? (Paste the URL, or type 'skip' to skip these channels.)"

If skipped: remove Smithery and skills.sh from the channel list and note: "Skipping Smithery and skills.sh — you can come back to these once your code is on GitHub."

---

## Phase 3 — Generate listing artifacts

Generate each artifact one at a time. Present each to the operator for review before moving to the next.

---

### 3A. Smithery (MCP servers)

**What it is:** The primary MCP server registry. 2,000+ servers listed. Agents on Smithery actively discover and connect to MCP servers.

**Generate `smithery.yaml`:**

```yaml
name: "{subdomain}"
description: "{description from page — first 2 sentences, max 200 chars}"
version: "1.0.0"
```

**Steps to list:**

1. Add `smithery.yaml` to the root of your GitHub repo and push:
   ```bash
   # Save this to your repo root
   cat > smithery.yaml << 'YAML'
   {generated yaml content}
   YAML
   git add smithery.yaml && git commit -m "Add Smithery listing config" && git push
   ```

2. Go to https://smithery.ai and sign in with GitHub

3. Click "Claim server" and connect your repository

4. Navigate to the Deployments tab to activate your listing

**Verification:** After listing, your server will be discoverable at `https://smithery.ai/server/@{subdomain}` (or your GitHub username).

---

### 3B. mcp.so (Community MCP directory)

**What it is:** Community-driven MCP server directory. Lower barrier than Smithery — submit via GitHub issue.

**Generate submission text:**

```markdown
### Server Submission

**Name:** {display_name}
**Repository:** {github_repo}
**Description:** {description — 1-2 sentences}
**Category:** {inferred from capabilities — e.g., "Data & Analytics", "Developer Tools", "Finance"}
**Tags:** {3-5 tags}
**Homepage:** https://{subdomain}.resolved.sh
**Agent Card:** https://{subdomain}.resolved.sh/.well-known/agent-card.json
```

**Steps:** Go to https://mcp.so and click "Submit" in the navigation, or open a GitHub issue on the mcp.so repository with the above content.

---

### 3C. skills.sh (Agent skills registry)

**What it is:** The largest agent skills registry (90,000+ skills). Skills are installed via `npx skills add`. Discovery is usage-based — more installs = higher ranking.

**Generate `SKILL.md` for your repo root:**

```yaml
---
name: "{subdomain}"
description: |
  {2-3 sentences focused on WHEN Claude should invoke this skill.
  Start with the use case, not a description of what it is.
  Example: "Use when the user needs real-time DeFi swap data on Base mainnet.
  Queries Uniswap v3 pools, returns pricing and volume data, and supports
  historical lookups. Requires API_KEY env var."}
license: MIT
metadata:
  author: "{operator name}"
  version: "1.0.0"
---

# {display_name}

{Reuse the md_content from the resolved.sh page, or generate a concise version
focused on how an AI assistant should use this skill.}

## Setup

```bash
export {SUBDOMAIN_UPPER}_API_KEY="your-api-key"
```

## Usage

{2-3 example invocations showing what the user would say to trigger this skill}
```

**Steps:**
1. Save `SKILL.md` to your repo root and push
2. Anyone can install via: `npx skills add {github_username}/{repo_name}`
3. The skill appears on skills.sh automatically once installed

---

### 3D. Glama (MCP registry)

**What it is:** Comprehensive MCP registry with 2,000+ servers indexed.

**Steps:** Visit https://glama.ai and look for "Submit MCP Server" or join their Discord community for submission guidance. Include:
- Server name: {display_name}
- Repository: {github_repo}
- Homepage: https://{subdomain}.resolved.sh

---

### 3E. awesome-a2a (Agents with A2A cards)

**What it is:** Community-curated GitHub list of A2A-compatible agents.

**Generate PR addition line:**

```markdown
- [{display_name}](https://{subdomain}.resolved.sh) — {one-line description, max 80 chars}
```

**Steps:**
1. Find the awesome-a2a repository on GitHub (search "awesome-a2a" or "awesome-agent2agent")
2. Fork the repo
3. Add the line above to the appropriate category section
4. Open a pull request with title: "Add {display_name}"

---

### 3F. HuggingFace (Data products)

Only if the operator has data files on resolved.sh.

**What it is:** The largest AI/ML model and dataset hub. Cross-listing here creates a funnel: researchers discover on HF, purchase on resolved.sh.

**Steps:**
1. Create a dataset card on HuggingFace with your dataset's description and schema
2. In the dataset card, link to the resolved.sh purchase page:
   > "Full dataset available for purchase at https://{subdomain}.resolved.sh/data/{filename}"
   > "Free schema inspection: https://{subdomain}.resolved.sh/data/{filename}/schema"
3. Include sample rows (from the free schema endpoint) as a preview on HuggingFace

---

## Phase 4 — Summary and maintenance checklist

After presenting all artifacts, output the complete summary:

```
══════════════════════════════════════════════
  rstack distribute: {subdomain}.resolved.sh
══════════════════════════════════════════════

  Artifacts generated for:
  {✓ or — for each channel, with status}

  ✓ Smithery       smithery.yaml ready
  ✓ mcp.so         submission text ready
  ✓ skills.sh      SKILL.md ready
  — Glama          manual submission (see steps above)
  ✓ awesome-a2a    PR line ready
  — HuggingFace    cross-listing guide provided

══════════════════════════════════════════════
```

Then the maintenance table:

```
When you update...              | Also update...
--------------------------------|------------------------------------------
resolved.sh page content        | Nothing — it's the canonical source
  (PUT /listing/{id})           |
Agent card (agent_card_json)    | Nothing — agents re-fetch on discovery
Capabilities / MCP tools        | Smithery (re-deploy to update listing)
Skill trigger description       | skills.sh SKILL.md (push updated file)
Display name or description     | mcp.so (submit update issue if significant)
Data files (new upload/delete)  | HuggingFace dataset card (if cross-listed)
```

Key message: "Your resolved.sh page is the canonical source. External listings link back to it. Keep your resolved.sh page current and the ecosystem follows."

---

## Completion Status

**DONE** — "Listing artifacts generated for {N} channels. Submit them using the steps above. Run `/rstack-audit` in 48 hours to check if any listings have been indexed."

**DONE_WITH_CONCERNS** — If the operator skipped GitHub-dependent channels: "Skipped {channels} because no GitHub repo was provided. Once your code is public, re-run `/rstack-distribute` to generate those artifacts."

**BLOCKED** — If registration is not active, or if the page has no description and no md_content: "Your page needs content before listing on external platforms. Run `/rstack-page` first, then come back."
