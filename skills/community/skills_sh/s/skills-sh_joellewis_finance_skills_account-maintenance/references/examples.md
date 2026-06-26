# Account Maintenance — Worked Examples

## Example 1: Processing an account re-registration from individual to revocable trust

**Scenario:** A 62-year-old client with $3.2M across three accounts at the firm (individual taxable brokerage account with $2.1M, traditional IRA with $800K, and Roth IRA with $300K) has recently established a revocable living trust with her estate attorney. The trust names the client as grantor and trustee, with her adult son as successor trustee. The client wants to transfer the taxable brokerage account into the trust. The IRA and Roth IRA cannot be held in a trust (they must remain in the individual's name).

**Step-by-step processing:**

1. **Verify the request and gather documentation.** Confirm the client's identity and the nature of the request. Obtain: (a) a trust certification or the relevant pages of the trust agreement showing the trust name, date of establishment, grantor, trustee(s), successor trustee(s), and the trust's powers regarding investment accounts; (b) a signed letter of instruction from the client directing the re-registration; (c) an updated W-9 in the trust's name (using the client's SSN, since this is a grantor trust). Depending on the custodian, a medallion signature guarantee on the letter of instruction may be required.

2. **Review the trust document.** Operations or the compliance team reviews the trust certification to confirm: the trust is validly established, the client is the current trustee with authority to open and manage investment accounts, the trust is revocable (confirming grantor trust status and SSN usage), and there are no restrictions on the types of investments the trust can hold. Flag any unusual provisions for compliance review.

3. **Prepare the custodian re-registration request.** Complete the custodian's account re-registration or re-titling form. The new registration will read something like: "Jane A. Smith, Trustee of the Jane A. Smith Revocable Living Trust dated January 15, 2026." Submit the form, trust certification, W-9, and letter of instruction to the custodian.

4. **Confirm the tax treatment.** This re-registration is not a taxable event. The assets move from the individual's name to her revocable trust with no change in beneficial ownership. All existing tax lots, cost basis, and acquisition dates carry over unchanged. The account will continue to report under the client's SSN for tax purposes. Document this determination in the account notes.

5. **Update internal systems.** After the custodian confirms the re-registration: update the CRM to reflect the trust account and its relationship to the client record; update the portfolio management system's account registration; verify that the model portfolio assignment and investment restrictions carry over; confirm that the billing account linkage is maintained (fees are typically still billed to the trust account or another account in the household); update beneficiary designations on the IRA and Roth IRA if the client wishes to name the trust as a beneficiary (noting the tax implications — a trust as IRA beneficiary may limit stretch distribution options).

6. **Client communication.** Send the client a confirmation of the completed re-registration with the new account title. Remind the client that the IRA and Roth IRA remain in her individual name and that she should coordinate with her estate attorney to ensure beneficiary designations on those accounts align with the trust's distribution provisions.

**Key risks and controls:** Verify that the SSN (not a separate EIN) is used for the grantor trust — using an EIN would create tax reporting errors. Confirm that cost basis records are preserved through the re-registration; some custodian systems may reset cost basis if the re-registration is processed as a close-and-reopen rather than a title change. Monitor for this and correct any basis discrepancies immediately.

## Example 2: Handling a death notification across multiple accounts with different registration types

**Scenario:** The firm receives a call from the wife of a 71-year-old client who passed away two days ago. The deceased client held five accounts at the firm: (1) an individual taxable brokerage account ($1.4M), (2) a joint taxable brokerage account with his wife as JTWROS ($900K), (3) a traditional IRA ($650K) with his wife as primary beneficiary and two adult children as contingent beneficiaries, (4) a Roth IRA ($200K) with the same beneficiary designation, and (5) a revocable trust account ($500K) where the deceased was sole trustee and his wife is named as successor trustee. The firm also manages the wife's individual IRA ($400K) separately.

**Step-by-step processing:**

1. **Receive and document the notification.** Record the date and time of the notification, the identity of the person providing notification (the wife), and the relationship to the deceased. Express appropriate condolences. Explain that you will need a certified death certificate to proceed with account processing and outline the general timeline. Assign a dedicated operations contact or "estate services coordinator" as the single point of contact for the family.

2. **Immediately restrict the deceased's accounts.** Place a death restriction on all five accounts. For accounts (1), (3), (4), and (5), this means no trading, distributions, or changes until appropriate documentation is received. For account (2) — the JTWROS account — the wife retains access as the surviving owner, but place a notation that the deceased owner must be removed via re-registration. Do not restrict the wife's own IRA (account 6), as it is not an account of the deceased.

3. **Request required documentation.** Provide the wife with a checklist of documents needed for each account:
   - *All accounts:* Certified death certificate (at least 3 copies recommended).
   - *Individual taxable account (1):* If a TOD designation is on file, a beneficiary claim form. If no TOD, letters testamentary (if there is a will) or letters of administration (if intestate), and the estate's EIN.
   - *JTWROS account (2):* Death certificate only — the wife will become sole owner.
   - *Traditional IRA (3) and Roth IRA (4):* Beneficiary claim forms for the wife as primary beneficiary. The wife will need to decide whether to roll the traditional IRA into her own IRA (spousal rollover), treat it as her own, or establish an inherited IRA. For the Roth IRA, a spousal rollover into her own Roth IRA is typically the most advantageous option.
   - *Trust account (5):* Trust certification showing the wife as successor trustee, or the relevant pages of the trust agreement confirming successor trustee status.

4. **Process each account upon receipt of documentation.**
   - *Account 1 (individual taxable):* Assume a TOD designation naming the wife. Upon receipt of the death certificate and signed beneficiary claim form, transfer assets to the wife's account (or a new account in her name). Apply the step-up in basis — revalue all positions to their fair market value as of the date of death. If no TOD, assets pass to the estate: open an estate account titled "Estate of [Deceased], [Personal Representative] as Executor/Administrator," obtain the estate's EIN, and transfer assets to the estate account pending probate and distribution.
   - *Account 2 (JTWROS):* Upon receipt of the death certificate, re-register the account in the wife's name alone. Remove the deceased's name from the account title. The wife's SSN remains on the account. Apply the step-up in basis to the deceased's half of the account (50% of each position is stepped up to date-of-death FMV in non-community-property states; in community property states, both halves may be stepped up).
   - *Account 3 (traditional IRA):* The wife elects spousal rollover, rolling the $650K into her own traditional IRA. This is the most common election because it allows the wife to defer RMDs until she reaches RMD age — 73 (SECURE 2.0; rises to 75 in 2033) — and name her own beneficiaries. Process the rollover as a trustee-to-trustee transfer. Cost basis is not relevant for traditional IRA assets (fully taxable on distribution), but the transfer must be processed as a non-taxable rollover and reported on Form 1099-R with the appropriate distribution code.
   - *Account 4 (Roth IRA):* The wife elects to treat the inherited Roth as her own Roth IRA by rolling it into her existing or a new Roth IRA. This preserves the tax-free growth and eliminates any distribution requirements during her lifetime.
   - *Account 5 (trust account):* Upon receipt of the trust certification confirming the wife as successor trustee, re-title the account to reflect her as trustee: "[Wife's Name], Trustee of the [Trust Name]." Review the trust terms to determine if the trust continues (common with revocable trusts that become irrevocable upon death of the grantor) or terminates and distributes assets to beneficiaries. If the trust becomes irrevocable, it will need its own EIN going forward.

5. **Coordinate tax reporting.** The deceased's final tax year runs from January 1 to the date of death. Activity on accounts (1) through (5) through the date of death is reported under the deceased's SSN. Activity after the date of death is reported under the wife's SSN (for accounts she takes over), the estate's EIN (for estate accounts), or the trust's EIN (if the trust becomes irrevocable). Work with the custodian to ensure correct TIN assignment on all accounts post-death.

6. **Update all internal systems.** Update the CRM to reflect the death, change the household structure, reassign the advisor relationship to the wife as the primary client, update account registrations in the portfolio management system, and adjust the billing configuration (the wife may now be the billable party for all accounts). Schedule a follow-up meeting between the advisor and the wife (after an appropriate interval) to review the consolidated portfolio, update her investment policy, and adjust the financial plan.

**Key risks and controls:** The greatest risk is processing transactions on a deceased person's account before proper documentation is in hand — this can create legal liability and tax reporting errors. The second risk is incorrect cost basis after the step-up: every position must be revalued to the date-of-death FMV, and the custodian's automated step-up process should be verified against an independent price source. Third, ensure that IRA beneficiary elections (spousal rollover vs inherited IRA) are documented in writing, as the choice is irrevocable and has significant long-term tax implications.

## Example 3: Implementing systematic account maintenance review and data quality processes

**Scenario:** A mid-sized RIA with $5B AUM across 4,000 accounts has identified recurring data quality issues: 12% of accounts have no beneficiary designation on file, 8% have addresses that generate returned mail, 15% of trust accounts are missing current trust certifications, and the firm has no systematic process for reviewing accounts that have not been updated in more than 3 years. The firm wants to implement a proactive account maintenance review program to improve data quality, reduce operational risk, and satisfy regulatory expectations for books and records.

**Designing the review program:**

1. **Establish a data quality baseline.** Generate a comprehensive data quality report across all accounts, measuring completeness and accuracy for critical fields:
   - *Beneficiary designations:* Percentage of eligible accounts (retirement accounts, TOD accounts) with primary and contingent beneficiaries on file, percentage with beneficiary review within the past 3 years.
   - *Contact information:* Percentage of accounts with validated mailing addresses (no returned mail), percentage with email on file, percentage with phone number on file and verified.
   - *Trust and entity documentation:* Percentage of trust accounts with trust certification on file and dated within the past 5 years, percentage of entity accounts with current formation documents and beneficial ownership certification.
   - *Suitability profiles:* Percentage of accounts with investment profile updated within the past 3 years, percentage with risk tolerance questionnaire on file.
   - *Standing instructions:* Percentage of accounts with systematic plans that have not been reviewed in more than 2 years.
   - *Cost basis records:* Percentage of holdings with uncovered shares that have no historical cost basis on file.

2. **Prioritize remediation by risk and impact.** Not all data quality issues carry equal risk. Prioritize:
   - *High priority (remediate within 90 days):* Missing beneficiary designations on retirement accounts (disposition risk at death), returned mail with no valid address on file (regulatory and escheatment risk), accounts with compliance or legal holds that have not been reviewed in 6+ months.
   - *Medium priority (remediate within 180 days):* Stale trust certifications (operational risk at trustee change or death), outdated suitability profiles (regulatory risk for ongoing recommendations), missing cost basis on large positions (tax reporting risk).
   - *Lower priority (remediate within 12 months):* Missing email addresses, missing contingent beneficiary designations, standing instructions that have not been reviewed recently.

3. **Design the ongoing review cadence.** Establish a recurring review cycle:
   - *Annual account maintenance review:* Coincide with the annual client review meeting. The advisor reviews and confirms: contact information, beneficiary designations, suitability profile, investment restrictions, standing instructions, and account features. The review is documented in the CRM with a timestamp and the advisor's attestation that all information is current.
   - *Quarterly data quality reports:* Operations generates quarterly metrics showing data completeness rates, trending, and accounts requiring attention. The report is reviewed by the chief compliance officer and the operations manager.
   - *Triggered reviews:* Certain events trigger an immediate account review outside the annual cycle: returned mail, life event notification (marriage, divorce, birth, death), significant market events that may affect suitability, advisor departure (all accounts assigned to a departing advisor receive an expedited review by the successor advisor), and custodian platform migration.

4. **Implement operational workflows for common maintenance items.** For each maintenance category, define a standard operating procedure (SOP) that specifies:
   - *Who* can initiate the request (client, advisor, operations, compliance)
   - *What* documentation or verification is required
   - *How* the request is processed (system workflow, custodian submission)
   - *When* the request must be completed (service-level agreement)
   - *What* quality checks are performed before and after processing
   - *How* the completed action is documented and retained

   For example, the SOP for an address change specifies: the advisor or client initiates the request; identity verification is performed per firm policy (callback to phone on file for verbal requests, or written/electronic authorization); the address is updated in the CRM (system of record); the CRM integration propagates the change to the custodian and correspondence system; a confirmation is sent to both the old and new addresses; senior investor protections are applied if the client is 65+ and the change triggers a red flag; the change is completed within 2 business days; and the change record is retained in the CRM activity log.

5. **Assign accountability and measure progress.** Designate an "account data steward" — a member of the operations team responsible for data quality monitoring and remediation coordination. Publish a monthly data quality dashboard tracking: percentage of accounts with complete and current data across all critical fields, number of open remediation items by priority, average age of open items, and NIGO rates (as a proxy for data quality at the point of custodian submission). Set targets: 95% completeness for high-priority fields within 12 months, 90% for medium-priority fields within 18 months.

**Key risks and controls:** The primary risk in a data quality remediation program is client fatigue — contacting thousands of clients to update information can strain advisor relationships if not managed carefully. Mitigate this by embedding updates in existing client interactions (annual review meetings, service calls) rather than launching a standalone outreach campaign. The second risk is privacy: ensure that all outreach communications about account data comply with Reg S-P and do not disclose nonpublic personal information. Third, maintain an audit trail of all remediation activities for regulatory examination purposes — examiners expect to see a documented, systematic approach to data quality, not ad hoc corrections.

