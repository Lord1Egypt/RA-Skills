# Product Knowledge

Use this reference for Yeelight product consultation, pedia search, manuals, FAQ candidates, material-code resources, attachments, and product specification questions.

## Intent Routing

- Use `product.pedia.search` for product information by fuzzy wording, product name, short name, material code, SKU, SPU, model, model number, barcode, manual, FAQ, installation guide, user guide, product image, product资料, or product简介.
- Put the most specific user phrase into `parameters.multiField`. Prefer material code first, then model/SKU, then exact product name, then the user's fuzzy keyword.
- Accept semantic parameter aliases when the user states them clearly: materialCode, productModel, model, productName, sku, keyword, query, name, pid.
- Keep the original user text in `utterance`; Runtime can use it as the fallback query if parameters are incomplete.
- Use `thing.product.info.batch_get`, `thing.product.info.v3.batch_get`, and `thing.schema.*` only for product model/schema questions where the user provides product ids or asks about capability vocabulary.
- Do not treat pedia results as proof that a device is installed or controllable in the user's home. Use `entity.capabilities`, `entity.list`, or `state.query` for installed-device truth.

## Response Rules

- Summarize by productName, productShortName, materialCode, productModel, productSku, productSpu, productBrand, category/class fields, support markers, status, and available resources. Do not dump every raw field by default.
- Preserve uncertainty when a field is absent or null. Say “资料中未给出” instead of inventing support, sale status, FAQ, or manual facts.
- Treat product-level attachments and resources attachments as source-returned records. Attachments whose type or name indicates 说明书/manual are stronger than candidate URLs.
- Treat manualCandidateUrl and faqCandidateUrl as predictable candidate resources. If Runtime marks candidate status as unverified, present them as possible resources, not guaranteed files.
- If multiple products match a broad keyword such as “青空灯”, give the most relevant few and ask whether the user wants a specific material code, model, or manual/FAQ.
- For “这个产品支持 Yeelight Pro/HomeKit 吗”, answer from isSupportYeelightPro and isSupportHomekit only when Runtime returns those fields.
- Never construct raw API requests, expose credential headers, or ask the user for a token. Always call Runtime through `scripts/invoke`.

## Natural Language Mapping

| User wording | Intent | Parameters |
| --- | --- | --- |
| 青空灯有什么资料 / 青空灯说明书 | `product.pedia.search` | `multiField: "青空灯"` |
| 查 1-000003268 的说明书 | `product.pedia.search` | multiField: "1-000003268", materialCode: "1-000003268" |
| YP-0117 是什么产品 | `product.pedia.search` | multiField: "YP-0117", productModel: "YP-0117" |
| Yeelight Pro Nightingale 青空灯夙夜版 FAQ | `product.pedia.search` | `multiField: "Yeelight Pro Nightingale青空灯夙夜版"` |
| YLP-Nightingale青空灯-夙夜版有图和说明书吗 | `product.pedia.search` | `multiField: "YLP-Nightingale青空灯-夙夜版"`, `sku: "YLP-Nightingale青空灯-夙夜版"` |

## Example SkillRequest Shape

```json
{
  "contractVersion": "1.0",
  "requestId": "generated-id",
  "locale": "zh-CN",
  "utterance": "帮我查一下青空灯说明书和常见问题",
  "intent": "product.pedia.search",
  "parameters": {
    "multiField": "青空灯"
  }
}
```
