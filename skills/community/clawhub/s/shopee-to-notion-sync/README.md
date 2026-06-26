# Shopee Notion Sync Skill for OpenClaw 🛍️

This OpenClaw skill searches Shopee products and syncs them into a configured Notion database using a local Node.js workflow.  
It is designed for deterministic execution, so product syncing happens through a predefined local script instead of web search, scraping, or alternative flows.

---

## Features

- Search products on Shopee using a keyword.
- Sync results into a configured Notion database.
- Create new products or update existing ones.
- Uses a local Node.js workflow for predictable execution.
- Supports configurable targets for different Notion databases.

---

## How It Works

This skill uses the following local command:

```bash
node jobs/sync-shopee-notion.js "<keyword>" <limit> <target>
```

### Parameters

- `keyword`: Shopee search term
- `limit`: number of products to process
- `target`: logical Notion target configured in `jobs/config.js`

### Defaults

- `target`: `shopee_produtos`
- `limit`: `10`

---

## Installation

Copy the skill folder into the OpenClaw workspace for the target agent:

```bash
cp -r shopee-to-notion ~/.openclaw/workspace-sales/
```

Then install dependencies:

```bash
cd ~/.openclaw/workspace-sales
npm install
```

Make sure the skill is available under the agent workspace, for example:

```bash
~/.openclaw/workspace-sales/
├── jobs/
├── skills/
│   └── shopee-to-notion/
│       └── SKILL.md
├── package.json
└── .env
```

---

## Environment Variables

This skill requires the following environment variables:

```env
SHOPEE_APP_ID=your_shopee_app_id
SHOPEE_SECRET=your_shopee_secret
NOTION_TOKEN=your_notion_token
NOTION_DATABASE_ID=your_notion_database_id
```

Optional additional targets:

```env
NOTION_DATABASE_ID_TESTE=your_test_database_id
NOTION_DATABASE_ID_OFERTAS=your_offers_database_id
```

You can place them in a local `.env` file inside the agent workspace.

---

## Required Notion Database Structure

The target Notion database should contain these fields:

- `id`
- `nome`
- `valor`
- `valor da comissão`
- `categoria`
- `url da imagem`
- `link do produto`

Recommended mapping used by the sync flow:

- `id` → Shopee `itemId`
- `nome` → Shopee `productName`
- `valor` → Shopee `priceMin`
- `valor da comissão` → Shopee `commission`
- `categoria` → fixed value such as `Shopee`
- `url da imagem` → Shopee `imageUrl`
- `link do produto` → Shopee `productLink`

If you need to adjust the Notion request headers or API version, check the `criarHeadersNotion` method in `jobs/notion-client.js`.

---

## Usage

Once installed, you can ask the OpenClaw agent things like:

```text
Search Shopee products for "blusas de academia femininas" and sync them to Notion.
```

or

```text
Use the Shopee→Notion flow for keyword "tenis", limit 10, target shopee_produtos.
```

The skill will execute the local Node.js workflow and return a short summary with:

- keyword used
- target used
- created count
- updated count
- failed count

---

## Example Commands

Direct script execution:

```bash
node jobs/sync-shopee-notion.js "celular" 10 shopee_produtos
node jobs/sync-shopee-notion.js "blusas de academia femininas" 10 shopee_produtos
node jobs/sync-shopee-notion.js "tenis corrida" 10 shopee_produtos
```

Example natural language prompts:

```text
Search Shopee products for "celular" and sync them to Notion.
Sync Shopee results for "blusas de academia femininas" into the target shopee_produtos.
Update the Shopee product table in Notion with 10 products for "tenis".
```

---

## Rules

This skill is designed to use only the local Node.js workflow.

It must **not**:

- use web search
- use browser tools
- use curl directly
- create Python scripts
- create shell scripts
- scrape websites
- write memory files
- invent product results

---

## Output Example

A typical execution summary looks like this:

```text
keyword usada: blusas de academia femininas
target usado: shopee_produtos
criados: 10
atualizados: 0
falhas: 0
```

---

## Dependencies

- [axios](https://www.npmjs.com/package/axios) – for HTTP requests
- [dotenv](https://www.npmjs.com/package/dotenv) – for environment variable loading
- Node.js 18+ recommended

Install dependencies with:

```bash
npm install
```

---

## Notes

- This skill depends on valid Shopee API credentials.
- The Notion database must already exist and be properly configured.
- The target database fields must match the structure expected by the sync script.
- If needed, the Notion request headers are defined in `jobs/notion-client.js`, in the `criarHeadersNotion` method.
- The skill is intended for deterministic product sync workflows inside OpenClaw.

---

## Contributing

Feel free to improve the workflow, extend target support, or adapt the integration for additional Shopee search scenarios and Notion database schemas.

## License

MIT License
