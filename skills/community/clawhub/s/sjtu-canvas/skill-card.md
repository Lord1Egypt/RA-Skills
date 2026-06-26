## Description: <br>
Helps agents manage Canvas LMS course data for SJTU or other Canvas instances, including course files, assignments, deadlines, grades, discussions, and study material extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xhh678876](https://clawhub.ai/user/xhh678876) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, instructors, and agent users working with Canvas LMS use this skill to retrieve course materials, inspect assignments, deadlines, grades, and discussions, extract PPT/PDF/DOCX content to Markdown, and optionally submit assignments or sync deadlines to Apple Calendar. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses private Canvas course data through a user-provided Canvas API token. <br>
Mitigation: Use the least-privilege Canvas token available, store it only in the local config file, and rotate or revoke it when it is no longer needed. <br>
Risk: Calendar sync and assignment submission can change user-visible external state. <br>
Mitigation: Review changes before execution, avoid untrusted course or assignment names for calendar sync, and require explicit user confirmation before submitting assignments. <br>
Risk: Security evidence flags unresolved assignment-submission issues, including syntax, confirmation, file-scope, and destination-validation gaps. <br>
Mitigation: Do not use assignment submission until those gaps are fixed and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xhh678876/sjtu-canvas) <br>
- [SJTU Canvas instance](https://oc.sjtu.edu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with Python/API results, file paths, and extracted course-material content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce downloaded course files, extracted Markdown, Apple Calendar events, and Canvas assignment submissions when the user configures credentials and invokes those workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
