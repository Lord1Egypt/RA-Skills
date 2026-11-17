# Session Atlas
A Claude JSONL source indexer plus a generic method for turning long agent sessions into evidence-linked maps. It records semantic turns, tool/result links, source line spans, snapshot hashes and reasoning coverage metadata. It does not use an LLM, write the narrative atlas for you, or support every agent transcript format.

## Install and use
Requires Python 3.11+, no third-party Python dependencies. Install with `npx skills add AntreasAntoniou/session-atlas-agent-skill`, copy this folder to your agent's skill directory as session-atlas, or use scripts directly. The optional installer uses Node.js and network access.
```sh
python3 scripts/index_claude_session.py --source /private/session.jsonl --out-dir /private/session-index
python3 scripts/validate_atlas.py --index-dir /private/session-index --source /private/session.jsonl --require-complete-tools
python3 -m unittest discover -s tests -v
```
These are path examples, not files included in the package. The output directory must be fresh and its parent must already exist. It is created with mode 0700 and files with mode 0600; existing output paths are refused. Use the methodology and template for a manually checked narrative map.

## Privacy and limits
Generated indexes contain prompts, assistant text, command summaries, tool previews and absolute source paths. They remain private even though thinking blocks are not reproduced. Hashing reasoning is coverage metadata, not anonymization of the rest of the session. Do not commit generated output.
The validator checks structure, bounds and prompt hashes. With --source, it verifies the snapshot prefix and re-indexes it to compare actual assistant/tool evidence and manifest counts. Without --source, self-reported coverage is not independently verified. Neither mode certifies narrative claims or replays tools. Appended source records may follow a valid snapshot. Incomplete tools are reported and optionally rejected. Duplicate tool IDs, unsupported record shapes and concurrent source edits need human review.
The indexer is exported from a private workflow; private reference atlases, raw histories, control ledgers and research-specific rules are excluded. Tests create clearly labelled structural fixtures only.
