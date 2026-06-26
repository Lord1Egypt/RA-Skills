## Description: <br>
Repurpose one long article into platform-sized drafts for Xiaohongshu, Douyin, Weibo, and WeChat using local text rules and no API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangshengli0421](https://clawhub.ai/user/wangshengli0421) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content and marketing users can convert a PR article, blog post, or long-form draft into copy blocks sized for common Chinese social platforms. The output is intended for manual review and posting, not direct platform publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated platform copy may be inaccurate, outdated against platform norms, or misaligned with brand voice. <br>
Mitigation: Review and edit each generated section before posting. <br>
Risk: The selected source article text is read locally and included in generated output. <br>
Mitigation: Run the skill only on articles intended for repurposing and avoid sensitive or confidential source text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangshengli0421/tianshu-repurpose) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown sections written to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts UTF-8 article text from --file or --text and produces locally clipped platform drafts; no network API access is indicated.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
