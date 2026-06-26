## Description: <br>
Checks Chinese web novel chapters for banned words, repetitive phrasing, chapter continuity, outline alignment, character consistency, pacing, terminology, and worldbuilding issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chn012cjus](https://clawhub.ai/user/chn012cjus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External authors, editors, and publishing assistants use this skill to review Chinese web novel chapters before publication. It produces structured quality findings and rewrite guidance for prohibited terms, repeated phrasing, continuity, outline fit, character consistency, pacing, terminology, and worldbuilding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local scanner reads manuscript files selected by the user and writes excerpts or findings to a local freq_result.txt file. <br>
Mitigation: Run it only on intended manuscript files and delete old freq_result.txt outputs when switching projects or handling sensitive drafts. <br>
Risk: The skill's strict quality rules may produce recommendations that do not match an author's intended style or narrative voice. <br>
Mitigation: Treat findings as review guidance and have a human author or editor approve changes before publication. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chn012cjus/web-novel-publishing-readiness-and-quality-check-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown quality report with line-numbered findings and local text scan output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The local Python scanner reads a selected manuscript file and writes freq_result.txt in the skill directory.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
