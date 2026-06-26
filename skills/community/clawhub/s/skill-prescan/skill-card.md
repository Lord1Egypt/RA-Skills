## Description: <br>
Pre-scan a SKILL.md locally before publishing to ClawHub. Simulates the ClawScan security review using the same prompt and evaluation criteria as the real scanner. Use when you want to check if your skill will pass ClawHub's security review before uploading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanningwang](https://clawhub.ai/user/hanningwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to run a local pre-scan of a SKILL.md before publishing to ClawHub. It helps them understand likely security review outcomes and privacy considerations before upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A scanned SKILL.md is sent to the configured remote LLM provider, which may log, cache, or retain transmitted content. <br>
Mitigation: Use the skill only with content you are comfortable disclosing, review the provider's retention terms, avoid secrets or proprietary material, and use a dedicated API key where possible. <br>
Risk: Local pre-scan results are advisory and may differ from ClawHub's production security review. <br>
Mitigation: Treat results as guidance, review the full skill artifact separately, and rely on ClawHub's hosted review before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanningwang/skill-prescan) <br>
- [ClawHub repository homepage](https://github.com/openclaw/clawhub) <br>
- [ClawScan security prompt reference](https://github.com/openclaw/clawhub/blob/main/convex/lib/securityPrompt.ts) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal text or JSON, with Markdown usage guidance in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a configured remote LLM endpoint; only the target SKILL.md content is sent for analysis.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
