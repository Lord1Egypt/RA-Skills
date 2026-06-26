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

export interface X402PaymentPayload {
  x402Version: number;
  scheme: "exact";
  network: string;
  payload: { transaction: string };
}

/** Wrap a signed XDR as an x402 PaymentPayload. */
export function wrapX402(
  transactionXdr: string,
  network: string,
  x402Version = 1,
): X402PaymentPayload {
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
