## Description: <br>
Checks whether an AI agent skill is safe before installing or using it by querying the PYX Scanner API for trust status, risk score, and safety recommendation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fysoul17](https://clawhub.ai/user/fysoul17) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to check a skill identifier before installing or using it, then review a concise safety verdict and scanner summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The curl fallback can place user-controlled skill identifiers into a shell command without strict validation. <br>
Mitigation: Use ordinary owner/name identifiers only, validate or URL-encode each identifier part before network calls, and prefer WebFetch when available. <br>
Risk: Scanner errors, rate limits, or missing records can leave the target skill unverified. <br>
Mitigation: Treat ERROR and UNSCANNED results as unverified and manually review the target skill before installing or using it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fysoul17/pyx-scan) <br>
- [PYX Scanner](https://scanner.pyxmate.com) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Structured markdown safety report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Verdict labels include SAFE, OUTDATED, CAUTION, FAILED, UNSCANNED, and ERROR; empty source-data sections are omitted.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
