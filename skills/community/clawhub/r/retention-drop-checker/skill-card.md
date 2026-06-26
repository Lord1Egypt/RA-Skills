## Description: <br>
Diagnose why short-video retention drops and suggest practical fixes. Use when views start but audience leaves early. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Leooooooow](https://clawhub.ai/user/Leooooooow) <br>

### License/Terms of Use: <br>
CC BY-NC-SA 4.0 <br>


## Use Case: <br>
Content teams, growth marketers, and short-video creators use this skill to diagnose early, mid-video, CTA, or completion-rate drop points from scripts, retention clues, or structured retention exports. It turns the diagnosis into concrete edits, a next-script skeleton, and an optional Python analysis script when structured data is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Python analysis scripts may be unsafe or unsuitable if run without review on local retention data. <br>
Mitigation: Review any generated Python script before execution and run it in an appropriate local environment. <br>
Risk: Heuristic retention diagnosis can be mistaken for precise retention modeling when structured data is not provided. <br>
Mitigation: Label qualitative findings as heuristic and reserve data-backed claims for structured retention exports or timestamped segment data. <br>
Risk: Part of the workflow starts in Chinese, which may be unsuitable for users expecting another language. <br>
Mitigation: Ask the agent to switch language explicitly before beginning the retention analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Leooooooow/retention-drop-checker) <br>
- [Output template](artifact/references/output-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with diagnostic tables, action lists, script skeletons, and optional Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Distinguishes heuristic diagnosis from data-backed analysis when structured retention data is unavailable.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
