# Acquisition

## Purpose and operating boundary

Build a repeatable acquisition workflow around a useful, verifiable piece of content. This module covers an agent-led article pipeline, newsletter production, network-specific social posts and a product affiliate program in Whop.

The editorial procedures are adapted from operating workflows, with private details removed. They are recommendations, not a claim that Whop natively runs an article factory, newsletter service or social scheduler. Use the publishing systems you actually control. Connect content to a verified Whop offer only where that offer helps the reader.

All examples are generic. Whop documentation was checked on 29 September 2026. Do not carry historical rates, audience sizes, visual specifications or client-specific schedules into a new business.

Default to local drafts and read-only research. Remote draft creation, media uploads, publication, scheduling, affiliate changes, invitations and transaction tests require approval for the exact target and action. Keep credentials and account references in the operator's protected environment, never in prompts, public content or a shared acquisition pack.

## 1. Choose one useful content-to-product journey

Start with a question your intended buyer actually needs answered. Define the next action before assigning agents.

```text
Audience:
Question or decision:
Evidence that the question matters:
Current page already answering it, if any:
Article's useful outcome:
Relevant offer and verified destination:
Reason the offer is relevant:
What the article must not promise:
Primary reader action:
Editorial owner / reviewer / publisher:
Language and audience location:
Measurement period and data sources:
Publication and sending permissions:
```

A course creator might explain how to check access to a paid worksheet, then offer the worksheet where it is relevant. A coaching business might publish a preparation guide leading to an already-approved service page. These are hypothetical content routes, not case studies or evidence of sales.

If the product, checkout or delivery route is not ready, keep the commercial CTA in draft. A genuinely free interest form is an option only after its scope and no-charge behavior have been approved and verified. A Whop checkout waitlist can collect card details and charge on approval; it must not be presented as an ordinary newsletter signup. [W7]

## 2. Build the article pipeline

### Roles and handoffs

The workflow uses a topic researcher, an editor, a writer, a visual producer, an independent verifier and a publisher. One operator may hold several roles, but the independent verifier must have the sources and must be able to refuse release.

| Stage | Owner | Required output | Gate for the next stage |
| --- | --- | --- | --- |
| Topic selection | Researcher and editor | Search-intent notes, duplicate check and approved brief | A distinct reader need, sufficient sources and an explicit offer boundary |
| Writing | Writer | Article, claim ledger, metadata and internal-link instructions | Every material claim has evidence or is marked unresolved |
| Visual production | Visual producer | Final images, captions, accessibility text and asset manifest | Images explain the approved content and contain no new unsupported claims |
| Verification | Independent verifier | PASS or FAIL with exact corrections and source references | Text, calculations, images and metadata agree; no unresolved material error |
| Publication | Publisher | Approved version deployed to the exact authorized target | PASS is current, publication is authorized and no competing write is in progress |
| Proof of publication | Publisher, checked against public evidence | Exact live URL, served-content checks and discovery state | The expected article and assets are actually served; unknowns remain visible |

Check risky claims before spending time on visuals. The final independent review must still inspect the completed text and final images together. Writing approval does not automatically approve a later infographic.

### Durable records and state

Use a private workspace per article and one coordinator-owned topic bank. Agents can propose new topics; only the coordinator reserves, replaces or releases them. Store each handoff before marking its stage complete.

Keep these records:

- Topic decision and search-intent evidence.
- Brief and approved offer facts.
- Article, metadata and claim ledger.
- Incoming-link instructions for existing pages.
- Final assets and their manifest.
- Current verdict and previous verdicts.
- Publication receipt and later discovery measurements.

Suggested article states:

```text
available -> reserved -> brief-approved -> drafted -> assets-ready
-> review-passed -> publish-approved -> published-unverified -> verified-live

Exception states:
needs-correction / waiting-for-source / waiting-for-approval
access-paused / quota-paused / publication-unknown / withdrawn
```

A task marked complete only closes its own stage. It does not establish publication. Search-engine indexing and commercial performance are separate measurements after `verified-live`.

Before starting a chain, confirm that every assigned agent or worker actually exists and that dependencies are enforced by the task system. Give every worker the brief, required inputs, owned files, exact output contract and stop conditions. Do not depend on another worker's chat history.

### Topic-bank template

```text
Query:
Audience / language / location:
Search intent:
Evidence source and checked date:
Measured demand and source, or not measured:
Existing page covering this intent:
Proposed angle and reader outcome:
Relevant offer:
Priority and reason:
Status:
Current reservation and owner:
Final slug:
Verified public URL, if published:
Previous failure or correction:
```

Deduplicate both query wording and intent. Changing a title does not make a topic new. Check commercial pages, older articles and drafts as well as the topic bank. An existing service page can already own the query you were about to target.

## 3. Select the topic and write the brief

1. Read the current public article inventory, relevant service pages and topic bank. Check the sitemap where the site exposes one.
2. Inspect the search results for the actual audience language and location. Record whether people appear to need a definition, a comparison, a procedure or a service.
3. Read the leading relevant pages. Note the questions they answer, evidence they use and useful omissions. A competitor's claim is a research lead, not a verified fact.
4. If keyword data is available within the approved research budget, record its source, location, date and unit. Otherwise write “not measured.” Do not invent volume, difficulty or cost-per-click data.
5. Decide whether to update an existing page or create a distinct article. Document any topic replacement so the coordinator can move the reservation safely.
6. Approve the primary question, angle, source set, section plan and relevant CTA. Reserve a unique slug in the actual publishing system before publication, without creating a remote object unless authorized.
7. Plan both outgoing links from the new article and incoming links from relevant existing pages. For each incoming link, specify the actual source page, insertion location and a factual bridging sentence.

Do not select a high-volume navigational query merely because its count is attractive. A reader looking for an official login or register may have no need for the offer. Conversely, missing keyword data does not prove that a useful customer question has no demand.

### Brief template

```text
Working title:
Primary question and intent:
Secondary questions:
Audience, language and location:
Distinct angle compared with existing pages:
Direct answer the opening must provide:
Section outline:
Required primary sources and their dates:
Claims needing specialist review:
Approved offer facts and excluded promises:
Visible length budget and reason:
Outgoing internal links:
Incoming links: source page / insertion point / proposed sentence
Useful visual mechanisms:
CTA and verified destination:
Known gaps:
Acceptance criteria:
```

Title lengths, article lengths and image budgets must fit the actual publishing template. Check whether the template adds a title suffix, creates its own heading or supplies the author signature. Do not import a fixed character budget from an unrelated site.

## 4. Draft from evidence

Give the writer this instruction with the brief and source material:

```text
Write the article defined in the approved brief. Answer the reader's question
in the opening. Preserve the approved offer, scope and uncertainty.

Use only supported facts. For each material factual or numerical claim,
record its source, location in the source and any limitation. Label unresolved
claims in the working draft; do not hide them in polished copy.

Do not invent customer stories, first-person experience, testimonials,
credentials, outcomes, prices or policies. Keep hypothetical examples visibly
hypothetical. Keep legal, medical and financial qualifications intact.

Deliver the article, metadata, claim ledger and exact incoming-link changes.
Do not publish, schedule or alter commerce settings.
```

The claim ledger should be small enough for a reviewer to use:

| Claim | Source and date | What the source supports | Limitation | Decision |
| --- | --- | --- | --- | --- |
| Exact sentence or numerical statement | Primary-source URL and relevant section | Scope, population, account behavior or rule | What cannot be inferred | Retain, qualify, remove or escalate |

Calculate rather than guess. Distinguish a percentage from percentage points, a relative change from an absolute one, and a gross amount from net proceeds. Preserve currencies and measurement periods. Verify publication titles and citation metadata instead of filling missing bibliographic fields from memory.

Check short callouts, captions, tables, headlines and structured answers against the main article. They often survive a body-text correction and keep the original error. When a source changes, update every place that repeats the claim.

The metadata handoff must include the final heading, browser title as actually rendered, description, slug, sharing title and image, canonical destination, indexing intent and any structured answers. Structured answers must match visible content. Never add ratings, qualifications or reviews merely to fill a schema.

## 5. Produce and verify visuals

Start with one pilot image. Inspect it against the topic before making the remaining assets.

1. Choose an object, action, document or diagram that directly explains the article. Avoid decorative machines, science imagery or metaphorical objects unrelated to the mechanism.
2. Compare the proposal with recent published visuals. Look at the actual images, not just their filenames. Keep the visual identity while varying the scene or information structure where appropriate.
3. Use owned, licensed or appropriately generated material. A generated person, receipt, balance, testimonial or official-looking document is not customer evidence.
4. For an infographic, map every label and number to an approved sentence or source. Compose important text with a controllable layout, then read the final image character by character.
5. Check legibility at the intended reading size, margins, cropping and caption placement. A high-resolution file can still be unreadable on a phone.
6. Export the exact formats and sizes supported by the destination. Prepare a separate sharing asset if needed. Measure the bytes actually served to preview crawlers rather than trusting an editor thumbnail.
7. Write accessibility text from the final pixels. Replace it whenever the image changes.

### Asset manifest template

```text
Asset role:
Final filename:
Final format / dimensions / byte size:
Approved article version:
Source, license or generation record:
Exact visible text:
Supporting article sentences or sources:
Alt text:
Caption and insertion point:
Comparison with recent published visuals:
Visual check result:
Public asset URL after approved upload:
Served-file verification result:
```

Keep a checksum for unchanged files. If the host recompresses an image, verify decoded dimensions and visible content rather than treating every byte difference as a failure. A different checksum does not establish visual variety.

## 6. Review, correct and authorize publication

The reviewer receives the complete article, sources, metadata, incoming-link instructions and final images. Separate factual review, language and voice review, and visual review when the subject warrants it. Specialists approve regulated advice where required.

Use this verdict format:

```text
VERDICT: PASS or FAIL
Article and asset version checked:

Blocking findings:
- Exact passage or asset:
- Source or reproducible defect:
- Required correction:
- Responsible role:
- Acceptance test:

Non-blocking notes:
Claims, calculations and links checked:
Visuals and alt text checked:
Remaining untested boundary:
```

A FAIL returns only the affected work to the responsible role. Preserve previous verdicts, then recheck the changed artifact and its dependents. For example, a corrected quantity may affect the article, infographic, summary and structured answers.

Set a bounded correction budget before running the chain. Two correction cycles is a reasonable starting policy, not a Whop rule. Escalate an unresolved disagreement after that limit rather than bouncing the same text between agents indefinitely. Do not count an authentication failure or provider quota outage as an editorial failure.

A stale internal note can be corrected without blocking release when the published text and images are demonstrably correct. An unsupported claim, wrong checkout, inaccessible promised content or misleading image remains blocking.

PASS means editorial approval of the checked version. The owner must separately approve publishing that version to the named destination. Any subsequent material edit reopens the relevant checks.

## 7. Publish and prove what is online

### Publication procedure

1. Confirm the exact site or publication, its current draft, the approved version and effective permissions. Close or coordinate stale editor tabs that could overwrite newer work.
2. Acquire a publication lock shared by automated and manual operators. Record the holder, target and start time. If another writer holds it, wait; before clearing a stale lock, verify that its holder is no longer writing.
3. Re-read the target's current state and compare it with the approved before-state. Stop on an unexpected competing edit.
4. Integrate the article using the real template. Preserve valid dates and signatures on existing pages. Add the approved images and internal-link changes, including the incoming links.
5. Run the project's actual build and content checks. Inspect the assembled article after captions and images are included.
6. Publish only within the authorized scope, then read back the exact target. Release the lock on success or on a safe stop.
7. Keep the result at `published-unverified` until the public checks below pass.

Do not reuse an earlier deployment merely because its name looks right. Confirm the version actually being served.

### Public proof checklist

- [ ] The exact canonical URL returns the intended article body, heading and version in a fresh visitor context.
- [ ] A missing or unrelated route does not masquerade as the same successful article. A site-wide HTTP 200 fallback is insufficient evidence.
- [ ] The title, description, canonical and crawl directives in served HTML match the intended publication state. Inspect the rendered page too.
- [ ] The exact canonical URL appears in the sitemap when the site's publication contract includes one. Validate the sitemap content rather than counting its HTTP response as proof.
- [ ] If no sitemap is provided by the platform, record “not provided” and use the actual public archive plus exact-content checks. Never claim sitemap inclusion without observing it.
- [ ] Images are downloaded from their public URLs and checked for content type, dimensions, file size and visible content.
- [ ] Captions and accessibility text match the served images. Stored metadata alone cannot prove that the public renderer emits accessible markup.
- [ ] Outgoing links open the intended pages. Approved incoming links are present in the existing articles or pillar page.
- [ ] The commercial CTA opens the intended offer and checkout with the approved terms. Do not submit a transaction without separate permission.
- [ ] Mobile rendering and primary navigation work. No draft marker, internal note or placeholder remains in public content.

A sitemap entry supports the publication check but does not prove search-engine indexing. A successful build, upload receipt or worker's “published” message is insufficient on its own.

### Publication receipt template

```text
Article title and approved version:
Expected public URL:
Observed final URL:
Published at / checked at, with time zone:
Deployment or revision reference, stored privately:
Expected article body and heading present:
Canonical / crawl policy:
Sitemap membership: yes / no / not provided / unreadable
Public archive entry:
Served images and metadata checks:
Outgoing and incoming links checked:
CTA and checkout checked without payment:
Desktop and mobile result:
State: verified-live / published-unverified / publication-unknown
Unresolved issue and next owner:
Search indexing: verified separately / not measured
```

If the sitemap or public host is temporarily unreadable, keep the state uncertain and retry within an agreed time budget. Do not re-create the article just because verification failed. If the page is live but a required sitemap entry is missing, repair that specific publication defect within scope.

### Operating the factory safely

- Use an idempotency reference for each article and stage. On restart, inspect existing work and resume the first unverified stage.
- Use atomic writes for the coordinator's state. Keep workers from overwriting the shared topic bank.
- Maintain a small reserve of approved topics. Refill it from evidence and deduplicate before merging; do not add invented topics to meet a quota.
- Limit concurrency at the actual bottleneck. Multiple researchers can work while a single publisher owns the shared deployment surface.
- Pause affected chains on lost authentication or exhausted provider quota. Preserve drafts, reservations and attempt counts; notify the operator with the exact blocked step. Do not buy credits or switch providers automatically.
- Give temporary service errors bounded retries with backoff. A generic rate-limit response does not, by itself, prove an exhausted paid quota.
- Preserve chains waiting for human input. Report their owner and next action rather than abandoning approved work to satisfy a timer.
- Escalate repeated unexplained failures and stop new launches when they indicate a shared fault.
- Do not restart or upgrade the orchestration runtime while a chain is writing. Resume with a reconciliation of existing artifacts and public state.

## 8. Turn the article into a newsletter

Use the approved article as the factual source. Decide whether the issue contains the full article or a teaser linking to a web version. These are different artifacts with potentially different URLs, audiences and publication states.

### Newsletter procedure

1. Inspect the most recent suitable sent edition and the recent subject-line history. Preserve an approved template's structure, but avoid repeating old promises or hooks.
2. Draft a subject and a complementary preview text. Set the web heading and search metadata separately; they do different jobs.
3. After permission to create a remote draft, duplicate or apply the tested template in the correct publication. Confirm draft state and clear any inherited schedule before editing.
4. Replace the article body and inherited title, slug, thumbnail, tags, audio, links and campaign labels. Recheck draft collisions before accepting an automatically altered slug.
5. Edit blocks through the supported editor or API. Preserve conditional containers and managed blocks; do not flatten the whole document to make an edit easier.
6. Reuse existing audience segments where appropriate. Read their actual definitions instead of assuming a displayed label is the stored condition.
7. Verify the email and web previews separately. Check a qualifying reader, an excluded reader and an anonymous web visitor for every important conditional block. State exactly which views were tested.
8. Check all media and links, the main CTA, relevant disclosures and unsubscribe controls. A product link in navigation does not prove that the intended offer block appears in the article body.
9. Obtain approval of the final content, audience, exclusions, date and time zone. Scheduling, web publication and email sending remain distinct actions.
10. After an authorized action, verify the saved state on that exact issue. A draft update does not necessarily change the live web article, and a published web article does not establish that the email was sent.

Do not subscribe purchasers, commenters or private-message recipients to marketing without the required permission. Collect only data needed for the stated purpose and keep subscriber-level data out of public reports.

### Teaser template

```text
Subject: [RECOGNIZABLE READER PROBLEM]
Preview: [USEFUL DETAIL THAT ADDS TO THE SUBJECT]

[Describe the decision or situation in ordinary language.]

[Give one supported finding or practical check.]

[Explain what the full article helps the reader do, including an important
limit when needed.]

Read the guide: [VERIFIED ARTICLE LINK]

[APPROVED SENDER SIGN-OFF]
[REQUIRED SENDER, PREFERENCE AND UNSUBSCRIBE ELEMENTS]
```

### Pre-send record

```text
Issue title:
Template and source article version:
Subject / preview / web title:
Editor destination / preview destination:
Web publication state:
Email state:
Audience / exclusions / consent basis:
Conditional-content tests:
Media and link tests:
Publication time and time zone, if approved:
Final approval:
Actual dispatch state and provider receipt, after sending:
```

Treat missing live alt text, broken contrast or a failed conditional block as a real rendering issue even if the stored draft looks correct. Document platform limitations honestly and choose an approved remedy; do not claim accessibility from asset metadata alone.

## 9. Adapt one source to each social network

Maintain a channel contract for each real destination: audience, language, supported format, length limits, link placement, media requirements, disclosure rules and approval state. The network classes below intentionally use generic labels. Map each to the owner's actual account before preparing posts.

| Network class | Useful adaptation | Link and media handoff | Review focus |
| --- | --- | --- | --- |
| Professional network | Explain a work decision, the mechanism and a short procedure | Evidence-led image or document; article link in the approved location | Professional relevance, supported claims and a complete thought before truncation |
| General-audience community network | Open with a familiar situation and explain the practical steps | Contextual image; body link or prepared first comment as the channel contract requires | Readability, context and permission to post in that community |
| Microblog network | Isolate a supported observation, then use a compact post, thread or long post if the account supports it | Standalone text or explanatory visual; prepare the link separately where required | Account format limits, caveats retained and no artificial engagement request |
| Short conversational network | Explain one useful point and invite a relevant response | Short native post with the approved link placement | Natural phrasing, enough context and no copied hook from the other networks |
| Visual or short-video network | Demonstrate one action or mechanism with a filmable script | Shot list, captions, cover, accessibility support and a tested destination route | Visual legibility, faithful captions and a CTA that actually works in that format |

No link-placement rule here is a universal ranking claim. Use account evidence and current platform rules. If the chosen workflow requires a first comment, deliver its text and verify the posting tool supports it before promising automated publication.

### Copy templates

Use one verified article and vary the angle. Replace the bracketed content with supported facts before approval.

```text
PROFESSIONAL NETWORK
When [WORK SITUATION], check [SPECIFIC CONDITION] before [ACTION].
[Explain the source-backed mechanism and its consequence.]
A practical sequence is [STEPS].
[State the important limit.]
CTA: [ONE RELEVANT ACTION]
First comment, if required: Full guide and sources: [VERIFIED ARTICLE LINK]
```

```text
GENERAL-AUDIENCE COMMUNITY NETWORK
If you are trying to [READER TASK], start by checking [OBSERVABLE DETAIL].
[Explain why it matters in ordinary language.]
[Give a usable step and the condition under which it applies.]
CTA: [ONE RELEVANT ACTION]
First comment, if required: The guide includes [SPECIFIC HELP]: [ARTICLE LINK]
```

```text
MICROBLOG NETWORK
[One supported observation about the task.]
[Mechanism, evidence and limit, in the account's supported format.]
[One practical check the reader can perform.]
CTA and link placement: [AS APPROVED FOR THIS ACCOUNT]
```

```text
SHORT CONVERSATIONAL NETWORK
[State one useful point from the article in a complete sentence.]
[Give enough context to prevent a misleading interpretation.]
[Ask a relevant question only if an answer would be useful.]
Destination: [APPROVED LINK OR REPLY]
```

```text
SHORT VIDEO
Opening: [A task or mistake visible on screen.]
Shot: [A feasible action using approved materials.]
Spoken explanation: [Source-backed mechanism in ordinary language.]
Demonstration: [What the viewer can actually observe.]
Limit: [What this demonstration does not establish.]
Closing action: [A route verified in this account.]
Captions / cover / media rights / disclosure:
```

For a comment-triggered delivery flow, verify the actual trigger, recipient experience and destination before using “comment to receive.” Send only what was requested. Broader marketing enrollment needs separate consent. If the flow is not operational, use another approved route instead of promising a private message.

### Distribution manifest

Keep the handoff provider-neutral, then map it to the scheduler's current import schema:

```text
Source article and version:
Destination account and network class:
Language:
Angle and hook:
Final text:
Final media and alt text:
Primary CTA:
First comment or reply, when required:
Verified destination link:
Campaign source / medium / campaign / content label:
Proposed local time / named time zone / explicit offset:
Approval state:
Provider state: local draft / remote draft / scheduled / published
Live post and comment URLs after publication:
```

Use campaign parameters for external distribution without putting personal data in them. Keep internal editorial links canonical. Traffic labels do not create affiliate attribution.

Before importing, read the scheduler's actual schema. Quote multiline and comma-containing fields correctly, confirm timezone behavior and verify the imported rows. A timestamp in a draft must not be mistaken for permission to schedule. Upload media sequentially when the provider requires it.

Inspect the final text, media, first comment and destination after an approved publication. Give any follow-up a genuinely different angle or new answer; do not repost identical copy to fill a calendar. Choose timing from the account's history and the article's availability, not from a supposed universal best hour.

## 10. Set up product affiliation in Whop

### Choose the correct mechanism

This section concerns affiliates who refer buyers to the seller's product.

| Mechanism | What it does | Boundary |
| --- | --- | --- |
| Product affiliate | Rewards attributed purchases of the agreed product or pricing variant | Configure global, member or custom terms explicitly |
| Revenue share | Splits revenue under an agreement at transaction level | Can apply without a referral click; do not use it as a shortcut for ordinary product referrals [W5] |
| Whop Partners | Refers business owners or partners to Whop | Separate enrollment, attribution and earnings rules; a product affiliate does not automatically become a referred business [W6] |
| Tracking link | Measures traffic and conversions for a selected destination | A traffic label alone does not establish an affiliate's commission [W8] |

Do not inject the publisher's own referral code into a seller's buyer checkout. Do not require a new Whop account or partner enrollment to use an otherwise compatible existing account. Whop's product-affiliate guide says sub-affiliates are not supported in that flow; do not import a separate partner-tier model into a product campaign. [W3, W6]

### Inspect defaults and approve economics

Whop's global-affiliate documentation describes a default 30% commission for marketplace promotion. This is a documented default as of 29 September 2026, not a recommended rate or proof of any account's configuration. Inspect the exact product. [W1]

Read global status and rate, member status and rate, and all existing custom overrides. Whop also documents that a member affiliate rate of 0% falls back to the global rate. Setting a member rate to zero is therefore not proof that affiliation is disabled. Use the supported enable/disable controls and verify the effective state. [W3]

Model the proposed commission with the business's own approved inputs:

```text
Net contribution per eligible sale =
retained sale revenue on the chosen accounting basis
- applicable platform and payment costs
- affiliate commission on its verified commission base
- fulfillment and support cost
- refund and dispute allowance
```

Keep taxes, currencies, settlement timing and refund assumptions explicit. Calculate using a spreadsheet or code. If a fee or commission base is unknown, the model is incomplete; do not select a profitable-looking rate by assuming the missing cost is zero. Use no real customer data in a public example.

### Program brief template

```text
Eligible product and pricing options, stored privately:
Program enabled or disabled:
Global commission:
Member commission and effective fallback:
Custom affiliates and overrides:
Percentage or fixed reward; unit and currency:
First payment or recurring payments:
Commission base:
Attribution terms and source:
Refund, reversal and dispute treatment:
Payout timing and applicable conditions:
Allowed channels and prohibited tactics:
Required disclosure and approved product claims:
Application or invitation process:
Approved support route:
Effective date and owner approval:
```

Keep membership access duration, subscription billing period and affiliate commission duration separate. A recurring customer payment does not prove a commission applies to every renewal.

### Dashboard setup, after approval

1. Select the correct business in the Whop dashboard. Open `Marketing` then `Affiliates`. Record the existing settings before changing them. [W3]
2. For product-wide settings, open the control to set the affiliate commission for a specific product or whop. Check the exact product row and set both global and member behavior deliberately. Labels may differ between documentation and the current interface. [W1, W3]
3. For a custom agreement, use `Set an affiliate commission for a specific user`. Resolve the intended person privately, choose percentage or fixed reward, choose `First Payment` or `Recurring Payments`, and restrict the eligible pricing options. Do not send an invitation without separate approval of its recipient and terms. [W2]
4. Save only the approved changes. Reopen the settings and verify the exact product, user scope, reward, duration and effective state. Check that unrelated products and prior agreements are unchanged.
5. Obtain the native affiliate link for the approved configuration. Never infer it from a username or silently replace its destination with an ordinary checkout. Test that it opens the intended offer and pricing option.
6. If the required post-purchase redirect belongs to a particular checkout configuration, confirm that the affiliate route preserves that behavior. When the platform-generated link and required checkout differ, resolve the binding before distribution; do not assume adding a parameter fixes it.
7. Give the affiliate the approved content kit and adjacent disclosure. Hold promotion until configuration and landing-page checks pass.

If using the API instead, read the current official schema and version before constructing a request. The developer guide describes creating or finding the affiliate record and then adding commission overrides; the record alone does not define the commission. Standard per-variant overrides support percentage or fixed rewards and first-payment or all-payment scope. Read back the saved override and use its returned links. Do not paste illustrative documentation identifiers into a real request. [W4]

### Attribution and earnings checks

Separate these checkpoints:

- Configuration saved and re-read.
- Native affiliate link resolves to the correct offer.
- An eligible purchase is attributed in Whop.
- Commission amount and status are recorded.
- Commission becomes available and any payout is actually completed.

A link click proves neither a purchase nor settled earnings. Do not create sham purchases or self-referrals to manufacture evidence. A legitimate end-to-end test needs explicit permission, a permitted test path or eligible participant, and compliance with the program's terms. If no such test occurred, label attribution and payout “not tested.”

Whop's developer guide describes a default 30-day attribution window. Its seller guide separately describes a 30-day wait before the affiliate receives commission. These are different clocks, both documented as of 29 September 2026; neither is a guarantee of a particular account's payout date. Confirm applicable terms before promising timing. The developer guide also describes refund-related commission reversals. [W3, W4]

For custom API reporting, the current developer guide describes cumulative earnings per override and says its v1 flow has no dedicated affiliate webhook or public payment-to-affiliate linkage. Re-read the relevant records on the reporting schedule rather than inventing that linkage from general payment events. Recheck the current API before implementation. Cumulative earnings are not proof of a bank withdrawal. [W4]

Before removing an affiliate, verify the consequences for prior sales. The seller guide says archiving stops new-sale commissions while recurring commissions from earlier sales continue. The developer guide's example instead says archiving blocks further commissions, without that qualification. These descriptions leave an ambiguity for API implementations. Confirm the treatment of existing recurring commissions with Whop before changing the agreement or promising a cutoff; do not assume archiving erases prior obligations. [W3, W4]

### Affiliate content kit

Provide:

- What the product delivers, who it is for and its material limits.
- Approved, current product claims and commercial terms.
- Licensed media and an authentic demonstration.
- The exact native affiliate link and its intended destination.
- Required disclosure beside the recommendation.
- Prohibited tactics, including fake reviews, unsolicited spam, fabricated scarcity and earnings guarantees.
- The process for reporting an incorrect claim, broken link or suspected abuse.

Generic disclosure:

```text
I may earn a commission if you purchase through this link.
Review the product details and terms before deciding whether it fits your needs.
```

Add any legally required information for the audience and channel. Do not add “at no extra cost,” a discount or preferential fees unless the actual terms support it.

### Optional tracking links

Whop documents `Dashboard` > `Marketing` > `Tracking links`, with a destination and pricing-option selection. After authorization, create only the required links, copy their native URLs and read back each destination. Test that redirecting or wrapping an affiliate link preserves its attribution and checkout behavior; if that cannot be established, keep the native affiliate link unchanged and report channel attribution as unknown. [W8]

## 11. Review outcomes before increasing volume

Use one row per asset and channel, with its source and measurement period. Preserve the distinction between output, reach and commercial results.

| Layer | Evidence to inspect | Decision it supports |
| --- | --- | --- |
| Article production | Stage completion, correction causes and verified-live receipt | Repair the slow or unreliable stage |
| Search discovery | Crawl state, indexed URL and measured impressions or clicks | Fix discovery and content relevance before expanding the backlog |
| Newsletter | Actual dispatch, delivery, unique clicks, unsubscribes and complaints | Improve the issue and audience fit; open-rate data alone is insufficient |
| Social | Verified live posts, valid destinations and attributable visits | Keep useful angles and fix broken handoffs |
| Whop offer | Checkout activity, eligible purchases, refunds and contribution | Test whether the content attracts suitable buyers |
| Product affiliates | Attributed eligible sales, commission status and reversals | Evaluate contribution and compliance rather than link clicks alone |

Use common periods and consistent units. Define each denominator before calculating a conversion rate, and do not add overlapping channel totals as unique people. Leave unavailable metrics blank or “not measured.”

At the end of each review, record the verified problem, one change, its owner and its acceptance test. When existing articles are not being discovered or the offer fails its access checks, fix that failure before increasing production.

## Whop sources

All sources below were consulted on 29 September 2026. Public documentation supports the product statements above; it does not prove configuration, eligibility, attribution or payouts for a particular account.

- [W1] [Set Up Global Affiliates](https://docs.whop.com/affiliates/setup-global): global defaults and separate global/member rates.
- [W2] [Set Up Custom Affiliates](https://docs.whop.com/affiliates/setup-custom): user-specific rewards, payment scope and eligible pricing options.
- [W3] [Promote Your Business](https://docs.whop.com/affiliates/promote-your-business): dashboard setup, member-rate fallback, payout waiting period, archiving and product sub-affiliate limits.
- [W4] [Affiliates](https://docs.whop.com/developer/guides/affiliates): affiliate records, overrides, attribution window, reversals and earnings-reporting limitations.
- [W5] [Set Up Revenue Share](https://docs.whop.com/affiliates/setup-rev-share): transaction-level revenue splits, distinct from ordinary referral links.
- [W6] [Partners](https://docs.whop.com/developer/partners/overview): the separate business-referral program and its attribution and earnings records.
- [W7] [Create a Checkout Link](https://docs.whop.com/manage-your-business/payment-processing/create-checkout-link): free, paid and recurring links, waitlist behavior and checkout routing.
- [W8] [Tracking Links](https://docs.whop.com/manage-your-business/growth-marketing/tracking-links): destination selection and channel-level traffic and conversion reporting.
