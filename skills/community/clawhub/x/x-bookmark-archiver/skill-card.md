## Description: <br>
Fetches X bookmarks, categorizes linked content, optionally generates OpenAI summaries, and saves organized markdown archives in an OpenClaw workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Iamadig](https://clawhub.ai/user/Iamadig) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and individual users use this skill to turn their X bookmarks into categorized local knowledge files with optional AI-generated titles, summaries, and tags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads bookmarks from the authenticated X account and writes bookmark data locally. <br>
Mitigation: Install and run it only for accounts whose bookmarks are appropriate to archive, and review generated X-knowledge and state files when bookmarks may include sensitive links. <br>
Risk: Optional OpenAI summarization can send bookmark URLs and tweet text to OpenAI. <br>
Mitigation: Leave OPENAI_API_KEY unset to use local fallback metadata, or set it only when external summarization is acceptable. <br>


## Reference(s): <br>
- [X Bookmarks Archiver on ClawHub](https://clawhub.ai/Iamadig/x-bookmark-archiver) <br>
- [bird CLI](https://github.com/steipete/bird) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files with YAML frontmatter, plus command-line status output and setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Archives are written under X-knowledge categories; state files track pending and processed bookmark IDs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
