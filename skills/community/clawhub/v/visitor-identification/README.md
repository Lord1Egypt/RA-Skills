# Visitor identification: identify which companies visit your website

To see which companies visit your website and what they read, identify the organisation behind each
visit with Snitcher and keep the results in two Cargo models, `website_visiting_companies` and
`website_visitor_sessions`. The site loads the tracker only after a visitor accepts it, and it
identifies companies, never named people.

```sh
cargo-ai project add cookbook/visitor-identification
```

```text
visitor accepts on the site
  -> the site's own Snitcher loader (profile ID only)
  -> Snitcher identifies the company from the visit
  -> website_visiting_companies + website_visitor_sessions   (Cargo, on its sync interval)
```

## Why it is built this way

**One deploy, no capture step.** Snitcher's tracker and workspace only exist once the companies
model is created. `visitingCompanies.config._trackingScript` and `._workspaceUuid` are project tokens,
so the sessions model and the site's env read them in the same deploy that creates them.

**The site owns its loader.** The provider's snippet is a script; the site takes only its public
profile ID from it, rejects any other shape at build time, and loads Snitcher with settings this
repository reviews: consent required, form, click, download, error and recording capture off.

**Nothing before consent.** Snitcher's own `waitForConsent` still records pageviews and sessions
before consent, so the gate does not request the tracker at all until the visitor accepts.

**Company-level by design.** An IP address resolved to an organisation. No identify call, no
person, no outreach in this skill.

## Placeholders (edit before deploy)

1. **Site URL**: `infra/models/companies.ts` `url`, the site's `canonicalUrl`.
2. **Privacy disclosure**: `site/visitors.json` `privacyPolicyUrl`, once copied into the app.

## Files

| Path                                  | What it is                                              |
| ------------------------------------- | ------------------------------------------------------- |
| `infra/connectors/snitcher.ts`        | Snitcher on Cargo's credits                             |
| `infra/models/companies.ts`           | `fetchOrganisations`: the companies, and the tracker    |
| `infra/models/sessions.ts`            | `fetchSessions`, on the provisioned workspace           |
| `site/lib/snitcher.ts`                | Snippet to reviewed settings; anything else fails       |
| `site/lib/visitors.ts`                | Build-time switch: settings, or no gate at all          |
| `site/components/visitor-consent.tsx` | The consent gate and the loader                         |
| `references/consent.md`               | Wiring the site, and checking the gate in a browser     |
| `references/data.md`                  | What the rows mean, querying, stopping                  |
| `evals/contract.mjs`                  | Graph and parser contract                               |

## Verify

```sh
node --import tsx visitor-identification/evals/contract.mjs
```
