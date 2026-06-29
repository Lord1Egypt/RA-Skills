## Description: <br>
Run durable long-running research in OpenClaw using isolated cron iterations, persistent state, bounded execution, and milestone updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vkambulov](https://clawhub.ai/user/vkambulov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and OpenClaw operators use this skill to run long-running, evidence-heavy research tasks that need scheduled bounded iterations, persistent source and finding logs, pause/resume/stop controls, review gates, and final reports or deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research traces and task workspaces may contain sensitive sources, findings, generated reports, chat identifiers, or local configuration. <br>
Mitigation: Keep research roots and task workspaces out of public commits, review deliverables before sharing, and redact local paths or owner-specific identifiers in public summaries. <br>
Risk: Scheduled cron iterations can continue across hours or days and may consume resources or continue work after conditions change. <br>
Mitigation: Use the skill's pause, resume, stop, unschedule, status, summary, health, and queue-status controls to inspect and manage active tasks. <br>
Risk: Task-local runtime preparation can install additional Python packages when requested. <br>
Mitigation: Install packages only into the task-local runtime and approve unusual or risky dependencies from a trusted operator workflow before use. <br>
Risk: Retrieved web pages, PDFs, emails, and files may contain untrusted instructions or misleading content. <br>
Mitigation: Treat retrieved material as evidence rather than instructions, prefer direct sources, and require review-gated finalization before user-facing delivery. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vkambulov/research-mode) <br>
- [Research Mode CLI Surface](docs/CLI.md) <br>
- [Research Mode State Versioning](docs/STATE_VERSIONING.md) <br>
- [Architecture](ARCHITECTURE.md) <br>
- [Security Policy](SECURITY.md) <br>
- [Examples](examples/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and operator guidance with JSON task state, JSONL evidence logs, shell commands, and task-local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates persistent research task directories, append-only sources and findings logs, iteration notes, worker result JSON, review-ready deliverables, and optional task-local analysis artifacts.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata, released 2026-06-22) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
