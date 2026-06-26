## Description: <br>
Autonomous Razorpay payment monitoring for Indian merchants. Tracks daily settlements, detects failed payments, sends WhatsApp/Telegram alerts for anomalies, and delivers weekly revenue summaries. Connects to the Razorpay API using your key and secret. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utsavs](https://clawhub.ai/user/utsavs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Indian merchants and their operators use this skill to monitor Razorpay payments, settlements, refunds, disputes, and revenue trends through scheduled reports, anomaly alerts, and on-demand commands. <br>

### Deployment Geography for Use: <br>
India <br>

## Known Risks and Mitigations: <br>
Risk: Payment-monitoring reports and anomaly alerts can contain sensitive financial, customer, refund, settlement, or dispute information. <br>
Mitigation: Configure recipients carefully, send only masked customer details, and keep alert content limited to what operators need to act. <br>
Risk: Razorpay API keys provide access to merchant payment data and must not be exposed in logs, messages, or generated output. <br>
Mitigation: Store RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET only in environment variables, avoid echoing secrets, and rotate keys if exposure is suspected. <br>
Risk: WhatsApp or Telegram delivery can send financial notifications outside the merchant's primary Razorpay dashboard. <br>
Mitigation: Use approved recipient accounts or groups, verify destinations before enabling alerts, and avoid sending unnecessary personal or payment details. <br>


## Reference(s): <br>
- [Razorpay Monitor ClawHub Release](https://clawhub.ai/utsavs/razorpay-monitor) <br>
- [Publisher Profile](https://clawhub.ai/user/utsavs) <br>
- [Razorpay API Base URL](https://api.razorpay.com/v1/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text payment reports, alert messages, command responses, Razorpay API requests, cron examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET; optional thresholds tune large-payment, failure-spike, and polling behavior; alerts may be routed through WhatsApp or Telegram.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
