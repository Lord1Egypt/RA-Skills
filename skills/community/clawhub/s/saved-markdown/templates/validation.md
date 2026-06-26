# Validation Template

Run this checklist before publishing.

## Global Checks

- Content is below `100 KB`
- No unresolved placeholders remain
- No invented sections without user-provided data
- Title and key metadata are present

## Markdown Checks

- Chart widgets use only supported chart types
- CSV numeric cells contain plain numbers only
- Chart titles and headers are clear

## HTML Checks

- `contentType` is set to `"html"`
- Sanitized static HTML only
- No scripts, forms, buttons, or other interactive controls
- Layout remains readable on mobile screens

## JSX Checks

- `contentType` is set to `"jsx"`
- Imports limited to `react` and `react-dom`
- No external packages
- State and derived values are internally consistent

## Final Output Checks

- Content aligns with selected template and user intent
- Sections with missing data are omitted, not fabricated
