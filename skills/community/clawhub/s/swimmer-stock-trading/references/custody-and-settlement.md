# Custody, settlement, and counterparty risk

The signer sends the offered SPL tokens to this fixed recipient:

```text
CdnwmDJhaokY6r5W9EpFGvxnf4xDcAfe2XPHqCvfR2cf
```

The packaged protocol asserts that this is the Swimmer Solana custodial recipient, but the package cannot cryptographically prove its operator or future validity. Before configuring or funding the wallet, the user must independently compare the full address with a current official publication reached from [swimmer.finance](https://swimmer.finance). Do not rely only on this skill, an agent message, route API output, or a shortened address.

The transaction is a one-way, irreversible token transfer with an order memo. It is not an atomic program swap and provides no on-chain escrow or minimum-receive enforcement. A successful signature or confirmation does not prove that the requested stock token or USDC was delivered.

Before signing, independently review current official terms covering custody, execution, market-order pricing, limit-order behavior, settlement timing, failed orders, cancellations, refunds, fees, token redemption, jurisdiction, and support. If those terms are unavailable, unclear, or unacceptable, stop without transferring funds. This package does not invent or guarantee operator policies.

An unquoted MARKET request uses memo request `0`. That provides no on-chain minimum receive, so the execution quantity is unknown at authorization time. An optional API quote is only an estimate and still creates no on-chain guarantee. A LIMIT memo states an offer/request ratio, but the transfer itself cannot force the custodian to execute or refund it.

After submission, retain the signature and confirmation digest. Verify on-chain confirmation and the operator’s order/settlement status separately. If status is uncertain, do not send another transaction automatically.
