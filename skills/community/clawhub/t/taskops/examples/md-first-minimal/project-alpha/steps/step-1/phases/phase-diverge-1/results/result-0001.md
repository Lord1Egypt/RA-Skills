---
graphTaskVersion: 2
entityType: result
id: result-0001
projectId: project-alpha
stepId: step-1
phaseId: phase-diverge-1
nodeId: node-compare-layout
status: done
recordedAt: 2026-04-24T14:00:00Z
expected: Validate a small canonical markdown layout that humans and tools can both parse
actual: Confirmed that folder-backed entities plus YAML frontmatter are readable and deterministic enough for a first parser target
artifacts:
  - references/md-first-vnext-spec.md
---

# Result 0001

## Expected
Validate a small canonical markdown layout that humans and tools can both parse.

## Actual
Confirmed that folder-backed entities plus YAML frontmatter are readable and deterministic enough for a first parser target.

## Notes
- Separate result files keep the protocol append-friendly.
- The next pressure test should check how multiple phases read in a tree UI.
