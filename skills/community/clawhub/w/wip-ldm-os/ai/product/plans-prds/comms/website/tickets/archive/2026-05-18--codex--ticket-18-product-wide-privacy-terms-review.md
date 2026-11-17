# Ticket 18: Product-wide privacy policy and terms review

**Date:** 2026-05-18
**Filed by:** Codex, with Parker
**Status:** archived, implemented and deployed. Legal rewrite shipped through PR #1026, then narrowed by #1033 and alias-updated by #1056. Product UI follow-ups remain separate Kaleidoscope tickets.
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Related:** Ticket 17 V04 footer/login/legal export, Ticket 16 website copy audit, Kaleidoscope guided onboarding ticket
**Surface:** WIP Computer legal pages for the complete website and product family

## Problem

The current legal pages are still written around a narrow Kaleidoscope demo.

Current source files:

```text
src/hosted-mcp/legal/privacy/en-ww/index.html
src/hosted-mcp/legal/internet-services/terms/site.html
```

Examples of stale scope:

```text
Privacy Policy - Kaleidoscope Demo
Terms of Service - Kaleidoscope Demo
WIP Computer, Inc. ("we", "us") operates the Kaleidoscope demo at wip.computer/demo.
This is a technology demonstration by WIP Computer, Inc.
This demo showcases passkey authentication, biometric permission, and AI image generation. It is not a production service.
Wallet balance (simulated, for demo purposes)
The demo wallet starts with $5.00 in simulated credits. No real money is charged.
This demo is provided "as is"...
```

That is no longer the right framing. The legal pages should cover WIP Computer's public website and active product surfaces broadly, including Kaleidoscope and future WIP Computer services, not only a throwaway demo.

This is a legal/content correctness ticket. It is not a visual footer ticket. Ticket 17 handles the white background and shared footer presentation.

## 2026-05-20 Deployment And Product UI Follow-Ups

PR #1026 was merged and deployed from commit `888260c`. The legal rewrite is live at:

```text
/legal/privacy/
/legal/internet-services/terms/site.html
/legal/internet-services/kaleidoscope/
```

The final review approved the legal pages for merge. The remaining items are product UI follow-ups, not another legal rewrite pass:

- [`ai/product/plans-prds/kaleidoscope/tickets/2026-05-20--codex--kaleidoscope-passkey-terms-acceptance.md`](../../../kaleidoscope/tickets/2026-05-20--codex--kaleidoscope-passkey-terms-acceptance.md)
- [`ai/product/plans-prds/kaleidoscope/tickets/2026-05-20--codex--kaleidoscope-generated-output-rights-notice.md`](../../../kaleidoscope/tickets/2026-05-20--codex--kaleidoscope-generated-output-rights-notice.md)

Do not reopen the legal copy for these two items unless counsel or Parker explicitly asks for a legal text change. The work now belongs in the Kaleidoscope product UI lane.

## Root Cause

The legal pages were added in commit `bd92ce4` with the subject:

```text
legal: production legal pages at Apple-style paths
```

That move created the production-looking URLs:

```text
/legal/privacy/en-ww/
/legal/internet-services/terms/site.html
```

But the body copy still came from the earlier Kaleidoscope demo legal pages. Since then, the homepage, login, footer, agent surfaces, and demo flow moved toward a broader WIP Computer product story, while these legal pages stayed frozen as demo disclaimers.

This is why the issue is surfacing now: the URL structure says product-wide legal, but the content still says Kaleidoscope demo.

## Intended Direction

Rewrite the legal pages so they cover WIP Computer as a company and product family:

- the public website at `wip.computer`
- Kaleidoscope
- passkey login and phone-rooted identity flows
- Lēsa-facing onboarding surfaces
- AI image generation and other third-party AI API calls
- wallet, credits, authorization, and payment-related product surfaces where present
- agent-facing install and inspection surfaces such as `agent.txt`, `llms.txt`, and `/install/*.txt`
- future WIP Computer products and services where the language can safely cover them without overclaiming

The pages should stop reading like a temporary demo disclaimer.

## URL Structure

Use a split legal structure instead of forcing every rule into one page.

Target shape:

```text
/legal/privacy/
/legal/internet-services/terms/site.html
/legal/internet-services/kaleidoscope/
```

Meaning:

- `/legal/privacy/` is the product-wide WIP Computer privacy policy. It should cover the website, WIP Computer account/login surfaces, passkeys, onboarding, wallet/credits data, agent surfaces, and product-family data practices where known.
- `/legal/internet-services/terms/site.html` is the general WIP Computer website and internet-services terms page. It should cover use of the site and shared WIP Computer services at a general level.
- `/legal/internet-services/kaleidoscope/` is the Kaleidoscope-specific service terms page. Product-specific terms that are unique to Kaleidoscope, including onboarding, Lēsa, xAI image generation, wallet/credits behavior, and phone-authorized actions, belong here rather than bloating the general site terms.

Build all three pages in this ticket.

Surface `/legal/internet-services/kaleidoscope/` as a legal link, not as a product/navigation link:

- link to it from the general Terms of Service page
- add a bottom legal link for Kaleidoscope-specific terms wherever the site shows the bottom legal link row for `Privacy Policy` and `Terms of Use`
- do not add it to the main product footer taxonomy, homepage nav, hero CTAs, or application/product link lists

The current `/legal/privacy/en-ww/` URL may stay as an alias or redirect if needed for compatibility, but the canonical product-wide privacy path should be `/legal/privacy/` unless the deployment/runtime requires the existing Apple-style path for now.

## Drafting Principles

Do not copy Apple or any other company's legal text. The Apple pages are useful only as a structural example: broad site terms plus product-specific service terms.

Write WIP Computer terms from how the product works today.

The terms should be protective for WIP Computer without pretending the product is more mature than it is. They should:

- preserve WIP Computer's rights in the site, product, onboarding materials, scripts, interface, examples, and WIP-supplied assets
- give users broad use rights for user-directed outputs where that is the product intent
- reserve WIP Computer's right to operate, improve, secure, demonstrate, explain, and market the service
- clearly say services are alpha, changing, and may be unavailable or modified
- clearly say third-party AI services and payment providers may have their own terms
- avoid promises the implementation does not yet satisfy
- be written so they can be updated as Kaleidoscope, wallet/payment behavior, and other WIP products mature

## 2026-05-20 Follow-Up: Trust Boundaries And System Layers

GPT 5.5 fresh review flagged that the legal pages are directionally right but still blur important boundaries:

- `WIP Computer` as company
- `wip.computer` and internet services as public website/services
- `Kaleidoscope` as the identity/access/onboarding client
- `LDM OS` as the runtime and orchestration layer
- `Memory Crystal` as the memory/context subsystem
- `Agent Pay` / `AI CASH` as the payments and authorization layer
- `Bridge` as coordination protocol
- local/on-device software
- hosted relay, registry, sync, wallet, payment, and cloud features
- third-party AI providers, tools, and MCP servers

The next legal-copy pass should sharpen those boundaries. The legal docs should sound like WIP Computer is building a distributed operating environment for AI systems, not merely a website with AI features.

### Product hierarchy to preserve

Use this architecture consistently:

```text
WIP Computer       umbrella company and product family
Kaleidoscope       identity, access, onboarding, and approval client
LDM OS             runtime and orchestration layer
Memory Crystal     memory, context, persistence, and retrieval subsystem
Agent Pay / AI CASH payments, wallet, and user-approved spend layer
Bridge             cross-agent and cross-runtime coordination protocol
```

Do not flatten these into one vague service. Do not make every legal obligation sound like it applies equally to local software, hosted services, third-party APIs, and future payment networks.

### Privacy trust-boundary requirements

Add explicit separation between:

- local device processing
- encrypted relay or sync
- hosted account services
- third-party AI providers
- payment and wallet infrastructure
- marketplace or registry services when they exist

Recommended direction:

```text
Many WIP Computer products are designed to operate primarily on-device. Data processed locally may not transit WIP-operated infrastructure unless you enable or use a synchronization, relay, payment, marketplace, registry, cloud, or third-party integration feature.
```

Review that sentence against implementation before shipping. If any current surface always sends data to WIP-operated infrastructure, narrow the language.

### Third-party model and tool boundaries

Add a section that distinguishes:

- WIP as orchestration layer
- third-party model execution
- local model or local tool execution
- third-party MCP servers, APIs, payment processors, package registries, and developer tools

Required meaning:

- When a user connects third-party AI systems or tools, those interactions may also be governed by the third party's terms and privacy practices.
- WIP Computer may route, coordinate, authorize, log, or display actions without being the model provider for every action.
- Local execution may stay on the user's machine unless the user enables sync, relay, payment, registry, or cloud features.

### Memory language

Define `memory` carefully. Avoid broad or scary phrasing such as:

- behavioral understanding
- we remember things
- permanent profile
- persistent identity, unless it is scoped to authentication/account continuity

Preferred framing:

- user-authorized persistence
- synchronization
- retrieval
- encrypted storage
- portable context
- agent memory systems

Suggested direction:

```text
Memory features are designed to store and retrieve user-authorized context so the user's agents can maintain continuity. Depending on the product and settings, memory may be local-only, synchronized, encrypted, or connected to third-party tools the user chooses.
```

Do not imply WIP can read encrypted private memory if the design is that WIP cannot. Do not imply all memory is end-to-end encrypted if some operational metadata remains server-readable.

### Stronger privacy commitments

Where true, state plainly:

- WIP Computer does not sell personal data.
- WIP Computer does not use advertising-network tracking.
- WIP Computer does not store biometric data server-side.
- WIP Computer does not receive Face ID or fingerprint data.
- Private keys remain device-bound or provider-bound where that is true.

Avoid absolute claims that may become false as products change. Use precise scope and caveats.

### Terms definitions to add

The general Terms of Use should define at least:

- `Services`
- `Software`
- `Agents`
- `Extensions`
- `Registries`
- `Third-Party Providers`
- `User Content`
- `Generated Content`
- `Local Runtime`
- `Hosted Services`
- `Payment Services`
- `Marketplace` if marketplace features are referenced

The point is not to make the terms long. The point is to stop legal ambiguity from turning local runtime, hosted services, third-party tools, and user-controlled agents into one undefined bucket.

### User responsibility for agents

Add stronger terms language around agent behavior, especially because WIP products involve tool calling, remote execution, code generation, and payments.

Required meaning:

- Users are responsible for agents, tools, extensions, permissions, and credentials they configure.
- Users authorize actions through passkeys, device approval, policies, spend limits, or other controls.
- Agents and AI systems may produce incorrect, unsafe, incomplete, destructive, or unexpected output.
- Users should review important actions before authorizing them.
- Third-party tools and providers are external systems and may fail, change, or behave outside WIP's control.

Do not imply the agent can spend, execute, or modify systems without user authorization.

### Agent Pay, AI CASH, marketplace, and payments

Agent Pay / AI CASH is documented in `repos/ldm-os/components/wip-agent-pay-private/` as:

- AI CASH: a default pool/checkout mode where the user approves payment with Apple Pay, Google Pay, or card
- Agent Wallet: optional bring-your-own wallet mode
- one-time payment links
- x402 and Stripe-backed payment paths
- user approval and spend limits
- no autonomous wallet funding or wallet destruction by the agent

Future-proof the legal copy, but do not imply payment products are live on every surface if they are not.

Terms should cover, where applicable:

- micropayments
- promotional credits
- wallet balances
- user-approved spend
- non-refundable usage or consumed services
- third-party seller/provider responsibility
- marketplace moderation
- fee routing
- fraud and abuse prevention
- sanctions, export controls, and prohibited transactions
- developer responsibility for tools, listings, and services

Suggested protective direction:

```text
Payment and wallet features may include promotional credits, user-funded balances, third-party checkout providers, marketplace transactions, or agent-requested purchases. Agents may request payment or spend actions, but users remain responsible for configured permissions, approvals, limits, and purchases they authorize.
```

Review wording against what is actually live before shipping.

### Kaleidoscope-specific legal emphasis

The Kaleidoscope terms should not undersell the product. Kaleidoscope is not just an app. It is the first identity, access, onboarding, and approval client.

Add or tighten language for:

- passkeys and WebAuthn
- phone or device authorization
- biometric approval staying on device
- delegated agent permissions
- session approval
- scoped tokens
- wallet or credit approval
- remote-control or handoff features, if surfaced through Kaleidoscope
- cryptographic identity, using careful non-overclaiming language

Preferred security wording:

- designed to
- intended to
- uses device-bound authentication
- uses passkey-based authentication
- uses industry-standard WebAuthn/passkey flows
- uses end-to-end encryption where implemented

Avoid:

- fully secure
- guaranteed private
- unhackable
- never accessible
- WIP can never see anything, unless narrowly true for a specific encrypted payload

## 2026-05-20 Follow-Up: Concrete Legal Rewrite Requirements

Claude Code reviewer read the three legal pages and identified concrete risks and representation gaps. The legal-hardening agent should rewrite the legal pages directly from these requirements and live product reality, not rely on summaries.

### Higher priority

1. **Privacy E2EE tense and scope.** The current clause:

```text
the system is designed for end-to-end encryption so WIP Computer cannot read the underlying private content
```

reads like a current-state representation. That is too risky for an alpha if Memory Crystal, Sapien ID, wallet, relay, or hosted account data are not all end-to-end encrypted in production today.

Required fix:

- split into current state and design destination
- name which storage categories are end-to-end encrypted now
- name which categories are designed for E2EE but not yet fully live
- name which operational data remains server-readable
- use one verb per category, such as `is encrypted`, `is designed to be encrypted`, `may be server-readable`, or `is processed to operate the service`

2. **Kaleidoscope generated image rights.** The Kaleidoscope terms currently grant WIP broad rights to use generated images. This may be intentional, but it is consumer-surprising and should be confirmed before shipping further.

Required review:

- confirm whether WIP really wants broad use, reproduction, display, distribution, modification, derivative-work, exploitation, marketing, commercializing, and explanatory rights for images created through Kaleidoscope
- reconcile WIP's intended rights with xAI/Grok terms for generated imagery
- if broad rights are intentional, add per-action consent at generation time or a clear in-flow notice
- if broad rights are not intentional, narrow the license to rights needed to operate, improve, debug, and display the service

3. **Privacy data-subject rights.** Add a real `Your Rights` section.

Required coverage:

- California CCPA/CPRA rights: access, deletion, correction, and opt out of sale or sharing for cross-context behavioral advertising where applicable
- GDPR/UK GDPR rights: access, rectification, erasure, portability, objection, restriction, and withdrawal of consent where applicable
- contact: `hello@wip.computer`
- response window: use a standard response target such as 30 days unless counsel directs otherwise
- do not overpromise availability of rights where local law does not require them, but make the page credible for California and EU/UK readers

### Medium priority

4. **Name xAI explicitly.** Privacy and Kaleidoscope should name xAI/Grok where current image generation sends prompts or images to xAI.

Required direction:

- keep generic `third-party AI providers` language for future surfaces
- explicitly list xAI/Grok as the current image-generation provider where true
- explain that xAI may receive prompts, inputs, images, metadata, or generated-output requests needed to perform the requested action

5. **Add a liability cap.** Site Terms and Kaleidoscope Terms disclaim categories of damages, but direct damages may remain uncapped.

Required direction:

- add `to the maximum extent permitted by law`
- add an aggregate cap, for example the greater of `$100` or fees paid to WIP Computer for the relevant service in the prior 12 months
- review whether the cap should differ for website-only, Kaleidoscope, and future paid Agent Pay services

6. **Add Cookies and Local Storage section.** The login/demo flow uses browser storage such as `lesa-token` and `lesa-agent` for session continuity.

Required coverage:

- sessionStorage/localStorage used for session continuity, login continuation, account state, passkeys preference, or local demo state where true
- expected lifespan, such as sessionStorage clearing when the tab/browser session closes
- no advertising cookies or advertising network tracking if true
- EU/ePrivacy sensitivity: local storage can be treated like cookies, so disclose plainly

7. **Third-party CDN dependency disclosure, or verify moot.** Reviewer flagged possible React/Babel/unpkg/Google Fonts dependencies. This may be stale because homepage static hardening removed React/Babel/unpkg/Google Fonts from the active homepage.

Required handling:

- first verify current live homepage and legal pages for third-party CDN script/font dependencies
- if none exist, do not add stale disclosure
- if any active page still loads third-party scripts, fonts, or CDNs, disclose what provider receives, such as IP address, User-Agent, and Referer
- if disclosure would conflict with local-first positioning, prioritize removing the dependency rather than adding legal cover

8. **Kaleidoscope age eligibility.** Kaleidoscope Terms should include an age clause.

Suggested direction:

```text
You must be at least 18 to use Kaleidoscope, or at least 13 with parent or guardian consent where local law permits.
```

Before real money or Agent Pay launches, review whether the product should require 18+ for wallet/payment features.

### Lower priority but should be decided

9. **Arbitration and class-action waiver.** Confirm whether omission is intentional. If WIP wants the standard US consumer posture, add binding arbitration and class-action waiver. If WIP wants California courts instead, record that decision.

10. **Venue and forum selection.** Site Terms and Kaleidoscope Terms currently name California governing law but should decide a venue, such as Los Angeles County or San Francisco County, if counsel agrees.

11. **Acceptance at passkey creation.** Verify the live `/login` create-account flow shows terms acceptance at the moment of passkey creation.

Required UI meaning:

```text
By creating a passkey, you agree to the Kaleidoscope Terms and Privacy Policy.
```

If the line is missing, file or update a separate implementation ticket. Do not rely only on legal page text for enforceable acceptance.

12. **Future Agent Pay real-money expansion.** Before Agent Pay or real-money wallet features launch, expand the wallet/payment terms.

Required future coverage:

- payment processor identity
- refund policy
- dispute process
- fees
- chargeback handling
- promotional credits versus real money
- seller/provider responsibility
- transaction limits
- sanctions, export controls, and prohibited transactions

Do not block the current alpha legal cleanup on the full Agent Pay launch language, but leave this as an explicit follow-up gate.

### Leave unchanged unless counsel directs otherwise

Keep:

- plain voice
- alpha framing
- layered structure: general Site Terms plus Kaleidoscope-specific terms
- no-passwords and no-biometric-data clarity
- `hello@wip.computer` contact
- consistent `May 18, 2026` effective date unless a new legal-copy ship date is chosen

## Required Changes

### Privacy Policy

Update the privacy page so it is product-wide.

Required content changes:

- remove `Kaleidoscope Demo` title/subtitle framing
- update `Last updated` to the actual ship date for the legal-copy update, expected `May 18, 2026` if this ships today
- replace `operates the Kaleidoscope demo at wip.computer/demo` with product-wide WIP Computer website/services language
- remove or revise demo-only data categories
- keep the passkey explanation, but make it apply to WIP Computer account/login surfaces
- keep the Face ID / fingerprint clarification: biometrics stay on the user's device and WIP Computer does not receive biometric data
- review whether `Photos ... never uploaded` is still true for all current and planned product surfaces before keeping it as broad policy language
- review whether `Cookies ... sessionStorage only` is still true across the full site and product family before keeping it
- update wallet language so it does not say only `simulated, for demo purposes`
- say plainly that WIP Computer tracks wallet balance, credits, authorization history, and related transaction metadata needed to show balances, approve actions, and prevent misuse
- do not imply a real-money wallet is live unless the implementation and business/legal decision are actually live
- add a safe distinction between sandbox/promotional credits and real-money wallet or payment features if both can exist
- keep xAI/Grok disclosure for image generation, but phrase it broadly as third-party AI services receiving the prompts or inputs required to perform requested actions
- remove or rewrite absolute `No analytics services` language unless the product will never use operational analytics; preferred shape is that WIP does not sell personal data or use advertising networks, and may use privacy-conscious operational analytics for reliability, abuse prevention, and product usage
- keep `No advertising networks` and `No data brokers` if true
- add end-to-end encryption language where accurate, with a metadata caveat: WIP Computer should not claim every field is unreadable if account metadata, passkey public credential data, routing metadata, logs, or fraud-prevention records remain server-readable
- review data retention, deletion, contact, and user-rights language for product-wide coverage

Required privacy sections:

- `What We Collect`
- `What We Do Not Collect`
- `How We Use Information`
- `Third-Party Services`
- `Data Storage And Encryption`
- `Data Retention, Deletion, And Export`
- `Children`
- `Changes To This Policy`
- `Contact`

`What We Collect` should cover, where accurate:

- passkey public credential data
- token name or account name
- wallet balance, credit balance, authorization history, and related transaction metadata
- prompts, actions, or requests the user authorizes
- generated outputs if WIP stores them
- uploaded, captured, or selected media only if the product actually receives or stores it
- device/session metadata needed to authenticate sessions, prevent abuse, operate the service, and debug reliability issues
- logs needed for security and reliability

`What We Do Not Collect` should cover, where accurate:

- passwords
- biometric data
- private keys
- sale of personal data
- advertising-network tracking

Be precise about photos and camera data. Do not say `Photos ... never uploaded` as a broad rule if any product flow uploads images, sends images to xAI, stores generated outputs, or later processes media server-side. If current camera capture is local-only, scope that statement to the specific feature.

Deletion/export language should tell users to contact:

```text
hello@wip.computer
```

Add a children/minors section because the site is public. Keep it simple unless counsel says otherwise.

Suggested privacy framing:

```text
WIP Computer operates products and services that use passkeys, device authorization, AI services, and wallet or credit balances. We collect the information needed to authenticate you, run the service, show balances, authorize actions, prevent misuse, and improve reliability.
```

Suggested wallet-data framing:

```text
Wallet balance, credit balance, authorization history, and related transaction metadata needed to show balances, approve actions, and prevent misuse.
```

Suggested third-party framing:

```text
We do not sell personal data or use advertising networks. We may use privacy-conscious operational analytics to understand reliability, abuse, and product usage. Third-party AI providers may receive the prompts, inputs, or metadata needed to perform actions you request.
```

Suggested encryption framing:

```text
Where WIP Computer stores user-controlled identity, memory, wallet, or agent context, the system is designed for end-to-end encryption so WIP Computer cannot read the underlying private content. Some operational metadata may still be processed to run, secure, and debug the service.
```

Review that wording against the actual implementation before shipping. If any part is not true yet, narrow it.

Naming note: `phone-rooted` describes the intended concept, but Parker wants a better public term. Treat it as provisional internal wording. Prefer plainer public language like `device-based`, `passkey-based`, `phone-authorized`, or `secured by your device` unless a final naming decision exists.

### Terms of Service

Update the terms page so it is product-wide.

Required content changes:

- remove `Kaleidoscope Demo` title/subtitle framing
- replace `This is a technology demonstration` with WIP Computer service/product language
- remove the `The Demo` section or rewrite it as `The Services`
- remove `It is not a production service` unless there is a precise alpha/beta disclaimer that applies honestly
- rewrite wallet terms so they can handle current sandbox credits and future real-money wallet behavior without misleading users
- do not promise users have $5.00 or $10.00 of real funds unless that is implemented and legally approved
- if promotional or test credits exist, say so clearly
- if real-money payments are not yet live, do not describe them as live
- remove generated-content license terms. The current generated-content license framing is wrong for Kaleidoscope images.
- review the statement that WIP may use generated images for marketing/research. This needs explicit product/legal approval before keeping.
- keep a no-warranty / alpha-software disclaimer, but avoid framing the whole service as fake
- add product-wide acceptable-use, user responsibility, third-party services, account/security, payment/credits, termination, and changes sections if needed

Required general site terms structure:

- `Agreement To Terms`
- `Use Of The Site`
- `Site Content`
- `Accounts And Security`, only if account behavior is referenced from the site terms
- `Additional Product Terms`
- `Third-Party Services And Links`
- `Feedback`
- `Availability And Changes`
- `Disclaimers`
- `Limitation Of Liability`
- `Indemnity`
- `Governing Law`
- `Contact`

The general site terms should be broad and boring. They cover the WIP Computer website, public pages, documentation, agent-readable pages, install instructions, footer links, and general internet services. They should not carry all Kaleidoscope-specific rules.

The general site terms should include a clear `Additional Product Terms` section that points to product-specific terms where applicable. For launch, that means:

```text
Kaleidoscope Terms: /legal/internet-services/kaleidoscope/
```

Do not turn the general terms into the Kaleidoscope terms. Keep the split clean.

### Draft Copy: General Website Terms

Use this as the first implementation draft for `/legal/internet-services/terms/site.html`. It still needs Parker/reviewer/legal review before final deployment.

```text
WIP Computer Website Terms of Use
Last updated: May 18, 2026

Agreement To Terms

These Website Terms of Use apply to wip.computer and the public websites, documentation, install instructions, agent-readable pages, and other internet services provided by WIP Computer, Inc. ("WIP Computer", "we", "us", or "our"). By using the site, you agree to these terms. If you do not agree, do not use the site.

Additional terms may apply to specific products or services. For Kaleidoscope, see the Kaleidoscope Terms at /legal/internet-services/kaleidoscope/. If product-specific terms conflict with these Website Terms, the product-specific terms control for that product.

Use Of The Site

You may use the site to learn about WIP Computer, inspect public product information, follow install instructions, read agent-facing documentation, and use public links we provide.

You may not misuse the site. This includes attempting unauthorized access, interfering with the site or its infrastructure, scraping in a way that burdens the service, impersonating another person or system, bypassing security controls, or using the site for unlawful activity.

Site Content

The site and its text, design, code, images, examples, documentation, interface, names, marks, product descriptions, and other materials are owned by WIP Computer or its licensors unless otherwise stated.

You may read, reference, and share public documentation for normal informational use. You may not copy, mirror, resell, or use WIP Computer content in a way that suggests endorsement, removes attribution, or misrepresents WIP Computer.

Open-source repositories, install documents, and packages may have their own licenses. Those licenses control your use of that code or package.

Accounts And Security

Some WIP Computer services use passkeys, device authorization, tokens, or other account credentials. You are responsible for keeping your devices and credentials secure and for activity authorized through your credentials.

Additional Product Terms

Some products have product-specific terms. Those terms apply in addition to these Website Terms.

Kaleidoscope Terms: /legal/internet-services/kaleidoscope/

Third-Party Services And Links

The site may link to GitHub, X, xAI, 1Password, package registries, app stores, or other third-party services. Those services are not controlled by WIP Computer and may have their own terms and privacy practices. You are responsible for reviewing them.

Feedback

If you send us feedback, ideas, bug reports, suggestions, or other comments, you allow WIP Computer to use them without restriction or compensation. Do not send confidential information through public channels.

Availability And Changes

WIP Computer is building active software. The site, product descriptions, documentation, install instructions, links, features, and availability may change at any time. Some products may be alpha, experimental, private, renamed, or unavailable.

Disclaimers

The site and its content are provided "as is" and "as available." WIP Computer does not promise that the site will be uninterrupted, error-free, secure, or current, or that any product or instruction will work for every user or environment.

Limitation Of Liability

To the fullest extent permitted by law, WIP Computer will not be liable for indirect, incidental, special, consequential, exemplary, or punitive damages, or for lost profits, lost data, lost goodwill, or service interruption arising from your use of the site.

Indemnity

You agree to defend and hold WIP Computer harmless from claims, damages, liabilities, costs, and expenses arising from your misuse of the site, violation of these terms, or violation of law or third-party rights.

Governing Law

These terms are governed by the laws of California and applicable United States law, without regard to conflict-of-law rules, unless local law requires otherwise.

Changes To These Terms

We may update these terms from time to time. The updated date will show when the terms last changed. Your continued use of the site after changes means you accept the updated terms.

Contact

Questions about these terms can be sent to hello@wip.computer.
```

### Kaleidoscope-Specific Terms

Add or plan the product-specific Kaleidoscope legal page at:

```text
/legal/internet-services/kaleidoscope/
```

This page should cover Kaleidoscope-specific behavior that should not be buried inside the general site terms:

- passkey login and phone-rooted identity in Kaleidoscope
- Lēsa as the AI inside Kaleidoscope
- onboarding flow and scripted guided actions
- xAI image generation and third-party AI calls initiated through Kaleidoscope
- wallet, credits, authorization, and spend confirmations
- distinction between current launch behavior, sandbox/promotional credits, and future real-money wallet behavior
- generated content and uploaded/captured media, only where technically accurate

This page should be implemented in this ticket and surfaced only through legal-context links.

The general Terms of Service page should include a clear pointer to this Kaleidoscope-specific page for product-specific rules.

Required Kaleidoscope terms structure:

- `Agreement To Kaleidoscope Terms`
- `What Kaleidoscope Is`
- `Accounts, Passkeys, And Device Authorization`
- `Onboarding And Lēsa`
- `Wallet, Credits, And Authorizations`
- `AI Services And Generated Content`
- `User Content And Media`
- `Acceptable Use`
- `Service Availability And Alpha Software`
- `Third-Party Services`
- `Privacy`
- `Termination`
- `Changes`
- `Contact`

Generated content needs product-specific treatment here.

Remove the current dual-license generated-content language. Do not say generated images are MIT, AGPL, Apache 2.0, or dual-licensed. Open-source software licenses do not belong on generated images in the Kaleidoscope terms.

Use this product rule instead, subject to final legal review:

- users may use the images they create in Kaleidoscope however they want, subject to law and any third-party AI provider restrictions
- WIP Computer retains a broad right to use, reproduce, display, distribute, modify, create derivative works from, exploit, and otherwise use images created through Kaleidoscope for operating, improving, demonstrating, marketing, commercializing, and explaining WIP Computer and Kaleidoscope
- onboarding imagery, example prompts, scripted walkthrough assets, interface text, and product-provided demo materials are WIP Computer content
- user-provided prompts, uploaded media, and user-directed generated outputs remain the user's content to the extent the user owns them, but WIP receives the rights needed to provide, secure, improve, support, demonstrate, market, and commercialize the service

Suggested generated-content framing:

```text
You may use images you create through Kaleidoscope for your own purposes, subject to applicable law and third-party service terms. WIP Computer may use, reproduce, display, distribute, modify, create derivative works from, exploit, and otherwise use images created through Kaleidoscope to operate, improve, demonstrate, market, commercialize, and explain WIP Computer and Kaleidoscope. Onboarding imagery, scripted walkthrough assets, example prompts, interface text, and other materials supplied by WIP Computer remain WIP Computer content. Prompts, uploaded media, and user-directed generated outputs remain your content to the extent you own them, and you grant WIP Computer the rights needed to provide, secure, improve, support, demonstrate, market, and commercialize the service.
```

Review this against xAI terms and any future image provider terms before shipping.

### Draft Copy: Kaleidoscope Terms

Use this as the first implementation draft for `/legal/internet-services/kaleidoscope/`. It still needs Parker/reviewer/legal review before final deployment.

```text
Kaleidoscope Terms of Service
Last updated: May 18, 2026

Agreement To Kaleidoscope Terms

These Kaleidoscope Terms apply to Kaleidoscope, Lēsa inside Kaleidoscope, Kaleidoscope onboarding, and related WIP Computer identity, wallet, authorization, and AI features. Kaleidoscope is provided by WIP Computer, Inc. ("WIP Computer", "we", "us", or "our").

By using Kaleidoscope, you agree to these terms and to the WIP Computer Website Terms of Use. If these Kaleidoscope Terms conflict with the Website Terms, these Kaleidoscope Terms control for Kaleidoscope.

What Kaleidoscope Is

Kaleidoscope is an early WIP Computer application for working with AI through passkey-based identity, device authorization, guided onboarding, Lēsa, wallet or credit balances, and AI services. Kaleidoscope is active software under development. Features may change, break, move, or be removed.

Accounts, Passkeys, And Device Authorization

Kaleidoscope uses passkeys and device authorization instead of passwords. Your biometric unlock, such as Face ID or fingerprint unlock, happens on your device. WIP Computer does not receive your biometric data.

You are responsible for the devices, passkeys, tokens, and authorizations you use with Kaleidoscope. Do not authorize actions you do not understand. If you believe your account, device, passkey, or token has been compromised, contact hello@wip.computer.

Onboarding And Lēsa

Lēsa is the AI inside Kaleidoscope. During onboarding, Kaleidoscope may use scripted flows, prompts, examples, generated imagery, and guided actions to explain WIP Computer products and help you set them up.

Kaleidoscope may limit what can be typed or requested during onboarding. This is intentional. The product is designed to guide users through specific actions rather than expose an unrestricted chat interface at all times.

Wallet, Credits, And Authorizations

Kaleidoscope may show a wallet balance, credit balance, promotional credits, test credits, transaction history, or authorization history. WIP Computer tracks these records to show balances, approve actions, prevent misuse, and operate the service.

Do not assume a displayed balance is real money unless Kaleidoscope clearly says it is real money and shows the applicable payment, authorization, and legal terms at the point of use.

Some balances may be promotional, test, sandbox, or non-cash credits. Some actions may require phone or device authorization before credits are spent or a third-party service is called. You are responsible for actions you authorize.

WIP Computer may change wallet, credit, authorization, pricing, and payment behavior as the product develops.

AI Services And Generated Content

Kaleidoscope may use third-party AI services, including image generation providers, to perform actions you request. Those providers may receive the prompts, inputs, metadata, or other information needed to perform the requested action. Third-party services may have their own terms and restrictions.

You may use images you create through Kaleidoscope for your own purposes, subject to applicable law and third-party service terms. WIP Computer may use, reproduce, display, distribute, modify, create derivative works from, exploit, and otherwise use images created through Kaleidoscope to operate, improve, demonstrate, market, commercialize, and explain WIP Computer and Kaleidoscope.

Onboarding imagery, scripted walkthrough assets, example prompts, interface text, product-provided demo materials, and other materials supplied by WIP Computer remain WIP Computer content.

Prompts, uploaded media, and user-directed generated outputs remain your content to the extent you own them, and you grant WIP Computer the rights needed to provide, secure, improve, support, demonstrate, market, and commercialize the service.

User Content And Media

You are responsible for prompts, uploaded media, instructions, and other content you provide to Kaleidoscope. Do not upload or request content you do not have the right to use. Do not use Kaleidoscope to create unlawful, abusive, infringing, deceptive, or harmful content.

If a feature processes media only on your device, WIP Computer will describe that behavior where relevant. If a feature sends prompts, images, or other inputs to a third-party AI service, that will be handled according to our Privacy Policy and the applicable third-party service terms.

Acceptable Use

You may not use Kaleidoscope to break the law, violate rights, bypass security, attack systems, impersonate others, abuse third-party services, generate harmful content, or interfere with WIP Computer products or infrastructure.

Service Availability And Alpha Software

Kaleidoscope is early software. It may be incomplete, unreliable, unavailable, or changed without notice. WIP Computer may pause, modify, limit, or discontinue any feature at any time.

Third-Party Services

Kaleidoscope may rely on third-party services such as AI providers, identity providers, developer platforms, hosting providers, payment providers, or software registries. WIP Computer is not responsible for third-party services, and their terms may apply.

Privacy

Your use of Kaleidoscope is covered by the WIP Computer Privacy Policy at /legal/privacy/. The Privacy Policy explains what information WIP Computer collects, how it is used, and how to contact us.

Termination

WIP Computer may suspend or terminate access to Kaleidoscope if we believe you violated these terms, created risk for WIP Computer or others, misused the service, or if we discontinue the product or feature.

Disclaimers

Kaleidoscope is provided "as is" and "as available." WIP Computer does not promise uninterrupted access, error-free operation, specific outputs, availability of any model or third-party provider, or that generated content will be accurate, useful, lawful for your intended use, or free of third-party claims.

Limitation Of Liability

To the fullest extent permitted by law, WIP Computer will not be liable for indirect, incidental, special, consequential, exemplary, or punitive damages, or for lost profits, lost data, lost goodwill, service interruption, model output, generated content, third-party service behavior, or actions you authorize.

Changes

We may update these Kaleidoscope Terms as the product changes. The updated date will show when the terms last changed. Your continued use of Kaleidoscope after changes means you accept the updated terms.

Contact

Questions about Kaleidoscope or these terms can be sent to hello@wip.computer.
```

## Wallet And Credits Guidance

Do not keep `Wallet balance (simulated, for demo purposes)` as the final product-wide language.

The product direction is moving toward a wallet that can be real. The legal copy needs to be honest about the current state without boxing WIP Computer into `demo only` language.

Recommended shape for the rewrite:

- if a product uses test credits, call them test credits or promotional credits
- if a product uses real money, say the product will disclose the amount, authorization step, and payment terms at the point of use
- if a balance is displayed, explain whether it is test, promotional, or real before the user authorizes spend
- never imply a user has real funds unless the backend and legal policy make that true

## Contact

Keep `hello@wip.computer` if that is the correct public contact.

If the legal pages need a fuller company contact block, add that as a review question rather than inventing address or legal-contact details.

## Out Of Scope

- Do not change the footer/layout work from Ticket 17 except where needed to avoid conflicting copy.
- Do not change authentication, passkey, wallet, image API, onboarding, Remote Control, relay, daemon, E2EE, or server behavior.
- Do not deploy.
- Do not invent legal claims, addresses, compliance regimes, payment terms, or data-processing practices.
- Do not make the policy sound more production-ready than the product is.

## Acceptance Criteria

- Privacy page no longer frames itself as `Kaleidoscope Demo`.
- Terms page no longer frames itself as `Kaleidoscope Demo`.
- Both pages cover WIP Computer's website and product family broadly.
- Kaleidoscope is included as one product surface, not the whole legal scope.
- Legal URL structure is explicit: product-wide privacy, general site terms, and Kaleidoscope-specific terms are separate concepts.
- `/legal/privacy/` exists or is explicitly routed as the canonical privacy path.
- `/legal/internet-services/terms/site.html` remains the canonical general terms path.
- `/legal/internet-services/kaleidoscope/` exists and contains Kaleidoscope-specific terms.
- `/legal/internet-services/kaleidoscope/` is linked from the general Terms of Service page.
- the bottom legal link row includes the Kaleidoscope-specific terms link where appropriate.
- `/legal/internet-services/kaleidoscope/` is not added to the main product footer taxonomy, homepage nav, hero CTAs, or application/product link lists.
- general site terms stay broad and link to Kaleidoscope-specific terms instead of absorbing product-specific rules.
- Kaleidoscope-specific terms remove the bad generated-content license framing, including MIT, AGPL, Apache 2.0, and dual-license language, and replace it with the WIP/user usage rule.
- Demo-only wallet language is removed or rewritten.
- Real-money wallet language is accurate and does not overclaim live functionality.
- Passkey and biometric language remains clear and accurate.
- Third-party AI service disclosure remains clear.
- Legal body copy is ready for Parker/reviewer/legal review.
- Any unresolved legal/business questions are listed clearly in the PR.
- No visual redesign beyond legal text changes and any already-approved Ticket 17 presentation.

## Review Notes For Coder

Work from current `origin/main` in a fresh worktree.

Stop at PR. Do not deploy.

Before writing final copy, report any assumptions that need Parker's decision, especially:

- whether the wallet is currently sandbox, promotional, real-money, or mixed
- whether generated images can be used by WIP Computer for marketing/research
- whether any analytics, cookies, logs, or retention practices exist outside the old demo language
- whether `hello@wip.computer` is the only required legal contact

This ticket can be implemented as a careful draft for review. It does not replace counsel review.
