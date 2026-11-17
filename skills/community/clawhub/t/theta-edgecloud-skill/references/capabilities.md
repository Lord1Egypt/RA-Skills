# Capability map and verified API contracts

## On-demand

Commands: `list_services`, `infer`, `get_request_status`, `get_upload_url`;
`theta.ondemand.listServices|infer|chat|status|inputPresignedUrls|pollUntilDone`.

Discovery base: `https://ondemand.thetaedgecloud.com/service/list?expand=template_id`.
Inspect all predictions, not just the default: `image_to_image` advertises
`stylize` (image_filename + style_image_filename), `upscale` and
`background_removal`. The service validates every field across predictions,
so send `style_image_filename:""` for non-stylize operations. Job inference
uses `/infer_request/{service}?prediction=...&wait=...`; the runtime also
puts `prediction` in the body, because the live API (2026-10-03) ignored the
query value and ran the default `stylize`. Request variant/webhook are
top-level; service input belongs under `input`.

Chat via `/infer_request/chat/completions` (`model:<slug>`): `glm_5_3`,
`glm_5_3_flash`, `qwen3_8_max`, `qwen3_8_flash` (optional `enable_thinking`),
`ling_3_0_flash_fin`. Structured tool calls work only on GLM-5.3/Flash. Live
2026-10-03, Qwen3.8 and Ling accepted `tools` but ignored them, so the runtime
rejects tools for them unless `allowUnverifiedTools` is exactly `true`. Ling writes its
reasoning into `content`: give it at least 1024 `max_tokens` (default 2048).
Its catalog price shows 0/0; treat the cost as unknown. `qwen3` keeps its
streaming job route.

Uploads: `get_upload_url` returns `uploads[field] = {upload_url, filename}`
(live raw shape `body[field].presigned_url`; legacy npm MCP 0.1.7 expected
`body.urls`). PUT the bytes with `Content-Type: application/octet-stream`;
other types fail the signature with 403. Pass `filename` as the input value.

Live public list 2026-10-03 (13): `ling_3_0_flash_fin`, `qwen3_8_max`,
`qwen3_8_flash`, `glm_5_3`, `glm_5_3_flash`, `qwen3`, `seedance_2_5`, `blip`,
`esrgan`, `image_to_image`, `stable_diffusion_xl_turbo`, `llava`, `whisper`.
This is a dated snapshot, NOT an allowlist. FLUX, step_video, GLM-5.2,
GPT-OSS, MiniMax and Llama are retired (`liveStatus` marks them).
`seedance_2_5` (BytePlus) is high-cost video and needs `confirm:true`; it
returned 503 "temporarily unavailable" on 2026-10-03. Its duration is 4–30 (the
MCP example value 1 is invalid).
ESRGAN can report "No instances available" and still record a cost on the
failed job.

Normalized chat output keeps `output.message`, `output.tool_calls`, model,
finish reason, usage and reasoning separately. For tool continuation pass the
assistant message with `content:null, tool_calls:[...]`, then a tool message
with the matching `tool_call_id`. Never execute unvalidated model tool arguments.

## GPU and dedicated serving

- `theta.deployments.listVm`: raw VM resource/specification/price catalog.
- `theta.templates.listStandard`: category `prototyping`, `serving`, or `training`.
- `theta.templates.listCustom`: `projectId` or configured project.
- `theta.deployments.list|create|start|stop|delete|routeProbe|validateDisposable`.
- `theta.deployments.startByBaseId`: `baseId`, optional configured `projectId`;
  documented PUT `/deployments/base/{baseId}/start?project_id=...`.
  This is restart of a STOPPED node, not a proven atomic restart of a running one.
- `theta.inference.models|chat|ready`: existing dedicated endpoints; select
  OpenAI `/v1/models` or Gradio `/config` readiness as appropriate.

### Hosted MCP (GPU Nodes + billing)

The expanded API from the Aug 27 announcement is published only as the
official hosted MCP server: server card
`https://www.thetaedgecloud.com/.well-known/mcp/server-card.json`, endpoint
`https://controller.thetaedgecloud.com/mcp`. The runtime calls it with
stateless JSON-RPC `tools/call` (SSE response) and the project key
(`x-api-key`, `THETA_EC_API_KEY`). It sends `project_id` from config and never
retries.
- `theta.gpu.resources.list`: hosted + community GPUs with country/region,
  availability and `price_per_hour_usd`. Filters: `provider`, `gpuModel`,
  `region`, `maxPricePerHourUsd`, `availableOnly`, `limit`; sorted cheapest
  first. 2026-10-03: 54 resources, community RTX 3060 from USD 0.065/h.
- `theta.gpu.resources.get` (`resourceId`, `region?`),
  `theta.gpu.templates.list`.
- `theta.gpu.deployments.list|get|events|logs` (`deploymentId`).
- `theta.gpu.deployments.create`: PAID. Requires `name`,
  `deploymentTemplateId`, `resourceId`, `maxPricePerHourUsd` (sent as Theta's
  provider-side price cap) and `confirm:true` after approval. Before
  provisioning, it refuses when the listed price exceeds the cap.
- `theta.gpu.deployments.start|stop|delete` (`deploymentId`, `confirm:true`).
  Start resumes billing; delete is permanent. All honour dry-run.
- `theta.billing.balance`: credits and USD (1 credit = USD 0.01). It falls
  back to the raw controller credit value if MCP fails.
- `theta.billing.usage` (`startDate`/`endDate` real YYYY-MM-DD dates, end not before
  start, range at most 366 days; validated locally),
  `theta.billing.topUps`, `theta.billing.pricing` (chatbot/storage; on-demand
  list may be empty; GPU prices come from resources).
- `theta.billing.balanceSnapshot`: raw numeric extraction for older flows.

The legacy npm `@thetalabs/on-demand-api-mcp@0.1.7` exposes only four on-demand
tools and the stale upload shape. Use the hosted server card instead.
The MCP's `infer` tool needs on-demand Bearer auth, not the project key.

## RAG

`theta.ai.agent.create|get|update|list` and
`theta.ai.agent.document.create|update|get|list` accept project-scoped controller
credentials. Document create/update takes `file:{filename,content,contentType?,
encoding?}`; it does not read paths from disk. Existing settings payloads support
documented agent tool toggles, but there is no independently verified custom-tool
management wrapper. Do not claim deletion commands that are not registered.

## Video hosting and streams

`theta.video.list` takes `serviceAccountId`; also exposed:
`uploadCreate`, `create` (`payload`), `get` (`videoId`), `streamCreate`
(`payload`), `streamGet` (`streamId`), `ingestorList`, `ingestorSelect`
(`ingestorId`, `body`). These call `https://api.thetavideoapi.com` using Video
service-account credentials, not the on-demand token. Search, stream listing,
ingestor unselect and analytics are not registered; consult their API specs
before adding adapters. Video hosting is not on-demand generative video.

## AI Characters

Official OpenAPI 1.0.0 base: `https://ai-chars-api.thetaedgecloud.com`.
Auth: separate per-game `THETA_CHARACTERS_API_KEY` Bearer token.
Registered `theta.characters.*` operations:
- `list|get|create|update|delete`: `gameId`, plus `characterId` for get/update/delete.
- `session.create`: payload matching SessionCreate.
- `session.get|session.delete`: `sessionId`.
- `session.list`: `gameId`.
- `session.context|session.message`: `sessionId`, `payload` matching the OpenAPI.
- `session.messages`: `sessionId`.

POST/PUT require an object `payload`. Every non-GET operation, including
`session.message` and `session.context`, requires `confirm:true` outside dry-run.
IDs are encoded, host is fixed, mutations honor dry-run and are never resent
automatically. Payload bodies remain spec-driven
pass-through; verify schemas when constructing them. No game creation, dashboard
session capture or game-key renewal is exposed. Runtime tests use fixtures;
live Characters tests require a configured game and approved test scope.

## Sources

- https://blog.thetatoken.org/ai-agents-can-now-deploy-edgecloud-gpus-themselves/
- https://blog.thetatoken.org/build-ai-characters-into-your-game-with-theta/
- https://github.com/thetatoken/on-demand-api-mcp
- https://www.thetaedgecloud.com/.well-known/mcp/server-card.json
- https://blog.thetatoken.org/theta-edgecloud-integrates-ling-3-0-flash-fin-via-zan/
- https://blog.thetatoken.org/seedance-2-5-and-byteplus-frontier-models-are-now-live-on-theta-edgecloud/
- https://github.com/thetatoken/theta-edge-cloud-ai-characters-public/blob/main/reference/ai-characters-openapi.json
- https://github.com/thetatoken/theta-edgecloud-chatbot-knowledge-example
- https://docs.thetatoken.org/docs/use-edgecloud-api-keys-to-manage-deployments

During the review the docs site blocked direct fetches (403). Previously imported
official deployment documentation was cross-checked with live read-only APIs;
the public GitHub specs, current blog and live service catalog were reachable.
