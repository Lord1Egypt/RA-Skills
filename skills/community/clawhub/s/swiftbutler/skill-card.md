## Description: <br>
Analyze, syntax-check, reindent, and distribute Swift source code with the SwiftButler CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill while working with Swift files or packages to inspect API shape, run quick syntax checks, normalize indentation, split large generated Swift files, and verify the SwiftButler CLI setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to run local SwiftButler and Homebrew commands that can read project files or modify Swift source indentation and distribution. <br>
Mitigation: Review proposed commands before execution and use dry-run or output options before allowing in-place source changes. <br>
Risk: Generated CLI output can be reused by agents for code edits, so incorrect or stale API summaries could lead to poor changes. <br>
Mitigation: Prefer structured JSON or YAML output for downstream parsing and rerun syntax checks before accepting generated Swift changes. <br>


## Reference(s): <br>
- [SwiftButler ClawHub listing](https://clawhub.ai/odrobnik/swiftbutler) <br>
- [SwiftButler project homepage](https://github.com/Cocoanetics/SwiftButler) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide use of SwiftButler outputs in interface, JSON, YAML, or Markdown formats.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
