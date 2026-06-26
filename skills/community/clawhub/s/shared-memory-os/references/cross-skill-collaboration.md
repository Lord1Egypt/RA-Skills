# Cross-Skill Collaboration

Use Shared Memory OS as the governance layer for other skills.

## Collaboration patterns
- memory -> skill: repeated learnings become skill guidance updates
- skill -> memory: repeated operational decisions become durable rules
- model / routing skills -> memory: fallback and retry behavior should be harvested into `.learnings/`
- web / browser skills -> memory: successful retrieval fallback patterns should be captured and indexed

## Recommended workflow
1. Run the target skill
2. Capture corrections, retries, and stable successful paths in `.learnings/`
3. Let Shared Memory OS detect duplicates, promotion candidates, and skill-upgrade candidates
4. Promote stable patterns back into the relevant skill docs or durable memory

## Good collaborators
- `thinking-policy`
- `model-registry-manager`
- `safe-smart-web-fetch`
- `agent-browser`
- `self-improvement`
