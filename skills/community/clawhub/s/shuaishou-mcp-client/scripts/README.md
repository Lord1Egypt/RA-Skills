# htyd-mcp-client scripts

Install:

```bash
npm install
```

Set endpoint (optional):

```bash
set MCP_URL=https://dz.shuaishou.com/mcp
set MCP_APP_KEY=ak_test_001
```

List tools:

```bash
node htyd-mcp.mjs tools
```

Call any tool:

```bash
node htyd-mcp.mjs call list_shops "{}"
```

## Business Workflow

This toolset supports two business workflows:

### Workflow 1: Collect → Claim (to drafts)

Only collects the product and claims it to a specified shop, stays in draft status, does NOT auto-publish.

```bash
# Step 1: Collect
node htyd-mcp.mjs collect_goods --originList "https://detail.1688.com/offer/xxx.html"

# Step 2: Claim (to drafts)
node htyd-mcp.mjs claim_goods --originList "https://detail.1688.com/offer/xxx.html" --platId 68 --merchantIds 2025050918
```

### Workflow 2: Collect → Claim → Publish (one-step) NEW

User provides a link, completes the full workflow of collect → claim → publish. **The flow ends when publish API call completes**, without waiting for async processing results.

```bash
node htyd-mcp.mjs collect_and_publish \
  --originList "https://detail.1688.com/offer/730708656407.html" \
  --platId 68 \
  --merchantIds 2025050918 \
  --pubShops 2025050918
```

#### Parameters

- `--originList` (required) - Product URL(s), multiple allowed
- `--platId` (required) - Platform ID, e.g., 68 for Temu
- `--merchantIds` (required) - Shop IDs for claiming, comma-separated
- `--pubShops` (optional) - Shop IDs for publishing, defaults to first merchantIds

#### Workflow (5 steps)

```
[1/5] collect_goods         → Call collect API with the link
[2/5] list_collected_goods  → Query collection result, get itemId
[3/5] claim_goods           → Claim to target shop (creates draft)
[4/5] list_temu_drafts      → Query drafts to locate claimed item
[5/5] publish_temu          → Call publish API (flow ends here)
```

**IMPORTANT**: Step 5 considers the flow complete when `publish_temu` API request is sent. It does NOT wait for or check async processing status, actual listing result, etc. **For publish success/failure status, user should check in Shuashou Store Manager (甩手店长).**

#### Draft Locating Strategy

After claiming, need to find the claimed item in drafts for publishing. Strategy:

1. **Shop scope**: Query only target shop (`shopId=merchantIds[0]`)
2. **Status scope**: Only unpublished (`status=UNPUBLISH`), excludes already published/publishing
3. **Time sort**: Sort by claim time descending, latest first
4. **URL match**: Match origin URL (partial domain+path matching)

**Duplicate claim handling**: If same link claimed multiple times to same shop, **always takes the latest claim** for publishing.

#### When to Use

Use case: When user says "publish this link to shop" or "collect and publish to shop", use this command instead of separate calls.

```bash
# Example: User wants to publish 1688 product to Temu shop
node htyd-mcp.mjs collect_and_publish \
  --originList "https://detail.1688.com/offer/730708656407.html" \
  --platId 68 \
  --merchantIds 2025050918
```

#### Troubleshooting

If step 4 cannot find draft item, possible reasons:
- Draft sync delay after claim (default 5s wait, may need retry)
- URL matching failed (check originUrl field format)
- Status changed (draft already published by other process)

If step 5 fails, check:
- `pubShops` parameter is correct
- Draft item ID is valid
