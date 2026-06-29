## Description: <br>
Automates Xiaohongshu content operations across topic discovery, style reference collection, draft writing, user-approved publishing, and performance tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators, creators, and agent users use this skill to run a Xiaohongshu posting workflow for a configured product. It helps collect candidate topics, analyze reference writing style, draft platform-native content, publish only after user approval, and track post performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates a logged-in Xiaohongshu creator browser session and can reach publish or reply actions. <br>
Mitigation: Use Xiaohongshu-scoped requests, keep the account browser session limited to the intended account, and review every publish or reply confirmation before allowing the action. <br>
Risk: The skill stores account configuration, drafts, screenshots, published-note records, comments, and analytics in the local workspace. <br>
Mitigation: Run it from an appropriate working directory, review files under workspaces/xhs-posting/, and avoid sharing that workspace without checking for account or campaign data. <br>
Risk: Automated posting can create platform, compliance, or account-quality issues if content limits and originality checks are skipped. <br>
Mitigation: Follow the built-in posting frequency, no-contact-info, no-external-link, originality, image-rights, and approval gates before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/skills/xiaohongshu-auto-posting) <br>
- [Xiaohongshu Creator Center](https://creator.xiaohongshu.com/new/home) <br>
- [Phase 1 topic collection reference](references/phase1-topic-collection.md) <br>
- [Phase 2 style case collection reference](references/phase2-case-collection.md) <br>
- [Phase 4 writing guidelines](references/phase4-writing.md) <br>
- [Phase 5 publishing reference](references/phase5-publish.md) <br>
- [Phase 6 tracking reference](references/phase6-tracking.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated local JSON, Markdown, screenshots, drafts, publish records, reply drafts, and reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a logged-in browser session and writes runtime data under workspaces/xhs-posting/ in the user's working directory; publishing and comment replies require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
