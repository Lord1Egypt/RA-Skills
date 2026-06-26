## Description: <br>
Slogan Maker helps agents generate brand taglines, industry slogans, rhyming slogans, bilingual slogan translations, slogan tests, and reference examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, marketing teams, and agents use this skill to draft, translate, compare, and test short advertising slogans for brands and common industries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes an unrelated data-processing helper script alongside the slogan-writing script. <br>
Mitigation: Review the extra script before installation and prefer invoking artifact/scripts/slogan.sh directly for slogan workflows. <br>
Risk: The unrelated helper script can store the first argument locally in a history file. <br>
Mitigation: Do not pass confidential brand plans, credentials, file paths, or sensitive business text to artifact/scripts/script.sh. <br>
Risk: Generated slogans and heuristic scores may be unsuitable, misleading, or culturally inappropriate without review. <br>
Mitigation: Review candidate slogans with humans and test them with the intended audience before public or commercial use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/slogan-maker) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [Slogan Maker tips](artifact/tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables, plain text, and shell command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Slogan generation and scoring are heuristic and should be reviewed before public use.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
