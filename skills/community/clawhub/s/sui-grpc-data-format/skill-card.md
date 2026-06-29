## Description: <br>
Helps developers update Sentio SDK 4 Sui processors that read raw transaction, object, event, or Move type structures by explaining the gRPC protobuf shapes that differ from older JSON-RPC formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[philz3906](https://clawhub.ai/user/philz3906) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when writing or upgrading Sentio Sui processors on SDK 4, especially when adapting raw chain-data access from JSON-RPC shapes to gRPC protobuf shapes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sui gRPC protobuf fields can change after SDK or upstream schema updates. <br>
Mitigation: Verify the current Sui RPC v2 protobuf schema before applying the guidance after an SDK upgrade. <br>
Risk: Old JSON-RPC assumptions for raw Move type strings can produce incorrect parsing or address comparisons. <br>
Mitigation: Use structural type parsing and explicit Sui address normalization, then review processor changes before deployment. <br>


## Reference(s): <br>
- [Sentio Sui RPC v2 protobufs](https://github.com/sentioxyz/sui-apis/tree/main/proto/sui/rpc/v2) <br>
- [MystenLabs sui-apis](https://github.com/MystenLabs/sui-apis) <br>
- [Move language_storage.rs](https://github.com/MystenLabs/sui/blob/main/external-crates/move/crates/move-core-types/src/language_storage.rs) <br>
- [Sui sui_serde.rs](https://github.com/MystenLabs/sui/blob/main/crates/sui-types/src/sui_serde.rs) <br>
- [Sui gRPC v2 render.rs](https://github.com/MystenLabs/sui/blob/main/crates/sui-rpc-api/src/grpc/v2/render.rs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown guidance with TypeScript code snippets and reference links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no automatic execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
