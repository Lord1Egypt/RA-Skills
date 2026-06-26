## Description: <br>
Provides SMS compliance, formatting, and delivery best practices for the Sendly API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sendly-live](https://clawhub.ai/user/sendly-live) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external teams use this skill when building Sendly SMS features that need compliant phone formatting, message classification, opt-out handling, quiet-hours behavior, delivery preparation, and error handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SMS compliance rules, Sendly behavior, and pricing can change after release. <br>
Mitigation: Verify current legal requirements and Sendly documentation before using the guidance for production messaging. <br>
Risk: Incorrectly treating marketing messages as transactional can lead to consent, quiet-hours, or opt-out failures. <br>
Mitigation: Review message type, recipient consent, opt-out status, and recipient local time before sending marketing traffic. <br>


## Reference(s): <br>
- [Sendly compliance docs](https://sendly.live/docs/concepts/compliance) <br>
- [Sendly quiet hours](https://sendly.live/docs/quiet-hours) <br>
- [Sendly country requirements](https://sendly.live/docs/country-requirements) <br>
- [Sendly opt-out handling](https://sendly.live/docs/how-to/handle-opt-outs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with inline API paths, error codes, and reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only guidance; no code execution or credential access.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
