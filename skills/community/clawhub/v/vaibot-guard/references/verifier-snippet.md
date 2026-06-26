# Inclusion Proof Verifier (reference)

This is a minimal verifier for VAIBot Guard inclusion proofs.

Assumptions:
- `leaf` is the leaf hash returned by the service (`sha256("leaf:" + eventHash)` already applied).
- `siblings[]` is the ordered list of sibling hashes returned by the service.
- Parent hash is ordered (left-to-right) as implemented in the guard: `sha256("node:" + left + ":" + right)`.

```ts
import { createHash } from "node:crypto";

function sha256Hex(s: string) {
  return createHash("sha256").update(s).digest("hex");
}

function parentHash(left: string, right: string) {
  return sha256Hex("node:" + left + ":" + right);
}

export function verifyInclusionProof(params: {
  leaf: string;
  siblings: string[];
  index: number; // 0-based leaf index
  expectedRoot: string;
}) {
  let h = params.leaf;
  let idx = params.index;

  for (const sib of params.siblings) {
    const isRight = idx % 2 === 1;
    h = isRight ? parentHash(sib, h) : parentHash(h, sib);
    idx = Math.floor(idx / 2);
  }

  return h === params.expectedRoot;
}
```
