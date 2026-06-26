[English](README.md) | [中文](README_CN.md)

# Remote Skill Test

An agent skill that automates end-to-end testing of other agent skills on a remote jump host. After updating a skill locally, this skill SSHs to the remote host, updates the installed skills, runs the target skill in a dedicated test directory, retrieves the generated report, and compares it against the previous run.

## Problem Statement

Testing agent skills after local edits currently requires a manual workflow:

- **Manual deployment** — SSH to the jump host, `npx skills add` to update, navigate to the right directory.
- **Manual execution** — Open OpenCode, type the prompt, interact with confirmations.
- **Manual comparison** — Find the previous report, visually diff structure and content, mentally map changes back to SKILL.md edits.

This is tedious and error-prone, especially during iterative skill development.

## What This Skill Does

1. **Collects SSH config, target skill name, and test prompt** from the user (no credentials stored in files). The test prompt can be provided directly in the conversation or constructed from context.
2. **Creates a timestamped test directory** on the remote host: `~/skill-tests/{timestamp}-{skill-name}/`.
3. **Installs all skills at project level** inside the test directory via `npx skills add panlm/skills -y` (not global). Skills have inter-dependencies (e.g., `aws-fis-experiment-execute` loads `app-service-log-analysis` at runtime), so all skills must be installed together.
4. **Executes the target skill** via `opencode run --dangerously-skip-permissions` with the user-provided prompt (auto-confirm suffix appended automatically). All output (stdout + stderr) is captured to `opencode-run.log` via `tee` for diagnostics.
5. **Retrieves the generated report and execution log** via `scp` into a timestamped local directory `./test-results/{skill-name}/{timestamp}/`. File names are kept identical to the remote originals.
6. **Finds the previous run's report** on the remote host by searching `~/skill-tests/*-{skill-name}/` directories, then retrieves it into the **same local run directory**. Both reports (current + previous) live side-by-side with their original file names for easy comparison.
7. **Compares reports** — checks structure compliance against SKILL.md template, diffs structural changes between runs, and correlates with recent SKILL.md git changes.
8. **Outputs analysis** — compliance table, change summary, and verdict (PASS / PARTIAL / FAIL).

## Design Decisions

1. **Generic framework, not FIS-specific.** Works with any skill in the repository. The user provides the test prompt directly in the conversation; this skill only orchestrates remote execution and report comparison.

2. **SSH config asked at runtime.** No IP addresses, usernames, or key paths are stored in any committed file. The skill asks the user every time (or the user can provide an SSH config alias).

3. **Test prompt provided by user.** The user provides the test prompt directly in the conversation (or it is constructed from context). Auto-confirm directives are appended automatically so the remote agent runs non-interactively without waiting for user confirmation.

4. **Timestamped directories with skill name.** Remote test directories use `{timestamp}-{skill-name}` format, making it trivial to find the previous run for the same skill and compare reports.

5. **Structure comparison, not data comparison.** Reports from different runs will have different timestamps, resource IDs, and metrics. The comparison focuses on structural compliance (sections, fields, tables) and correlates structural changes with SKILL.md updates.

6. **OpenCode `run` for non-interactive execution.** Uses `opencode run --dangerously-skip-permissions "prompt"` which runs in non-interactive mode — no TUI, no manual interaction, no permission prompts. All output is captured to `opencode-run.log` via `tee` for diagnostics.

7. **Project-level full-repo installation.** All skills are installed inside the test directory via `npx skills add panlm/skills -y`. Skills have inter-dependencies (e.g., `aws-fis-experiment-execute` loads `app-service-log-analysis`), so the full repo must be installed to avoid missing-dependency failures. Each test run is isolated at project level without affecting other environments.

8. **Reports and logs stored locally in timestamped directories.** Each test run is saved to `./test-results/{skill-name}/{timestamp}/`. The current report, previous report, execution log, and test analysis are all co-located in a single directory with their original file names, making each run self-contained and easy to review.

## Workflow Overview

```
Step 1:  Collect SSH config + skill name + test prompt
          ↓
Step 2:  SSH → mkdir ~/skill-tests/{timestamp}-{skill-name}/
          ↓
Step 3:  SSH → cd test-dir && npx skills add panlm/skills -y (project level, all skills for inter-dependencies)
          ↓
Step 4:  SSH → cd test-dir && opencode run --dangerously-skip-permissions "prompt" | tee opencode-run.log
          ↓
Step 5:  SCP → retrieve report files + opencode-run.log to local ./test-results/{skill-name}/{timestamp}/
           ↓
Step 6:  SSH → find previous ~/skill-tests/*-{skill-name}/ directory on remote
           ├── Found → SCP previous report into the same local run directory
           └── Not found → first run, skip comparison
          ↓
Step 7:  Analyze: structure compliance + diff vs previous + correlate SKILL.md changes
          ↓
Step 8:  Output results + verdict (PASS / PARTIAL / FAIL)
```

## Report Comparison Dimensions

The comparison does **NOT** compare data values (timestamps, resource IDs, metrics). It focuses on:

| Dimension | What It Checks |
|---|---|
| **Structure compliance** | Does the report contain all sections/fields/tables required by SKILL.md? |
| **Structural diff** | Which H2/H3 sections were added/removed vs the previous run? |
| **SKILL.md correlation** | Do report structural changes match recent SKILL.md edits? |

### Verdict Criteria

| Verdict | Meaning |
|---|---|
| **PASS** | All required sections present; structural changes match SKILL.md updates |
| **PARTIAL** | Most sections present; some SKILL.md changes not reflected or unexpected changes |
| **FAIL** | Missing required sections; or SKILL.md changes not reflected at all |

## Prerequisites

- **ssh / scp** — for remote access (user provides credentials at runtime)
- **npx** — installed on the remote host
- **opencode** — installed and configured on the remote host with LLM provider access
- **git** — for reading SKILL.md change history

## Error Handling

| Error | Cause | Resolution |
|---|---|---|
| SSH connection refused | Wrong host/user/key | Verify SSH config with user |
| `npx: command not found` | Node.js not installed on remote | Install Node.js on remote host |
| `opencode: command not found` | OpenCode not installed on remote | Install OpenCode on remote host |
| `opencode run` timeout | Skill execution takes too long | Increase SSH timeout; check remote logs |
| No report generated | Skill failed or prompt was wrong | Check opencode session output on remote |
| No previous report found | First run for this skill | Skip comparison, output compliance check only |

## Safety Rules

| Rule | Description |
|---|---|
| **No stored credentials** | SSH config asked at runtime, never committed to files |
| **No sensitive data in repo** | IP addresses, hostnames, usernames never appear in committed files |
| **No remote modifications** | Only creates test directories and runs `opencode run` |
| **No remote deletions** | Previous test results are always preserved for comparison |

## Usage Examples

```
"Test the aws-fis-experiment-execute skill remotely"
"远程测试 aws-fis-experiment-prepare skill"
"到跳板机上验证 execute skill 的更新效果"
"Run remote test for eks-workload-best-practice-assessment"
```

## Directory Structure

```
others/remote-skill-test/
├── SKILL.md          # Main skill definition (agent instructions)
├── README.md         # This file (English)
└── README_CN.md      # Chinese documentation
```

## Limitations

- Requires OpenCode installed and configured on the remote host with valid LLM provider API keys.
- `opencode run` runs non-interactively — skills that genuinely require human judgment during execution may not produce correct results.
- SSH timeout may be too short for long-running skills (e.g., FIS experiments that take 10+ minutes). Use `ssh -o ServerAliveInterval=60` if needed.
- Report comparison is structural only — it cannot assess whether the report *content* (insights, recommendations) improved in quality.
- First run for a skill has no previous report to compare against — only structure compliance is checked.
