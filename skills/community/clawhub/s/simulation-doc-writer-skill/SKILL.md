---
name: simulation-doc-writer
description: Write, revise, or review Chinese plain-text documentation for communication simulation programs. Use when Codex needs to produce a plain-text (.txt) 仿真程序说明文档, simulation program manual, model description, experiment/reproduction guide, code-to-paper comparison, or technical report for wireless, optical, satellite, radar, modulation/coding, channel modeling, link-level, system-level, MATLAB/Python/C++ communication simulation code. For MATLAB simulation folders, document every .m file and every function in each .m file, map paper algorithms to their corresponding implementation functions, and identify which code files define the simulation environment.
---

# Simulation Doc Writer

## Overview

Use this skill to write Chinese plain-text (`.txt`) documentation for communication simulation programs with enough technical detail for readers to understand, run, verify, and extend the simulation.

Prefer a professional engineering style: precise, traceable, concise, and reproducible. Explain the simulation purpose, model assumptions, signal chain, parameters, input/output data, experiment design, result interpretation, and known limitations.

## Workflow

1. Clarify missing essentials before drafting if the user's request lacks the simulation object, code language/tool, target reader, or expected document type.
2. Inspect any provided code, configs, plots, logs, papers, or existing notes before inventing details.
3. Choose the document structure from `references/communication-simulation-doc-template.md`.
4. Draft in Chinese unless the user asks otherwise.
5. Separate confirmed facts from reasonable assumptions. Mark uncertain items as "待确认" instead of silently fabricating.
6. For MATLAB folders, enumerate every `.m` file before writing. For each file, identify whether it is a main script, function file, helper function file, plotting script, data-processing script, or obsolete/backup artifact.
7. For each `.m` file, document every function it defines, including local/subfunctions inside the file. State the function purpose, inputs, outputs, calling relationship, and role in the simulation.
8. When a paper is provided, map each named paper algorithm, model, benchmark, metric, and simulation setup to concrete code files and function names. If no matching implementation is found, mark it as "未找到明确对应实现" and explain the evidence.
9. Explicitly identify simulation-environment files: main entry scripts, parameter/configuration locations, channel/model construction files, codebook/data generation files, metric/statistics files, plotting files, and saved-data dependencies.
10. Generate the program description document as a plain-text file with a `.txt` extension. Do not use `.md`, `.docx`, `.pdf`, or other formats unless the user explicitly requests an additional export.
11. Put generated code, generated Markdown documentation, and related output files in the folder containing the user-provided paper. If there is no paper path, the paper path cannot be resolved, or the folder does not exist, ask the user where to save the outputs before creating files.
12. Include runnable commands, parameter tables, and result file descriptions when the codebase provides them.
13. End with verification and reproduction guidance: environment, command sequence, expected outputs, and common failure cases.

## Document Quality Rules

- Use terminology common in communication engineering, such as 调制方式, 信道模型, 编码率, 载噪比, 信噪比, 误码率, 误帧率, 吞吐量, 频谱效率, 链路级仿真, 系统级仿真.
- State mathematical models with symbols, units, and assumptions. Define each symbol near first use.
- For algorithms, describe both the processing flow and where the implementation lives in code.
- For paper-code comparison, provide an "论文算法/模型到代码映射表" with paper section/algorithm/figure, corresponding file, corresponding function, consistency judgment, and notes.
- For MATLAB code documentation, provide a "MATLAB 文件与函数说明表" that covers every `.m` file in the target folder and every function defined in those files. Do not skip small helper files.
- For simulation environment documentation, provide a "仿真环境对应代码文件" section that identifies where language/tool versions, system parameters, channel parameters, random seeds, Monte Carlo count, SNR/Ka sweeps, codebook size, and plotting/data loading paths are set.
- For parameters, provide name, meaning, unit, default value, allowed range, and effect on results when possible.
- For random simulations, document random seed policy, Monte Carlo iteration count, stopping criteria, and confidence/variance caveats.
- For results, explain how plots or metrics are generated and how to judge whether the result is reasonable.
- Avoid marketing language. Keep the tone like an engineering design note or lab deliverable.

## Reference

Read `references/communication-simulation-doc-template.md` when drafting or reviewing a full document, choosing section order, or creating tables/checklists.

## Self-Evolution Mechanism

After each execution of this Skill:

1. Evaluate whether the output achieved the intended goal: **pass / fail**.
2. If it fails, reflect on the cause of failure and append a “failure case + improvement suggestion” to `diary/YYYY-MM-DD.md`.
3. If a certain improvement suggestion is repeatedly mentioned in the most recent three executions, refine it into a formal rule and submit a PR to modify this `SKILL.md`.
