## Description: <br>
Exports Grok conversations from X via browser-network capture and converts them into Obsidian-ready Markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hajekt2](https://clawhub.ai/user/hajekt2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and personal knowledge-management users use this skill to capture their Grok chat history from X and convert the captured JSON into Obsidian-ready Markdown notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can export broad private Grok/X conversation history. <br>
Mitigation: Run it only in a trusted browser profile and store the JSON and Markdown outputs in protected locations, away from synced or shared folders. <br>
Risk: An interrupted capture can leave raw conversation data in browser localStorage. <br>
Mitigation: Clear the xgrok_capture_checkpoint_v1 localStorage entry after interrupted runs or before using a shared browser profile. <br>


## Reference(s): <br>
- [X Grok](https://x.com/i/grok) <br>
- [ClawHub Skill Page](https://clawhub.ai/hajekt2/x-grok-to-obsidian) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Markdown] <br>
**Output Format:** [Markdown instructions with shell command examples; scripts produce JSON captures and Markdown notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browser capture requires an authenticated X session; the converter can include reasoning traces only when requested.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
