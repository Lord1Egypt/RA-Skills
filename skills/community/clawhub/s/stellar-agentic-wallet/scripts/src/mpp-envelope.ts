/**
 * MPP charge envelope encoder — thin wrapper over `mppx.Credential`.
 *
 * Historically this file hand-rolled the wire format (RFC 8785 canonicalize,
 * base64url JSON packing, DID construction). Every time mppx changed a
 * detail we drifted and shipped a regression (v1.1.0 through v1.1.3 each
 * fixed a different manifestation). Since mppx now ships the authoritative
 * serializer as a pure library with no peer deps beyond ox/zod/viem, we
 * delegate directly and this file stays a ~20-line adapter.
 *
 * What we still own:
 *  - Choosing the `source` DID from the challenge-provided `network` field
 *    (`did:pkh:${network}:${pubkey}` — note `network` already carries the
 *    `stellar:` chain prefix, so we must NOT prepend another).
 *  - Emitting the `{type: "transaction", transaction}` payload variant.
 *    mppx treats `payload` as an opaque discriminated union; the charge
 *    flow always produces a signed XDR.
 */
import * as mppx from "mppx";

/**
 * Re-export mppx's Challenge type under the name the rest of the skill
 * uses. This is the authoritative shape — `id, realm, method, intent,
 * request, expires?, description?, digest?, opaque?` — with `request`
 * and `opaque` as structured objects (not base64url strings).
 */
export type MppChallenge = mppx.Challenge.Challenge;

/** The `stellar.charge` request payload shape — narrows `challenge.request`. */
export interface MppChargeRequest {
  amount: string;
  currency: string;
  recipient: string;
  methodDetails?: {
    network?: string;
    feePayer?: boolean;
    maxTimeoutSeconds?: number;
    [k: string]: unknown;
  };
  [k: string]: unknown;
}

/**
 * Build the `Authorization: Payment <base64url>` header value for an
 * MPP charge credential.
 */
export function encodeMppHeader(
  transactionXdr: string,
  signerPubkey: string,
  challenge: MppChallenge,
): string {
  const req = challenge.request as MppChargeRequest;
  // The `network` field comes from the server challenge; it already
  // carries the chain name (`stellar:pubnet` / `stellar:testnet`), so
  // the DID is `did:pkh:${network}:${pubkey}` — NOT
  // `did:pkh:stellar:${network}:...` (which was the v1.1.2 bug producing
  // `did:pkh:stellar:stellar:pubnet:...`).
  const network = req.methodDetails?.network ?? "stellar:pubnet";
  const source = `did:pkh:${network}:${signerPubkey}`;

  return mppx.Credential.serialize({
    challenge,
    payload: { type: "transaction", transaction: transactionXdr },
    source,
  });
}
