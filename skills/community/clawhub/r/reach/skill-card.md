## Description: <br>
Agent web interface. Browse websites, fill forms, login to services, sign transactions, send/receive email, solve CAPTCHAs, and interact with the web autonomously. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[potdealer](https://clawhub.ai/user/potdealer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use Reach to give AI agents web browsing, form interaction, authentication, email, observation, wallet signing/payment, and MCP tool access for web workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform high-authority actions such as wallet signing, token payments, login/session use, outbound email, CAPTCHA solving, and webhook-driven automation. <br>
Mitigation: Use isolated test wallets and test accounts first, and require explicit approval gates before signing, payment, login, cookie import, email, CAPTCHA solving, or webhook-triggered actions. <br>
Risk: Cookies, API-key sessions, inbox contents, form data, recordings, screenshots, and local state may be persisted and should be treated as sensitive. <br>
Mitigation: Protect access to the data directory, avoid production private keys, and regularly clear saved sessions, cookies, recordings, inbox data, and form memory. <br>
Risk: Webhook and email handlers can receive external events that may influence agent behavior. <br>
Mitigation: Expose webhook listeners only in controlled environments, validate event sources, and keep webhook-triggered actions behind human or policy approval. <br>
Risk: The supplied test report shows authentication and click-navigation failures in some real-world flows. <br>
Mitigation: Test target workflows before relying on them, and require human review for login and navigation flows until site-specific reliability is confirmed. <br>


## Reference(s): <br>
- [Reach ClawHub listing](https://clawhub.ai/potdealer/reach) <br>
- [Reach README](artifact/README.md) <br>
- [Reach test report](artifact/TEST-REPORT.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, API Calls] <br>
**Output Format:** [Markdown or JSON responses, shell command output, screenshots, and local state/session files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist cookies, API sessions, inbox contents, form memory, recordings, screenshots, and state under local data storage when those features are used.] <br>

## Skill Version(s): <br>
0.2.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
