## Description: <br>
Universal smart routing skill that chooses the best installed skill or skill chain across mixed environments, and automatically applies OpenClaw-aware routing when an OpenClaw workspace or skill inventory is detected. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[e2e5g](https://clawhub.ai/user/e2e5g) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to choose the best installed skill or short skill chain for a request, especially when several skills overlap or a task spans multiple phases. It can route in general environments and switch to OpenClaw-aware routing when the workspace or visible skill inventory supports it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects visible skill metadata and OpenClaw environment markers, which may be sensitive in some workspaces. <br>
Mitigation: Invoke it explicitly or disable implicit invocation in workspaces where installed skill metadata or OpenClaw markers are sensitive. <br>
Risk: Recommended chains may point to downstream skills that perform browser, publishing, memory, or account-bound actions. <br>
Mitigation: Review the recommended skill or chain before allowing downstream skills to take those actions. <br>


## Reference(s): <br>
- [Smart Router Omni release page](https://clawhub.ai/e2e5g/smart-router-omni) <br>
- [Publisher profile](https://clawhub.ai/user/e2e5g) <br>
- [Ambiguity And Fallbacks](references/ambiguity-and-fallbacks.md) <br>
- [Chain Patterns](references/chain-patterns.md) <br>
- [Environment Detection](references/environment-detection.md) <br>
- [Research Notes 2026-03](references/research-notes-2026-03.md) <br>
- [Scoring Rubric](references/scoring-rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown routing decision with mode, confidence, rationale, prerequisites, fallbacks, optional chain, and clarifying questions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code, network calls, credential access, or persistence are performed by the skill itself.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
