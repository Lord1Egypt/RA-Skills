---
name: quantum-safe-file-attestation
description: "Quantum-Safe File Attestation: Issue and verify formally verified. Use when an agent needs quantum safe file attestation, sign software releases with formally verified post quantum cryptography, create proof carrying attestation certificates with lean 4 verified acceptance kernels, verify file integrity with nist standardized ml dsa 65 digital signatures and pqclean runtimes, generate compliance evidence for soc 2 sox hipaa and regulatory audits with cryptographic proof chains, attest."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/quantum-safe-file-attestation
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/quantum-safe-file-attestation"}}
---
# Quantum-Safe File Attestation

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Issue formally verified, post-quantum cryptographic attestation certificates for any file. Every attestation is backed by a proof-carrying certificate bundle whose acceptance logic is proven correct in Lean 4. Signing uses ML-DSA-65 from the NIST post-quantum standard, executed through PQClean standardized runtimes with the private key secured in a hardware security module. A 4-check verification pipeline confirms signature validity, manifest consistency, artifact integrity, and certificate Merkle-tree integrity — all must pass. Anyone can verify certificates independently using the open-source offline verifier. No trust in our infrastructure required.

## Product Instructions
### Quantum-Safe File Attestation

Create and verify post-quantum cryptographic attestation packages for files using ML-DSA-65 (Dilithium3).

#### Actions

##### `attest_artifact`
Create a cryptographic attestation for a file in storage. The attestation package is saved to file storage.

Required:
- `file_id` (string): file ID of the artifact to attest. Upload the file first using the File Management tool (action `upload_standard`), then pass the returned `file_id` here.

Optional:
- `artifact_name` (string): human-readable name (defaults to stored filename)
- `metadata` (object): freeform key-value pairs to include in the manifest

```json
{"action":"attest_artifact","file_id":"abc-123","artifact_name":"release-v2.1.tar.gz","metadata":{"version":"2.1.0"}}
```

Response:
- `artifact_sha256`: SHA-256 of the attested file
- `package_id`: unique attestation identifier
- `attestation_file_id`: file ID of the saved attestation package (use this for verify_attestation)
- `attestation_signed_url`: download URL for the attestation package JSON

##### `verify_attestation`
Verify a previously issued attestation package against the original artifact. Both must be in file storage. If verifying a package received from someone else, upload it first using the File Management tool.

Required:
- `file_id` (string): file ID of the original artifact
- `attestation_file_id` (string): file ID of the attestation package JSON (from attest_artifact, or uploaded via File Management)

Optional:
- `check_bundle` (boolean, default true): verify CAB certificate bundle integrity

```json
{"action":"verify_attestation","file_id":"abc-123","attestation_file_id":"def-456"}
```

Response:
- `accept`: true if all checks pass
- `failed_checks`: list of check names that failed (empty when accepted)
- `manifest_sha256`: hash of the canonical manifest
- `signer_public_key_hex`: the public key that signed the manifest

##### `get_public_key`
Return the signer's public key and algorithm info for independent verification.

```json
{"action":"get_public_key"}
```

#### Typical Workflow

1. Upload a file using the File Management tool (`upload_standard`) to get a `file_id`
2. Call `attest_artifact` with the `file_id` — save the returned `attestation_file_id`
3. To verify later, call `verify_attestation` with both `file_id` (original artifact) and `attestation_file_id` (the attestation package)
4. Share the attestation package (downloadable via `attestation_signed_url`) with anyone who needs to verify independently

#### Independent Offline Verification

Recipients can verify attestation packages offline without this tool: https://github.com/Abraxas1010/verified-pqc-verifier

#### Security Properties

- **Post-quantum security**: ML-DSA-65 (FIPS 204 / Dilithium3) resistant to quantum attacks
- **Hardware key protection**: signing key never leaves the hardware security module
- **Tamper evidence**: any modification invalidates the signature
- **Self-verification**: every attestation is verified immediately after signing

## When To Use
- Use this skill for `Quantum-Safe File Attestation` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: quantum safe file attestation, sign software releases with formally verified post quantum cryptography, create proof carrying attestation certificates with lean 4 verified acceptance kernels, verify file integrity with nist standardized ml dsa 65 digital signatures and pqclean runtimes, generate compliance evidence for soc 2 sox hipaa and regulatory audits with cryptographic proof chains, attest artifact, file id, artifact name.
- Supported action names: `attest_artifact`, `get_public_key`, `verify_attestation`.

## Use Cases
- Sign software releases with formally verified post-quantum cryptography
- Create proof-carrying attestation certificates with Lean 4 verified acceptance kernels
- Verify file integrity with NIST-standardized ML-DSA-65 digital signatures and PQClean runtimes
- Generate compliance evidence for SOC 2 SOX HIPAA and regulatory audits with cryptographic proof chains
- Timestamp and cryptographically attest intellectual property artifacts with tamper-evident CAB bundles
- Verify software supply chain integrity with 4-check verification pipeline
- Issue verifiable certificates for code repositories and release archives backed by formal proofs
- Provide independent verification keys for third-party auditors and partners
- Create provenance records for AI model weights and training data with quantum-safe signatures
- Attest firmware images and embedded software updates with hardware-backed signing
- Notarize documents with post-quantum signatures backed by information-theoretic security foundations
- Sign configuration files and infrastructure-as-code with formally verified cryptographic protocol stack

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `3`.
x402 availability: not enabled for this product.

- `attest_artifact` (action slug: `attest-artifact`): Create a post-quantum cryptographic attestation for a file in storage. Signs with ML-DSA-65 via hardware security module. Saves the attestation package to file storage and returns its file_id. Price: `25` credits. Parameters: `artifact_name`, `file_id`, `metadata`.
- `get_public_key` (action slug: `get-public-key`): Return the signer's public key, algorithm, and fingerprint so independent verifiers can confirm attestation signatures without calling this tool. Price: `5` credits. Parameters: none.
- `verify_attestation` (action slug: `verify-attestation`): Verify a previously issued attestation package against the original artifact. Both the artifact and the attestation package must be in file storage. Checks ML-DSA-65 signature, manifest integrity, artifact SHA-256 match, and CAB bundle. Price: `5` credits. Parameters: `attestation_file_id`, `check_bundle`, `file_id`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "quantum-safe-file-attestation"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "quantum-safe-file-attestation"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "quantum-safe-file-attestation"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "quantum-safe-file-attestation"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "quantum-safe-file-attestation"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "quantum-safe-file-attestation"
  }
}
```

## Call This Tool
Product slug: `quantum-safe-file-attestation`

Marketplace page: https://www.agentpmt.com/marketplace/quantum-safe-file-attestation

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
    "name": "Quantum-Safe-File-Attestation",
    "arguments": {
      "action": "attest_artifact",
      "artifact_name": "example artifact name",
      "file_id": "example file id",
      "metadata": {}
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "quantum-safe-file-attestation",
  "parameters": {
    "action": "attest_artifact",
    "artifact_name": "example artifact name",
    "file_id": "example file id",
    "metadata": {}
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `attest_artifact` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/quantum-safe-file-attestation
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
