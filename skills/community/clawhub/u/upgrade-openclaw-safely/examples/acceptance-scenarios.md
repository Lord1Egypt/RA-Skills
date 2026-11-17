# Offline behavioral acceptance

The authoritative expanded cases are [test-prompts.json](test-prompts.json). The root test-prompts.json is a generated compatibility subset for older consumers.

For each case, evaluate next actions, permitted mutations, stopping point and required evidence using the skill and only relevant references. No case authorizes a live host update, restart, model call, network install, outward message or cleanup.

For an independent forward pass, supply only each prompt and raw context, omitting expected outcomes and prior audit conclusions. Give the reviewer the skill and required references, not the implementation plan. Compare the resulting decisions with expected outcomes afterward.

A pass requires correct scope/authority, exact target and operation identity, recovery coverage before mutation, no competing/duplicate core mutation, complete observation evidence and safe retention. A technically plausible command is not a pass if these invariants fail.

Include the legacy-driver, physical-store, private-runtime, slow-start, full-window, semantic-SQL and retention cases when changing transport, migration or completion policy. Validate description/frontmatter and local links separately; they do not prove behavior.

The historical numeric fixtures describe particular cases, not default package versions, timeout values, retention counts or stability durations.
