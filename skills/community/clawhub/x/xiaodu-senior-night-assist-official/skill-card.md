## Description: <br>
Coordinates a low-stimulation night-assist routine for Xiaodu smart displays and IoT lights when an older adult gets up at night, using scenes first, selected lighting, short speech, and timed auto-off. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dueros-mcp](https://clawhub.ai/user/dueros-mcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with a configured Xiaodu home environment use this skill to help an older adult complete short nighttime activities, such as going to the bathroom or getting water, with restrained path lighting, brief speech, and automatic light shutoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control selected household lights and related Xiaodu devices after broad night-assist phrases. <br>
Mitigation: Install only with a trusted xiaodu-control-official setup, use wake-word or active-session gating, and review the target lights and rooms before deployment. <br>
Risk: Preference persistence can reveal household nighttime routines. <br>
Mitigation: Review or disable XIAODU_CONTEXT.md and MEMORY.md persistence when household routine privacy matters. <br>


## Reference(s): <br>
- [Usage Notes](references/usage-notes.md) <br>
- [Test Cases](references/test-cases.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dueros-mcp/xiaodu-senior-night-assist-official) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses serial execution, scene-first fallback planning, preference notes, and timed light shutoff when dependencies are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
