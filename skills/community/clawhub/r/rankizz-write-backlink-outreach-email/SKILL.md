---
name: rankizz-write-backlink-outreach-email
description: Write concise, personalized backlink outreach emails for an editorial replacement, guest contribution, disclosed sponsored post, or narrow reciprocal-link partnership using verified page, product, audience, authority, and traffic evidence. Use when a user needs subject lines, body copy, a low-friction CTA, prospect-specific variants, or a backlink outreach campaign draft with clear do, do not, limitation, disclosure, and search-policy checks. Rankizz metrics are optional.
---

# Write a backlink outreach email

Give the recipient a defensible editorial reason to respond. Do not dress a ranking transaction up as reader value.

Read [references/backlink-outreach-policy.md](references/backlink-outreach-policy.md) before drafting. The three copy-ready templates requested for this workflow are included below so they remain visible on the public skill page.

## Invoke Rankizz MCP tools

When using Rankizz through MCP, the initial tool list is intentionally compact. Call `search_tools` with a capability query or exact domain-tool name and set `includeSchemas: true` unless the arguments are already known. Invoke a discovered tool with `call_read_tool` when its `readOnlyHint` is `true`; use `call_tool` for every other tool. Pass the discovered name as `tool` and its original input object as `arguments`. REST callers continue to use the direct `/api/v1/tools/<tool-name>` endpoint.

## Gather the evidence

Resolve:

- sender name, role, organization, postal/contact footer, and sending domain;
- recipient name or team, public source, role, and site;
- exact target page and the relevant section, item, claim, or missing resource;
- outreach type and the benefit to the recipient's readers;
- app or website name, URL, what it does, target user, differentiator, and limitations;
- the destination page the sender wants linked;
- proof, screenshots, data, free access, or a draft the sender can genuinely provide;
- any budget, currency, deliverables, disclosure expectation, and link qualification;
- verified site metrics the recipient may care about;
- recipient and sender jurisdictions and the user's sending/opt-out process.

Do not draft around facts the user cannot support. Mark missing personalization or evidence as a placeholder for the user instead of inventing it.

## Choose one legitimate proposal

### Editorial update or better listicle fit

Use when the target page contains an outdated product, broken destination, factual error, missing category, or a weaker fit for a specific reader.

- Cite the exact page and issue.
- Explain the proposed replacement or addition in one sentence.
- Supply evidence the editor can check without accepting the pitch.
- Do not call something broken, outdated, or incorrect unless it is.
- Give the editor freedom to keep, replace, add, or ignore the suggestion.

### Guest contribution

Use when the site visibly accepts contributors or the proposed article fills a documented content gap.

- Pitch a useful topic and reader outcome, not a pretext for an exact-match anchor.
- Explain why the sender can write it.
- Offer an outline or draft, and follow the publisher's editorial rules.
- If money changes hands, call it sponsored or paid and accept `rel="sponsored"` or `rel="nofollow"`.

### Paid placement or sponsorship

Use only as a transparent advertising or sponsorship proposal.

- State the user's real budget or ask for the publisher's media kit and rate.
- Do not ask for a paid link that passes ranking credit.
- Require appropriate disclosure and `rel="sponsored"` or `rel="nofollow"`.
- Do not imply that payment buys a positive review, false claim, or editorial endorsement.

### Narrow reciprocal resource partnership

Use only when each link independently helps its own audience.

- Name both relevant pages and why each link belongs.
- Keep editorial control with both site owners.
- Avoid exact-match anchor demands, partner-page farms, and repeated exchanges.
- Do not scale or disguise `link to me and I will link to you` arrangements intended mainly to manipulate rankings.

If the user's requested arrangement conflicts with these conditions, explain the risk and draft a compliant sponsorship or editorial alternative.

## Verify metrics before using them

Metrics support a pitch only when they help the recipient judge fit.

- `DA` means Moz Domain Authority. Do not rename another provider's score as DA.
- `DR` means Ahrefs Domain Rating. Rankizz can retrieve DR with `get_ahrefs_domain_rating` when the user chooses paid enrichment.
- Traffic must include its source, scope, and date or period. Label third-party traffic as an estimate.
- Use `get_domain_overview` or backlink tools when relevant, not merely to decorate the email.
- Treat `site link` as the proposed destination-page URL unless the user explicitly means Google sitelinks.

Rankizz is optional. Before any paid MCP or API call, confirm the account has at least 10 credits. Record the operation and exact credits charged. Use user-supplied or public evidence when a paid call would not improve the pitch.

Never inflate, round up deceptively, mix dates, or compare DA and DR as if they were the same scale. Omit a metric when it does not strengthen the recipient's decision.

## Write the email

### Subject

Use a short, accurate subject tied to the page or proposal. Usually two to eight words is enough.

Good:

- `Small update for your invoicing list`
- `Guest idea for [Site]`
- `Sponsorship rates for [Page]`
- `Resource fit for [Topic]`

Bad:

- `URGENT: Huge SEO opportunity!!!`
- `Quick question` when the email contains a sales pitch
- `Broken link on your site` when no link is broken
- `Guaranteed traffic partnership`

### Body

Keep a first email compact, usually around 70 to 140 words when the evidence fits. Use plain text and short paragraphs.

1. Address the recipient naturally.
2. Name the exact page and observation.
3. Explain the reader or editorial value.
4. Introduce the app, site, or asset with one verified sentence.
5. State the proposal and any required commercial terms plainly.
6. Ask one low-effort question.
7. Sign with a real identity and the compliance footer the sender needs.

Do not lead with the sender's DR, traffic, or product biography. For reciprocal partnerships, a brief verified metric can help after relevance is clear. For listicle corrections, the page evidence matters more than the sender's authority score.

Good body:

> Hi Mina,
>
> Your remote invoicing guide still lists LedgerFox as desktop-only, but its March release added a web app. The comparison table may be sending browser-first teams to the wrong option.
>
> I work on BillNest, a browser-based invoicing tool for small agencies. It could fit the same section because it supports client approvals and recurring invoices. I can send a two-sentence entry, current pricing, and screenshots so you can judge it against the other tools.
>
> Would that be useful for your next update?

Bad body:

> I love your amazing blog! We are the leading revolutionary platform in the industry with impressive DA and traffic. Please add our dofollow link with the anchor "best invoicing software". We can pay immediately.

The bad version uses fake praise, unsupported claims, an optimized anchor demand, and a paid ranking link.

### CTA

Ask for one small decision.

Good:

- `Would a two-sentence replacement and screenshot help?`
- `Is this topic suitable for your contributor calendar?`
- `Could you send your sponsorship rates and link-disclosure terms?`
- `Does the resource fit that section, or should I leave it there?`

Bad:

- `Can we schedule a 30-minute call tomorrow?`
- `Please add the link and confirm when it is live.`
- `Thoughts?`
- `Reply ASAP to secure this opportunity.`

## Copy-ready templates

Replace every bracketed field with verified information for one prospect. Delete any sentence that does not apply. Do not send these as mail-merge copy.

### Template 1: outdated listicle or better replacement

Use this when an existing entry is outdated, incorrect, broken, or a poor fit for a specific reader. If the current item is still valid, pitch the app as an additional option rather than pretending it needs replacement.

Subject options:

```text
Update for your [topic] list
[Page title]: [specific correction]
Another option for [reader type]
```

Full email:

```text
Hi [name],

I was checking your [page title] and noticed [exact outdated, incorrect, broken, or missing point] in the section about [item or category]. [Brief source or checked fact] shows [specific correction].

I [built/work on] [app] ([destination URL]), which helps [specific user] [verified function]. It may be a better fit for [exact reader or use case] because [one defensible difference]. I can send a two-sentence entry, current pricing, and [screenshot/data/source] so you can compare it with the existing options.

Would that material help with your next update?

[real name]
[role and company]
[required postal address, privacy notice, and opt-out]
```

CTA:

```text
Would that material help with your next update?
```

### Template 2: paid guest post or sponsorship

Use this only for a disclosed paid contribution. The user must supply the real budget or ask for the publisher's rates. Accept `rel="sponsored"` or `rel="nofollow"`; payment must not buy a followed link, false claim, or positive review.

Subject options:

```text
Sponsored article for [topic]
Sponsorship rates for [page or section]
Paid contribution for [audience]
```

Full email:

```text
Hi [name],

I saw that [site] [accepts sponsored contributions/covers specific topic]. I am looking at a disclosed paid article about [specific reader problem or proposed title] for [audience].

I [built/work on] [app], which [verified function] for [specific user]. We can provide [original draft/data/screenshots/product access], and the article would cover [two or three concrete sections] under your editorial review.

Our budget is [amount and currency/range]. We are comfortable with clear sponsorship disclosure and rel="sponsored" or rel="nofollow".

Could you send your rates, editorial requirements, and available placement options?

[real name]
[role and company]
[required postal address, privacy notice, and opt-out]
```

CTA:

```text
Could you send your rates, editorial requirements, and available placement options?
```

### Template 3: relevant backlink exchange

Use this only when each link independently improves its own page. Do not use it for scaled reciprocal-link campaigns, exact-match anchor trades, or partner pages created only for cross-linking.

Subject options:

```text
Resource fit for [shared topic]
Two useful resources for [audience]
[Target page] resource suggestion
```

Full email:

```text
Hi [name],

Your [target page URL or title] explains [specific point]. I [built/work on] [app] ([app URL]), which helps [specific audience] [verified function]. Our [resource page URL] adds [specific evidence, tool, example, or workflow] that could help readers in the section about [exact location].

We also maintain [sender page URL], where your [recipient resource URL] would help our readers with [distinct need]. [Optional: Our site has Moz DA [number] or Ahrefs DR [number], plus [traffic estimate and source], checked [date].]

Would you be open to reviewing both resources independently? Either editor should skip a link that does not fit the page.

[real name]
[role and company]
[required postal address, privacy notice, and opt-out]
```

CTA:

```text
Would you be open to reviewing both resources independently?
```

## Personalize without pretending

- Refer to one exact page detail the sender actually checked.
- Explain the match in the recipient's terms.
- Use the sender's real voice and expertise.
- Keep honest uncertainty when fit depends on the editor.
- Remove corporate filler, exaggerated praise, fake familiarity, and AI-sounding cadence.
- Remove em dashes and en dashes from the final draft.
- Never invent a prior relationship, shared audience, customer result, or article readership.

## Compliance and sending boundary

This skill drafts copy. It does not send messages, enroll contacts in a sequence, or determine that outreach is lawful.

- Use accurate From and Reply-To information and a truthful subject.
- Identify the sender and commercial relationship.
- Include the postal address, advertising notice, privacy information, and opt-out mechanism required for the actual jurisdictions and sending method.
- Honor prior objections and suppression lists before preparing a send batch.
- Do not email addresses collected for privacy, abuse, security, legal, billing, or support purposes unless the message belongs there.
- Default to one personalized email and at most one polite follow-up after five to seven business days. Stop after a rejection, opt-out, or no response to the follow-up.

## Do

- Make the page-specific reason visible in the first two sentences.
- Offer evidence or work that reduces the editor's effort.
- Keep budget, sponsorship, and relationship terms explicit.
- Let the recipient choose wording, placement, anchor text, and whether to link.
- Accept qualified links for paid arrangements.
- Check every metric and product statement.
- Write one prospect at a time, even when using a shared structure.

## Do not

- Offer money for an undisclosed link that passes ranking credit.
- arrange excessive reciprocal links for ranking manipulation.
- ask for exact-match anchor text as a condition.
- claim the recipient's page is wrong without evidence.
- copy a generic compliment from the homepage.
- attach files or add multiple links in the first email without a reason.
- hide the app's ownership or the sender's commercial interest.
- promise rankings, traffic, conversions, or a positive review.
- automate sending or evade unsubscribe and platform controls.

## Output format

For one prospect, return:

```markdown
# Backlink outreach draft

## Proposal check
- Type:
- Target page and exact opportunity:
- Recipient and contact source:
- Reader benefit:
- Commercial terms and link qualification:
- Verified claims and metrics:
- Missing evidence:

## Subject options
1. ...
2. ...
3. ...

## Email
[Plain-text draft]

## Optional follow-up
[One shorter follow-up, or `Not requested`]

## Before sending
- [ ] Reopen the page and confirm the observation
- [ ] Confirm the contact is role-relevant and not suppressed
- [ ] Verify every product and metric claim
- [ ] Check paid or reciprocal link policy risk
- [ ] Add required identity, address, privacy, and opt-out details
- [ ] Send and follow up manually
```

For several prospects, create `backlink-outreach-drafts-YYYY-MM-DD.md` when the user requests a file or when the drafts would be unwieldy in the terminal. Do not overwrite an existing report. Give each prospect its own evidence block and draft; do not produce one mail-merge paragraph with token substitutions.

## Limitations

- A strong email cannot make an irrelevant or policy-conflicting link appropriate.
- DA, DR, and traffic estimates do not prove editorial quality or predict a response.
- Search engines may ignore links or act against manipulative link schemes.
- The recipient controls placement, wording, link attributes, and editorial judgment.
- Laws and provider rules vary by jurisdiction and can change.
- Deliverability depends on sender reputation, authentication, list hygiene, recipient interest, and sending behavior outside this skill.
