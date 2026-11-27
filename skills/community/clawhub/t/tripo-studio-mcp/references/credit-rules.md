# Feature entitlements and credit rules

Use these values as reference estimates. Check [Tripo Studio](https://studio.tripo3d.ai/) for current plan terms and account allowances. The connected tool catalogue defines which operations are available.

- Check the plan, feature restrictions, base credits and add-ons together. A missing price does not establish that an operation is free.
- An operation that consumes no credits can still require membership, export quota, storage capacity or a Studio-side trial allowance.
- MCP cannot query or use an account's remaining trial uses. Do not present Studio-side trial terms as MCP availability or as a confirmed account entitlement.
- If an applicable cost or entitlement is unclear, explain what needs verification before estimating an account-specific charge.

## Modeling base credits

These rows describe the base operation, before applicable add-ons. “Paid plans”
refers to Starter, Pro, Advanced and Max;
permissions and allowances are not evidence of the current account's tier.

| Operation | Reference base credits | Plan conditions |
| --- | --- | --- |
| Text or single-image HD v2.5/v3.0/v3.1 | 15 | Basic and paid plans marked available |
| Multiview HD, same three versions | 15 | Basic unavailable; paid plans available |
| Text or single-image Smart Mesh P1 | 35 | Basic and paid plans marked available |
| Multiview Smart Mesh P1 | 35 | Basic unavailable; paid plans available |
| Text, image or multiview Smart Mesh P2 | 100 | Paid plans available; any Basic trial terms are Studio-side only. MCP cannot query or use remaining trial uses |

Use P1/P2 aliases only when supported by the connected schema; see
[Generation](generation.md). MCP cannot query or use remaining trial uses, and a
reference cost does not establish that an account can afford the operation.

## Options and processing rules

| Feature | Documented credits | Conditions and interpretation |
| --- | --- | --- |
| 2K texture (`texture_quality: standard`) | 10 | Base texture item, not the modeling base price |
| 4K texture (`texture_quality: detailed`) | Additional 10 on 2K | Texture component totals 20 when that combination applies |
| 8K texture (`texture_quality: extreme`) | Additional 20 on 2K | Texture component totals 30 when applicable; eligibility is Studio-side. MCP cannot query or use remaining trial uses, so do not promise access |
| HD generation quads | Additional 5 | Listed for those HD versions; do not apply automatically to P1/P2 |
| HD detailed geometry | 15 | Applies to detailed geometry when supported by the selected model version |
| Part generation | 30 | Member feature; any Basic trial terms are Studio-side only. MCP cannot query or use remaining trial uses. May apply in addition to generation. MCP requires texture=false |
| Segmentation | 40 | Member feature; any Basic trial terms are Studio-side only. MCP cannot query or use remaining trial uses |
| Triangle retopology | 5 | Distinguish from smart low-poly |
| Quad retopology | Additional 5 on triangle retopology | 10 total for the two retopology components when applicable |
| Smart low-poly | 30 | Basic unavailable; paid plans available |
| Texture style reference | 5 | Separate option; do not apply without that option |
| PBR | 5 | Feature rule, not the total cost of a larger workflow |
| Rigging/animation | 20 | Do not apply this row to every motion or retarget request |
| Motion generation | 20 | The reference does not specify per-request, per-segment or duration-based units; do not invent them |
| Image upscale | 10 per image | Basic unavailable; Starter/Pro/Max shown available; Check Advanced eligibility in Studio |
| UV generation | Studio-side trial or paid terms | MCP cannot query or use remaining trial uses. UV retry is a separate rule, not the MCP UV unwrap operation |
| Texture upscale | 10 | Member feature with 8K-only-Max note; Confirm the applicable option and total in Studio |

Check current Studio terms for 8K eligibility. MCP cannot query or use remaining trial uses.

## Explicitly non-credit features

| Feature | Product rule | MCP or entitlement boundary |
| --- | --- | --- |
| Manual part completion | No credits; all plans marked available | Do not assume the AI completion tool is this manual feature |
| AI completion | No credits; Basic unavailable | Check eligibility for the specific operation in Studio |
| Motion retarget | No credits; Basic/Starter/Pro/Max marked available | Check eligibility for the requested operation |
| Own-model export | No credits, with plan limits | Basic: HD v2.5 only, up to 15 models/month. Starter download row: 45/month; higher plans unlimited. Remaining quota is unknown |
| Image multiview | No credits; member feature | Distinct from multiview-to-model, which consumes modeling credits |
| Image split | No credits; member feature | Basic unavailable, not unrestricted free use |
| Model import | No credits; listed plans available | Storage/asset eligibility still apply; not proof of import success |

Rows absent from this reference do not default to free. Do not apply a UI-only
feature rule to an unrelated MCP tool merely because the names resemble one
another. Other export sources, public models, retry types and plan-specific
exceptions can have different rules.

## Answering a cost question

For “P2 with textures, about how many credits; do not generate,” explain that
the documented modeling base is **100 credits**, with applicable texture charges
and any Studio-side eligibility conditions. MCP cannot query or use remaining
trial uses. If texture resolution is unspecified, do not
invent one to give a single total. State that this is a reference rule, not the
account's final charge, then stop without tools or a submission offer.

A supported component calculation can be explained: HD base 15 + 2K texture 10
= **25 reference credits**, assuming those are the selected components with no
other add-ons or allowances. Do not apply that sum to an unspecified request.
A hard account-specific spending cap still needs verification/enforcement that
this static reference cannot provide. Monthly plan credit grants are allocations,
not the user's current balance; they cannot establish whether a write is affordable.
