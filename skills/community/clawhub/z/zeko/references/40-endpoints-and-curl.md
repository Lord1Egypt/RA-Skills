# Endpoints And Curl

Use this file when you need exact public endpoints, Bridge SDK config values, or directly runnable queries.

## Common agent use

- If the user asks which endpoints to pass to the Zeko Bridge SDK or `Bridge.init`, start here.
- If the user asks for a query they can run right now with `curl`, start here.
- If the user asks to actually execute a bridge end to end, do not reconstruct the full protocol with raw `curl`; use the Bridge CLI or SDK instead.

## Testnet defaults

- Zeko GraphQL: `https://testnet.zeko.io/graphql`
- Zeko archive: `https://archive.testnet.zeko.io/graphql`
- Mina gateway (devnet): `https://gateway.mina.devnet.zeko.io`
- Mina gateway (mainnet): `https://gateway.mina.mainnet.zeko.io`
- Mina archive gateway (devnet): `https://gateway.mina.archive.devnet.zeko.io`
- Mina archive gateway (mainnet): `https://gateway.mina.archive.mainnet.zeko.io`
- Actions API: `https://testnet.api.actions.zeko.io/graphql`
- Faucet claim API: `https://api.faucet.zeko.io/claim`
- Bridge UI: `https://testnet.bridge.zeko.io` (`https://alpha.bridge.zeko.io` is an alias)
- Faucet UI: `https://faucet.zeko.io`
- Explorer: `https://zekoscan.io/testnet`

## Mainnet endpoints

- Zeko GraphQL: `https://mainnet.zeko.io/graphql`
- Zeko archive: `https://archive.mainnet.zeko.io/graphql`
- Mina GraphQL: `https://gateway.mina.mainnet.zeko.io`
- Mina archive: `https://gateway.mina.archive.mainnet.zeko.io`
- Actions API: `https://api.actions.zeko.io/graphql`
- Bridge UI: `https://bridge.zeko.io`

## Non-testnet note

- This skill defaults to public testnet values because those are the stable public builder defaults.
- If the user needs a browser wallet or custom network config for another network, start with `https://docs.zeko.io/developers/guides/custom-network`.

## Native MINA transfer rule

- Use `sendPayment` for native MINA transfers.
- This path is for native MINA only. Arbitrary zkApp tokens need token-specific flows instead.
- GraphQL expects `UInt64` base units, not human MINA strings.
- `1 MINA = 1_000_000_000` base units.

## Shell helper: convert human MINA to base units

```bash
to_nanomina() {
  node -e 'const [value] = process.argv.slice(1); const [whole, frac = ""] = value.split("."); const nanos = BigInt(whole) * 1000000000n + BigInt((frac + "000000000").slice(0, 9)); console.log(nanos.toString())' "$1"
}
```

## Example: send 1.25 MINA from X to Y

```bash
FROM="B62qSenderAddress"
TO="B62qRecipientAddress"
AMOUNT_MINA="1.25"
FEE_MINA="0.10"

AMOUNT_NANOMINA="$(to_nanomina "$AMOUNT_MINA")"
FEE_NANOMINA="$(to_nanomina "$FEE_MINA")"

echo "$AMOUNT_NANOMINA"  # 1250000000
echo "$FEE_NANOMINA"     # 100000000
```

## Curl: inspect the sender nonce before signing

```bash
curl -sS https://testnet.zeko.io/graphql \
  -H 'content-type: application/json' \
  --data '{"query":"query SenderNonce($pk: PublicKey!) { account(publicKey: $pk) { nonce inferredNonce } }","variables":{"pk":"B62qSenderAddress"}}'
```

## Curl: broadcast a signed native MINA payment

```bash
curl -sS https://testnet.zeko.io/graphql \
  -H 'content-type: application/json' \
  --data '{"query":"mutation SendPayment($input: SendPaymentInput!, $signature: SignatureInput) { sendPayment(input: $input, signature: $signature) { payment { hash amount fee from to nonce } } }","variables":{"input":{"from":"B62qSenderAddress","to":"B62qRecipientAddress","amount":"1250000000","fee":"100000000"},"signature":{"rawSignature":"<signed-payment-signature>"}}}'
```

## Signing note

- On public endpoints, assume you need to provide a valid signature.
- Generate the signature from the same transaction fields you pass in `input`, typically with a wallet or `o1js`, then submit the signed payload with `curl`.

## Curl: inspect the sequencer public key

```bash
curl -sS https://testnet.zeko.io/graphql \
  -H 'content-type: application/json' \
  --data '{"query":"query SequencerPK { sequencerPk }"}'
```

## Curl: inspect live bridge and circuit config

```bash
curl -sS https://testnet.zeko.io/graphql \
  -H 'content-type: application/json' \
  --data '{"query":"query FetchConfig { circuitsConfig { zekoL1 zekoL2 holderAccountsL1 holderAccountL2 chainL1 chainL2 withdrawalDelay } }"}'
```

## Curl: inspect Mina runtime config through the gateway

```bash
curl -sS https://gateway.mina.devnet.zeko.io \
  -H 'content-type: application/json' \
  --data '{"query":"query RuntimeConfig { runtimeConfig }"}'
```

## Curl: inspect a Mina account through the gateway

```bash
curl -sS https://gateway.mina.devnet.zeko.io \
  -H 'content-type: application/json' \
  --data '{"query":"query Account($pk: PublicKey!) { account(publicKey: $pk) { zkappState } }","variables":{"pk":"B62q..."}}'
```

## Curl: inspect archive height before historical queries

```bash
curl -sS https://gateway.mina.archive.devnet.zeko.io \
  -H 'content-type: application/json' \
  --data '{"query":"query NetworkState { networkState { maxBlockHeight { canonicalMaxBlockHeight pendingMaxBlockHeight } } }"}'
```

## Curl: inspect historical Mina actions from the archive node

```bash
curl -sS https://gateway.mina.archive.devnet.zeko.io \
  -H 'content-type: application/json' \
  --data '{"query":"query FetchActions($pk: String!) { actions(input: { address: $pk, from: 0, to: 1 }) { blockInfo { height timestamp } actionData { transactionInfo { hash } data } } }","variables":{"pk":"B62q..."}}'
```

## Curl: inspect Zeko archive event filter fields before running an event query

```bash
curl -sS https://archive.testnet.zeko.io/graphql \
  -H 'content-type: application/json' \
  --data '{"query":"query EventFilterShape { __type(name: \"EventFilterOptionsInput\") { inputFields { name } } }"}'
```

## Practical rule

- Use the live Zeko endpoint for `sequencerPk`, `circuitsConfig`, and live request status.
- Use archive nodes when you need historical actions, events, or backfill-style debugging.
