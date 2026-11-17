---
name: visitor-identification
description: 'Identify which companies visit your website and what they read: Snitcher identifies the organisation behind each visit, two Cargo models keep the visiting companies and their sessions current, and the site loads the tracker only after a visitor accepts it. Triggers: "who is visiting our website", "identify website visitors", "which companies visit our site", "track website sessions by company", "add visitor identification to our website", "website visitor intelligence", "Snitcher on our site", "which accounts read our pricing page". Cargo project, defineModel, model.config, Snitcher, consent. Skip when: you want to identify named people, which this does not do; you want buying signals from the wider market, which is monitor-buying-signals; or there is no site to add it to yet, which is website-building.'
version: "0.1.2"
compatibility: "Requires @cargo-ai/cli with @cargo-ai/cdk 1.0.98 or later (`model.config.<key>` tokens and token-valued app env), a website on Cargo Hosting (website-building), Node.js 22.18 or later, and a Cargo workspace."
homepage: https://github.com/getcargohq/gtm-skills/tree/main/visitor-identification
metadata:
  author: getcargo
  source: cookbook
  personas:
    - marketing
    - sales-development
    - gtm-engineering
  openclaw:
    requires:
      bins:
        - cargo-ai
    install:
      - kind: node
        package: "@cargo-ai/cli@latest"
        bins:
          - cargo-ai
    homepage: https://github.com/getcargohq/gtm-skills
---

# Visitor identification

## The outcome

Every company whose people read your website lands in a Cargo model, with the pages they read and
where they came from, and stays current without anyone running anything. It is company-level: an
IP address resolved to an organisation, never a named person, and nothing is sent to anyone.

Three pieces make it:

1. **A companies model.** `fetchOrganisations` on Snitcher, through Cargo's credits. Creating it
   provisions a Snitcher workspace for the site and writes the tracker's snippet and workspace into
   the model's config.
2. **A sessions model.** `fetchSessions` reads the workspace the companies model provisioned,
   `visitingCompanies.config._workspaceUuid`, in the same deploy.
3. **A consent gate on the site.** The website app receives the snippet as an env token,
   `visitingCompanies.config._trackingScript`, keeps only its public profile ID, and loads
   Snitcher with its own reviewed settings once a visitor accepts. Before that, nothing loads.

**Two things worth knowing before you start.** Each identified company is billed when it first
lands, so spend follows traffic, not a cap. And Snitcher's own `waitForConsent` still tracks
pageviews before consent, which is why the gate loads nothing at all until the visitor says yes.

## Example

> Show us which companies visit www.fabrikam.example, and only track visitors who accept.

Illustrative output, fictional records:

```text
model:website_visiting_companies     deployed   12 companies after the first day
  northwind.example     Software     first seen 09:14   last seen 16:02
  contoso.example       Logistics    first seen 11:40   last seen 11:52
model:website_visitor_sessions       deployed   31 sessions
  northwind.example     /pricing/ /about/      referrer: linkedin.com
app:website                          updated    consent gate on, tracker after accept only
```

Rows land on Cargo's own sync interval. A day with no identified company is an honest zero: not
every IP resolves to an organisation.

## Put it in your project

This folder is a **worked example**: real project resources written for some other company. The job is
to end up with the code your company would have written, in your project, and an agent does the
adapting. If the `cargo-project` skill is in your session it carries the long form of this; if
not, this is enough.

1. **Install it: the CLI does the copy.** From inside the project (the folder holding `cargo.json`),
   `cargo-ai project add cookbook/visitor-identification` writes the models to
   `infra/visitor-identification/` and this procedure, with the `site/` files, to
   `.claude/skills/visitor-identification/`. No project yet?
   `cargo-ai project init <dir> --cookbook visitor-identification && cd <dir> && npm install`.
   **If you are reading this from the project's `.claude/skills/`, the install already happened;
   start at step 2.**
2. **Reconcile it with what is already declared.** The website must already be declared, usually
   by `website-building`; this skill adds to it, it does not create one. A Snitcher connector or
   visitor model the project already has is rewired to, not duplicated.
3. **Wire the site.** Follow [consent](references/consent.md): copy `site/` into the website app,
   render the gate from its layout, add the env token to its `defineApp`, and set the privacy URL.
4. **Adapt.** Work the sections below in order: _What should not change_ is what you argue back
   about (say what breaks, then do it if they still want it); _What you can change_ is what you
   offer unprompted; _What you will be asked_ is the floor, and you derive before you ask. Record
   what you changed and why under a `## Decisions` section in your copy of this file.
5. **Plan, then stop.** `node --import tsx evals/contract.mjs` from this skill's folder, then
   `npm run check && cargo-ai project plan` from the project root, show the diff, and deploy only on
   an explicit yes: `cargo-ai project deploy`. If the project deploys from CI, the merged pull request
   is the deploy; do not also deploy from a laptop.
6. **Verify.** Walk _Done when_ line by line in a real browser, and report each with evidence.
   Read [data](references/data.md) for what the rows mean before reporting a count.

## What you will be asked

**Derive before you ask.** An input with a lookup is looked up, not asked.

| Input                                                    | Kind    | How it is answered                                                                                         | Why it matters                                                                                                          |
| -------------------------------------------------------- | ------- | ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| site URL (`infra/models/companies.ts`)                   | derived | the website app's `site.json` `canonicalUrl`, which must be HTTPS and the site `ready`                     | Snitcher provisions a workspace for this exact origin, and the gate only runs on it. Changing it later starts over.    |
| Snitcher connection (`infra/connectors/snitcher.ts`)     | derived | `cargo-ai connection connector list`: the workspace's default Snitcher connection, on Cargo's credits      | The managed path provisions the tracker. A workspace's own Snitcher key provisions nothing and needs a different setup. |
| acceptable spend                                         | asked   | the live price per identified company from the integration, quoted with the current credit balance         | Usage grows with traffic and nothing caps it. The operator agrees to that before the first deploy.                      |
| privacy disclosure (`visitors.json` `privacyPolicyUrl`)  | asked   | the operator's reviewed page describing Snitcher, the purpose, retention and contact                       | The banner links to it. This skill never writes legal text.                                                             |

Checked before moving on, not after the deploy:

- the site is `ready` with an HTTPS `canonicalUrl`, and the companies model's `url` is that origin
- the spend was quoted from the live price and the operator agreed to it
- `visitors.json` `privacyPolicyUrl` points at a reviewed disclosure
- `node --import tsx evals/contract.mjs` passes against the adapted graph

## What you can change

The code is a worked example. These reshapes are expected, and the agent offers them rather than
waiting to be asked. Every one costs something.

| Variation         | When it is right                                          | How                                                                                                                   | What it costs                                                                                         |
| ----------------- | --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `existing-cmp`    | The site already runs a consent management platform       | Call `loadSnitcher` from the CMP's grant event and its deny path from revocation, instead of rendering the gate      | The same behaviour has to be re-tested against the CMP's events, including withdrawal.                |
| `scoring-input`   | Visits should move an account's score                     | Read the companies model from `account-scoring` and weight recency and pages read                                     | A score that leans on visits favours companies with more staff online, not more intent.               |
| `alert-on-visit`  | Sales wants to know when a target account is on the site  | A segment over the companies model joined to the target list, with an alert on new rows                               | Alerts on company-level data invite reps to guess who visited; the alert has to say it is a company. |
| `own-snitcher`    | The company already pays for Snitcher                     | Use its connector, select the existing workspace in the companies model, and pass that workspace to sessions          | No managed provisioning: the snippet and workspace come from the existing account, outside this graph. |

## What should not change

However far you adapt, these hold. Ask for one anyway and the agent tells you what breaks, then does
it if you still want it, and records why under `## Decisions` in your copy of this file.

- **Nothing loads before an explicit accept.** (`site/components/visitor-consent.tsx`) Snitcher's
  `waitForConsent` still records pageviews before consent; only not requesting the script keeps a
  visit untracked. Global Privacy Control counts as a no.
- **The site loads its own reviewed loader, never the provider's snippet.** (`site/lib/snitcher.ts`)
  Only the public profile ID is taken from it, and an unrecognised snippet fails the build. Form,
  click, download, error and recording capture stay off.
- **Tracking runs only on the canonical origin of a `ready` site.** (`site/lib/visitors.ts`) The
  Cargo URL, previews and a draft site load nothing.
- **Company-level only.** No identify call, no email capture, no named person inferred from a visit.
- **The companies model's `url` stays stable.** A new URL provisions a new Snitcher workspace: a new
  tracker, an empty history.
- **No credentials, deploy commands, or customer data in this repository.**

## Done when

- `node --import tsx evals/contract.mjs` passes: the companies model is `fetchOrganisations` on the
  Snitcher connector with an HTTPS `url`, the sessions model is `fetchSessions` reading
  `config._workspaceUuid` from it, both are filed in `visitor_identification_models`
- the plan's first deploy shows the two models and the app update, and the operator approved the
  spend against the live price
- in a browser on the canonical origin: no request to `snitcher.com` before a choice, after
  "Reject tracking", or after withdrawing and reloading; one "Accept tracking" makes a request to
  `cdn.snitcher.com` and `radar.snitcher.com`
- the Cargo URL and a draft preview make no request to `snitcher.com` and show no banner
- after the sync interval the models hold rows, or a zero reported as a zero
- the banner links to the reviewed privacy disclosure

## What it costs

Each company Snitcher identifies is billed once, when it first lands in the companies model;
sessions add nothing. Read the live price from the integration (`cargo-ai connection integration
get snitcher`) and the workspace's credit balance before the first deploy, and quote both. Spend
follows the site's traffic and there is no built-in cap, so say that too. Removing the companies
model stops the billing.

## Composes into

`website-building` (the site this adds to), `account-scoring` (visits as a recency signal on the
accounts it scores), `tam-building` (which visiting companies are in the market you chose), and
`agentic-engagement` (a reason to reach out, said as a company, never as a person).
