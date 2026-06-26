# Retriever Agent

## Goal
Retrieve candidate supporting notes from a seed note.

## Model Tier
- Use `agent_models.retriever` from config.
- Resolve to `models.fast` by default for retrieval orchestration.
- Use `models.deep` only for complex query reformulation when needed.

## Input
- `seed_note_path`
- `zettel_dir`
- retrieval limits (`link_depth`, `max_links`)

## Procedure
1. Read retrieval limits from config and target candidate count from `retrieval.max_links`.
2. Check if the external `zettel-link` skill is available. If it exists, run semantic retrieval via its `scripts/search.py` command using the seed note's topic or title. If it does not exist, warn the user and skip this step.
3. Run local retrieval (`scripts/find_links.py`) to collect explicit wikilinked and tag-overlap notes.
4. Merge and deduplicate all candidates from both sources.
5. Prioritize semantic candidates (if any), then fill remaining slots with local retrieval results up to configured count.
6. Exclude the seed note itself.

## Output
- `candidate_paths`: unique prioritized list of markdown note paths
- `stats`: counts for semantic, wikilink, and tag-similar hits

## Constraints
- Use local vault evidence only.
- Do not score relevance in this stage.
