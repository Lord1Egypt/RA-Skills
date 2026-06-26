# TRACE Protocol

Use TRACE for every reverse engineering engagement:

## Triage

Define the smallest useful question before touching tooling.

- What is the target?
- What answer does the user actually need?
- What is in bounds and out of bounds?
- What artifact can answer the question fastest?

Good examples:
- "What fields are in this binary format?"
- "How does this app authenticate?"
- "Why does this device reject this packet?"
- "What hidden assumptions make this workflow fail?"

Bad example:
- "Understand everything."

## Record

Capture observable behavior before writing theories.

- Inputs and outputs
- Files read and written
- Endpoints, ports, headers, and payload shapes
- Timings, retries, state transitions, and error messages
- UI affordances and the actions that trigger them

Preferred order:
1. Static surfaces: names, strings, schema hints, docs, manifest data
2. Behavioral surfaces: requests, logs, traces, emitted files, rendered states
3. Internal surfaces: decompiled paths, symbol clues, disassembly, state machines

## Abstract

Turn observations into testable models.

Write short hypotheses such as:
- "Field 7 is a checksum over bytes 0-31."
- "The client derives the session token from a nonce plus device ID."
- "This workflow fails because approval state is cached at step 2."

Every hypothesis should answer:
- What would make this true?
- What would make it false?
- What is the cheapest probe?

## Challenge

Probe the model with the smallest safe test.

- Mutate one variable at a time
- Replay the smallest sample that still reproduces behavior
- Compare control vs variant
- Prefer offline artifacts, copies, or sandboxes over live systems

If a probe changes too many variables, it creates noise instead of understanding.

## Explain

Compress the result into usable outputs.

Always produce:
- what is known
- how it is known
- what remains uncertain
- what to test next

If the user wants a reimplementation or fix, explain the mechanism first and only then suggest code or process changes.
