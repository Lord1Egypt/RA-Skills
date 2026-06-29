## Description: <br>
Designs or implements a bilingual K12 paper-exam grading workflow that uses scans, teacher answer keys, OCR/vision providers, deterministic scoring, review queues, reports, and separated teacher/student memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[addogiavara-tech](https://clawhub.ai/user/addogiavara-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers, school IT staff, and developers use this skill to design or implement K12 scan-to-grade workflows for paper exams and homework. It helps plan student page grouping, OCR/AI provider adapters, answer-key-based scoring, teacher review queues, Excel/Web/PDF exports, printable student reports, and separate teacher/student memory archives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may require sensitive OCR/AI provider credentials. <br>
Mitigation: Have users configure their own provider credentials and store them with the host application's secure storage mechanism; do not hardcode credentials in skill files, code, logs, or exported reports. <br>
Risk: Cloud OCR or AI calls may upload exam images or student information to selected vendors. <br>
Mitigation: Show what data is uploaded for each provider, provide privacy modes such as local-only or hybrid review, and require compliance with school, privacy, and vendor policies. <br>
Risk: Automated extraction or grading can be incorrect, especially for low-confidence OCR, provider disagreement, missing pages, or subjective answers. <br>
Mitigation: Use the teacher-confirmed answer key as the scoring authority, keep an exception review queue, and make final scores traceable to the original image, provider result, normalized answer, rule, and teacher correction. <br>
Risk: Teacher memory and student learning archives can expose private educational records if mixed or exported carelessly. <br>
Mitigation: Keep teacher and student memory in separate structures, avoid including real private data in the skill package, and preserve clear input, working, output, and memory boundaries. <br>


## Reference(s): <br>
- [Teacher Grading Pipeline Design Reference](artifact/references/design.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/addogiavara-tech/u-autoclaw-teacher-grading-pipeline) <br>
- [U-AutoClaw Project Website](https://www.wboke.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with structured workflow steps, JSON schemas, configuration examples, shell-command suggestions, and report-template guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include bilingual English/Chinese guidance; users supply their own OCR/AI provider credentials and teacher-confirmed answer keys.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
