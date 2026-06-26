## Description: <br>
Apple Design Award standard Swift/SwiftUI project validation skill that checks build status, architecture, design system usage, accessibility, internationalization, performance, native integration, and testing, then generates a consolidated report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soponcd](https://clawhub.ai/user/soponcd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use Swiftverify after feature completion, before pull-request merge, or before release to evaluate Swift and SwiftUI application quality against build, architecture, design, accessibility, internationalization, performance, native integration, and test criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release references shell scripts that were not included in the reviewed package. <br>
Mitigation: Before running any referenced command, confirm the scripts exist, are from a trusted source, and have been reviewed in the local project or CI environment. <br>
Risk: Some checks, including performance validation with Instruments, require local tooling or manual review and may not be fully automated by the skill artifact. <br>
Mitigation: Treat generated validation results as engineering guidance and verify build, accessibility, internationalization, performance, and test outcomes with the appropriate Apple tooling. <br>


## Reference(s): <br>
- [Swiftverify ClawHub release page](https://clawhub.ai/soponcd/swiftverify) <br>
- [soponcd publisher profile](https://clawhub.ai/user/soponcd) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, check tables, CI configuration snippets, and report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces validation workflow guidance and report structure; referenced quality scripts must exist in the local Swift project or CI environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
