## Description: <br>
Tracks a user-provided topic by researching recent sources, identifying timely hot topics, drafting a long-form article, and fact-checking the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianheihei002](https://clawhub.ai/user/tianheihei002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, editors, analysts, and agents use this skill to turn a current topic into a researched source report, a short list of timely angles, a long-form article, and a fact-check report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs web research on user-provided topics, which can expose sensitive private topics through search queries. <br>
Mitigation: Avoid using sensitive private topics unless the user is comfortable with those terms being searched. <br>
Risk: The skill creates dated Markdown and optional DOCX article files, and may update article content during fact-checking. <br>
Mitigation: Check the workspace for existing article files with the same date before running the skill. <br>
Risk: Scheduled runs may reuse the previous tracking topic, which can continue work on stale or unintended subjects. <br>
Mitigation: Confirm the intended tracking topic before enabling or executing scheduled runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianheihei002/yq-hot-topic-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/tianheihei002) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown reports and article content, with an optional DOCX article file when a conversion tool is available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a tracking summary, hot-topic list, saved dated article file, and fact-check report.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
