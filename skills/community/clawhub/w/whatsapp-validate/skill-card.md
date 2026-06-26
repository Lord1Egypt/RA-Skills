## Description: <br>
Check if phone numbers exist in the local Baileys session cache. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarcosRippel](https://clawhub.ai/user/MarcosRippel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to check whether phone numbers are present in the connected account's local WhatsApp/Baileys session cache, either one at a time, in batches, or by listing cached numbers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A number reported as unknown may still have WhatsApp because the skill checks only the local session cache. <br>
Mitigation: Treat unknown results as cache misses rather than authoritative WhatsApp availability decisions. <br>
Risk: The list command can print cached phone numbers and JIDs into the agent conversation or logs. <br>
Mitigation: Run the list command only when disclosure of cached WhatsApp identifiers is intended. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON] <br>
**Output Format:** [JSON emitted by a Node.js command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are based only on the local Baileys session cache and may include cached phone numbers and JIDs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
