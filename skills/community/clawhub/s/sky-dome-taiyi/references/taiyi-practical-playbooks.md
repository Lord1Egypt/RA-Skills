# Taiyi Practical Playbooks / 太一实战手册

Optional large reference. Search with `taiyi_recipe_search.py`. Do not load fully unless building a complete operating manual.

## Playbook 001: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 002: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 003: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 004: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 005: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 006: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 007: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 008: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 009: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 010: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 011: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 012: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 013: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 014: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 015: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 016: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 017: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 018: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 019: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 020: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 021: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 022: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 023: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 024: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 025: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 026: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 027: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 028: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 029: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 030: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 031: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 032: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 033: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 034: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 035: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 036: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 037: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 038: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 039: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 040: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 041: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 042: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 043: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 044: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 045: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 046: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 047: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 048: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 049: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 050: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 051: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 052: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 053: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 054: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 055: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 056: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 057: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 058: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 059: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 060: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 061: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 062: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 063: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 064: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 065: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 066: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 067: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 068: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 069: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 070: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 071: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 072: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 073: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 074: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 075: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 076: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 077: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 078: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 079: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 080: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 081: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 082: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 083: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 084: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 085: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 086: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 087: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 088: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 089: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 090: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 091: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 092: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 093: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 094: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 095: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 096: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 097: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 098: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 099: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 100: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 101: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 102: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 103: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 104: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 105: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 106: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 107: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 108: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 109: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 110: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 111: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 112: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 113: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 114: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 115: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 116: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 117: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 118: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 119: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 120: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 121: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 122: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 123: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 124: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 125: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 126: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 127: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 128: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 129: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 130: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 131: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 132: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 133: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 134: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 135: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 136: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 137: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 138: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 139: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 140: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 141: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 142: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 143: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 144: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 145: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 146: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 147: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 148: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 149: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 150: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 151: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 152: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 153: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 154: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 155: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 156: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 157: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 158: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 159: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 160: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 161: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 162: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 163: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 164: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 165: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 166: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 167: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 168: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 169: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 170: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 171: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 172: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 173: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 174: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 175: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 176: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 177: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 178: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 179: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 180: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 181: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 182: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 183: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 184: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 185: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 186: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 187: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 188: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 189: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 190: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 191: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 192: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 193: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 194: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 195: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 196: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 197: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 198: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 199: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 200: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 201: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 202: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 203: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 204: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 205: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 206: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 207: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 208: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 209: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 210: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 211: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 212: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 213: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 214: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 215: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 216: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 217: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 218: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 219: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 220: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 221: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 222: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 223: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 224: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 225: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 226: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 227: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 228: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 229: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 230: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 231: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 232: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 233: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 234: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 235: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 236: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 237: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 238: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 239: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 240: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 241: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 242: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 243: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 244: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 245: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 246: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 247: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 248: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 249: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 250: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 251: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 252: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 253: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 254: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 255: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 256: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 257: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 258: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 259: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 260: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 261: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 262: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 263: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 264: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 265: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 266: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 267: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 268: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 269: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 270: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 271: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 272: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 273: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 274: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 275: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 276: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 277: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 278: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 279: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 280: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 281: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 282: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 283: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 284: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 285: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 286: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 287: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 288: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 289: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 290: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 291: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 292: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 293: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 294: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 295: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 296: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 297: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 298: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 299: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 300: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 301: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 302: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 303: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 304: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 305: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 306: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 307: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 308: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 309: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 310: Performance — Verified Operating Pattern

### Keywords
baseline benchmark profile compare regression, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Performance** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Performance task"
python scripts/taiyi_workflow.py create project-execution "Performance run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Performance report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 311: Documentation — Verified Operating Pattern

### Keywords
audience structure examples quickstart troubleshooting, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Documentation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Documentation task"
python scripts/taiyi_workflow.py create project-execution "Documentation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Documentation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 312: Workflow Automation — Verified Operating Pattern

### Keywords
trigger steps state evidence board handoff, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Workflow Automation** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Workflow Automation task"
python scripts/taiyi_workflow.py create project-execution "Workflow Automation run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Workflow Automation report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 313: Release Engineering — Verified Operating Pattern

### Keywords
versioning clean staging changelog publish inspect rollback, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Release Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Release Engineering task"
python scripts/taiyi_workflow.py create project-execution "Release Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Release Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 314: Debugging — Verified Operating Pattern

### Keywords
symptom reproduce config smoke root cause prevention, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Debugging** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Debugging task"
python scripts/taiyi_workflow.py create project-execution "Debugging run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Debugging report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 315: Research — Verified Operating Pattern

### Keywords
question sources cross-check synthesis citation uncertainty, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Research** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Research task"
python scripts/taiyi_workflow.py create project-execution "Research run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Research report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 316: Data Work — Verified Operating Pattern

### Keywords
schema sample validate transform report anomaly, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Data Work** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Data Work task"
python scripts/taiyi_workflow.py create project-execution "Data Work run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Data Work report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 317: API Integration — Verified Operating Pattern

### Keywords
endpoint auth smoke payload status retry contract, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **API Integration** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "API Integration task"
python scripts/taiyi_workflow.py create project-execution "API Integration run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "API Integration report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 318: Agent Memory — Verified Operating Pattern

### Keywords
preference decision lesson prune checkpoint dream, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Agent Memory** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Agent Memory task"
python scripts/taiyi_workflow.py create project-execution "Agent Memory run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Agent Memory report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 319: Prompt Engineering — Verified Operating Pattern

### Keywords
goal context constraints output examples verification, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Prompt Engineering** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Prompt Engineering task"
python scripts/taiyi_workflow.py create project-execution "Prompt Engineering run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Prompt Engineering report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 320: Project Management — Verified Operating Pattern

### Keywords
milestone blocker owner next risk evidence, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Project Management** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Project Management task"
python scripts/taiyi_workflow.py create project-execution "Project Management run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Project Management report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered

## Playbook 321: Code Quality — Verified Operating Pattern

### Keywords
test lint typecheck build review refactor, taiyi, evidence, workflow, checkpoint, delivery

### When to use
Use this playbook when the task belongs to **Code Quality** and the user expects practical progress, not abstract advice. The goal is to turn ambiguous intent into a small inspected action, then into verified delivery.

### Mission framing
- Desired outcome:
- Current state:
- Unknowns:
- Constraints:
- Success gate:
- Evidence source:

### Operating sequence
1. **Frame** the actual objective in one sentence. If the objective is unclear, ask one blocking question only.
2. **Inspect** the nearest real state: file, config, source, log, API response, version, screenshot, or user-provided artifact.
3. **Choose** the smallest reversible move that reduces uncertainty or creates a useful artifact.
4. **Execute** with the relevant Taiyi helper or host tool.
5. **Verify** using a concrete gate. Prefer readback, diff, status, test, benchmark, schema, source URL, or manifest.
6. **Compress** the result into a short handoff: result, evidence, changed files, next action.
7. **Consolidate** only if the lesson is durable and safe to store.

### Useful Taiyi helpers
```bash
python scripts/taiyi_calibrate.py "Code Quality task"
python scripts/taiyi_workflow.py create project-execution "Code Quality run" --mission "deliver verified result"
python scripts/taiyi_doctor.py <path>
python scripts/taiyi_report.py "Code Quality report"
python scripts/taiyi_answer_check.py < draft.md
```

### Evidence gates
- File artifact exists and was read back.
- Command completed and output was inspected.
- Version/status/source was checked after mutation.
- Any claim with uncertainty is labeled as inference.
- Remaining risk is named instead of hidden.

### Anti-dumb constraints
- Do not recite all Taiyi modes.
- Do not overuse persona language.
- Do not promise future work when a tool can act now.
- Do not store noisy temporary state.
- Do not claim completion without evidence.

### Output pattern
```text
结果：...
证据：...
改动：...
下一步：...
```

### Reusable checklist
- [ ] Goal clear
- [ ] Current state inspected
- [ ] Active step chosen
- [ ] Verification gate selected
- [ ] Evidence captured
- [ ] Delivery concise
- [ ] Durable lesson considered


## Micro Playbook 322: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 322"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 323: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 323"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 324: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 324"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 325: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 325"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 326: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 326"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 327: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 327"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 328: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 328"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 329: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 329"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 330: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 330"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 331: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 331"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 332: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 332"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 333: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 333"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 334: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 334"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 335: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 335"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 336: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 336"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 337: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 337"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 338: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 338"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 339: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 339"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 340: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 340"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 341: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 341"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 342: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 342"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 343: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 343"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 344: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 344"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 345: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 345"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 346: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 346"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 347: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 347"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 348: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 348"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 349: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 349"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 350: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 350"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 351: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 351"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 352: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 352"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 353: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 353"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 354: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 354"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 355: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 355"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 356: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 356"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 357: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 357"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 358: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 358"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 359: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 359"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 360: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 360"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 361: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 361"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 362: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 362"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 363: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 363"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 364: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 364"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 365: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 365"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 366: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 366"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 367: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 367"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 368: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 368"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 369: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 369"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 370: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 370"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 371: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 371"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 372: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 372"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 373: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 373"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 374: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 374"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 375: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 375"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 376: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 376"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 377: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 377"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 378: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 378"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 379: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 379"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 380: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 380"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 381: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 381"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 382: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 382"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 383: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 383"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 384: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 384"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 385: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 385"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 386: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 386"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 387: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 387"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 388: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 388"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 389: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 389"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 390: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 390"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 391: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 391"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 392: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 392"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 393: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 393"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 394: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 394"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 395: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 395"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 396: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 396"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 397: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 397"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 398: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 398"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 399: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 399"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 400: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 400"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 401: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 401"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 402: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 402"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 403: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 403"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 404: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 404"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 405: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 405"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 406: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 406"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 407: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 407"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 408: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 408"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 409: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 409"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 410: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 410"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 411: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 411"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 412: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 412"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 413: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 413"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 414: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 414"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 415: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 415"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 416: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 416"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 417: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 417"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 418: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 418"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 419: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 419"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 420: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 420"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 421: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 421"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 422: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 422"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 423: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 423"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 424: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 424"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 425: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 425"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 426: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 426"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 427: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 427"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 428: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 428"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 429: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 429"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 430: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 430"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 431: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 431"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 432: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 432"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 433: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 433"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 434: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 434"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 435: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 435"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 436: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 436"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 437: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 437"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 438: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 438"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 439: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 439"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 440: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 440"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 441: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 441"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 442: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 442"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 443: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 443"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 444: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 444"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 445: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 445"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 446: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 446"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 447: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 447"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 448: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 448"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 449: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 449"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 450: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 450"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 451: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 451"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 452: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 452"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 453: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 453"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 454: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 454"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 455: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 455"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 456: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 456"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 457: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 457"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 458: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 458"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 459: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 459"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 460: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 460"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 461: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 461"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 462: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 462"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 463: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 463"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 464: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 464"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 465: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 465"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 466: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 466"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 467: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 467"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 468: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 468"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 469: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 469"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 470: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 470"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 471: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 471"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 472: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 472"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 473: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 473"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 474: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 474"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 475: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 475"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 476: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 476"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 477: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 477"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 478: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 478"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 479: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 479"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 480: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 480"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 481: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 481"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 482: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 482"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 483: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 483"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 484: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 484"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 485: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 485"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 486: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 486"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 487: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 487"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 488: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 488"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 489: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 489"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 490: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 490"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 491: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 491"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 492: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 492"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 493: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 493"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 494: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 494"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 495: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 495"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 496: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 496"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 497: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 497"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 498: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 498"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 499: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 499"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 500: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 500"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 501: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 501"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 502: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 502"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 503: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 503"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 504: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 504"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 505: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 505"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 506: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 506"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 507: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 507"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 508: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 508"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 509: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 509"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 510: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 510"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 511: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 511"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 512: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 512"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 513: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 513"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 514: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 514"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 515: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 515"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 516: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 516"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 517: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 517"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 518: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 518"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 519: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 519"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 520: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 520"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 521: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 521"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 522: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 522"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 523: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 523"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 524: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 524"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 525: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 525"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 526: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 526"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 527: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 527"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 528: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 528"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 529: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 529"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 530: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 530"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 531: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 531"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 532: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 532"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 533: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 533"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 534: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 534"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 535: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 535"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 536: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 536"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 537: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 537"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 538: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 538"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 539: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 539"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 540: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 540"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 541: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 541"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 542: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 542"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 543: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 543"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 544: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 544"
python scripts/taiyi_answer_check.py < draft.md
```


## Micro Playbook 545: Evidence-First Delivery

Use when Taiyi must stay practical. Inspect state, choose one action, verify, compress.

Checklist:
- Goal stated in one sentence.
- Evidence source named.
- One reversible action chosen.
- Verification gate selected.
- Result delivered in result/evidence/next format.

Commands:
```bash
python scripts/taiyi_calibrate.py "micro task 545"
python scripts/taiyi_answer_check.py < draft.md
```


