## Description: <br>
Plan-aware UseClick link-shortening and analytics API workflows for geo links, affiliate links, link management, QR generation, and custom/branded domains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[petercsipkay](https://clawhub.ai/user/petercsipkay) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to build UseClick.io integrations that create and manage short links, fetch analytics, configure geo-targeting, and adapt workflows to plan limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: UseClick API keys could be exposed if pasted into chat, logs, or source files. <br>
Mitigation: Store API keys in environment variables or a secret manager and avoid sharing real tokens in prompts, logs, or code examples. <br>
Risk: Update and delete workflows can change links or remove analytics in a UseClick account. <br>
Mitigation: Explicitly confirm update or delete actions before executing them and review affected slugs and target URLs. <br>
Risk: Plan-limited features may fail or produce unusable workflows when a requested feature is unavailable. <br>
Mitigation: Check pricing and feature gates before suggesting advanced fields, and provide a compatible fallback or upgrade path. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/petercsipkay/useclick-link-shortening-analytics) <br>
- [UseClick API Reference](references/api.md) <br>
- [UseClick Pricing And Limits](references/pricing-and-limits.md) <br>
- [Integration Workflows](references/workflows.md) <br>
- [UseClick Website](https://useclick.io) <br>
- [UseClick Pricing](https://useclick.io/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with API examples, cURL commands, JSON payloads, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include plan-aware fallbacks, rate-limit handling guidance, and credential-handling reminders.] <br>

## Skill Version(s): <br>
1.0.5 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
