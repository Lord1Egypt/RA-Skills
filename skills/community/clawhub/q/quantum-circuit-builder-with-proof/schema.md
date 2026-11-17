# Quantum Circuit Builder with Proof Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `quantum-circuit-builder-with-proof`

x402 availability: not enabled for this product.

## `certify_circuit`

Action slug: `certify-circuit`

Price: `10` credits

Use when a normalized circuit and an exact claim ledger are ready for kernel-backed certificate construction. The request is accepted as a background task even while the proof service starts; poll free get_task and do not resubmit it. The service validates the circuit, constructs the qpcert, and verifies its generated certificate; do not automatically call verify_certificate or extract_circuit on the fresh result.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `circuit` | `object` | yes | Complete validated heyting.quantum_circuit_ir.v1 object. Required fields are schema, circuit_id, semantic_profile, nonempty qubits, classical_bits, initial_state, operations, and optional metadata; use inspect_circuit or a corpus .qcir.json example for the exact shape. |
| `claims` | `object` | yes | Complete heyting.quantum_claim_evidence.v1 ledger bound to circuit_subject_sha256. Pass dashboard certification_claims unchanged or use a matching corpus .claims.json example; certification rejects unsupported, malformed, or unbound claims. |

Sample parameters:

```json
{
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
```

Generated JSON parameter schema:

```json
{
  "circuit": {
    "description": "Complete validated heyting.quantum_circuit_ir.v1 object. Required fields are schema, circuit_id, semantic_profile, nonempty qubits, classical_bits, initial_state, operations, and optional metadata; use inspect_circuit or a corpus .qcir.json example for the exact shape.",
    "properties": {
      "circuit_id": {
        "description": "Stable circuit identifier.",
        "required": true,
        "type": "string"
      },
      "classical_bits": {
        "description": "Classical-bit declarations; may be empty.",
        "items": {
          "properties": {
            "id": {
              "description": "Unique classical-bit ID.",
              "required": true,
              "type": "string"
            }
          },
          "type": "object"
        },
        "required": true,
        "type": "array"
      },
      "initial_state": {
        "description": "Initial state.",
        "enum": [
          "zero"
        ],
        "required": true,
        "type": "string"
      },
      "metadata": {
        "description": "Optional descriptive metadata.",
        "properties": {
          "name": {
            "description": "Human-readable name.",
            "required": false,
            "type": "string"
          },
          "scope": {
            "description": "Human-readable scope.",
            "required": false,
            "type": "string"
          }
        },
        "required": false,
        "type": "object"
      },
      "operations": {
        "description": "Ordered gate, measure, and reset operations in canonical circuit IR form.",
        "items": {
          "properties": {
            "kind": {
              "description": "gate, measure, or reset.",
              "enum": [
                "gate",
                "measure",
                "reset"
              ],
              "required": true,
              "type": "string"
            },
            "op_id": {
              "description": "Unique operation ID.",
              "required": true,
              "type": "string"
            }
          },
          "type": "object"
        },
        "required": true,
        "type": "array"
      },
      "qubits": {
        "description": "Nonempty qubit declarations.",
        "items": {
          "properties": {
            "id": {
              "description": "Unique qubit ID.",
              "required": true,
              "type": "string"
            }
          },
          "type": "object"
        },
        "minItems": 1,
        "required": true,
        "type": "array"
      },
      "schema": {
        "description": "Circuit artifact schema.",
        "enum": [
          "heyting.quantum_circuit_ir.v1"
        ],
        "required": true,
        "type": "string"
      },
      "semantic_profile": {
        "description": "Exact circuit semantics.",
        "enum": [
          "unsigned_binary_symplectic_clifford_v1",
          "signed_binary_symplectic_v2",
          "exact_clifford_t_v2",
          "exact_clifford_t_measurement_v1",
          "exact_cyclotomic_2k_v1",
          "exact_cyclotomic_24_v1"
        ],
        "required": true,
        "type": "string"
      }
    },
    "required": true,
    "type": "object"
  },
  "claims": {
    "description": "Complete heyting.quantum_claim_evidence.v1 ledger bound to circuit_subject_sha256. Pass dashboard certification_claims unchanged or use a matching corpus .claims.json example; certification rejects unsupported, malformed, or unbound claims.",
    "properties": {
      "circuit_subject_sha256": {
        "description": "Canonical subject digest returned by inspection/import/template work.",
        "pattern": "^[0-9a-f]{64}$",
        "required": true,
        "type": "string"
      },
      "claims": {
        "description": "Nonempty exact claim obligations.",
        "items": {
          "properties": {
            "accepted_evidence_tiers": {
              "description": "Allowed evidence tiers.",
              "items": {
                "enum": [
                  "kernel_certified",
                  "checker_verified",
                  "simulator_crosscheck",
                  "provider_attested",
                  "reported"
                ],
                "type": "string"
              },
              "minItems": 1,
              "required": true,
              "type": "array"
            },
            "claim_id": {
              "description": "Stable claim ID.",
              "required": true,
              "type": "string"
            },
            "description": {
              "description": "Bounded human-readable claim scope.",
              "required": true,
              "type": "string"
            },
            "statement": {
              "description": "Copy the complete typed statement without translating it. well_formed requires profile; circuit_property requires predicate, parameters, and relation.",
              "properties": {
                "claim_type": {
                  "description": "Exact claim family; preserve this value and its corresponding fields.",
                  "enum": [
                    "well_formed",
                    "normalization_equivalent",
                    "lowering_equivalent",
                    "circuit_property",
                    "resource_optimality",
                    "simulation_crosscheck",
                    "execution_attestation",
                    "visualization_correspondence"
                  ],
                  "required": true,
                  "type": "string"
                },
                "parameters": {
                  "description": "Required string map for circuit_property; preserve all supplied entries.",
                  "required": false,
                  "type": "object"
                },
                "predicate": {
                  "description": "Required for circuit_property; preserve namespace, name, and version exactly.",
                  "properties": {
                    "name": {
                      "description": "Predicate name.",
                      "required": true,
                      "type": "string"
                    },
                    "namespace": {
                      "description": "Predicate namespace.",
                      "required": true,
                      "type": "string"
                    },
                    "version": {
                      "description": "Predicate version.",
                      "required": true,
                      "type": "string"
                    }
                  },
                  "required": false,
                  "type": "object"
                },
                "profile": {
                  "description": "Required for well_formed; must match the circuit profile.",
                  "required": false,
                  "type": "string"
                },
                "relation": {
                  "description": "Required exact equivalence relation for claim families that use one.",
                  "required": false,
                  "type": "string"
                }
              },
              "required": true,
              "type": "object"
            }
          },
          "type": "object"
        },
        "minItems": 1,
        "required": true,
        "type": "array"
      },
      "ledger_id": {
        "description": "Stable ledger ID.",
        "required": true,
        "type": "string"
      },
      "schema": {
        "description": "Claim-ledger artifact schema.",
        "enum": [
          "heyting.quantum_claim_evidence.v1"
        ],
        "required": true,
        "type": "string"
      },
      "semantic_profile": {
        "description": "Must match circuit.semantic_profile.",
        "enum": [
          "unsigned_binary_symplectic_clifford_v1",
          "signed_binary_symplectic_v2",
          "exact_clifford_t_v2",
          "exact_clifford_t_measurement_v1",
          "exact_cyclotomic_2k_v1",
          "exact_cyclotomic_24_v1"
        ],
        "required": true,
        "type": "string"
      }
    },
    "required": true,
    "type": "object"
  }
}
```

## `certify_from_lean`

Action slug: `certify-from-lean`

Price: `15` credits

Use when restricted, internally trusted Lean CircuitSpec source is authoritative. The request is accepted as a background task even while the proof service starts; poll free get_task and do not resubmit it. Cloud Run executes Lean as trusted_direct_v1 in the shared service container; IAM authentication is not untrusted-code isolation. On success, returns a verified qpcert in File Manager; receipts report execution_mode and untrusted_code_isolation.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `claims` | `object` | no | Optional complete heyting.quantum_claim_evidence.v1 ledger. Omit to request the service's minimal well-formed claim; when supplied, copy the complete ledger from a trusted matching source without dropping nested statement fields. |
| `lean_source` | `string` | yes | Complete CircuitSpec authoring fragment defining spec. Use search_lean with authoring_only=true and a worked .lean corpus example when authoring. Maximum 1048576 characters. |
| `resource_class` | `string` | no | small supports up to 2 qubits; standard supports up to 4. Each admitted Lean source run is capped at 1,200 seconds and 20,000,000 heartbeats. |

Sample parameters:

```json
{
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
  },
  "lean_source": "example lean source",
  "resource_class": "small"
}
```

Generated JSON parameter schema:

```json
{
  "claims": {
    "description": "Optional complete heyting.quantum_claim_evidence.v1 ledger. Omit to request the service's minimal well-formed claim; when supplied, copy the complete ledger from a trusted matching source without dropping nested statement fields.",
    "properties": {
      "circuit_subject_sha256": {
        "description": "Canonical circuit subject digest.",
        "pattern": "^[0-9a-f]{64}$",
        "required": true,
        "type": "string"
      },
      "claims": {
        "description": "Nonempty exact claim obligations.",
        "items": {
          "properties": {
            "accepted_evidence_tiers": {
              "description": "Allowed evidence tiers.",
              "items": {
                "enum": [
                  "kernel_certified",
                  "checker_verified",
                  "simulator_crosscheck",
                  "provider_attested",
                  "reported"
                ],
                "type": "string"
              },
              "minItems": 1,
              "required": true,
              "type": "array"
            },
            "claim_id": {
              "description": "Stable claim ID.",
              "required": true,
              "type": "string"
            },
            "description": {
              "description": "Bounded claim scope.",
              "required": true,
              "type": "string"
            },
            "statement": {
              "description": "Copy the complete typed statement. well_formed requires profile; circuit_property requires predicate, parameters, and relation.",
              "properties": {
                "claim_type": {
                  "description": "Exact claim family; preserve this value and its corresponding fields.",
                  "enum": [
                    "well_formed",
                    "normalization_equivalent",
                    "lowering_equivalent",
                    "circuit_property",
                    "resource_optimality",
                    "simulation_crosscheck",
                    "execution_attestation",
                    "visualization_correspondence"
                  ],
                  "required": true,
                  "type": "string"
                },
                "parameters": {
                  "description": "Required string map for circuit_property; preserve all supplied entries.",
                  "required": false,
                  "type": "object"
                },
                "predicate": {
                  "description": "Required for circuit_property; preserve namespace, name, and version exactly.",
                  "properties": {
                    "name": {
                      "description": "Predicate name.",
                      "required": true,
                      "type": "string"
                    },
                    "namespace": {
                      "description": "Predicate namespace.",
                      "required": true,
                      "type": "string"
                    },
                    "version": {
                      "description": "Predicate version.",
                      "required": true,
                      "type": "string"
                    }
                  },
                  "required": false,
                  "type": "object"
                },
                "profile": {
                  "description": "Required for well_formed; must match the circuit profile.",
                  "required": false,
                  "type": "string"
                },
                "relation": {
                  "description": "Required exact equivalence relation for claim families that use one.",
                  "required": false,
                  "type": "string"
                }
              },
              "required": true,
              "type": "object"
            }
          },
          "type": "object"
        },
        "minItems": 1,
        "required": true,
        "type": "array"
      },
      "ledger_id": {
        "description": "Stable ledger ID.",
        "required": true,
        "type": "string"
      },
      "schema": {
        "description": "Claim-ledger artifact schema.",
        "enum": [
          "heyting.quantum_claim_evidence.v1"
        ],
        "required": true,
        "type": "string"
      },
      "semantic_profile": {
        "description": "Must match the emitted circuit.",
        "enum": [
          "unsigned_binary_symplectic_clifford_v1",
          "signed_binary_symplectic_v2",
          "exact_clifford_t_v2",
          "exact_clifford_t_measurement_v1",
          "exact_cyclotomic_2k_v1",
          "exact_cyclotomic_24_v1"
        ],
        "required": true,
        "type": "string"
      }
    },
    "required": false,
    "type": "object"
  },
  "lean_source": {
    "description": "Complete CircuitSpec authoring fragment defining spec. Use search_lean with authoring_only=true and a worked .lean corpus example when authoring. Maximum 1048576 characters.",
    "maxLength": 1048576,
    "minLength": 1,
    "required": true,
    "type": "string"
  },
  "resource_class": {
    "description": "small supports up to 2 qubits; standard supports up to 4. Each admitted Lean source run is capped at 1,200 seconds and 20,000,000 heartbeats.",
    "enum": [
      "small",
      "standard"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `execute_locally`

Action slug: `execute-locally`

Price: `15` credits

Use for local simulator observations from internally trusted Lean-owned construction, routing, and lowering. The request is accepted as a background task even while the proof service starts; poll free get_task and do not resubmit it. Lean runs as trusted_direct_v1 in the shared Cloud Run service container, not an untrusted-code sandbox. With no classical bits, .auto selects terminal_z_all; compact results expose observation and measurement_injected. Simulation is never a proof tier or hardware execution.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `lean_source` | `string` | yes | Complete admitted Lean source defining spec with a LeanCPExecutableSpec instance. |
| `resource_class` | `string` | no | small supports up to 2 qubits; standard supports up to 4. |
| `shots` | `integer` | yes | Number of local simulator shots. |

Sample parameters:

```json
{
  "lean_source": "example lean source",
  "resource_class": "small",
  "shots": 1
}
```

Generated JSON parameter schema:

```json
{
  "lean_source": {
    "description": "Complete admitted Lean source defining spec with a LeanCPExecutableSpec instance.",
    "maxLength": 1048576,
    "minLength": 1,
    "required": true,
    "type": "string"
  },
  "resource_class": {
    "description": "small supports up to 2 qubits; standard supports up to 4.",
    "enum": [
      "small",
      "standard"
    ],
    "required": false,
    "type": "string"
  },
  "shots": {
    "description": "Number of local simulator shots.",
    "maximum": 65536,
    "minimum": 1,
    "required": true,
    "type": "integer"
  }
}
```

## `export_provider_programs`

Action slug: `export-provider-programs`

Price: `10` credits

Use to generate checked offline provider observation programs from internally trusted Lean. The request is accepted as a background task even while the proof service starts; poll free get_task and do not resubmit it. Lean runs as trusted_direct_v1 in the shared Cloud Run service container, not an untrusted-code sandbox. With no classical bits, .auto selects terminal_z_all and provider output materializes or records terminal measurement; compact results expose observation and measurement_injected. Output is not hardware execution or proof.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `export_targets` | `array` | yes | One to four unique offline output targets. Current provider target snapshots are resolved privately by the connector. |
| `lean_source` | `string` | yes | Complete CircuitSpec authoring fragment defining spec. The current service export contract is Lean-owned; this action does not accept a qpcert. |
| `resource_class` | `string` | no | small supports up to 2 qubits; standard supports up to 4. Omit only when the service default is appropriate. |

Sample parameters:

```json
{
  "export_targets": [
    "openqasm3"
  ],
  "lean_source": "example lean source",
  "resource_class": "small"
}
```

Generated JSON parameter schema:

```json
{
  "export_targets": {
    "description": "One to four unique offline output targets. Current provider target snapshots are resolved privately by the connector.",
    "items": {
      "enum": [
        "openqasm3",
        "qiskit_python",
        "cirq_python",
        "braket_python"
      ],
      "type": "string"
    },
    "maxItems": 4,
    "minItems": 1,
    "required": true,
    "type": "array",
    "uniqueItems": true
  },
  "lean_source": {
    "description": "Complete CircuitSpec authoring fragment defining spec. The current service export contract is Lean-owned; this action does not accept a qpcert.",
    "maxLength": 1048576,
    "minLength": 1,
    "required": true,
    "type": "string"
  },
  "resource_class": {
    "description": "small supports up to 2 qubits; standard supports up to 4. Omit only when the service default is appropriate.",
    "enum": [
      "small",
      "standard"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `extract_circuit`

Action slug: `extract-circuit`

Price: `10` credits

Use after receiving an existing qpcert when the normalized circuit and projections must be recovered by proof replay. The request is accepted as a background task even while the proof service starts; poll free get_task and do not resubmit it. Do not call merely to inspect a certificate just produced in the same flow.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `certificate_file_id` | `string` | yes | Budget-visible File Manager ID containing a typed qpcert. The kernel replays the evidence before returning the normalized circuit. |

Sample parameters:

```json
{
  "certificate_file_id": "example certificate file id"
}
```

Generated JSON parameter schema:

```json
{
  "certificate_file_id": {
    "description": "Budget-visible File Manager ID containing a typed qpcert. The kernel replays the evidence before returning the normalized circuit.",
    "maxLength": 200,
    "minLength": 1,
    "required": true,
    "type": "string"
  }
}
```

## `get_corpus_example`

Action slug: `get-corpus-example`

Price: `1` credits

Use after search_corpus_examples to retrieve one exact Lean, circuit, claims, qpcert, template, provider-intake, or designer-sample asset. The path is corpus-relative; traversal and absolute paths reject. If the proof service is starting, the request is retained as a background task; poll free get_task and do not resubmit it.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `example_path` | `string` | yes | Exact relative asset path returned by search_corpus_examples, such as authored_specs/bell_spec.lean. |

Sample parameters:

```json
{
  "example_path": "example example path"
}
```

Generated JSON parameter schema:

```json
{
  "example_path": {
    "description": "Exact relative asset path returned by search_corpus_examples, such as authored_specs/bell_spec.lean.",
    "maxLength": 500,
    "minLength": 1,
    "required": true,
    "type": "string"
  }
}
```

## `get_document`

Action slug: `get-document`

Price: `1` credits

Use after search_knowledge to retrieve the complete selected knowledge record and provenance. Do not guess document IDs. If the proof service is starting, the request is retained as a background task; poll free get_task and do not resubmit it.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document_id` | `integer` | yes | Positive document ID returned by search_knowledge. |

Sample parameters:

```json
{
  "document_id": 1
}
```

Generated JSON parameter schema:

```json
{
  "document_id": {
    "description": "Positive document ID returned by search_knowledge.",
    "minimum": 1,
    "required": true,
    "type": "integer"
  }
}
```

## `get_task`

Action slug: `get-task`

Price: `0` credits

Free polling action for an always-background action or a direct action retained during startup. Use wait_seconds=60 while processing so the server waits for a stage or terminal change while remaining below the chat tool-call deadline. The response keeps action=get_task and reports the retained operation as task_action. warming_service means the accepted request is waiting for proof-service startup; waiting_on_kernel means proof-related work is running; running_action means a deferred direct action is running. While processing, progress remains 0 because no trustworthy percentage is available; a moving date_updated shows worker liveness. Never resubmit a processing paid action; outputs may contain File Manager references.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `task_id` | `string` | yes | Exact budget-scoped UUID returned by the initiating action. Task IDs from another budget are not visible. |
| `wait_seconds` | `integer` | no | Long-poll duration. Use 60 while processing; the call returns sooner when status, stage, progress, error, or outputs change and remains below the chat tool-call deadline. Defaults to 0 for an immediate snapshot. |

Sample parameters:

```json
{
  "task_id": "example task id",
  "wait_seconds": 0
}
```

Generated JSON parameter schema:

```json
{
  "task_id": {
    "description": "Exact budget-scoped UUID returned by the initiating action. Task IDs from another budget are not visible.",
    "maxLength": 36,
    "minLength": 36,
    "pattern": "^[0-9a-fA-F-]{36}$",
    "required": true,
    "type": "string"
  },
  "wait_seconds": {
    "default": 0,
    "description": "Long-poll duration. Use 60 while processing; the call returns sooner when status, stage, progress, error, or outputs change and remains below the chat tool-call deadline. Defaults to 0 for an immediate snapshot.",
    "maximum": 60,
    "minimum": 0,
    "required": false,
    "type": "integer"
  }
}
```

## `import_provider_circuit`

Action slug: `import-provider-circuit`

Price: `3` credits

Use to parse bounded hand-authored Qiskit, Cirq, or Braket Python into normalized circuit IR without executing the source. This is parsing and round-trip validation, not proof. Use certify_circuit afterward when certification is required. If the proof service is starting, the request is retained as a background task; poll free get_task and do not resubmit it.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `circuit_id` | `string` | yes | Stable lowercase identifier for the imported circuit. |
| `provider_target` | `string` | yes | Grammar used to parse source. Provider source is never executed. |
| `qubit_count` | `integer` | no | Required for braket_python because Circuit() does not encode idle-wire width. Optional for Qiskit and Cirq, which declare width. |
| `semantic_profile` | `string` | yes | Explicit semantic profile; the parser never guesses it. |
| `source` | `string` | yes | UTF-8 hand-authored provider source ending in exactly one newline. Qiskit requires exactly `from qiskit import QuantumCircuit` followed by `circuit = QuantumCircuit(N)`; aliases such as qc reject. Maximum 262144 characters. Generated or dynamic Python is outside the bounded grammar. |

Sample parameters:

```json
{
  "circuit_id": "example circuit id",
  "provider_target": "qiskit_python",
  "qubit_count": 1,
  "semantic_profile": "unsigned_binary_symplectic_clifford_v1",
  "source": "example source"
}
```

Generated JSON parameter schema:

```json
{
  "circuit_id": {
    "description": "Stable lowercase identifier for the imported circuit.",
    "pattern": "^[a-z][a-z0-9_]{0,63}$",
    "required": true,
    "type": "string"
  },
  "provider_target": {
    "description": "Grammar used to parse source. Provider source is never executed.",
    "enum": [
      "qiskit_python",
      "cirq_python",
      "braket_python"
    ],
    "required": true,
    "type": "string"
  },
  "qubit_count": {
    "description": "Required for braket_python because Circuit() does not encode idle-wire width. Optional for Qiskit and Cirq, which declare width.",
    "maximum": 4096,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "semantic_profile": {
    "description": "Explicit semantic profile; the parser never guesses it.",
    "enum": [
      "unsigned_binary_symplectic_clifford_v1",
      "signed_binary_symplectic_v2",
      "exact_clifford_t_v2",
      "exact_clifford_t_measurement_v1",
      "exact_cyclotomic_2k_v1",
      "exact_cyclotomic_24_v1"
    ],
    "required": true,
    "type": "string"
  },
  "source": {
    "description": "UTF-8 hand-authored provider source ending in exactly one newline. Qiskit requires exactly `from qiskit import QuantumCircuit` followed by `circuit = QuantumCircuit(N)`; aliases such as qc reject. Maximum 262144 characters. Generated or dynamic Python is outside the bounded grammar.",
    "maxLength": 262144,
    "minLength": 1,
    "required": true,
    "type": "string"
  }
}
```

## `inspect_circuit`

Action slug: `inspect-circuit`

Price: `3` credits

Use for structural/semantic validation and subject-address computation before certification, or when visual explanations are useful. Validation and visualization are not proof or hardware execution. Set image_format to store a logical wire-circuit PNG or JPEG in the current budget's File Manager for display with AgentPMT's image card. If the proof service is starting, the request is retained as a background task; poll free get_task and do not resubmit it.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `circuit` | `object` | yes | Complete heyting.quantum_circuit_ir.v1 object, normally returned by instantiate_template, import_provider_circuit, certify_from_lean diagnostics, or extract_circuit. |
| `claims` | `object` | no | Optional heyting.quantum_claim_evidence.v1 ledger used only to enrich applicable visualizations. It is not certified by this action. |
| `image_format` | `string` | no | Optional stored image output. Set to png or jpeg to render the digest-bound logical wire_circuit projection, save it in budget-scoped File Manager, and return image_file metadata. The image is explanatory, not proof or hardware execution. |
| `include_visualizations` | `boolean` | no | When true, return all applicable structured semantic visualization lenses after validation. Defaults to false. This is independent of image_format. |

Sample parameters:

```json
{
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
        "basis": "x",
        "classical_bit": "example classical bit",
        "controls": [
          "example control"
        ],
        "gate": "example gate",
        "kind": "gate",
        "op_id": "example op id",
        "parameters": [
          {
            "inverse": true,
            "level": 0,
            "parameter_type": "example parameter type"
          }
        ],
        "qubit": "example qubit"
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
  },
  "image_format": "png",
  "include_visualizations": false
}
```

Generated JSON parameter schema:

```json
{
  "circuit": {
    "description": "Complete heyting.quantum_circuit_ir.v1 object, normally returned by instantiate_template, import_provider_circuit, certify_from_lean diagnostics, or extract_circuit.",
    "properties": {
      "circuit_id": {
        "description": "Stable circuit identifier.",
        "maxLength": 64,
        "minLength": 1,
        "required": true,
        "type": "string"
      },
      "classical_bits": {
        "description": "Ordered classical-bit declarations; may be empty.",
        "items": {
          "properties": {
            "id": {
              "description": "Unique classical-bit ID referenced by measurements.",
              "required": true,
              "type": "string"
            }
          },
          "type": "object"
        },
        "required": true,
        "type": "array"
      },
      "initial_state": {
        "description": "Declared initial state; current certified flows use zero.",
        "enum": [
          "zero"
        ],
        "required": true,
        "type": "string"
      },
      "metadata": {
        "description": "Optional descriptive metadata; it does not create proof claims.",
        "properties": {
          "name": {
            "description": "Human-readable name.",
            "required": false,
            "type": "string"
          },
          "scope": {
            "description": "Human-readable epistemic scope.",
            "required": false,
            "type": "string"
          }
        },
        "required": false,
        "type": "object"
      },
      "operations": {
        "description": "Ordered operations. Gate rows use kind, op_id, gate, controls, targets, parameters; measurement rows use basis, qubit, classical_bit; reset rows use qubit.",
        "items": {
          "properties": {
            "basis": {
              "description": "Measurement basis for measure rows.",
              "enum": [
                "x",
                "y",
                "z"
              ],
              "required": false,
              "type": "string"
            },
            "classical_bit": {
              "description": "Destination bit ID for measurement rows.",
              "required": false,
              "type": "string"
            },
            "controls": {
              "description": "Control-qubit IDs for gate rows.",
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            },
            "gate": {
              "description": "Gate mnemonic for gate rows, constrained by semantic_profile.",
              "required": false,
              "type": "string"
            },
            "kind": {
              "description": "Operation kind.",
              "enum": [
                "gate",
                "measure",
                "reset"
              ],
              "required": true,
              "type": "string"
            },
            "op_id": {
              "description": "Unique operation ID.",
              "required": true,
              "type": "string"
            },
            "parameters": {
              "description": "Typed exact gate parameters; empty for non-parameterized gates.",
              "items": {
                "properties": {
                  "inverse": {
                    "description": "Whether the exact phase is inverted.",
                    "required": false,
                    "type": "boolean"
                  },
                  "level": {
                    "description": "Cyclotomic phase level when applicable.",
                    "minimum": 0,
                    "required": false,
                    "type": "integer"
                  },
                  "parameter_type": {
                    "description": "Exact parameter family, such as cyclotomic_phase.",
                    "required": true,
                    "type": "string"
                  }
                },
                "type": "object"
              },
              "required": false,
              "type": "array"
            },
            "qubit": {
              "description": "Qubit ID for measure/reset rows.",
              "required": false,
              "type": "string"
            },
            "targets": {
              "description": "Target-qubit IDs for gate rows.",
              "items": {
                "type": "string"
              },
              "required": false,
              "type": "array"
            }
          },
          "type": "object"
        },
        "required": true,
        "type": "array"
      },
      "qubits": {
        "description": "Nonempty ordered qubit declarations.",
        "items": {
          "properties": {
            "id": {
              "description": "Unique qubit ID referenced by operations.",
              "required": true,
              "type": "string"
            }
          },
          "type": "object"
        },
        "minItems": 1,
        "required": true,
        "type": "array"
      },
      "schema": {
        "description": "Circuit artifact schema.",
        "enum": [
          "heyting.quantum_circuit_ir.v1"
        ],
        "required": true,
        "type": "string"
      },
      "semantic_profile": {
        "description": "Exact semantics under which operations are interpreted.",
        "enum": [
          "unsigned_binary_symplectic_clifford_v1",
          "signed_binary_symplectic_v2",
          "exact_clifford_t_v2",
          "exact_clifford_t_measurement_v1",
          "exact_cyclotomic_2k_v1",
          "exact_cyclotomic_24_v1"
        ],
        "required": true,
        "type": "string"
      }
    },
    "required": true,
    "type": "object"
  },
  "claims": {
    "description": "Optional heyting.quantum_claim_evidence.v1 ledger used only to enrich applicable visualizations. It is not certified by this action.",
    "properties": {
      "circuit_subject_sha256": {
        "description": "Expected canonical circuit subject digest.",
        "pattern": "^[0-9a-f]{64}$",
        "required": true,
        "type": "string"
      },
      "claims": {
        "description": "Nonempty claim obligations with claim_id, statement, accepted_evidence_tiers, and description.",
        "items": {
          "properties": {
            "accepted_evidence_tiers": {
              "description": "Evidence tiers allowed to discharge this claim.",
              "items": {
                "enum": [
                  "kernel_certified",
                  "checker_verified",
                  "simulator_crosscheck",
                  "provider_attested",
                  "reported"
                ],
                "type": "string"
              },
              "minItems": 1,
              "required": true,
              "type": "array"
            },
            "claim_id": {
              "description": "Stable claim identifier.",
              "required": true,
              "type": "string"
            },
            "description": {
              "description": "Human-readable bounded claim scope.",
              "required": true,
              "type": "string"
            },
            "statement": {
              "description": "Copy the complete typed statement from the dashboard or a matching corpus example without dropping nested fields. well_formed requires profile; circuit_property requires predicate, parameters, and relation.",
              "properties": {
                "claim_type": {
                  "description": "Exact claim family; preserve this value and its corresponding fields.",
                  "enum": [
                    "well_formed",
                    "normalization_equivalent",
                    "lowering_equivalent",
                    "circuit_property",
                    "resource_optimality",
                    "simulation_crosscheck",
                    "execution_attestation",
                    "visualization_correspondence"
                  ],
                  "required": true,
                  "type": "string"
                },
                "parameters": {
                  "description": "Required string map for circuit_property; preserve all supplied entries.",
                  "required": false,
                  "type": "object"
                },
                "predicate": {
                  "description": "Required for circuit_property; preserve namespace, name, and version exactly.",
                  "properties": {
                    "name": {
                      "description": "Predicate name.",
                      "required": true,
                      "type": "string"
                    },
                    "namespace": {
                      "description": "Predicate namespace.",
                      "required": true,
                      "type": "string"
                    },
                    "version": {
                      "description": "Predicate version.",
                      "required": true,
                      "type": "string"
                    }
                  },
                  "required": false,
                  "type": "object"
                },
                "profile": {
                  "description": "Required for well_formed; must match the circuit profile.",
                  "required": false,
                  "type": "string"
                },
                "relation": {
                  "description": "Required exact equivalence relation for claim families that use one.",
                  "required": false,
                  "type": "string"
                }
              },
              "required": true,
              "type": "object"
            }
          },
          "type": "object"
        },
        "minItems": 1,
        "required": true,
        "type": "array"
      },
      "ledger_id": {
        "description": "Stable ledger ID.",
        "required": true,
        "type": "string"
      },
      "schema": {
        "description": "Claim-ledger artifact schema.",
        "enum": [
          "heyting.quantum_claim_evidence.v1"
        ],
        "required": true,
        "type": "string"
      },
      "semantic_profile": {
        "description": "Profile matching the circuit.",
        "enum": [
          "unsigned_binary_symplectic_clifford_v1",
          "signed_binary_symplectic_v2",
          "exact_clifford_t_v2",
          "exact_clifford_t_measurement_v1",
          "exact_cyclotomic_2k_v1",
          "exact_cyclotomic_24_v1"
        ],
        "required": true,
        "type": "string"
      }
    },
    "required": false,
    "type": "object"
  },
  "image_format": {
    "description": "Optional stored image output. Set to png or jpeg to render the digest-bound logical wire_circuit projection, save it in budget-scoped File Manager, and return image_file metadata. The image is explanatory, not proof or hardware execution.",
    "enum": [
      "png",
      "jpeg"
    ],
    "required": false,
    "type": "string"
  },
  "include_visualizations": {
    "default": false,
    "description": "When true, return all applicable structured semantic visualization lenses after validation. Defaults to false. This is independent of image_format.",
    "required": false,
    "type": "boolean"
  }
}
```

## `instantiate_template`

Action slug: `instantiate-template`

Price: `2` credits

Use to create a normalized circuit from a supported GHZ, Bernstein-Vazirani, teleportation, Grover, or QFT template. This expands a template but does not certify it; pass the resulting circuit and claims to certify_circuit when proof is required. If the proof service is starting, the request is retained as a background task; poll free get_task and do not resubmit it.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `descriptor` | `object` | yes | Typed template choice. ghz requires qubits 2-4096; bernstein_vazirani requires a binary secret; teleportation has no extra field; grover requires qubits 2-4096 and marked_item less than 2^qubits; qft requires qubits 2-6. |

Sample parameters:

```json
{
  "descriptor": {
    "family": "ghz",
    "marked_item": 0,
    "qubits": 2,
    "secret": "example secret",
    "semantic_profile": "unsigned_binary_symplectic_clifford_v1"
  }
}
```

Generated JSON parameter schema:

```json
{
  "descriptor": {
    "description": "Typed template choice. ghz requires qubits 2-4096; bernstein_vazirani requires a binary secret; teleportation has no extra field; grover requires qubits 2-4096 and marked_item less than 2^qubits; qft requires qubits 2-6.",
    "properties": {
      "family": {
        "description": "Template family. Family-specific fields are validated strictly.",
        "enum": [
          "ghz",
          "bernstein_vazirani",
          "teleportation",
          "grover",
          "qft"
        ],
        "required": true,
        "type": "string"
      },
      "marked_item": {
        "description": "Required only for grover; little-endian basis index satisfying 0 <= marked_item < 2^qubits.",
        "minimum": 0,
        "required": false,
        "type": "integer"
      },
      "qubits": {
        "description": "Required for ghz, grover, and qft. QFT is limited to 6; other applicable families allow up to 4096.",
        "maximum": 4096,
        "minimum": 2,
        "required": false,
        "type": "integer"
      },
      "secret": {
        "description": "Required only for bernstein_vazirani; a nonempty bit string containing only 0 and 1.",
        "maxLength": 4096,
        "minLength": 1,
        "required": false,
        "type": "string"
      },
      "semantic_profile": {
        "description": "Exact semantics for the expanded circuit; choose a profile compatible with the selected family.",
        "enum": [
          "unsigned_binary_symplectic_clifford_v1",
          "signed_binary_symplectic_v2",
          "exact_clifford_t_v2",
          "exact_clifford_t_measurement_v1",
          "exact_cyclotomic_2k_v1",
          "exact_cyclotomic_24_v1"
        ],
        "required": true,
        "type": "string"
      }
    },
    "required": true,
    "type": "object"
  }
}
```

## `search_corpus_examples`

Action slug: `search-corpus-examples`

Price: `1` credits

Use to find worked proof chains, template inputs, provider-intake samples, or designer samples in the bundled corpus. With no query, returns a bounded index. Results contain exact relative paths accepted by get_corpus_example. If the proof service is starting, the request is retained as a background task; poll free get_task and do not resubmit it.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | `string` | no | Optional space-separated terms matched case-insensitively against stable example IDs, kinds, and asset paths. |
| `result_count` | `integer` | no | Maximum matching summaries. Defaults to 8. |

Sample parameters:

```json
{
  "query": "example search query",
  "result_count": 8
}
```

Generated JSON parameter schema:

```json
{
  "query": {
    "description": "Optional space-separated terms matched case-insensitively against stable example IDs, kinds, and asset paths.",
    "maxLength": 4000,
    "minLength": 1,
    "required": false,
    "type": "string"
  },
  "result_count": {
    "default": 8,
    "description": "Maximum matching summaries. Defaults to 8.",
    "maximum": 50,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `search_knowledge`

Action slug: `search-knowledge`

Price: `2` credits

Use when the agent needs conceptual, research, architecture, or repository context before acting. Do not call as a mandatory preflight. Returns ranked results with source provenance; use get_document for the selected full record. If the proof service is starting, the request is retained as a background task; poll free get_task and do not resubmit it.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | `string` | yes | Natural-language question, concept, quotation fragment, or repository term to find. Maximum 4000 characters. |
| `result_count` | `integer` | no | Maximum ranked results. Defaults to 8. |
| `search_mode` | `string` | no | hybrid combines semantic and keyword matching; semantic favors meaning; keyword favors exact terms. Defaults to hybrid. |

Sample parameters:

```json
{
  "query": "example search query",
  "result_count": 8,
  "search_mode": "hybrid"
}
```

Generated JSON parameter schema:

```json
{
  "query": {
    "description": "Natural-language question, concept, quotation fragment, or repository term to find. Maximum 4000 characters.",
    "maxLength": 4000,
    "minLength": 1,
    "required": true,
    "type": "string"
  },
  "result_count": {
    "default": 8,
    "description": "Maximum ranked results. Defaults to 8.",
    "maximum": 50,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "search_mode": {
    "default": "hybrid",
    "description": "hybrid combines semantic and keyword matching; semantic favors meaning; keyword favors exact terms. Defaults to hybrid.",
    "enum": [
      "hybrid",
      "semantic",
      "keyword"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `search_lean`

Action slug: `search-lean`

Price: `2` credits

Use after starting from a worked CircuitSpec corpus example when the agent needs a Lean declaration, theorem, namespace, signature, or authoring primitive. authoring_only restricts results to the four modules admitted by submitted specs; false browses the wider reference corpus. If the proof service is starting, the request is retained as a background task; poll free get_task and do not resubmit it.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `authoring_only` | `boolean` | no | When true, prefilter declarations to CircuitSpec, Qasm3Subset, Edifice.ProductionPurePipeline, and Edifice.ProductionEffectfulPipeline before ranking. Use true when writing submitted Lean; false browses the full reference catalog. |
| `query` | `string` | yes | Lean concept, identifier, theorem name, namespace, or signature fragment. Maximum 4000 characters. |
| `result_count` | `integer` | no | Maximum ranked results. Defaults to 8. |

Sample parameters:

```json
{
  "authoring_only": false,
  "query": "example search query",
  "result_count": 8
}
```

Generated JSON parameter schema:

```json
{
  "authoring_only": {
    "default": false,
    "description": "When true, prefilter declarations to CircuitSpec, Qasm3Subset, Edifice.ProductionPurePipeline, and Edifice.ProductionEffectfulPipeline before ranking. Use true when writing submitted Lean; false browses the full reference catalog.",
    "required": false,
    "type": "boolean"
  },
  "query": {
    "description": "Lean concept, identifier, theorem name, namespace, or signature fragment. Maximum 4000 characters.",
    "maxLength": 4000,
    "minLength": 1,
    "required": true,
    "type": "string"
  },
  "result_count": {
    "default": 8,
    "description": "Maximum ranked results. Defaults to 8.",
    "maximum": 50,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `verify_certificate`

Action slug: `verify-certificate`

Price: `10` credits

Use at a trust boundary to independently replay a qpcert received from another party against separately supplied circuit and claims. The request is accepted as a background task even while the proof service starts; poll free get_task and do not resubmit it. Do not automatically re-verify a qpcert just produced by certify_circuit or certify_from_lean, because those actions already verify their generated certificate.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `certificate_file_id` | `string` | yes | Budget-visible File Manager ID containing an application/vnd.heyting.qpcert+json certificate. Upload an external qpcert to File Manager first. |
| `circuit` | `object` | yes | Complete independently supplied heyting.quantum_circuit_ir.v1 object expected to be bound by the certificate. |
| `claims` | `object` | yes | Complete independently supplied heyting.quantum_claim_evidence.v1 ledger expected to be bound by the certificate. Preserve every nested statement field exactly. |

Sample parameters:

```json
{
  "certificate_file_id": "example certificate file id",
  "circuit": {
    "circuit_id": "example circuit id",
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
```

Generated JSON parameter schema:

```json
{
  "certificate_file_id": {
    "description": "Budget-visible File Manager ID containing an application/vnd.heyting.qpcert+json certificate. Upload an external qpcert to File Manager first.",
    "maxLength": 200,
    "minLength": 1,
    "required": true,
    "type": "string"
  },
  "circuit": {
    "description": "Complete independently supplied heyting.quantum_circuit_ir.v1 object expected to be bound by the certificate.",
    "properties": {
      "circuit_id": {
        "description": "Stable circuit ID.",
        "required": true,
        "type": "string"
      },
      "operations": {
        "description": "Ordered canonical operations.",
        "items": {
          "properties": {
            "kind": {
              "description": "Operation kind.",
              "enum": [
                "gate",
                "measure",
                "reset"
              ],
              "required": true,
              "type": "string"
            },
            "op_id": {
              "description": "Unique operation ID.",
              "required": true,
              "type": "string"
            }
          },
          "type": "object"
        },
        "required": true,
        "type": "array"
      },
      "qubits": {
        "description": "Nonempty qubit declarations.",
        "items": {
          "properties": {
            "id": {
              "description": "Unique qubit ID.",
              "required": true,
              "type": "string"
            }
          },
          "type": "object"
        },
        "minItems": 1,
        "required": true,
        "type": "array"
      },
      "schema": {
        "description": "Circuit artifact schema.",
        "enum": [
          "heyting.quantum_circuit_ir.v1"
        ],
        "required": true,
        "type": "string"
      },
      "semantic_profile": {
        "description": "Exact circuit semantics.",
        "enum": [
          "unsigned_binary_symplectic_clifford_v1",
          "signed_binary_symplectic_v2",
          "exact_clifford_t_v2",
          "exact_clifford_t_measurement_v1",
          "exact_cyclotomic_2k_v1",
          "exact_cyclotomic_24_v1"
        ],
        "required": true,
        "type": "string"
      }
    },
    "required": true,
    "type": "object"
  },
  "claims": {
    "description": "Complete independently supplied heyting.quantum_claim_evidence.v1 ledger expected to be bound by the certificate. Preserve every nested statement field exactly.",
    "properties": {
      "circuit_subject_sha256": {
        "description": "Expected circuit subject digest.",
        "pattern": "^[0-9a-f]{64}$",
        "required": true,
        "type": "string"
      },
      "claims": {
        "description": "Exact claims expected to be certified.",
        "items": {
          "properties": {
            "accepted_evidence_tiers": {
              "description": "Allowed evidence tiers.",
              "items": {
                "enum": [
                  "kernel_certified",
                  "checker_verified",
                  "simulator_crosscheck",
                  "provider_attested",
                  "reported"
                ],
                "type": "string"
              },
              "minItems": 1,
              "required": true,
              "type": "array"
            },
            "claim_id": {
              "description": "Stable claim ID.",
              "required": true,
              "type": "string"
            },
            "description": {
              "description": "Bounded claim scope.",
              "required": true,
              "type": "string"
            },
            "statement": {
              "description": "Copy the complete typed statement. well_formed requires profile; circuit_property requires predicate, parameters, and relation.",
              "properties": {
                "claim_type": {
                  "description": "Exact claim family; preserve this value and its corresponding fields.",
                  "enum": [
                    "well_formed",
                    "normalization_equivalent",
                    "lowering_equivalent",
                    "circuit_property",
                    "resource_optimality",
                    "simulation_crosscheck",
                    "execution_attestation",
                    "visualization_correspondence"
                  ],
                  "required": true,
                  "type": "string"
                },
                "parameters": {
                  "description": "Required string map for circuit_property; preserve all supplied entries.",
                  "required": false,
                  "type": "object"
                },
                "predicate": {
                  "description": "Required for circuit_property; preserve namespace, name, and version exactly.",
                  "properties": {
                    "name": {
                      "description": "Predicate name.",
                      "required": true,
                      "type": "string"
                    },
                    "namespace": {
                      "description": "Predicate namespace.",
                      "required": true,
                      "type": "string"
                    },
                    "version": {
                      "description": "Predicate version.",
                      "required": true,
                      "type": "string"
                    }
                  },
                  "required": false,
                  "type": "object"
                },
                "profile": {
                  "description": "Required for well_formed; must match the circuit profile.",
                  "required": false,
                  "type": "string"
                },
                "relation": {
                  "description": "Required exact equivalence relation for claim families that use one.",
                  "required": false,
                  "type": "string"
                }
              },
              "required": true,
              "type": "object"
            }
          },
          "type": "object"
        },
        "minItems": 1,
        "required": true,
        "type": "array"
      },
      "ledger_id": {
        "description": "Stable ledger ID.",
        "required": true,
        "type": "string"
      },
      "schema": {
        "description": "Claim-ledger artifact schema.",
        "enum": [
          "heyting.quantum_claim_evidence.v1"
        ],
        "required": true,
        "type": "string"
      },
      "semantic_profile": {
        "description": "Must match the circuit and certificate.",
        "enum": [
          "unsigned_binary_symplectic_clifford_v1",
          "signed_binary_symplectic_v2",
          "exact_clifford_t_v2",
          "exact_clifford_t_measurement_v1",
          "exact_cyclotomic_2k_v1",
          "exact_cyclotomic_24_v1"
        ],
        "required": true,
        "type": "string"
      }
    },
    "required": true,
    "type": "object"
  }
}
```
