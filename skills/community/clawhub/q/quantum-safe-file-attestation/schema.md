# Quantum-Safe File Attestation Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `quantum-safe-file-attestation`

x402 availability: not enabled for this product.

## `attest_artifact`

Action slug: `attest-artifact`

Price: `25` credits

Create a post-quantum cryptographic attestation for a file in storage. Signs with ML-DSA-65 via hardware security module. Saves the attestation package to file storage and returns its file_id.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `artifact_name` | `string` | no | Human-readable name for the artifact being attested. Defaults to the stored filename. |
| `file_id` | `string` | yes | File ID from file storage (from upload or GitHub download). |
| `metadata` | `object` | no | Optional freeform metadata to include in the attestation manifest. |

Sample parameters:

```json
{
  "artifact_name": "example artifact name",
  "file_id": "example file id",
  "metadata": {}
}
```

Generated JSON parameter schema:

```json
{
  "artifact_name": {
    "description": "Human-readable name for the artifact being attested. Defaults to the stored filename.",
    "required": false,
    "type": "string"
  },
  "file_id": {
    "description": "File ID from file storage (from upload or GitHub download).",
    "required": true,
    "type": "string"
  },
  "metadata": {
    "description": "Optional freeform metadata to include in the attestation manifest.",
    "required": false,
    "type": "object"
  }
}
```

## `get_public_key`

Action slug: `get-public-key`

Price: `5` credits

Return the signer's public key, algorithm, and fingerprint so independent verifiers can confirm attestation signatures without calling this tool.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `verify_attestation`

Action slug: `verify-attestation`

Price: `5` credits

Verify a previously issued attestation package against the original artifact. Both the artifact and the attestation package must be in file storage. Checks ML-DSA-65 signature, manifest integrity, artifact SHA-256 match, and CAB bundle.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `attestation_file_id` | `string` | yes | File ID of the attestation package JSON (returned as attestation_file_id by attest_artifact). |
| `check_bundle` | `boolean` | no | Whether to also verify the CAB verifier bundle material. Defaults to true. |
| `file_id` | `string` | yes | File ID of the original artifact to verify. |

Sample parameters:

```json
{
  "attestation_file_id": "example attestation file id",
  "check_bundle": true,
  "file_id": "example file id"
}
```

Generated JSON parameter schema:

```json
{
  "attestation_file_id": {
    "description": "File ID of the attestation package JSON (returned as attestation_file_id by attest_artifact).",
    "required": true,
    "type": "string"
  },
  "check_bundle": {
    "description": "Whether to also verify the CAB verifier bundle material. Defaults to true.",
    "required": false,
    "type": "boolean"
  },
  "file_id": {
    "description": "File ID of the original artifact to verify.",
    "required": true,
    "type": "string"
  }
}
```
