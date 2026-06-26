#!/usr/bin/env node
/**
 * Tencent Meeting API - HMAC-SHA256 Signature Utility
 * Generates auth headers for Tencent Meeting REST API (AK/SK).
 *
 * Usage:
 *   node sign.js <method> <uri> [body]
 *
 * Env vars required:
 *   TM_SECRET_ID   - API SecretId (X-TC-Key)
 *   TM_SECRET_KEY  - API SecretKey
 *   TM_APP_ID      - Enterprise AppId
 *   TM_SDK_ID      - Application SdkId
 */

const crypto = require("crypto");

function sign(secretId, secretKey, method, nonce, timestamp, uri, body) {
  const headerString = `X-TC-Key=${secretId}&X-TC-Nonce=${nonce}&X-TC-Timestamp=${timestamp}`;
  const toSign = `${method}\n${headerString}\n${uri}\n${body}`;
  const hmac = crypto.createHmac("sha256", secretKey);
  hmac.update(toSign);
  const hexHash = hmac.digest("hex");
  return Buffer.from(hexHash).toString("base64");
}

function buildHeaders(method, uri, body = "") {
  const secretId = process.env.TM_SECRET_ID;
  const secretKey = process.env.TM_SECRET_KEY;
  const appId = process.env.TM_APP_ID;
  const sdkId = process.env.TM_SDK_ID;

  if (!secretId || !secretKey || !appId || !sdkId) {
    console.error("Error: Missing env vars. Set TM_SECRET_ID, TM_SECRET_KEY, TM_APP_ID, TM_SDK_ID");
    process.exit(1);
  }

  const nonce = Math.floor(Math.random() * 100000).toString();
  const timestamp = Math.floor(Date.now() / 1000).toString();
  const signature = sign(secretId, secretKey, method, nonce, timestamp, uri, body);

  return {
    "Content-Type": "application/json",
    "X-TC-Key": secretId,
    "X-TC-Timestamp": timestamp,
    "X-TC-Nonce": nonce,
    "X-TC-Signature": signature,
    "AppId": appId,
    "SdkId": sdkId,
    "X-TC-Registered": "1",
  };
}

// CLI mode
if (require.main === module) {
  const [,, method, uri, body] = process.argv;
  if (!method || !uri) {
    console.error("Usage: node sign.js <METHOD> <URI> [BODY]");
    process.exit(1);
  }
  const headers = buildHeaders(method.toUpperCase(), uri, body || "");
  console.log(JSON.stringify(headers, null, 2));
}

module.exports = { sign, buildHeaders };
