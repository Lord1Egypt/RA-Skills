## Description: <br>
Analyzes sleep data from EDF, BDF, and GDF files and returns sleep-stage, respiratory, stress, and related sleep-health guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[znsyhandao](https://clawhub.ai/user/znsyhandao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to analyze sleep-study files, keep analysis results in session memory, and export selected results when explicitly requested. It is intended for sleep-quality exploration and operational review, not as a substitute for clinical judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server security evidence marks this release suspicious because the artifacts are internally inconsistent and include undisclosed file and environment access. <br>
Mitigation: Review the source and run the skill only in a sandbox with non-sensitive test data before installation or production use. <br>
Risk: Server security guidance states that the main skill appears broken and that some modules may create or export sensitive analysis files outside the behavior promised in documentation. <br>
Mitigation: Validate command execution and monitor filesystem writes, especially output and export paths, before allowing access to real sleep-study data. <br>
Risk: The artifact contains conflicting documentation about output directories, including safe_outputs, analysis_outputs, skill-directory output, and user-specified export locations. <br>
Mitigation: Treat documented storage claims as untrusted until the exact write paths are confirmed from the packaged source and runtime behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/znsyhandao/sleep-rabbit-plugin) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [SECURITY_TRUTH.md](artifact/SECURITY_TRUTH.md) <br>
- [SECURITY_STATEMENT.md](artifact/SECURITY_STATEMENT.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>
- [clawhub.json](artifact/clawhub.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Guidance] <br>
**Output Format:** [Plain text or Markdown-style command responses, with optional JSON export files for selected analysis results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Handles user-provided sleep-study files and may create analysis outputs or exports when enabled or explicitly requested.] <br>

## Skill Version(s): <br>
5.3.4 (source: server release metadata, artifact clawhub.json, config.yaml, skill.py, and CHANGELOG.md; server release created 2026-04-22) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
