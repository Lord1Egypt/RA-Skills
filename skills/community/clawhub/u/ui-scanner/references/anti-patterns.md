# Common Anti-Patterns

1. **Fabricating non-existent components**: Making up pricing card styles when none exist on page → only output visible components
2. **Missing estimated annotation**: Filling in HEX for hover color without source → mark `estimated` + inference basis
3. **Mixed color formats**: Mixing HEX/RGB/HSL → unify to `#RRGGBB`
4. **Over-analysis**: Outputting 10 typography levels for a simple landing page → only write what the page has
5. **Ignoring responsive differences**: Only analyzing desktop → note breakpoints and layout changes (if inferable)
