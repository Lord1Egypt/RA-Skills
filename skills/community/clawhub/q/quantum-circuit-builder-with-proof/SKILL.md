---
name: quantum-circuit-builder-with-proof
description: "Quantum Circuit Builder with Proof: Use this product when a quantum circuit needs verifiable evidence, not just. Use when an agent needs quantum circuit builder with proof, formally verified quantum circuit design, proof carrying quantum circuit certificates (qpcert), independent verification of a quantum proof certificate from another party, audit ready quantum computing artifacts for research and compliance, certify circuit, circuit, claims through AgentPMT-hosted remote tool calls."
version: 1.0.4
homepage: https://www.agentpmt.com/marketplace/quantum-circuit-builder-with-proof
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/quantum-circuit-builder-with-proof"}}
---
# Quantum Circuit Builder with Proof

## Freshness
Last updated: `2026-09-09`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Build quantum circuits that ship with a machine-checked proof. Quantum Circuit Builder with Proof turns an algorithm template, a Qiskit, Cirq, or Braket snippet, or Lean source into a normalized circuit, draws it as a downloadable PNG or JPEG diagram, and verifies the claims you state with the Lean 4 proof kernel. The result is a qpcert: a proof certificate anyone can replay independently, without trusting the agent that produced it. Export checked OpenQASM 3, Qiskit, Cirq, and Braket programs, run local simulations, and keep audit receipts for every step. Use it when a circuit must be audited, shared, or relied on. Plain Qiskit is simpler for throwaway experiments.

## Product Instructions
### Proof-Carrying Quantum

Use this product to research proof-carrying quantum concepts, find Lean declarations and worked corpus assets, build normalized circuits, create or independently verify kernel-backed qpcerts, export offline provider programs, and obtain local simulator observations.

The listed action schemas are the complete agent contract. Choose the action that advances the user's goal; there is no discovery preflight.

#### Trust boundaries

- Knowledge and corpus results are reference material, not proof.
- Provider-source import parses bounded source and never executes it. Parsing and round-trip validation are not proof.
- Circuit inspection validates structure and semantics and can produce visual explanations, including a File Manager PNG or JPEG of the logical wire circuit. Validation and visualization are not proof or hardware execution.
- `certify_circuit` and `certify_from_lean` create qpcerts through the pinned Lean kernel and verify the generated certificate before returning it.
- `verify_certificate` is an independent recipient-side replay for evidence received from another party. Do not automatically verify a qpcert just produced by a certification action.
- `extract_circuit` replays an existing qpcert before recovering its normalized circuit. It is optional, not a mandatory post-certification step.
- Provider exports are offline source artifacts and receipts; they do not claim provider execution.
- `execute_locally` returns simulator observations and receipts. Simulation does not add a proof tier.
- Lean submitted to `certify_from_lean`, `export_provider_programs`, or `execute_locally` runs as `trusted_direct_v1` inside the private Cloud Run service container. IAM authenticates callers, but Lean shares the service filesystem, network, and service identity; this is not untrusted-code isolation. Submit only internally trusted Lean. The receipt fields `execution_mode` and `untrusted_code_isolation` are the machine-readable authority.

#### Choose a flow

Research only when information is missing:

1. Use `search_knowledge` for concepts, design rationale, and repository documentation.
2. Use `search_lean` for declarations and authoring primitives; set `authoring_only` to true when writing submitted CircuitSpec source.
3. Use `search_corpus_examples`, then retrieve a selected asset with `get_corpus_example`.

Build and certify:

1. Start with `instantiate_template`, `import_provider_circuit`, or Lean source.
2. Use `inspect_circuit` when validation details or visualizations are useful.
3. Use `certify_circuit` for a normalized circuit plus an exact claim ledger, or `certify_from_lean` when Lean source is authoritative.
4. Optionally use `export_provider_programs` or `execute_locally` with Lean source.

Receive external evidence:

1. Put the qpcert in File Manager.
2. Use `verify_certificate` with the independently supplied circuit and claims.
3. Use `extract_circuit` only when the circuit must be recovered from the qpcert.

#### Choose the proof claim

Choose the narrowest claim that matches what the user actually asked to establish. If the user asks to "make a proof," "prove this circuit," or "create a certificate" without naming a stronger semantic property, default to a **well-formed certificate**. Never choose `exactUnitary` merely because the request uses the word "proof."

- **Well formed** (`well_formed` in a claim ledger; `.wellFormed` in Lean) is the default for an arbitrary circuit built on the canvas, imported from a provider, or supplied as normalized IR. It proves that the circuit has nonzero width, has operations, and is admitted by the selected circuit/profile contract. It does not prove an algorithm result, a target state, or equivalence to a particular unitary. For `certify_circuit`, use `inspect_circuit` first when the canonical subject digest is not already available, then create a complete well-formed claim ledger bound to that digest. For `certify_from_lean`, use `claims := []` and omit the request-level claims when only the service's minimal well-formed certificate is needed.
- **Exact unitary** (`.exactUnitary`) is for a gate-only circuit when the user explicitly asks for its exact unitary semantics or an exact unitary equivalence. It rejects measurement and reset. Use it only with a matching checked-in corpus example, contracted template, or already-authored theorem and proof strategy. Exact matrix normalization can exhaust Lean heartbeats even for a short circuit; gate count alone is not a cost estimate.
- **Exact instrument** (`.exactInstrument`) is for circuits with measurement or reset when the user explicitly asks to prove the exact measurement-channel/instrument semantics. Use a matching measurement/reset corpus example and its proof strategy; do not substitute it for ordinary structural certification.
- **Signed transport** (`.signedTransport`) is for an explicitly requested Clifford signed-tableau/Pauli transport claim. Use it only when the circuit is supported by the Clifford translation and a matching corpus example or authored theorem exists.
- **Custom** (`.custom claimId statement`) is for a specific trusted Lean proposition the user supplied or explicitly requested. It requires an authored proof of that exact proposition. Never invent a custom proposition and present it as the user's requested result.

Choose the certification action separately from the claim strength:

- Use `certify_circuit` when the normalized circuit is authoritative. Prefer a matching `certification_inputs` result or `.claims.json` corpus asset. Do not translate a canvas circuit back into Lean merely to certify it.
- Use `certify_from_lean` only when trusted Lean `CircuitSpec` source is itself authoritative or an exact/custom claim needs a matching Lean proof that is already supported by the corpus or supplied proof material.

If an exact semantic proof exhausts Lean heartbeats or another kernel resource limit, do not blindly increase `maxHeartbeats`, repeatedly submit the same expensive proof, or silently claim that a weaker certificate proves the exact property. If the original request was only for a generic certificate, start a new well-formed certification instead and describe its narrower scope. If the user explicitly requested the exact property, report that it was not proved and use a matching corpus theorem/proof strategy or ask before reducing the claim.

#### Background tasks and files

Certification, certificate replay, extraction, provider export, and execution always start persisted background tasks. Other service-dependent actions return directly when the service is ready. During a cold start, however, every service-dependent request is retained instead of failing: it returns `status: processing` and a `task_id`, then runs after startup. Call the free `get_task` action with that ID and `wait_seconds: 60`; the call returns sooner when the task changes and remains below the chat tool-call deadline. If it is still processing, repeat the same free long poll. Do not rapidly poll or submit a duplicate paid action. Proof certification commonly takes 3-5 minutes, and larger or more complex proofs can take longer.

While processing, `progress` remains 0 because no trustworthy percentage is available. `get_task` responses keep `action: get_task` and identify the retained operation in `task_action`. `stage: warming_service` means the accepted request is waiting for the proof service. `stage: waiting_on_kernel` means a proof, replay, extraction, export, or execution action is running; `stage: running_action` means a deferred direct action such as inspection is running. `awaiting_resume` or `resuming` means an interrupted MCP worker is being recovered from its saved request; continue polling the same task ID. A changing `date_updated` means the worker is alive. Stages then move through `packaging_result` to `completed`.

On completion, the original action response is in `outputs[0]`. Results larger than 32 KiB are stored intact in File Manager as `outputs[0].result_file`; read that JSON file when needed. Certification always stores the full qpcert as `outputs[0].certificate_file`, even when the rest of the receipt is also moved to a result file. Files and tasks are budget-scoped.

On failure, read `error` and `error_details`. Correct invalid source, circuit, claims, or file input and start a new task. Ordinary service warming remains `processing`; a task fails only when startup exhausts its deadline or another real error occurs. A retryable service failure says so explicitly; retry the same action later instead of running diagnostic actions.

#### Knowledge and corpus actions

##### `search_knowledge`

Use when conceptual or repository context is needed. Required: `query`. Optional: `result_count` 1-50, default 8; `search_mode` is `hybrid`, `semantic`, or `keyword`, default `hybrid`. Use `get_document` with a returned document ID when the full record is needed.

```json
{"action":"search_knowledge","query":"why certificate replay is a trust boundary","result_count":6,"search_mode":"hybrid"}
```

##### `search_lean`

Use to find Lean declarations, theorem names, namespaces, signatures, and allowed authoring primitives. Required: `query`. Optional: `result_count` 1-50; `authoring_only`, default false. When writing a CircuitSpec, start with `get_corpus_example` for `authored_specs/bell_spec.lean`, then use `authoring_only: true` to look up names in the four admitted modules: `CircuitSpec`, `Qasm3Subset`, `Edifice.ProductionPurePipeline`, and `Edifice.ProductionEffectfulPipeline`. Use `authoring_only: false` to browse the wider reference corpus.

```json
{"action":"search_lean","query":"CircuitSpec controlled X gate","result_count":8,"authoring_only":true}
```

##### `get_document`

Use after knowledge search. Required: positive `document_id` returned by `search_knowledge`. Do not guess IDs.

```json
{"action":"get_document","document_id":42}
```

##### `search_corpus_examples`

Use to find worked proof chains, template inputs, provider-intake samples, or designer samples. Optional: `query`; omit it for a bounded index. Optional: `result_count` 1-50, default 8. Returned summaries contain exact asset paths.

```json
{"action":"search_corpus_examples","query":"bell claims","result_count":10}
```

##### `get_corpus_example`

Use after corpus search. Required: the exact relative `example_path`. Absolute paths and traversal reject. JSON, Lean, qpcert, and text assets retain their media type; large assets may return a File Manager result file.

```json
{"action":"get_corpus_example","example_path":"authored_specs/bell_spec.lean"}
```

#### Circuit actions

##### `instantiate_template`

Use to expand a supported template. Required: `descriptor.semantic_profile` and `descriptor.family`, plus family-specific fields:

- `ghz`: `qubits` 2-4096.
- `bernstein_vazirani`: nonempty binary `secret`.
- `teleportation`: no additional field.
- `grover`: `qubits` 2-4096 and `marked_item` satisfying `0 <= marked_item < 2^qubits`.
- `qft`: `qubits` 2-6.

The result is not certified. It normally includes the normalized circuit, validation/visualization material, and certification inputs where the template has contracted claims.

```json
{"action":"instantiate_template","descriptor":{"semantic_profile":"exact_clifford_t_v2","family":"grover","qubits":3,"marked_item":5}}
```

##### `import_provider_circuit`

Use to parse hand-authored Qiskit, Cirq, or Braket Python without executing it. Required: `circuit_id`, explicit `semantic_profile`, `provider_target`, and `source`. The source must end in exactly one newline and is limited to 262144 characters. `qubit_count` is required for Braket because idle-wire width is not encoded by `Circuit()`; it is optional for Qiskit and Cirq.

Supported source targets are `qiskit_python`, `cirq_python`, and `braket_python`. The parser accepts only its bounded grammar; dynamic Python and arbitrary execution reject.

```json
{"action":"import_provider_circuit","circuit_id":"bell_import","semantic_profile":"unsigned_binary_symplectic_clifford_v1","provider_target":"qiskit_python","source":"from qiskit import QuantumCircuit\ncircuit = QuantumCircuit(2)\ncircuit.h(0)\ncircuit.cx(0, 1)\n"}
```

##### `inspect_circuit`

Use for validation, canonical subject-address computation, and optional visual explanation. Required: complete `circuit`. Optional: `claims` to enrich claim-aware visualizations; `include_visualizations`, default false, to return the complete structured visualization pack; `image_format` (`png` or `jpeg`) to render the digest-bound logical `wire_circuit` projection and store it in the current budget's File Manager. `image_format` triggers the needed visualization internally and does not require `include_visualizations: true`.

The circuit must be a complete `heyting.quantum_circuit_ir.v1` object with `circuit_id`, a supported `semantic_profile`, nonempty `qubits`, `classical_bits`, `initial_state`, and ordered `operations`. Gate rows use `kind`, `op_id`, `gate`, `controls`, `targets`, and `parameters`; measurement rows use `basis`, `qubit`, and `classical_bit`; reset rows use `qubit`.

When `image_format` is set, the response includes top-level `image_file` metadata. If a visual response is useful, immediately call AgentPMT's built-in `present_resource_card` with `variant: "image"` and `image_file.file_id`, `filename`, `content_type`, and `size_bytes`. Use `file_id` as the card's only locator: do not also pass `url`, and do not present or persist `signed_url`. The card resolves a fresh budget-scoped URL when it enters view or is replayed. The image is a logical explanation bound to the circuit and visualization digests; the qpcert, not the image, is the proof artifact.

```json
{"action":"inspect_circuit","image_format":"png","circuit":{"schema":"heyting.quantum_circuit_ir.v1","circuit_id":"bell_pair","semantic_profile":"unsigned_binary_symplectic_clifford_v1","qubits":[{"id":"q0"},{"id":"q1"}],"classical_bits":[],"initial_state":"zero","operations":[{"kind":"gate","op_id":"g0","gate":"h","controls":[],"targets":["q0"],"parameters":[]},{"kind":"gate","op_id":"g1","gate":"cx","controls":["q0"],"targets":["q1"],"parameters":[]}],"metadata":{"name":"Bell pair","scope":"unsigned symplectic action"}}}
```

Then display the returned file with the chat card:

```json
{
  "variant": "image",
  "title": "Bell pair logical circuit",
  "description": "Logical gate visualization; this image is not proof.",
  "file_id": "<image_file.file_id>",
  "filename": "<image_file.filename>",
  "content_type": "image/png",
  "size_bytes": 48321
}
```

#### Proof actions

##### `certify_circuit`

Use when a normalized circuit and exact claim ledger are ready. This is the normal path for a circuit built on the canvas, imported from a provider, or returned by a template. Required: complete `circuit` and `claims`. The claim ledger must use `heyting.quantum_claim_evidence.v1`, match the circuit's semantic profile and canonical subject digest, and contain nonempty typed claim obligations. Unless the user explicitly requested a supported stronger property, use a `well_formed` obligation. Start from matching `certification_inputs` or a `.claims.json` corpus example rather than inventing a relation or evidence tier. When the Quantum Agent dashboard supplies `certification_claims`, pass that object unchanged. The only accepted evidence-tier names are `kernel_certified`, `checker_verified`, `simulator_crosscheck`, `provider_attested`, and `reported`.

This action validates the circuit, runs kernel-backed bundle construction, verifies the generated qpcert, stores it in File Manager, and returns a compact certificate summary. Do not automatically call verification or extraction on this fresh result.

```json
{"action":"certify_circuit","circuit":{"schema":"heyting.quantum_circuit_ir.v1","circuit_id":"bell_pair","semantic_profile":"unsigned_binary_symplectic_clifford_v1","qubits":[{"id":"q0"},{"id":"q1"}],"classical_bits":[],"initial_state":"zero","operations":[{"kind":"gate","op_id":"g0","gate":"h","controls":[],"targets":["q0"],"parameters":[]},{"kind":"gate","op_id":"g1","gate":"cx","controls":["q0"],"targets":["q1"],"parameters":[]}],"metadata":{}},"claims":{"schema":"heyting.quantum_claim_evidence.v1","ledger_id":"bell_claims","semantic_profile":"unsigned_binary_symplectic_clifford_v1","circuit_subject_sha256":"c2324b23b67cc6eb4ce677e2b6f165c9000b6c87775e93e03fe2f422cd2c8201","claims":[{"claim_id":"bell_well_formed","statement":{"claim_type":"well_formed","profile":"unsigned_binary_symplectic_clifford_v1"},"accepted_evidence_tiers":["kernel_certified","checker_verified"],"description":"The normalized circuit is well formed in the active semantic profile."}],"evidence":[],"metadata":{"state":"obligations_only"}}}
```

##### `certify_from_lean`

Use only when restricted Lean CircuitSpec source is authoritative or the requested exact/custom claim has a matching trusted Lean proof. Do not convert a normalized canvas circuit to Lean just to obtain an ordinary certificate; use `certify_circuit` with a well-formed ledger instead. Required: `lean_source` defining `spec`. Optional: `resource_class` (`small` up to 2 qubits or `standard` up to 4); optional complete `claims`. When request-level claims are omitted, the service synthesizes a minimal well-formed claim. On rejection, the failed task contains Lean/kernel diagnostics; on success, it stores the complete qpcert. Cloud Run executes this Lean in the shared service container as `trusted_direct_v1`; IAM authentication is not untrusted-code isolation, so submit only internally trusted Lean and inspect the receipt fields.

```json
{"action":"certify_from_lean","resource_class":"small","lean_source":"import HeytingLean.Quantum.ProofCarrying.CircuitSpec\n\nopen HeytingLean.Quantum.ProofCarrying\n\ndef spec : CircuitSpec where\n  circuitId := \"agent_bell\"\n  semanticProfile := \"unsigned_binary_symplectic_clifford_v1\"\n  qubits := 2\n  classicalBits := 0\n  ops := [.gate .H 0 0, .gate .CX 0 1]\n  claims := []\n  metadataScope := \"agent request\"\n\ntheorem spec_claims : CircuitSpec.ClaimsHold spec := by\n  simp [CircuitSpec.ClaimsHold, spec]\n"}
```

##### `verify_certificate`

Use to independently replay external evidence. Required: `certificate_file_id`, complete independently supplied `circuit`, and complete independently supplied `claims`. The file must contain a typed qpcert and be visible to the current budget. A mismatch between any of the three inputs rejects.

```json
{"action":"verify_certificate","certificate_file_id":"2f5c8b82-3383-4d56-9ef2-c59546099e45","circuit":{"schema":"heyting.quantum_circuit_ir.v1","circuit_id":"bell_pair","semantic_profile":"unsigned_binary_symplectic_clifford_v1","qubits":[{"id":"q0"},{"id":"q1"}],"classical_bits":[],"initial_state":"zero","operations":[{"kind":"gate","op_id":"g0","gate":"h","controls":[],"targets":["q0"],"parameters":[]},{"kind":"gate","op_id":"g1","gate":"cx","controls":["q0"],"targets":["q1"],"parameters":[]}],"metadata":{}},"claims":{"schema":"heyting.quantum_claim_evidence.v1","ledger_id":"bell_claims","semantic_profile":"unsigned_binary_symplectic_clifford_v1","circuit_subject_sha256":"c2324b23b67cc6eb4ce677e2b6f165c9000b6c87775e93e03fe2f422cd2c8201","claims":[{"claim_id":"bell_well_formed","statement":{"claim_type":"well_formed","profile":"unsigned_binary_symplectic_clifford_v1"},"accepted_evidence_tiers":["kernel_certified","checker_verified"],"description":"The circuit is well formed."}],"evidence":[],"metadata":{}}}
```

##### `extract_circuit`

Use when an existing qpcert must be replayed and reduced to its normalized circuit and projections. Required: budget-visible `certificate_file_id`. Do not call this merely to repeat a fresh certification flow.

```json
{"action":"extract_circuit","certificate_file_id":"2f5c8b82-3383-4d56-9ef2-c59546099e45"}
```

#### Provider and execution actions

##### `export_provider_programs`

Use to produce checked offline provider programs from Lean source. Required: `lean_source` defining `spec`; unique `export_targets`, one to four of `openqasm3`, `qiskit_python`, `cirq_python`, and `braket_python`. Optional: `resource_class` (`small` or `standard`).

The connector verifies and emits the Lean source, derives the circuit width, resolves current provider target snapshots internally, and invokes the Lean-owned export. This action does not accept a qpcert and does not submit to hardware. Its Lean runs as `trusted_direct_v1` in the shared Cloud Run service container, not an untrusted-code sandbox.

When `classicalBits := 0`, Lean's default `.auto` observation is `terminal_z_all`. Provider outputs are runnable observation programs, so OpenQASM, Qiskit, and Cirq materialize terminal Z measurements and Braket records the equivalent terminal observation as implicit. The source circuit operations remain unchanged. Compact results report `observation`, `source_operation_count`, and `measurement_injected` so this materialization is explicit.

```json
{"action":"export_provider_programs","resource_class":"small","export_targets":["openqasm3","qiskit_python"],"lean_source":"import HeytingLean.Quantum.ProofCarrying.CircuitSpec\n\nopen HeytingLean.Quantum.ProofCarrying\n\ndef spec : CircuitSpec where\n  circuitId := \"agent_bell\"\n  semanticProfile := \"unsigned_binary_symplectic_clifford_v1\"\n  qubits := 2\n  classicalBits := 0\n  ops := [.gate .H 0 0, .gate .CX 0 1]\n  claims := []\n  metadataScope := \"agent request\"\n\ntheorem spec_claims : CircuitSpec.ClaimsHold spec := by\n  simp [CircuitSpec.ClaimsHold, spec]\n"}
```

##### `execute_locally`

Use for local simulator observations from Lean-owned construction, routing, and lowering. Required: `lean_source` defining `spec` with a `LeanCPExecutableSpec` instance; `shots` 1-65536. Optional: `resource_class` (`small` or `standard`). The service chooses a compatible bundled backend; there is no backend-selection field. With `classicalBits := 0`, `.auto` observes terminal Z on every qubit, which makes the simulation runnable without adding measure operations to the authored spec. Compact results report that observation and whether measurements were injected. Lean runs as `trusted_direct_v1` in the shared Cloud Run service container, not an untrusted-code sandbox.

```json
{"action":"execute_locally","resource_class":"small","shots":1024,"lean_source":"import HeytingLean.Quantum.ProofCarrying.CircuitSpec\n\nopen HeytingLean.Quantum.ProofCarrying\n\ndef spec : CircuitSpec where\n  circuitId := \"agent_bell\"\n  semanticProfile := \"unsigned_binary_symplectic_clifford_v1\"\n  qubits := 2\n  classicalBits := 0\n  ops := [.gate .H 0 0, .gate .CX 0 1]\n  claims := []\n  metadataScope := \"agent request\"\n\ntheorem spec_claims : CircuitSpec.ClaimsHold spec := by\n  simp [CircuitSpec.ClaimsHold, spec]\n"}
```

#### Task action

##### `get_task`

Use only with the exact `task_id` returned by an always-background action or a direct action deferred during startup. This action costs zero credits. While processing, set `wait_seconds` to 60 so one call waits for a meaningful task change without reaching the chat tool-call deadline. Repeat only after that long poll returns, and do not create duplicate paid work. The response keeps `action: get_task`; `task_action` identifies the retained operation. `warming_service` is an accepted request waiting for startup, `waiting_on_kernel` is running proof-related work, `running_action` is running a deferred direct action, and `awaiting_resume` or `resuming` is recovering an interrupted worker. `progress` deliberately stays 0 rather than inventing a percentage; a moving `date_updated` heartbeat and the current `stage` show that the worker is alive.

```json
{"action":"get_task","task_id":"12345678-1234-1234-1234-123456789012","wait_seconds":60}
```

## When To Use
- Use this skill for `Quantum Circuit Builder with Proof` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: quantum circuit builder with proof, formally verified quantum circuit design, proof carrying quantum circuit certificates (qpcert), independent verification of a quantum proof certificate from another party, audit ready quantum computing artifacts for research and compliance, certify circuit, circuit, claims.
- Supported action names: `certify_circuit`, `certify_from_lean`, `execute_locally`, `export_provider_programs`, `extract_circuit`, `get_corpus_example`, `get_document`, `get_task`, `import_provider_circuit`, `inspect_circuit`, `instantiate_template`, `search_corpus_examples`, `search_knowledge`, `search_lean`, `verify_certificate`.

## Use Cases
- Formally verified quantum circuit design
- Proof-carrying quantum circuit certificates (qpcert)
- Independent verification of a quantum proof certificate from another party
- Audit-ready quantum computing artifacts for research and compliance
- Import Qiskit Cirq and Braket circuits without executing code
- Export verified OpenQASM 3 Qiskit Cirq and Braket programs
- Quantum circuit diagrams as downloadable PNG or JPEG
- GHZ Bernstein-Vazirani teleportation Grover and QFT circuit templates
- Lean 4 quantum circuit proofs and theorem search
- Local quantum circuit simulation with explicit measurement accounting
- Reproducible quantum circuit exchange between AI agents and systems
- Quantum computing research with a searchable knowledge base and Lean corpus

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `15`.
x402 availability: not enabled for this product.

- `certify_circuit` (action slug: `certify-circuit`): Use when a normalized circuit and an exact claim ledger are ready for kernel-backed certificate construction. The request is accepted as a background task even while the proof service starts; poll free get_task and do not resubmit it. The service validates the circuit, constructs the qpcert, and verifies its generated certificate; do not automatically call verify_certificate or extract_circuit on the fresh result. Price: `10` credits. Parameters: `circuit`, `claims`.
- `certify_from_lean` (action slug: `certify-from-lean`): Use when restricted, internally trusted Lean CircuitSpec source is authoritative. The request is accepted as a background task even while the proof service starts; poll free get_task and do not resubmit it. Cloud Run executes Lean as trusted_direct_v1 in the shared service container; IAM authentication is not untrusted-code isolation. On success, returns a verified qpcert in File Manager; receipts report execution_mode and untrusted_code_isolation. Price: `15` credits. Parameters: `claims`, `lean_source`, `resource_class`.
- `execute_locally` (action slug: `execute-locally`): Use for local simulator observations from internally trusted Lean-owned construction, routing, and lowering. The request is accepted as a background task even while the proof service starts; poll free get_task and do not resubmit it. Lean runs as trusted_direct_v1 in the shared Cloud Run service container, not an untrusted-code sandbox. With no classical bits, .auto selects terminal_z_all; compact results expose observation and measurement_injected. Simulation is never a proof tier or hardware execution. Price: `15` credits. Parameters: `lean_source`, `resource_class`, `shots`.
- `export_provider_programs` (action slug: `export-provider-programs`): Use to generate checked offline provider observation programs from internally trusted Lean. The request is accepted as a background task even while the proof service starts; poll free get_task and do not resubmit it. Lean runs as trusted_direct_v1 in the shared Cloud Run service container, not an untrusted-code sandbox. With no classical bits, .auto selects terminal_z_all and provider output materializes or records terminal measurement; compact results expose observation and measurement_injected. Output is not hardware execution or proof. Price: `10` credits. Parameters: `export_targets`, `lean_source`, `resource_class`.
- `extract_circuit` (action slug: `extract-circuit`): Use after receiving an existing qpcert when the normalized circuit and projections must be recovered by proof replay. The request is accepted as a background task even while the proof service starts; poll free get_task and do not resubmit it. Do not call merely to inspect a certificate just produced in the same flow. Price: `10` credits. Parameters: `certificate_file_id`.
- `get_corpus_example` (action slug: `get-corpus-example`): Use after search_corpus_examples to retrieve one exact Lean, circuit, claims, qpcert, template, provider-intake, or designer-sample asset. The path is corpus-relative; traversal and absolute paths reject. If the proof service is starting, the request is retained as a background task; poll free get_task and do not resubmit it. Price: `1` credits. Parameters: `example_path`.
- `get_document` (action slug: `get-document`): Use after search_knowledge to retrieve the complete selected knowledge record and provenance. Do not guess document IDs. If the proof service is starting, the request is retained as a background task; poll free get_task and do not resubmit it. Price: `1` credits. Parameters: `document_id`.
- `get_task` (action slug: `get-task`): Free polling action for an always-background action or a direct action retained during startup. Use wait_seconds=60 while processing so the server waits for a stage or terminal change while remaining below the chat tool-call deadline. The response keeps action=get_task and reports the retained operation as task_action. warming_service means the accepted request is waiting for proof-service startup; waiting_on_kernel means proof-related work is running; running_action means a deferred direct action is running. While processing, progress remains 0 because no trustworthy percentage is available; a moving date_updated shows worker liveness. Never resubmit a processing paid action; outputs may contain File Manager references. Price: `0` credits. Parameters: `task_id`, `wait_seconds`.
- `import_provider_circuit` (action slug: `import-provider-circuit`): Use to parse bounded hand-authored Qiskit, Cirq, or Braket Python into normalized circuit IR without executing the source. This is parsing and round-trip validation, not proof. Use certify_circuit afterward when certification is required. If the proof service is starting, the request is retained as a background task; poll free get_task and do not resubmit it. Price: `3` credits. Parameters: `circuit_id`, `provider_target`, `qubit_count`, `semantic_profile`, `source`.
- `inspect_circuit` (action slug: `inspect-circuit`): Use for structural/semantic validation and subject-address computation before certification, or when visual explanations are useful. Validation and visualization are not proof or hardware execution. Set image_format to store a logical wire-circuit PNG or JPEG in the current budget's File Manager for display with AgentPMT's image card. If the proof service is starting, the request is retained as a background task; poll free get_task and do not resubmit it. Price: `3` credits. Parameters: `circuit`, `claims`, `image_format`, `include_visualizations`.
- `instantiate_template` (action slug: `instantiate-template`): Use to create a normalized circuit from a supported GHZ, Bernstein-Vazirani, teleportation, Grover, or QFT template. This expands a template but does not certify it; pass the resulting circuit and claims to certify_circuit when proof is required. If the proof service is starting, the request is retained as a background task; poll free get_task and do not resubmit it. Price: `2` credits. Parameters: `descriptor`.
- `search_corpus_examples` (action slug: `search-corpus-examples`): Use to find worked proof chains, template inputs, provider-intake samples, or designer samples in the bundled corpus. With no query, returns a bounded index. Results contain exact relative paths accepted by get_corpus_example. If the proof service is starting, the request is retained as a background task; poll free get_task and do not resubmit it. Price: `1` credits. Parameters: `query`, `result_count`.
- `search_knowledge` (action slug: `search-knowledge`): Use when the agent needs conceptual, research, architecture, or repository context before acting. Do not call as a mandatory preflight. Returns ranked results with source provenance; use get_document for the selected full record. If the proof service is starting, the request is retained as a background task; poll free get_task and do not resubmit it. Price: `2` credits. Parameters: `query`, `result_count`, `search_mode`.
- `search_lean` (action slug: `search-lean`): Use after starting from a worked CircuitSpec corpus example when the agent needs a Lean declaration, theorem, namespace, signature, or authoring primitive. authoring_only restricts results to the four modules admitted by submitted specs; false browses the wider reference corpus. If the proof service is starting, the request is retained as a background task; poll free get_task and do not resubmit it. Price: `2` credits. Parameters: `authoring_only`, `query`, `result_count`.
- `verify_certificate` (action slug: `verify-certificate`): Use at a trust boundary to independently replay a qpcert received from another party against separately supplied circuit and claims. The request is accepted as a background task even while the proof service starts; poll free get_task and do not resubmit it. Do not automatically re-verify a qpcert just produced by certify_circuit or certify_from_lean, because those actions already verify their generated certificate. Price: `10` credits. Parameters: `certificate_file_id`, `circuit`, `claims`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "quantum-circuit-builder-with-proof"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "quantum-circuit-builder-with-proof"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "quantum-circuit-builder-with-proof"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "quantum-circuit-builder-with-proof"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "quantum-circuit-builder-with-proof"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "quantum-circuit-builder-with-proof"
  }
}
```

## Call This Tool
Product slug: `quantum-circuit-builder-with-proof`

Marketplace page: https://www.agentpmt.com/marketplace/quantum-circuit-builder-with-proof

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Quantum-Circuit-Builder-with-Proof",
    "arguments": {
      "action": "certify_circuit",
      "circuit": {
        "circuit_id": "example circuit id",
        "classical_bits": [
          {
            "id": "example id"
          }
        ],
        "initial_state": "zero",
        "metadata": {
          "name": "example name",
          "scope": "example scope"
        },
        "operations": [
          {
            "kind": "gate",
            "op_id": "example op id"
          }
        ],
        "qubits": [
          {
            "id": "example id"
          }
        ],
        "schema": "heyting.quantum_circuit_ir.v1",
        "semantic_profile": "unsigned_binary_symplectic_clifford_v1"
      },
      "claims": {
        "circuit_subject_sha256": "example circuit subject sha256",
        "claims": [
          {
            "accepted_evidence_tiers": [
              "kernel_certified"
            ],
            "claim_id": "example claim id",
            "description": "example description",
            "statement": {
              "claim_type": "well_formed",
              "parameters": {},
              "predicate": {
                "name": "example name",
                "namespace": "example namespace",
                "version": "example version"
              },
              "profile": "example profile",
              "relation": "example relation"
            }
          }
        ],
        "ledger_id": "example ledger id",
        "schema": "heyting.quantum_claim_evidence.v1",
        "semantic_profile": "unsigned_binary_symplectic_clifford_v1"
      }
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "quantum-circuit-builder-with-proof",
  "parameters": {
    "action": "certify_circuit",
    "circuit": {
      "circuit_id": "example circuit id",
      "classical_bits": [
        {
          "id": "example id"
        }
      ],
      "initial_state": "zero",
      "metadata": {
        "name": "example name",
        "scope": "example scope"
      },
      "operations": [
        {
          "kind": "gate",
          "op_id": "example op id"
        }
      ],
      "qubits": [
        {
          "id": "example id"
        }
      ],
      "schema": "heyting.quantum_circuit_ir.v1",
      "semantic_profile": "unsigned_binary_symplectic_clifford_v1"
    },
    "claims": {
      "circuit_subject_sha256": "example circuit subject sha256",
      "claims": [
        {
          "accepted_evidence_tiers": [
            "kernel_certified"
          ],
          "claim_id": "example claim id",
          "description": "example description",
          "statement": {
            "claim_type": "well_formed",
            "parameters": {},
            "predicate": {
              "name": "example name",
              "namespace": "example namespace",
              "version": "example version"
            },
            "profile": "example profile",
            "relation": "example relation"
          }
        }
      ],
      "ledger_id": "example ledger id",
      "schema": "heyting.quantum_claim_evidence.v1",
      "semantic_profile": "unsigned_binary_symplectic_clifford_v1"
    }
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `certify_circuit` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/quantum-circuit-builder-with-proof
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
