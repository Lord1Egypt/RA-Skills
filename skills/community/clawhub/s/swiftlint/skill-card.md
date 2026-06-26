## Description: <br>
Swift linting and style enforcement via CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexissan](https://clawhub.ai/user/alexissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run SwiftLint on Swift projects, configure linting rules, autocorrect fixable style issues, and integrate checks into Xcode or CI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SwiftLint autofix commands can modify Swift source files. <br>
Mitigation: Run lint-only commands first, scope checks with --path when possible, and review version-control diffs before accepting swiftlint --fix changes. <br>


## Reference(s): <br>
- [ClawHub Swiftlint page](https://clawhub.ai/alexissan/swiftlint) <br>
- [SwiftLint upstream repository](https://github.com/realm/SwiftLint) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown, Code] <br>
**Output Format:** [Markdown with inline shell, Swift, and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SwiftLint reporter outputs such as JSON, CSV, XML, plist, Markdown, HTML, or JUnit when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
