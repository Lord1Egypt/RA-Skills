# Build On Zeko

Use this file when the user wants to build apps, zkApps, contracts, or lower-level integrations on Zeko.

## Start with Zeko docs

- Developer getting started: `https://docs.zeko.io/developers/getting-started`
- Custom network setup: `https://docs.zeko.io/developers/guides/custom-network`
- Bridge SDK docs: `https://docs.zeko.io/developers/guides/bridge-sdk`

## o1js path

- `o1js` is the default TypeScript path for most Zeko builders.
- Official docs: `https://docs.o1labs.org/o1js/`
- Constraint-system intro: `https://docs.o1labs.org/o1js/getting-started/what-is-a-zk-constraint-system`
- zkApps intro: `https://docs.o1labs.org/o1js/zkapps/intro`
- zkApp CLI: `https://github.com/o1-labs/zkapp-cli`
- o1js repo: `https://github.com/o1-labs/o1js`

## Inline Node plus o1js

- For ad hoc agent scripting, it is useful to have `o1js` installed in the current directory before running inline Node scripts that import it.
- This is a good fit when `curl` is too limited and the agent needs key handling, amount math, or live account inspection in one short script.

## Inline example: derive a sender public key and convert amounts

```bash
node --input-type=module <<'EOF'
import { PrivateKey, UInt64 } from "o1js"

const toNanomina = (value) => {
  const [whole, frac = ""] = value.split(".")
  return UInt64.from(
    BigInt(whole) * 1000000000n + BigInt((frac + "000000000").slice(0, 9))
  )
}

const senderKey = PrivateKey.fromBase58(process.env.MINA_PRIVATE_KEY)

console.log({
  from: senderKey.toPublicKey().toBase58(),
  amount: toNanomina("1.25").toString(),
  fee: toNanomina("0.10").toString()
})
EOF
```

## Inline example: parse a public key and keep the boundary straight

```bash
node --input-type=module <<'EOF'
import { PublicKey } from "o1js"

const pk = PublicKey.fromBase58(process.env.PUBLIC_KEY)

console.log({
  publicKey: pk.toBase58()
})
EOF
```

- You can derive a public key from a private key.
- You cannot derive a private key from a public key.
- So the reverse direction is parse and validate a public key string, not reconstruct a private key.

## Inline example: inspect a live Zeko account

```bash
node --input-type=module <<'EOF'
import { Mina, PublicKey } from "o1js"

const network = Mina.Network({
  networkId: "zeko",
  mina: "https://testnet.zeko.io/graphql",
  archive: "https://archive.testnet.zeko.io/graphql"
})

Mina.setActiveInstance(network)

const pk = PublicKey.fromBase58(process.env.ADDRESS)
const { account } = await Mina.fetchAccount({ publicKey: pk })

console.log({
  nonce: account?.nonce?.toString(),
  balance: account?.balance?.toString()
})
EOF
```

## OCaml path

- Direct OCaml and protocol-native work is also valid on Zeko.
- Public protocol repo: `https://github.com/zeko-labs/zeko`
- Use this path when the user explicitly wants lower-level contracts, rollup internals, sequencer-adjacent logic, or protocol research instead of `o1js`.

## MCP note

- No canonical public o1js MCP page is listed in the current o1Labs docs.
- If the agent environment already exposes an o1js MCP server, use it as a convenience layer and keep the official o1js docs as the semantic source of truth.

## Practical routing

- Need endpoints or direct GraphQL inspection: read `references/40-endpoints-and-curl.md`.
- Need protocol roles like sequencer or DA layer: read `references/60-sequencer-archive-and-da.md`.
