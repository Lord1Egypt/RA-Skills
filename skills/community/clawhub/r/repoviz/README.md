<div align="center">

# Repoviz

**Turn any codebase into architecture, flowchart, and Sankey diagrams — zero setup, instant Markdown URLs, optional SVG/PNG/HTML export.**

English | [简体中文](README.zh.md)

![Claude Code](https://img.shields.io/badge/Claude%20Code-native-blue)
![Cursor](https://img.shields.io/badge/Cursor-native-blue)
![Windsurf](https://img.shields.io/badge/Windsurf-native-blue)
![Codex CLI](https://img.shields.io/badge/Codex%20CLI-compatible-blue)
![ClawHub](https://img.shields.io/badge/ClawHub-publishable-green)
![skills.sh](https://img.shields.io/badge/skills.sh-installable-green)

</div>

`repoviz` is an agent skill that scans a repository and answers with the right
visualization — an **architecture map**, **Sankey flow**, **flowchart**,
**sequence diagram**, **mind map**, or **Gantt chart** — rendered as a single
embeddable URL. No local installs, no file writes by default; every diagram is a
Markdown image link you can paste into a README, doc, or chat.

**Live showcase** — these render right now, from real URLs (a production AWS platform, and where its budget goes):

![repoviz architecture sample](https://x-cmd.com/draw/arch2?t=shadcn&title=Production%20web%20platform%20on%20AWS&n=r53;cloud;Route%2053;DNS;r0c0;aws:route53&n=waf;sec;WAF;rules;r0c1&n=cf;cloud;CloudFront;CDN;r0c2;aws:cloudfront&n=s3;db;S3;static%20assets;r0c3;aws:s3&n=igw;cloud;Internet%20Gateway;public%20ingress;r1c3;aws:igw&n=alb;cloud;ALB;HTTPS%20443;r1c2;aws:alb&n=api;be;API%20service;ECS%20Fargate;r2c0;aws:ecs&n=lam;be;Lambda;async%20jobs;r2c1;aws:lambda&n=sqs;bus;SQS;queue;r2c2;aws:sqs&n=auth;sec;Cognito;OIDC;r2c3&n=rds;db;RDS;PostgreSQL;r3c0;aws:rds&n=redis;db;ElastiCache;session%20cache;r3c1;aws:redis&n=ddb;db;DynamoDB;items;r3c2;aws:dynamodb&n=os;db;OpenSearch;index;r3c3;aws:opensearch&n=cw;be;CloudWatch;metrics%20%26%20alerts;r4c1;aws:cloudwatch&n=sns;bus;SNS;notifications;r4c2&e=r53;cf;resolve&e=waf;cf;filter&e=cf;alb;forward;main&e=cf;s3;static&e=igw;alb;public&e=alb;api;route;main&e=api;auth;verify&e=api;rds;query;main&e=api;ddb;read%20%26%20write;main&e=api;redis;cache&e=api;lam;enqueue&e=lam;sqs;consume&e=sqs;sns;notify&e=lam;os;index&e=api;cw;OTLP&e=lam;cw;logs&b=Edge;r53%20waf%20cf%20s3%20igw%20alb&b=Compute;api%20lam%20auth&b=Data;rds%20redis%20ddb%20os%20sqs%20sns%20cw)

![repoviz sankey sample](https://x-cmd.com/draw?type=sankey&t=fund&labels=Budget,Compute,Storage,Network,Data,Prod,ML,Analytics,Other&links=Budget>Compute:42;Budget>Storage:18;Budget>Network:14;Budget>Data:26;Compute>Prod:30;Compute>ML:12;Storage>Prod:8;Storage>Other:10;Network>Other:14;Data>Analytics:17;Data>ML:9&title=Monthly%20cloud%20spend&unit=%241k&w=880&h=540)

## Why repoviz?

Four properties that change how diagrams live in your repo:

* **🔗 URL-as-Data (AI-Native Diagrams)** — every diagram URL self-contains its
  full structural definition. Future AI agents can read, understand, and
  incrementally update your diagrams **directly from the URL text — zero
  vision/multimodal tokens required**.
* **🔄 Living Documentation** — traditional diagrams rot the moment code changes.
  Because repoviz diagrams are lightweight text URLs, one prompt regenerates and
  syncs every chart after a refactor (`scripts/inject_readme.sh` keeps the README
  block updatable in place).
* **🎨 Publication-Grade Aesthetics** — powered by [x-cmd draw](https://x-cmd.com/draw),
  dry code structures become clean, high-readability **Architecture, Sankey,
  Flowchart, and Sequence** visuals that make READMEs and RFCs stand out.
* **🪶 Zero Repo Bloat** — no binary `.png` or massive `.svg` diffs cluttering your
  Git history — with one-command local SVG / PNG / standalone HTML export whenever
  you need offline assets.

| | Raw Mermaid | Frontend-Only Generators | **repoviz** |
|---|---|---|---|
| Diagram variety (Sankey / Arch / Flow / Seq / Mindmap / Gantt) | Flow + Seq only | Usually one fixed type | **All six, auto-routed per intent** |
| Local dependencies | JS runtime or CLI install | Node + browser toolchain | **Zero — URLs render in any Markdown viewer** |
| Token efficiency | Verbose DSL per diagram | Full AST dumps | **Flat, readable URL params; agent reads 1 manifest, not 100 files** |
| Markdown / README readiness | Needs a renderer on the viewer side | Export step required | **Paste the URL — done** |
| Offline export (SVG / PNG / HTML) | CLI only | Often paid/watermarked | **One `sh` script call each, POSIX + curl only** |

## Chart gallery

Copy a prompt, drop it in your agent (with repoviz installed), and it scans + routes + answers with a live diagram:

**1. Delivery pipeline** — *"Map this repo's CI/CD pipeline."*

![Architecture gallery](https://x-cmd.com/draw/arch2?t=shadcn&title=CI%2FCD%20pipeline%20on%20AWS&n=src;ext;GitHub;source%20repo;r0c0&n=pipe;be;CodePipeline;orchestration;r1c0;aws:codepipeline&n=build;be;CodeBuild;build%20%2B%20test;r1c1;aws:codebuild&n=ecr;db;ECR;image%20registry;r2c1;aws:ecr&n=ecs;be;ECS%20Fargate;run%20containers;r2c2;aws:ecs&n=cd;be;CodeDeploy;canary%20release;r3c2;aws:codedeploy&n=obs;be;CloudWatch;logs%20%26%20alerts;r3c3;aws:cloudwatch&e=src;pipe;push%20triggers&e=pipe;build&e=build;ecr;push%20image&e=build;obs;logs&e=ecr;ecs;pull%20image&e=ecs;cd;deploy&e=cd;obs;metrics&e=obs;pipe;rollback%3Bdash&b=Pipeline;pipe%20build%20ecr%20ecs%20cd)

**2. Data pipeline (Sankey)** — *"Trace how data flows through this pipeline."*

![Sankey gallery](https://x-cmd.com/draw?type=sankey&t=pipeline&labels=Events,Collector,Stream,Hot%20Store,Cold%20Store,Dashboard,ML%20Pipeline&links=Events>Collector:100;Collector>Stream:96;Stream>Hot%20Store:40;Stream>Cold%20Store:56;Hot%20Store>Dashboard:32;Hot%20Store>ML%20Pipeline:8;Cold%20Store>ML%20Pipeline:30;Cold%20Store>Dashboard:12&title=Data%20pipeline%20flow&unit=GB%2Fday&w=880&h=540)

**3. Execution flow (agent loop)** — *"Walk me through how repoviz handles one request, end to end."*

![Agent loop gallery](https://x-cmd.com/draw/arch2?t=shadcn&title=One%20repoviz%20request%2C%20end%20to%20end&n=input;fe;User%20request;repo%20%26%20intent;r0c0&n=scan;be;Repo%20scan;manifests%20%26%20entries;r0c1&n=route;be;Chart%20routing;references%2F%2A.md;r0c2&n=build;svc;Build%20URL;encode%20nodes%20%26%20edges;r0c3&n=guard;sec;Guardrails;URL%20length%20%26%20escaping;r1c3&n=render;svc;Render;SVG%20via%20URL;r1c2&n=export;svc;Export;SVG%20%C2%B7%20PNG%20%C2%B7%20HTML;r1c1&n=final;fe;Answer;diagram%20%2B%20link%20%2B%20notes;r1c0&n=refs;db;Syntax%20refs;references%2F%2A.md;r2c1&n=notes;svc;Insights;bullets%20per%20diagram;r2c2&e=input;scan&e=scan;route&e=route;build&e=build;guard&e=guard;render&e=render;export&e=export;final&e=route;refs;lazy-load&e=refs;build;grammar&e=render;notes&e=notes;final&e=final;input;feedback%3Bdash&b=Agent%20loop;input%20scan%20route%20build%20guard%20render%20export%20final&b=Knowledge;refs%20notes)

**4. Sequence diagram** — *"Show the API handshake sequence for creating an order."*

![Sequence gallery](https://x-cmd.com/draw/seq?t=shadcn&title=API%20handshake&n=c;fe;Client;&n=g;be;API%20Gateway;&n=a;sec;Auth;&n=s;be;Service;&e=c;g;POST%20%2Forders&e=g;a;verify%20token&e=a;g;claims;dash&e=g;s;forward&e=s;g;201%20Created;dash)

**5. ERD (database schema)** — *"Document this project's database schema as an ERD."*

![ERD gallery](https://x-cmd.com/draw/erd?title=Multi-tenant%20SaaS%20schema&n=tenants;table;tenants;id%3Auuid%20%28pk%29%0Aslug%3Atext%20%28uk%29%0Aplan%3Atext%0Acreated_at%3Atimestamp;r0c0&n=users;table;users;id%3Auuid%20%28pk%29%0Aemail%3Atext%20%28uk%29%0Acreated_at%3Atimestamp;r0c2&n=memberships;table;memberships;tenant_id%3Auuid%20%28fk%29%0Auser_id%3Auuid%20%28fk%29%0Arole%3Atext%0Ajoined_at%3Atimestamp;r1c1&n=projects;table;projects;id%3Auuid%20%28pk%29%0Atenant_id%3Auuid%20%28fk%29%0Aname%3Atext%0Aarchived_at%3Atimestamp;r2c0&n=tasks;table;tasks;id%3Auuid%20%28pk%29%0Aproject_id%3Auuid%20%28fk%29%0Aassignee_id%3Auuid%20%28fk%29%0Atitle%3Atext%0Astatus%3Atext%0Adue_at%3Atimestamp;r2c2&n=comments;table;comments;id%3Auuid%20%28pk%29%0Atask_id%3Auuid%20%28fk%29%0Aauthor_id%3Auuid%20%28fk%29%0Abody%3Atext%0Acreated_at%3Atimestamp;r3c1&e=tenants;memberships;1%3AN&e=users;memberships;1%3AN&e=tenants;projects;1%3AN&e=projects;tasks;1%3AN&e=users;tasks;1%3AN&e=tasks;comments;1%3AN&e=users;comments;1%3AN)

**6. Gantt (release plan)** — *"Plan the v2.0 release on a Gantt chart."*

![Gantt gallery](https://x-cmd.com/draw/gantt2?title=Release%20plan&m=gantt%0A%20%20dateFormat%20YYYY-MM-DD%0A%20%20section%20Core%0A%20%20Scan%20engine%20%3Adone%2C%20s1%2C%202026-11-02%2C%204d%0A%20%20Chart%20router%20%3Aactive%2C%20s2%2C%20after%20s1%2C%203d%0A%20%20section%20Export%0A%20%20HTML%20report%20%3As3%2C%20after%20s2%2C%205d)

**7. Mind map (feature tree)** — *"Lay out repoviz's feature tree as a mind map."*

![Mindmap gallery](https://x-cmd.com/draw/mindmap?style=tree&title=repoviz%20feature%20map&n=repoviz%2FCharts%2FArchitecture&n=repoviz%2FCharts%2FSequence&n=repoviz%2FCharts%2FSankey&n=repoviz%2FCharts%2FFlowchart&n=repoviz%2FCharts%2FMindmap&n=repoviz%2FCharts%2FGantt&n=repoviz%2FExport%2FSVG&n=repoviz%2FExport%2FPNG&n=repoviz%2FExport%2FHTML%20report&n=repoviz%2FOutput%2FMarkdown%20links)

> More chart types (class, dataflow, lifecycle, use-case, radar, butterfly, quadrant, calendar, QR, and the full metric-chart set) live in [`references/`](references/) and in the [gallery issue](https://github.com/qiakai/repoviz/issues/1) — every URL is live-tested.


## Quick installation

```bash
# Install via the skills CLI (works with Claude Code, Cursor, Windsurf, Codex, ...)
# (skills CLI pinned to 1.8.1 -- the version this README was verified against)
npx skills@1.8.1 add qiakai/repoviz

# Or via ClawHub (OpenClaw agents)
clawhub install repoviz
```

Manual install — just copy the folder into your agent's skills directory:

```bash
# Claude Code
git clone https://github.com/qiakai/repoviz ~/.claude/skills/repoviz

# Cursor
git clone https://github.com/qiakai/repoviz ~/.cursor/skills/repoviz
```

That's it: no packages, no build step, no API keys. The export scripts need only
POSIX `sh` + `curl` (both already on macOS, Linux, and Windows Git Bash).

## Usage prompts (copy & paste)

**Default — Markdown URL mode (writes nothing locally):**

```
Visualize this repo's architecture as a diagram I can embed in the README.
```

**Multi-chart deep-dive:**

```
Give me a full visual breakdown of this codebase: a system architecture diagram,
a Sankey of the data flow, and a sequence diagram of the main request lifecycle.
```

**Local SVG / PNG export:**

```
Map the architecture and save it locally as an SVG (also a PNG at 2x for the slides).
```

**Standalone HTML report:**

```
Scan this repo and generate a standalone HTML report with the architecture,
data-flow Sankey, and your notes — dark mode aware, for sharing with the team.
```

**PR / change impact (delta diagram):**

```
What does this PR change architecturally? Base is main. Show the blast radius
as a delta diagram plus a +/- summary for the review.
```

**Embed diagrams into the README (in place):**

```
Visualize the architecture and put the diagrams straight into my README.md —
keep that block updatable on future runs.
```

**Short links & batch export:**

```
Save the Sankey as a 2x PNG and the architecture as an SVG in ./assets, and
give me a permanent short link for the Sankey — the URL is getting huge.
```

Under the hood the agent picks the right chart type (routing table in
`SKILL.md`), scans manifests and entry points with a token budget, and emits
flat percent-encoded render URLs — plus, only on request, runs
`scripts/export.sh` (single or `--batch`), `scripts/shorten.sh`,
`scripts/build_html.sh` (with filterable source-evidence tables and PDF-friendly
printing), `scripts/inject_readme.sh`, or `scripts/validate.sh`.

## Privacy & security

- **Rendering transmits labels, not files.** A diagram URL carries node/edge labels
  to the x-cmd.com renderer so it can draw the image; treat those labels like any
  outbound URL (they may appear in server access logs). Percent-encoding is not
  encryption — don't put secrets, credentials, or sensitive internal names in labels.
- **No uploads, no installs.** Default mode writes zero local files. The export
  scripts only download the rendered file with `curl`, with optional fallbacks to
  CLIs already installed on your machine — nothing is ever fetched from a package
  registry or executed beyond that. Note the export download itself contacts the
  renderer (the URL carries the labels) — local files are not the same as offline
  rendering; the latter needs a locally installed draw CLI.
- For confidential codebases, prefer local SVG/PNG export, and think twice before
  embedding diagram URLs in public READMEs (image proxies fetch them automatically).
- Short links are permanent and public: `shorten.sh` uploads the full chart
  definition to x-cmd.com, and anyone holding the `/draw/c/<hash>` link can render
  it. Never shorten diagrams that name confidential systems.
- Renderer allowlist: the export/validate/report scripts fetch only
  `https://x-cmd.com/draw...` and `https://www.x-cmd.com/draw...` URLs; any other
  origin is rejected before a network call is made.
- **Install transparency**: the quick-start command pins the `skills` CLI to
  `1.8.1` (`npx skills@1.8.1 add qiakai/repoviz`) so a compromised future CLI
  release cannot rug-pull the install. Bump the pin deliberately after re-verifying.

## Repository layout

```text
repoviz/
├── SKILL.md               # routing logic, scanning rules, output templates
├── references/            # lazy-loaded per-diagram syntax guides (all URLs live-tested)
│   ├── architecture.md    # archmap / arch2 grammar: n=, e=, b=
│   ├── flowchart.md       # mermaid flowchart, seq, lifecycle
│   ├── sankey.md          # labels=, links=, weights, limits
│   ├── general-charts.md  # mindmap, gantt, auxiliary repo-metric charts
│   ├── repository-ir.md   # evidence discipline, IR schema, 3-layer validation
│   └── architecture-diff.md # impact mode: git diff → delta diagram + +/- summary
├── scripts/
│   ├── export.sh          # URL → local .svg / .png (single or --batch manifest)
│   ├── shorten.sh         # chart JSON → permanent /draw/c/<hash> short link
│   ├── build_html.sh      # URLs + notes + evidence → standalone HTML report
│   ├── inject_readme.sh   # insert/update diagrams between repoviz markers in a README
│   └── validate.sh        # L1 render check (SVG/PNG) + L2 IR structure check
└── README.md
```

## License

MIT — embed the diagrams anywhere.
