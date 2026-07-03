# Vendored crypto

`eth-signer.mjs` is an esbuild bundle of `@noble/curves@1.6.0` + `@noble/hashes@1.5.0`
exposing two pure-JS, dependency-free functions used by `a2a-runtime.mjs`:

- `addressFromPrivateKey(pkHex)` → checksum-lowercase 0x address
- `signMessage(pkHex, message)` → EIP-191 personal_sign 65-byte hex (v=27/28)

Vendored so the skill signs runtime-token requests without requiring viem/ethers
in the OpenClaw host. MIT-licensed (noble). Regenerate with:

    npm i @noble/curves@1.6.0 @noble/hashes@1.5.0
    npx esbuild signer-src.mjs --bundle --format=esm --platform=node --outfile=eth-signer.mjs
