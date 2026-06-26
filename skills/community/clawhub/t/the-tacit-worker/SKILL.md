---
name: ai-engineering-os
description: >
  A unified AI Engineering Operating System that orchestrates the full lifecycle
  of agent creation - extracting tacit knowledge, structuring the Agent OS, and
  enforcing pre-deployment governance. Use this skill to build production-ready,
  context-aware agents that are immune to AI Execution Hallucination and the
  Expertise Paradox.
---

# AI Engineering Operating System (The Unified Architecture)

This skill represents a paradigm shift from "Prompt Engineering" to "Knowledge Engineering." It combines three foundational capabilities—Tacit Knowledge Extraction, Agent OS Architecture, and Anti-Micromanagement Governance—into a single, self-improving cognitive architecture.

## The Six Paradigm Shifts

1. **From Prompt Engineering to Knowledge Engineering**: The prompt is the last step. The real work is upstream extraction and structuring.
2. **From Agent as Tool to Agent as Apprentice**: The agent interviews the master (SECI model), learns the craft, and operates under supervision.
3. **From Trust by Default to Trust by Proof**: Trust is an engineering artifact earned through the Mandatory Proof of Action Protocol.
4. **From One-Shot to Living Configuration**: The agent's OS is a living document that evolves through continuous feedback.
5. **From Automation to Augmented Cognition**: Human judgment and agent capability are structurally interleaved.
6. **From Scaling Agents to Scaling Intent**: You are not scaling compute; you are scaling the human's extracted judgment.

## The Unified Workflow

When tasked with building or deploying a new AI agent, execute this three-phase pipeline:

### Phase 1: The Extraction Interview (Tacit Knowledge Extractor)
Do not accept vague prompts. Ask the user for a concrete past example of the task.
Conduct a structured interview using the `references/extraction_framework.md` to map workflows, decision rules, and edge cases.
Synthesize the answers and generate the `templates/tacit_profile_template.md`.
*Crucial Step: You must pause and ask the user to confirm the synthesis before proceeding.*

### Phase 2: The OS Build (Agent OS Builder)
Convert the confirmed Tacit Profile into a structured, version-controllable file system.
Generate the core OS files using the templates in `templates/os_files/`:
- `SOUL.md`: Personality and boundaries.
- `AGENTS.md`: Step-by-step workflows and IF/THEN decision rules.
- `USER.md`: User preferences and quality standards.
- `HEARTBEAT.md`: Periodic task checklist.
- `TOOLS.md`: Authorized tools and constraints.

### Phase 3: The Pre-Deployment Audit (Anti-Micromanagement Guard)
Before the agent is allowed to execute tasks, enforce the governance framework using `references/governance_checklist.md`.
Ensure the agent is configured to follow the **Mandatory Proof of Action Protocol**: every completion claim must include an exact file path, actual content confirmation, and a timestamp.
Run the `scripts/verify_action.py` script to validate the agent's output.

## The Self-Improving Feedback Loop

This unified system learns from its own deployments. After every full cycle:
1. **Extraction Loop**: Did the user have to correct the synthesis in Phase 1? If yes, update the `extraction_framework.md` with better probing questions.
2. **Architecture Loop**: Were any OS files missing necessary context in Phase 2? If yes, update the OS templates.
3. **Governance Loop**: Did the agent attempt to hallucinate execution in Phase 3? If yes, strengthen the `governance_checklist.md`.

## Resources

- **References**: `extraction_framework.md`, `os_architecture_guide.md`, `governance_checklist.md`
- **Templates**: `tacit_profile_template.md`, `audit_report_template.md`, and the `os_files/` directory.
- **Scripts**: `verify_action.py` (The Proof of Action validator).
