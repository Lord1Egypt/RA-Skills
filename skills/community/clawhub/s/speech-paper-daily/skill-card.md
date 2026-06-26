## Description: <br>
Finds recent speech and audio arXiv preprints, reads relevant papers, summarizes methods and results in Chinese with a 10-point expert score, and creates a Tencent Docs report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JusperLee](https://clawhub.ai/user/JusperLee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate daily Chinese briefings on current arXiv speech and audio papers, including paper metadata, technical analysis, source links, demo or code links when present, and expert ratings. The skill can publish the report to a configured Tencent Docs folder or return the report in chat if publishing fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create Tencent Docs reports through a local account and fixed destination folder. <br>
Mitigation: Confirm the Tencent Docs account and folder ID YUsookchBhki are the intended destination before invoking the publishing step. <br>
Risk: Generated paper summaries, classifications, links, and ratings may be incomplete or inaccurate. <br>
Mitigation: Review the cited arXiv pages, source paper text, and generated ratings before sharing or relying on the report. <br>
Risk: The workflow may write temporary files and execute a helper Python script to publish the report. <br>
Mitigation: Inspect generated files and commands, and run the skill only in an environment where local file creation and Tencent Docs side effects are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JusperLee/speech-paper-daily) <br>
- [arXiv cs.SD new submissions](https://arxiv.org/list/cs.SD/new) <br>
- [arXiv eess.AS new submissions](https://arxiv.org/list/eess.AS/new) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Chinese Markdown or MDX report with paper metadata, links, summaries, technical analysis, experiment notes, and scores.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write temporary Markdown and Python helper files, call a local Tencent Docs integration, and create smartcanvas documents in a configured folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
