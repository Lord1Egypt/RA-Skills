## Description: <br>
Design automated win-back campaigns targeting lapsed customers with personalized re-engagement sequences across email, SMS, and paid ads, using recency-based segmentation to maximize reactivation rates and recovered revenue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leooooooow](https://clawhub.ai/user/leooooooow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing and ecommerce teams use this skill to design data-driven win-back campaigns for lapsed customers, including RFM segmentation, multi-channel sequencing, channel configuration, holdout measurement, and post-campaign analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer data used for behavioral personalization or customer-list advertising may exceed privacy notices, consent, lawful basis, or platform terms. <br>
Mitigation: Confirm privacy notices, consent or lawful basis, opt-out handling, and platform terms before launch; minimize uploaded customer fields and involve legal or privacy review for regulated regions. <br>
Risk: SMS win-back messages can create compliance exposure if recipients lack documented marketing consent or opt-out handling. <br>
Mitigation: Verify explicit SMS opt-in consent for every recipient, keep consent records, include opt-out instructions in each message, and configure quiet hours before enrollment. <br>
Risk: Sending to deeply lapsed or legally suppressed contacts can harm deliverability and violate marketing obligations. <br>
Mitigation: Remove hard bounces, invalid addresses, unsubscribes, deletion requests, and other suppressed contacts; ramp deeply lapsed sends gradually and monitor bounce and spam complaint rates. <br>
Risk: Poor cross-channel suppression can continue ads, SMS, or email after purchase or opt-out, wasting spend and degrading customer experience. <br>
Mitigation: Configure purchase, unsubscribe, SMS STOP, bounce, and complaint events to suppress the appropriate channels immediately or near real time. <br>


## Reference(s): <br>
- [Win-Back Campaign Skill](artifact/SKILL.md) <br>
- [Recency-Frequency-Monetary Segmentation Guide for Win-Back Campaigns](artifact/segmentation-guide.md) <br>
- [Multi-Channel Strategy Guide for Win-Back Campaigns](artifact/channel-strategy-guide.md) <br>
- [Win-Back Campaign Output Template](artifact/output-template.md) <br>
- [Win-Back Campaign Quality Checklist](artifact/quality-checklist.md) <br>
- [Klaviyo Win-Back Flow Best Practices](https://www.klaviyo.com/blog/winback-email-examples) <br>
- [FCC Guidance on Unwanted Robocalls and Texts](https://www.fcc.gov/consumers/guides/stop-unwanted-robocalls-and-texts) <br>
- [Google Ads Customer Match](https://support.google.com/google-ads/answer/6379332) <br>
- [Meta Custom Audiences Documentation](https://www.facebook.com/business/help/744354708981227) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown campaign plans, tables, checklists, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include channel-specific recommendations, audience segmentation tables, suppression rules, measurement plans, and optimization notes.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
