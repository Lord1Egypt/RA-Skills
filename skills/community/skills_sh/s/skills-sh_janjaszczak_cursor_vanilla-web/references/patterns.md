<!-- .cursor/skills/vanilla-web/references/patterns.md -->

# Patterns

## Minimal module pattern
- main.js: selects root nodes, wires events, bootstraps modules
- modules/*.js: exports init(root, options) and pure helpers

## Event delegation
Attach one listener on a stable parent and switch by data attributes:
- data-action="open-modal"
- data-action="delete-item"
