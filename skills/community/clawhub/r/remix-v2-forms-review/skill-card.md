## Description: <br>
Reviews Remix v2 form code for manual fetch() mutations, native <form> misuse, wrong useNavigation/useFetcher choice, missing pending state, unbounded uploads, and intent-pattern violations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code reviewers use this skill to inspect Remix v2 form and mutation code for framework-specific correctness, progressive enhancement, pending-state handling, upload safety, and validation issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides an agent to inspect application source code during review. <br>
Mitigation: Use it only in repositories where code review access is authorized and appropriate. <br>
Risk: Review findings can be misleading if Remix context-sensitive exceptions are skipped. <br>
Mitigation: Require file-location evidence, exemption checks, form-method checks, and the referenced review verification protocol before acting on findings. <br>


## Reference(s): <br>
- [Form vs Fetcher Misuse](references/form-vs-fetcher.md) <br>
- [Pending State Anti-patterns](references/pending-state.md) <br>
- [Uploads, FormData Validation & Optimistic State](references/uploads-validation.md) <br>
- [Multi-action Routes & Method Choice](references/multi-action-routes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown review findings with file locations, verification notes, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings should be supported by direct location evidence and context-sensitive exemption checks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
