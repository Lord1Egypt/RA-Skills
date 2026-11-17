import { pathToFileURL } from "node:url";

export const endpoint = "https://api.usesaferoute.com/v1/swap-safety-check";
export const input = { from: "USDC", to: "WETH", amount: "1" };
export const payTo = "0x08a6a2ddecdebdbfcb29d725042a6f3d74849e08";
export const usdc = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913";
export function permitted(requirement) {
  return (
    requirement.scheme === "exact" &&
    requirement.network === "eip155:8453" &&
    requirement.asset?.toLowerCase() === usdc &&
    requirement.payTo?.toLowerCase() === payTo &&
    /^\d+$/.test(requirement.amount) &&
    BigInt(requirement.amount) === 1000n
  );
}
export async function runFirstCall({
  fetchImpl = fetch,
  paidFetch,
  source,
  applicationId,
  referralCode,
} = {}) {
  for (const value of [source, applicationId, referralCode]) {
    if (value !== undefined && !/^[a-zA-Z0-9_.:-]{1,80}$/.test(value))
      throw new Error(
        "Use non-personal attribution labels of 1–80 letters, digits, dots, underscores, colons or hyphens.",
      );
  }
  const headers = {
    "Content-Type": "application/json",
    ...(source ? { "X-SafeRoute-Source": source } : {}),
    ...(applicationId ? { "X-SafeRoute-Application": applicationId } : {}),
    ...(referralCode ? { "X-SafeRoute-Referral": referralCode } : {}),
  };
  const options = {
    method: "POST",
    headers,
    body: JSON.stringify(input),
    redirect: "error",
    signal: AbortSignal.timeout(20000),
  };
  const probe = await fetchImpl(endpoint, options);
  if (probe.status !== 402)
    throw new Error(
      `Expected an unpaid 402 challenge, received ${probe.status}`,
    );
  const encoded = probe.headers.get("payment-required");
  if (!encoded) throw new Error("Missing PAYMENT-REQUIRED header");
  const challenge = JSON.parse(Buffer.from(encoded, "base64").toString());
  if (!challenge.accepts?.some(permitted))
    throw new Error(
      "Unexpected network, merchant or price; no payment authorized",
    );
  if (!paidFetch)
    return {
      stage: "challenge_verified",
      priceUsdc: 0.001,
      paid: false,
      next: "Use your existing x402 client only after authorizing one 0.001 USDC service payment.",
    };
  const response = await paidFetch(endpoint, {
    ...options,
    signal: AbortSignal.timeout(60000),
  });
  const settlementHeader = response.headers.get("payment-response");
  const body = await response.json();
  const settlement = settlementHeader
    ? JSON.parse(Buffer.from(settlementHeader, "base64").toString())
    : null;
  if (
    !response.ok ||
    !body ||
    body.error ||
    body.isError === true ||
    !settlement?.success ||
    !/^0x[0-9a-f]{64}$/i.test(settlement.transaction ?? "")
  )
    throw new Error(
      "Payment or result is unconfirmed. Do not automatically retry; reconcile the original attempt.",
    );
  const requestId = response.headers.get("x-saferoute-request-id");
  const feedbackContext = new URLSearchParams({ product: "swap_safety_check" });
  if (requestId && /^[0-9a-f-]{36}$/i.test(requestId))
    feedbackContext.set("request", requestId);
  if (source) feedbackContext.set("source", source);
  if (applicationId) feedbackContext.set("application", applicationId);
  return {
    stage: "paid_response_received",
    requestId,
    optionalFeedback: `https://usesaferoute.com/api-feedback#${feedbackContext}`,
    settlement,
    result: body,
  };
}
async function main() {
  console.log(
    JSON.stringify(
      await runFirstCall({
        source: process.env.SAFEROUTE_SOURCE || undefined,
        applicationId: process.env.SAFEROUTE_APPLICATION || undefined,
      }),
      null,
      2,
    ),
  );
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href)
  main().catch((error) => {
    console.error(error.message);
    process.exitCode = 1;
  });
