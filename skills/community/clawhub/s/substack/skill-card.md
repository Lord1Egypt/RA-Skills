## Description: <br>
Publish, edit, and manage Substack posts for the Alternative Partners publication via Substack's internal REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[breynol01](https://clawhub.ai/user/breynol01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators and publishing agents use this skill to create drafts, publish posts, update existing posts, retrieve post IDs, and manage Alternative Partners Substack publishing workflows without browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or edit live Substack content using a long-lived session cookie. <br>
Mitigation: Install only for users authorized to operate the Alternative Partners Substack, store SUBSTACK_SID in a secrets manager, and require explicit preview plus approval naming the target post before live publish or edit actions. <br>
Risk: Plain-text conversion produces simple paragraph-only Substack bodies, so formatting such as headings, lists, links, and emphasis may be lost. <br>
Mitigation: Review rendered drafts before publication and use a richer ProseMirror conversion path when formatted content is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/breynol01/substack) <br>
- [Alternative Partners Substack](https://alternativepartners.substack.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, API Calls] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce draft or published Substack post URLs and requires a SUBSTACK_SID session cookie supplied through a secrets manager.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
