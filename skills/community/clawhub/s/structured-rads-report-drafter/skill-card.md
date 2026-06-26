## Description: <br>
Use this skill when a radiologist, fellow, resident, or radiology PA needs to draft a structured report aligned to an ACR RADS lexicon, with lexicon-controlled findings and an unsigned attending sign-out block for radiologist review before clinical action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Radiologists, radiology trainees, radiology PAs/RAs, and structured-reporting teams use this skill to draft lexicon-aligned radiology report text from raw findings, technique details, and prior comparisons. The output is a draft for attending radiologist review, not a final clinical report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft report text could be mistaken for final clinical documentation. <br>
Mitigation: Require attending radiologist review and retain the draft-only sign-out language before any clinical use. <br>
Risk: Users could enter direct patient identifiers into the agent conversation. <br>
Mitigation: Use accession-number-only workflows and refuse patient name, MRN, DOB, SSN, and full date-of-service. <br>
Risk: RADS lexicons, ACR guidance, and institutional reporting requirements can change. <br>
Mitigation: Verify current lexicon editions, ACR guidance, and local policy before using any drafted report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/structured-rads-report-drafter) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown draft report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft-only radiology report text with PHI-minimization prompts, lexicon citations, unresolved-information flags, and attending-review sign-out language.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence and changelog, released 2026-05-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
