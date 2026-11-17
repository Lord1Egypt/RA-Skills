# Product Knowledge

Use this reference for Yeelight product consultation, pedia search, manuals, FAQ candidates, SKU resources, attachments, and product specification questions.

## Intent Routing

- Use `product.pedia.search` for product information by fuzzy wording, product name, short name, SKU, SPU, model, model number, barcode, manual, FAQ, installation guide, user guide, product image, product资料, or product简介.
- Put the most specific user phrase into the `query` field. Prefer an exact SKU or model first, then exact product name, then the user's fuzzy keyword.
- Accept structured public aliases when the user states them clearly: model, productName, sku, keyword, query, and name.
- Keep the original user text in `utterance`; Runtime can use it as the fallback query if parameters are incomplete.
- Use `thing.product.info.batch_get`, `thing.product.info.v3.batch_get`, and `thing.schema.*` only for product model/schema questions where Runtime has returned suitable product capability references or the user asks about capability vocabulary.
- Do not treat pedia results as proof that a device is installed or controllable in the user's home. Use `entity.capabilities`, `entity.list`, or `state.query` for installed-device truth.

## Response Rules

- Summarize by product name, short name, SKU, model, SKU/SPU, brand, category/class fields, support markers, status, and available resources. Do not dump every technical field by default.
- Preserve uncertainty when a field is absent or null. Say “资料中未给出” instead of inventing support, sale status, FAQ, or manual facts.
- Treat product-level attachments and resources attachments as source-returned records. Attachments whose type or name indicates 说明书/manual are stronger than candidate URLs.
- Treat manualCandidateUrl and faqCandidateUrl as predictable candidate resources. If Runtime marks candidate status as unverified, present them as possible resources, not guaranteed files.
- If multiple products match a broad keyword such as “青空灯”, give the most relevant few and ask whether the user wants a specific SKU, model, or manual/FAQ.
- For “这个产品支持 Yeelight Pro/HomeKit 吗”, answer only from Runtime-returned support markers.
- Never construct internal requests, expose credential headers, or ask the user for a token. Always call Runtime through `scripts/invoke.sh`.

## Product Advice Boundary

- Product pedia is for consultation, manuals, FAQs, images, category, SKU, model, support markers, and resources.
- Lighting design product selection uses `assets/catalog/lighting-design-products.json` through `node scripts/product-select.mjs`. Use it to choose design-slot candidates from user wording, then use `product.pedia.search` only when official product facts or resources are needed.
- Product pedia is not a substitute for installed-home topology. Do not say "你的客厅有这个产品" unless Runtime returns installed entity evidence.
- If the user asks "能不能控制/自动化/加入场景", answer in two layers: product information may indicate a possible feature, but installed device support must be checked by `entity.capabilities` or the relevant Runtime intent.
- If the user asks installation, wiring, or ecosystem advice, keep it as informational and recommend official manual or installer verification when safety or wiring is involved.
- If the user asks for FAQ content and Runtime returns only a candidate resource, say it may need opening or later verification instead of claiming the FAQ exists.

## Design Candidate Catalog

- The design candidate catalog is a compact, release-safe smart product list with readable product names, SKU/SPU, series, controllable properties, property events, sensor events, aliases, design attributes, design roles, design keywords, and capability tags.
- Retrieve candidates with:

```bash
node scripts/product-select.mjs --query "白色嵌入式射灯" --room "客厅" --goal "全屋照明设计" --limit 8
```

- Choose the final candidate by combining:
  - the user's explicit wording and `requestedSignals`;
  - `constraintReview.matched` and `constraintReview.missing`;
  - `designAttributes` such as color, install style, beam angle, opening, size, head count, wattage, and shape;
  - `designRoles` such as ambient, accent, task, focused, comfort, control, sensing, covering, or climate;
  - `designKeywords` such as version, short-name, or product-positioning words;
  - `capabilityTags` such as power, brightness, colorTemperature, color, openPercent, or sensorEvents;
  - adjustable property and event evidence when the later scene or automation needs dimming, color temperature, RGB color, switch state, motion, contact, illuminance, or presence behavior;
  - the room role and the design goal.
- Do not select only because a string matched first. The script recalls candidates and organizes evidence; the AI must make the final design judgment.
- Do not discard a candidate only because one optional attribute is absent; separate hard constraints from preferences. Hard constraints include SKU, category, install style, color, opening, size, beam angle, wattage, shape, series, and required capability.
- For a full design import, pass the chosen `skuCode`, `capabilityPid`, `productComponentId`, `productName`, `category`, `series`, and concise notes in the slot item so Runtime receives explicit product evidence.
- Keep a short note such as "AI chose this as a black embedded grille accent candidate" or "AI assumed 75 opening 36° S-series spot for bedroom focus lighting" when importing design slots. This makes later review and installer handoff auditable.

## Answer Shape

- Broad query: list up to a few likely matches with product name, SKU, model, category, status, and resource availability.
- Exact SKU/model query: focus on that product and include manual/FAQ/attachment availability when present.
- Comparison query: compare only returned fields; mark missing fields as unknown.
- Resource query: return manual/FAQ/image/resource links only as Runtime-returned resources or Runtime-labeled candidates.

## Natural Language Mapping

| User wording | Intent | Parameters |
| --- | --- | --- |
| 青空灯有什么资料 / 青空灯说明书 | `product.pedia.search` | `query: "青空灯"` |
| 查 1-000003268 的说明书 | `product.pedia.search` | `query: "1-000003268"` |
| YP-0117 是什么产品 | `product.pedia.search` | `query: "YP-0117"`, `model: "YP-0117"` |
| Yeelight Pro Nightingale 青空灯夙夜版 FAQ | `product.pedia.search` | `query: "Yeelight Pro Nightingale青空灯夙夜版"` |
| YLP-Nightingale青空灯-夙夜版有图和说明书吗 | `product.pedia.search` | `query: "YLP-Nightingale青空灯-夙夜版"`, `sku: "YLP-Nightingale青空灯-夙夜版"` |

## Example SkillRequest Shape

```json
{
  "contractVersion": "1.0",
  "requestId": "generated-id",
  "locale": "zh-CN",
  "utterance": "帮我查一下青空灯说明书和常见问题",
  "intent": "product.pedia.search",
  "parameters": {
    "query": "青空灯"
  }
}
```
