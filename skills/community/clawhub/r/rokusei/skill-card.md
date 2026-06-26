## Description: <br>
Rokusei calculates a Six Star Astrology profile from a birth date, including star type, polarity, life-cycle phase, destiny star, compatibility, and sakkai warnings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ikplpeter](https://clawhub.ai/user/ikplpeter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to answer birthday-based Japanese astrology prompts and generate entertainment-oriented Rokusei profiles in multiple languages. It is not intended for professional, medical, legal, financial, or other consequential advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat astrology outputs as professional or consequential advice. <br>
Mitigation: Present Rokusei results as entertainment and avoid relying on them for medical, legal, financial, employment, or relationship decisions. <br>
Risk: The skill processes birth dates and depends on an external npm package for lunar calendar calculations. <br>
Mitigation: Avoid collecting unnecessary personal data and review the npm dependency before deployment in stricter environments. <br>
Risk: Broad birthday-fortune or Japanese-astrology prompts may activate this skill unexpectedly. <br>
Mitigation: Use clear invocation criteria and confirm the user wants an entertainment astrology reading before generating a profile. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ikplpeter/rokusei) <br>
- [Publisher Profile](https://clawhub.ai/user/ikplpeter) <br>
- [Online Rokusei Tool](https://halfct.ltd/rokusei?lang=en) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON birthday-based astrology profile, with optional CLI shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a birth date only; supports multiple output languages and entertainment-oriented interpretation.] <br>

## Skill Version(s): <br>
3.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
