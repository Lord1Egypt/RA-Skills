# Delivery Diagnosis Template — Date: {{DATE}}

## Pre-flight
- [ ] Read `v3-compiled-{{DATE}}.json`
- [ ] Read `v3-closure-state-{{DATE}}.json`
- [ ] List recovery tickets in `recovery-tickets-v3/{{DATE}}/`
- [ ] Read `automated-recovery-loop-v1.md` and `blocker-recovery-contract-v1.md`

## Layer Checks (in order)

### 1. Hunter Raw
**Expected:** pain-map, selection-layer, intel-pack, delivery-receipt  
**Check paths:**
- `social-intel/pain-map-{{DATE}}.md`
- `social-intel/selection-layer-{{DATE}}.md`
- `social-intel/intel-pack-{{DATE}}.json`
- `social-intel/delivery-receipt-{{DATE}}.md`

**Status:** ___  
**If missing:** Create recovery ticket `rt-{{DATE}}-hunter-01`, classify `missing_artifact`

---

### 2. JK Processed
**Expected:** jk-content-writer-output-{{DATE}}.md + jk-processed-receipt-{{DATE}}.json  
**Check paths:**
- `content-delivery/jk-content-writer-output-{{DATE}}.md`
- `content-delivery/jk-processed-receipt-{{DATE}}.json`

**Status:** ___  
**If delivered after deadline:** Mark `DELIVERED_LATE`, close ticket if open

---

### 3. Elon X
**Expected:** Live X post URL + acceptance receipt  
**Check paths:**
- `social-packs/elon-social-pack-{{DATE}}-morning.json`
- Any X receipt with live URL

**Blocking layer:** ___ (NONE / GENERATED_NOT_PUBLISHED / TOOL_FAILURE / missing_proof)  
**Recovery action if GENERATED_NOT_PUBLISHED:**
1. Verify social pack exists
2. Construct Postiz payload for X
3. RUN: `node scripts/postiz-publish.mjs --input /tmp/postiz-x.json --output /tmp/postiz-x-receipt.json`
4. If success → capture URL → write acceptance receipt
5. Update ticket `rt-{{DATE}}-elon-01`

**Max attempts:** 3. Escalate on failure.

---

### 4. Elon LinkedIn
Same pattern as Elon X, platform=linkedin.

---

### 5. Mark Facebook
**Expected:** Published post URL + engagement check receipt  
**Check paths:**
- `mark/receipts/mark-*-{{DATE}}.json`
- `workspace-elon/receipts/facebook-*-latest.json`

**Blocking layer:** ___  
**Recovery action if TOOL_FAILURE:**
1. Check auth: `node scripts/facebook-verify-browser-use.mjs --check-auth`
2. If auth ok → retry `node scripts/facebook-poster.mjs --file /tmp/fb-post.txt`
3. If auth fail → `human_required`

---

### 6. Tony Blog
**Expected:** source-publish receipt + blog QA receipt  
**Check paths:**
- `content-delivery/tony-content-artifact-{{DATE}}.md`
- `content-delivery/tony-asset-check-{{DATE}}.json`
- `content-delivery/tony-blog-preflight-{{DATE}}.json`
- `tony-blog-source-publish-{{DATE}}.json`
- `blog-qa-receipt-{{DATE}}.json`

**Recovery action if all inputs ready but no publish:**
1. RUN: `node scripts/tony-blog-publish.mjs --date {{DATE}}`
2. After publish → verify live URLs
3. Write `blog-qa-receipt-{{DATE}}.json`
4. Update ticket `rt-{{DATE}}-tony-01`

---

### 7. Peter Deploy
**Expected:** deploy receipt + live verification  
**Check:** `peter-inserted-slug-handoff-{{DATE}}.json`  
**If Tony source-publish missing:** No action. Update ticket state `UPSTREAM_MISSING`.
**If Tony source-publish appears:** RUN `node scripts/peter-blog-closeout-verify.mjs --date {{DATE}}`

---

### 8. Jenny Activation
**Expected:** activation execution receipt + acceptance receipt  
**Check:** `workspace-jenny/.env` for `supabaseUrl`  
**Recovery action:**
- If config missing → `human_required`, write blocker receipt
- If config ok → RUN activation batch script, capture log

---

### 9. Tully SEO
**Expected:** `tully-daily-delivery-{{DATE}}.json` + /skills/ pages  
**If v3-compiled shows NOT_IN_SCOPE but artifacts exist:** File bug note. Preserve delivered truth.

---

## Post-Diagnosis

### Write Outputs
- [ ] `delivery-diagnosis-{{DATE}}-HHMM.json` → `mission-control/data/`
- [ ] Update all recovery tickets with `DIAGNOSIS` log entry
- [ ] If recovery script executed → add `RECOVERY_ATTEMPT` log entry
- [ ] If state changed → update `status`, `recoveryState`, `updated_at`

### Summary Format
```json
{
  "date": "{{DATE}}",
  "compiledAt": "ISO",
  "lanes": [
    {
      "lane": "...",
      "status": "DELIVERED|DELIVERED_LATE|BLOCKED|...",
      "blocking_layer": "...",
      "recovery_action": "...",
      "escalate": true|false
    }
  ],
  "summary": {
    "total_lanes": 9,
    "delivered": 0,
    "blocked": 0,
    "escalation_required": []
  }
}
```

## Acceptance Rule

This diagnosis is complete only when:
1. Every in-scope lane has been checked
2. Every blocked lane has a concrete recovery action (not "follow up later")
3. Every recovery ticket has been updated with this run's log entry
4. The diagnosis file has been written to disk
5. Escalation conditions are explicitly stated
