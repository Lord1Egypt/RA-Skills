#!/usr/bin/env node
/**
 * Read-only x402 challenge check: makes one unpaid HTTP request.
 * No wallet access, signing, settlement, or automatic retry.
 */
import { EXPECTED, inspectOffer } from "./offer-terms.mjs";

const target = process.argv[2] || "https://example.com/";
if (!/^https:\/\//i.test(target)) {
  console.error("Usage: node scripts/check-offer.mjs https://public.example/path");
  process.exit(2);
}

const url = new URL("https://signallayer.floot.app/_api/v1/agent/preflight");
url.searchParams.set("target", target);
url.searchParams.set("intent", "pay");

const res = await fetch(url, { redirect: "manual", signal: AbortSignal.timeout(15000) });
if (res.status !== 402) {
  throw new Error(`Expected an unpaid 402 challenge; got HTTP ${res.status}`);
}
const header = res.headers.get("payment-required");
if (!header) throw new Error("Missing PAYMENT-REQUIRED header");

let requirement;
try {
  requirement = JSON.parse(Buffer.from(header, "base64").toString("utf8"));
} catch {
  throw new Error("Malformed PAYMENT-REQUIRED challenge");
}

const verdict = inspectOffer(requirement, { resourceUrl: url.toString() });
console.log(JSON.stringify({
  httpStatus: res.status,
  x402Version: requirement.x402Version,
  expectedPriceAtomicUnits: EXPECTED.amount,
  ...verdict
}, null, 2));
if (!verdict.valid) {
  console.error("STOP: payment terms do not match the expected recipient, asset, chain, price and resource.");
  process.exit(1);
}
console.log("PASS: unsigned x402 challenge matches known terms. No payment and no safety assessment occurred.");
