## Description: <br>
Search for a text pattern in files within a directory, showing matching lines with filenames and line numbers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinwangmok](https://clawhub.ai/user/jinwangmok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other users can use this skill to locate where a word, phrase, or pattern appears across files in a chosen directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searching broad home, configuration, credential, or private project directories can expose matching lines in the session output. <br>
Mitigation: Limit searches to the specific directory needed for the task and avoid sensitive folders unless output disclosure is acceptable. <br>
Risk: Searches are case-sensitive and may miss expected matches when casing differs. <br>
Mitigation: Tell users that matching is case-sensitive and adjust the pattern or command options when case-insensitive search is required. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text search results and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Matching output follows FILENAME:LINE_NUMBER:MATCHING_LINE when grep finds matches.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
