## Description: <br>
Converts uploaded novels or story text into structured film script material, including character profiles, episode outlines, and storyboard/script excerpts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liyayong000-sketch](https://clawhub.ai/user/liyayong000-sketch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill to transform source manuscripts or stories into screenplay planning assets through the Zeelin service. The agent uploads a supported document, submits a script-generation job, polls for completion, and formats the returned result as Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded documents and the Zeelin App-Key are sent to a plain-HTTP IP service. <br>
Mitigation: Use only non-sensitive documents unless the publisher and endpoint are trusted and verified; prefer a dedicated low-privilege App-Key. <br>
Risk: Script generation may deduct Zeelin credits from the user's account. <br>
Mitigation: Confirm expected credit usage before submitting jobs and follow the documented polling interval to avoid unnecessary cost. <br>
Risk: Private or proprietary manuscripts may be exposed to an external service with unclear data-handling terms. <br>
Mitigation: Avoid private manuscripts until the service provides verified HTTPS and clearer retention and handling commitments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liyayong000-sketch/zeelin-script-gen-skill) <br>
- [Zeelin platform](https://skills.zeelin.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with structured sections and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Formats only fields returned by the service and may save the final result as an md file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
