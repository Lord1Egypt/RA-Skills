import {
  getTokenAddress,
  getChainName,
  isPayoutSupported,
  type TokenSymbol,
} from "./chains.js";
import { randomUUID } from "crypto";

const API_BASE = "https://intentapiv4.rozo.ai/functions/v1/payment-api";
const MIN_AMOUNT = 0.01;
const MAX_AMOUNT = 10_000;

export interface CreatePaymentParams {
  appId?: string;
  type?: "exactIn" | "exactOut";
  sourceChain: number;
  sourceToken: TokenSymbol;
  destChain: number;
  destAddress: string;
  destToken: TokenSymbol;
  destAmount: string;
  destMemo?: string;
  orderId?: string;
  sourceAmount?: string;
  dryrun?: boolean;
}

export interface PaymentResponse {
  success: boolean;
  payment?: Record<string, unknown>;
  statusCode?: number;
  error?: unknown;
}

export async function createPayment(params: CreatePaymentParams): Promise<PaymentResponse> {
  const {
    appId = "rozoAgent",
    type = "exactOut",
    sourceChain,
    sourceToken,
    destChain,
    destAddress,
    destToken,
    destAmount,
    destMemo,
    orderId,
    sourceAmount,
    dryrun = false,
  } = params;

  // Validate amount limits
  const amount = parseFloat(destAmount);
  if (isNaN(amount) || amount < MIN_AMOUNT || amount > MAX_AMOUNT) {
    return {
      success: false,
      error: `Amount must be between $${MIN_AMOUNT} and $${MAX_AMOUNT.toLocaleString()}. Got: ${destAmount}`,
    };
  }

  if (!isPayoutSupported(destChain, destToken)) {
    return {
      success: false,
      error: `Payout not supported: ${destToken} on ${getChainName(destChain)}`,
    };
  }

  const sourceTokenInfo = getTokenAddress(sourceChain, sourceToken, "payin");
  if (!sourceTokenInfo) {
    return {
      success: false,
      error: `Pay-in not supported: ${sourceToken} on ${getChainName(sourceChain)}`,
    };
  }

  const destTokenInfo = getTokenAddress(destChain, destToken, "payout");
  if (!destTokenInfo) {
    return {
      success: false,
      error: `Payout not supported: ${destToken} on ${getChainName(destChain)}`,
    };
  }

  const payload: Record<string, unknown> = {
    appId,
    type,
    orderId: orderId ?? randomUUID(),
    display: {
      title: "Payment",
      currency: "USD",
    },
    source: {
      chainId: sourceChain,
      tokenSymbol: sourceToken,
      tokenAddress: sourceTokenInfo.address,
      ...(type === "exactIn" && { amount: sourceAmount ?? destAmount }),
    },
    destination: {
      chainId: destChain,
      receiverAddress: destAddress,
      tokenSymbol: destToken,
      tokenAddress: destTokenInfo.address,
      ...(type === "exactOut" && { amount: destAmount }),
      ...(destMemo && { receiverMemo: destMemo }),
    },
  };

  let response: Response;
  try {
    const url = dryrun ? `${API_BASE}?dryrun=true` : API_BASE;
    response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  } catch (err) {
    return { success: false, error: `Network error: ${(err as Error).message}` };
  }

  let body: Record<string, unknown>;
  try {
    body = await response.json();
  } catch {
    return { success: false, statusCode: response.status, error: "Invalid JSON response from Rozo API" };
  }

  if (!response.ok) {
    return { success: false, statusCode: response.status, error: body };
  }

  return { success: true, payment: body };
}

// CLI entry point
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  const get = (flag: string): string | undefined => {
    const idx = args.indexOf(flag);
    return idx !== -1 ? args[idx + 1] : undefined;
  };

  const sourceChain = get("--source-chain");
  const sourceToken = get("--source-token");
  const destChain = get("--dest-chain");
  const destAddress = get("--dest-address");
  const destToken = get("--dest-token");
  const destAmount = get("--dest-amount");

  if (!sourceChain || !sourceToken || !destChain || !destAddress || !destToken || !destAmount) {
    console.error(
      "Usage: --source-chain <id> --source-token <USDC|USDT> --dest-chain <id> --dest-address <addr> --dest-token <USDC|USDT> --dest-amount <amount>"
    );
    process.exit(1);
  }

  const result = await createPayment({
    appId: get("--app-id") ?? "rozoAgent",
    type: (get("--type") as "exactIn" | "exactOut") ?? "exactOut",
    sourceChain: Number(sourceChain),
    sourceToken: sourceToken.toUpperCase() as TokenSymbol,
    destChain: Number(destChain),
    destAddress,
    destToken: destToken.toUpperCase() as TokenSymbol,
    destAmount,
    destMemo: get("--dest-memo"),
    orderId: get("--order-id"),
    sourceAmount: get("--source-amount"),
    dryrun: args.includes("--dryrun"),
  });

  console.log(JSON.stringify(result, null, 2));
  if (!result.success) process.exit(1);
}
