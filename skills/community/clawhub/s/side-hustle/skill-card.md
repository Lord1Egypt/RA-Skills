## Description: <br>
Search for side hustle opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to initiate browser-based searches for side hustle or part-time income opportunities when prompted by broad English or Chinese phrases. Review the external browser-search dependency before using the skill in sensitive environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may open a browser and search the web when broad money-related phrases are used. <br>
Mitigation: Install only where this behavior is expected, and review or narrow triggers before use in sensitive environments. <br>
Risk: The packaged skill delegates behavior to an external browser-search function that is not included in the artifact. <br>
Mitigation: Review or obtain the referenced capabilities_clawhub.py and capability_executor.py implementations before deployment. <br>
Risk: The skill documentation contains unrelated learned content that may confuse users about intended behavior. <br>
Mitigation: Use a cleaned version of the skill documentation and remove unrelated learned content before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/side-hustle) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/534422530) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Markdown or plain text response summarizing search results and next actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May open a browser and search the web; packaged behavior delegates to an external function not included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
