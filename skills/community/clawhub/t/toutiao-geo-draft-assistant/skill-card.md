## Description: <br>
Transforms structured brand content into plain-language, scenario-based Toutiao draft assets and can assist with filling a visible local browser draft for human review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ljseeking](https://clawhub.ai/user/ljseeking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
B2B teams, founders, and content operators use this skill to adapt structured brand knowledge into Toutiao-friendly articles, titles, summaries, cover prompts, micro-posts, keyword suggestions, and publish checklists. Users can also run a local Playwright helper to paste draft content into Toutiao while keeping final review and publishing manual. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a visible browser while the user is logged into Toutiao and fill content into a draft editor. <br>
Mitigation: Run the helper locally in a virtual environment, keep the browser visible, and manually review the title, article, cover, and facts before saving or publishing. <br>
Risk: Generated content may contain factual errors, overclaims, or platform-sensitive marketing language. <br>
Mitigation: Use the generated publish checklist and quality review prompts to verify facts, remove exaggerated claims, and confirm platform fit before publishing. <br>
Risk: Changing the helper into an auto-publishing or session-saving tool would increase account and platform compliance risk. <br>
Mitigation: Keep final publishing manual and do not add behavior that saves credentials, stores browser sessions, bypasses verification, or clicks publish automatically. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ljseeking/toutiao-geo-draft-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/ljseeking) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [User documentation](artifact/README.md) <br>
- [Automation safety rules](artifact/automation/safety_rules.md) <br>
- [Playwright draft flow](artifact/automation/playwright_draft_flow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown drafts, prompt outputs, checklist files, and optional shell commands for a local Playwright helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated assets are intended for human review before any Toutiao save or publish action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
