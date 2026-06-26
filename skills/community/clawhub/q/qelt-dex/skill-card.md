## Description: <br>
Interact with Uniswap v4 pools and liquidity positions on QELT Mainnet, including pool queries, WQELT wrapping and unwrapping, token swaps, liquidity provision, position NFTs, and Uniswap v4 contract addresses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PRQELT](https://clawhub.ai/user/PRQELT) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agents use this skill to inspect QELT Mainnet Uniswap v4 pools, retrieve verified contract addresses, prepare DEX transactions, and broadcast raw transactions that the user has already signed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A swap, wrap, unwrap, or liquidity transaction may be irreversible or may execute with unintended parameters. <br>
Mitigation: Confirm slippage, deadlines, token addresses, amounts, and the signed transaction payload before broadcasting. <br>
Risk: Private key disclosure would compromise funds. <br>
Mitigation: Do not provide private keys; use only pre-signed raw transactions for write operations. <br>
Risk: Using Uniswap v2 or v3 paths on QELT will fail because this deployment supports only Uniswap v4. <br>
Mitigation: Use the documented v4 PoolManager, UniversalRouter, PositionManager, Permit2, and WQELT addresses. <br>


## Reference(s): <br>
- [QELT DEX on ClawHub](https://clawhub.ai/PRQELT/qelt-dex) <br>
- [QELTScan](https://qeltscan.ai) <br>
- [Uniswap v4 Contract Addresses - QELT Mainnet](artifact/references/contracts.md) <br>
- [Uniswap v4 SDK Examples - QELT Mainnet](artifact/references/sdk-examples.md) <br>
- [PoolManager on QELTScan](https://qeltscan.ai/address/0x11c23891d9f723c4f1c6560f892e4581d87b6d8a) <br>
- [UniversalRouter on QELTScan](https://qeltscan.ai/address/0x7d5AbaDb17733963a3e14cF8fB256Ee08df9d68A) <br>
- [PositionManager on QELTScan](https://qeltscan.ai/address/0x1809116b4230794c823b1b17d46c74076e90d035) <br>
- [Permit2 on QELTScan](https://qeltscan.ai/address/0x403cf2852cf448b5de36e865c5736a7fb7b25ea2) <br>
- [WQELT on QELTScan](https://qeltscan.ai/address/0xfebc6f9f0149036006c4f5ac124685e0ef48e8a2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown with inline bash and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-RPC request payloads and contract address tables.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
