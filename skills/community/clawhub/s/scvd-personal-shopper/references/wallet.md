# A compatible wallet

Prefer a wallet the user already trusts and has authorized. Check the actual
client against the fresh SCVD quote before requesting any funding. Chain names
alone do not establish compatibility: version, signing scheme, asset and
signing domain must agree too.

## A concrete Base option

Coinbase publishes [Agentic Wallet skills](https://github.com/coinbase/agentic-wallet-skills)
and an [x402 payment guide](https://docs.cdp.coinbase.com/agentic-wallet/cli/skills/pay-for-service).
Use these official sources for the current installation, authentication and
funding flow. This is a candidate integration, not a claim that every personal
agent host has been tested with it.

After the user chooses this provider and authorizes setup, a host supporting
Node and the Skills CLI can install its wallet instructions with:

```sh
npx skills add coinbase/agentic-wallet-skills
```

Read the installed instructions and use their supported CLI version. Check
wallet status and balance without printing credentials. Let the user complete
provider authentication and any payment-method entry in its secure interface.
If that interface is unavailable, stop at a clear handoff rather than asking
the user to paste secrets into chat.

For funding, state the wallet address, exact network, proposed deposit and
provider fees/minimums. Let the user approve and complete the provider flow,
then verify the balance. Do not assume the wallet needs funding just because
it is new to this conversation. Do not promise that a tiny item can be funded
with an equally tiny deposit; onramp minimums may dominate the purchase.

The documented payment command is `awal x402 pay`, with `--max-amount` in USDC
atomic units and `-h` accepting JSON headers. Use the approved quote amount
for the ceiling and pass the preserved `Idempotency-Key` through those headers.
Use the provider's current version and syntax, pass arguments safely, and do
not call this command to obtain a free quote: it can automatically pay.
Check that the client can preserve the selected network and all approved terms;
if it cannot, use a compatible client or stop before signing.

## AIsa and Circle Gateway

[AIsa's published skill](https://github.com/AIsa-team/nanopayment-x402/blob/main/SKILL.md)
describes a Gateway-specific signing domain. A balance deposited in Gateway
is not automatically a directly spendable SCVD x402 balance. Do not deposit,
bridge, withdraw or change the store's accepted networks just to make this
skill work. Those are separate operations requiring verified compatibility,
fees and user authorization. Start with a wallet/client that already supports
an offered SCVD payment row.
