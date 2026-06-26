## Description: <br>
Tencent Doc Update Watcher re-crawls Tencent Docs links, compares snapshots, and produces structured update reports for sheet, doc, and AIO links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinasilva](https://clawhub.ai/user/chinasilva) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and document owners use this skill to check configured Tencent Docs links for updates, compare the latest crawl against a prior snapshot, and generate a local manifest plus human-readable diff report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local Python workflow fetches configured Tencent Docs links with curl and writes snapshot data under the chosen workspace. <br>
Mitigation: Review the config file before running, use only links you are authorized to check, and choose a private workspace for generated snapshots. <br>
Risk: Using --keep-raw can retain raw page, header, and cookie data locally. <br>
Mitigation: Avoid --keep-raw unless debugging requires it, and delete raw files after use if they may contain sensitive document or session data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chinasilva/tencent-doc-update-watch) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Tencent Docs update checker script](artifact/scripts/check-qq-doc-updates.py) <br>
- [Default Tencent Docs config](artifact/references/default-docs.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python shell commands, JSON configuration examples, and generated JSON manifest plus Markdown report artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The update workflow writes snapshots under the selected workspace and deletes raw fetched HTML, opendoc, header, and cookie files by default unless raw debugging output is explicitly enabled.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
