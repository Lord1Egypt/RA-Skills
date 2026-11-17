# Architecture Diagrams (`/draw/archmap`)

## When to Use

System topology, folder/service hierarchy, microservice maps, deployment views, tech-stack overviews. Use it when the user asks to *"map the architecture"*, *"show the system design"*, *"visualize the repo structure"*, or *"draw how the services connect"*.

Patterns that fit: layered tiers (client → edge → service → data), request path across components, or a module map where adjacency matters. For temporal call ordering use `seq` (see `flowchart.md`); for weighted data movement use `sankey` (see `sankey.md`).

## URL Schema & Encoding Rule

```
https://x-cmd.com/draw/archmap?n=<node>[&n=<node>...][&e=<edge>...][&b=<boundary>...][&title=][&t=][&scheme=][&w=][&h=]
```

Three repeatable parameters form the whole grammar (learn once, reused by `arch2`, `seq`, `uc`, `dataflow`, `lifecycle`, `erd`, `class`):

```
n=id;type;label[;sub][;pos]      # node   (repeat for each node)
e=from;to[;label][;variant]      # edge   (repeat for each edge)
b=label;id id ...                # boundary box around existing node ids
```

| Field | Rule |
|---|---|
| `id` | Letters, digits, `.` `-` `_`. Must not start with punctuation. Referenced by `e=` and `b=`. |
| `type` | One of `ext fe be db cloud sec bus svc` (semantic colors: ext=external user, fe=frontend, be=backend, db=database, cloud=cloud service, sec=security, bus=message bus, svc=generic service). Wrong type = 400 whose message lists the valid set. |
| `label` | Big text. Spaces as `%20`. |
| `sub` | Small caption under the label; `%0A` inserts a line break (e.g. a port list or file path). Leave empty (`;;`) when only `pos` is needed. |
| `pos` | Optional. Grid cell `r<row>c<col>` (0-based), span `r0c1w2` (wide) / `r1c0h2` (tall, max span 3), or pixel escape `p40,80[,120x48]`. Omit it and the engine auto-layouts nodes in the order written. |
| `e=` variant | `main` = emphasized primary-flow edge; `dash` = secondary edge. Omit for a normal edge. |

**Encoding (applies to every repoviz diagram URL):** space `%20` (a bare `+` also parses as space, but `%20` is canonical), literal plus `%2B`, `&` `%26`, `#` `%23`, `<` `%3C`, `>` `%3E`, newline `%0A`. Structural separators `;` `=` `,` `:` `/` `@` stay unescaped. Build URLs from plain text by percent-encoding only those characters — no Base64, no deflate.

**Common modifiers:** `title=` diagram title · `scheme=dark|light` · `t=evil` (alternate style family) · `w=` 200–1600 / `h=` 140–1200.

**arch2 extras — icons & skins:** `/draw/arch2` (the prettier architecture sibling of `archmap`) accepts an optional **6th field on `n=` — a tech icon**, and shines with `t=shadcn`:

```
n=api;be;API service;ECS Fargate;r2c0;aws:ecs
```

Icons use `namespace:name` tokens; confirmed namespaces include `aws:*` (e.g. `aws:ecs`, `aws:rds`, `aws:lambda`, `aws:s3`, `aws:sqs`, `aws:dynamodb`, `aws:redis`, `aws:alb`, `aws:cloudfront`, `aws:cloudwatch`, `aws:route53`, `aws:opensearch`, `aws:apigw`, `aws:iam`, `aws:igw`, `aws:nlb`, `aws:eks`, `aws:codebuild`, `aws:codepipeline`, `aws:codedeploy`, `aws:ecr`) and `org:*` (registries/organizations). Unknown icons are ignored silently — the node still renders, so icon fields are safe to sprinkle in. Grid positions, spans, and boundaries work exactly as in `archmap`; both endpoints share the same `n=`/`e=`/`b=` grammar.

**CJK note for PNG export:** the rasterizer embeds a subsetted Noto Sans SC (GB2312 level-1 only). Rare characters outside the subset (e.g. `渲`) render as tofu in **PNG** output. SVG output is unaffected. Prefer common synonyms in Chinese PNG labels (`渲染` → `生成`).

## Minimal Working Example (5 nodes)

Raw definition (readable form):

```
n=web;fe;Browser;;r0c0
n=cdn;cloud;CDN;;r0c1
n=gw;be;API;;r0c2
n=auth;sec;Auth;;r1c1
n=pg;db;Postgres;;r1c2
e=web;cdn;https
e=cdn;gw
e=gw;auth;verify;main
e=gw;pg;sql
```

Final URL (each `n=`/`e=` becomes one query parameter, `&`-joined):

```
https://x-cmd.com/draw/archmap?n=web;fe;Browser;;r0c0&n=cdn;cloud;CDN;;r0c1&n=gw;be;API;;r0c2&n=auth;sec;Auth;;r1c1&n=pg;db;Postgres;;r1c2&e=web;cdn;https&e=cdn;gw&e=gw;auth;verify;main&e=gw;pg;sql&title=Minimal%20service
```

## Production Repo Example

Three-tier web service: CDN in front, gateway routing to auth + core service, data layer boxed by `b=`, one node spanning two columns:

```
https://x-cmd.com/draw/archmap?title=Sample%20web%20service&n=user;ext;User;;r0c0&n=cdn;cloud;CDN;;r0c1&n=gw;be;API%20Gateway;rate%20limit;r0c2&n=auth;sec;Auth;JWT;r1c1&n=svc;be;Core%20Service;logic;r1c2&n=pg;db;Postgres;;r2c1&n=redis;db;Redis;cache;r2c2&e=user;cdn;https&e=cdn;gw&e=gw;auth;verify;main&e=gw;svc;route;main&e=auth;svc;claims&e=svc;pg;sql;main&e=svc;redis;cache&b=Data%20Layer;pg%20redis
```

Pixel-position variant for fine control: `n=a;fe;A;p40,80&n=b;be;B;p200,80&e=a;b` (x,y in pixels, optional `120x48` size).

## Anti-Patterns & Limits

- **Hard limit: ≤500 nodes.** Beyond that, split into an overview `archmap` plus per-subsystem diagrams (repoviz does this automatically for large repos).
- Keep a single diagram to ~15–20 nodes so the URL stays readable and well within CDN limits; prefer `b=` boundaries over drawing every file.
- A 400 `unknown type "x" (one of ext/fe/be/db/cloud/sec/bus/svc)` means a bad `type` token — fix the node, the error already shows the valid vocabulary.
- Spans wider than 3 (`w4`) are rejected; scale the grid instead.
- `b=` only groups **existing** ids — it never creates nodes. A boundary referencing a missing id renders incomplete. Encode the spaces between ids as `%20` (`b=Data%20Layer;pg%20redis`): raw spaces inside the URL get the request dropped before it reaches the renderer.
- Unescaped `&` or `#` inside a label silently truncates the diagram — always `%26` / `%23`.
- Long labels are truncated by the engine rather than overlapping; keep labels ≤ ~24 chars and move detail into `sub`.
