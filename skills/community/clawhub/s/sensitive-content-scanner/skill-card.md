## Description: <br>
This skill scans local documents for sensitive content, prohibited words, and PII using built-in rules, custom keywords, or a data dictionary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qinkai25](https://clawhub.ai/user/qinkai25) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, document reviewers, compliance teams, and security auditors use this skill to scan selected local documents for PII, sensitive words, and prohibited content before sharing or publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports can contain local file paths and sensitive matches. <br>
Mitigation: Scan only intended files or directories and keep generated reports private. <br>
Risk: A broad trigger phrase or recursive directory scan can process more private content than intended. <br>
Mitigation: Invoke the skill with explicit scan targets and avoid broad private directories unless that scope is intended. <br>
Risk: The optional encrypted dictionary format should not be treated as strong secrecy. <br>
Mitigation: Treat encrypted dictionaries as convenience packaging and avoid placing secrets in dictionaries unless separately protected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qinkai25/sensitive-content-scanner) <br>
- [PII personal information recognition patterns](references/pii_patterns.md) <br>
- [Sensitive words hash list](references/sensitive_words_hashed.txt) <br>
- [Custom words example](assets/custom_words_example.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [HTML, Markdown, or JSON report files plus concise terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports summarize matched files, sensitive-content categories, confidence or risk levels, and optional custom dictionary scores.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release evidence and scan_sensitive.py header) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
