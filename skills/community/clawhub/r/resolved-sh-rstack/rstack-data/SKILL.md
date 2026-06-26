---
name: rstack-data
preamble-tier: 2
version: 1.0.0
description: |
  Optimizes data files on a resolved.sh listing for discoverability and conversion.
  The free schema endpoint is the key conversion surface — buyers inspect it before
  paying. This skill makes descriptions compelling, verifies queryability, gives
  pricing strategy guidance, and adds a data showcase section to the operator page.
  Ends with ready-to-run PATCH commands for each file and a PUT command for the page.
  Use when asked to "improve my dataset", "set up data sales", "optimize my data
  listing", "help me sell my CSV", or after rstack-audit reports gaps in Data Marketplace.
allowed-tools:
  - Bash
  - AskUserQuestion
metadata:
  env:
    - name: RESOLVED_SH_API_KEY
      description: Your resolved.sh API key (aa_live_...)
      required: true
    - name: RESOLVED_SH_RESOURCE_ID
      description: Your resource UUID
      required: true
    - name: RESOLVED_SH_SUBDOMAIN
      description: Your subdomain slug
      required: true
---

# rstack-data

The resolved.sh schema endpoint (`/data/{filename}/schema`) is free for buyers to call.
It's their first look at your data before committing to a purchase. This skill makes that
first look compelling — and generates the commands to apply every improvement.

---

## Preamble (run first)

```bash
# Fetch current data files
curl -sf "https://resolved.sh/listing/$RESOLVED_SH_RESOURCE_ID/data" \
  -H "Authorization: Bearer $RESOLVED_SH_API_KEY" \
  -o /tmp/rstack_files.json

echo "Current data files:"
cat /tmp/rstack_files.json | python3 -c "
import sys, json
d = json.load(sys.stdin)
files = d.get('files', [])
if not files:
    print('  (none)')
else:
    for f in files:
        print(f'  {f[\"filename\"]} | \${f[\"price_usdc\"]} | desc: {len(f.get(\"description\") or \"\")} chars')
"
```

If no files exist, ask: "You have no data files yet. Do you have datasets to sell? (A) Yes — let's set up your first one, (B) No — nothing to optimize here"

If B: respond "Nothing to do here yet. Come back when you have data files to upload." and end with DONE.

For each file, also fetch its schema:

```bash
for FILENAME in $(cat /tmp/rstack_files.json | python3 -c "
import sys, json
d = json.load(sys.stdin)
for f in d.get('files', []): print(f['filename'])
"); do
  echo "=== schema: $FILENAME ==="
  curl -sf "https://$RESOLVED_SH_SUBDOMAIN.resolved.sh/data/$FILENAME/schema"
  echo
done
```

Parse queryability (`queryable: true/false`) and existing column names for each file.

---

## Phase 1 — Understand the data (per file with thin or missing description)

For each file where description is missing or fewer than 60 characters, ask these questions. One file at a time, one question at a time.

**Q1:** "Describe `{filename}` in plain English: what domain is it in, what does each row represent, and approximately how many rows are there?"

**Q2:** "What are the most important column names and what do they mean? List the 3–5 most valuable ones."

**Q3:** "Who is the ideal buyer? What would they do with this data? Give me a concrete use case."

**Q4:** "Where did this data come from — and how fresh is it? (source, collection method, update frequency)"

---

## Phase 2 — Evaluate each file

For each file, assess:

**Description quality:**
- Does it mention the domain? (e.g., "DeFi", "e-commerce", "weather")
- Does it describe what a row represents?
- Does it name the key columns?
- Does it give ≥2 concrete use cases?
- Is it ≥80 chars?

**Queryability:**
- Is `queryable: true` in the schema response?
- If not: is the file a CSV or JSONL? (These should be queryable — if they're not, the file may need to be re-uploaded with proper formatting. Note this as a concern.)
- If yes: are the column names descriptive? (e.g., `wallet_address` good; `col1` bad)

**Pricing fit:**
- < $0.01: invalid (minimum is $0.01 via x402)
- $0.01–$0.49: x402 only — Stripe won't process. Good for high-frequency agent queries where volume matters.
- $0.50–$5.00: sweet spot — works for both x402 and Stripe. Good for AI researchers and developer buyers.
- $5.01–$25.00: human/enterprise range. Stripe path required. Needs a very strong description and provenance story to justify.
- > $25.00: premium pricing. Only works with unique, hard-to-replicate data. Flag if description doesn't justify it.

**Split pricing** (queryable files only):
- Does the file have both query and download access paths?
- If `query_price_usdc` is not set, per-row queries cost the same as a full download (`price_usdc`) — which is almost always wrong for queryable files.
- Flag files where `price_usdc` ≥ $0.50 but `query_price_usdc` is not set: buyers doing per-row queries are being charged full-download prices.
- Recommended pattern: low `query_price_usdc` ($0.01–$0.10) to drive agent query volume + higher `download_price_usdc` or `price_usdc` ($1–$10) for human buyers who want the full file.

---

## Phase 3 — Generate improved descriptions

For each file needing improvement, write a description using this template:

> "{Domain} dataset: {row count if known, otherwise "dataset"} of {what each row represents}. Key columns: {3–5 column names with brief descriptions}. Use cases: {2–3 specific, concrete use cases — name the exact task}. Source: {provenance}. Updated: {frequency}."

**Example of a weak description:**
> "Transaction data with wallet info"

**Example of a strong description:**
> "DeFi swap dataset: ~180K Uniswap v3 swap events on Base mainnet. Key columns: timestamp (unix ms), pool_address, token_in_symbol, token_out_symbol, amount_usd, wallet_address. Use cases: MEV pattern detection, wallet behavior clustering, liquidity pool performance analysis. Source: on-chain event logs via Alchemy. Updated: daily."

The description should make a buyer want to call the schema endpoint even before deciding to purchase.

---

## Phase 4 — Generate sample queries for page showcase

For each queryable file, generate a sample query that demonstrates the data's value. The query should show a realistic buyer use case.

```
# Free: inspect the schema before paying
GET https://{subdomain}.resolved.sh/data/{filename}/schema

# Paid query via x402 ($0.01/query) — {description of what this returns}
GET https://{subdomain}.resolved.sh/data/{filename}/query?{filter_col}={example_val}&_select={col1},{col2},{col3}&_limit=10

# Supported filter operators:
#   col=value           exact match
#   col__gt=n           greater than
#   col__lt=n           less than
#   col__gte=n          greater than or equal
#   col__lte=n          less than or equal
#   col__in=a,b,c       set membership
#   col__contains=val   substring match
```

Use real column names from the schema. Make the example query answer a specific business question (e.g., `?wallet_address=0xabc&amount_usd__gt=1000` to find a wallet's large swaps).

---

## Phase 5 — Generate update commands

**PATCH command for each file (update description and/or split pricing):**

```bash
# Replace {file_id} with the id from GET /listing/{resource_id}/data
curl -X PATCH "https://resolved.sh/listing/$RESOLVED_SH_RESOURCE_ID/data/{file_id}" \
  -H "Authorization: Bearer $RESOLVED_SH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "{improved description}",
    "query_price_usdc": {per-row query price, e.g. 0.01 — omit to leave unchanged},
    "download_price_usdc": {full file download price — omit to leave unchanged}
  }'
```

**Split pricing notes:**
- Omit `query_price_usdc` or `download_price_usdc` entirely to leave those values unchanged.
- Send `0` for either field to clear the override and fall back to `price_usdc` for that access type.
- If you only want to update the description, send only `{"description": "..."}`.

Generate one command per file that needs updating. Show them all together so the operator can run them in sequence.

**PUT command to add/update a Data section in md_content:**

Fetch the current md_content first, then append or update a `## Data` section:

```bash
# Check current md_content
curl -sf "https://$RESOLVED_SH_SUBDOMAIN.resolved.sh?format=json" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('md_content') or '(none)')"
```

Generate a `## Data` section to add:

```markdown
## Data

| Dataset | Description | Price |
|---------|-------------|-------|
| [{filename}](https://{subdomain}.resolved.sh/data/{filename}/schema) | {first 80 chars of description} | ${price}/query |

Free schema inspection: `GET https://{subdomain}.resolved.sh/data/{filename}/schema`

Sample query:
\`\`\`
GET https://{subdomain}.resolved.sh/data/{filename}/query?{key_col}={example_val}&_select={col1},{col2}&_limit=5
\`\`\`
Buyers pay per query via x402 USDC on Base or Stripe. Schema inspection is always free.
```

Show the operator the full PUT command with the updated md_content.

---

## Phase 6 — Pricing recommendations (if applicable)

If any file's pricing looks suboptimal based on Phase 2 assessment:

- **File is priced at $0.01–$0.10 but isn't queryable (download-only):** "Consider re-uploading as a structured CSV/JSONL to enable querying. Per-query pricing at low prices drives 10–100x more revenue than one-time downloads of the same file."
- **File is priced above $5 but description doesn't justify it:** "Your pricing is in the human/enterprise range but your description doesn't explain the data's unique value. Either lower the price or strengthen the description — buyers at this price point need a compelling reason."
- **File is priced below $0.50 and relies on Stripe buyers:** "Note: Stripe requires a minimum of $0.50. x402 handles sub-$0.50 pricing. If you want Stripe buyers (human researchers, developers), consider pricing at $0.50+."
- **Queryable file with no split pricing and `price_usdc` ≥ $0.50:** "Consider split pricing: set `query_price_usdc` to $0.01–$0.10 for per-row agent queries and keep the higher `price_usdc` as the download price. Without split pricing, every query costs the full download price — most agents won't pay that."

---

## Completion Status

**DONE** — All files have strong descriptions and update commands are generated. "Run the PATCH commands above, then `/rstack-audit` to re-score your Data Marketplace grade."

**DONE_WITH_CONCERNS** — If any files are not queryable (CSV/JSONL but `queryable: false`): "⚠ {filename} is not queryable. This likely means the file wasn't parsed as structured data. To enable querying, delete and re-upload the file. Queryable files earn significantly more because buyers can pay $0.01/query vs. $X for a one-time download."

**BLOCKED** — If API key is missing or the data endpoint returns an auth error.
