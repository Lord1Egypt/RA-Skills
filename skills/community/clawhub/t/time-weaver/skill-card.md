## Description: <br>
Time Weaver helps authors create exploratory time-travel fiction through choice-driven story setup, chapter generation, state tracking, publishing, and EPUB export workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harry720320](https://clawhub.ai/user/harry720320) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External authors and writing assistants use this skill to plan, generate, continue, publish, and export branching Chinese time-travel novels. The workflow maintains book state in Markdown files, generates new chapters with choice points, and can publish chapters to the Time Weaver website when configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated chapters may be uploaded to the Time Weaver website as part of the normal chapter workflow. <br>
Mitigation: Disable or avoid auto-publishing unless online publication is intended, and require explicit user confirmation before each upload. <br>
Risk: The publishing flow stores the Time Weaver API key in a local plaintext configuration file. <br>
Mitigation: Use a throwaway or least-privilege API key, rotate it regularly, and delete the local configuration when publishing is no longer needed. <br>
Risk: Generated story state, chapters, and publishing status are written to local workspace files. <br>
Mitigation: Review generated files before sharing or publishing, especially if drafts include private prompts, names, or unpublished story material. <br>


## Reference(s): <br>
- [Time Weaver ClawHub listing](https://clawhub.ai/harry720320/time-weaver) <br>
- [Publisher profile: harry720320](https://clawhub.ai/user/harry720320) <br>
- [Time Weaver publishing site](https://time-weaver-782300018128.us-west1.run.app/) <br>
- [Character Generator Reference](references/character-generator.md) <br>
- [Era Settings Reference](references/era-settings.md) <br>
- [Maoni Style Reference](references/maoni-style.md) <br>
- [Protagonist Templates Reference](references/protagonist-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown prose and state files, shell commands, local configuration, and optional EPUB files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write book state under .learnings/books, store publishing status, store a local API key configuration, upload chapter content when publishing is enabled, and export EPUB files.] <br>

## Skill Version(s): <br>
0.7.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
