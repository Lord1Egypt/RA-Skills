---
name: skill-install-firewall
description: >-
  Screen any agent skill or MCP server BEFORE it lands in the fleet: compare the
  declared manifest against actual behavior, flag injection and credential
  patterns, and emit a pass/fail verdict with evidence. Use when installing
  skills from a marketplace, vendoring an MCP server, or when a fleet rule
  requires a pre-install security gate.
version: 1.0.0
metadata:
  triggers: |-
    is this skill safe to install
    vet this skill before install
    screen this MCP server
    pre-install security gate
    audit a skill package
  kind: guardrail
  openclaw:
    requires:
      bins:
        - curl
    envVars:
      - name: DDG_AGENT_ID
        required: false
        description: Stable agent identity sent as X-Agent-Id; the skill-safety scan is agent-only, so set this for the hosted pass.
    homepage: https://agents.daedalusdevelopmentgroup.com
    emoji: "🧱"
allowed-tools: Bash, Read, Grep
---

# Skill Install Firewall

Marketplaces are the new supply chain: audit programs report ~80% of skills
declaring one behavior and shipping another, and millions of malicious-skill
downloads. The cheapest moment to catch a hostile skill is BEFORE install —
after it is in the fleet, every session is a potential incident. This gate
turns "looks fine to me" into a recorded verdict.

**Endpoints:** `POST /v1/ai-skill-safety-scan` (**free** during the launch
promo, `X-Agent-Id` required), `POST /v1/mcp-tool-security-audit` ($0.01),
both on `https://agents.daedalusdevelopmentgroup.com`.

**External cost:** the skill-safety scan costs $0.00 during the launch promo;
the MCP tool audit is $0.01 per call in USDC on Base via x402. No account or
API key is required; the paid path needs an x402-capable client.

## Procedure

1. **Collect the artifact.** The skill directory (SKILL.md + scripts) or the
   MCP server's tool list. Never install first "to look at it".
2. **Local pass (free).** Grep for the classic tells: `curl | sh`, base64
   blobs piped to a shell, credential literals (`api_key=`, `token=`),
   env-var exfiltration, `sudo` inside skill scripts, network calls to
   non-declared hosts. Record file+line for each hit.
3. **Hosted pass (the part that catches declaration mismatch).**
   ```bash
   curl -s -X POST https://agents.daedalusdevelopmentgroup.com/v1/ai-skill-safety-scan \
     -H 'content-type: application/json' -H "X-Agent-Id: $DDG_AGENT_ID" \
     -d '{"skill":"<name@version>","declared":"<what the manifest claims>","files":"<SKILL.md + scripts text>"}' \
     > out/scan.json
   ```
   For MCP servers, submit the tool list to `/v1/mcp-tool-security-audit`
   ($0.01) instead: tool-risk matrix, dangerous capability flags, auth
   boundary.
4. **Verdict rules.** Any critical finding → BLOCK (do not install; keep the
   report). Medium → WARN (install only with the finding recorded in the
   fleet changelog). Clean + scan id → ALLOW, and record the scan id next to
   the pinned version.
5. **Re-screen on update.** A skill that passed at v1.2 is a different
   artifact at v1.3. Re-run step 3 on every version bump; diff the reports.

## Findings schema

```json
{"artifact": "name@version", "local_hits": [{"file": "...", "line": 12,
 "kind": "curl_pipe_shell"}], "scan_id": "...", "verdict": "BLOCK|WARN|ALLOW",
 "critical": 0, "medium": 2, "evidence_url": "..."}
```

## Failure handling

- `403 agent_only` = the scan route requires an agent identity header; set
  `X-Agent-Id` and retry — no unit or money is consumed by the refusal.
- `422` = the body is wrong (no files/skill text); fix and resend.
- `503` = backend unavailable, no charge; retry with backoff.
- Never paste live secrets into a scan body: findings are redacted, but the
  request still leaves your machine — scan diffs and rotated-out values.

## Rules

- Screen BEFORE install, not after — post-install scans find incidents, not risks.
- Declared behavior is a claim; the scan is evidence. When they disagree, believe the scan.
- Record the verdict + scan id; an unrecorded ALLOW is indistinguishable from no check.
- One package per verdict; never batch-approve a marketplace category.

## Not for

- Runtime incident response after a skill already ran (that is forensics, not a gate).
- Grading your own first-party skills you wrote and version-control yourself.
- Code review of ordinary application repos — this is for installable agent artifacts.

## Example

**Ask:** "Install the `crypto-tips` skill from the marketplace for me."

**Before:** agent installs it; the skill ships an undeclared `curl | sh` and a
wallet-key regex; first run exfiltrates a key from the env.

**After:** local grep flags the pipe-to-shell line; the DDG scan returns
critical: 1 (undeclared network + credential read), verdict BLOCK; the user
gets the report and the install never happens.

## Version

1.0.0 — initial staged draft (pre-install gate: local heuristics + hosted scan verdict).
