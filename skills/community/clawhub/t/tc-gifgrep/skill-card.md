## Description: <br>
Search, preview, download, and process GIFs from Tenor and Giphy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search GIF providers, retrieve GIF URLs or downloads, and create still frames or frame sheets for media workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and invokes an external gifgrep CLI package. <br>
Mitigation: Verify the external CLI source before installing and prefer pinned versions when possible. <br>
Risk: GIF provider searches can send query text to Tenor or Giphy. <br>
Mitigation: Avoid sensitive project names, credentials, or private data in GIF search terms. <br>
Risk: Provider API keys may be exposed if reused broadly or handled carelessly. <br>
Mitigation: Use only Tenor or Giphy API keys intended for this tool and manage them through the agent environment. <br>
Risk: Downloaded GIFs and generated image files write to local paths. <br>
Mitigation: Save outputs only to safe workspace directories and review generated files before sharing or reusing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/tc-gifgrep) <br>
- [Publisher Profile](https://clawhub.ai/user/terrycarter1985) <br>
- [GifGrep CLI Source Referenced by Artifact](https://github.com/steipete/gifgrep) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown, JSON-like tool call examples, CLI output, GIF files, PNG frames, and PNG frame sheets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gifgrep CLI; optional GIPHY_API_KEY and TENOR_API_KEY environment variables can improve provider access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
