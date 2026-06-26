## Description: <br>
Detects repeated queries as implicit negative feedback and non-repetition as positive feedback, enabling continuous learning by writing reflections and patterns to MEMORY.md and SOUL.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KAVentures](https://clawhub.ai/user/KAVentures) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Reflexlearn to capture implicit feedback from repeated or non-repeated prompts and convert it into memory entries, pending behavior updates, and learned response patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores raw prompts and derived interaction history, which may include secrets, personal data, or sensitive work. <br>
Mitigation: Avoid enabling it for sensitive prompts unless appropriate; regularly inspect and prune ~/.openclaw/reflex_history.json and MEMORY.md. <br>
Risk: The skill can modify long-term agent behavior through MEMORY.md, pending SOUL.md updates, and heartbeat reinforcement. <br>
Mitigation: Use cautious mode, review pending updates before applying them, and inspect SOUL.md after heartbeat runs. <br>
Risk: Optional Ollama reflection sends prompt text to a local service. <br>
Mitigation: Use --use-ollama only when the local Ollama service and model are trusted. <br>
Risk: Model dependencies and weights are downloaded during installation. <br>
Mitigation: Run install.sh only after reviewing its declared PyPI and Hugging Face network operations; use --offline at runtime once weights are cached. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KAVentures/reflex-learn) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [sentence-transformers/all-MiniLM-L6-v2 model](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) <br>
- [Ollama](https://ollama.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown entries and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes interaction history, reflections, pending updates, and learned patterns under ~/.openclaw/.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
