## Description: <br>
A Vedic astrology (Jyotish) analyzer that estimates sidereal birth-chart placements and produces Nakshatra, Vimshottari Dasha, and Navagraha interpretations from user-provided birth details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eamanc-lab](https://clawhub.ai/user/eamanc-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to request self-reflection-oriented Jyotish readings from birth date, birth time, and birthplace. Agents use it to produce approximate chart summaries, Dasha timelines, and interpretive guidance while disclosing calculation limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save birth date, birth time, birthplace, timezone, and chart estimates in a local MEMORY.md file for reuse. <br>
Mitigation: Use only when local reuse is acceptable; review or delete MEMORY.md in shared environments or keep readings session-only. <br>
Risk: Chart positions are approximate and may be wrong near sign boundaries or when precise degree-level placements are needed. <br>
Mitigation: Label positions as estimates and recommend verification with a dedicated astronomical engine for precision-sensitive readings. <br>
Risk: Astrology output can be overread as certainty or professional advice. <br>
Mitigation: Keep interpretations exploratory, preserve user agency, and avoid medical, legal, financial, fatalistic, or fear-based claims. <br>


## Reference(s): <br>
- [Vedic Astrology Calculation Rules](references/calculation-rules.md) <br>
- [Vedic Astrology Interpretation Guide](references/interpretation-guide.md) <br>
- [Project homepage](https://github.com/eamanc-lab/fortune-telling-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, files] <br>
**Output Format:** [Markdown report with optional local MEMORY.md profile and chart cache] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should label chart positions as approximate and avoid fatalistic or professional-advice claims.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
