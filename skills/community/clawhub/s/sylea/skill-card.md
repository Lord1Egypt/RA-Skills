## Description: <br>
Syléa is a French-first, English-aware personal life coach and decision assistant that analyzes dilemmas, tracks life goals across 5 psychological dimensions, runs well-being check-ins, and stores data locally in ~/.sylea/. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clotilde563](https://clawhub.ai/user/clotilde563) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use Syléa as a French-first local coaching assistant for structured dilemma analysis, long-term goal planning, and daily well-being check-ins. It saves plain Markdown notes under ~/.sylea/ so the user can track personal decisions and progress over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores personal coaching notes, goals, dilemmas, and check-ins in ~/.sylea/, which may contain sensitive personal data. <br>
Mitigation: Use it only on trusted machines, treat ~/.sylea/ as private data, and periodically review or delete stored Markdown files. <br>
Risk: Users may rely too heavily on estimated probabilities or coaching outputs for important life decisions. <br>
Mitigation: Treat the outputs as structured reflection aids, not guarantees or professional advice; the skill explicitly keeps the final decision with the user. <br>


## Reference(s): <br>
- [Syléa ClawHub listing](https://clawhub.ai/clotilde563/sylea) <br>
- [Syléa homepage](https://sylea-ai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown with comparison tables, scoring summaries, local file paths, and occasional bash setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local Markdown files under ~/.sylea/ when the user follows the skill protocols.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and changelog, released 2026-04-20) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
