# ray-delivery-diagnosis

## Purpose

Recovery ticket runner and delivery diagnosis agent. Runs every 4 hours (and on-demand) to scan all delivery lanes, detect unresolved blockers, classify failure type, and execute concrete recovery actions.

## Trigger

- Cron: `recovery-ticket-runner-4hourly`
- Also called by: `peter-deployment-recovery`, `social-post-failure-recovery-morning`, `social-post-failure-recovery-evening`

## Input

- Date (default: today Asia/Shanghai)
- `v3-compiled-YYYY-MM-DD.json`
- `v3-closure-state-YYYY-MM-DD.json`
- Recovery tickets in `mission-control/data/recovery-tickets-v3/YYYY-MM-DD/`
- Agent summaries

## Layer Check Order (MUST follow in order)

1. **Hunter raw** — pain-map, selection-layer, intel-pack, delivery-receipt
2. **JK processed** — content writing package, processed receipt, source grounded
3. **Elon X** — social pack, live X URL, visibility proof, acceptance receipt
4. **Elon LinkedIn** — social pack, live LinkedIn URL, visibility proof
5. **Mark Facebook** — published post URL, engagement check receipt
6. **Tony blog** — drafts, artifact, ASSET_CHECK, source-publish receipt, blog QA receipt
7. **Peter deploy** — inserted-slug handoff, deploy receipt, live verification
8. **Jenny activation** — activation batch executed, receipt, ASSET_CHECK
9. **Tully SEO** — /skills/ pages written, skill-pages.ts updated, receipt

## Failure Classification

| Class | Meaning | Example |
|-------|---------|---------|
| `missing_proof` | Work happened, proof missing | Post exists but no URL captured |
| `execution_blocked` | Script/tool failed | API timeout, auth error |
| `missing_artifact` | Upstream output missing | No Tony drafts for today |
| `partial_success_with_debt` | Some done, chain incomplete | X posted but acceptance missing |
| `aggregate_coupling_failure` | Child success lost in aggregate | X done but social lane blocked |
| `human_required` | Stop automation, wait for human | Account risk, policy issue |

## Recovery Actions by Lane

### Tony Blog — `GENERATED_NOT_PUBLISHED`
- Check inputs: `tony-content-artifact-YYYY-MM-DD.md`, `tony-asset-check-YYYY-MM-DD.json`, `tony-blog-preflight-YYYY-MM-DD.json`
- If all inputs exist → RUN: `node scripts/tony-blog-publish.mjs --date YYYY-MM-DD`
- After publish → run blog QA → write `blog-qa-receipt-YYYY-MM-DD.json`
- Max attempts: 3 auto; escalate on attempt 4

### Elon X / LinkedIn — `GENERATED_NOT_PUBLISHED`
- Check input: `social-packs/elon-social-pack-YYYY-MM-DD-morning.json`
- If input exists → construct Postiz payload → RUN: `node scripts/postiz-publish.mjs --input /tmp/postiz-x.json --output /tmp/postiz-x-receipt.json`
- Capture live URL + screenshot → write acceptance receipt
- Max attempts: 3 auto; escalate on attempt 4

### Mark Facebook — `TOOL_FAILURE`
- Check auth: `node scripts/facebook-verify-browser-use.mjs --check-auth`
- If auth ok → retry publish with `node scripts/facebook-poster.mjs --file /tmp/fb-post.txt`
- If auth failed → classify `human_required`, write blocker receipt
- Max attempts: 2 auto

### Jenny Activation — `TOOL_FAILURE`
- Check config: `~/.openclaw/workspace-jenny/.env` must contain `supabaseUrl`
- If missing → classify `human_required` (Ray must fix config)
- If config ok → RUN: `node workspace-jenny/scripts/jenny/send-activation-batch.mjs batch`
- Max attempts: 2 auto

### Peter Deploy — `UPSTREAM_MISSING`
- No action until Tony source-publish completes
- Auto-check every run: if `tony-blog-source-publish-YYYY-MM-DD.json` appears → RUN: `node scripts/peter-blog-closeout-verify.mjs --date YYYY-MM-DD`

### Tully SEO
- If delivered but `v3-compiled` shows `NOT_IN_SCOPE` → file v3-compiled bug note, do not downgrade lane

## Ticket Update Rules

For every run:
1. Read existing ticket from `recovery-tickets-v3/YYYY-MM-DD/rt-YYYY-MM-DD-{lane}-NN.json`
2. Append runner log entry with `action: DIAGNOSIS` or `action: RECOVERY_ATTEMPT`
3. If recovery script executed → add `attempt_log` entry with result
4. If state changed → update `status`, `recoveryState`, `updated_at`
5. If `max_attempts` reached → `status: ESCALATED`, notify

## Output

- Write `delivery-diagnosis-YYYY-MM-DD-HHMM.json` to `mission-control/data/`
- Update recovery tickets
- Write runner log to `recovery-runner-log/`
- If escalation triggered → update Mission Control attention-required

## Non-Goals

- Do not rewrite historical receipts into fake success
- Do not mask missing delivery with older historical wins
- Do not publish without brand gate pass
- Do not retry indefinitely; respect max_attempts

## Safety

- Always prefer `--dry-run` first when testing a new publish path
- For external publish (X, LinkedIn, Facebook, blog), verify content with brand-positioning-tony.md before executing
- If auth/credential issue → `human_required`, do not brute-force
