## Description: <br>
Build and run a low-friction movie/anime recommendation and follow-up loop that adapts from watched, unfinished, dropped, and rejected-title feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GloryXia](https://clawhub.ai/user/GloryXia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who want ongoing movie and anime recommendations use this skill to receive one title at a time, record lightweight viewing feedback, and adapt future picks over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can keep a small long-term media-preference history for recommendations and reminders. <br>
Mitigation: Choose where any JSON or SQLite record is stored, avoid private identifiers, and periodically review or delete the record when long-term tracking is no longer wanted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/GloryXia/screen-recommendation-loop) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with lightweight record schemas and follow-up prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May maintain a small JSON or SQLite preference record when the user chooses to keep long-term taste history.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
