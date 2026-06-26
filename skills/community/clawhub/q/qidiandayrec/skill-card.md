## Description: <br>
Recommends Qidian web novels from Sanjiang new-book lists and classic high-subscription titles, with SBTI-style personalization, Markdown-ready summaries, source links, and local caching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drow931](https://clawhub.ai/user/drow931) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate personalized Qidian web-novel recommendations from current Sanjiang selections or classic high-subscription works. The skill can return concise recommendation reports with SBTI-style fit, book metadata, Qidian links, and optional IP or overseas-popularity notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically install unpinned Python packages during normal use. <br>
Mitigation: Review dependencies first, use an isolated virtual environment, and preinstall reviewed pinned packages instead of allowing runtime pip installs. <br>
Risk: The scripts may contact qidiantu.com or Qidian and write local cache and recommendation-history files. <br>
Mitigation: Run the skill only in environments where those outbound requests and local cache or history files are acceptable. <br>
Risk: Recommendation links preserve an attribution query parameter. <br>
Mitigation: Keep the parameter when attribution is desired, and review link handling if attribution tags are not appropriate for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drow931/qidiandayrec) <br>
- [Qidian data guide](artifact/references/qidian_data_guide.md) <br>
- [Qidiantu Sanjiang list data source](https://www.qidiantu.com/bang/1/6/{date}) <br>
- [Qidiantu 100k subscription badge data source](https://www.qidiantu.com/badge/shiwanjunding) <br>
- [Qidiantu 10k subscription badge data source](https://www.qidiantu.com/badge/wanrenzhuipeng) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown recommendation reports or JSON records generated from local Python scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Qidian URLs with the _trace=qidiandayrec_skill attribution parameter and local cache or history effects.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
