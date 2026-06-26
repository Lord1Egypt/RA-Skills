---
name: syft-profile-summary
description: Build or refresh a high-dimensional user profile from `syft following` output. Use when Codex needs to turn a Syft CLI following list into reusable profile artifacts such as `following_topics.md`, raw interest or aversion blocks, and an interpretive `profile_summary.md`, especially when only Syft CLI output is available and richer dashboard or trace artifacts are missing.
---

# Syft Profile Summary

Assume a Syft-only workflow unless the user provides richer profile artifacts. Treat the following list as the canonical source when no dashboard, trace URL, or local Python pipeline is available.

## Outputs

Create or refresh these artifacts:

- `profiles/following_topics.md`
- `profiles/raw_interest_block.txt`
- `profiles/raw_aversion_block.txt`
- `profiles/profile_summary.md`
- optionally `profiles/profile_notes.md`

If the workspace already has a different profile directory, reuse it instead of creating a second one.

## Workflow

1. Confirm that Syft is available.
   Run `syft status`.

2. Read the user's following list.
   Run `syft following`.

3. Save the following list as a first-class artifact.
   Write the original topic list into `profiles/following_topics.md`.
   Keep this file close to the original Syft output, with only light cleanup for readability.
   Treat this as the canonical source artifact in Syft-only environments.

4. Optionally derive a usable raw interest block.
   The following list usually has topic names but not explicit scores, so infer relative strength from:
   - repeated motifs across many followed topics
   - specificity of the topic
   - how central that motif feels to the whole follow graph
   - whether it looks like a structural worldview axis or a lighter side-interest

5. Use stable score bands instead of fake precision.
   Prefer bands such as `100 / 85 / 70 / 55 / 35`.
   Interpret them as:
   - `100`: defining axis or obsession
   - `85`: strong recurring axis
   - `70`: meaningful secondary axis
   - `55`: supporting but not central
   - `35`: light or occasional interest

6. Do not invent aversions from following data alone.
   If the user has not explicitly stated dislikes, keep `raw_aversion_block.txt` minimal and honest.
   Use this default when needed:
   `Original aversions: (not explicitly provided by user yet)`

7. Produce two profile layers together.
   - canonical source layer: the unscored `following_topics.md`
   - interpretive layer: the high-dimensional `profile_summary.md`

8. Treat `raw_interest_block.txt` as optional helper output, not the canonical truth.
   In Syft-only environments, the true source is the following list itself.
   If you create `raw_interest_block.txt`, treat it as a heuristic interpretation of follows rather than user-provided scores.

9. Read [references/profile-summary-prompt.md](references/profile-summary-prompt.md) before drafting `profile_summary.md`.
   Follow that prompt shape when producing the interpretive summary.

10. Before treating the profile as stable, show the user a short understanding check.
   Summarize:
   - the main axes you inferred
   - the side-interests you think matter
   - any uncertainty caused by missing aversion data

## Output rules

- Write all user-facing content in Simplified Chinese unless the user asks otherwise.
- If you generate `raw_interest_block.txt`, keep it exhaustive enough to preserve fidelity.
- Keep the profile summary interpretive, not mechanical.
- If the follow graph clearly shows "hard macro reality tracking + soft personal refuge interests", call that tension out directly.

## Raw block format

Use this exact style:

`Original interests: Topic A | Score: 100 - Topic B | Score: 85 - Topic C | Score: 55`

For aversions:

`Original aversions: Topic X | Score: 90 - Topic Y | Score: 50`

If no aversions are known:

`Original aversions: (not explicitly provided by user yet)`
