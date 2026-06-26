# Skill Creator

A specialized tool for scoping, drafting, and iteratively improving AI skills. It provides a structured workflow to transform user intent into high-quality, benchmarked agent instructions.

## 🌟 Overview

`skill-creator` is part of the **Universal Skill Management (USM)** ecosystem. While `skill-manager` handles distribution and `skill-installer` handles acquisition, `skill-creator` is the engine for **development and quality assurance**.

## 🔄 The Development Lifecycle

1. **Capture Intent**: Identify what the skill should enable the AI to do.
2. **Scaffold**: Generate the `SKILL.md` and `meta.yaml` structure.
3. **Benchmark**: Run parallel evaluations (with-skill vs. baseline) to measure performance.
4. **Iterate**: Improve instructions based on qualitative feedback and quantitative metrics.
5. **Optimize**: Refine the skill description for better triggering accuracy.

## 🛠 Features

- **Progressive Disclosure Support**: Drafts skills that utilize specialist agents and deep references.
- **Automated Testing**: Built-in support for spawning subagents to run test cases.
- **Eval Viewer**: A web-based interface for comparing different iterations of a skill.
- **Description Optimizer**: Uses LLM-driven loops to maximize triggering reliability.

## 📖 Ecosystem Integration

After creating a skill with `skill-creator`, you should use **[skill-manager](https://github.com/ZiweiAxis/skill-manager)** to:
- Configure the skill's visibility (`scope`).
- Synchronize symbolic links across all your agent platforms (Cursor, Claude Code, etc.).

## 🏗 Directory Structure
- `agents/`: Specialist subagents for grading and analysis.
- `scripts/`: Python scripts for running loops, benchmarks, and packaging.
- `eval-viewer/`: The frontend viewer for reviewing evaluation results.
- `references/`: Schemas and writing guides.
- `LICENSE.txt`: Apache License 2.0.

## 🤝 Credits
This tool is based on the **`skill-creator`** workflow and scripts originally developed for **Claude Code**.
