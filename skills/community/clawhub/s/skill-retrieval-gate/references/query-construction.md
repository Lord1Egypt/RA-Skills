# Query Construction

Do not copy the full user prompt into `memory_search` by default.

Build a compact retrieval query from:

- task object
- task type
- key field, symptom, module, or entity

## Recommended template

```text
<object> + <task type> + <key module/symptom/field>
```

## Examples

- `payment service timeout rollout`
- `project summary deployment checklist`
- `memory search fetch failed provider`
- `design system color tokens migration`

## Query quality rules

- prefer specific nouns over long sentences
- include the project or system name when available
- include the failure symptom for troubleshooting tasks
- include the module or business term for requirements work
- avoid overpacking the query with every detail from the request
