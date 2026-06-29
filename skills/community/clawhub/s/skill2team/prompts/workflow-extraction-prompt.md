# Workflow Extraction Prompt

Extract trigger, inputs, stages, stage-internal deliverables, required user input nodes, branches, loops, gates, human intervention points, tools/data, artifacts, known-good behavior, and failure modes. Treat this as workflow preservation, not as a loose summary.

For each stage, record named outputs produced before handoff, including candidate sets, prompt packages, registries, matrices, files, audit records, checkpoints, and closing prompts.

For each human intervention point, record the source requirement, default action, and allowed choices: `preserve_as_human_wait`, `convert_to_reviewer_gate`, `auto_advance_with_audit`, or `remove_as_redundant`. Default to preserving source-mandated waits and choices unless the user explicitly selects safe automation.

Before source conversion starts, record the top-level human-interaction execution mode. Allowed modes are `preserve_source_human_interaction_steps`, `selective_human_intervention_retention`, and `fully_automated_with_audit`; default to `preserve_source_human_interaction_steps`.

Then create a workflow migration map with concrete nodes, edges, stage mappings, stage-internal deliverables, required user input nodes, human intervention policy, gates, checkpoints, resume rules, and terminal boundaries. Do not return only a prose summary.
