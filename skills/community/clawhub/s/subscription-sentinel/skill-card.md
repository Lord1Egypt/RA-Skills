## Description: <br>
Subscription Sentinel is a financial data agent that scans email receipts, infers subscription billing cycles, and alerts or assists with cancellation before unwanted renewals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JoeySome](https://clawhub.ai/user/JoeySome) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users running OpenClaw use this skill to analyze recent billing email receipts, maintain a local subscription record, forecast upcoming renewals, and receive cancellation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive email receipts and billing details. <br>
Mitigation: Use it only with a trusted email integration and review the requested email access before running a scan. <br>
Risk: The skill persists inferred subscription history in subscriptions.json. <br>
Mitigation: Periodically inspect, protect, or delete subscriptions.json if retained billing history is not desired. <br>
Risk: Browser-driven cancellation can change paid services or account status. <br>
Mitigation: Require the agent to show the service, account, official site, supporting evidence, and consequences before each cancellation action. <br>
Risk: Subscription inference can be incomplete or wrong, especially for receipts routed through Apple, PayPal, or Google Play. <br>
Mitigation: Verify important findings against account pages or bank statements before relying on an alert or cancellation recommendation. <br>


## Reference(s): <br>
- [Subscription Sentinel on ClawHub](https://clawhub.ai/JoeySome/subscription-sentinel) <br>
- [JoeySome publisher profile](https://clawhub.ai/user/JoeySome) <br>
- [Declared project homepage](https://github.com/your-username/SubscriptionSentinel) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance, Shell commands] <br>
**Output Format:** [Markdown report with tables, plus a local subscriptions.json state file when persistence tools are available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires trusted email access; may use web search or browser control for cancellation assistance when explicitly authorized.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
