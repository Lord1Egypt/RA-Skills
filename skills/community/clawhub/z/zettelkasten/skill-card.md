## Description: <br>
A card-box note-taking skill that captures ideas, generates structured Markdown cards, suggests tags and insights, detects connections, and supports daily review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rainy-cogmet](https://clawhub.ai/user/rainy-cogmet) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to record personal knowledge as structured Zettelkasten cards, receive generated insights and related suggestions, and review saved notes over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local note persistence can store personal ideas in zettelkasten_<user_id>_db.json. <br>
Mitigation: Run the skill only in an approved local workspace and avoid entering sensitive notes unless local storage is acceptable. <br>
Risk: The bundle includes publish.sh, which can use ClawHub credentials to upload the current folder. <br>
Mitigation: Do not run publish.sh unless you intentionally want to publish the package and have reviewed the exact directory contents and credential use. <br>


## Reference(s): <br>
- [README.en.md](artifact/README.en.md) <br>
- [README.md](artifact/README.md) <br>
- [ClawHub release page](https://clawhub.ai/rainy-cogmet/zettelkasten) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [Markdown note cards with YAML-style metadata and text prompts; local JSON persistence for saved cards.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local zettelkasten_<user_id>_db.json files for stored cards.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact/clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
