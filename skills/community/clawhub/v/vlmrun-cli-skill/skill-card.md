## Description: <br>
Use the VLM Run CLI (`vlmrun`) to interact with Orion visual AI agent for natural-language processing of images, videos, and documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spillai](https://clawhub.ai/user/spillai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to install and operate the VLM Run CLI for visual AI chat, OCR, extraction, summarization, and generation tasks over images, videos, and documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external VLM Run service and the `vlmrun[cli]` package. <br>
Mitigation: Verify that the VLM Run package and service are trusted before installing or using the CLI. <br>
Risk: The CLI requires a VLM Run API key. <br>
Mitigation: Use a dedicated API key and avoid exposing it in shared shells, logs, prompts, or committed files. <br>
Risk: Images, videos, PDFs, contracts, invoices, meeting recordings, and prompts may be externally processed and cached locally as artifacts. <br>
Mitigation: Avoid sending confidential inputs unless external processing and local artifact caching are acceptable; configure or clean the cache directory as needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spillai/vlmrun-cli-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, json, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; VLM Run CLI responses may be text, JSON, or generated artifact files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VLMRUN_API_KEY; may use VLMRUN_BASE_URL and VLMRUN_CACHE_DIR; generated artifacts can be saved locally.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
