/**
 * Rozo intent API client — pure library, hardcoded API_BASE.
 *
 * If a caller needs to override the base URL for a self-hosted Rozo,
 * they must edit this file directly. CLI entry points do not expose
 * that override.
 */

const API_BASE = "https://intentapiv4.rozo.ai/functions/v1/payment-api";

export interface RozoCreateRequest {
  appId: "rozoAgent";
  orderId?: string;
  type: "exactOut";
  display: { title: string; description?: string; currency: "USD" };
  source: {
    chainId: number;
    tokenSymbol: "USDC";
    tokenAddress: string;
  };
  destination: {
    chainId: number;
    receiverAddress: string;
    receiverMemo?: string;
    tokenSymbol: "USDC" | "USDT";
    tokenAddress: string;
    amount: string;
  };
}

export interface RozoCreateResponse {
  id: string;
  appId: string;
  status: string;
  type: string;
  createdAt: string;
  expiresAt: string;
  source: {
    chainId: number;
    tokenSymbol: string;
    amount: string;
    receiverAddress: string;
    receiverMemo?: string;
    fee?: string;
  };
  destination: {
    chainId: number;
    receiverAddress: string;
    tokenSymbol: string;
    amount: string;
  };
}

/** Create a cross-chain payment intent. */
export async function createPayment(
  body: RozoCreateRequest,
): Promise<RozoCreateResponse> {
  const res = await fetch(`${API_BASE}/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Rozo create-payment failed: ${res.status} ${text}`);
  }
  return (await res.json()) as RozoCreateResponse;
}

/** Fetch the status of a payment intent. */
export async function getPaymentStatus(id: string): Promise<any> {
  const res = await fetch(`${API_BASE}/payments/${id}`);
  if (!res.ok) {
    throw new Error(`Status fetch failed: ${res.status} ${res.statusText}`);
  }
  return await res.json();
}
