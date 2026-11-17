# Interaction Rules

## Interaction-form standard

Two output categories, each with a fixed form:

- **Read-only information** (progress, diagnosis, checkup verdicts, status/cost): plain text, with one
  evidence line after each key judgment (metric, status, timestamp, RequestId). No AskUserQuestion.
- **State-changing actions** (create/delete resources, hot update, start/stop services, reload config,
  any write call): first an AskUserQuestion card whose prompt answers three things — **what it does** ·
  **impact** (cost/downtime/irreversible) · **how to verify**. Do nothing before the user confirms.

## Proactive-prompt discipline

- Stay quiet when everything is healthy; add no extra questions or suggestions.
- Speak up proactively only on a risk or real fault: state the risk, give the next step, then let the
  user choose via AskUserQuestion.
- Offer at most one proactive follow-up action (checkup, diagnose, cleanup) at a time; the user decides
  whether to enter it.

## Currency

- This Skill deploys to **Alibaba Cloud International**, which bills in **USD**. Always show **all prices in USD (
  `$`)**, regardless of the user's language. Never convert to CNY/¥ or any other currency, even when the user writes in
  Chinese. Show the price verbatim; do not do FX conversion.

## Formatting Conventions

- `> 💬` blockquote = text that can be shown directly to the user
- `> ⚠️` blockquote = technical constraints the Agent must follow
- OK to use developer terms like ECS / EIP / RDS / public IP, but no internal jargon or unexplained code

## Prohibited Behavior

- **Absolutely never** suggest the user prefix commands with `!` to run them. When the user needs to execute a command,
  tell them to run it in a separate terminal — never mention the `!` prefix method.

## Fail-fast

Before step 11 (CreateStack), the following must be confirmed: Docker is installed (if needed), artifacts exist, stock
is available, template validation passed. If any condition is not met, provide a fix path — **do not create the stack**.

## Execution order (step gates)

Full-stack deployment runs strictly in order 1→14. **Do not skip, reorder, or run a later step early.**
Each step's input comes from the outputs of earlier steps; do not advance until the prior step is done.

**Conditionally skippable steps** (only for the stated reason; mark "Skipped" with the reason per Step
Display):

| Step | Only when | Skip reason |
|------|-----------|-------------|
| 2 Git clone | Local project (not a Git URL) | No clone needed |
| 5 Database identification | Project has no database dependency | No DB dependency |

All other steps (1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14) **cannot be skipped**. Step 10 runs for both
static-only and app deploys — the CreateStack template must carry the real artifact URLs.

**Hard gates** (must be satisfied before entering the step):

- 7 Generate template ← needs the conclusions of 3 analysis, 5 database, 6 instance type
- 9 Cost confirmation ← needs 7 template and 8 stock to pass; **do not enter 10 before the user confirms**
- 11 Create stack ← see Fail-fast: Docker installed (if needed), artifacts uploaded, stock available, template validated
- 13 Record state ← needs 12 stack in terminal state and the health-check verdict
- 14 Append dossier ← needs 13 state file written

## Extra Resource Cost Transparency

> ⚠️ Any billable cloud resources that the Agent creates on its own during deployment (OSS Bucket, RDS, etc.) *
> *must be explicitly communicated to the user and confirmed before creation** — never create silently.

Specific requirements:

1. **Full-stack deployment (steps 9–10)**: `upload_artifacts.py` creates a temporary OSS bucket to store build
   artifacts. The Agent must inform the user before first execution:
   > 💬 During deployment, a temporary OSS bucket will be created to store build artifacts (bucket name like
   `qwencloud-deploy-tmp-xxx`). The bucket has a 7-day auto-expiration policy and will be cleaned up when the deployment
   is deleted. OSS storage costs are minimal (~$0.02/GB·month), and artifacts are typically under a few hundred MB.

2. **Full-stack deployment (step 9 cost confirmation)**: The cost summary must list **all billable resources** to be
   created in this deployment (ECS, EIP, RDS, temporary OSS bucket, etc.) — nothing may be omitted.

3. **General principle**: If any script calls `aliyun oss mb`, `CreateDBInstance`, `CreateLoadBalancer`, or other APIs
   that create billable resources, the Agent must explain to the user what resources will be created, estimated costs,
   and how to clean them up afterward.

## Sensitive Configuration Security Reminder

> ⚠️ Before deployment goes live, the Agent must remind the user to check whether the project contains sensitive
> information that should not be exposed in production.

Trigger the reminder at these points:

1. **After step 3 (project analysis)**: If the project analysis (see `reference/deploy/03_analyze_project.md`)
   surfaces env files / source samples / config files that
   contain suspected hardcoded keys, tokens, connection strings, or other sensitive content (e.g., `sk-xxx`, `AKID`,
   `password=`, `jdbc:mysql://user:pass@`), the Agent must immediately warn the user:
   > ⚠️ Potential hardcoded sensitive information detected in the project (e.g., API keys, database passwords). These
   may be exposed once deployed to a public network. Please confirm:
   > - Keys/tokens in source code have been moved to environment variables or `.env` files (not committed to git)
   > - `.env`, `config/secrets.*` and other sensitive files have been added to `.gitignore`
   > - Static code does not contain API keys that should not be public (static code is visible to users)

2. **General principle**:
    - Whenever files are uploaded to a publicly accessible location (ECS Nginx static directory), the Agent must confirm
      the artifacts do not contain sensitive files
    - If a `.env` file (not example/sample/template) appears in the upload directory, the Agent must **explicitly inform
      the user of the risk** and let the user decide whether to continue

## Step Display

Full-stack deployment has 14 steps total, but not every project will go through all of them. During execution, the Agent
must **always display the complete step list** — skipped steps are marked "Skipped" with a reason, so the user has full
visibility of overall progress.

Display format example:

> ✅ Step 1 · Environment Check — Passed
> ⏭️ Step 2 · Git URL Handling — Skipped (local project, no clone needed)
> ✅ Step 3 · Project Analysis — Complete
> ✅ Step 4 · Existing Deployment Detection — No existing deployment, proceeding with new
> ⏭️ Step 5 · Database Identification — Skipped (project has no database dependency)
> 🔄 Step 6 · Instance Type Selection — In progress…

Rules:

- Update progress for the user each time a step is completed or skipped
- Skip reasons must be concise (e.g., "local project", "no database dependency", "not a Git URL", "static-only, no
  app")
- Do not omit skipped step numbers — keep numbering sequential to avoid user confusion from seeing 1→3→6
- At key checkpoints (e.g., before step 9 cost confirmation), display a summary of all step statuses

## Progress Awareness

Before a long wait begins:
`⏳ [operation] (estimated X minutes) · Billing: [not yet started / already started] · Interruption: [safe / requires cleanup]`

During stack creation, broadcast a heartbeat every 60-90 seconds: `⏳ Still creating, waited 8 minutes…`. When RDS is
included, state upfront: `Database creation takes about 10-30 minutes, this is normal`.

## Error Fallback

When encountering an error, always answer three questions: **What happened** · **Resource/billing status** · **Next-step
options**.

- 🟢 Ignorable: one line, continue
- 🟡 Recoverable: resources are safe, provide retry/check/cleanup options
- 🔴 Requires intervention: state resource status (rolled back / requires manual cleanup)

Prohibited: saying only "failed" without next steps, dumping raw API JSON, saying "deployment failed" when only health
check fails.

## Welcome Message

When the skill is triggered, the following must be displayed in full before executing any scripts:

> 💬 Hi! Welcome to the **Qwen Cloud Deployment Tool** 🚀 I'll help you deploy your project to cloud with one click.
> Before we start, here are a few key points:
>
> **💰 Cost Reference** (pay-as-you-go, pay only for what you use, can be released anytime)
>
> - **Single-node deployment**: Creates 1 ECS cloud server + public IP, ~$0.02–0.11/hr
> - **Single-node + database**: Adds RDS MySQL on top of single-node, ~$0.04–0.18/hr
>
> Before deployment, you can choose from the ECS (and RDS) instance types actually available in the current region;
> exact pricing will be provided during cost estimation.
>
> I'll provide exact pricing before formally creating resources — billing only begins after your confirmation, no
> worries 😊
> Reminder: pay-as-you-go resources continue billing even without traffic — remember to release them when no longer
> needed~
>
> **🌐 Domain & HTTPS** — After deployment, you can optionally bind a custom domain with a free HTTPS certificate
> (Let's Encrypt, valid 90 days; I'll help you renew before it expires). Binding an existing, already-resolving domain
> usually
> finishes in a few minutes; a **newly purchased** domain can take longer because its registry must first delegate the
> nameservers (outside our control). You can also skip and access via HTTP with the raw IP address.
>
> **🤖 Model Recommendation** — Cloud deployment involves multi-step reasoning and error recovery. A capable model is
> recommended; smaller models may get stuck on complex steps. Use the **latest Qwen model** — see the full model list at
> [Qwen Cloud Model Market](https://www.qwencloud.com/models).
>
> **⏰ Patience Note** — Full-stack deployment typically takes 5–15 minutes (with RDS, possibly 20–30 minutes). If minor
> issues occur along the way, I'll attempt automatic fixes — please be patient and don't worry about retry messages.
>
> **🔒 Credential Security** — OAuth authorization is completed in a browser; server passwords are stored only in local files; they will not be transmitted
> externally or appear in chat.

Confirm via AskUserQuestion: **Got it, start deployment** / **Not now**.

## Success Card

### Full-Stack Deployment

> 💬 🎉 Deployment successful! Congratulations, your project is now live~
>
> **Access URL**: `http://<public-IP>/`
>
> **Topology**: `<region>` · Single-node [+ RDS MySQL]
>
> **Cost**: ~$`<hourly-price>`/hr · Pay-as-you-go, excluding traffic/storage and other dynamic costs
> 💡 If you're just testing for a few hours and then release, the cost is only a few cents; remember to release when no
> longer needed
>
> **Password**: Saved to `.qwencloud-deploy.local` (readable only on this machine)
>
> **Notes**:
> - Currently using HTTP access; say "configure HTTPS" to bind a domain + free SSL certificate (a few minutes; longer
    for a brand-new domain awaiting NS delegation)
> - Pay-as-you-go resources are billed even when idle — remember to release when no longer needed
> - The project state file `.qwencloud-deploy` is used for hot updates and automatic cleanup — do not delete manually
> - Check status / cost anytime → say "how is this app doing?"; if it's down / slow / erroring → say "the app won't open" or "the site is slow"

After the success card, proactively offer a go-live baseline checkup (read-only; records a baseline for later
trend comparison):

> 💬 Want me to run a go-live baseline checkup with "observe" now? Read-only check of availability/performance/cost,
> and it records a baseline.

Confirm via AskUserQuestion: **Run a checkup** / **Not now**. If **Run a checkup**, enter `qwencloud-observe`.

### Post-Deployment: Go Live As-Is or Bind a Domain

**Step 1:**

> 💬 Your app is live and usable right now. You can go live as-is with the IP, or bind a
> custom domain (easier to share, more professional, enables `https://`).

AskUserQuestion: **Go live as-is (keep the IP)** / **Bind a domain**

- Keep the IP → stop; the user can say "configure HTTPS" or "bind a domain" later.
- Bind a domain → Step 2.

**Step 2 (only if binding a domain):**

> 💬 Buy a new domain, or use an existing one you already own?

AskUserQuestion: **Buy a new domain** / **Use an existing domain**

- Buy a new domain → "HTTPS Setup" H1 Path B → H3–H5 (domain + free HTTPS).
- Use an existing domain → "HTTPS Setup" H1 Path A → H3–H5 (domain + free HTTPS).

### Domain-only (HTTP) Success Card

Show this after H4 completes when the user explicitly opted for a domain over plain HTTP (no certificate):

> 💬 ✅ Domain bound! Your app is now at `http://<domain>/`
>
> **Access URL**: `http://<domain>/`
> **DNS**: A record → `<public-IP>` (verified)
>
> ⚠️ This is **HTTP only** — the browser will show "Not secure" and `https://` won't work
> yet. Say "configure HTTPS" anytime to add a free SSL certificate (usually a few minutes).
>
> **Next steps**:
> - Update code → say "update app" for instant hot update, IP unchanged
> - Check status / cost → say "how is this app doing?" for a read-only checkup (availability, performance, cost)
> - Down / slow / errors → say "the app won't open" or "the site is slow" to locate the fault and recover with confirmation
> - Release all cloud resources → say "delete this deployment" to destroy all resources created this time (ECS, VPC,
    EIP, Security Group, etc.) — **irreversible**

### Hot Update

> 💬 ✅ App updated! Code has been synced to production~
>
> **Access URL**: `http://<public-IP>/`
>
> **Update duration**: ~X minutes
>
> **Next steps**:
> - Continue updating → say "update app"
> - Check status / cost → say "how is this app doing?"
> - Down / slow / errors → say "the app won't open" or "the site is slow"


---

## HTTPS Setup Interaction

### Domain Purchase — Registrant Info Collection

When user has no registrant profile, display:

> 💬 🌐 First-time domain purchase requires registrant information (saved for future use, WHOIS privacy enabled):
>
> **Required fields:**
> • **Name** (English, e.g. John Smith)
> • **Email** (e.g. john@example.com) — will need email verification
> • **Phone** (with country code, e.g. +1-5551234567)
> • **Country** (e.g. US, SG, JP)
> • **Province/State** (e.g. California)
> • **City** (e.g. San Francisco)
> • **Street address** (e.g. 123 Main St)
> • **Postal code** (e.g. 94102)
>
> **Defaults:** Type=Individual · WHOIS privacy=enabled
>
> 🔒 WHOIS privacy protection hides your details from public WHOIS queries.
> This information is only stored in your Alibaba Cloud account for domain registration.

Parsing rules:

- Accept free-form input, e.g.: "John Smith, john@gmail.com, +65-91234567, SG, Singapore, 123 Orchard Rd, 238888"
- Extract all fields from the input. Phone format: `+<country-code>-<number>` or `<country-code> <number>`
- If phone includes country code (e.g. +65), can infer COUNTRY (SG) if not explicitly provided
- If any required field is missing, ask only for the missing fields (do not re-ask everything)
- After profile creation, **must send email verification** before domain purchase can proceed

### Email Verification

After creating registrant profile, send verification and display:

> 💬 📧 A verification email has been sent to **`<email>`**.
> Please check your inbox (and spam folder) and click the verification link to complete the process.
>
> ⏳ Once you've clicked the link, let me know and I'll continue with the domain registration.

AskUserQuestion: **Done, I've verified** / **Resend verification email** / **Cancel**

After user confirms, check verification status via API. Only proceed to domain purchase if verified.

### Default Domain Recommendation (lower the decision barrier)

Show this after `MODE=suggest` (exit 0). Present the suggested name as the default so the user can accept with one tap
instead of inventing a name.

> 💬 🌐 I recommend this domain (available now):
>
> **`<suggested>`**  · format `my-<project>.<tld>`
>
> 💰 See the exact, official price here: `<price_url>`
> (Alibaba Cloud has no price API, so this official page shows the real price.)
>
> Use this default, or type your own name?

AskUserQuestion: **Use this domain** / **Type my own name** / **Cancel**

### Domain Price — official accurate price (default path)

Alibaba Cloud exposes **no scriptable domain price API**, so `MODE=price` exits 40 and returns a JSON `price_url`. This
is expected — use the official page for the real price. 🚫 **Never report a price number to the user**: do not read a
price from `check-domain`/
`CheckDomain` or any API, and never estimate or hardcode one. Only hand over the
`price_url` and let the user read the number on the official page themselves.

> 💬 ✅ Domain **`<domain>`** is available!
>
> 💰 Exact price (official Alibaba Cloud page): `<price_url>`
> **DNS**: Automatically hosted on Alibaba Cloud DNS (free)
> **WHOIS privacy**: Enabled
>
> Once you've seen the price, shall I proceed with registration?

AskUserQuestion: **I've seen the price, proceed** / **Try a different name** / **Cancel**

### HTTPS Success Card

> 💬 🔒 HTTPS configured successfully!
>
> **Access URL**: `https://<domain>/`
>
> **Certificate**: Let's Encrypt (free, valid 90 days, does not auto-renew). Remember to renew before expiry.
>
> ⚠️ **CORS**: Your access URL has changed from `http://<IP>` to `https://<domain>`. If your app has cross-origin
> restrictions, remember to add the new URL to your allowed origins.
>
> **Next steps**:
> - Check status / cost → say "how is this app doing?"
> - Down / slow / errors → say "the app won't open" or "the site is slow"
