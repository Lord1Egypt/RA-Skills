# Writing for Astra provenance

Operator-owned adaptation inspired by Matt Pocock's writing-for-agents.
Upstream: https://github.com/mattpocock/skills
Source path: skills/productivity/writing-for-agents
Original integration revision: 3cca18b368ae95cdbdebbff572ccafa662551015
License: MIT; upstream attribution is retained in LICENSE.

Basis: [OpenAI guidance for Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).

This is a separate maintained skill, not a one-to-one mirror. Upstream updates
do not overwrite it automatically. New semantic changes need owner review.

Retained: narrow context pointers, conditional disclosure, grouped concepts,
canonical sources, meaningful completion and model-relative evaluation of rules.
Changed: outcome-led guidance instead of prioritizing ordered recipes; no hidden
sequence through forced context boundaries, adjective escalation, speculative
negation rule or compression of technical criteria into vague keywords.
Codex-specific invocation guidance lives in a conditional reference.
Intentional orchestration and multi-model correctness remain requirements.

Root line counts at creation: upstream 81; adapted root 63.
No measured performance or allowance improvement is claimed by this rewrite.

## Adaptation rationale

| Adaptation | Reason |
| --- | --- |
| Prefer purpose, constraints and completion over mandatory recipes | Give Astra freedom to select an approach while preserving correctness requirements. |
| Split conditional reference material, not sequential steps hidden behind context resets | Load guidance when relevant without forcing orchestration merely to reduce context. |
| Remove adjective escalation and speculative negation advice | Use concrete requirements rather than unsupported prompting heuristics. |
| Preserve technical criteria instead of compressing them into vague keywords | Optimize useful context, not minimum line count. |
| Put Codex invocation mechanics in references/codex-skill-mechanics.md | Harness-specific details should be loaded only when applicable. |
| Preserve safety, compatibility and intentional orchestration | These encode requirements, not compensation for older models. |

The rationale follows [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).
These are editorial choices, not measured performance claims.

## 2026-10-06 upstream review

Current reviewed source revision: 4588b32ecab9ecc9fc8cc6b6c5e7d675b6004b0d.

The current upstream and support-file hashes match the previously reviewed
baseline. This review compared the available source and support files with the
adaptation and incorporated useful guidance on context pointers, context and
cognitive load, information hierarchy, completion criteria and source-of-truth
choices in Astra-compatible language. It keeps invocation mechanics in the
conditional Codex reference.

Skipped: fixed recipes and context resets as a general way to prevent premature
completion, claims that leading words reliably recruit model priors or reduce
tokens, and blanket claims that negation makes a behavior more likely. Those
conflict with the existing outcome-led rationale or make behavioral claims
without evidence for Astra. The adaptation still asks authors to test
model-relative guidance when that distinction matters.

The fresh upstream checkout contains only its current shallow snapshot, so the
previous source revision's commit history was unavailable. The recorded file
hashes match the current source inventory. No measured performance claim is
made.

## 2026-10-19 upstream review

Current reviewed source revision: 49dd158d1076134a641b33efb035946536778336.

The upstream `writing-for-agents` source files and license are byte-identical
to the 2026-10-06 reviewed baseline. No content change was needed in Writing
for Astra. The review confirmed the existing outcome-led rationale, conditional
Codex mechanics reference, and model-relative evaluation guidance remain
appropriate; the source pin advances to record the completed review.

## Update review

UPSTREAM.json stores the reviewed Writing for Agents files and license hashes.
The daily Review adapted skill upstreams workflow opens or updates a GitHub issue
on additions, changes or removals. It leaves our version and baseline untouched.
Review each relevant upstream change against the rationale above; port or skip it
explicitly, then update the reviewed commit/hashes in the approved change.
Closing an issue without updating the baseline does not acknowledge that update.
