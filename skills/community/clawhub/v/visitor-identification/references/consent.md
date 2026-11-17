# Consent and the site wiring

The models collect only what the site's tracker sends, and the tracker loads only after a visitor
accepts. This is the wiring, in the website app (`infra/website-building/apps/website/` when the
site came from `website-building`).

## 1. Copy the site files

From this skill's `site/` folder into the app, keeping the paths:

| From                                | To, in the app                    |
| ----------------------------------- | --------------------------------- |
| `site/lib/snitcher.ts`              | `lib/snitcher.ts`                 |
| `site/lib/visitors.ts`              | `lib/visitors.ts`                 |
| `site/components/visitor-consent.tsx` | `components/visitor-consent.tsx` |
| `site/visitors.json`                | `visitors.json`                   |

`lib/visitors.ts` reads `site` from `lib/site.ts` and the app's `Button`; both come with
`website-building`. In another app, point those two imports at its equivalents.

## 2. Render the gate from the layout

In `app/layout.tsx`:

```tsx
import { VisitorConsent } from "@/components/visitor-consent";
import { visitorTracking } from "@/lib/visitors";

const tracking = visitorTracking();

// inside <body>, after the page content:
{tracking !== null ? <VisitorConsent tracking={tracking} /> : null}
```

`visitorTracking()` runs at build time. It returns `null`, and the export carries no profile ID,
unless the snippet is set **and** `site.json` is `ready` with a `canonicalUrl`.

## 3. Hand the snippet to the app

In the app's `defineApp` (`infra/website-building/apps/website.ts`):

```ts
import { visitingCompanies } from "../../visitor-identification/models/companies";

env: {
  NEXT_PUBLIC_SNITCHER_SNIPPET: visitingCompanies.config._trackingScript,
},
```

The token resolves after the companies model exists, in the same deploy. Only `lib/visitors.ts`
reads it, on the server, and only the profile ID reaches the page.

## 4. Point at the disclosure

Set `visitors.json` `privacyPolicyUrl` to the operator's reviewed page: what is collected (the
visiting company and the pages read), by whom (Snitcher, through Cargo), why, how long it is kept,
and how to reach the company. The build fails while it is empty and tracking is on. Never generate
the legal text.

## What the gate does

- **Before a choice:** a banner with equal "Accept tracking" and "Reject tracking", and a link to
  the disclosure. No request to Snitcher.
- **Accept:** the choice is saved, then the loader queues Snitcher's API and requests its script
  with the reviewed settings (`waitForConsent`, capture features off) and grants consent.
- **Reject, or withdraw later** from "Privacy choices": the choice is saved, Snitcher is told to
  deny, and the page reloads, which removes the tracker's listeners. Other open tabs reload too.
  This stops future collection; it does not erase what Snitcher already holds.
- **Global Privacy Control:** treated as a no. The banner says so and "Accept" is disabled.
- **Any origin but the canonical one** (the Cargo URL, a preview): the gate renders nothing.

Snitcher's own `waitForConsent` setting still records pageviews and sessions before consent
(<https://docs.snitcher.com/product/tracker/cookie-consent>). That is why the gate loads nothing at
all until the visitor accepts, rather than relying on it.

## Checking it

In a private window on the canonical origin, with the network panel filtered to `snitcher`:

1. Load a page: the banner shows, no request.
2. "Reject tracking": no request. Reload: still none, no banner.
3. "Privacy choices", then "Accept tracking": requests to `cdn.snitcher.com` and
   `radar.snitcher.com`.
4. "Privacy choices", then "Reject tracking": the page reloads with no request.
5. Open the Cargo URL: no banner, no request.
