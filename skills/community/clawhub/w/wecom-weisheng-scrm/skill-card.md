## Description: <br>
Built for WeCom customer operations, helping teams review customer and group activity, prepare campaign assets, and move follow-up, messaging, and opportunity workflows forward. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangfang19](https://clawhub.ai/user/fangfang19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer operations, sales, and service teams use this skill to query and manage WeCom SCRM data such as customers, tags, groups, campaign materials, follow-ups, chat archives, contacts, opportunities, reports, drawings, and schedules. The agent can guide authorized users through environment checks, identity checks, API discovery, controlled API calls, and structured result review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive WeCom SCRM APP KEY and can access business customer data. <br>
Mitigation: Use a least-privilege APP KEY, avoid shared machines, and rotate the key if it may have appeared in logs or transcripts. <br>
Risk: Some workflows can perform write-capable business actions such as creating, editing, deleting, or sending data. <br>
Mitigation: Require explicit user confirmation before write operations and avoid automatic retries after write failures. <br>
Risk: Disabling SSL verification can expose credentials and business data in transit. <br>
Mitigation: Do not enable SCRM_SKIP_SSL_VERIFY except in a controlled internal environment with a reviewed network path. <br>
Risk: Uploaded files may become publicly reachable through returned media URLs. <br>
Mitigation: Treat uploaded files as potentially public and avoid uploading sensitive content unless the sharing behavior is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fangfang19/wecom-weisheng-scrm) <br>
- [Weisheng Open Platform](https://open.wshoto.com) <br>
- [CLAW API summary](https://open.wshoto.com/doc/pages/claw/CLAW_SUMMARY.md) <br>
- [Agent runbook](references/agent-runbook.md) <br>
- [Usage guide](references/guide.md) <br>
- [Examples](references/examples.md) <br>
- [File utilities](references/file-utils.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and structured JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Python CLI commands, WeCom SCRM credentials, remote API documentation, cached identity and token data, and optional image upload/download workflows.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence; artifact frontmatter says 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
