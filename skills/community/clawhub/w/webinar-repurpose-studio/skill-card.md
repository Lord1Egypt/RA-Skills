## Description: <br>
Transforms webinar source material into reviewable Markdown drafts for replay descriptions, short copy, social outlines, FAQs, follow-up emails, and repurposing suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content marketers, and event operators use this skill to turn webinar topics, transcripts, and highlighted segments into structured, reviewable content assets for post-event reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes webinar material locally, which may include unpublished, personal, or sensitive content. <br>
Mitigation: Keep unpublished or personal material out unless necessary, use explicit input and output paths, and review drafts before publishing or sending. <br>
Risk: Generated repurposed content may be mistaken for publication-ready copy without human review. <br>
Mitigation: Treat outputs as reviewable drafts, verify facts against the provided source material, and do not use the skill to invent guest details or disclose non-public information. <br>
Risk: The bundled script includes unused audit helper code outside the primary drafting workflow. <br>
Mitigation: Use the documented drafting commands and do not modify the bundled specification to audit arbitrary directories unless that behavior is intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/webinar-repurpose-studio) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [Artifact README](artifact/README.md) <br>
- [Output template](artifact/resources/template.md) <br>
- [Structured output spec](artifact/resources/spec.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown drafts, optional JSON, and local command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reviewable drafts and explicit confirmation items; local script requires python3 and uses only standard-library dependencies according to the release evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
