## Description: <br>
Audit and improve SwiftUI runtime performance from code review and architecture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soponcd](https://clawhub.ai/user/soponcd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose slow SwiftUI rendering, janky scrolling, high CPU or memory use, excessive view updates, and layout thrash. It guides code review first and asks the user to collect Instruments traces when code review alone is insufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may share proprietary source code, customer data, screenshots, or performance traces while requesting an audit. <br>
Mitigation: Share only relevant code and trace excerpts, and redact secrets, customer data, and unrelated proprietary information before using the skill. <br>
Risk: Performance recommendations may be incomplete or incorrect without runtime measurements. <br>
Mitigation: Validate proposed fixes with the same baseline capture and compare CPU, frame drops, memory, and responsiveness before adopting changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/soponcd/timeflow-swiftui-performance-audit) <br>
- [Publisher Profile](https://clawhub.ai/user/soponcd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with analysis, issue lists, Swift code examples, metrics tables, and remediation steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request user-provided SwiftUI code, reproduction steps, screenshots, or Instruments traces; no executable payload is included.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
