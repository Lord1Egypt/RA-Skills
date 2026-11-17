/**
 * x402 envelope encoder — pure library.
 *
 * Wraps a signed Stellar XDR as an x402 PaymentPayload and encodes
 * it for the X-Payment HTTP header. No network calls, no env reads.
 */

export interface X402PaymentRequirements {
  scheme: "exact";
  network: "stellar:testnet" | "stellar:pubnet";
  amount: string;
  asset: string;
  payTo: string;
  maxTimeoutSeconds: number;
  extra?: { areFeesSponsored?: boolean };
}

/**
 * The wire payload sent back after signing. Two shapes, by version:
 *   v1: scheme + network at the top level
 *   v2: the accepted PaymentRequirements echoed in `accepted`
 */
export type X402PaymentPayload =
  | {
      x402Version: number;
      scheme: "exact";
      network: string;
      payload: { transaction: string };
    }
  | {
      x402Version: number;
      accepted: X402PaymentRequirements;
      payload: { transaction: string };
    };

/** Wrap a signed XDR as an x402 PaymentPayload. */
export function wrapX402(
  transactionXdr: string,
  network: string,
  x402Version = 1,
  accepted?: X402PaymentRequirements,
): X402PaymentPayload {
  // The envelope shape changed between versions, and getting it wrong
  // fails silently: the server cannot parse the credential, so it
  // answers 402 again — indistinguishable from a rejected payment.
  //
  //   v1: { x402Version, scheme, network, payload }
  //   v2: { x402Version, accepted: PaymentRequirements, payload }
  //
  // v2 requires echoing back the exact requirement the client accepted.
  // Servers verify by strict equality against it (scheme, network,
  // asset, payTo, amount), so it must be the requirement object from
  // the challenge, not a reconstruction.
  if (x402Version >= 2) {
    if (!accepted) {
      throw new Error(
        "x402 v2 payload requires the accepted PaymentRequirements from the challenge.",
      );
    }
    return {
      x402Version,
      accepted,
      payload: { transaction: transactionXdr },
    };
  }
  return {
    x402Version,
    scheme: "exact",
    network,
    payload: { transaction: transactionXdr },
  };
}

/** Base64-encode a PaymentPayload for the X-Payment header. */
export function encodeX402Header(payload: X402PaymentPayload): string {
  return Buffer.from(JSON.stringify(payload), "utf8").toString("base64");
}

/**
 * Validate that the server advertised sponsored-fees mode.
 * x402 Stellar exact requires this; throws otherwise.
 */
export function assertSponsored(req: X402PaymentRequirements): void {
  if (req.extra?.areFeesSponsored === false) {
    throw new Error(
      "x402 Stellar exact requires areFeesSponsored=true. " +
        "The server advertised areFeesSponsored=false, which is not compatible.",
    );
  }
}
