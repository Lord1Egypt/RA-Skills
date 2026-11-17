## Description:

Helps developers update Sentio SDK 4 Sui processors that inspect raw transactions, objects, events, or Move type strings so they use Sui gRPC protobuf data shapes instead of older JSON-RPC shapes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philz3906](https://clawhub.ai/user/philz3906)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when writing or upgrading Sentio SDK 4 Sui processors that inspect raw transactions, events, objects, or Move type strings. It helps adapt code from older JSON-RPC shapes to Sui gRPC protobuf shapes while avoiding brittle type-string parsing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Protocol schema guidance can become stale after Sentio SDK or Sui RPC v2 protobuf changes.

Mitigation: Re-check field names and shapes against the current Sui RPC v2 protobufs before applying the guidance after an SDK or API upgrade.

Risk: Incorrect raw type-string parsing can cause processors to misclassify Sui Move types or addresses.

Mitigation: Use structural generic parsing and address normalization rather than whitespace-dependent splitting or manual leading-zero stripping.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/philz3906/skills/sui-grpc-data-format)
- [Sentio Sui RPC v2 protobufs](https://github.com/sentioxyz/sui-apis/tree/main/proto/sui/rpc/v2)
- [MystenLabs sui-apis upstream](https://github.com/MystenLabs/sui-apis)
- [Move language_storage.rs](https://github.com/MystenLabs/sui/blob/main/external-crates/move/crates/move-core-types/src/language_storage.rs)
- [Sui sui_serde.rs](https://github.com/MystenLabs/sui/blob/main/crates/sui-types/src/sui_serde.rs)
- [Sui gRPC v2 render.rs](https://github.com/MystenLabs/sui/blob/main/crates/sui-rpc-api/src/grpc/v2/render.rs)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance with TypeScript snippets and checklist items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no hidden execution or privilege behavior found in security evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
