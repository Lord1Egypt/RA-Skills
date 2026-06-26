## Description: <br>
Transforms AI-GEO brand assets into Zhihu-style questions, answers, article drafts, topic suggestions, and publishing checklists for human review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ljseeking](https://clawhub.ai/user/ljseeking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Brand teams, founders, and AI-GEO operators use this skill to convert prepared brand, FAQ, keyword, and source-material assets into Zhihu-ready Q&A and article drafts. The intended workflow keeps drafting assisted while final factual review, disclosure checks, formatting, and publishing remain human decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a no-ad rewrite flow and may be used to make brand content less visibly promotional on Zhihu. <br>
Mitigation: Use it only for human-reviewed, disclosure-compliant drafting, and do not use the rewrite flow to hide sponsorship, evade moderation, or make promotional content appear independent. <br>
Risk: The browser-assist script interacts with a logged-in Zhihu session and can be affected by page changes, verification prompts, or platform controls. <br>
Mitigation: Run only the visible local browser flow, avoid storing cookies or browser storage, stop for verification challenges, and let a human complete review, saving, and publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ljseeking/zhihu-geo-draft-assistant) <br>
- [Skill overview](artifact/SKILL.md) <br>
- [Safety rules](artifact/automation/safety_rules.md) <br>
- [Playwright draft flow](artifact/automation/playwright_draft_flow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown drafts, prompt instructions, checklist content, and optional Python/Playwright command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are draft materials for human review; the browser helper fills visible draft editors but does not publish.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and CHANGELOG, released 2026-05-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
