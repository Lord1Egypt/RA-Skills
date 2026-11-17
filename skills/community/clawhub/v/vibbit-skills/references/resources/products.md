# Product library and creative inputs

Query, select, parse, save, update and delete products, supplying real inputs for marketing images, videos and research. Use [API client](../runtime/api-client.md) for authentication; reuse the same account, environment and selected product.

## Match the user's goal

| Goal | Operation |
| --- | --- |
| Browse my products or search by name | [list_products](../api/list_products.md), following actual pagination |
| Inspect or use a product | [get_product](../api/get_product.md) for detail |
| Analyze or preview a link only | [parse_products](../api/parse_products.md), without saving |
| Add supplied facts manually | [create_product](../api/create_product.md) |
| Import one or more links | Parse, then [batch_create_products](../api/batch_create_products.md) for selected successful entries |
| Update product information | Read detail first, then [update_product](../api/update_product.md) |
| Explicitly delete an identified product | [delete_product](../api/delete_product.md); never automatically clean up candidates |

Pages start at page=0. Use content, total_elements, total_pages, number and size for the actual scope. Resolve duplicate names using real IDs, images, sources and variants. Display numbers are not API IDs. Keep platform IDs as strings; third-party IDs/ASINs cannot replace them. Lists are summaries: read selected detail before production. Returned count does not prove an account-wide inventory.

## Prepare a product for marketing

Start from a link, existing ID/name or customer-supplied facts. An explicit request to produce marketing images/video from a product link includes parsing and saving by default. Respect analysis-only, planning-only, no-save and supplied-material-only requests. Complete existing facts need no mandatory parsing, import or competitor research.

1. **Retain the goal**: image/video purpose, market, language, style, count and duration. Do not ask again for confirmed choices. In video context, a product link with “make an ad for US customers” enters [product video](../workflows/product-video.md). Ask only when an unresolved deliverable type changes the outcome.
2. **Parse**: use parse_products, not video share-link parsing. Check every status, name, image, source and actual price/currency. Preserve successes and failures; do not fabricate missing facts or save failed entries.
3. **Match or save**: locate candidates using a known ID or list search, then compare detail's third_product_url, third_product_id, source and variant. Reuse an unambiguous identical product. Similar names/appearance do not prove identity; never silently overwrite facts. Save new products using the mapping below, retain real IDs and read detail. This check is not server idempotency.
4. **Prepare creative inputs**: retain real images, descriptions, claims, target market, forbidden expressions and customer additions with product ID, source and adopted references. Keep facts, customer requirements and AI profile/creative judgments separate. Continue to [marketing images](../workflows/product-marketing-image.md) or [product video](../workflows/product-video.md).

Parsing does not produce a platform ID; saving does. ai_analysis_status and selection_info_status may remain PENDING/PROCESSING after a successful save. Sufficient real facts can be used immediately, without claiming analysis completion. When a missing profile matters, make bounded detail checks based on actual state; do not invent analysis task IDs or poll indefinitely without a public lifecycle contract.

### Map parsed entries to saving

batch_create_products also accepts one parsed product. Select only documented input fields: url, name, price, price_unit, image_url, image_urls, description, selling_points, third_product_id, third_product_url, source, platform and status. Omit unknown/null optional values. Resolve missing names, source identity or essential reference images instead of inventing successful records.

Retain real third-party IDs and source links. If platform exists but source does not, the same source identifier can supply source. Use the actual third_product_id; do not copy source_asin, error_code, product_profile, target_market or other parse/detail fields into the request. Customer market, image purpose and creative instructions belong to the current production context, not undocumented save fields.

Match saved IDs to source identity, not array position. Read detail to resolve missing sources or duplicate names. Client item_summary counts succeeded, failed and unknown entries; result retains the raw response. Unmatched entries are not confirmed saves. For uncertain writes/timeouts, follow [task lifecycle](../runtime/task-lifecycle.md); never automatically repeat a save.

## Facts and reference images

A product_profile's audience, scenarios, visual hooks and marketing suggestions inform planning; they do not establish features, certifications or outcomes. Explicit customer facts take priority. Surface conflicts rather than allowing an outdated profile to override current facts. Reviews and research inferences are not product promises.

Select images from image_urls and image_url that accurately show the chosen variant. Deduplicate and inspect clarity, specification, color, packaging and purpose. Exclude icons, video play markers, unrelated products and wrong variants; do not simply take the first images. Follow [image preview](../runtime/media-preview.md), and claim inspection only for what was actually viewed.

Pass actual reference URLs to image/video generation. Merely mentioning a product is not supplying a reference. Prefer the customer's selected photos. Resolve inaccessible URLs without treating generated concept images as source evidence. Saving image URLs does not register materials or produce material_id.

## Updates, delivery and continuation

Read and retain current detail, requested changes and documented writable values before updating. The CLI currently accepts name, price/currency, description and selling points. Omission/null/clearing semantics are not established; do not promise arbitrary lossless patches. Resolve behavior first when existing information may be lost. Target market, forbidden expressions and AI profiles are readable; frontend fields do not establish OpenAPI write support.

Present name, image, real ID, source and actual state. Background, claim, language or shot revisions reuse the product and adopted assets. Product saves, material links, saved marketing outputs and editable platform projects are separate operations. Current product commands do not attach generated media or create projects.

Use [product research](../workflows/product-research.md) for research. Save selected candidates when requested, without writing an entire research report into product fields.
