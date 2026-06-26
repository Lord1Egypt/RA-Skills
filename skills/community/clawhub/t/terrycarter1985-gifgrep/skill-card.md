## Description: <br>
Search, preview, download, and process GIFs from Tenor and Giphy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search GIF providers, preview GIF results, download selected GIFs, and extract frames or frame sheets for media workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external gifgrep CLI installed through Homebrew or Go. <br>
Mitigation: Verify the CLI source and chosen install method before deployment, especially when using a moving '@latest' Go install. <br>
Risk: Tenor and Giphy API keys may be provided to improve provider access or rate limits. <br>
Mitigation: Use dedicated API keys with the minimum practical access and rotate them according to local credential policy. <br>
Risk: Download and processing actions can write GIF or image files to user-provided paths. <br>
Mitigation: Review requested output paths before execution and keep generated media inside approved workspace locations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/terrycarter1985-gifgrep) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/terrycarter1985) <br>
- [GifGrep project link from skill metadata](https://github.com/steipete/gifgrep) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with command parameters and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create GIF, PNG, or frame-sheet files at user-requested output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
