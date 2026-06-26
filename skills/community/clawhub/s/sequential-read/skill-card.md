## Description: <br>
Read prose sequentially with structured reflections to simulate the reading experience. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[horace-claw](https://clawhub.ai/user/horace-claw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to have an agent read long-form prose in order, preserve chunk-level reactions, and synthesize the evolving reading experience into a final report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected source text and generated reflections are stored locally under memory/sequential_read. <br>
Mitigation: Use the skill only with documents suitable for local retention, and delete session folders when the retained text or reflections are no longer needed. <br>
Risk: Hand-crafted path-like session IDs could make local session handling harder to reason about. <br>
Mitigation: Use generated session IDs and avoid manually supplied path-like identifiers. <br>


## Reference(s): <br>
- [Sequential Read release page](https://clawhub.ai/horace-claw/sequential-read) <br>
- [horace-claw publisher profile](https://clawhub.ai/user/horace-claw) <br>
- [Agentic Sequential Reading](https://doi.org/10.5281/zenodo.18596456) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown synthesis with local session files, chunk reflections, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores per-session chunks, reflections, annotations, state, and final synthesis under memory/sequential_read/<session-id>/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
