## Description:

Tencent MPS Video Dubbing helps agents generate commands for Tencent Cloud MPS workflows that translate a video's language, optionally burn translated subtitles, and create AI-cloned dubbed audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-mpaas-skills](https://clawhub.ai/user/tencent-mpaas-skills)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers, operators, and content localization teams use this skill to generate Tencent Cloud MPS commands for end-to-end video localization from a video input to a translated, dubbed output video. It also supports command generation for dry runs, language listing, environment checks, task submission, task polling, result queries, and output download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Tencent Cloud credentials and can submit paid MPS and COS operations.

Mitigation: Use least-privilege, preferably temporary Tencent Cloud credentials; run dry runs before submission; keep budget alerts or spending limits enabled; and require explicit charge confirmation before paid processing.

Risk: The bundled scripts can automatically install or upgrade Python dependencies.

Mitigation: Run the skill in an isolated virtual environment with reviewed or pinned dependencies, or disable the auto-upgrade path before use in controlled environments.

Risk: The environment loader reads local dotenv and shell configuration files to find Tencent Cloud settings.

Mitigation: Run from trusted directories, keep secrets out of command arguments and repositories, and review local dotenv files before execution.

Risk: Video files and generated outputs are uploaded to or downloaded from Tencent Cloud COS.

Mitigation: Confirm that the selected buckets, regions, retention settings, and access policies meet the user's data handling requirements before processing media.

## Reference(s):

- [Tencent Cloud MPS Video Dubbing Parameters and Examples](references/mps_video_dubbing.md)
- [Video Dubbing ProcessMedia Request Examples](references/example.md)
- [Tencent Cloud MPS One-Stop Dubbing Integration](https://cloud.tencent.com/document/product/862/124504)
- [Tencent Cloud MPS ProcessMedia API](https://cloud.tencent.com/document/product/862/37578)
- [Tencent Cloud MPS DescribeTaskDetail API](https://cloud.tencent.com/document/api/862/37614)
- [Tencent Cloud MPS Pricing](https://cloud.tencent.com/document/product/862/36180)
- [Tencent Cloud MPS Region List](https://cloud.tencent.com/document/product/862/37572)
- [Tencent Cloud COS Region List](https://cloud.tencent.com/document/product/436/6224)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, markdown]

**Output Format:** [Markdown text with shell command snippets, task identifiers, and result links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may cover dry runs, environment checks, language listing, interactive setup, paid task submission, polling, querying, upload, and download.]

## Skill Version(s):

1.0.6 (source: evidence release, SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
