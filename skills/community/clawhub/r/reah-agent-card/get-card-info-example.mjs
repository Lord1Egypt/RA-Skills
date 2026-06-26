#!/usr/bin/env node
import { webcrypto } from "node:crypto";

const DEFAULT_ENDPOINT = "https://agents.reah.com/graphql";
const FETCH_CARD_INFO_BY_ACCESS_KEY_QUERY = `query FetchByAccessKey($accessKey: String!, $sessionId: String!) {
  individualCardByAccessKey(accessKey: $accessKey, sessionId: $sessionId) {
    cardInfoPartA: encryptedPan { iv data }
    cardInfoPartB: encryptedCvc { iv data }
  }
}`;
const REAH_CARD_RSA_PUBLIC_KEY = `-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCAP192809jZyaw62g/eTzJ3P9H
+RmT88sXUYjQ0K8Bx+rJ83f22+9isKx+lo5UuV8tvOlKwvdDS/pVbzpG7D7NO45c
0zkLOXwDHZkou8fuj8xhDO5Tq3GzcrabNLRLVz3dkx0znfzGOhnY4lkOMIdKxlQb
LuVM/dGDC9UpulF+UwIDAQAB
-----END PUBLIC KEY-----`;

const cryptoApi = globalThis.crypto ?? webcrypto;
const textEncoder = new TextEncoder();
const textDecoder = new TextDecoder();

function usage() {
  process.stderr.write(`Usage:
  node get-card-info-example.mjs --access-key <key> [options]

Options:
  --timeout-ms <ms>       Request timeout (default: 15000)
`);
}

function parseArgs(argv) {
  const opts = {
    timeoutMs: 15000,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    switch (arg) {
      case "--access-key":
        opts.accessKey = argv[++i];
        break;
      case "--timeout-ms":
        opts.timeoutMs = Number.parseInt(argv[++i], 10);
        break;
      case "-h":
      case "--help":
        usage();
        process.exit(0);
        break;
      default:
        throw new Error(`unknown argument: ${arg}`);
    }
  }

  if (!opts.accessKey) {
    throw new Error("--access-key is required");
  }
  if (!Number.isFinite(opts.timeoutMs) || opts.timeoutMs <= 0) {
    throw new Error("--timeout-ms must be a positive integer");
  }
  return opts;
}

function isHex(input) {
  return /^[0-9A-Fa-f]+$/.test(input);
}

function hexToBytes(hex) {
  if (!isHex(hex) || hex.length % 2 !== 0) {
    throw new Error("hex must be an even-length hex string");
  }

  const out = new Uint8Array(hex.length / 2);
  for (let i = 0; i < hex.length; i += 2) {
    out[i / 2] = Number.parseInt(hex.slice(i, i + 2), 16);
  }
  return out;
}

function bytesToBase64(bytes) {
  return Buffer.from(bytes).toString("base64");
}

function base64ToBytes(input) {
  return new Uint8Array(Buffer.from(input, "base64"));
}

function parsePemToDer(pem) {
  const header = "-----BEGIN PUBLIC KEY-----";
  const footer = "-----END PUBLIC KEY-----";
  if (!pem.includes(header) || !pem.includes(footer)) {
    throw new Error("invalid PEM public key");
  }
  const body = pem
    .replace(header, "")
    .replace(footer, "")
    .replace(/\s+/g, "");
  return Buffer.from(body, "base64");
}

async function generateSessionId(pem) {
  if (!pem) {
    throw new Error("pem is required");
  }

  const secretKey = cryptoApi.randomUUID().replace(/-/g, "");
  const secretKeyBase64 = bytesToBase64(hexToBytes(secretKey));

  const rsaPublicKey = await cryptoApi.subtle.importKey(
    "spki",
    parsePemToDer(pem),
    { name: "RSA-OAEP", hash: "SHA-1" },
    true,
    ["encrypt"],
  );

  const encrypted = await cryptoApi.subtle.encrypt(
    { name: "RSA-OAEP" },
    rsaPublicKey,
    textEncoder.encode(secretKeyBase64),
  );

  return {
    secretKey,
    sessionId: bytesToBase64(new Uint8Array(encrypted)),
  };
}

async function decryptSecret(base64Secret, base64Iv, secretKey) {
  if (!base64Secret) {
    throw new Error("base64Secret is required");
  }
  if (!base64Iv) {
    throw new Error("base64Iv is required");
  }
  if (!secretKey || !isHex(secretKey)) {
    throw new Error("secretKey must be a hex string");
  }

  const cryptoKey = await cryptoApi.subtle.importKey(
    "raw",
    hexToBytes(secretKey),
    { name: "AES-GCM" },
    false,
    ["decrypt"],
  );

  const decrypted = await cryptoApi.subtle.decrypt(
    { name: "AES-GCM", iv: base64ToBytes(base64Iv) },
    cryptoKey,
    base64ToBytes(base64Secret),
  );

  return textDecoder.decode(decrypted);
}

function buildHeaders() {
  return {
    "content-type": "application/json",
  };
}

function parseEncryptedPayload(json) {
  const result = json?.data?.individualCardByAccessKey;
  if (!result?.cardInfoPartA?.iv || !result?.cardInfoPartA?.data) {
    return null;
  }
  if (!result?.cardInfoPartB?.iv || !result?.cardInfoPartB?.data) {
    return null;
  }
  return {
    encryptedCardInfoPartA: result.cardInfoPartA,
    encryptedCardInfoPartB: result.cardInfoPartB,
  };
}

async function postGraphQL(endpoint, headers, variables, timeoutMs) {
  if (endpoint !== DEFAULT_ENDPOINT) {
    throw new Error("Custom endpoint is not allowed for security reasons");
  }
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const resp = await fetch(endpoint, {
      method: "POST",
      headers,
      body: JSON.stringify({
        query: FETCH_CARD_INFO_BY_ACCESS_KEY_QUERY,
        variables,
      }),
      signal: controller.signal,
    });

    const text = await resp.text();
    let json;
    try {
      json = JSON.parse(text);
    } catch {
      throw new Error(`non-JSON GraphQL response (status ${resp.status}): ${text}`);
    }

    if (!resp.ok) {
      throw new Error(`GraphQL HTTP ${resp.status}: ${JSON.stringify(json)}`);
    }
    return json;
  } finally {
    clearTimeout(timer);
  }
}

async function main() {
  try {
    const opts = parseArgs(process.argv.slice(2));
    const headers = buildHeaders();

    const { secretKey, sessionId } = await generateSessionId(REAH_CARD_RSA_PUBLIC_KEY);

    const json = await postGraphQL(
      DEFAULT_ENDPOINT,
      headers,
      {
        accessKey: opts.accessKey,
        sessionId,
      },
      opts.timeoutMs,
    );

    const encrypted = parseEncryptedPayload(json);
    if (!encrypted) {
      throw new Error(`GraphQL query failed: ${JSON.stringify(json?.errors ?? json)}`);
    }

    await decryptSecret(
      encrypted.encryptedCardInfoPartA.data,
      encrypted.encryptedCardInfoPartA.iv,
      secretKey,
    );
    await decryptSecret(
      encrypted.encryptedCardInfoPartB.data,
      encrypted.encryptedCardInfoPartB.iv,
      secretKey,
    );
  } catch (err) {
    process.stderr.write(`${err.message}\n`);
    process.exit(1);
  }
}

await main();
