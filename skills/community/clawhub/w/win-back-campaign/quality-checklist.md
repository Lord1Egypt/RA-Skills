# Win-Back Campaign Quality Checklist

Complete this checklist before launching any win-back campaign. Every item should be checked and verified. Items marked with [CRITICAL] can cause legal, financial, or deliverability damage if missed.

---

## Segmentation and Data (8 items)

- [ ] Lapse thresholds are based on actual purchase interval data, not arbitrary round numbers
- [ ] RFM scores have been calculated and validated against historical return rates
- [ ] Each segment has a minimum viable size (500+ customers) for statistical significance
- [ ] [CRITICAL] Hard bounces, invalid emails, and role addresses have been removed from the audience
- [ ] [CRITICAL] Legally suppressed contacts (GDPR deletion requests, CAN-SPAM unsubscribes) have been excluded
- [ ] Customers with active subscriptions or auto-replenishment orders have been excluded
- [ ] Segment sizes and estimated revenue potential have been documented and reviewed
- [ ] Seasonal buyer flags have been applied where applicable

## Holdout and Measurement (6 items)

- [ ] Holdout groups have been randomly assigned for each segment (10-15% of population)
- [ ] Holdout assignment is stratified by RFM score to ensure balanced representation
- [ ] Holdout groups are documented and locked -- no contacts will be added or removed mid-campaign
- [ ] Primary KPIs are defined with specific numeric targets
- [ ] Measurement windows are defined (30-day, 60-day, 90-day)
- [ ] Reporting dashboard or template is built and tested with sample data

## Email Configuration (10 items)

- [ ] Email templates have been designed, coded, and tested across major email clients (Gmail, Outlook, Apple Mail, Yahoo)
- [ ] Mobile rendering has been verified on iOS and Android devices
- [ ] Dynamic content blocks (product recommendations, last purchased items) are pulling correct data
- [ ] Personalization tokens have fallback values for missing data (e.g., "there" if first name is empty)
- [ ] Subject lines and preheaders are written for all touches and reviewed for spam trigger words
- [ ] [CRITICAL] Unsubscribe links are functional and process opt-outs within 10 business days (CAN-SPAM requirement)
- [ ] Physical mailing address is included in email footer (CAN-SPAM requirement)
- [ ] From address and reply-to address are monitored -- replies will not go to a dead inbox
- [ ] Sending domain DNS is properly configured (SPF, DKIM, DMARC)
- [ ] [CRITICAL] Warm-up plan is in place for sending to deeply lapsed segments (6+ months no engagement)

## SMS Configuration (7 items)

- [ ] [CRITICAL] SMS opt-in consent has been verified for every recipient -- consent date, source, and language on file
- [ ] [CRITICAL] Opt-out mechanism is included in every SMS message ("Reply STOP to unsubscribe")
- [ ] [CRITICAL] Quiet hours are configured (no sends before 9am or after 9pm recipient local time)
- [ ] Messages are within 160-character target to avoid multi-segment charges
- [ ] Short links are functional, tracked, and use HTTPS
- [ ] Phone numbers have been validated (carrier lookup, disconnected number removal)
- [ ] SMS platform is configured to honor STOP replies immediately and across all future sends

## Paid Ads Configuration (6 items)

- [ ] Custom audiences have been uploaded to ad platforms with correct formatting
- [ ] Audience match rates have been reviewed (flag if below 40% -- may indicate data quality issues)
- [ ] [CRITICAL] Frequency caps are set (recommended: 3-5 impressions per user per week)
- [ ] Conversion exclusion audiences are configured and updating at least daily
- [ ] Ad creative has been reviewed for brand consistency with email/SMS messaging
- [ ] Budget pacing is set to distribute spend evenly across the campaign duration

## Cross-Channel Orchestration (5 items)

- [ ] [CRITICAL] Cross-channel suppression is configured: purchase event triggers exit from all channels
- [ ] Suppression latency has been tested: email and SMS suppress within 1 hour, ads within 4 hours
- [ ] Email and SMS are never scheduled on the same day for the same recipient
- [ ] Ad creative rotation aligns with the current email sequence stage (offer timing matches)
- [ ] UTM parameters are correctly applied to all links across all channels for attribution tracking

## Incentive and Offer Structure (4 items)

- [ ] Discount codes are generated, tested, and have correct expiration dates
- [ ] Discount codes have usage limits to prevent abuse (one per customer)
- [ ] Offer escalation is properly sequenced -- no touch offers a lower discount than a previous touch
- [ ] Free shipping thresholds (if applicable) are clearly communicated and technically functional

## Flow Logic and Automation (5 items)

- [ ] Flow entry criteria correctly identify lapsed customers in each segment
- [ ] Exit criteria are configured: purchase, unsubscribe, bounce, and sequence completion all trigger exit
- [ ] Wait steps between touches have correct durations
- [ ] Branching logic (if any) has been tested with sample contacts through every path
- [ ] [CRITICAL] Flow does not re-enroll customers who have already completed or exited the sequence

## Legal and Compliance (4 items)

- [ ] [CRITICAL] Campaign complies with CAN-SPAM Act requirements (unsubscribe mechanism, physical address, honest subject lines)
- [ ] [CRITICAL] Campaign complies with GDPR requirements for EU contacts (lawful basis for processing, data subject rights honored)
- [ ] [CRITICAL] Campaign complies with TCPA requirements for SMS (prior express written consent for marketing messages)
- [ ] Privacy policy is up to date and accessible from all email footers

## Pre-Launch Verification (5 items)

- [ ] Test sends have been completed for all email touches to internal team members
- [ ] Test SMS messages have been sent and received correctly
- [ ] End-to-end flow has been tested with a small batch of real contacts (seed list or internal accounts)
- [ ] All stakeholders have reviewed and approved the campaign plan, creative, and offers
- [ ] Launch schedule is documented with specific dates, responsible owners, and escalation contacts

---

## Sign-Off

| Role | Name | Approved | Date |
|---|---|---|---|
| Campaign Owner | | [ ] | |
| Email Marketing Lead | | [ ] | |
| Legal / Compliance | | [ ] | |
| Director / VP Marketing | | [ ] | |

**Total items: 60** | **Critical items: 12**

Any item marked [CRITICAL] that cannot be checked must be resolved before launch. No exceptions.
