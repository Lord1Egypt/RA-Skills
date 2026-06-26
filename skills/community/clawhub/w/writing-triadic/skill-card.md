## Description: <br>
Writing Triadic is a privacy-focused three-role writing framework that helps agents mine intent, generate draft variants, evaluate them from a reader perspective, and maintain consent-gated writing preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sallyface0](https://clawhub.ai/user/sallyface0) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and writing-focused agents use this skill to plan, draft, revise, score, and personalize content across blogs, essays, business copy, resumes, long-form documents, SEO content, and social posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent writing profiles and session folders may retain sensitive drafts, resumes, reports, style fingerprints, or SEO history. <br>
Mitigation: Use local privacy mode for sensitive content, and inspect or delete MEMORY.md, session folders, style fingerprints, and SEO profiles regularly. <br>
Risk: The skill makes broad local-only privacy claims while substantial writing context may be routed through remote model sub-agents by default. <br>
Mitigation: Review the skill before installing, avoid confidential material unless the runtime is appropriate, and keep sub-agent context limited to the current task. <br>
Risk: Web research can send topic-derived search keywords to external services. <br>
Mitigation: Decline web research when privacy matters and approve only search queries that are safe to transmit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sallyface0/writing-triadic) <br>
- [Publisher profile](https://clawhub.ai/user/sallyface0) <br>
- [README_EN.md](artifact/README_EN.md) <br>
- [PRIVACY.md](artifact/PRIVACY.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>
- [Template library](artifact/references/template-library.md) <br>
- [Style cloning guide](artifact/references/style-cloning-guide.md) <br>
- [SEO module](artifact/references/seo-module.md) <br>
- [State contract](artifact/references/state-contract.md) <br>
- [Model configuration](artifact/references/model-config.md) <br>
- [InkOS architecture reference](https://github.com/Narcooo/inkos) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Files] <br>
**Output Format:** [Markdown drafts, review notes, writing plans, session state, and preference update guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local writing workspace files such as MEMORY.md, session-state.md, drafts, reviews, and final copy.] <br>

## Skill Version(s): <br>
2.9.2 (source: server release evidence, SKILL.md frontmatter, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
