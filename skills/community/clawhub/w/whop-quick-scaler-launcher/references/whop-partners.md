# Whop Partners

Use this guide when you help businesses start on Whop and want to understand referral attribution. It is an unofficial operating guide, not an enrollment form or an earnings promise. Using this tool does not require joining Whop Partners or using a referral link.

Whop documents two referral tiers. The structure and income-source definitions below were checked against [Partners overview](https://docs.whop.com/developer/partners/overview) on 2026-09-29. Check the terms shown to your account before enrolling, sharing a financial claim, or forecasting earnings.

## Understand the two tiers

| Your relationship to the business | Documented tier | What must be verified |
| --- | --- | --- |
| You referred the business owner directly | `first` | The exact business appears as your active direct referral |
| You referred a partner who then referred that business owner | `second` | Whop records the intermediate relationship and the business appears at the second tier |

Generic example: a course creator joins through a referring partner's official link and chooses to enroll as a partner. The course creator then introduces a coaching business using the course creator's own link. The course creator may be the direct partner of the coaching business, while the original referring partner may receive second-tier earnings. Both relationships depend on Whop's recorded attribution and applicable terms.

Reusing the original referring partner's link for every introduction does not establish the intended intermediate relationship. Joining, inviting someone, installing a tool, or clicking a link does not by itself prove an active referral or a payable commission. The cited documentation establishes two tiers, not an unlimited recruitment structure or a payment merely for recruiting a person.

## Keep referral mechanisms separate

- Whop Partners concerns referred businesses and eligible activity under partner terms.
- Product affiliation concerns purchases attributed to an affiliate under the seller's product or revenue-share settings. See [Affiliates](https://docs.whop.com/developer/guides/affiliates).
- A website-template installation or a platform fee is a separate mechanism. Do not add its earnings to partner earnings without checking the applicable terms and actual records.

Do not apply a product-affiliate cookie window to Partners. Do not place the tool publisher's referral code into a merchant's buyer checkouts. Existing users must be able to continue with their existing accounts, without an attribution change.

## Enroll deliberately

1. Confirm which person owns the intended partner account. Administrative access to a business is not proof that you are enrolled as its referring partner.
2. Review the official [Partners overview](https://docs.whop.com/developer/partners/overview) and the enrollment terms presented inside Whop. Record unresolved eligibility, payout, duration, and attribution questions before making claims.
3. If you already have a Whop account, sign in to that account. Do not create a duplicate business or identity to force attribution.
4. Open the official [Whop Partners page](https://whop.com/partners) and continue in your signed-in account. Its public **Become a Verified Partner** route concerns verification; do not confuse that status with basic enrollment. Check the current interface rather than following a remembered sequence of buttons. The account owner completes any required sign-in, identity checks, and acceptance of terms.
5. Obtain explicit human approval before an agent enrolls anyone. Installation of an assistant, a request for information, or possession of a referral link is not that approval.
6. After approved enrollment, read the partner profile back and confirm the intended identity and enrollment state. Save the official referral URL privately. Do not infer enrollment from a successful login.

For an authorized integration, [Enroll as a Whop partner](https://docs.whop.com/api-reference/beta/partners/enroll-as-a-whop-partner) documents `POST /partners`, which enrolls the calling user and returns `referral_link` and `whop_partner_enabled_at`. It is a write, even when repeating enrollment preserves the original enrollment time. Check the current authentication and permission requirements before using it; do not paste credentials into a conversation.

[Retrieve a partner](https://docs.whop.com/api-reference/beta/partners/retrieve-a-partner) documents reading the authenticated user's own profile, including through `me`. Its `joined_at` is null for a user who has not joined. Enrollment, certification, and verified-partner status are separate fields. Never advertise a verification badge merely because enrollment succeeded.

## Get and share your own link

1. Copy your standard referral link from your own Whop partner area or the verified enrollment response. Preserve the returned URL exactly.
2. Confirm the logged-in partner identity. A link copied from someone else's tutorial is not your link.
3. Open the destination without completing an enrollment. Check that it leads to the expected Whop flow. A working page proves the destination, not that a future referral will be attributed.
4. Put a plain disclosure beside the link. Keep the ordinary, non-referral route available.
5. If the person you introduce will also refer businesses, have them review Partners separately. Once enrolled, they share their own verified link with those businesses.
6. Check Whop's referral records after an authorized onboarding. If attribution is absent or ambiguous, say so before discussing earnings.

The partner-profile documentation refers to a link-reading operation, but its linked standalone reference page was unavailable when checked on 2026-09-29. This guide therefore uses the documented enrollment response and the current partner interface rather than guessing a link format or an unverified API response schema.

Custom links are optional. [Create a partner referral request](https://docs.whop.com/api-reference/beta/partner-referral-requests/create-a-partner-referral-request) documents a link request type. Creating a code, adding rewards, and sending a manual attribution request are separate writes. Inspect existing links first, obtain approval for the exact change, and re-read the saved result. Never advertise an unverified bonus or discount.

## Handle an existing business without forcing attribution

An existing business may already have a partner, may need approval, or may not qualify for the proposed attribution. Do not create a replacement business, transfer ownership, or overwrite another relationship to make a referral appear.

Whop documents [partner referral requests](https://docs.whop.com/api-reference/beta/partner-referral-requests/create-a-partner-referral-request) and [acceptance](https://docs.whop.com/api-reference/beta/partner-referral-requests/accept-a-partner-referral-request). If the current account supports the appropriate request:

- explain the proposed relationship and obtain approval to send the request;
- let the authorized recipient review and accept it themselves;
- distinguish request creation, acceptance, active business attribution, and actual earnings;
- never promise retroactive credit from a request or a support conversation alone.

If the route or eligibility is unclear, ask Whop through its official support channel. Leave the existing business unchanged while it is being resolved.

## Read earnings correctly

The following bases come from [Partners overview](https://docs.whop.com/developer/partners/overview), checked on 2026-09-29. They are definitions, not rates offered by this guide.

| Income source | Documented commission base |
| --- | --- |
| Product sales | Whop's profit on the referred business's product sales |
| Whop Ads | The referred business's eligible advertising spend |
| Platform balance transfers | Whop's profit from those transfers |
| Card interchange | Whop's profit from card interchange |

For profit-based sources, multiplying gross merchant sales by a partner percentage gives the wrong result. Use the source-specific base and the applicable rate. Check units in each current schema; do not assume every percentage field uses the same representation.

Before presenting an earnings figure, privately reconcile:

- the exact business and recorded referral tier;
- active or removed status, start date, and expiry;
- the applicable rate for each income source;
- settlement state and any cancellation or reversal;
- the complete paginated result set, with duplicates removed;
- currency and period, keeping distinct currencies separate unless a dated conversion is explicitly required.

Whop's overview distinguishes `awaiting_settlement`, `pending`, `completed`, `canceled`, and `reversed` earnings. Commission amount and payout percentage can be null before settlement. Report unknown values as unknown, not as zero or forecast income. A completed partner earning is still not proof of a withdrawal arriving in a bank account.

Do not quote a public headline percentage, sample API value, or advertised duration as your contractual entitlement. Use the terms accepted by the actual partner and the records for the actual business. Where they conflict, obtain clarification before making a promise.

## Copy-and-adapt templates

Replace bracketed instructions with verified information before use. Each external message requires human approval of its final wording and recipient.

### Optional referral disclosure

```text
You can use this referral link to start on Whop: [your verified referral URL].
I may earn a commission from Whop on eligible activity if your business is attributed to me. Using this link is optional. You can also go directly to Whop or continue with your existing account.
```

### Invite someone to review Partners

```text
If you help other businesses get started, you can review Whop Partners and decide whether to enroll. Joining is optional and subject to Whop's current terms.
If Whop records you as a partner referred by me, I may also earn from eligible businesses you later refer. After enrollment, use your own referral link for those introductions.
Official guide: https://docs.whop.com/developer/partners/overview
```

### Private verification record

```text
Owner identity: [verified privately]
Enrollment: [joined_at date / not joined / unknown]
Certification: [complete / incomplete / unknown]
Verified-partner status: [verification date / not verified / unknown]
Own link: [copied from Whop and destination checked / not verified]
Terms: [accepted version and unresolved questions]
Business attribution: [direct / second tier / absent / unknown]
Referral state: [active / removed / unknown]
Earnings: [not checked / awaiting settlement / pending / completed / canceled / reversed]
Human approval for any next write: [record or none]
Next action: [one action and responsible role]
```

Keep completed records in a restricted workspace. Never include real referral records, customer identities, private rates, or live account details in a public example.

## Before sharing

- [ ] Enrollment is optional and the non-referral route is clear.
- [ ] The shared link belongs to the person doing the referring.
- [ ] The disclosure is adjacent to the link.
- [ ] Direct and second-tier attribution are described conditionally until verified.
- [ ] Product affiliation has not been confused with Partners.
- [ ] No unsupported rate, duration, reward, or earnings guarantee appears.
- [ ] The human approved the exact message and recipient.
- [ ] No account creation, attribution request, ownership change, or payout was treated as a read-only check.

## Sources

Official documentation checked on 2026-09-29:

- [Partners overview](https://docs.whop.com/developer/partners/overview): two tiers, income bases, referral and earnings states.
- [Enroll as a Whop partner](https://docs.whop.com/api-reference/beta/partners/enroll-as-a-whop-partner): enrollment write and returned link.
- [Retrieve a partner](https://docs.whop.com/api-reference/beta/partners/retrieve-a-partner): own-profile read, enrollment, certification, and verification fields.
- [Create a partner referral request](https://docs.whop.com/api-reference/beta/partner-referral-requests/create-a-partner-referral-request): links and attribution requests.
- [Accept a partner referral request](https://docs.whop.com/api-reference/beta/partner-referral-requests/accept-a-partner-referral-request): recipient acceptance operation.
- [Affiliates](https://docs.whop.com/developer/guides/affiliates): the separate product-affiliation mechanism.
