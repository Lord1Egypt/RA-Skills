## Description: <br>
Extracts YouTube captions and summarizes video transcripts into concise overviews with main points, arguments, and conclusions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vovavvk](https://clawhub.ai/user/vovavvk) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to turn YouTube videos with available captions into structured summaries without watching the full video. It is suited for educational, news, documentary, and reference videos where transcript-based analysis is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser-exported YouTube cookies may expose authenticated account data if stored, shared, or committed carelessly. <br>
Mitigation: Use cookies only when needed, keep the cookie file outside shared or synced folders, restrict file permissions, never commit it, and delete it after use. <br>
Risk: Cached transcripts and video metadata can retain sensitive or private viewing context on disk. <br>
Mitigation: Use the skill with non-sensitive videos by default and clear the configured cache directory when transcript data should not persist. <br>
Risk: Disabled certificate checking reduces transport security during YouTube extraction. <br>
Mitigation: Review the helper script before use and prefer a version that removes certificate-check bypassing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vovavvk/tl-dw) <br>
- [Attribution](ATTRIBUTION.md) <br>
- [Original tldw project](https://github.com/stong/tldw) <br>
- [Original tldw website](https://tldw.tube) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON transcript output from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transcript summaries depend on available YouTube captions and the user's configured agent model.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
