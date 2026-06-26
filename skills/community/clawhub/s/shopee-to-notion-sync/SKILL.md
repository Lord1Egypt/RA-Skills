---
name: shopee_notion_sync
description: Sync Shopee products into Notion using the local Node.js workflow only.
---

# Shopee Notion Sync

Use this skill for any request involving:
- searching Shopee products
- saving Shopee products to Notion
- updating the Shopee product table in Notion
- syncing Shopee with Notion

## Mandatory rule

For any request covered by this skill, you MUST use only this command:

`node jobs/sync-shopee-notion.js "<keyword>" <limit> <target>`

Do NOT:
- use web search
- use browser tools
- use curl directly
- create Python scripts
- create shell scripts
- scrape websites
- write memory files
- invent product results

## Defaults

- default target: `shopee_produtos`
- default limit: `10`

## Response format

Return only:
- keyword usada
- target usado
- criados
- atualizados
- falhas

## Examples

- `node jobs/sync-shopee-notion.js "celular" 10 shopee_produtos`
- `node jobs/sync-shopee-notion.js "blusas de academia femininas" 10 shopee_produtos`
