## Description: <br>
Ziwei Verify calibrates birth time from verification points by searching nearby Chinese time-period offsets to improve confidence in Ziwei Doushu chart validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caojyb](https://clawhub.ai/user/caojyb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to validate Ziwei chart packets, suggest candidate birth-time corrections, and return calibrated results that can be reviewed before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes birth time, location, and astrological chart details that may be sensitive. <br>
Mitigation: Use it only when that data is appropriate to process, minimize sensitive details, and obtain user consent before sending generated prompts to external LLMs. <br>
Risk: Corrected birth times and calibration candidates can be treated as more certain than the evidence supports. <br>
Mitigation: Prefer interactive review before saving corrected birth times and expose confidence, status, warnings, and candidate details to the user. <br>
Risk: Long-running deployments may retain dialogue-session context longer than intended. <br>
Mitigation: Clear dialogue sessions after review and avoid retaining unnecessary birth-time or chart context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caojyb/ziwei-verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, structured data] <br>
**Output Format:** [JSON-style StandardDataPacket responses with optional Markdown comparison tables and verification prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return calibration status, confidence, corrected birth time, candidate lists, warnings, errors, and metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
