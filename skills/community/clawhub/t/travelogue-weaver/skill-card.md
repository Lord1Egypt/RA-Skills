## Description: <br>
智能旅游记录 helps an agent manage a local multimedia travel journal, organize moments into a timeline, generate narrative travelogues, and export them as Markdown, HTML, or PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ludiansheng](https://clawhub.ai/user/ludiansheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-assistant agents use this skill to start and end trips, record text, image, audio, and video moments, generate a polished travelogue from the trip timeline, and export the result for review or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local journal may contain travel messages, uploaded media, timestamps, locations, and EXIF metadata. <br>
Mitigation: Install only when local storage of this information is acceptable, and remove sensitive media or metadata before sharing outputs. <br>
Risk: Markdown, HTML, and PDF exports may include identifying travel details or unsafe embedded HTML from notes. <br>
Mitigation: Review exported files before sharing or opening them in sensitive environments. <br>
Risk: Delete and export actions can remove local journal data or disclose a complete trip record. <br>
Mitigation: Confirm delete and export requests deliberately before running the related commands. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ludiansheng/travelogue-weaver) <br>
- [Data model reference](references/data_model.md) <br>
- [Narrative guide](references/narrative_guide.md) <br>
- [Export format specification](references/export_format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated Markdown, HTML, or PDF travelogue files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores trip records, uploaded media, timestamps, locations, and optional EXIF metadata in local travelogue_data files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
