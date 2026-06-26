## Description: <br>
紫微斗数双人合盘：先以 zwds-cli 各排一盘，再将两份 data 送入 hepan-cli 得 0-100 匹配分、维度分项与 hits。用户提及合盘、配对、缘分指数、双人紫微匹配时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luyao-inc](https://clawhub.ai/user/luyao-inc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to calculate and explain Zi Wei Dou Shu compatibility for two people from zwds-cli chart data. It returns a structured compatibility score, dimension scores, confidence, and evidence hits for cautious cultural or entertainment interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes personal birth and chart data through a local Node.js astrology calculator. <br>
Mitigation: Run it locally, share only the minimum required birth or chart data, and avoid treating outputs as psychological, legal, investment, or life-decision advice. <br>
Risk: A non-default or untrusted rule_version can change which local rule pack is loaded and alter the compatibility calculation. <br>
Mitigation: Prefer the default compat/v1 rule pack unless the local rule files are trusted; maintainers should add explicit rule allowlisting or path containment checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luyao-inc/zwds-hepan-openclaw) <br>
- [zwds-hepan reference](artifact/reference.md) <br>
- [compat/v1 rule pack](artifact/hepan-cli/src/rules/compat/v1.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON CLI inputs and outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local 0-100 compatibility score with dimension scores, confidence, hits, and penalties from two zwds-cli chart data JSON objects.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, hepan-cli/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
