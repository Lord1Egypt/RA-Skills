## Description: <br>
Cross-platform skill dependency doctor for preflight checks of missing binaries, version mismatches, system libraries, CJK fonts, Playwright and Chromium runtime, and project-level dependencies before skills run. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RangeKing](https://clawhub.ai/user/RangeKing) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill before running agent skills to inspect runtime dependency readiness across binaries, versions, system libraries, fonts, Playwright and Chromium, project dependency manifests, and CI baselines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The fallback Python wrapper can import and run a same-named package from the current working directory. <br>
Mitigation: Prefer the installed skill-deps-doctor command from a trusted or pinned PyPI source, and run the fallback wrapper only from trusted directories. <br>
Risk: Third-party plugin checkers and generated fix scripts can execute or suggest environment changes that are outside the core skill. <br>
Mitigation: Use --no-plugins unless third-party checkers are trusted, and inspect any generated fix.sh before executing it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/RangeKing/skill-deps-doctor) <br>
- [Publisher Profile](https://clawhub.ai/user/RangeKing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; optional JSON, fix scripts, snapshots, and dependency graph outputs from the underlying CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate fix scripts, snapshots, baseline reports, or DOT/tree dependency graphs when requested; generated shell scripts should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
