# Session Transcripts (aligning the AI on "how to use it + how to report")

> Tone/granularity samples for user-facing summaries. Real output always comes from the script JSON; report with "conclusion first, then key points, ask whether details are wanted". Security-relevant actions (login, write pass-through, running installers) must be restated to the user and explicitly consented to first.

## Example 1: AIP NLQ query (first-use scenario, incl. install guidance)

**User**: I want sales ranking by region, and I haven't installed the ZY Action platform yet.

**AI**:
- Not installed → install guidance (SKILL.md section 3): open https://zyinfo.pro/action/ and download the **versioned** artifact (e.g. `ZY-Action-Platform_v2026.09.rar`); run `verify-artifact --file <file> --sha256 <official value>` until `"match": true`, then verify the digital signature (expected publisher: ZY Tech / zyinfo.pro); restate the artifact name and both results to the user and **extract/run only after consent**. After extracting, copy `config.yaml.example` to `config.yaml`, fill the DeepSeek key at `llm.api_keys.deepseek`; if no PostgreSQL locally, change `database.type` to `SQLite`; double-click the launcher exe to start.
- After the user confirms it's up, run in order (login previews its destination with --dry-run and gets consent first):

```bash
python3 scripts/zy_platform.py health --product aip
python3 scripts/zy_platform.py login --product aip --username <user> --password <pass> --dry-run   # show destination → user consents →
python3 scripts/zy_platform.py login --product aip --username <user> --password <pass>
python3 scripts/zy_platform.py chat --product aip --query "Top 5 sales by region"
```

**AI report**: Ranked high-to-low by region: ① East X ② South Y …. SQL is `SELECT ...`, confidence 0.97 (show if asked). Want a chart or a drill-down into one region?

## Example 2: AIP workflow — list → run → poll

**User**: Run the "inventory replenishment suggestion" automation for me.

**AI**:
```bash
python3 scripts/zy_platform.py workflow-list --product aip
python3 scripts/zy_platform.py workflow-run --product aip --workflow-id <id> --params '{"region":"east"}'
python3 scripts/zy_platform.py workflow-status --product aip --execution-id <eid>
```
**AI report**: Workflow `<name>` completed (execution_id `xxxx`), status `completed`, all 4 nodes succeeded. Key conclusion: 3 SKUs in the East region are below reorder point; suggested restock total ≈ …. Show per-node output?

## Example 3: Cross-product + reading bundled docs from the install dir

**User**: The platform is installed at D:\zyaction. Check whether Foundry has an "order" ontology, then search Gotham for intel about "Xuanwu Group".

**AI** (read the install-dir docs first, then call):
```bash
# 1) Read D:\zyaction\README.md for ports/accounts; docs\manuals and api-demo samples when needed
# 2) Direct verification and login (preview the destination with --dry-run and get consent first)
python3 scripts/zy_platform.py health --product foundry
python3 scripts/zy_platform.py login --product foundry --username <user> --password <pass> --dry-run
python3 scripts/zy_platform.py login --product foundry --username <user> --password <pass>
# 3) Ontology object types; find "order"
python3 scripts/zy_platform.py ontology-objects --product foundry
python3 scripts/zy_platform.py ontology-search --product foundry --query "order"
# 4) Gotham intel search (each product logs in independently)
python3 scripts/zy_platform.py search --product gotham --query "Xuanwu Group" --limit 5
```
**AI report**: Foundry ontology includes `order (sales order)` etc. with 2 related metrics; Gotham found 5 hits: 1 resolved entity, 2 timeline events (incl. "Xuanwu Group executive meeting"), 2 map points. Expand a domain / generate a brief?

## Example 4: Read-only pass-through + session wrap-up

**User**: Show me what's in the metric catalog, then clear my login state when done.

**AI**:
```bash
# read-only pass-through (GET allowed by default; add --with-token after consent when auth is needed)
python3 scripts/zy_platform.py request --product foundry --method GET --path=metrics/catalog --with-token
# write pass-through (if needed): first --dry-run to show method/URL/body → user consents → --allow-write for real
# python3 scripts/zy_platform.py request --product aip --method POST --path=chat \
#   --data '{"query":"..."}' --dry-run
# python3 scripts/zy_platform.py request --product aip --method POST --path=chat \
#   --data '{"query":"..."}' --allow-write
# wrap-up: log out and clear the cached token
python3 scripts/zy_platform.py logout --product foundry
```
**AI report**: The metric catalog has N entries (list a few key ones); logged out and the local cached token has been removed.

## Common Failures & Suggested Wording

- Exit 2 (unreachable) → "The platform doesn't seem to be running; double-click the launcher and tell me to retry, or check --product port / --base-url." (If stderr mentions a **certificate verification failure**, the remote https certificate is self-signed/expired/mismatched — ops must fix it; don't bypass.)
- Exit 4 (401) → "The login has expired; please provide the platform account credentials again and I'll login once more (I'll dry-run the destination for you first)."
- Exit 1 with "security policy" in stderr → follow the prompt: restate to the user (remote-origin confirmation / write confirmation / why the path is outside the allowlist), then retry with `--trust-host`/`--allow-write` after consent or switch to a built-in command.
- Business code≠0 with an LLM hint → "Check that `llm.api_keys.deepseek` in the install dir's config.yaml holds a real key, then restart the platform."
- 404 → "This version may not have that endpoint / the route name differs. Try the real path with `request` against the bundled `API 接入及测试方法参考.txt` (within the read-only allowlist)."
