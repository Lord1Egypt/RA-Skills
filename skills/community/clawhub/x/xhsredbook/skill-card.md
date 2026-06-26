## Description: <br>
Automatically publishes notes to Xiaohongshu creator center by generating template-based content, creating cover images, and driving a Playwright browser session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HarveyZzzz](https://clawhub.ai/user/HarveyZzzz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators, operators, and social media teams use this skill to prepare Xiaohongshu posts, generate square cover images, and publish image-text notes through a logged-in creator account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish live Xiaohongshu posts through a logged-in creator browser session without a final confirmation step. <br>
Mitigation: Review generated titles, body text, and images before execution, and run the publishing scripts only against the intended account and browser profile. <br>
Risk: Saved browser profiles, screenshots, or debug HTML may contain account, session, or draft-post information. <br>
Mitigation: Use a dedicated browser profile, protect or delete saved login profiles when finished, and periodically clear screenshots and debug HTML. <br>
Risk: Template-generated social content may be inaccurate, misleading, or inconsistent with the publisher's brand requirements. <br>
Mitigation: Edit and approve the generated post content and cover images before allowing the automation to publish. <br>


## Reference(s): <br>
- [XHS_Content productionandpublishing on ClawHub](https://clawhub.ai/HarveyZzzz/xhsredbook) <br>
- [Xiaohongshu Creator Center Publish Page](https://creator.xiaohongshu.com/publish/publish) <br>
- [Selector Reference](references/selectors.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and generated local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Xiaohongshu post titles, body text, cover images, screenshots or debug artifacts, and browser automation actions when scripts are executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
