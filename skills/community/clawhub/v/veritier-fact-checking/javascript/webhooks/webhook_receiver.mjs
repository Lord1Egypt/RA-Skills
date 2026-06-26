/**
 * Webhook Receiver with HMAC-SHA256 Verification - Veritier Example (JavaScript)
 * ================================================================================
 * A minimal Express server that receives async webhook deliveries from Veritier
 * and verifies their HMAC-SHA256 signatures before processing.
 *
 * When you enable webhooks in your Veritier dashboard and set `use_webhook: true`
 * in API requests, results are delivered asynchronously to this endpoint.
 *
 * Setup:
 *   1. npm install express dotenv
 *   2. Set VERITIER_WEBHOOK_SECRET in your .env (the vtsec_... value from the dashboard)
 *   3. node webhook_receiver.mjs
 *   4. The server listens on http://localhost:5050/webhooks/veritier
 *
 * For production:
 *   - Use HTTPS (required by Veritier for non-localhost URLs)
 *   - Deploy behind a reverse proxy (nginx, Caddy, etc.)
 *
 * Full webhook docs: https://veritier.ai/docs
 */

import "dotenv/config";
import express from "express";
import { createHmac, timingSafeEqual } from "node:crypto";

const app = express();
const PORT = 5050;

const WEBHOOK_SECRET = process.env.VERITIER_WEBHOOK_SECRET || "";

if (!WEBHOOK_SECRET) {
  console.warn("⚠ Warning: VERITIER_WEBHOOK_SECRET is not set.");
  console.warn("  Configure a webhook at https://veritier.ai/dashboard to get your secret.");
}

// IMPORTANT: Use raw body for HMAC verification, NOT parsed JSON
// Express must capture the raw bytes before any JSON middleware
app.use(
  "/webhooks/veritier",
  express.raw({ type: "application/json" })
);
app.use(express.json());

app.post("/webhooks/veritier", (req, res) => {
  /**
   * Receive and verify a Veritier webhook delivery.
   *
   * Security flow:
   *   1. Read the raw request body BEFORE any JSON parsing
   *   2. Compute HMAC-SHA256 of the raw bytes using your webhook secret
   *   3. Compare against the X-Veritier-Signature header (timing-safe)
   *   4. Only then parse and process the payload
   */
  const signature = req.headers["x-veritier-signature"] || "";

  if (!WEBHOOK_SECRET) {
    console.error("✗ Webhook secret not configured - rejecting request");
    return res.status(500).json({ error: "Webhook secret not configured" });
  }

  // ── Step 1: Verify the signature ────────────────────────────────────
  // req.body is a Buffer here because of express.raw() middleware
  const rawBody = req.body;

  const expectedSignature =
    "vtsec_" +
    createHmac("sha256", WEBHOOK_SECRET)
      .update(rawBody)
      .digest("hex");

  // Timing-safe comparison prevents signature oracle attacks
  try {
    const sigBuffer = Buffer.from(signature, "utf8");
    const expectedBuffer = Buffer.from(expectedSignature, "utf8");

    if (
      sigBuffer.length !== expectedBuffer.length ||
      !timingSafeEqual(sigBuffer, expectedBuffer)
    ) {
      console.error("✗ Invalid webhook signature - rejecting request");
      return res.status(401).json({ error: "Invalid signature" });
    }
  } catch {
    console.error("✗ Signature comparison failed - rejecting request");
    return res.status(401).json({ error: "Invalid signature" });
  }

  // ── Step 2: Parse and process the payload ───────────────────────────
  const payload = JSON.parse(rawBody.toString("utf8"));
  const transactionId = payload.transaction_id || "unknown";
  const results = payload.results || [];

  const icons = { true: "✅", false: "❌", null: "❓" };

  console.log(`\n${"─".repeat(50)}`);
  console.log(`✓ Webhook received - Transaction: ${transactionId}`);
  console.log(`  Claims verified: ${results.length}`);

  for (const r of results) {
    const icon = icons[String(r.verdict)] || "❓";
    console.log(`  ${icon} ${r.claim} → ${r.verdict}`);
  }

  console.log(`${"─".repeat(50)}\n`);

  return res.json({ status: "ok" });
});

app.get("/health", (_req, res) => {
  res.json({ status: "ok" });
});

app.listen(PORT, () => {
  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  console.log("  Veritier Webhook Receiver");
  console.log(`  Listening on http://localhost:${PORT}/webhooks/veritier`);
  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
});
