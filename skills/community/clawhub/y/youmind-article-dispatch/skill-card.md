## Description: <br>
Dispatches a single content topic across multiple publishing platforms, coordinating YouMind research, platform-specific adaptation, draft or publish actions, and aggregated dispatch results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindy-youmind](https://clawhub.ai/user/mindy-youmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, developer advocates, and publishing teams use this skill to turn one topic into platform-specific articles, newsletters, posts, or threads and dispatch them through connected YouMind platform accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can coordinate posting through multiple connected accounts, increasing the impact of an incorrect target, accidental broadcast, or unsuitable localization. <br>
Mitigation: Confirm target platforms before dispatch, prefer draft mode first, and review adapted content before live publishing. <br>
Risk: The skill may use prior YouMind materials to personalize content and can persist writing profiles, rosters, and learning logs under ~/.youmind. <br>
Mitigation: Review what source material is used, keep shared profile files under user control, and inspect or remove ~/.youmind/author-profile.yaml, dispatch-roster.yaml, and learning-log.yaml when persistent profiling is not desired. <br>
Risk: Publishing depends on sensitive YouMind API credentials and connected platform accounts. <br>
Mitigation: Use only trusted environments, validate connected accounts before publishing, and avoid exposing YOUMIND_API_KEY or connector access in shared logs or files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindy-youmind/youmind-article-dispatch) <br>
- [YouMind API key settings](https://youmind.com/settings/api-keys?utm_source=youmind-article-dispatch) <br>
- [YouMind connector settings](https://youmind.com/settings/connector) <br>
- [Dispatch protocol](shared/DISPATCH_CONTRACT.md) <br>
- [Publishing guidelines](shared/PUBLISHING.md) <br>
- [YouMind home directory convention](shared/YOUMIND_HOME.md) <br>
- [Platform registry](references/platform-registry.md) <br>
- [Content brief format](references/content-brief-format.md) <br>
- [Author profile specification](references/author-profile-spec.md) <br>
- [Content adaptation matrix](references/content-adaptation-matrix.md) <br>
- [Profile learning](references/profile-learning.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance, API calls] <br>
**Output Format:** [Markdown summaries, platform-specific content, YAML configuration updates, and publishing status links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May coordinate draft or live publishing through connected YouMind accounts and persist roster/profile files under ~/.youmind.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
