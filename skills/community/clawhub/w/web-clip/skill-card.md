## Description: <br>
Fetch web pages, strip to clean readable text, summarize into agent-ready markdown. Research assistant foundation. No browser required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to fetch web pages, extract readable text, convert pages to markdown, and save clipped content for research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch arbitrary URLs and save fetched page content locally. <br>
Mitigation: Review URLs before use, avoid sensitive intranet, localhost, authenticated, or private targets, and configure the cache directory intentionally. <br>
Risk: Fetched web content may be untrusted, misleading, or unsuitable for direct use in agent context. <br>
Mitigation: Treat clipped content as untrusted input and verify important claims against primary sources before acting on them. <br>
Risk: Local archives may retain sensitive, copyrighted, or unexpected page content. <br>
Mitigation: Store clips only in approved locations, restrict file access, and delete cached content that is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/web-clip) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, metadata, guidance] <br>
**Output Format:** [JavaScript objects and markdown files containing extracted page text, markdown, metadata, and optional summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local caching and archive output are supported when configured by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
