# Profile Summary Route

Use this route when Codex needs to turn `syft following` into reusable profile artifacts.

## Goal

Create or refresh:

- `profiles/following_topics.md`
- `profiles/raw_interest_block.txt`
- `profiles/raw_aversion_block.txt`
- `profiles/profile_summary.md`
- optionally `profiles/profile_notes.md`

Reuse an existing profile directory if the workspace already has one.

## Steps

1. Run `syft status`.
2. Run `syft following`.
3. Save the following list with only light cleanup into `profiles/following_topics.md`.
4. Treat the following list as the canonical source artifact in Syft-only environments.
5. If a raw interest block is useful, infer broad score bands rather than fake precision.
6. Do not invent aversions from follows alone.
7. Draft `profile_summary.md` as an interpretive layer, not a mechanical restatement.
8. Before treating the profile as stable, summarize your inferred axes and note uncertainty caused by missing aversion data.

## Scoring Guidance

If a raw interest block is needed, use stable score bands such as:

- `100`: defining axis
- `85`: strong recurring axis
- `70`: meaningful secondary axis
- `55`: supporting but not central
- `35`: light or occasional interest

Keep the file honest about being heuristic rather than user-authored.

## Output Rules

- Write user-facing content in Simplified Chinese unless asked otherwise.
- Call out the tension directly when the follow graph shows hard macro tracking alongside softer refuge interests.
- Keep `following_topics.md` closer to raw truth than `raw_interest_block.txt`.
