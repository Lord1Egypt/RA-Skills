## Description: <br>
Zhuge Skill helps agents make football match predictions by combining sports data sources, 6-dimension scoring, a 64-hexagram decision model, local experience records, and optional LLM commentary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangfei222666-9](https://clawhub.ai/user/yangfei222666-9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to predict football matches, run batch predictions, backfill outcomes, view hit-rate statistics, and generate optional LLM-assisted reports. It is suited to decision-support workflows where predictions should remain reviewable and not be treated as guaranteed outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require sports-data API keys and optional LLM provider credentials. <br>
Mitigation: Configure only providers you trust, keep keys in local environment or .env files, and rotate keys if logs or exported files may have exposed credential-bearing URLs. <br>
Risk: Optional LLM commentary can send match context and generated prompts to the configured LLM provider or relay service. <br>
Mitigation: Use direct official provider endpoints for production workflows and avoid relay or custom base URLs unless the intermediary is trusted. <br>
Risk: Predictions, reports, exports, and experience records are decision-support artifacts and can be inaccurate or misleading. <br>
Mitigation: Review outputs before acting on them or sharing them, and treat generated predictions as advisory rather than guaranteed results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yangfei222666-9/zhuge-skill) <br>
- [README.en.md](artifact/README.en.md) <br>
- [PRIVACY.md](artifact/PRIVACY.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with optional local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local prediction history, crystal, export, error-log, and configuration files under the skill directory.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
