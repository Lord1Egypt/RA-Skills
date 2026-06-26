## Description: <br>
Drafts ASAM criteria-aligned individualized treatment plans for substance use disorder clients, including level-of-care rationale, DSM-5-TR diagnosis documentation, SMART goals, interventions, discharge criteria, and clinician review prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External addiction counselors, behavioral health clinicians, SUD treatment teams, and documentation specialists use this skill to draft structured treatment plans for licensed clinician review, signature, and local workflow adaptation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft clinical content may be incomplete, incorrect, or unsuitable for a specific client. <br>
Mitigation: Require review, modification, and signature by an appropriately licensed clinician before clinical, billing, authorization, or medical-record use. <br>
Risk: Patient identifiers or protected SUD treatment information could be entered into an agent conversation. <br>
Mitigation: Use initials or case numbers only, omit direct identifiers, and follow 42 CFR Part 2 confidentiality requirements before sharing any draft output. <br>
Risk: The draft may imply a diagnosis, ICD-10-CM code, or ASAM level of care that has not been clinically confirmed. <br>
Mitigation: Flag assumptions and unresolved items for clinician confirmation, and keep diagnosis and coding entries as draft material until confirmed by the responsible clinician. <br>
Risk: Medication-assisted treatment details could be misused as prescribing guidance. <br>
Mitigation: Do not recommend initiation or dosing; refer medication decisions to a licensed prescriber such as a physician or APRN. <br>
Risk: Crisis, overdose, or imminent-harm disclosures require immediate local response rather than document drafting. <br>
Mitigation: Pause plan drafting and direct the clinician to agency crisis protocol and local emergency services until safety is confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/sud-treatment-plan-drafter) <br>
- [README](artifact/README.md) <br>
- [Skill source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown draft treatment plan with structured sections, open questions, and clinician review block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [All clinical output is labeled as draft material for licensed clinician review and signature.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence and changelog, released 2026-05-29) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
