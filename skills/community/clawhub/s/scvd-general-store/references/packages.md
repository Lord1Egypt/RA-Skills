# Choose a package only when the task needs one

| Task | Existing option |
| --- | --- |
| Application or offline verification of x402 signed offers/receipts | `x402-verify`; inspect its installed README, exports and support matrix |
| Issue signed offers/receipts as the merchant | `x402-sign`; issuer key handling remains with the user's own application |
| Command-line endpoint inspection | `scvd-cli`; check installed help for supported commands and output |
| Application endpoint inspection | `scvd-preflight`; check installed exports for `inspectOne` |
| Local account of tools, trials and renewals | `scvd-tab`; local MCP server, with explicit consent before sending a contribution |
| One-off check in a connected host | Existing read-only MCP/browser tool, or the free HTTPS desk; no package installation required |

Install only what the user's environment and task require. Follow the selected
version's documentation rather than guessing an export or translating a hosted
request body into a library call. No package is required just to browse history.

For protocol-aware inspection, use `scvd inspect <url>` only when the installed
help lists it, or `inspectOne` when the installed `scvd-preflight` exports it.
Both preserve the hosted report and its inspection gaps. Inspection exit 0
means a response was inspected, including an MPP-only or partial response;
it does not mean ready or safe to pay. `scvd preflight` and the preflight Action
retain their x402 deploy-gate meaning and existing exits. If the inspection
entry point is unavailable, use the free hosted tool or HTTP desk and report
its actual capabilities. A prepared source version is not proof of registry
publication or of what is installed locally.

For structured result statuses, follow the installed verifier's documented
contract and supported algorithms. This skill introduces no support for new
signature algorithms and makes no browser/Node/Workers parity promise.

For store-issued evidence bundles, `x402-verify` includes the `scvd-evidence`
command. Use its installed help and trusted key input; preserve the distinction
between bundle integrity, certificate signature, observation freshness and
what the underlying observations did not establish. For new artifacts,
keep user-controlled signing keys inside the user's own signer, never in a
request to the store or a chat message.
