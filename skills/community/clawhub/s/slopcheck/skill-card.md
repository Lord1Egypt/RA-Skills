## Description: <br>
Validate npm package references in markdown, YAML, and config files against the live npm registry to catch hallucinated, slopsquatted, or security-held packages before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mattschaller](https://clawhub.ai/user/mattschaller) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and maintainers use slopcheck before installing, committing, or reviewing AI-generated documentation and configuration files that mention npm packages. It helps identify nonexistent package names and npm security holds before those references are trusted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the recommended npx command executes external npm package code. <br>
Mitigation: Use a trusted or pinned slopcheck version when provenance matters, and review the command before execution. <br>
Risk: Registry checks can disclose private or internal package names to the npm registry. <br>
Mitigation: Avoid scanning files with private package names unless the scope is limited or the documented ignore option is used. <br>
Risk: A package existing on npm does not prove that it is safe, compatible, or appropriate to install. <br>
Mitigation: Treat slopcheck as an existence check and use package security tools for dependency risk, version, and malware review. <br>


## Reference(s): <br>
- [slopcheck documentation](https://github.com/mattschaller/slopcheck) <br>
- [ClawHub release page](https://clawhub.ai/mattschaller/slopcheck) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI reports verified packages, missing packages, security holds, source locations, and exit codes.] <br>

## Skill Version(s): <br>
0.1.2 (source: evidence.release.version and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
