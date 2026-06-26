## Description: <br>
Xiamen Tide Calculator helps agents calculate tide times for Xiamen waters and provide beachcombing advice, including lunar date conversion, tide-size classification, scoring, location recommendations, equipment suggestions, and safety reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingwingshome](https://clawhub.ai/user/kingwingshome) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer Xiamen tide queries, compare beachcombing windows, and produce practical outing guidance for specific solar or lunar dates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tide and beachcombing guidance may not reflect official tide tables, current weather, or on-site conditions. <br>
Mitigation: Treat results as advisory and confirm plans with official tide tables, weather forecasts, and local observations. <br>
Risk: The skill runs local Python scripts and depends on the zhdate package for lunar date conversion. <br>
Mitigation: Install dependencies in a virtual environment and review generated guidance before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingwingshome/xiamen-tide-calculator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style tide reports, beachcombing recommendations, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory output based on local Python calculations for requested dates and modes.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
