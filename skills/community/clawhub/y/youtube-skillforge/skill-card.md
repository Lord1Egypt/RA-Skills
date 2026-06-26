## Description: <br>
Turn YouTube videos into structured, reusable skill files that make any AI agent smarter. Forge, compound, and recall creator-attributed knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[koren-source](https://clawhub.ai/user/koren-source) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to turn YouTube transcripts into structured, reusable skill files, then search or serve those local skills for later agent recall. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release depends on an external npm package and a yt-dlp installation source. <br>
Mitigation: Install only after confirming that the package and yt-dlp source are trusted for the target environment. <br>
Risk: Generated video-derived skills persist locally and may influence future agent recall. <br>
Mitigation: Review saved skills before relying on them or making them available to an agent. <br>
Risk: The skill writes a local library, configuration, proposals, and SQLite search index under ~/.skillforge/. <br>
Mitigation: Use the first-run consent prompt and explicit output paths to control where generated files are stored. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/koren-source/youtube-skillforge) <br>
- [youtube-skillforge npm package](https://www.npmjs.com/package/youtube-skillforge) <br>
- [yt-dlp Homebrew formula](https://formulae.brew.sh/formula/yt-dlp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown skill files, CLI text, MCP JSON-RPC tool responses, and local SQLite index data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated skill library, proposals, configuration, and search index under ~/.skillforge/ unless the user supplies an explicit output path.] <br>

## Skill Version(s): <br>
4.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
