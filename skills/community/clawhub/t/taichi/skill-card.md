## Description: <br>
Taichi is a Redis-based multi-agent workflow framework that supports centralized, distributed, and hybrid execution modes across Planner, Drafter, Validator, and Dispatcher stages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indivisible2025](https://clawhub.ai/user/indivisible2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Taichi to run multi-agent task workflows through centralized, distributed, or hybrid modes backed by a Redis message bus. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags broad local command execution and weak safety checks. <br>
Mitigation: Install only in an isolated development environment and do not use untrusted task text until shell execution is disabled or sandboxed and task payloads are authenticated and validated. <br>
Risk: The skill can install and start Redis locally and uses Redis-backed worker coordination. <br>
Mitigation: Run it only where Redis service changes are acceptable, and avoid shared or production Redis instances unless install, start, and stop behavior is explicitly user-controlled. <br>
Risk: Uninstall behavior can delete the configured Taichi workspace. <br>
Mitigation: Set a dedicated workspace and review workspace contents before running uninstall commands. <br>


## Reference(s): <br>
- [Taichi Framework README](artifact/taichi-framework/README.md) <br>
- [ClawHub skill page](https://clawhub.ai/indivisible2025/taichi) <br>
- [Publisher homepage](https://github.com/Indivisible2025/Cloudfin) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and text output from local workflow runs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.9+, Redis, and a local virtual environment.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
