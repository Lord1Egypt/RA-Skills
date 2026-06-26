## Description: <br>
SkillGuard scans ClawHub skills for prompt injection and malicious content using Lakera Guard before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xmerkle](https://clawhub.ai/user/0xmerkle) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use SkillGuard to scan ClawHub skills by slug or search query before installing them, then decide whether to proceed, block installation, or explicitly override flagged results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires high-trust Apify, Lakera, webhook URL, and webhook token credentials. <br>
Mitigation: Use dedicated, rotatable credentials and a protected webhook endpoint scoped to this workflow. <br>
Risk: The skill automatically changes persistent workspace policy on first install. <br>
Mitigation: Review or remove the TOOLS.md policy write before relying on the installed skill. <br>
Risk: A passing SkillGuard result is limited to the scanned SKILL.md content and does not prove the full package is safe. <br>
Mitigation: Treat scan results as advisory and review the full artifact, scripts, and required credentials before installation. <br>


## Reference(s): <br>
- [SkillGuard Apify actor](https://apify.com/numerous_hierarchy/skill-guard-actor) <br>
- [ClawHub SkillGuard page](https://clawhub.ai/0xmerkle/skill-guard-actor) <br>
- [Integration guide](artifact/INTEGRATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls] <br>
**Output Format:** [Markdown responses with shell commands and JSON/API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APIFY_TOKEN, LAKERA_API_KEY, OPENCLAW_WEBHOOK_URL, and OPENCLAW_HOOKS_TOKEN; scan results are delivered asynchronously by webhook.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
