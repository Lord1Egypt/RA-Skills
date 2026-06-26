---
name: unitree-hermes-colab
description: Build or review a safety-gated Google Colab workflow that installs Hermes Agent and uses it for read-only Unitree Robotics repository analysis, simulation runbooks, log triage, and contribution planning. Use for Unitree, Hermes Agent, Colab, robot-safety, or Codex-skill tasks; do not use for live robot control.
metadata:
  openclaw:
    homepage: https://github.com/zack-dev-cm/unitree-g1-colab-ik
    skillKey: unitree-hermes-colab
    requires:
      bins:
        - git
      anyBins:
        - python3
        - python
    envVars:
      - name: OPENAI_API_KEY
        required: false
        description: Optional model provider key for Hermes Agent runs.
      - name: OPENROUTER_API_KEY
        required: false
        description: Optional model provider key for Hermes Agent runs.
      - name: NOUS_API_KEY
        required: false
        description: Optional Nous provider key for Hermes Agent runs.
---

# Unitree Hermes Colab

## Goal

Create or review a Colab notebook that makes Hermes Agent useful for Unitree
work without pretending Colab is a safe robot-control host. The notebook should
install or check Hermes, clone selected Unitree repositories, generate
read-only artifacts, and show clear pass/fail review gates.

## Hard Boundaries

- Do not execute robot-control commands from Colab.
- Do not publish DDS, ROS, motor, sport-mode, or low-level commands.
- Do not SSH, SCP, tunnel, or scan Unitree robot LAN addresses such as
  `192.168.123.0/24`.
- Do not claim physical hardware validation unless the user provided external
  evidence.
- Put risky local-host commands in quoted runbooks for a human to review and
  run on the correct machine.
- Hermes one-shot execution must be opt-in. It is acceptable to install Hermes
  and prepare prompts by default.

## Build Workflow

1. Keep one configuration block near the top of the notebook or runner:
   `INSTALL_HERMES`, `RUN_HERMES_AGENT`, `CLONE_UNITREE_REPOS`, `PROVIDER`,
   `MODEL`, and output directory.
2. Record runtime versions: Python, platform, GPU/CUDA when present, Hermes CLI
   status, and cloned repo commit SHAs.
3. Clone only important Unitree repositories by default:
   `unitreerobotics/xr_teleoperate`, `unitree_sdk2_python`, and
   `unitree_mujoco`.
4. Write a local `AGENTS.md` safety file before any optional Hermes run.
5. Generate these use cases at minimum:
   simulation runbook, teleoperation preflight checklist, log triage,
   contribution scouting, and IK evidence review.
6. Render user-facing outputs as a report: cards, repository map, flow
   visualization, review gates, references, and saved artifacts.
7. Save `unitree-hermes-report.md`, `unitree-hermes-review.json`, `AGENTS.md`,
   and a flow visualization.

## Output Standards

- Do not leak meta-instructions like "Notebook organization" into the report.
  Use user-facing labels such as "Review gates", "Runtime", "Use cases", and
  "References".
- Keep references limited to important sources: Hermes Agent, Hermes docs,
  Unitree repositories, and Codex skills/subagents when the artifact includes a
  Codex skill.
- Include a critical usefulness score. Good default framing:
  high value for setup review and log triage, low value for live robot control.
- Mark skipped Hermes execution clearly when no provider key is present or
  `RUN_HERMES_AGENT` is false.

## Validation

Run the project checks when working in this repo:

```bash
python3 -m py_compile src/unitree_colab_ik/hermes_lab.py src/unitree_colab_ik/hermes_cli.py notebooks/run_unitree_hermes_agent_lab.py
python3 -m json.tool notebooks/unitree_hermes_agent_lab.ipynb >/dev/null
python3 -m compileall -q src tests
python3 skill/unitree-hermes-colab/scripts/check_lab_artifacts.py <path-to-unitree-hermes-review.json>
```

Run tests if `pytest` is available:

```bash
python3 -m pytest tests/test_hermes_lab.py
```

## Subagent Review

Use Codex subagents only when the user explicitly asks for parallel/subagent
review. Keep them read-heavy. Good split:

- safety reviewer: checks no robot-control execution path exists
- notebook reviewer: checks clean-runtime reproducibility and visible outputs
- contribution reviewer: checks whether the Unitree/Hermes use cases are
  genuinely useful and small enough to publish

The main agent should wait for summaries and integrate findings. Avoid
parallel write-heavy edits unless the user explicitly requests that.
