## Description: <br>
Studio Booking Manager helps an agent automate recording studio bookings through Telegram, including availability checks, booking changes, payment links, notifications, and client history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[producedbysavant](https://clawhub.ai/user/producedbysavant) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External booking agents, studio operators, and developers use this skill to guide Telegram-based studio reservations, payment-link generation, cancellations, rescheduling, occupancy checks, and client follow-up workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes payment-link and refund handling without enough built-in confirmation controls. <br>
Mitigation: Require explicit user or admin confirmation before cancellation, refund, or payment-affecting actions. <br>
Risk: Booking management and customer history workflows may expose contact, payment, or visit-history data. <br>
Mitigation: Enforce owner or admin authorization, log booking changes, and disclose what customer data is collected, shared with TelegaPay, retained, and visible to staff. <br>


## Reference(s): <br>
- [TelegaPay documentation](https://telegapay.com/docs) <br>
- [python-telegram-bot documentation](https://docs.python-telegram-bot.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, SQL, API Calls, Configuration] <br>
**Output Format:** [Markdown with SQL and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes booking workflow patterns, database query templates, payment-link guidance, notification scenarios, pricing rules, and error-handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
