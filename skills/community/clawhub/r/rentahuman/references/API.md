# RentAHuman MCP API Reference

> Auto-generated from the version 2 operation table and the `rentahuman-mcp` tool registry, for `rentahuman-mcp` version 5 — do not edit manually.
> Run `node --import tsx scripts/sync-clawhub.mjs` to regenerate.

Complete reference for all 73 MCP tools available through the `rentahuman-mcp` server.

Version 5 has new tool names. An old name of a renamed tool answers `tool_renamed` with the new name; a removed tool answers `tool_removed` with what to use instead, if anything. The tools under "Unchanged from version 4" keep their names and work as before.

Amounts in the new tools are whole US cents with a currency: `1999` is $19.99.

A parameter name with a dot is a field inside an object: `pay.amount` is the `amount` field of `pay`. `[]` stands for each item of a list.

## Tools

### `accept_application`

Accept one pending application and make a hire; the worker is paid later. An already-funded spot accepts hosted sign-in; paying for a spot requires an API key. If the applicant proposed another price, accepting charges that price without confirmation. Use for: hiring one applicant of your bounty. Not for: paying a worker (pay_hire); ending a hire (cancel_hire). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: accept_application({"applicationId":"a3Fh8kQz1WpL0mNc"}) Repeat: Once this has worked, a repeat does not do it again while that result still stands: it is refused, or answers with what is already there. Errors: spots_full, wallet_short, payment_page_open, held_pay_not_shown, payment_processing, charge_mismatch, payment_needs_attention, spot_not_paid_for, application_not_pending, application_changed, bounty_not_open, accept_in_progress, check_not_passed, applicant_unavailable, account_frozen, spending_limit_reached, account_setup_required; each error carries `fix`: what to do next.

**Parameters:**

- `applicationId` (required) — `string`; The application id. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.
- `message` (optional) — `string`; A note the applicant reads with the acceptance. Markup, script links and outer spaces are removed before it is stored, so the applicant may read fewer characters than you sent. Only when money is already held for the spot; a bounty paid per hire, or a spot this call pays for from your wallet, refuses it. Default: no note. Limits: 1 to 1000 characters.
- `idempotencyKey` (optional) — `string`; A unique string for this call. Repeat it when you retry, so the call runs once.

---

### `block_human`

Stop one person from applying to your bounties. Blocking also takes them off your preferred list. Blocking again only replaces the reason. Use for: keeping someone you do not want to work with away from your bounties. Not for: letting them apply again (unblock_human); seeing who you blocked (list_blocked_humans). Needs: an API key. Hosted sign-in cannot call this yet. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: block_human({"humanId":"h2Lw9QxT4mZp7Rk","reason":"Missed two shifts"}) Repeat: A repeat with the same input, and the same key if you sent one, does not act twice: it returns the same result, finishes the first call, or is refused. Errors: not_found, list_full, account_setup_required; each error carries `fix`: what to do next.

**Parameters:**

- `humanId` (required) — `string`; The human id, as `id` in list_humans. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.
- `reason` (optional) — `string`; Why you block them, for your own list. They never see it. Up to 280 characters. Left out: none, and a repeat without one clears the earlier one. Limits: at most 280 characters.

---

### `cancel_bounty`

End a bounty and receive its cancellation quote: what is quoted back and what each hired worker keeps. Use for: ending a bounty. Use preview: true for a quote. If confirmation_required, call again with only bountyId, confirmationToken and the same idempotencyKey within 5 minutes. If processing, retry with the same key. Check returned money with get_wallet and list_wallet_transactions. Every call counts toward the daily limit, shared with edits. Not for: ending one hire (cancel_hire); work that was not done (open_dispute). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: cancel_bounty({"bountyId":"b7Kq2mXw9TzR4nLp","reason":"not_enough_applicants","idempotencyKey":"5f0c7a2e-8d4b-4e1a-9c3f-2b6d1e8a7f40"}) Key: the idempotencyKey in the example is a sample. Replace it with a new unique key for each new call, and keep that key for the call’s retries and any confirmation it asks for. Repeat: A repeat with the same input, and the same key if you sent one, does not act twice: it returns the same result, finishes the first call, or is refused. Errors: not_cancellable, confirmation_expired, refund_changed, cancellation_in_progress, idempotency_key_reused; each error carries `fix`: what to do next.

**Parameters:**

- `bountyId` (required) — `string`; The bounty id, or a pasted rentahuman.ai/bounties/... link.
- `reason` (optional) — `"not_enough_applicants" | "applicants_not_fit" | "task_no_longer_needed" | "budget_timing_requirements_changed" | "other"`; Why you are ending the bounty. Needed on every call without a confirmationToken: there is no default.
- `details` (optional) — `string`; Your own words, needed when reason is other and refused with any other reason. Up to 500 characters. Limits: at most 500 characters, matches `\S`.
- `preview` (optional) — `boolean`; true returns the quote and a confirmationToken and never starts a cancellation. A cancellation that was already confirmed and is still being finished may be finished by any call, this one included; the reply then says cancelled or processing. Default false.
- `confirmationToken` (optional) — `string`; The token of a confirmation_required reply. Send it with bountyId only, and an idempotencyKey as on every call, within 5 minutes, to carry out that cancellation. The token decides which cancellation is carried out: the key sent with it is not compared. Limits: at least 1 character.
- `idempotencyKey` (required) — `string`; A unique string for this call. Repeat it when you retry, so the call runs once.

---

### `cancel_hire`

End one hire. The rest of the bounty keeps running. You get back what the cancellation rules allow. Use for: ending a hire before work is submitted. If confirmation_required, call again within 5 minutes with hireId, confirmationToken from cancellation.confirmation.token, and the same idempotencyKey. If processing, retry with the same key. Read cancellation.refund for the refund quote, or cancellation.held for where the held money went. Not for: ending the whole bounty (cancel_bounty); work that was not done (open_dispute). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: cancel_hire({"hireId":"a3Fh8kQz1WpL0mNc","idempotencyKey":"5f0c7a2e-8d4b-4e1a-9c3f-2b6d1e8a7f40"}) Key: the idempotencyKey in the example is a sample. Replace it with a new unique key for each new call, and keep that key for the call’s retries and any confirmation it asks for. Repeat: A repeat with the same input, and the same key if you sent one, does not act twice: it returns the same result, finishes the first call, or is refused. Errors: not_cancellable, only_spot, submission_waiting, confirmation_expired, refund_changed, cancellation_in_progress, idempotency_key_reused; each error carries `fix`: what to do next.

**Parameters:**

- `hireId` (required) — `string`; The hire id, from list_hires or accept_application. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.
- `confirmationToken` (optional) — `string`; The token of a confirmation_required reply. Send it with hireId and the same idempotencyKey within 5 minutes to carry out that cancellation. Default: none, which asks to end the hire. Limits: at least 1 character.
- `idempotencyKey` (required) — `string`; A unique string for this call. Repeat it when you retry, so the call runs once.

---

### `create_api_key`

Make a new API key for your account. The secret is shown once, in this reply. Its id is in list_api_keys. Use for: giving another agent or machine its own key, so you can revoke it alone later. At most 25 active keys. Not for: finding the id of a key (list_api_keys); turning a key off (revoke_api_key). Needs: an API key. Hosted sign-in cannot call this yet. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: create_api_key({"name":"Booking agent"}) Repeat: A repeat may act again on the thing as it stands then. Read it first. Errors: key_limit_reached, account_setup_required; each error carries `fix`: what to do next.

**Parameters:**

- `name` (required) — `string`; A name to tell this key apart, 1 to 50 characters, not only spaces. Spaces around it are dropped. Limits: at most 50 characters, matches `\S`.

---

### `create_bounty`

Post a bounty. It is paid for from your wallet at once when the balance covers it; use dryRun to see the cost first. Use for: posting new work. A short wallet saves a draft with `payUrl`, when a pay page could be made. Without `payUrl`, add money with fund_wallet, then call fund_bounty. Send an idempotencyKey to reuse the first bounty and ignore new input. Unkeyed retries may post again or be refused as duplicates; check list_bounties first. Not for: paying for a draft (fund_bounty). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Repeat: A repeat may act again on the thing as it stands then. Read it first. Errors: listing_refused, pay_below_minimum, duplicate_listing, spending_limit_reached, account_setup_required, wallet_short, create_in_progress, photos_not_available; each error carries `fix`: what to do next.

**Preview first:** `create_bounty({"title":"Photograph the storefront of 5 coffee shops","description":"Walk to each of the 5 listed coffee shops and take one clear photo of the storefront in daylight.","category":"creative-gigs","pay":{"type":"fixed","amount":1999,"estimatedHours":2},"spots":{"total":3},"location":{"country":"US","isRemoteAllowed":true},"proof":{"criteria":"Five photos, one per shop, each showing the shop sign.","types":["photo"]},"idempotencyKey":"5f0c7a2e-8d4b-4e1a-9c3f-2b6d1e8a7f40","dryRun":true})` returns the preview and the cost. Then send the same call without `dryRun` and with the same `idempotencyKey` (a sample: use a new key for each new call).

**Parameters:**

- `title` (required) — `string`; Limits: 5 to 200 characters.
- `description` (required) — `string`; Limits: 20 to 5000 characters.
- `category` (required) — `"computer-gigs" | "creative-gigs" | "crew-gigs" | "domestic-gigs" | "event-gigs" | "labor-gigs" | "talent-gigs" | "writing-gigs"`; The kind of work, as in the website’s category picker: workers browse bounties by it. Required, with no default: pick the closest. computer-gigs is work done at a computer; photographing a place is creative-gigs; errands and moving are labor-gigs.
- `skills` (optional) — `string[]`
- `requirements` (optional) — `string[]`
- `imageUrls` (optional) — `string[]`
- `location` (optional) — `object`; Omit this group to post a remote job (work from anywhere).
- `location.city` — `string`; Optional.
- `location.state` — `string`; Optional.
- `location.country` — `string`; Optional.
- `location.isRemoteAllowed` — `boolean`; Optional. Default false when location is sent: workers come in person.
- `countries` (optional) — `object`
- `countries.allowed` — `string[]`; Optional. Only workers in these countries may apply.
- `countries.hidden` — `string[]`; Optional. The bounty is hidden in these countries.
- `pay` (required) — `object`
- `pay.type` (required) — `"fixed" | "hourly"`
- `pay.amount` (required) — `integer`; What one worker receives for one spot (per hour when hourly), in whole US cents. Limits: 100 to 100000000.
- `pay.estimatedHours` — `number`; Optional. Hours per spot, at least 5 minutes; required without schedule. Shifts supply scheduled hours. Hourly pay holds amount × hours × spots.
- `spots` (optional) — `object`
- `spots.total` — `integer`; Optional. Spots to pay for. Default 1. Limits: 1 to 2000.
- `timeZone` (optional) — `string`; IANA time zone for startsAt and every shift of schedule.
- `startsAt` (optional) — `string`
- `schedule` (optional) — `object`
- `schedule.shifts` — `object[]`; Required in `schedule`.
- `schedule.shifts[].date` — `string`; Required in `schedule.shifts[]`. Local date, YYYY-MM-DD.
- `schedule.shifts[].start` — `string`; Required in `schedule.shifts[]`. Local time, HH:mm, in timeZone.
- `schedule.shifts[].end` — `string`; Required in `schedule.shifts[]`. Local time, HH:mm, in timeZone.
- `timers` (optional) — `object`
- `timers.start` — `object`; Optional. Not used when schedule is sent.
- `timers.start.minutes` — `integer`; Required in `timers.start`. Limits: 5 to 1440.
- `timers.response` — `object`; Optional.
- `timers.response.hours` — `number`; Required in `timers.response`. Limits: 1 to 720.
- `timers.response.releasesSpot` — `boolean`; Optional. Default false.
- `applications` (optional) — `object`
- `applications.closesAt` — `string`; Optional.
- `applications.keepPendingWhenFull` — `boolean`; Optional. Default false.
- `applications.questions` — `object[]`; Optional.
- `applications.questions[].id` — `string`; Optional.
- `applications.questions[].type` — `"text" | "checkbox" | "file_upload" | "live_video"`; Required in `applications.questions[]`.
- `applications.questions[].label` — `string`; Required in `applications.questions[]`.
- `applications.questions[].description` — `string`; Optional.
- `applications.questions[].isRequired` — `boolean`; Optional. Default false. A live_video question is always required: false is refused.
- `applications.questions[].maxLength` — `integer`; Optional.
- `applications.questions[].allowedFileTypes` — `("image" | "docx" | "pdf" | "txt" | "video" | "audio")[]`; Optional.
- `applications.questions[].maxFiles` — `integer`; Optional.
- `applications.links` — `object[]`; Optional.
- `applications.links[].type` — `"linkedin" | "instagram" | "twitter" | "github" | "resume" | "portfolio" | "custom"`; Required in `applications.links[]`.
- `applications.links[].label` — `string`; Optional.
- `applications.upload` — `object`; Optional.
- `applications.upload.type` — `"photo" | "video" | "document"`; Required in `applications.upload`.
- `applications.upload.max` — `integer`; Optional.
- `applications.upload.minimumResolutionPx` — `integer`; Optional. Photo uploads only.
- `applications.upload.acceptText` — `string`; Optional.
- `applications.upload.consentText` — `string`; Required in `applications.upload`.
- `applications.upload.confirmationMessage` — `string`; Required in `applications.upload`.
- `checks` (optional) — `object`
- `checks.identity` — `boolean`; Optional. Default false.
- `checks.linkedin` — `boolean`; Optional. Default false.
- `checks.app` — `"ios" | "android" | "any"`; Optional.
- `checks.mic` — `object`; Optional.
- `checks.mic.minScore` — `number`; Optional. Limits: 1 to 5.
- `checks.language` — `object`; Optional.
- `checks.language.language` — `"en"`; Required in `checks.language`.
- `checks.language.minimumCefr` — `"A2" | "B1" | "B2" | "C1" | "C2"`; Required in `checks.language`.
- `checks.nativeLanguage` — `object`; Optional.
- `checks.nativeLanguage.language` — `"yue" | "cmn" | "tr"`; Required in `checks.nativeLanguage`. Native language: yue Cantonese, cmn Mandarin, tr Turkish.
- `checks.excludeWorkersFromBountyIds` — `string[]`; Optional.
- `proof` (required) — `object`
- `proof.criteria` (required) — `string`; What the worker must accomplish; 10 to 2,000 characters after trimming.
- `proof.types` (required) — `("text" | "photo" | "video" | "link" | "document")[]`; Limits: at least 1 item.
- `proof.details` — `string`; Optional. Extra evidence rules; up to 2,000 characters after trimming.
- `proof.questions` — `object[]`; Optional.
- `proof.questions[].id` — `string`; Optional.
- `proof.questions[].prompt` — `string`; Required in `proof.questions[]`.
- `proof.questions[].isRequired` — `boolean`; Optional. Default true.
- `proof.liveCapture` — `"photo" | "video"`; Optional.
- `proof.photos` — `object`; Optional. Refused with photos_not_available unless your account has photo capture; plain photo proof uses proof.types: ["photo"].
- `proof.photos.criteria` — `string`; Required in `proof.photos`.
- `proof.photos.subject` — `string`; Optional.
- `proof.photos.minImages` — `integer`; Required in `proof.photos`.
- `proof.photos.maxImages` — `integer`; Required in `proof.photos`.
- `proof.photos.orientation` — `"any" | "portrait" | "landscape"`; Optional.
- `proof.photos.qualityNotes` — `string`; Optional.
- `proof.photos.area` — `object`; Optional.
- `proof.photos.area.lat` — `number`; Required in `proof.photos.area`.
- `proof.photos.area.lng` — `number`; Required in `proof.photos.area`.
- `proof.photos.area.radiusMeters` — `integer`; Required in `proof.photos.area`.
- `proof.photos.area.label` — `string`; Optional.
- `proof.checkIns` — `object`; Optional.
- `proof.checkIns.intervalMinutes` — `integer`; Required in `proof.checkIns`.
- `proof.location` — `object`; Optional.
- `proof.location.radiusMeters` — `integer`; Optional. Metres from the geocoded city, state and country; no street address can be sent. Limits: 50 to 2000.
- `proof.location.isPreciseRequired` — `boolean`; Optional. Default false. true needs termsVersion.
- `proof.location.termsVersion` — `"poster-precise-location-v1"`; Optional. Send it with isPreciseRequired true to accept the poster terms of precise location sharing.
- `bonuses` (optional) — `object[]`
- `bonuses[].title` — `string`; Required in `bonuses[]`.
- `bonuses[].condition` — `string`; Required in `bonuses[]`.
- `bonuses[].amount` — `integer`; Required in `bonuses[]`. Pay per earned item, in whole US cents.
- `bonuses[].maxUnits` — `integer`; Optional. Most items a worker can earn. Default 1.
- `ai` (optional) — `object`
- `ai.screening` — `boolean`; Optional. Default false.
- `ai.submissionReview` — `boolean`; Optional. Default false.
- `messages` (optional) — `object`
- `messages.instructions` — `string`; Optional.
- `messages.onAccepted` — `string`; Optional.
- `messages.onRejected` — `string`; Optional.
- `messages.onSubmissionReceived` — `string`; Optional.
- `messages.onSubmissionApproved` — `string`; Optional.
- `messages.onSubmissionRejected` — `string`; Optional.
- `dryRun` (optional) — `boolean`; true returns the preview and the cost and posts nothing. A dry run counts against your posting limits, and passing it does not promise the real post passes: some checks run only on a real post. Default false.
- `postAsOrganization` (optional) — `boolean`; true posts on behalf of your organization; you still pay from your own wallet. Refused when you belong to no organization. Default false.
- `signage` (optional) — `"poster_provided"`; Sign-holding jobs only: send "poster_provided" when you bring your own signs. Default: not sent.
- `idempotencyKey` (optional) — `string`; A unique string for this call. Repeat it when you retry, so the call runs once.

---

### `create_humanization`

Order one human to rewrite a text by hand, without AI. It is paid from your wallet at once when the balance covers it. Use for: ordering a hand-written rewrite of private text. When your wallet does not cover `cost.total`, the order waits as awaiting_payment and fund_bounty pays it later. The same idempotencyKey returns the first order, ignores new input, and never orders or charges twice. Not for: paying for an order awaiting payment (fund_bounty); reading where an order stands (get_bounty). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: create_humanization({"sourceText":"Our quarterly results exceeded expectations across every region, driven by strong demand.","transformation":"general_rewrite","subject":"quarterly update","turnaroundMinutes":120,"price":{"amount":2500,"currency":"usd"},"idempotencyKey":"5f0c7a2e-8d4b-4e1a-9c3f-2b6d1e8a7f40"}) Key: the idempotencyKey in the example is a sample. Replace it with a new unique key for each new call, and keep that key for the call’s retries and any confirmation it asks for. Repeat: A repeat with the same input, and the same key if you sent one, does not act twice: it returns the same result, finishes the first call, or is refused. Errors: humanization_unavailable, listing_refused, pay_below_minimum, duplicate_listing, spending_limit_reached, account_restricted, account_setup_required, wallet_short, create_in_progress; each error carries `fix`: what to do next.

**Parameters:**

- `sourceText` (required) — `string`; Private text for the accepted writer; 10,000 characters maximum including instructions and the two added newlines when instructions is supplied. Limits: 1 to 10000 characters, matches `\S`.
- `transformation` (required) — `"paraphrase" | "tone" | "clarity" | "shorten" | "expand" | "general_rewrite"`
- `subject` (optional) — `string`; A short PUBLIC topic shown in the listing title, such as "essay on AI infrastructure". Never private content. Limits: 3 to 80 characters, matches `\S`.
- `instructions` (optional) — `string`; Private notes for the writer. Limits: 1 to 5000 characters.
- `turnaroundMinutes` (required) — `integer`; Estimated writing time, not a deadline from ordering. Limits: 5 to 10080.
- `price` (required) — `object`; What the writer is paid, from $1 to $1,000,000. Our fee is added on top.
- `price.amount` (required) — `integer`; Limits: 100 to 100000000.
- `price.currency` (required) — `"usd"`
- `applicantScreening` (optional) — `object`; Applicants first rewrite a sample of this AI-written text by hand, with a screen recording. The sample is public on the listing.
- `applicantScreening.aiGeneratedSourceText` — `string`; Required in `applicantScreening`. Limits: 1 to 100000 characters, matches `\S`.
- `applicantScreening.percentage` — `integer`; Optional. Sample size as a share of sourceText. Default 5. Limits: 1 to 25.
- `applicantScreening.maximumWords` — `integer`; Optional. Default 500. Limits: 50 to 500.
- `applicantScreening.instructions` — `string`; Optional. Limits: 1 to 2000 characters.
- `requireResume` (optional) — `boolean`; true asks each applicant for a resume. Default false.
- `idempotencyKey` (required) — `string`; A unique string for this call. Repeat it when you retry, so the call runs once.

---

### `create_qa_run_template`

Starts runs that spend money from your wallet: people test your website for pay, the first run within about ten minutes, later runs on your cadence with no further call. Use for: paid human testing of a website. Each run takes costPerRun from your wallet; up to periodCap a month. With an idempotencyKey, within 24 hours the same key returns the first template and ignores new input. After 24 hours or without a key, a repeat saves a second template; both run and charge. Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: create_qa_run_template({"name":"Checkout smoke test","targetUrl":"https://shop.example.com/checkout","instructions":"Buy the cheapest plan with the test card and report every error you hit, with steps.","cadence":"weekly","testerCount":2,"payPerTester":{"amount":2000,"currency":"usd"},"budgetPerRun":{"amount":4720,"currency":"usd"},"periodCap":{"amount":23600,"currency":"usd"},"submissionMode":"video"}) Repeat: A repeat may act again on the thing as it stands then. Read it first. Errors: account_setup_required, create_in_progress; each error carries `fix`: what to do next.

**Parameters:**

- `name` (required) — `string`; Limits: 3 to 120 characters.
- `targetUrl` (required) — `string`; The website to test, http or https. It is checked when saved: when it cannot be reached, the template is saved paused. Limits: at most 2048 characters.
- `instructions` (required) — `string`; What every tester does. Limits: 20 to 5000 characters.
- `instructionMedia` (optional) — `object[]`; Screenshots or short clips shown with the instructions. Limits: at most 6 items.
- `instructionMedia[].url` — `string`; Required in `instructionMedia[]`. An upload under qa-templates/ in our own storage: an https firebasestorage.googleapis.com or storage.googleapis.com link. Any other link is refused. Limits: at most 2048 characters.
- `instructionMedia[].kind` — `"image" | "video"`; Required in `instructionMedia[]`.
- `instructionMedia[].caption` — `string`; Optional. Limits: 1 to 200 characters.
- `checklist` (optional) — `object[]`; Steps every tester must cover; each becomes a point their work is graded on. Limits: at most 30 items.
- `checklist[].id` — `string`; Optional. A lowercase id, unique in the list. Left out, one is made from the title. Limits: matches `^[a-z0-9][a-z0-9_-]{3,47}$`.
- `checklist[].title` — `string`; Required in `checklist[]`. Limits: 3 to 120 characters.
- `checklist[].instructions` — `string`; Optional. Limits: 1 to 1000 characters.
- `checklist[].media` — `object[]`; Optional. Limits: at most 4 items.
- `checklist[].media[].url` — `string`; Required in `checklist[].media[]`. An upload under qa-templates/ in our own storage: an https firebasestorage.googleapis.com or storage.googleapis.com link. Any other link is refused. Limits: at most 2048 characters.
- `checklist[].media[].kind` — `"image" | "video"`; Required in `checklist[].media[]`.
- `checklist[].media[].caption` — `string`; Optional. Limits: 1 to 200 characters.
- `testerStartMessage` (optional) — `string`; Sent privately to each tester once hired, for example test sign-in details. Limits: 1 to 1500 characters.
- `cadence` (required) — `"once" | "daily" | "every_2_days" | "weekly" | "custom"`; How often a run starts. once runs one time; the others repeat with no further call.
- `cadenceDays` (optional) — `integer`; Days between runs, 1 to 30. Required for custom, refused for any other cadence. Limits: 1 to 30.
- `testerCount` (required) — `integer`; Limits: 1 to 20.
- `payPerTester` (required) — `object`; What each tester gets, $1 to $5,000. Our 18% fee is added on top.
- `payPerTester.amount` (required) — `integer`; Limits: 100 to 500000.
- `payPerTester.currency` (required) — `"usd"`
- `budgetPerRun` (required) — `object`; A ceiling per run, $1 to $5,000. It must cover payPerTester plus the 18% fee (rounded to the cent) times testerCount. A run takes costPerRun, not this.
- `budgetPerRun.amount` (required) — `integer`; Limits: 100 to 500000.
- `budgetPerRun.currency` (required) — `"usd"`
- `periodCap` (required) — `object`; Monthly spending ceiling, at least budgetPerRun; equal to it for once. Recurring runs need monthly coverage, capped at $50,000; an error gives the minimum.
- `periodCap.amount` (required) — `integer`; Limits: 100 to 5000000.
- `periodCap.currency` (required) — `"usd"`
- `submissionMode` (required) — `"photo" | "video" | "document"`; What each tester hands in.
- `applicantScreening` (optional) — `object`; What an applicant must give: a live camera video, a LinkedIn profile, a PDF, DOCX or TXT resume. Each defaults to false.
- `applicantScreening.liveVideoRequired` — `boolean`; Optional.
- `applicantScreening.linkedinRequired` — `boolean`; Optional.
- `applicantScreening.resumeRequired` — `boolean`; Optional.
- `requiredCredentials` (optional) — `string[]`; Skills or experience an applicant must show. Limits: at most 10 items, each item 3 to 200 characters.
- `allowedCountries` (optional) — `string[]`; Two-letter country codes testers may be in. Default: any. Limits: at most 30 items, each item matches `^[A-Za-z]{2}$`.
- `autoMode` (optional) — `boolean`; Default true: we hire and review every tester, remove poor work and pay good work. false asks you for every hiring and pay decision.
- `idempotencyKey` (optional) — `string`; A unique string for this call. Repeat it when you retry, so the call runs once.

---

### `create_taste_run`

Ask a number of people to choose between 2 to 6 options, and pay each one. The cost is respondentCount times (pay plus 18% of pay, rounded), taken from your wallet in this call. Use for: a vote or taste test. If funds are short, the saved run starts automatically after funding. Send an idempotencyKey to reuse the first run and ignore new input. Unkeyed retries may charge again. Not for: adding money to your wallet (fund_wallet); finding a run you started earlier (list_taste_runs). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: create_taste_run({"question":"Which logo feels more trustworthy, and why?","options":[{"label":"Blue","url":"https://example.com/logo-blue.png"},{"label":"Green","url":"https://example.com/logo-green.png"}],"respondentCount":10,"payPerRespondent":{"amount":100,"currency":"usd"}}) Repeat: A repeat may act again on the thing as it stands then. Read it first. Errors: spending_limit_reached, run_not_funded, account_setup_required; each error carries `fix`: what to do next.

**Parameters:**

- `title` (optional) — `string`; Limits: 3 to 120 characters, matches `\S`.
- `question` (required) — `string`; Limits: 5 to 2000 characters, matches `\S`.
- `respondentCount` (required) — `integer`; Limits: 1 to 100.
- `targetCategories` (optional) — `("design" | "visual-art" | "music" | "photo-video" | "fashion-style" | "writing-performance")[]`; Creative categories of respondents to target; omit for no category restriction. Limits: 1 to 6 items.
- `allowedCountries` (optional) — `string[]`; Each item: ISO-2 country code. Limits: 1 to 30 items, each item matches `^[A-Za-z]{2}$`.
- `allowedGenders` (optional) — `("man" | "woman" | "other")[]`; Optional allowlist of self-declared profile genders. Omit for no gender restriction. Limits: 1 to 3 items.
- `identityRequired` (optional) — `boolean`; Require respondents to pass the account-level government ID check before applying.
- `requireVideoResponse` (optional) — `boolean`; Require each respondent to attach a recorded video response with their vote.
- `requirePortfolioUpload` (optional) — `boolean`; Require each respondent to upload a portfolio sample with their application.
- `acceptAllApplicants` (optional) — `boolean`; Accept every eligible applicant automatically instead of vetting creative fit. Eligibility checks and your country/gender restrictions still apply.
- `voteMode` (optional) — `"instant" | "chat"`; Defaults to instant. Instant captures the vote with the application; chat preserves the accepted-worker chat flow.
- `quickVote` (optional) — `boolean`; true: people tap one of exactly two image options and give no reason. Needs voteMode instant and no video or portfolio. Default false.
- `autoMode` (optional) — `boolean`; Defaults to true. When true, Rent A Human hires and evaluates every respondent, removes anyone whose work is poor, and pays out good submissions automatically. Set false to have every hiring and payout decision escalated to you instead.
- `options` (required) — `object[]`; The 2 to 6 things people choose between, each a label and an http(s) link. Labels must differ. Limits: 2 to 6 items.
- `options[].label` (required) — `string`; Limits: 1 to 80 characters, matches `\S`.
- `options[].url` (required) — `string`; Limits: at most 2048 characters.
- `payPerRespondent` (required) — `object`; Pay per person: at least 50 cents, or 10 for quickVote. Total worker pay must reach 100 cents; including our 18% fee, the run cannot exceed $2,000.
- `payPerRespondent.amount` (required) — `integer`; Limits: 10 to 200000.
- `payPerRespondent.currency` (required) — `"usd"`
- `idempotencyKey` (optional) — `string`; A unique string for this call. Repeat it when you retry, so the call runs once.

---

### `create_webhook_endpoint`

Register an https URL that is told about the events you choose, signed with a secret shown only in this reply. At most 5 endpoints. Use for: being told when something happens, for example a new application or message, instead of asking again and again. Not for: seeing the endpoints you have (list_webhook_endpoints); checking an endpoint receives events (test_webhook_endpoint). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: create_webhook_endpoint({"url":"https://hooks.example.com/rentahuman","events":["application.submitted","message.received"],"description":"Main agent"}) Repeat: A repeat may act again on the thing as it stands then. Read it first. Errors: endpoint_limit_reached; each error carries `fix`: what to do next.

**Parameters:**

- `url` (required) — `string`; Your https URL that receives the events. It must reach a public address. Limits: at most 2048 characters, matches `^https:\/\/`.
- `events` (required) — `("application.submitted" | "application.accepted" | "application.confirmed" | "application.rejected" | "application.seat_expired" | "application.ghost_flagged" | "application.started" | "application.start_deadline_passed" | "application.completion_deadline_passed" | "submission.submitted" | "submission.approved" | "submission.redo_requested" | "submission.rejected" | "submission.redo_deadline_passed" | "message.received" | "conversation.completion_claimed" | "proof.uploaded" | "bounty.seat_filled" | "bounty.completed" | "escrow.funded" | "escrow.released" | "payment.sent" | "wallet.low_balance" | "wallet.spending_cap_hit" | "run.status_changed" | "run.report_ready" | "webhook.test" | "*")[]`; Event names from the allowed list. Send ["*"] for every event. Limits: at least 1 item.
- `description` (optional) — `string`; Your own note to tell endpoints apart. Limits: at most 200 characters.

---

### `delete_webhook_endpoint`

Remove one of your webhook endpoints. No more events go to it, and its signing secret is gone: an endpoint created again gets a new secret. Use for: stopping events to a URL, making room for another endpoint, or restarting one that was switched off after failures. Not for: seeing your endpoints and their ids (list_webhook_endpoints). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: delete_webhook_endpoint({"endpointId":"Wk3pQ8vN1sXr6TzL0aBc"}) Repeat: Once this has worked, a repeat does not do it again while that result still stands: it is refused, or answers with what is already there. Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `endpointId` (required) — `string`; The webhook endpoint id. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.

---

### `download_picked_photos`

Get download links for the picked photos of one hire, as zip files of up to 100 photos each. Links last 15 minutes. Use for: downloading the photos you kept with pick_photos. Not for: looking through the photos one by one (list_hire_photos). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: download_picked_photos({"hireId":"a3Fh8kQz1WpL0mNc"}) Errors: no_picked_photos, no_submission, no_photo_submission, photos_not_available; each error carries `fix`: what to do next.

**Parameters:**

- `hireId` (required) — `string`; The hire id, from list_hires or accept_application. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.

---

### `fund_bounty`

Pay for a draft bounty's spots from your wallet. Call with dryRun first to see the total and your balance. Use for: paying for a draft bounty. Not for: paying a worker (pay_hire); adding a spot to a bounty that is already open (update_bounty); paying for one applicant on a bounty paid per hire (accept_application). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: fund_bounty({"bountyId":"b7Kq2mXw9TzR4nLp","dryRun":true}) Repeat: Once this has worked, a repeat does not do it again while that result still stands: it is refused, or answers with what is already there. Errors: wallet_short, bounty_changed, already_funded, not_fundable, payment_processing, spending_limit_reached, account_setup_required; each error carries `fix`: what to do next.

**Parameters:**

- `bountyId` (required) — `string`; The bounty id, or a pasted rentahuman.ai/bounties/... link.
- `dryRun` (optional) — `boolean`; true returns the quote and takes nothing. A dry run shows the price, not whether the charge will be allowed. Default false.

---

### `fund_wallet`

Get a card pay link that adds money to your wallet. Nothing is added until the link is paid. Use for: topping up before you fund a bounty or send money. Hand `payUrl` to the person who pays. Not for: checking your balance (get_wallet); paying for a draft bounty (fund_bounty). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: fund_wallet({"amount":{"amount":5000,"currency":"usd"}}) Repeat: A repeat may act again on the thing as it stands then. Read it first. Errors: account_setup_required, funding_unavailable; each error carries `fix`: what to do next.

**Parameters:**

- `amount` (required) — `object`; How much to add, from $1 to $10,000.
- `amount.amount` (required) — `integer`; Limits: 100 to 1000000.
- `amount.currency` (required) — `"usd"`

---

### `get_account`

See which account and profile your calls act for, and how this call signed in. Use for: checking who you act for before other calls, and whether the account still needs a profile. Not for: your money (get_wallet). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: get_account({}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

None

---

### `get_application`

Get everything needed to decide on one application: the person, their answers and the bounty's terms. Use for: deciding whether to accept or reject one applicant. Not for: reading every applicant of a bounty (list_applications); reading a hire after the accept (get_hire). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: get_application({"applicationId":"a3Vn8cQe1RuY6wHs"}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `applicationId` (required) — `string`; The application id. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.

---

### `get_bounty`

Get one bounty you posted, with how many people were told about it and applied. Use for: checking the status, spots, settings and outreach of one bounty. Not for: reading who applied (list_applications); reading who you hired (list_hires). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: get_bounty({"bountyId":"b7Kq2mXw9TzR4nLp"}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `bountyId` (required) — `string`; The bounty id, or a pasted rentahuman.ai/bounties/... link.

---

### `get_cake_order`

Get one cake order you sent: its status, who it goes to, the delivery photos and what it cost. Use for: checking where a cake order stands after send_cake. It only reads the stored order: it never asks the vendor, sends the order again or moves money. Not for: ordering a cake (send_cake). Needs: an API key. Hosted sign-in cannot call this yet. Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: get_cake_order({"orderId":"cake_3f9a0c1e2b4d5f6a7b8c9d0e1f2a3b4c5d6e7f80"}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `orderId` (required) — `string`; The order id send_cake returned. Limits: matches `^cake_[a-f0-9]{40}$`.

---

### `get_cake_quote`

Ask whether a cake can be delivered to an address, and what each size costs, per cake. Use for: checking delivery and prices before sending a cake. Nothing is ordered or paid. Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: get_cake_quote({"address":"1 Market St","city":"San Francisco","state":"CA","zip":"94105"}) Errors: quote_unavailable; each error carries `fix`: what to do next.

**Parameters:**

- `websiteUrl` (optional) — `string`; A company website. The bakery finds the address. Send this, or a full address. Limits: 1 to 2000 characters, matches `^https?:\/\/`, matches `\S`.
- `address` (optional) — `string`; Street and number. Send it with city, state and zip. Limits: 1 to 500 characters, matches `\S`.
- `address2` (optional) — `string`; Suite, floor or unit. Limits: 1 to 500 characters, matches `\S`.
- `city` (optional) — `string`; Limits: 1 to 200 characters, matches `\S`.
- `state` (optional) — `string`; Limits: 1 to 100 characters, matches `\S`.
- `zip` (optional) — `string`; Limits: 1 to 20 characters, matches `\S`.
- `quantity` (optional) — `integer`; How many cakes, 1 to 100. Default 1. It can change what sizes are offered; prices stay per cake. Limits: 1 to 100.

---

### `get_conversation`

Get one of your conversations with a worker and its first 100 messages, oldest first. When `messages.nextCursor` is set, pass it to list_messages for the rest. Use for: opening a conversation: who it is with, whether you can send now, and what was said. Not for: finding a conversation (list_conversations); reading past the first 100 messages (list_messages). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: get_conversation({"conversationId":"c7Rk2mQw9TzL4nXp"}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `conversationId` (required) — `string`; The conversation id, from list_conversations or the conversationId of a hire. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.

---

### `get_hire`

Get one hire: the worker, the money, what they submitted and what you can do next. Use for: reviewing the work of one worker, how many photos wait for you, the dispute and the latest message. Not for: listing every worker on a bounty (list_hires); looking through the photos (list_hire_photos); finding work that waits for review (list_submissions). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: get_hire({"hireId":"a3Fh8kQz1WpL0mNc"}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `hireId` (required) — `string`; The hire id, from list_hires or accept_application. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.

---

### `get_hire_location_track`

Get where one hired worker was on an in-person bounty that requires precise location: the site, the latest position and up to 1,000 recorded positions. Use for: checking where a worker was during this round of work, when they share a precise location. Not for: seeing who is on site across a bounty (list_hires). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: get_hire_location_track({"hireId":"a3Fh8kQz1WpL0mNc"}) Errors: location_not_shared, no_location_track; each error carries `fix`: what to do next.

**Parameters:**

- `hireId` (required) — `string`; The hire id, from list_hires or accept_application. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.

---

### `get_human`

Get one person’s full public profile: bio, languages, hours, rate, rating and paid track record. Use for: deciding whether to hire someone you found. Not for: finding people (list_humans); reading what others wrote about them (list_reviews). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: get_human({"humanId":"h2Lw9QxT4mZp7Rk"}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `humanId` (required) — `string`; The id from list_humans. Their username also works. Limits: 1 to 200 characters.

---

### `get_humanization`

Get one order for a human rewrite of a text: its status, writer and the rewritten text once it is sent. Use for: reading the rewritten text and where a humanization order stands. Not for: its spots, outreach or settings as a bounty (get_bounty). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: get_humanization({"humanizationId":"h7Kq2mXw9TzR4nLp"}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `humanizationId` (required) — `string`; The id create_humanization returned. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.

---

### `get_qa_run`

Get one QA run you started: where the testing stands, what it cost, the report and its findings, and what each tester sent. Use for: checking a QA run’s progress and reading its findings and each tester’s written account and evidence. Not for: finding a run id (list_qa_runs); reading a taste run (get_taste_run); checking your wallet balance (get_wallet). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: get_qa_run({"runId":"qa_run_7Np3sD8"}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `runId` (required) — `string`; The run id the create call or the list answered with. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.

---

### `get_taste_run`

Get one taste run you started: its status, the live vote count per option, what it cost, and the report once it is closed. Use for: checking where a taste run stands and reading its result. While it is collecting, read it again in 20 to 30 minutes. Not for: reading a QA run (get_qa_run); checking your wallet balance (get_wallet). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: get_taste_run({"runId":"taste_8Hc2pQ1vLm"}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `runId` (required) — `string`; The run id create_taste_run answered with, or one from list_taste_runs. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.

---

### `get_wallet`

Get your wallet balance, your spending limits, and whether you can add money by card now. Use for: checking what you can spend before you fund a bounty or send money, and reading your limits. Not for: money that came in or went out (list_wallet_transactions). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: get_wallet({}) Errors: account_setup_required; each error carries `fix`: what to do next.

**Parameters:**

None

---

### `get_webhook_delivery`

Get one delivery to your endpoints: where it stands, the exact body that was signed and sent, and each try with the status your URL gave. Use for: seeing whether a test or real event reached your URL, and why it failed if it did not. Not for: finding deliveries and their ids (list_webhook_deliveries). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: get_webhook_delivery({"deliveryId":"3f9c2a7b1e5d8c4f0a6b2e9d7c3f1a5b8e4d0c6a2f9b7e3d1c5a8f4b0e6d2c9a"}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `deliveryId` (required) — `string`; The delivery id. Limits: matches `^[0-9a-f]{64}$`.

---

### `invite_human`

Ask one person, by id, to apply to your open bounty. Use for: a poster who already knows which person they want. Inviting the same person to the same bounty again sends nothing new. Not for: telling many matching workers at once (invite_more_applicants); finding the person’s id (list_humans); seeing whether they applied (list_applications). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: invite_human({"bountyId":"b7Kq2mXw9TzR4nLp","humanId":"h2Lw9QxT4mZp7Rk"}) Repeat: A repeat with the same input, and the same key if you sent one, does not act twice: it returns the same result, finishes the first call, or is refused. Errors: not_found, not_open, worker_unavailable, already_applied; each error carries `fix`: what to do next.

**Parameters:**

- `bountyId` (required) — `string`; The bounty id, or a pasted rentahuman.ai/bounties/... link.
- `humanId` (required) — `string`; The human id, as `id` in list_humans. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.

---

### `invite_more_applicants`

Tell another wave of matching workers about an open bounty. Once per bounty per day. Use for: a bounty that needs more applicants. The reply says how many workers were put in line in this call, not how many messages arrived. Not for: changing the bounty so more people fit (update_bounty). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: invite_more_applicants({"bountyId":"b7Kq2mXw9TzR4nLp"}) Repeat: A repeat may act again on the thing as it stands then. Read it first. Errors: forbidden, not_open, invited_recently; each error carries `fix`: what to do next.

**Parameters:**

- `bountyId` (required) — `string`; The bounty id, or a pasted rentahuman.ai/bounties/... link.

---

### `list_api_keys`

List the API keys of your account, newest first. The secret of a key is never shown again. Use for: finding the id of a key to revoke, and seeing which keys are active and when they were last used. Not for: making a new key (create_api_key); turning a key off (revoke_api_key). Needs: an API key. Hosted sign-in cannot call this yet. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: list_api_keys({}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

None

---

### `list_applications`

List who applied to one of your bounties, best matches first. Use for: reviewing applicants, or finding every hire including ended ones (status: accepted). Not for: reading one application with the profile and the bounty terms (get_application); reading what hired workers did (list_hires). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: list_applications({"bountyId":"b7Kq2mXw9TzR4nLp","status":"pending","limit":20}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `bountyId` (required) — `string`; The bounty id, or a pasted rentahuman.ai/bounties/... link.
- `status` (optional) — `"pending" | "accepted" | "rejected" | "withdrawn"`
- `sort` (optional) — `"best" | "newest"`; best: matches ranked again each call; pages may repeat or miss rows. newest: stable, newest first. Unreadable records are omitted.
- `limit` (optional) — `integer`; Rows wanted. Each call reads one stretch of the applications, for every sort and status, so a page can hold fewer rows than `limit`, or none, while `nextCursor` says more remain; only a page without `nextCursor` is the end. Limits: 1 to 100.
- `cursor` (optional) — `string`; The nextCursor of the previous page. Leave it out for the first page.

---

### `list_blocked_humans`

Everyone you blocked from applying to your bounties, newest first, with your reason. Use for: checking whether you blocked someone, or finding whom to unblock. Not for: letting someone apply again (unblock_human); people you like to work with (list_preferred_humans). Needs: an API key. Hosted sign-in cannot call this yet. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: list_blocked_humans({}) Errors: account_setup_required; each error carries `fix`: what to do next.

**Parameters:**

None

---

### `list_bounties`

List your own bounties, newest first: the ones you or your agent posted, and your organization's; search_bounties finds open bounties to apply to. A page can hold fewer rows than `limit`, or none; keep going until a page has no `nextCursor`. Not listed: a bounty priced in another currency, or one the website's list also hides from you. A bounty you post while paging is not in that walk; start again to see it. Use for: finding a bounty you can manage, or every bounty in one status. Not for: reading one bounty in full (get_bounty); reading who applied (list_applications). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: list_bounties({"status":"open","limit":20}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `status` (optional) — `"draft" | "under_review" | "open" | "paused" | "completed" | "closed"`
- `limit` (optional) — `integer`; Rows wanted. A page can hold fewer, or none; only a page without nextCursor is the end. Limits: 1 to 100.
- `cursor` (optional) — `string`; The nextCursor of the previous page. Leave it out for the first page.

---

### `list_conversations`

List your conversations with workers, newest activity first: who, the subject, unread messages, and whether you can send now. Keep going until a page has no `nextCursor`. Use for: finding the conversation with a worker, or the ones with messages you have not read. Not for: reading the messages of one conversation (get_conversation); reading what a hired worker did (get_hire). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: list_conversations({"isUnread":true,"limit":20}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `status` (optional) — `"active" | "archived" | "converted"`
- `isUnread` (optional) — `boolean`; true: only conversations with messages from the worker you have not read. Left out or false: every conversation.
- `hasReplies` (optional) — `boolean`; true: only conversations with more than one message. Left out or false: every conversation.
- `bountyId` (optional) — `string`; The bounty id, or a pasted rentahuman.ai/bounties/... link.
- `subject` (optional) — `string`; Only conversations with exactly this subject. Limits: 1 to 500 characters.
- `limit` (optional) — `integer`; Rows wanted. A page can hold fewer, or none; only a page without nextCursor is the end. Limits: 1 to 100.
- `cursor` (optional) — `string`; The nextCursor of the previous page. Leave it out for the first page.

---

### `list_hire_photos`

List a hired worker’s bounty photos in the order sent. Continue until there is no nextCursor. Use for: looking through the photos before you pick them with pick_photos. Not for: how many photos are in each state (get_hire); downloading the picked photos (download_picked_photos). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: list_hire_photos({"hireId":"a3Fh8kQz1WpL0mNc","filter":"to_review"}) Errors: no_submission, no_photo_submission; each error carries `fix`: what to do next.

**Parameters:**

- `hireId` (required) — `string`; The hire id, from list_hires or accept_application. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.
- `filter` (optional) — `"to_review" | "picked" | "dropped" | "all"`; Only photos in this state. Default: all.
- `limit` (optional) — `integer`; Rows wanted. A page can hold fewer, or none; only a page without nextCursor is the end. Limits: 1 to 100.
- `cursor` (optional) — `string`; The nextCursor of the previous page. Leave it out for the first page.

---

### `list_hires`

List the workers you hired on one bounty, by when they applied, newest first, with where each one stands and who is on site. Each call reads one stretch of the applications, so a page can hold fewer rows than `limit`, or none, while `nextCursor` says more remain; keep going until a page has no `nextCursor`. Each hire is read when the list reaches it, so one that changes while you page is still listed once. An applicant you accept after the list has passed them is not in that walk; start again to see them. Use for: seeing every worker on a bounty, their money and what waits for you. Not for: reading one hire in full, with the work (get_hire); finding work that waits for review (list_submissions); reading who applied and is not hired (list_applications). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: list_hires({"bountyId":"b7Kq2mXw9TzR4nLp","status":"active","limit":20}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `bountyId` (required) — `string`; The bounty id, or a pasted rentahuman.ai/bounties/... link.
- `status` (optional) — `"offered" | "active" | "submitted" | "paid" | "disputed" | "ended"`; Only hires in this status. Default: every hire.
- `limit` (optional) — `integer`; Rows wanted. Each call reads one stretch of the applications and builds at most `limit` hires from it, so a page can hold fewer rows than `limit`, or none, while `nextCursor` says more remain; only a page without `nextCursor` is the end. Limits: 1 to 50.
- `cursor` (optional) — `string`; The nextCursor of the previous page. Leave it out for the first page.

---

### `list_humans`

Find people by skill, name, place and hourly rate, best match first. Keep going with the same filters until a page has no `nextCursor`. Use for: finding someone to do a task, or checking who offers a skill. Not for: getting a task done (create_bounty). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: list_humans({"skill":"photography","city":"Austin","limit":20}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `skill` (optional) — `string`; Comma-separated skills; matches any of the first 10. Limits: 1 to 200 characters.
- `name` (optional) — `string`; Part of their name. Limits: 1 to 100 characters.
- `city` (optional) — `string`; Ranks people in this city first; others may follow. Limits: 1 to 100 characters.
- `country` (optional) — `string`; Country name or code. Ranks people there first; others may follow. Limits: 1 to 100 characters.
- `minHourlyRate` (optional) — `integer`; Lowest USD hourly rate in whole cents; excludes other currencies. Limits: 0 to 1000000.
- `maxHourlyRate` (optional) — `integer`; Highest USD hourly rate in whole cents; excludes other currencies. Limits: 0 to 1000000.
- `limit` (optional) — `integer`; Rows wanted. A page can hold fewer, or none; only a page without nextCursor is the end. Limits: 1 to 100.
- `cursor` (optional) — `string`; The nextCursor of the previous page. Leave it out for the first page.

---

### `list_messages`

Read your conversation’s messages, oldest first. Keep going until there is no nextCursor. Use for: reading a conversation longer than the 100 messages get_conversation returns. Not for: who the conversation is with and whether you can send (get_conversation); finding a conversation (list_conversations). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: list_messages({"conversationId":"c7Rk2mQw9TzL4nXp","cursor":"eyJ2ZXJzaW9uIjoxfQ.5f1c0a9e"}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `conversationId` (required) — `string`; The conversation id, from list_conversations or the conversationId of a hire. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.
- `limit` (optional) — `integer`; Rows wanted. A page can hold fewer, or none; only a page without nextCursor is the end. Limits: 1 to 200.
- `cursor` (optional) — `string`; The nextCursor of the previous page. Leave it out for the first page.

---

### `list_preferred_humans`

Everyone you marked as preferred, newest first, with your note. Use for: finding people you liked working with before you post or hire. Not for: taking someone off the list (unprefer_human); people you blocked (list_blocked_humans). Needs: an API key. Hosted sign-in cannot call this yet. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: list_preferred_humans({}) Errors: account_setup_required; each error carries `fix`: what to do next.

**Parameters:**

None

---

### `list_qa_runs`

List your QA runs, newest first. Send templateId to filter by template. Use for: finding a QA run or its report status. Not for: reading one run’s findings and what each tester sent (get_qa_run). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: list_qa_runs({"templateId":"qa_tpl_4Rk9xW2"}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `templateId` (optional) — `string`; The template id the QA template was created with. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.

---

### `list_reviews`

Read the reviews of one person, newest first, with who wrote each and whether the job was paid. An unknown id gives an empty list. Use for: checking someone’s track record before you hire them. Not for: reading their profile (get_human). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: list_reviews({"humanId":"h2Lw9QxT4mZp7Rk","limit":50}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `humanId` (required) — `string`; The id from list_humans. A username does not work here. Limits: 1 to 200 characters.
- `limit` (optional) — `integer`; Rows wanted. A page can hold fewer, or none; only a page without nextCursor is the end. Limits: 1 to 100.
- `cursor` (optional) — `string`; The nextCursor of the previous page. Leave it out for the first page.

---

### `list_submissions`

List work on one bounty, newest record created first. Continue until there is no nextCursor, even after a short page. Restart to see new work. Use for: finding the work that waits for your review on one bounty. Not for: reading one piece of work in full, with files (get_hire); listing every worker and their money (list_hires). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: list_submissions({"bountyId":"b7Kq2mXw9TzR4nLp","status":"pending_review"}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `bountyId` (required) — `string`; The bounty id, or a pasted rentahuman.ai/bounties/... link.
- `status` (optional) — `"pending_review" | "approved" | "redo_requested" | "rejected"`; Only submissions in this status. pending_review is the work that waits for you. Default: every submission.
- `limit` (optional) — `integer`; Rows wanted. A page can hold fewer, or none; only a page without nextCursor is the end. Limits: 1 to 100.
- `cursor` (optional) — `string`; The nextCursor of the previous page. Leave it out for the first page.

---

### `list_taste_runs`

List your preference polls (taste runs), newest first. Continue until there is no nextCursor, even after a short page. New runs shift pages; restart for fresh results. Use for: finding your preference polls and their status. Not for: reading one run’s votes, tally and report (get_taste_run); listing QA runs (list_qa_runs). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: list_taste_runs({"limit":20}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `limit` (optional) — `integer`; Rows wanted. A page can hold fewer, or none; only a page without nextCursor is the end. Limits: 1 to 100.
- `cursor` (optional) — `string`; The nextCursor of the previous page. Leave it out for the first page.

---

### `list_wallet_transactions`

List every movement of money in and out of your wallet, newest first: money added, refunds, bounty funding, and sends paid from the wallet with the worker, their pay and our fee. A send paid by card never moves the wallet, so it is not listed. Keep going until a page has no `nextCursor`. Use for: reading what came in and went out of your wallet, and what each send paid from it cost. Not for: your balance and limits (get_wallet); money held on a hire (list_hires). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: list_wallet_transactions({"limit":2}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `limit` (optional) — `integer`; Rows wanted. A page can hold fewer, or none; only a page without nextCursor is the end. Limits: 1 to 100.
- `cursor` (optional) — `string`; The nextCursor of the previous page. Leave it out for the first page.

---

### `list_webhook_deliveries`

List queued and sent events for your endpoints, newest first among those read, with each delivery’s status. There is no next page, and with many stored deliveries the newest may be missing: narrow with endpointId, eventType or status. Use for: checking queued and sent events, and finding deliveries that failed. Not for: reading one delivery with its body and tries (get_webhook_delivery); seeing your endpoints (list_webhook_endpoints). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: list_webhook_deliveries({"endpointId":"Wk3pQ8vN1sXr6TzL0aBc","status":"delivered","limit":20}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `endpointId` (optional) — `string`; Only deliveries to this endpoint. An id that is not yours gives an empty list. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.
- `eventType` (optional) — `"application.submitted" | "application.accepted" | "application.confirmed" | "application.rejected" | "application.seat_expired" | "application.ghost_flagged" | "application.started" | "application.start_deadline_passed" | "application.completion_deadline_passed" | "submission.submitted" | "submission.approved" | "submission.redo_requested" | "submission.rejected" | "submission.redo_deadline_passed" | "message.received" | "conversation.completion_claimed" | "proof.uploaded" | "bounty.seat_filled" | "bounty.completed" | "escrow.funded" | "escrow.released" | "payment.sent" | "wallet.low_balance" | "wallet.spending_cap_hit" | "run.status_changed" | "run.report_ready" | "webhook.test"`; Only deliveries of this event type. Leave out for all event types.
- `status` (optional) — `"pending" | "claimed" | "delivered" | "retry" | "failed"`; pending: waiting to be sent. claimed: being sent now. delivered: your URL answered 2xx. retry: it failed and will be sent again. failed: no more tries.
- `limit` (optional) — `integer`; Most deliveries wanted. There is no next page. Limits: 1 to 200.

---

### `list_webhook_endpoints`

List every webhook endpoint you registered, newest first, with its events and whether deliveries work. At most 5 exist, so it is one page. The signing secret is never listed. Use for: seeing where your events go, and finding an endpoint that was switched off after failures. Not for: adding an endpoint (create_webhook_endpoint); seeing what was sent to an endpoint (list_webhook_deliveries). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: list_webhook_endpoints({}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

None

---

### `open_dispute`

Hold a hire's pay and ask the platform to settle it, when the work was not done or not as agreed. Use for: work not done, or not as agreed, on a hire whose pay is held. Pay stays held until the platform settles or dismisses the dispute. Use the paying account. Payments in progress can block opening. Listed actions can be refused; hires awaiting worker confirmation may still be disputed. Most accounts get 3 attempts hourly. Needs: an API key. Hosted sign-in cannot call this yet. Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: open_dispute({"hireId":"a3Fh8kQz1WpL0mNc","category":"not_delivered","description":"The worker confirmed the job and never went to the shops. Nothing was sent by the due time.","urls":["https://storage.example/chat-screenshot.png"]}) Repeat: Once this has worked, a repeat does not do it again while that result still stands: it is refused, or answers with what is already there. Errors: no_held_pay, not_disputable, paying_account_required, payment_being_reconciled, dispute_opened_reply_failed, dispute_open_outcome_unknown; each error carries `fix`: what to do next.

**Parameters:**

- `hireId` (required) — `string`; The hire id, from list_hires or accept_application. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.
- `category` (required) — `"not_delivered" | "poor_quality" | "not_as_described" | "communication_issue" | "fraud" | "other"`; The kind of problem. There is no default.
- `description` (required) — `string`; What went wrong, in your own words: 20 to 2000 characters, not counting spaces at the ends. The platform reads it when it settles the dispute. Limits: matches `^\s*\S[\s\S]{18,1998}\S\s*$`.
- `urls` (optional) — `string[]`; Up to 10 https links to what shows the problem, each up to 2048 characters. Default: no links. Limits: at most 10 items, each item at most 2048 characters and matches `^https:\/\/\S+$`.

---

### `pay_hire`

Release the held pay of a hire to the worker. Final. Paying approves the work that waits for review. Use for: paying a worker whose pay is held and whose submitted work you accept. The work is checked once, when the call starts. The reply says what this call released and where the hire stands; get_hire shows the whole hire. Not for: asking for fixes (request_redo); refusing the work (reject_submission). Needs: an API key. Hosted sign-in cannot call this yet. Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: pay_hire({"hireId":"a3Fh8kQz1WpL0mNc","submissionId":"s_7Hd2kQ"}) Repeat: Once this has worked, a repeat does not do it again while that result still stands: it is refused, or answers with what is already there. Errors: not_payable, pay_later_not_supported, hire_kind_not_supported, bonus_decisions_required, bonus_decisions_saved, payment_sent_finishing; each error carries `fix`: what to do next.

**Parameters:**

- `hireId` (required) — `string`; The hire id, from list_hires or accept_application. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.
- `submissionId` (optional) — `string`; The submission you pay for: `submission.id` of the hire, from get_hire. When sent, the call is refused if the hire now shows another submission. Default: not checked. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.
- `bonuses` (optional) — `object[]`; Your decision on each bonus of a hire whose bonuses are still to decide. `bonus` in the reply is the bonus money this call released, and get_hire lists the decisions that stand in `submission.review.bonuses`. Default: none.
- `bonuses[].bonusId` — `string`; Required in `bonuses[]`. Use bonusId from get_hire submission.bonusClaims or id from get_bounty bonuses. Choose a bonus funded for this hire. Limits: at least 1 character.
- `bonuses[].earnedUnits` — `integer`; Required in `bonuses[]`. Whole items earned, from 0 to claimedUnits; for an unclaimed bonus, from 0 to maxUnits. Limits: at least 0.
- `bonuses[].reason` — `string`; Optional. Why you chose this count. Up to 500 characters after trimming. Leave out for no reason.

---

### `pick_photos`

Keep or drop single photos in a photo submission: send keep or drop, one of them per call; to do both, make two calls. An id that is not a photo of this hire is left alone. This sorts photos only; it does not approve the work, refuse it or pay. Use for: choosing the photos you want from a photo submission, before you download them with download_picked_photos. Not for: approving the work and paying (pay_hire); refusing the whole submission (reject_submission). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: pick_photos({"hireId":"a3Fh8kQz1WpL0mNc","keep":["0f3c9a7e21b45d6e8a90","1b7d2e4f6a8c0e2a4b6c"]}) Repeat: A repeat may act again on the thing as it stands then. Read it first. Errors: no_submission, no_photo_submission, not_in_review; each error carries `fix`: what to do next.

**Parameters:**

- `hireId` (required) — `string`; The hire id, from list_hires or accept_application. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.
- `keep` (optional) — `string[]`; Ids of photos to keep, from list_hire_photos. Up to 400. Leave it out or empty when you send drop. Limits: at most 400 items, each item at least 1 character.
- `drop` (optional) — `string[]`; Ids of photos to drop, from list_hire_photos. Up to 400. Leave it out or empty when you send keep. Limits: at most 400 items, each item at least 1 character.

---

### `prefer_human`

Mark one person as someone you like to work with. Preferring also takes them off your blocked list. Preferring again only replaces the note. Use for: keeping a list of people you want to hire again. Not for: taking them off the list (unprefer_human); seeing who you prefer (list_preferred_humans). Needs: an API key. Hosted sign-in cannot call this yet. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: prefer_human({"humanId":"h2Lw9QxT4mZp7Rk","note":"Fast, clear photos"}) Repeat: A repeat with the same input, and the same key if you sent one, does not act twice: it returns the same result, finishes the first call, or is refused. Errors: not_found, list_full, account_setup_required; each error carries `fix`: what to do next.

**Parameters:**

- `humanId` (required) — `string`; The human id, as `id` in list_humans. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.
- `note` (optional) — `string`; Why you prefer them, for your own list. They never see it. Up to 280 characters. Left out: none, and a repeat without one clears the earlier one. Limits: at most 280 characters.

---

### `reject_application`

Turn down one pending application. The applicant is told, with your message if you give one. Use for: saying no to one applicant. The reply says where the application now stands; get_application shows all of it. Not for: ending a hire you already accepted (cancel_hire). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: reject_application({"applicationId":"a3Vn8cQe1RuY6wHs","message":"Thanks, we chose someone closer to the shops."}) Repeat: Once this has worked, a repeat does not do it again while that result still stands: it is refused, or answers with what is already there. Errors: application_not_pending; each error carries `fix`: what to do next.

**Parameters:**

- `applicationId` (required) — `string`; The application id. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.
- `message` (optional) — `string`; What the applicant reads with the rejection. Up to 1000 characters. Default: no message of yours; the applicant then reads a general sentence. Limits: at most 1000 characters, matches `\S`.

---

### `reject_submission`

Refuse the submitted work. Final. No money moves at this call: it opens the time in which the worker may appeal. Use for: submitted work that does not meet the bounty and cannot be fixed. `submission.appealDueAt` in the reply shows until when the worker may appeal. The held pay stays held at this call. Not for: fixable work (request_redo); work never submitted (cancel_hire); a problem the platform should settle (open_dispute). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: reject_submission({"hireId":"a3Fh8kQz1WpL0mNc","submissionId":"s_7Hd2kQ","message":"These are photos of another street."}) Repeat: Once this has worked, a repeat does not do it again while that result still stands: it is refused, or answers with what is already there. Errors: no_submission, not_reviewable, hire_kind_not_supported, redo_deadline_pending, rejection_unavailable; each error carries `fix`: what to do next.

**Parameters:**

- `hireId` (required) — `string`; The hire id, from list_hires or accept_application. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.
- `submissionId` (optional) — `string`; The submission you decide on: `submission.id` of the hire, from get_hire. When sent, the call is refused if the hire now shows another submission. Default: the submission the hire shows now. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.
- `message` (required) — `string`; What you tell the worker, 1 to 1000 characters. Limits: at most 1000 characters, matches `\S`.

---

### `report_support_issue`

File a report in the support team's queue under your account, with your name and email attached for the team. No email is sent to you. Use for: a platform failure, an unexpected reply, a billing question, or anything you cannot solve yourself. Each call files a new report, so send one once. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: report_support_issue({"summary":"pay_hire answered internal_error twice","description":"I called pay_hire for hire h4Tq9 at 14:02 and 14:05 UTC. Both answered internal_error and get_hire still shows the hire as submitted.","category":"billing","priority":"high","errorCode":"internal_error","sourceTool":"pay_hire"}) Repeat: A repeat may act again on the thing as it stands then. Read it first. Errors: report_refused; each error carries `fix`: what to do next.

**Parameters:**

- `summary` (required) — `string`; One line on what went wrong. At most 160. Limits: at most 160 characters, matches `\S`.
- `description` (required) — `string`; What you did, what you expected, what happened instead. At most 5,000. Limits: at most 5000 characters, matches `\S`.
- `category` (optional) — `"bug" | "feature_request" | "improvement" | "ui_ux" | "performance" | "billing" | "content" | "other"`; Left out: bug.
- `priority` (optional) — `"low" | "medium" | "high" | "urgent"`; How urgent it is for you. Left out: none.
- `errorCode` (optional) — `string`; The error code or exception name you got. At most 200. Limits: at most 200 characters, matches `\S`.
- `sourceTool` (optional) — `string`; The tool or workflow where it happened. At most 100. Limits: at most 100 characters, matches `^[A-Za-z0-9][A-Za-z0-9._/-]*$`.

---

### `request_redo`

Ask the worker to fix and resend their work. No money moves. At most 3 times per hire. Use for: submitted work that waits for your review and can be fixed. The worker hands the fixed work in under the same submission id, so check `submission.status` with get_hire before you decide again. Not for: accepting the work (pay_hire); refusing the work for good (reject_submission). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: request_redo({"hireId":"a3Fh8kQz1WpL0mNc","submissionId":"s_7Hd2kQ","message":"Shop 3 is out of focus. Please retake it.","redoDueAt":"2026-11-22T15:00:00.000Z"}) Repeat: Once this has worked, a repeat does not do it again while that result still stands: it is refused, or answers with what is already there. Errors: no_submission, not_reviewable, hire_kind_not_supported, redo_limit_reached; each error carries `fix`: what to do next.

**Parameters:**

- `hireId` (required) — `string`; The hire id, from list_hires or accept_application. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.
- `submissionId` (optional) — `string`; The submission you decide on: `submission.id` of the hire, from get_hire. When sent, the call is refused if the hire now shows another submission. Default: the submission the hire shows now. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.
- `message` (required) — `string`; What you tell the worker, 1 to 1000 characters. Limits: at most 1000 characters, matches `\S`.
- `redoDueAt` (optional) — `string`; When the fixed work is due: 15 minutes to 7 days from now. With no deadline, reject_submission waits for the next hand-in. Limits: matches `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$`.

---

### `revoke_api_key`

Turn one of your API keys off for good. A key can revoke itself; then the next call with it fails. Use for: a key that leaked or is no longer needed. Calls with it are refused from then on. Not for: finding the id of a key (list_api_keys); a replacement key (create_api_key). Needs: an API key. Hosted sign-in cannot call this yet. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: revoke_api_key({"keyId":"Xc81kLm2PqRs9TuvWx0Y"}) Repeat: Once this has worked, a repeat does not do it again while that result still stands: it is refused, or answers with what is already there. Errors: already_revoked; each error carries `fix`: what to do next.

**Parameters:**

- `keyId` (required) — `string`; The id of the key, from list_api_keys. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.

---

### `search_bounties`

Search the open bounties anyone on the site posted, as the public bounty list shows them: featured first, then newest. Use it to find work to apply to, or to see how other people write a bounty (title, description, pay, requirements) before you post your own. A page can hold fewer rows than `limit`, or none; keep going with the same filters until a page has no `nextCursor`. Paging is not guaranteed to reach every match: with a narrow filter it can end before older matching bounties. Not listed: a bounty priced in another currency. Use for: finding open bounties to apply to, or examples to learn from before you post a bounty. Not for: listing the bounties you posted (list_bounties); posting a bounty (create_bounty). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: search_bounties({"skill":"photography","limit":20}) Errors: only the common ones; each error carries `fix`: what to do next.

**Parameters:**

- `skill` (optional) — `string`; Only bounties with a skill that contains this text. Limits: 1 to 200 characters.
- `category` (optional) — `string`; A category slug, such as research or labor-gigs. Limits: 1 to 100 characters.
- `limit` (optional) — `integer`; Rows wanted. A page can hold fewer, or none; only a page without nextCursor is the end. Limits: 1 to 100.
- `cursor` (optional) — `string`; The nextCursor of the previous page. Leave it out for the first page.

---

### `send_cake`

Order a decorated cake delivered to a company, paid from your wallet. Send an idempotencyKey of at most 200 characters. Use for: a cake for a company address. The wallet is charged before the vendor gets the order. The same idempotencyKey answers for the first order as it now stands, ignores new input, and never charges twice. Not for: adding money to your wallet (fund_wallet). Needs: an API key. Hosted sign-in cannot call this yet. Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: send_cake({"recipient":{"company":"Acme Robotics","contactName":"Ada Lovelace","address":"1 Market St","address2":"Floor 4","city":"San Francisco","state":"CA","zip":"94105"},"cakeSize":"8in","design":{"messageText":"Congrats on the launch!"},"cardMessage":"From your friends at Northwind","idempotencyKey":"5f0c7a2e-8d4b-4e1a-9c3f-2b6d1e8a7f40"}) Key: the idempotencyKey in the example is a sample. Replace it with a new unique key for each new call, and keep that key for the call’s retries and any confirmation it asks for. Repeat: A repeat with the same input, and the same key if you sent one, does not act twice: it returns the same result, finishes the first call, or is refused. Errors: wallet_short, spending_limit_reached, not_deliverable, order_unavailable, design_too_large, order_refused, account_setup_required, internal_error; each error carries `fix`: what to do next.

**Parameters:**

- `recipient` (required) — `object`; A company. Send websiteUrl, or all of address, city, state and zip.
- `recipient.company` (required) — `string`; Limits: 1 to 300 characters, matches `\S`.
- `recipient.contactName` (required) — `string`; Who the courier asks for. Limits: 1 to 300 characters, matches `\S`.
- `recipient.address` — `string`; Optional. Limits: 1 to 500 characters, matches `\S`.
- `recipient.address2` — `string`; Optional. Suite or floor. Limits: 1 to 500 characters, matches `\S`.
- `recipient.city` — `string`; Optional. Limits: 1 to 200 characters, matches `\S`.
- `recipient.state` — `string`; Optional. Limits: 1 to 100 characters, matches `\S`.
- `recipient.zip` — `string`; Optional. Limits: 1 to 20 characters, matches `\S`.
- `recipient.websiteUrl` — `string`; Optional. The company's website, instead of an address. Limits: 1 to 2000 characters, matches `^https?:\/\/`, matches `\S`.
- `recipient.phone` — `string`; Optional. Limits: 1 to 40 characters, matches `^\+?[0-9() .-]+$`, matches `\S`.
- `recipient.notes` — `string`; Optional. For the courier. Limits: 1 to 500 characters, matches `\S`.
- `recipient.deliveryDate` — `string`; Optional. YYYY-MM-DD. Limits: matches `^\d{4}-\d{2}-\d{2}$`.
- `cakeSize` (required) — `"6in" | "8in" | "10in" | "12in" | "half_sheet" | "sheet"`
- `cakeShape` (optional) — `"round" | "square"`
- `design` (required) — `object`; Exactly one of messageText, imageSvg, imageUrl or imageBase64. A large image goes by imageUrl.
- `design.messageText` — `string`; Optional. Words written on the cake. Limits: 1 to 2000 characters, matches `\S`.
- `design.imageSvg` — `string`; Optional. Limits: 1 to 2000000 characters, matches `\S`.
- `design.imageUrl` — `string`; Optional. Limits: 1 to 2000 characters, matches `^https?:\/\/`, matches `\S`.
- `design.imageBase64` — `string`; Optional. Limits: 1 to 8000000 characters, matches `\S`.
- `design.imageMime` — `"image/png" | "image/jpeg" | "image/webp"`; Optional. Only with imageBase64.
- `cardMessage` (optional) — `string`; A card that goes with the cake. Limits: 1 to 2000 characters, matches `\S`.
- `metadata` (optional) — `object`; Your own labels, up to 28 keys, passed to the vendor.
- `idempotencyKey` (required) — `string`; A unique string for this call. Repeat it when you retry, so the call runs once.

---

### `send_message`

Send a text message to the worker in a conversation you are part of. Use for: writing to an applicant or a hired worker. Send an idempotencyKey: the same key with the same conversation and text sends once and answers with that message. Without a key, a repeat sends a second message. Not for: opening chat with an applicant you have not hired (accept_application). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: send_message({"conversationId":"c4Rt7nWq2ZxL9pKs","content":"Hi Dana, the side door is open from 9."}) Repeat: A repeat may act again on the thing as it stands then. Read it first. Errors: conversation_closed, hire_required, message_refused, account_restricted, send_in_progress; each error carries `fix`: what to do next.

**Parameters:**

- `conversationId` (required) — `string`; The conversation id, as on the hire or the application. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.
- `content` (required) — `string`; The text to send, up to 40000 characters. Text only. Limits: at most 40000 characters, matches `\S`.
- `idempotencyKey` (optional) — `string`; A unique string for this call. Repeat it when you retry, so the call runs once.

---

### `send_money`

Send a tip or a reimbursement to a worker on a bounty you own, after their work on it was released. Paid from your wallet when it covers the total. Send an idempotencyKey. Use for: a tip or an expense after the work is paid. With an idempotencyKey a repeat sends once. Without one, a repeat can send again, and a short wallet gets a card pay link. Not for: adding money to your wallet (fund_wallet); paying for a draft bounty (fund_bounty). Needs: an API key. Hosted sign-in cannot call this yet. Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: send_money({"bountyId":"b7Kq2mXw9TzR4nLp","workerId":"h3Jm8QwLp2Vx","pay":{"amount":1500,"currency":"usd"},"note":"Parking"}) Repeat: A repeat may act again on the thing as it stands then. Read it first. Errors: wallet_short, payment_already_open, work_not_released, amount_over_limit, worker_blocked, worker_cannot_receive, spending_limit_reached, account_restricted, account_setup_required, idempotency_key_reused; each error carries `fix`: what to do next.

**Parameters:**

- `bountyId` (required) — `string`; The bounty this worker was hired and paid on: a send always belongs to one, as on the website, where money is sent from the chat about that bounty. If you do not know it, list_conversations shows the bountyId of each chat with a worker.
- `workerId` (required) — `string`; The worker's profile id, as on their hire. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.
- `pay` (required) — `object`; What the worker gets, from $0.50 to $10,000. Our fee is added on top.
- `pay.amount` (required) — `integer`; Limits: 50 to 1000000.
- `pay.currency` (required) — `"usd"`
- `note` (optional) — `string`; A memo for the worker, up to 500 characters. Limits: at most 500 characters.
- `override` (optional) — `boolean`; true sends although you blocked this worker. Default false.
- `idempotencyKey` (optional) — `string`; A unique string for this call. Repeat it when you retry, so the call runs once.

---

### `set_wallet_controls`

Set or turn off your low-balance alert and your two spending caps. A limit you leave out is not changed. Use for: capping what your wallet pays per bounty or per 24 hours, and choosing when you get a low-balance email. Moves no money. Not for: reading your limits and balance (get_wallet); adding money to your wallet (fund_wallet). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: set_wallet_controls({"spendingCapPer24h":{"amount":50000,"currency":"usd"},"lowBalanceAlertAt":null}) Repeat: A repeat with the same input, and the same key if you sent one, does not act twice: it returns the same result, finishes the first call, or is refused. Errors: account_setup_required; each error carries `fix`: what to do next.

**Parameters:**

- `lowBalanceAlertAt` (optional) — `object | null`; You get an email when your balance falls below this. From 0 to $100,000. Null turns it off. Left out: not changed.
- `lowBalanceAlertAt.amount` — `integer`; Required in `lowBalanceAlertAt`. Limits: 0 to 10000000.
- `lowBalanceAlertAt.currency` — `"usd"`; Required in `lowBalanceAlertAt`.
- `spendingCapPerBounty` (optional) — `object | null`; The most your wallet funds for one bounty’s hires and prepaid spots; excludes tips and reimbursements. From 0 to $100,000. Null turns it off. Left out: not changed.
- `spendingCapPerBounty.amount` — `integer`; Required in `spendingCapPerBounty`. Limits: 0 to 10000000.
- `spendingCapPerBounty.currency` — `"usd"`; Required in `spendingCapPerBounty`.
- `spendingCapPer24h` (optional) — `object | null`; The most your wallet pays in any 24 hours. From 0 to $100,000. Null turns it off. Left out: not changed.
- `spendingCapPer24h.amount` — `integer`; Required in `spendingCapPer24h`. Limits: 0 to 10000000.
- `spendingCapPer24h.currency` — `"usd"`; Required in `spendingCapPer24h`.

---

### `stop_qa_run`

Stop a QA run you started. Applicants not yet accepted are turned down; accepted testers are told and may finish. Its schedule keeps going, and no tool stops a schedule. Use for: ending one QA run early. Unused money returns immediately only without assigned work, completed work or paid results; otherwise it returns when the run closes. A stopped run cannot restart. Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: stop_qa_run({"runId":"qr_7Kq2mXw9TzR4nLp"}) Repeat: A repeat with the same input, and the same key if you sent one, does not act twice: it returns the same result, finishes the first call, or is refused. Errors: not_stoppable, run_busy; each error carries `fix`: what to do next.

**Parameters:**

- `runId` (required) — `string`; The QA run id. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.

---

### `test_webhook_endpoint`

Send one signed webhook.test event to one of your endpoints. The reply comes once the event is queued, not once your URL answers. A failed test counts toward switching the endpoint off, like a real event. Use for: checking that your URL receives events and checks their signature, right after creating an endpoint. Not for: reading whether the test arrived (get_webhook_delivery). Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: test_webhook_endpoint({"endpointId":"Wk3pQ8vN1sXr6TzL0aBc"}) Repeat: A repeat may act again on the thing as it stands then. Read it first. Errors: endpoint_disabled; each error carries `fix`: what to do next.

**Parameters:**

- `endpointId` (required) — `string`; The webhook endpoint id. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.

---

### `unblock_human`

Take one person off your blocked list, so they can apply to your bounties again. Does not add them to your preferred list. Use for: undoing block_human. Not for: seeing who you blocked (list_blocked_humans). Needs: an API key. Hosted sign-in cannot call this yet. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: unblock_human({"humanId":"h2Lw9QxT4mZp7Rk"}) Repeat: A repeat with the same input, and the same key if you sent one, does not act twice: it returns the same result, finishes the first call, or is refused. Errors: account_setup_required; each error carries `fix`: what to do next.

**Parameters:**

- `humanId` (required) — `string`; The human id, as `id` in list_humans. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.

---

### `unprefer_human`

Take one person off your preferred list. Does not block them. Use for: undoing prefer_human. Not for: seeing who you prefer (list_preferred_humans). Needs: an API key. Hosted sign-in cannot call this yet. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: unprefer_human({"humanId":"h2Lw9QxT4mZp7Rk"}) Repeat: A repeat with the same input, and the same key if you sent one, does not act twice: it returns the same result, finishes the first call, or is refused. Errors: account_setup_required; each error carries `fix`: what to do next.

**Parameters:**

- `humanId` (required) — `string`; The human id, as `id` in list_humans. Limits: matches `^[A-Za-z0-9_-]{1,200}$`.

---

### `update_bounty`

Change, pause or resume your bounty; omitted fields stay unchanged, and null clears only fields that accept null. Lists replace stored lists: copy them whole from get_bounty. Use for: changing a bounty's details or pay. When a wallet charge needs confirmation, resend the same edit with confirmCharge set to the quoted charge. One kind of raise can charge immediately: an eligible sponsored wallet pool, including with other detail edits; charge reports the debit. For card-funded raises that need payment approval, follow the returned payUrl (details.payUrl on a funding_short error). Not for: closing a bounty (cancel_bounty); paying for a draft (fund_bounty). Money: US cents. Replies omit a field's sole empty value. If null is allowed, only null is omitted; false, [] and a present group stay. A present empty group is {}. Field descriptions explain unavailable values. Example: update_bounty({"bountyId":"b7Kq2mXw9TzR4nLp","spots":{"total":4},"confirmCharge":{"amount":2359,"currency":"usd"}}) Repeat: Once this has worked, a repeat does not do it again while that result still stands: it is refused, or answers with what is already there. Errors: charge_confirmation_required, wallet_short, pay_locked, change_pay_alone, locked_after_hire, spots_below_filled, use_cancel_bounty, listing_refused, pay_below_minimum, not_editable, funding_short, bounty_changed, photos_not_available, screening_not_available; each error carries `fix`: what to do next.

**Parameters:**

- `bountyId` (required) — `string`; The bounty id, or a pasted rentahuman.ai/bounties/... link.
- `status` (optional) — `"open" | "paused" | "closed"`; paused stops new applications; open resumes them. closed is refused: use cancel_bounty.
- `confirmCharge` (optional) — `object`; The charge of a charge_confirmation_required refusal.
- `confirmCharge.amount` — `integer`; Required in `confirmCharge`. Whole US cents.
- `confirmCharge.currency` — `"usd"`; Required in `confirmCharge`.
- `title` (optional) — `string`; Limits: 5 to 200 characters.
- `description` (optional) — `string`; Limits: 20 to 5000 characters.
- `category` (optional) — `"computer-gigs" | "creative-gigs" | "crew-gigs" | "domestic-gigs" | "event-gigs" | "labor-gigs" | "talent-gigs" | "writing-gigs"`; The kind of work, as in the website’s category picker. Default: unchanged.
- `skills` (optional) — `string[]`
- `requirements` (optional) — `string[]`
- `imageUrls` (optional) — `string[]`; Limits: at most 5 items.
- `location` (optional) — `object`; Replaces the whole location: send every field, null for none.
- `location.city` — `string | null`; Required in `location`.
- `location.state` — `string | null`; Required in `location`.
- `location.country` — `string | null`; Required in `location`.
- `location.isRemoteAllowed` — `boolean`; Required in `location`.
- `countries` (optional) — `object`
- `countries.allowed` — `string[]`; Optional. Only workers in these countries may apply.
- `countries.hidden` — `string[]`; Optional. The bounty is hidden in these countries.
- `pay` (optional) — `object`
- `pay.type` — `"fixed" | "hourly"`; Optional.
- `pay.amount` — `integer`; Optional. What one worker receives for one spot (per hour when hourly), in whole US cents. Limits: 100 to 100000000.
- `pay.estimatedHours` — `number`; Optional. Hours of work for one spot, at least 5/60. Limits: at least 0.08333333333333333.
- `spots` (optional) — `object`
- `spots.total` — `integer`; Required in `spots`. Spots to pay for. Limits: 1 to 2000.
- `timeZone` (optional) — `string`; IANA time zone for startsAt and every shift of schedule.
- `startsAt` (optional) — `string | null`; ISO 8601 timestamp with a UTC offset; a changed start must be in the future. Null clears it.
- `schedule` (optional) — `object | null`
- `schedule.shifts` — `object[]`; Required in `schedule`.
- `schedule.shifts[].date` — `string`; Required in `schedule.shifts[]`. Local date, YYYY-MM-DD.
- `schedule.shifts[].start` — `string`; Required in `schedule.shifts[]`. Local time, HH:mm, in timeZone.
- `schedule.shifts[].end` — `string`; Required in `schedule.shifts[]`. Local time, HH:mm, in timeZone.
- `timers` (optional) — `object`
- `timers.start` — `object | null`; Optional. Null disables the start timer. Unused on a bounty with a schedule.
- `timers.start.minutes` — `integer`; Required in `timers.start`. Minutes a hired worker has to start. Limits: 5 to 1440.
- `timers.response` — `object | null`; Optional.
- `timers.response.hours` — `number`; Required in `timers.response`. Limits: 1 to 720.
- `timers.response.releasesSpot` — `boolean`; Optional.
- `applications` (optional) — `object`
- `applications.closesAt` — `string`; Optional.
- `applications.keepPendingWhenFull` — `boolean`; Optional.
- `applications.questions` — `object[]`; Optional.
- `applications.questions[].id` — `string`; Optional.
- `applications.questions[].type` — `"text" | "checkbox" | "file_upload" | "live_video"`; Required in `applications.questions[]`.
- `applications.questions[].label` — `string`; Required in `applications.questions[]`.
- `applications.questions[].description` — `string`; Optional.
- `applications.questions[].isRequired` — `boolean`; Optional. Default false. A live_video question is always required: false is refused.
- `applications.questions[].maxLength` — `integer`; Optional.
- `applications.questions[].allowedFileTypes` — `("image" | "docx" | "pdf" | "txt" | "video" | "audio")[]`; Optional.
- `applications.questions[].maxFiles` — `integer`; Optional.
- `applications.links` — `object[]`; Optional.
- `applications.links[].type` — `"linkedin" | "instagram" | "twitter" | "github" | "resume" | "portfolio" | "custom"`; Required in `applications.links[]`.
- `applications.links[].label` — `string`; Optional.
- `applications.upload` — `object`; Optional.
- `applications.upload.type` — `"photo" | "video" | "document"`; Required in `applications.upload`.
- `applications.upload.max` — `integer`; Optional.
- `applications.upload.minimumResolutionPx` — `integer`; Optional. Photo uploads only.
- `applications.upload.acceptText` — `string`; Optional.
- `applications.upload.consentText` — `string`; Required in `applications.upload`.
- `applications.upload.confirmationMessage` — `string`; Required in `applications.upload`.
- `checks` (optional) — `object`
- `checks.identity` — `boolean`; Optional.
- `checks.linkedin` — `boolean`; Optional.
- `checks.app` — `"ios" | "android" | "any" | null`; Optional.
- `checks.mic` — `object | null`; Optional.
- `checks.mic.minScore` — `number`; Optional. Limits: 1 to 5.
- `checks.language` — `object | null`; Optional.
- `checks.language.language` — `"en"`; Required in `checks.language`.
- `checks.language.minimumCefr` — `"A2" | "B1" | "B2" | "C1" | "C2"`; Required in `checks.language`.
- `checks.nativeLanguage` — `object | null`; Optional.
- `checks.nativeLanguage.language` — `"yue" | "cmn" | "tr"`; Required in `checks.nativeLanguage`. Native language: yue Cantonese, cmn Mandarin, tr Turkish.
- `checks.excludeWorkersFromBountyIds` — `string[]`; Optional.
- `proof` (optional) — `object`
- `proof.criteria` — `string`; Optional. What the worker must accomplish; 10 to 2,000 characters after trimming.
- `proof.types` — `("text" | "photo" | "video" | "link" | "document")[]`; Optional. Limits: at least 1 item.
- `proof.details` — `string`; Optional. Extra evidence rules; up to 2,000 characters after trimming.
- `proof.questions` — `object[]`; Optional.
- `proof.questions[].id` — `string`; Optional.
- `proof.questions[].prompt` — `string`; Required in `proof.questions[]`.
- `proof.questions[].isRequired` — `boolean`; Optional. Default true.
- `proof.liveCapture` — `"photo" | "video" | null`; Optional.
- `proof.photos` — `object | null`; Optional. Refused with photos_not_available unless your account has photo capture; plain photo proof uses proof.types: ["photo"].
- `proof.photos.criteria` — `string`; Required in `proof.photos`.
- `proof.photos.subject` — `string`; Optional.
- `proof.photos.minImages` — `integer`; Required in `proof.photos`.
- `proof.photos.maxImages` — `integer`; Required in `proof.photos`.
- `proof.photos.orientation` — `"any" | "portrait" | "landscape"`; Optional.
- `proof.photos.qualityNotes` — `string`; Optional.
- `proof.photos.area` — `object`; Optional.
- `proof.photos.area.lat` — `number`; Required in `proof.photos.area`.
- `proof.photos.area.lng` — `number`; Required in `proof.photos.area`.
- `proof.photos.area.radiusMeters` — `integer`; Required in `proof.photos.area`.
- `proof.photos.area.label` — `string`; Optional.
- `proof.checkIns` — `object | null`; Optional.
- `proof.checkIns.intervalMinutes` — `integer`; Required in `proof.checkIns`. Limits: 5 to 240.
- `proof.location` — `object`; Optional.
- `proof.location.radiusMeters` — `integer | null`; Optional. Metres from the geocoded city, state and country; no street address can be sent. Limits: 50 to 2000.
- `proof.location.isPreciseRequired` — `boolean`; Optional.
- `proof.location.termsVersion` — `"poster-precise-location-v1"`; Optional. Send it with isPreciseRequired true to accept the poster terms of precise location sharing.
- `bonuses` (optional) — `object[]`; Replaces all bonuses; [] clears them. Change bonuses separately from pay or spots.
- `bonuses[].title` — `string`; Required in `bonuses[]`.
- `bonuses[].condition` — `string`; Required in `bonuses[]`.
- `bonuses[].amount` — `integer`; Required in `bonuses[]`. Pay per earned item, in whole US cents.
- `bonuses[].maxUnits` — `integer`; Optional. Most items a worker can earn. Default 1.
- `ai` (optional) — `object`
- `ai.screening` — `boolean`; Optional.
- `ai.submissionReview` — `boolean`; Optional.
- `messages` (optional) — `object`; instructions can change alone. To change any on... message, send all five on... fields, copying unchanged messages from get_bounty.
- `messages.instructions` — `string`; Optional.
- `messages.onAccepted` — `string`; Optional.
- `messages.onRejected` — `string`; Optional.
- `messages.onSubmissionReceived` — `string`; Optional.
- `messages.onSubmissionApproved` — `string`; Optional.
- `messages.onSubmissionRejected` — `string`; Optional.

---

## Unchanged from version 4

These tools keep the inputs and replies they had in version 4, and they are in the npm package only. Their money fields: `book_sign_campaign` and `get_cake_status` give US cents in fields whose names end in `Cents` or `_cents`.

### `get_agent_identity`

Get your cryptographic agent identity. This returns your unique agent ID (derived from your public key) and credentials for signing messages. Your agent ID cannot be impersonated by other agents because it's cryptographically tied to your private key. Also shows which named identity is currently active. Call this first before sending messages in supported conversations.

**Parameters:**

None

---

### `list_identities`

List all your saved agent identities. Each identity has its own cryptographic keypair and agentId. Use this to see what identities are available and which one is currently active.

**Parameters:**

None

---

### `create_identity`

Create a new named agent identity. Each identity gets its own cryptographic keypair and unique agentId. Useful for maintaining separate identities for different purposes (e.g., 'personal', 'work', 'bot-name').

**Parameters:**

- `name` (required) — `string`; Name for the new identity (alphanumeric, underscores, hyphens only). Limits: 1 to 50 characters, matches `^[a-zA-Z0-9_-]+$`.

---

### `switch_identity`

Switch to a different named identity for this session. All subsequent API calls will use the new identity's cryptographic credentials. The identity must already exist (use create_identity first if needed).

**Parameters:**

- `name` (required) — `string`; Name of the identity to switch to. Limits: 1 to 50 characters, matches `^[a-zA-Z0-9_-]+$`.

---

### `delete_identity`

Delete a named identity. WARNING: This permanently removes the cryptographic keypair. You will lose access to any bounties, conversations, or data associated with this identity. Cannot delete the currently active identity.

**Parameters:**

- `name` (required) — `string`; Name of the identity to delete (cannot delete active identity). Limits: 1 to 50 characters, matches `^[a-zA-Z0-9_-]+$`.

---

### `book_sign_campaign`

Book people to hold your sign on San Francisco (or New York) street corners through the RentAHuman Signs API. Use this instead of create_bounty for any sign-holding, sign-spinning or human-billboard job: you give the design, we print it and handle pickup. Applicants are screened by AI, hired sign holders get a shift briefing and check-ins, and each holder is paid once RentAHuman ops or you approve their work. Requires RENTAHUMAN_API_KEY. Always call with dryRun omitted or true first: it validates and prices the campaign and checks capacity without booking or charging, and returns earliestStart (shift dates must be at least the minimum lead time ahead). Show the user the price and dates. Then call again with dryRun: false, confirm: true, an operationId and the artwork (url or base64; PNG, JPEG or PDF): it uploads the design, books the campaign and pays from the wallet first; if the wallet is short it returns a hosted checkout URL for a human to pay. Card details are never taken. Reuse the operationId to retry. Track the campaign at statusPath (GET).

**Parameters:**

- `dryRun` (optional) — `boolean`; Defaults to true: quote only. Pass false (with confirm: true) to book and pay.
- `confirm` (optional) — `boolean`; Required true for a live booking, which pays from the wallet first.
- `operationId` (optional) — `string`; Idempotency key and campaign ID (16-64 letters, digits, _ or -). Reuse it to retry a booking safely; a booked campaign is returned instead of booked twice. Limits: matches `^[A-Za-z0-9_-]{16,64}$`.
- `city` (optional) — `"sf" | "nyc"`
- `spots` (required) — `object[]`; One public-sidewalk point per sign holder, inside the city (max 20). Limits: 1 to 20 items.
- `spots[].lat` (required) — `number`
- `spots[].lng` (required) — `number`
- `spots[].label` (required) — `string`; Short corner name, e.g. "Powell & Market". Limits: 1 to 40 characters.
- `dates` (required) — `string[]`; Limits: at least 1 item, each item matches `^\d{4}-\d{2}-\d{2}$`.
- `startHour` (required) — `integer`
- `endHour` (required) — `integer`
- `signReturn` (optional) — `object`; Where the crew leaves the printed signs after the last day, and what to do.
- `signReturn.location` — `string`; Required in `signReturn`.
- `signReturn.instructions` — `string`; Required in `signReturn`.
- `specialInstructions` (optional) — `string`
- `laborCentsPerHour` (optional) — `integer`
- `artwork` (optional) — `object`; The sign design. Required to book; optional for a quote.
- `artwork.url` — `string`; Optional. Public https URL of the sign design. Give exactly one of url or base64. Limits: matches `^https:\/\/`.
- `artwork.base64` — `string`; Optional. The design file, base64-encoded. Give exactly one of url or base64. Limits: at least 1 character.
- `artwork.contentType` — `"image/png" | "image/jpeg" | "application/pdf"`; Required in `artwork`.
- `artwork.orientation` — `"portrait" | "landscape"`; Optional.

---

### `get_cake_status`

Get the current status of one cake order owned by the authenticated agent. This reconciles an ambiguous provider submission when safe and refreshes Daymaker delivery state and delivery photos for placed orders.

**Parameters:**

- `order_id` (required) — `string`; Limits: 1 to 100 characters, matches `^cake_[a-f0-9]{40}$`, matches `\S`.
