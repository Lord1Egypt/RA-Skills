/**
 * Webhook Receiver with HMAC-SHA256 Verification - Veritier Example (JavaScript)
 * ================================================================================
 * Verifies X-Veritier-Signature against the raw body bytes, then processes
 * extract / verify / validate / attestation deliveries.
 *
 * Retries send the same Idempotency-Key / X-Veritier-Idempotency-Key
 * (attest: attestation:{action_id}:{transaction_id}). HMAC is over the body only.
 *
 * Setup:
 *   1. npm install
 *   2. Set VERITIER_WEBHOOK_SECRET in .env
 *   3. node webhook_receiver.mjs
 *
 * Docs: https://veritier.ai/docs#webhooks
 */

import "dotenv/config";
import express from "express";
import { createHmac, timingSafeEqual } from "node:crypto";

const app = express();
const PORT = 5050;
const WEBHOOK_SECRET = process.env.VERITIER_WEBHOOK_SECRET || "";
const seenIdem = new Set();

if (!WEBHOOK_SECRET) {
  console.warn("Warning: VERITIER_WEBHOOK_SECRET is not set.");
}

app.use("/webhooks/veritier", express.raw({ type: "application/json" }));
app.use(express.json());

app.post("/webhooks/veritier", (req, res) => {
  const signature = req.headers["x-veritier-signature"] || "";
  const idem =
    req.headers["idempotency-key"] || req.headers["x-veritier-idempotency-key"] || "";
  const actionId = req.headers["x-veritier-action-id"] || "";

  if (!WEBHOOK_SECRET) {
    return res.status(500).json({ error: "Webhook secret not configured" });
  }

  const rawBody = req.body;
  const expectedSignature =
    "vtsec_" + createHmac("sha256", WEBHOOK_SECRET).update(rawBody).digest("hex");

  try {
    const sigBuffer = Buffer.from(signature, "utf8");
    const expectedBuffer = Buffer.from(expectedSignature, "utf8");
    if (
      sigBuffer.length !== expectedBuffer.length ||
      !timingSafeEqual(sigBuffer, expectedBuffer)
    ) {
      return res.status(401).json({ error: "Invalid signature" });
    }
  } catch {
    return res.status(401).json({ error: "Invalid signature" });
  }

  if (idem) {
    if (seenIdem.has(idem)) {
      console.log(`Duplicate Idempotency-Key ${idem} - ignoring retry`);
      return res.json({ status: "ok", duplicate: true });
    }
    seenIdem.add(idem);
  }

  const payload = JSON.parse(rawBody.toString("utf8"));
  const transactionId = payload.transaction_id || "unknown";
  const kind = payload.type || "event";
  const results = payload.results;

  console.log(`\n${"─".repeat(50)}`);
  if (payload.is_test) console.log("[TEST MODE] No quota was consumed.");
  console.log(`type=${kind}  tx=${transactionId}  idem=${idem || "(none)"}`);
  if (actionId) console.log(`X-Veritier-Action-Id=${actionId}`);

  if (kind === "attestation" && results && !Array.isArray(results)) {
    console.log(`  decision=${results.decision}  credential_id=${results.credential_id}`);
  } else if (Array.isArray(results)) {
    console.log(`  claims: ${results.length}`);
    for (const r of results) {
      console.log(`    ${r.claim} -> ${r.verdict}`);
    }
  }

  console.log(`${"─".repeat(50)}\n`);
  return res.json({ status: "ok" });
});

app.get("/health", (_req, res) => {
  res.json({ status: "ok" });
});

app.listen(PORT, () => {
  console.log("Veritier Webhook Receiver");
  console.log(`  Listening on http://localhost:${PORT}/webhooks/veritier`);
});
