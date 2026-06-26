## Description: <br>
Humanize generates or rewrites Chinese communication copy so it sounds more natural, less templated, and less like polished AI writing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianyidatascience](https://clawhub.ai/user/tianyidatascience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content creators, support teams, and developers use this skill to generate or rewrite Chinese customer replies, emails, social posts, status updates, and other communication copy. The skill exposes a visible baseline-to-challenger process with local scoring, keep-or-discard decisions, and report artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may route generation through the user's configured CoPaw or local OpenAI-compatible model backend and stores drafts and outputs in local run folders. <br>
Mitigation: Use the skill only when the selected model backend and filesystem retention are acceptable for the text being processed; avoid confidential customer, legal, or internal text unless approved. <br>
Risk: First-run setup installs a local Python runtime and downloads dependency and model artifacts. <br>
Mitigation: Install and run the skill in a trusted environment, and review the dependency and model download behavior before deployment. <br>


## Reference(s): <br>
- [Scoring reference](artifact/references/scoring.md) <br>
- [Preset reference](artifact/references/presets.md) <br>
- [Open-source model and dependency notes](artifact/OPEN_SOURCE.md) <br>
- [BAAI/bge-reranker-v2-m3 model card](https://huggingface.co/BAAI/bge-reranker-v2-m3) <br>
- [ClawHub skill page](https://clawhub.ai/tianyidatascience/self-evolving-humanize-zh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown process summary with generated Chinese copy, scores, JSON traces, and optional HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local run folders containing drafts, score files, session traces, selected outputs, and rendered reports.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release metadata and SKILL.md metadata.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
