# Agent Protocol for 小天铺货AI助手

This reference defines how an agent without a script runtime (Codex, Cursor, Claude Code, Trae, OpenClaw, or any HTTP-capable host) can provide the 小天铺货AI助手 capabilities using its own tools instead of the bundled Python scripts.

The protocol intentionally mirrors the behavior of the script-based package. Keep the deterministic checks, rendering rules, and safety boundaries identical to `SKILL.md` and `references/api-protocol.md`.

## 1. Protocol vs script mode

- Script mode: WorkBuddy installs the full package with `scripts/run.py`, `scripts/login.py`, and `scripts/api.py`. Use the exact commands in `SKILL.md`.
- Protocol mode: the package contains `SKILL.md` plus this reference and no scripts. The agent must call the backend directly with HTTP/browser/file tools.
- Both modes must produce the same user-visible behavior, including the fixed image-search table. If a platform cannot perform one of the required deterministic steps, fail that step with a business-friendly message instead of guessing.

## 2. Environment and channels

Channels are materialized as separate package identities:

| Channel | Slug | Display name | Default env | Backend | Frontend |
| --- | --- | --- | --- | --- | --- |
| Development | `xtph-ecommerce-assistant-dev` | 小天铺货AI助手（开发版） | `test` | `https://puhuoapi.huitun.com` | `https://puhuo-test.huitun.com` |
| Production | `xtph-ecommerce-assistant` | 小天铺货AI助手 | `prod` | `https://puhuoapi.huitun.com` | `https://puhuo.huitun.com` |

Frontend entry URLs:

| Entry | Test | Production |
| --- | --- | --- |
| Home | `https://puhuo-test.huitun.com/home` | `https://puhuo.huitun.com/home` |
| Distribution records | `https://puhuo-test.huitun.com/distribut_man` | `https://puhuo.huitun.com/distribut_man` |
| Manual goods restock | `https://puhuo-test.huitun.com/goods_restock` | `https://puhuo.huitun.com/goods_restock` |

Never let the development package use production credentials or the reverse. Session and workflow paths are slug-scoped.

## 3. Runtime state

The protocol mode keeps state in the user profile, out of the conversation and out of repository files.

Session file:

```text
Development: ~/.xtph/sessions/xtph-ecommerce-assistant-dev.json
Production:  ~/.xtph/sessions/xtph-ecommerce-assistant.json
```

Saved preview workflows:

```text
~/.xtph/workflows/{slug}/{workflowId}.json
```

Optional generated image-search HTML pages:

```text
~/.xtph/image-search-results/{slug}/{timestamp}.html
```

Rules:

- Write session files with mode `0600`.
- Include `sessionToken` only in the session file. Never print, paste, summarize, log, or store it elsewhere.
- Preserve workflow files until publishing is finished or the user asks to clean them.
- Never include `sessionToken` in workflow JSON or HTML pages.

## 4. Authorization

Explicit connect/reconnect/reauthorization requests are terminal actions. Do not chain `shop-info`, `shop-group-info`, or `auth-status` after a successful authorization unless the user asks for one of those checks separately.

### 4.1 authSession polling flow

The protocol mode uses a backend-managed authorization session instead of a loopback callback. The agent opens a browser authorization page, the page binds the browser-created `handoffCode` to the authSession, and the agent polls until the backend exchanges the code and returns the session token. The browser never needs to reach `127.0.0.1` and the user never copies a code.

1. Start an authorization session:

```http
POST https://puhuoapi.huitun.com/agent/ecommerce/session/handoff/init
Content-Type: application/json
Accept: application/json

{}
```

Response:

```json
{
  "success": true,
  "code": 0,
  "data": {
    "authSessionId": "{authSessionId}",
    "authUrl": null,
    "expiresInSeconds": 300
  }
}
```

The backend no longer returns the authorization page URL. Build the page URL per channel:

- Development: `https://puhuo-test.huitun.com/agent/ecommerce/connect?authSessionId={authSessionId}`
- Production: `https://puhuo.huitun.com/agent/ecommerce/connect?authSessionId={authSessionId}`

2. Open the built page URL with the platform's browser tool or show it to the user as a manual link. A normal system-browser `open` may be used only when the agent runs outside a sandbox and the user expects it.
3. Wait for the user to log in, select a shop, and click confirm in the opened page. The page binds the browser-created `handoffCode` to the authSession internally; no callback is involved and no code is shown to the user.
4. Poll the authorization session every 2 seconds until `status` is `ready`, `expired`, or the local timeout (default 300 seconds) is reached:

```http
POST https://puhuoapi.huitun.com/agent/ecommerce/session/handoff/check
Content-Type: application/json
Accept: application/json

{
  "authSessionId": "{authSessionId}"
}
```

`pending` response:

```json
{
  "success": true,
  "code": 0,
  "data": {
    "status": "pending"
  }
}
```

`ready` response:

```json
{
  "success": true,
  "code": 0,
  "data": {
    "status": "ready",
    "sessionToken": "{sessionToken}",
    "loginShopId": 1001,
    "currentShopId": 2002
  }
}
```

`expired` response:

```json
{
  "success": true,
  "code": 0,
  "data": {
    "status": "expired"
  }
}
```

5. On `ready`, read `sessionToken` from the response and store it in the slug-scoped session file. Never print or summarize the token.
6. On `expired`, start a new authorization session and ask the user to confirm again.

### 4.2 Session validity

- Before any authenticated call, read the session file for the active slug.
- If the file is missing or the token is empty, run the authorization flow first.
- If a read-only request returns `code: 3011`, delete the session file and ask the user to reconnect.
- Reuse the session token with header `X-Session-Token: {sessionToken}`.

## 5. Read capabilities

### 5.1 Shop info

Trigger: 获取我的店铺信息 / 查询店铺信息 / 当前店铺是什么 / 看看当前店铺.

```http
GET https://puhuoapi.huitun.com/shop/shop_info
X-Session-Token: {sessionToken}
Accept: application/json
```

Render only safe business fields:

- Shop ID
- Shop name
- Edition or spec value
- Expiration time
- Authorization commitment status
- Auto-rectify grant status

Do not render `authCode`, `authCommitmentDesc`, or `sessionToken`.

### 5.2 Shop group info

Trigger: 查询店群信息 / 看看店群 / 当前店群是什么 / 店群详情.

```http
GET https://puhuoapi.huitun.com/shopGroup/detail
X-Session-Token: {sessionToken}
Accept: application/json
```

Render only safe business fields:

- Group ID
- Master shop ID / name
- Owner shop ID
- Member count
- Status
- Expiration time
- Creation time
- Member shop ID / name
- Member edition or spec value
- Member role
- Join time

Do not render `inviteCode` or internal compute-account details.

### 5.3 Authorization status

Trigger: 查询授权状态 / 查看授权状态 / 看看授权店铺 / 当前授权情况.

```http
POST https://puhuoapi.huitun.com/shop/getAuthShopList
X-Session-Token: {sessionToken}
Accept: application/json
Content-Type: application/json

{}
```

Render only safe business fields:

- Authorized shop ID
- Authorized shop name
- Expiration time
- Platform
- Update time

Do not render `sessionToken`.

## 6. Image-based 1688 source search

### 6.1 Trigger and input

Trigger by intent plus available image context: image attachment, image URL, or a clear reference such as 这张图 / 上面的图片 / 附件 combined with finding same-style, similar, lower-price, or 1688 source products. This is intent routing, not exact keyword matching.

Inputs:

- Up to 10 image files or image URLs.
- Image files must be JPG/JPEG/PNG and no larger than 3 MB each.
- Image URLs must use `http` or `https`.
- If only a filename is available but no readable image, ask the user to reattach the image or provide its URL.

### 6.2 Request

```http
POST https://puhuoapi.huitun.com/skill/product/image-similar
X-Session-Token: {sessionToken}
Accept: application/json
Content-Type: application/json

{
  "images": [
    {
      "imgBase64": "data:image/jpeg;base64,...",
      "imageKeywords": ""
    },
    {
      "imgUrl": "https://example.com/product.jpg",
      "imageKeywords": ""
    }
  ]
}
```

For local files, generate the base64 payload with an available shell tool, for example:

```bash
base64 -w 0 /path/to/product.jpg
```

Prefix the result with `data:image/jpeg;base64,` (or the matching MIME prefix). Do not send `shopId` or `sourceUserId`.

### 6.3 Deterministic selection check

A product in `data.products` is accepted only when all three core fields are present and valid:

1. `detailUrl` is a normalized 1688 product link (`https://detail.1688.com/offer/{id}.html`).
2. `title` is non-empty.
3. `price` is non-empty.

Product image and consign price are optional for selection. Ignore `imageSearchUrl`. Do not fetch product detail pages and do not replace returned values.

- At least one accepted product means selection succeeds.
- Zero accepted products means selection fails because the response did not contain complete product information. Report the failure and stop the selection step.
- Selection success is independent from publishability.

### 6.4 Fixed rendering

Always render the mandatory text table in both channels:

```markdown
| 排名 | 商品标题 | 价格 | 1688商品链接 |
|---|---|---|---|
```

Rules:

- Show at most the first 10 accepted products from `data.products`, preserving interface order.
- Use only returned image, title, price, consign price, and normalized `detailUrl`.
- The link column must contain the full clickable 1688 URL, not an offer ID or shortened label.
- Never show or use `imageSearchUrl`.
- If `data.productResultsPage.url` is present, you may generate a local HTML page from the returned fields and provide it as a manual `查看同款商品` link. Keep the text table mandatory.
- Do not open the page through the system browser and never claim it was opened. If the host supports a built-in browser, the host agent may open the manual link; otherwise tell the user to click it.

## 7. Preview flow

### 7.1 Entry

Trigger: 预览1688商品铺货 / 采集1688链接生成预览 / 检查这些1688商品能不能铺货 / 用这些1688链接做铺货预览, or the user-selected products from image search.

Accept 1688 links in the form `https?://detail.1688.com/offer/{id}.html`. Normalize every accepted link to `https://detail.1688.com/offer/{id}.html` and de-duplicate.

### 7.2 Preconditions

- Valid session.
- At least one source link.
- Preview-only until a later confirmed publish step.

### 7.3 Optional preflight

When practical, follow the frontend-consistent preflight before creating a preview task. Call the relevant endpoints when the backend exposes them:

```text
GET  /shop/shop_info
POST /shop/dyPublishProductLimit
POST /shop/lowSalesProductQuota
POST /material/getCapInfos
POST /shop/publish_limit
POST /shop/freight_templates
```

If a preflight response clearly reports insufficient daily quota, monthly publish quota, or material capacity, stop before preview creation and explain the blocker.

### 7.4 Create preview task

```http
POST https://puhuoapi.huitun.com/product/preview_task/create
X-Session-Token: {sessionToken}
Accept: application/json
Content-Type: application/json

{
  "sourcePlatform": 1688,
  "sourceRefs": [
    "https://detail.1688.com/offer/955816756852.html"
  ]
}
```

### 7.5 Poll draft results

Poll the preview task with the preview batch ID and per-task cursors returned by creation:

```http
POST https://puhuoapi.huitun.com/product/preview_task/draft/query
X-Session-Token: {sessionToken}
Accept: application/json
Content-Type: application/json

{
  "previewBatchId": "{previewBatchId}",
  "taskLastChunkNos": [
    {
      "previewTaskId": "{previewTaskId}",
      "lastChunkNo": null
    }
  ]
}
```

Default polling is every 1 second; default timeout is 180 seconds. Advance `lastChunkNo` from each task's `currentChunkNo` after every poll. Continue until every task is terminal (`DONE` or `FAIL`) or the timeout is reached.

### 7.6 Enrichment and classification

Use the preview items plus enrichment endpoints:

```text
POST /product/cate_property
POST /product/batch_qualification_config
POST /product/batch_product_update_rule
POST /product/brandQueryAuth
```

Guidance:

- Use `cate_property` per collected category ID to detect required attributes and required category property images.
- Use `batch_qualification_config` to detect required qualification attachments.
- Use `batch_product_update_rule` to classify title length, shipping origin, after-sales, size chart, SKU spec count, SKU combination count, and all-SKU-disabled blockers.
- Use `brandQueryAuth` only when the source item carries a brand offer marker.

Classify each item as `ready`, `blocked`, `failed`, `skipped`, or still `processing`. Build `requiredAttributeRepairRequests` only for required product attributes that are still empty.

### 7.7 Save and render

Save the preview workflow locally under the slug-scoped workflow directory. Include raw preview items and `publishDraft` payloads needed for a later publish rebuild. Never include `sessionToken`.

Render only safe preview fields:

- Input count, valid count, duplicate count, invalid count
- Target shop ID and shop name
- Preview batch ID and task statuses
- Product title, source product ID, main image, category, SKU count, price range, total stock
- Blockers, warnings, failed items, processing status, next action
- Required attribute repair targets when applicable

Do not render raw `publishDraft` payloads by default. Preview must never call `/product/preview/publishV2`.

## 8. Required attribute repair

### 8.1 Entry

Run repair only after a preview workflow is saved and `requiredAttributeRepairRequests` is non-empty.

### 8.2 Proposal rules

The agent may propose fills only for empty required product attributes:

- `text`, `select`, `multi_select`, and low-risk `measure` properties.
- General `text` fields require explicit `source_attribute` evidence.
- 产品名称 / 商品名称 may use `derived_product_name` evidence from the title and category.
- Low-risk `measure` fields such as net content, net weight, grammage, weight, or capacity may be proposed only when upstream evidence provides a numeric unit value or a strong numeric source attribute.
- `select` and `multi_select` must use an existing target option `valueId` or exact option name from the target options.
- `measure` must include `numericValue` and `unitName`.

Do not propose:

- Overrides of already-filled attributes.
- High-risk fields: brand, origin, certifications, standards, approval numbers, qualifications, or effect claims.
- Certificate-like fields that are only lexically similar.
- Missing shelf-life, date, or compliance facts without explicit upstream evidence.
- Quantity-only values such as `14卷`, `1提`, or `3包` when the target asks for net content or gram weight.
- Non-product-attribute blockers such as qualifications, attribute images, size charts, shipping origin, after-sales, or SKU blockers.

Proposal shape:

```json
[
  {
    "previewItemId": "item-id",
    "propertyId": "3422",
    "action": "fill",
    "valueName": "塑料",
    "valueId": "",
    "source": {"kind": "source_attribute", "name": "外壳材质", "value": "塑料"},
    "confidence": 0.95,
    "reason": "铅笔类目中外壳材质可作为笔杆材质的明确上游证据。"
  }
]
```

### 8.3 Apply, validate, revalidate

1. Update the saved workflow with accepted proposals.
2. Reject invented option IDs, overrides of filled attributes, and high-risk fields.
3. Revalidate the affected items.
4. Continue to publish only if the saved workflow has ready items and no selected blockers.

Report accepted, rejected, and publish summary counts. Do not expose full raw draft payloads by default.

## 9. Publish flow

### 9.1 Modes

- `preview_confirm`: submit a saved preview workflow with `workflowId` after the user confirms selected items.
- `auto_publish`: run preview internally and submit only ready items when the user explicitly requests direct automatic publishing.

Default to `preview_confirm`. Choose the mode before the write flow starts and keep it visible across preview, confirmation, and execution.

### 9.2 Submit

```http
POST https://puhuoapi.huitun.com/product/preview/publishV2
X-Session-Token: {sessionToken}
Accept: application/json
Content-Type: application/json

{
  "previewBatchId": "{previewBatchId}",
  "items": [
    {
      "previewItemId": "{previewItemId}",
      "previewTaskId": "{previewTaskId}",
      "pid": null,
      "publishDraft": {}
    }
  ]
}
```

Guardrails:

- `preview_confirm` requires `workflowId`; `auto_publish` requires source-link input.
- Do not publish if the preview did not complete.
- Do not publish selected items with blockers.
- Do not publish if the saved workflow lacks `rawItems[].publishDraft`.
- Do not publish repaired items unless repair was accepted and the workflow revalidated to ready.
- If direct publishing hits `requiredAttributeRepairRequests`, run `preview -> repair -> submit preview_confirm with ready items`, without requesting a second manual confirmation.

### 9.3 Render

Render only safe result fields:

- Mode
- Preview batch ID
- Selected count and submitted count
- Returned `pid`, item status, and message
- Blocked, missing draft, timeout, or backend failure reason

Every result needs `frontendEntry`. Exception: when required attributes block publishing, use the manual goods restock fallback below.

## 10. Fixed output and fallback rules

### 10.1 Image search table

Always use exactly:

```markdown
| 排名 | 商品标题 | 价格 | 1688商品链接 |
|---|---|---|---|
```

### 10.2 Need manual goods restock

When required product attributes remain missing and the selected products cannot be published, do not ask the user to resume the agent workflow or reply with 确认铺货. Render the exact sentence, one fenced code block per selected 1688 link, and the client entry:

```text
请复制以下商品链接去手动铺货：
```

```text
https://detail.1688.com/offer/955816756852.html
```

```markdown
[去小天铺货客户端铺货](https://puhuo-test.huitun.com/goods_restock)
```

For production use `https://puhuo.huitun.com/goods_restock`. Do not add product titles, ranking numbers, Markdown link text, bullets, preview batch IDs, or repair details around the link blocks.

### 10.3 Frontend entries

- `source-link-publish`: distribution records page, unless the manual restock fallback applies.
- Other results: home page.
- Required-attribute block: `goods_restock` page with label `去小天铺货客户端铺货`.
- Normal label: `去小天铺货查看进度`.

## 11. Output policy

- Development channel may expose technical detail when useful for testing.
- Production channel must hide scripts, commands, API names, endpoint paths, stack traces, internal workflow names, raw payloads, and other technical language by default.
- `XTPH_SKILL_DEBUG=1` may expose structured diagnostic fields only when the user explicitly requests troubleshooting. It never permits revealing private reasoning, credentials, or session tokens.
- Never render `authCode`, `authCommitmentDesc`, `imageSearchUrl`, image base64 data, full raw `publishDraft` payloads, or session tokens.

## 12. Error handling

- HTTP non-2xx or invalid JSON: return a business-friendly failure and the applicable frontend entry.
- `success: false, code: 3011`: delete the slug-scoped session file and guide the user to reconnect.
- Preview or publish rejection for missing/invalid data: explain the business reason in conversational Chinese for that item, keep the selected links, and follow the manual goods restock fallback when required. Do not force-publish.
- Never reinterpret a publish blocker as a failed image search.

## 13. Field verification needed

The following request shapes should be re-verified against a captured frontend network trace before production rollout of protocol mode:

- Exact body of `/product/preview_task/draft/query` (verified against the script: `previewBatchId` plus `taskLastChunkNos[].previewTaskId` / `taskLastChunkNos[].lastChunkNo`).
- Exact bodies and response fields of the optional preflight endpoints in section 7.3.
- Exact exchange response field name for `sessionToken`.

Keep this reference in sync with `SKILL.md`, `references/capabilities.md`, and the backend API contract.
