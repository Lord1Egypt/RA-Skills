---
name: rule-get
description: A rule retrieval skill based on the "Tradebee Website Builder" Open API. It is used to read the exact tenant-scoped HTML fragment rules for one selected language and one fixed scene before generating Tradebee description HTML.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# rule-get

## Overview

Use this skill before generating any of these HTML fragments:

- `blog.description`
- `faq.answer`
- `products.description`
- `productsgroup.section.top`
- `productsgroup.section.bottom`
- `custompage.content`

This skill sends the rule request through the skill runtime with the configured `BEE_API_KEY`. The model must pass only the exact `language` and exact `scene`.

## Input Parameters

Authentication uses only the configured `BEE_API_KEY` environment variable. Never provide API keys in tool inputs, prompts, examples, logs, or chat text.

### `language` (string, Required)

- Select one exact site language from `languages-get`
- Do not guess, translate, normalize, or replace it

### `scene` (string, Required)

Use one exact fixed value only:

- `blog.description`
- `faq.answer`
- `products.description`
- `productsgroup.section.top`
- `productsgroup.section.bottom`
- `custompage.content`

Do not invent, shorten, translate, or rename the `scene` value.

## Required Execution Order

1. Select the exact site `language` first.
2. Select the exact fixed `scene` that matches the target HTML field.
3. Call `rule-get`.
4. Generate the HTML fragment only after `rule-get` returns successfully.

## Failure Rule

- If `rule-get` fails, do not continue by guessing colors, fonts, links, layout, or other fragment rules.
- Stop and report the failure instead of generating a fragment from assumptions.

## Dependencies

```json
{
  "language": {
    "skill": "languages-get",
    "field": "list[].language",
    "mode": "select"
  }
}
```
