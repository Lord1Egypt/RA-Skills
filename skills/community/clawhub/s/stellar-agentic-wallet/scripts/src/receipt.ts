/**
 * Payment-Receipt decoding — pure library.
 *
 * A 402 server returns the settlement proof in the `Payment-Receipt`
 * response header as a dot-separated, base64url-encoded token. The exact
 * segment layout differs per dialect (single-segment payload vs. classic
 * JWT header.payload.signature), so we decode every segment that parses
 * as a JSON object and merge them. Signature segments simply fail to
 * parse and are skipped.
 *
 * Everything here is best-effort: a receipt we cannot decode yields an
 * empty summary rather than an error, so a successful payment is never
 * reported as a failure because of a cosmetic parsing problem.
 */

export interface ReceiptSummary {
  /** Stellar transaction hash, only when it is a well-formed 64-hex hash. */
  txHash?: string;
  /** Human USDC amount, only when the receipt states it unambiguously. */
  amount?: string;
  /** Destination account the payment settled to. */
  payTo?: string;
  /** ISO-8601 timestamp, converted from unix seconds when needed. */
  timestamp?: string;
}

function decodeBase64UrlJson(segment: string): Record<string, unknown> | null {
  if (!segment) return null;
  try {
    const b64 = segment.replace(/-/g, "+").replace(/_/g, "/");
    const text = Buffer.from(b64, "base64").toString("utf8");
    const parsed = JSON.parse(text);
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) return null;
    return parsed as Record<string, unknown>;
  } catch {
    return null;
  }
}

export function decodeReceipt(receipt: string): ReceiptSummary {
  const merged: Record<string, unknown> = {};
  for (const segment of receipt.split(".")) {
    const obj = decodeBase64UrlJson(segment);
    if (obj) Object.assign(merged, obj);
  }

  const str = (...keys: string[]): string | undefined => {
    for (const k of keys) {
      const v = merged[k];
      if (typeof v === "string" && v.trim()) return v.trim();
      if (typeof v === "number") return String(v);
    }
    return undefined;
  };

  // Amounts are reported either as human USDC ("0.025") or as base units
  // ("250000"), and the token carries no unit metadata to tell them apart.
  // A bare integer is genuinely ambiguous — "1" is both 1 USDC and
  // 0.0000001 USDC — and guessing wrong misreports what the user paid by
  // seven orders of magnitude. So we only accept a decimal-point value as
  // human USDC and leave the ambiguous case undefined; the caller falls
  // back to the 402 challenge, whose units are unambiguous.
  const rawAmount = str("amount", "maxAmountRequired", "value");
  const amount = rawAmount && /^\d+\.\d+$/.test(rawAmount) ? rawAmount : undefined;

  const rawTimestamp = str("timestamp", "iat", "settledAt");
  const timestamp =
    rawTimestamp && /^\d{9,10}$/.test(rawTimestamp)
      ? new Date(Number(rawTimestamp) * 1000).toISOString()
      : rawTimestamp;

  // Explicit transaction-hash fields win over the generic `reference`,
  // which is not guaranteed to be a transaction hash at all. Whatever we
  // pick must look like a Stellar tx hash (32 bytes, hex) before it is
  // turned into an explorer URL — a bad link is worse than no link.
  const candidate = str("transaction", "txHash", "tx_hash", "hash", "reference");
  const txHash =
    candidate && /^[0-9a-fA-F]{64}$/.test(candidate) ? candidate : undefined;

  return {
    txHash,
    amount,
    payTo: str("payTo", "pay_to", "destination", "to", "recipient"),
    timestamp,
  };
}

export function explorerUrl(
  txHash: string,
  network: "testnet" | "pubnet",
): string {
  const segment = network === "pubnet" ? "public" : "testnet";
  return `https://stellar.expert/explorer/${segment}/tx/${txHash}`;
}
