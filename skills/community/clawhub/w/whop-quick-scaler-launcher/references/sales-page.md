# Sales page

Use this module to prepare a Whop product page that lets a buyer understand the offer, inspect the product, see the full purchase terms, and reach the correct checkout. The structure is an operating recommendation, not a promise of higher conversion.

Reference check: 2026-09-29. This is independent guidance, not official Whop documentation. Examples are fictional and contain no customer data. Draft locally first. Creating a product, uploading public media, changing a live page, opening sales, or submitting to the marketplace each requires the appropriate owner approval.

## 1. Assemble the source pack

Before writing, obtain the approved offer, the actual deliverable or a faithful demonstration, pricing and access terms, and media with confirmed reuse rights. Match every source to the exact product. A testimonial about a coaching service does not prove the quality of a separate course.

Build a private claim register:

| Proposed claim | Required evidence | If evidence is missing |
|---|---|---|
| Contents and quantities | Inspect the actual files, lessons, or service scope | Remove the quantity or finish the missing content |
| Delivery and access | Verified delivery route and entitlement settings | Keep the page unpublished until the essential promise is settled |
| Billing, trial, and cancellation | Approved terms plus the exact checkout configuration | Ask for the unresolved commercial decision |
| Product sample | Actual included material or a clearly labeled demonstration | Do not redraw a fake sample |
| Review or result | Exact source, relevant product, date, context, and permission | Omit it; show the product instead |
| Limited availability | Actual stock or measured service capacity | Omit scarcity language |

Keep the register outside buyer-facing copy. Remove private names, contact details, transaction data, internal notes, credentials, and hidden document metadata from any public example or image. Do not carry private source paths into the page.

## 2. Map the page before filling the editor

| Surface | What the buyer should learn | What to put there |
|---|---|---|
| Product name | What is being sold | A descriptive product name |
| Headline | Which immediate job it helps with | One concrete benefit within the headline limit |
| First media item | What the product looks like | Recognizable cover, actual interface, or real deliverable |
| Description opening | Whether the offer fits their situation | Audience, problem, and delivered result |
| Contents or features | What they receive and how they use it | Specific deliverables paired with their use |
| Pricing and purchase area | What they pay and what happens next | Due-now amount, renewal if any, currency, tax wording, access period, and one main purchase action |
| Remaining gallery | Evidence of what is included | Readable excerpts and a truthful usage sequence |
| FAQ | Answers needed before purchase | Fit, delivery, access, billing, support, policies, and exclusions |

Whop's product-creation guide covers the name, headline, pricing, apps, media, description, features, and FAQs. The product reference separately describes the ordered gallery and purchase-button configuration. Use the fields actually supported by the current editor; do not assume a rich-text description can recreate every native component. [S1, S2]

A dedicated product page should make price and billing terms easy to find next to the purchase action. A general service homepage can introduce the practice before showing prices in offer sections. Do not copy the homepage layout into a purchase page and leave the buyer searching for the amount.

## 3. Write a headline of no more than 80 characters

Whop's current Create a Product guide specifies an 80-character maximum for the headline. Count spaces and punctuation. Older indexed guidance can conflict with the current page; use the stricter current limit and confirm acceptance in the active editor. [S1, checked 2026-09-29]

A useful starting pattern is:

```text
[DO THE BUYER'S JOB] with [THE CONCRETE DELIVERABLE OR METHOD]
```

Fictional examples, counted including spaces:

| Headline | Characters |
|---|---:|
| Turn scattered launch notes into a ready-to-use course outline | 62 |
| Plan, write and review your next newsletter with a repeatable workflow | 70 |
| Prepare your next coaching session with a focused action plan | 61 |

These describe intended use. They are not evidence of guaranteed results. Do not add unverified earnings, rankings, time savings, professional credentials, or a deadline the seller cannot control.

For a local character check:

```js
const headline = "Turn scattered launch notes into a ready-to-use course outline";
const count = [...headline].length;
console.log({ count, withinLimit: count <= 80 });
```

This counts Unicode code points. The editor or API may count complex emoji differently, so keep margin and validate the actual field as well. The example headlines use plain text.

## 4. Write the description and purchase terms

Open with the buyer's recognizable situation. Explain the deliverable and how it will be used. Replace vague feature labels with concrete contents.

For example, “Templates included” leaves the work undefined. “Use the outline worksheet to choose a learner outcome and order the lessons” tells the buyer what the file does.

For a service, explain the approved work before, during, and after the session. A preparation review or written action plan belongs in the copy only if the seller agreed to provide it. State the format and duration separately from the total work involved.

### Copy-and-adapt description

Replace every bracketed field with verified information. Delete unsupported sections rather than making up a benefit to fill them.

```text
[PRODUCT NAME]

For [BUYER] who needs to [IMMEDIATE JOB].
You receive [DELIVERABLE] to help you [SPECIFIC USE].

What is included
- [ITEM]: use it to [TASK].
- [ITEM]: use it to [TASK].
- [ITEM, ONLY IF INCLUDED]: use it to [TASK].

How it works
[WHAT THE BUYER DOES AFTER PAYMENT].
[WHERE AND WHEN THE DELIVERABLE ARRIVES].
[ANY NECESSARY INPUTS OR ACCOUNT STEPS].

Access and support
[DEFINED ACCESS PERIOD].
[SUPPORT SCOPE, ROUTE, AND ANY CORRECTION ALLOWANCE].

Before you buy
[PREREQUISITES AND IMPORTANT EXCLUSIONS].
[VERIFIED REFUND / CANCELLATION POLICY REFERENCE].
```

Do not turn the description into a list of operator instructions. A buyer needs to know how to use the product, not how its deployment works. For an explicitly sold technical template, installation requirements remain essential product information.

### Fictional description example

The following defines an imaginary workbook; it makes no claim about an existing product. Use it only as a writing example.

> Course outline workbook
>
> For course creators with useful material but no clear lesson order. Work through a learner-outcome worksheet, a lesson map, and a review checklist to prepare an outline you can use when recording.
>
> The workbook includes a blank version and a completed demonstration. Compare your outline with the demonstration, then use the checklist to identify gaps before production.
>
> This is a self-guided resource. Recording, editing, personal feedback, and help selling the course are outside its scope.

This body still needs approved price, access duration, delivery, support, and policy information before it becomes a complete sellable page.

### Purchase-area template

```text
Due now: [AMOUNT AND CURRENCY]
Billing: [ONE-TIME, OR EXACT RENEWAL AMOUNT AND INTERVAL]
Trial, if offered: [PERIOD / AMOUNT DUE TODAY / FIRST PAID CHARGE]
Tax display: [WORDING MATCHING THE CHECKOUT]
Access: [DEFINED PERIOD AND START CONDITION]
After payment: [REAL NEXT STEP]
Purchase action: [APPROVED ACTION LABEL]
```

If a service is paid before booking, state that order and send the button to the correct checkout, not directly to an unpaid booking screen. If delivery requires a manual step, name the step and approved timing instead of promising instant access.

Match the button to the canonical returned checkout URL, including its configured post-purchase route. Use a supported native button label; a custom button on a separate website must still describe its real action. Never invent a purchase URL from the product name. [S2, S4]

Whop's Seller Terms require defined access periods and prohibit lifetime, perpetual, or indefinite-access listings. Keep platform access, file delivery, permitted use, future updates, and support duration distinct. Do not invent a license or refund policy to complete the copy. [S5]

## 5. Answer the buying questions in the FAQ

Write answers for the exact offer and language on this page. A neighboring product's terms, a free channel's activity, or an old promotion is not proof of what this buyer receives.

Use the following as an answer worksheet. Replace the fields before publication.

```text
Who is this for?
It is for [BUYER / EXPERIENCE LEVEL / IMMEDIATE JOB].
You will need [PREREQUISITES]. It does not include [IMPORTANT EXCLUSION].

What exactly do I get?
You receive [VERIFIED CONTENTS / FORMATS / QUANTITIES].
[NAME ANY OPTIONAL ITEM] is sold separately.

How do I receive it?
After payment, [VERIFIED ACCESS STEPS].
[DELIVERY TIMING AND ANY REQUIRED BUYER ACTION].

How long can I access it?
[DEFINED ACCESS PERIOD AND WHEN IT STARTS].
[SEPARATE UPDATE OR SUPPORT PERIOD, IF DIFFERENT].

Is this a subscription?
[EXACT BILLING MODEL]. You pay [DUE-NOW AMOUNT], then [RENEWAL TERMS,
IF ANY]. [TRIAL TERMS, IF ANY].

Can I get personal help?
[WHAT SUPPORT IS INCLUDED / WHERE TO REQUEST IT / AGREED LIMITS].
[WHAT REQUIRES A SEPARATE PURCHASE].

What if I cancel or request a refund?
[APPROVED POLICY AND VERIFIED REQUEST ROUTE].
[WHEN BILLING STOPS AND WHAT HAPPENS TO ACCESS, WHERE APPLICABLE].
```

Add a product-specific objection when needed, such as required software, expected starting material, accessibility, or whether personal feedback is included. Avoid adding generic reassurance that does not answer a real question.

Do not assume saving a description updates separate FAQ records. Reopen the native FAQ editor, then expand every question on the actual public product page. Compare question count, full answers, language, and billing wording. Check the direct checkout separately; the purchase surface can show different or older text.

## 6. Prepare the gallery and banners

Keep a separate composition for each placement. Whop's older first-party store-page gallery guidance recommends 16:9 media. This module uses that ratio as a production template for product galleries, subject to the current product editor's crop preview; the older store-page article does not establish every current product-gallery requirement. [S3, published 2025-05-14; checked 2026-09-29]

| Placement | Working aspect ratio | Example export size | Purpose |
|---|---|---|---|
| Product gallery image | 16:9 | 1600 × 900 px | Cover, excerpt, or usage demonstration |
| Product banner | 2:1 | 1600 × 800 px | Compact recognition of the individual product |
| Store banner | 3:1 | 1800 × 600 px | Coherent introduction to the store's offer range |

The export sizes are production choices, not Whop upload limits. The product-banner and store-banner ratios are the working templates for this playbook; the current public documentation reviewed here does not establish them as universal platform requirements. Confirm the actual destination and crop controls before exporting the final version. A field called “banner” must not be assumed to mean the gallery's first image.

### Suggested gallery sequence

Use only frames that contribute evidence. This sequence is a recommendation, not a required image count.

1. Product cover. Show the product name, a short description of its job, and a recognizable real deliverable. Keep decoration secondary.
2. Contents. Show the actual table of contents, lesson list, or service stages. Any number on the image must match the delivered product.
3. Useful excerpt. Enlarge a real worksheet, checklist, or lesson section so a buyer can inspect it. A small stack of illegible pages is weak evidence.
4. Usage example. Show how the material is used. Label demonstration data as an example; never present it as a customer result.
5. Scope and access. Clarify who it suits, what is included, and the next step. Do not repeat the whole description inside an image.

For a recurring editorial offer, an approved sample edition and its source-check workflow can demonstrate the deliverable. A production-board screenshot with private names or internal instructions does not belong in the public gallery.

The first image must remain understandable without the later frames. Keep prices and promotional deadlines in editable page fields where possible, so changing an offer does not leave an old price embedded in a cover. Essential purchase terms must also be readable as page text.

### Rules for credible visuals

- Start from approved source files. Use a real PDF page, actual product screen, or authentic photograph where it shows what is sold.
- Preserve the source's meaning. Crop to a useful area without changing data, hiding a material limitation, or implying a larger deliverable.
- Remove private data from the exported asset. Use irreversible redaction, flatten it, remove sensitive metadata, and reopen the result. A movable rectangle over text is not sufficient.
- Compose labels and exact wording as controlled text layers. Do not ask an image generator to recreate a document page, testimonial, transaction, or chart as evidence.
- Generated decoration must not impersonate a customer, practitioner, office, event, or real result. Keep it clearly separate from product proof, and disclose it where needed to prevent confusion.
- Use testimonials only with an exact source, relevant product association, and reuse permission. Public availability alone is not permission. Do not fabricate ratings, member counts, certifications, or endorsements.
- Use readable type, strong contrast, and clear spacing. Recompose for each aspect ratio instead of stretching the image. Keep important text away from crop edges.
- If a real sample cannot be shown safely, use a genuinely supplied blank template or a clearly labeled demonstration. Omit the proof claim if neither is available.

### Asset brief to copy

```text
Placement: [GALLERY / PRODUCT BANNER / STORE BANNER]
Target aspect ratio: [RATIO]
Approved source material: [ASSET DESCRIPTION]
Main buyer question answered: [QUESTION]
Exact text to typeset: [APPROVED WORDING]
Real excerpt to show: [DESCRIPTION OF INCLUDED MATERIAL]
Private or misleading elements to remove: [LIST]
Crop-safe area: [WHAT MUST REMAIN VISIBLE]
Alt text or adjacent accessible description: [WHAT IS ACTUALLY SHOWN]
Rights and approval: [CONFIRMED / NOT CONFIRMED]
```

### Technical and visual checks

1. Decode the exported image with an image library and confirm its real format, width, height, and aspect ratio. A filename extension is not proof of format.
2. Open the file and inspect it at full size and at realistic mobile display size. Check spelling, accents, missing glyphs, low contrast, unreadable screenshots, and unexpected transparency.
3. Compare each excerpt with the original file. Verify counts and labels against the delivered version.
4. Check the uploader's current accepted formats and file-size limits. Compress for loading speed without destroying sample legibility.
5. Inspect the destination crop, thumbnail, and gallery order after an authorized upload. Add alt text if supported; otherwise give meaningful equivalent information in visible page text.

No image inspection is complete from dimensions alone. A correctly sized file can still show the wrong product or unreadable content.

## 7. Apply changes without overwriting other work

For a writing-only assignment, stop at the finished local copy and asset brief. Use the following procedure only after approval to update the selected Whop product.

1. Confirm the exact business, product, existing media order, and pricing configuration. Reuse the existing product when appropriate.
2. Snapshot protected fields: price, currency, billing, availability, access, custom fields, redirects, and marketplace status.
3. Close stale editor tabs without saving. Reopen the current state before applying approved copy.
4. Change only the approved fields. An image-only correction must not also reprice, hide, publish, or resubmit the product.
5. If using the API, follow the documented upload flow: create a public file record only for approved public media, send the bytes to the returned upload URL with its exact headers, then confirm the upload is ready. Attach it using the current gallery field. Do not trust a legacy banner flag solely because it returns success. Replacing an ordered gallery can remove other images, so reread it immediately before replacement. [S2, S7]
6. Read back the exact product and fetch its attached public asset. Compare the decoded dimensions and image content with the approved local version. Hosting may recompress an image, so a changed file hash alone does not establish different visible content.
7. Verify the served product page and checkout rather than only the editor preview.

An uploaded public file is already exposed at its asset URL, even if the product is hidden. Never upload private source material as a temporary design step. [S7]

## 8. Buyer-view acceptance checklist

Run the inspection in a fresh non-admin session on desktop and a narrow mobile view. The following widths are test choices, not Whop limits: 390 px for the narrow view and an intermediate width to catch cropped or overlapping content.

### Content and media

- [ ] The intended product and seller appear at the verified destination; a successful HTTP response alone is insufficient.
- [ ] The headline is within 80 characters and remains readable in the rendered layout. [S1]
- [ ] Description, FAQ, images, and checkout describe the same product, language, contents, access period, and exclusions.
- [ ] Every displayed quantity can be reconciled with the delivered files or approved service scope.
- [ ] Gallery order is correct, images load after scrolling, and useful excerpts can be read without guessing.
- [ ] Each banner crop preserves its subject and essential text on mobile.
- [ ] No private data, internal notes, unresolved placeholders, invented proof, or unlicensed assets are visible.

### Purchase and delivery

- [ ] Due-now amount, currency, tax wording, trial, renewal, and cancellation information match the exact checkout.
- [ ] The primary action opens the canonical intended checkout, preserving its post-purchase routing.
- [ ] A preparation-only checkout is actually closed. An authorized live checkout shows the appropriate loaded payment controls rather than a loading placeholder.
- [ ] Optional offers do not block access to the base product or imply an automatic extra charge.
- [ ] A configured redirect is described as configured until an authorized transaction proves it executed.
- [ ] Actual buyer access and the correct downloaded file are tested separately when authorized; administrator access is not delivery proof.

### Publication state

Report saved copy, product visibility, checkout availability, and marketplace approval separately. Whop's Publish Product documentation distinguishes a submitted listing awaiting review from an approved discoverable listing. A public direct checkout is not proof of marketplace discovery. [S6]

```text
Page copy: [READY / BLOCKED, WITH REASON]
Source and media-rights check: [RESULT]
Headline length: [COUNT]
Description and FAQ consistency: [RESULT]
Gallery and banner checks: [RESULT / NOT PERFORMED]
Canonical checkout inspection: [RESULT / NOT PERFORMED]
Product visibility and purchase availability: [EXACT OBSERVED STATES]
Marketplace state: [EXACT OBSERVED STATE / NOT CHECKED]
Real payment and buyer delivery: [TESTED / NOT TESTED]
Next required decision: [ONLY THE UNRESOLVED DECISION]
```

## Sources

All sources below were consulted on 2026-09-29. Source citations establish the stated platform behavior, not conversion performance or the availability of a feature in every account.

- [S1] Whop Docs, [Create a Product](https://docs.whop.com/manage-your-business/products/create-product). Headline maximum of 80 characters; product details, pricing, media, description, features, and FAQs.
- [S2] Whop Docs, [Product](https://docs.whop.com/api-reference/beta/products/product). Ordered gallery images, product description, pricing variants, and purchase-button destination.
- [S3] Whop, [How to set up Whop Content Rewards](https://whop.com/blog/set-up-content-rewards/#3-add-gallery-images), published 2025-05-14, store-page gallery section. Recommends 16:9 media on that older surface. Used as a production-template reference, not proof of current product-gallery requirements, banner ratios, or upload limits.
- [S4] Whop Docs, [Create a Checkout Configuration](https://docs.whop.com/api-reference/beta/checkout-configurations/create-a-checkout-configuration). Returned purchase URL and checkout-specific redirect.
- [S5] Whop, [Seller Terms](https://whop.com/seller-terms/), page updated 2026-07-14. Accurate listings, seller responsibilities, specific access periods, and prohibition of indefinite-access products.
- [S6] Whop Docs, [Publish Product](https://docs.whop.com/api-reference/beta/products/publish-product). Marketplace review and approved-discovery states.
- [S7] Whop Docs, [Upload Files](https://docs.whop.com/developer/guides/upload-files). File creation, byte upload, readiness checks, and public-file exposure.
