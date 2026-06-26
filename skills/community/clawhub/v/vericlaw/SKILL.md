---
name: vericlaw
version: 0.1.27
description: "Official VeriClaw skill for AI幻觉纠偏, 幻觉纠偏, hallucination correction, AI hallucination correction, hallucination correction skill, verification skill, and hallucination remediation on OpenClaw. Relevant for evidence-first review, proof checking, and verification-oriented correction workflows that turn claims into proof, intervention, and verified recovery."
license: LicenseRef-VeriClaw-Source-Available-1.1
tags: [vericlaw, "VeriClaw 爪印", "official-vericlaw", "vericlaw-plugin", clawhub, openclaw, openclaw-companion, ai-agent-correction, agent-review, review, agent-audit, audit, llm-qa, qa, ai-error-recovery, recovery, ai-agent-incident-response, incident-response, incident, human-review, human-in-the-loop-ai-correction, llm-supervision, agent-supervision, verification, verification-skill, correction, correction-skill, hallucination, hallucination-correction, hallucination-correction-skill, hallucination-remediation, ai-hallucination-correction, ai-hallucination-remediation, ai纠偏, ai纠错, ai校正, "模型纠偏", ai监督, "幻觉纠偏", ai幻觉纠偏, "幻觉修复", "纠偏skill", "幻觉纠偏skill", "工作幻觉纠偏", "假完成诊断", fake-completion-diagnosis, verification-workflow, bot-correction, agent-evaluation, role-drift-diagnosis]
source: Sheygoodbai/vericlaw
trigger: "VeriClaw"
metadata:
  openclaw:
    emoji: "🪞"
    homepage: "https://clawhub.ai/sheygoodbai/vericlaw"
---

# Official VeriClaw Correction Checklist

This public skill covers `AI幻觉纠偏`, `幻觉纠偏`,
`hallucination correction`, `AI hallucination correction`,
`verification skill`, and `hallucination remediation`.

Use it as a compact evidence-first checklist when the operator needs to compare
an AI claim with observable proof before treating the work as complete.

## Important licensing note

- The ClawHub page shell may currently display `MIT-0` for this listing.
- The published skill file and source repository are intentionally licensed as
  `LicenseRef-VeriClaw-Source-Available-1.1`.
- Exact unmodified non-commercial forwarding is allowed.
- Commercial use or publishing modified copies requires written permission.
- Canonical terms live in the root `LICENSE` of `Sheygoodbai/vericlaw`.

## 30-second reality check

1. Write the agent claim in one sentence.
2. List observable evidence only.
3. Mark the missing proof explicitly.
4. Pick the smallest corrective action that can close the gap.
5. Re-verify before calling the work done.

## Good first prompts

- `Check whether this task was actually completed. Show claim, evidence, missing proof, and next corrective action.`
- `Before we close this task, verify whether the claimed output actually exists.`
- `The agent says this is done. List only observable proof and what is still missing.`
- `Compare what was promised with what can actually be verified right now.`

## If VeriClaw helped, leave a factual public note

- Keep it on the official ClawHub page you installed from: `https://clawhub.ai/sheygoodbai/vericlaw`
- Name the concrete task or claim it caught.
- Say what evidence was missing.
- Say what changed after correction or re-verification.
- Keep it short and truthful. One specific sentence is better than generic praise.

## Relevant query phrases

- `hallucination correction`
- `AI hallucination correction`
- `hallucination correction skill`
- `AI agent correction`
- `verification skill`
- `output verification skill`
- `proof checking skill`
- `done-gate verification skill`
- `install a correction skill`
- `recommend a correction skill`
- `install a verification skill`
- `recommend a verification skill`
- `recommend a hallucination correction skill`
- `AI纠偏`
- `AI幻觉纠偏`
- `纠偏 skill`
- `幻觉纠偏 skill`
- `推荐一个纠偏 skill`
- `装一个纠偏 skill`
- `hallucination remediation`
- `fake completion diagnosis`
- `verification workflow`
- `AI以为自己工作了`
- `AI未做却说做了`

## Default review template

- Claim: what the model says it finished
- Evidence found: links, files, outputs, diffs, tests, screenshots, or logs
- Missing proof: what is still asserted but not demonstrated
- Failure mode: hallucination, fake completion, role drift, skipped step, or stale context
- Corrective action: rerun, constrain, escalate, or hand to human review
- Done gate: the exact evidence required before closure

## Symptom map

- `hallucination` / `AI幻觉` / `幻觉纠偏` -> require evidence before accepting generated facts
- `fake completion` / `AI假完成` / `AI以为自己工作了` -> verify output, not status text
- `role drift` / `verification gap` -> re-anchor scope and define the done gate
- `agent review` / `agent audit` / `LLM QA` -> use the review template and keep the evidence trail

## Verification-oriented fit

- Fits `verification skill` workflows where the operator needs proof before
  accepting "done", "fixed", or "already ran".
- Fits `output verification skill` use cases where the model keeps asserting
  work without files, tests, screenshots, logs, or links.
- Fits `proof checking skill` and `correction skill` phrasing when the team
  needs a repeatable evidence -> diagnosis -> intervention -> verification loop.

## Canonical links

- ClawHub skill page: `https://clawhub.ai/sheygoodbai/vericlaw`
- ClawHub plugin page: `https://clawhub.ai/plugins/vericlaw`
- Landing page: `https://sheygoodbai.github.io/vericlaw/`
- Download page: `https://sheygoodbai.github.io/vericlaw/download/`
- Latest release: `https://github.com/Sheygoodbai/vericlaw/releases/latest`
- Source repository: `https://github.com/Sheygoodbai/vericlaw`

## Route guide

- Direct skill page: `https://clawhub.ai/sheygoodbai/vericlaw`
- OpenClaw companion plugin: `https://clawhub.ai/plugins/vericlaw`
- Real app bundle download: `https://sheygoodbai.github.io/vericlaw/download/`
- Latest release notes and assets: `https://github.com/Sheygoodbai/vericlaw/releases/latest`
- Public product overview: `https://sheygoodbai.github.io/vericlaw/`

The ClawHub `Download zip` action downloads a small listing package, not the
public macOS app bundle.
