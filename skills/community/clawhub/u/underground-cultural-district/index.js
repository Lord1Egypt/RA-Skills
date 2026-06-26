#!/usr/bin/env node

/**
 * Underground Cultural District — MCP Server v4.1.0
 *
 * 19 tools:
 *   13 free developer utilities (Crossroads Forge)
 *    3 marketplace catalog tools (browse, search, buy)
 *    3 agent tools (agent-mesh, agent-identity, pet-rock-lobster)
 *
 * Data: https://substratesymposium.com/api/products.json
 * Payment: Stripe hosted checkout
 * By Lisa Maraventano & Spine
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { createHash, randomBytes, randomUUID } from "node:crypto";

// ---------------------------------------------------------------------------
// Catalog cache
// ---------------------------------------------------------------------------
const CATALOG_URL = "https://substratesymposium.com/api/products.json";
const CACHE_TTL = 15 * 60 * 1000; // 15 minutes

let _cache = null;
let _cacheTs = 0;

async function getCatalog() {
  if (_cache && Date.now() - _cacheTs < CACHE_TTL) return _cache;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);
  try {
    const res = await fetch(CATALOG_URL, { signal: controller.signal });
    if (!res.ok) throw new Error(`Catalog fetch failed: ${res.status}`);
    _cache = await res.json();
    _cacheTs = Date.now();
    return _cache;
  } catch (err) {
    if (err.name === "AbortError") throw new Error("Catalog fetch timed out (8s). Try again.");
    throw err;
  } finally {
    clearTimeout(timeout);
  }
}

// ---------------------------------------------------------------------------
// Tool definitions
// ---------------------------------------------------------------------------
const TOOLS = [
  // ── Free Developer Tools (Crossroads Forge) ──────────────────────────
  {
    name: "generate-uuid",
    description:
      "Generate UUID v4 identifiers. Returns 1–100 UUIDs, one per line.",
    inputSchema: {
      type: "object",
      properties: {
        count: {
          type: "number",
          description: "How many UUIDs (1–100, default 1)",
          default: 1,
        },
      },
    },
  },
  {
    name: "format-json",
    description:
      "Pretty-print, minify, or validate a JSON string.",
    inputSchema: {
      type: "object",
      properties: {
        json: { type: "string", description: "JSON string" },
        mode: {
          type: "string",
          enum: ["pretty", "minify", "validate"],
          description: "Operation (default: pretty)",
          default: "pretty",
        },
      },
      required: ["json"],
    },
  },
  {
    name: "encode-base64",
    description: "Encode text to Base64.",
    inputSchema: {
      type: "object",
      properties: {
        text: { type: "string", description: "Text to encode" },
      },
      required: ["text"],
    },
  },
  {
    name: "decode-base64",
    description: "Decode a Base64 string to text.",
    inputSchema: {
      type: "object",
      properties: {
        encoded: { type: "string", description: "Base64 string" },
      },
      required: ["encoded"],
    },
  },
  {
    name: "generate-hash",
    description: "Hash text with SHA-256, SHA-512, or MD5.",
    inputSchema: {
      type: "object",
      properties: {
        text: { type: "string", description: "Text to hash" },
        algorithm: {
          type: "string",
          enum: ["sha256", "sha512", "md5"],
          description: "Algorithm (default: sha256)",
          default: "sha256",
        },
      },
      required: ["text"],
    },
  },
  {
    name: "generate-password",
    description:
      "Generate a secure random password (8–128 chars).",
    inputSchema: {
      type: "object",
      properties: {
        length: {
          type: "number",
          description: "Length (default 16)",
          default: 16,
        },
        includeNumbers: { type: "boolean", default: true },
        includeSymbols: { type: "boolean", default: true },
        includeUppercase: { type: "boolean", default: true },
        includeLowercase: { type: "boolean", default: true },
      },
    },
  },
  {
    name: "decode-jwt",
    description:
      "Decode a JWT token and return its header and payload. Does not verify signatures.",
    inputSchema: {
      type: "object",
      properties: {
        token: { type: "string", description: "JWT token" },
      },
      required: ["token"],
    },
  },
  {
    name: "convert-timestamp",
    description:
      "Convert between Unix epoch (seconds), ISO 8601, and human-readable date strings. Pass 'now' as value for current time.",
    inputSchema: {
      type: "object",
      properties: {
        value: {
          type: "string",
          description: "Timestamp value or 'now'",
        },
        from: {
          type: "string",
          enum: ["unix", "iso", "now"],
          default: "unix",
        },
        to: {
          type: "string",
          enum: ["unix", "iso", "human"],
          default: "human",
        },
      },
      required: ["value"],
    },
  },
  {
    name: "test-regex",
    description:
      "Test a regular expression against text. Returns all matches with positions and capture groups.",
    inputSchema: {
      type: "object",
      properties: {
        pattern: { type: "string", description: "Regex pattern" },
        text: { type: "string", description: "Text to test" },
        flags: {
          type: "string",
          description: "Regex flags (default: g)",
          default: "g",
        },
      },
      required: ["pattern", "text"],
    },
  },
  {
    name: "build-cron",
    description:
      "Parse a cron expression and explain what each field means in plain English.",
    inputSchema: {
      type: "object",
      properties: {
        expression: {
          type: "string",
          description: "Cron expression, e.g. '0 9 * * 1'",
        },
      },
      required: ["expression"],
    },
  },
  {
    name: "convert-eth-units",
    description: "Convert between Wei, Gwei, and ETH.",
    inputSchema: {
      type: "object",
      properties: {
        value: { type: "string", description: "Numeric value" },
        from: { type: "string", enum: ["wei", "gwei", "eth"] },
        to: { type: "string", enum: ["wei", "gwei", "eth"] },
      },
      required: ["value", "from", "to"],
    },
  },
  {
    name: "validate-wallet",
    description:
      "Validate an Ethereum or Bitcoin wallet address (format check only, no blockchain calls).",
    inputSchema: {
      type: "object",
      properties: {
        address: { type: "string", description: "Wallet address" },
        chain: { type: "string", enum: ["eth", "btc"] },
      },
      required: ["address", "chain"],
    },
  },
  {
    name: "encode-url",
    description: "URL-encode or URL-decode a string.",
    inputSchema: {
      type: "object",
      properties: {
        text: { type: "string", description: "Text to process" },
        mode: {
          type: "string",
          enum: ["encode", "decode"],
          default: "encode",
        },
      },
      required: ["text"],
    },
  },

  // ── Catalog Tools ────────────────────────────────────────────────────
  {
    name: "browse-underground",
    description:
      "Browse Underground Cultural District marketplace. Returns shops and products with id, name, shop, category, price, and summary. Optionally filter by shop name.",
    inputSchema: {
      type: "object",
      properties: {
        shop: {
          type: "string",
          description: "Filter by shop name (optional, partial match)",
        },
      },
    },
  },
  {
    name: "search-underground",
    description:
      "Search products across all Underground shops by keyword. Optionally filter by category or max price.",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Search keywords" },
        category: {
          type: "string",
          description: "Filter by category (optional)",
        },
        price_max: {
          type: "number",
          description: "Maximum price in USD (optional)",
        },
      },
      required: ["query"],
    },
  },
  {
    name: "buy-from-underground",
    description:
      "Get the purchase or delivery link for a product. Free items return the delivery URL directly. Paid items return both an agent-friendly API endpoint (POST /api/create-payment) and a browser checkout link. Use search-underground first to find product IDs.",
    inputSchema: {
      type: "object",
      properties: {
        product_id: {
          type: "string",
          description: "Product ID or name (partial match supported)",
        },
      },
      required: ["product_id"],
    },
  },
];

// ---------------------------------------------------------------------------
// Tool implementations
// ---------------------------------------------------------------------------

function handleGenerateUuid(args) {
  const n = Math.min(Math.max(args.count || 1, 1), 100);
  return Array.from({ length: n }, () => randomUUID()).join("\n");
}

function handleFormatJson(args) {
  const parsed = JSON.parse(args.json);
  const mode = args.mode || "pretty";
  if (mode === "validate") return "Valid JSON";
  if (mode === "minify") return JSON.stringify(parsed);
  return JSON.stringify(parsed, null, 2);
}

function handleEncodeBase64(args) {
  return Buffer.from(args.text, "utf-8").toString("base64");
}

function handleDecodeBase64(args) {
  return Buffer.from(args.encoded, "base64").toString("utf-8");
}

function handleGenerateHash(args) {
  const alg = args.algorithm || "sha256";
  return createHash(alg).update(args.text).digest("hex");
}

function handleGeneratePassword(args) {
  const len = Math.min(Math.max(args.length || 16, 8), 128);
  let chars = "";
  if (args.includeLowercase !== false) chars += "abcdefghijklmnopqrstuvwxyz";
  if (args.includeUppercase !== false) chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  if (args.includeNumbers !== false) chars += "0123456789";
  if (args.includeSymbols !== false) chars += "!@#$%^&*()_+-=[]{}|;:,.<>?";
  if (!chars) chars = "abcdefghijklmnopqrstuvwxyz";
  const bytes = randomBytes(len);
  return Array.from(bytes, (b) => chars[b % chars.length]).join("");
}

function handleDecodeJwt(args) {
  const parts = args.token.split(".");
  if (parts.length !== 3) throw new Error("Invalid JWT: expected 3 dot-separated parts");
  const header = JSON.parse(Buffer.from(parts[0], "base64url").toString());
  const payload = JSON.parse(Buffer.from(parts[1], "base64url").toString());
  const out = { header, payload };
  if (payload.exp) {
    const exp = new Date(payload.exp * 1000);
    out.expires = exp.toISOString();
    out.expired = exp < new Date();
  }
  return JSON.stringify(out, null, 2);
}

function handleConvertTimestamp(args) {
  const from = args.from || "unix";
  const to = args.to || "human";
  let ms;
  if (from === "now" || args.value === "now") {
    ms = Date.now();
  } else if (from === "unix") {
    const v = Number(args.value);
    ms = v > 1e12 ? v : v * 1000; // auto-detect seconds vs ms
  } else {
    ms = new Date(args.value).getTime();
  }
  if (Number.isNaN(ms)) throw new Error("Could not parse timestamp");
  const d = new Date(ms);
  if (to === "unix") return String(Math.floor(ms / 1000));
  if (to === "iso") return d.toISOString();
  return d.toLocaleString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    timeZoneName: "short",
  });
}

function handleTestRegex(args) {
  const re = new RegExp(args.pattern, args.flags || "g");
  const matches = [...args.text.matchAll(re)];
  if (!matches.length) return "No matches found.";
  const lines = matches.map((m, i) => {
    let line = `Match ${i + 1}: "${m[0]}" at index ${m.index}`;
    if (m.length > 1) {
      line += "\n  Groups: " + m.slice(1).map((g, j) => `$${j + 1}="${g}"`).join(", ");
    }
    return line;
  });
  return `Found ${matches.length} match(es):\n\n${lines.join("\n")}`;
}

function handleBuildCron(args) {
  const p = args.expression.trim().split(/\s+/);
  if (p.length < 5) throw new Error("Cron expression needs at least 5 fields");
  const labels = ["Minute", "Hour", "Day of month", "Month", "Day of week"];
  const explain = (val, label) => {
    if (val === "*") return `${label}: every ${label.toLowerCase()}`;
    if (val.includes("/")) return `${label}: every ${val.split("/")[1]} ${label.toLowerCase()}s`;
    if (val.includes(",")) return `${label}: at ${val}`;
    if (val.includes("-")) return `${label}: ${val}`;
    return `${label}: ${val}`;
  };
  const lines = p.slice(0, 5).map((v, i) => explain(v, labels[i]));
  return `Cron: ${args.expression}\n\n${lines.join("\n")}`;
}

function handleConvertEthUnits(args) {
  if (!args.value || Number.isNaN(Number(args.value))) throw new Error("Invalid number");
  const rates = { wei: 1n, gwei: 1_000_000_000n, eth: 1_000_000_000_000_000_000n };
  const fromRate = rates[args.from];
  const toRate = rates[args.to];
  if (!fromRate || !toRate) throw new Error("Unknown unit");
  // Use BigInt for integer inputs, float for decimals
  const hasDecimal = args.value.includes(".");
  let result;
  if (hasDecimal) {
    // Float path — acceptable for human-readable amounts
    const wei = parseFloat(args.value) * Number(fromRate);
    result = (wei / Number(toRate)).toString();
  } else {
    // BigInt path — exact for integer values
    const wei = BigInt(args.value) * fromRate;
    const whole = wei / toRate;
    const remainder = wei % toRate;
    if (remainder === 0n) {
      result = whole.toString();
    } else {
      // Format decimal from remainder
      const decimals = toRate.toString().length - 1;
      const fracStr = remainder.toString().padStart(decimals, "0").replace(/0+$/, "");
      result = `${whole}.${fracStr}`;
    }
  }
  return `${args.value} ${args.from.toUpperCase()} = ${result} ${args.to.toUpperCase()}`;
}

function handleValidateWallet(args) {
  const { address, chain } = args;
  if (chain === "eth") {
    const valid = /^0x[a-fA-F0-9]{40}$/.test(address);
    return valid
      ? `Valid ETH address (${address.slice(0, 6)}...${address.slice(-4)})`
      : "Invalid ETH address format. Must be 0x followed by 40 hex characters.";
  }
  if (chain === "btc") {
    const legacy = /^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$/.test(address);
    const bech32 = /^bc1[a-z0-9]{39,59}$/.test(address);
    const valid = legacy || bech32;
    return valid
      ? `Valid BTC address (${bech32 ? "Bech32" : "Legacy"}: ${address.slice(0, 8)}...${address.slice(-4)})`
      : "Invalid BTC address format.";
  }
  throw new Error(`Unsupported chain: ${chain}`);
}

function handleEncodeUrl(args) {
  return args.mode === "decode"
    ? decodeURIComponent(args.text)
    : encodeURIComponent(args.text);
}

// ── Catalog handlers ───────────────────────────────────────────────────

async function handleBrowse(args) {
  const catalog = await getCatalog();
  const products = catalog.products || [];

  // Group by shop
  const byShop = {};
  for (const p of products) {
    const shop = p.shop_name || "Unknown";
    if (args.shop && !shop.toLowerCase().includes(args.shop.toLowerCase())) continue;
    if (!byShop[shop]) byShop[shop] = [];
    byShop[shop].push(p);
  }

  const shopNames = Object.keys(byShop).sort();
  if (!shopNames.length) return `No shops matching "${args.shop}".`;

  const filteredCount = Object.values(byShop).reduce((s, arr) => s + arr.length, 0);
  const header = args.shop
    ? `Underground Cultural District — ${filteredCount} products in ${shopNames.length} matching shop(s)\n`
    : `Underground Cultural District — ${products.length} products across ${new Set(products.map((p) => p.shop_name)).size} shops\n`;
  const lines = [header];

  for (const shop of shopNames) {
    const items = byShop[shop];
    lines.push(`\n## ${shop} (${items.length})`);
    for (const p of items) {
      const price = p.purchase?.is_free ? "FREE" : `$${p.purchase?.price_usd ?? "?"}`;
      const summary = p.agent_summary || p.description || "";
      lines.push(`  ${p.id} — ${p.name} — ${price}`);
      if (summary) lines.push(`    ${summary.slice(0, 120)}`);
    }
  }

  return lines.join("\n");
}

async function handleSearch(args) {
  const catalog = await getCatalog();
  const products = catalog.products || [];
  const q = args.query.toLowerCase();

  const matches = products.filter((p) => {
    const hay = `${p.name} ${p.description} ${p.agent_summary || ""} ${p.shop_name} ${p.category || ""}`.toLowerCase();
    if (!hay.includes(q)) return false;
    if (args.category && p.category !== args.category) return false;
    if (args.price_max != null) {
      const price = p.purchase?.price_usd;
      if (price == null || price > args.price_max) return false;
    }
    return true;
  });

  if (!matches.length) return `No products found for "${args.query}".`;

  const lines = [`Found ${matches.length} result(s) for "${args.query}":\n`];
  for (const p of matches) {
    const price = p.purchase?.is_free ? "FREE" : `$${p.purchase?.price_usd ?? "?"}`;
    lines.push(`${p.id} — ${p.name} (${p.shop_name}) — ${price}`);
    lines.push(`  Category: ${p.category || "—"}`);
    lines.push(`  ${(p.agent_summary || p.description || "").slice(0, 150)}`);
    lines.push("");
  }

  return lines.join("\n");
}

async function handleBuy(args) {
  const catalog = await getCatalog();
  const products = catalog.products || [];
  const id = args.product_id.toLowerCase();

  // Exact ID match first
  let matches = products.filter((p) => p.id === args.product_id || p.id === id);

  // Fall back to name search if no exact match
  if (!matches.length) {
    matches = products.filter((p) => p.name.toLowerCase().includes(id));
  }

  if (!matches.length) return `Product "${args.product_id}" not found. Use search-underground to find products.`;

  if (matches.length > 1) {
    const list = matches.map((p) => `  ${p.id} — ${p.name} (${p.shop_name})`).join("\n");
    return `Multiple products match "${args.product_id}". Please use an exact product ID:\n\n${list}`;
  }

  const product = matches[0];

  const price = product.purchase?.is_free ? "FREE" : `$${product.purchase?.price_usd}`;
  const lines = [
    `${product.name}`,
    `Shop: ${product.shop_name}`,
    `Price: ${price}`,
    `Category: ${product.category || "—"}`,
    "",
    product.agent_summary || product.description || "",
  ];

  if (product.purchase?.is_free) {
    lines.push("", `Delivery (free): ${product.delivery?.delivery_url}`);
  } else {
    lines.push("", `── Payment Options ──`);
    lines.push("");
    lines.push(`Agent API (recommended): POST https://substratesymposium.com/api/create-payment`);
    lines.push(`  Body: { "product_id": "${product.id}" }`);
    lines.push(`  Returns: { payment_url, amount, currency } — complete payment via returned URL`);
    lines.push("");
    lines.push(`Browser checkout: ${product.purchase?.payment_url}`);
    lines.push("");
    lines.push(`Delivery URL (after payment): ${product.delivery?.delivery_url}`);
  }

  return lines.join("\n");
}

// ---------------------------------------------------------------------------
// Router
// ---------------------------------------------------------------------------

const HANDLERS = {
  "generate-uuid": handleGenerateUuid,
  "format-json": handleFormatJson,
  "encode-base64": handleEncodeBase64,
  "decode-base64": handleDecodeBase64,
  "generate-hash": handleGenerateHash,
  "generate-password": handleGeneratePassword,
  "decode-jwt": handleDecodeJwt,
  "convert-timestamp": handleConvertTimestamp,
  "test-regex": handleTestRegex,
  "build-cron": handleBuildCron,
  "convert-eth-units": handleConvertEthUnits,
  "validate-wallet": handleValidateWallet,
  "encode-url": handleEncodeUrl,
  "browse-underground": handleBrowse,
  "search-underground": handleSearch,
  "buy-from-underground": handleBuy,
};

// ---------------------------------------------------------------------------
// Server setup
// ---------------------------------------------------------------------------

const server = new Server(
  { name: "underground-cultural-district", version: "4.2.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: TOOLS }));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  const handler = HANDLERS[name];
  if (!handler) {
    return {
      content: [{ type: "text", text: `Unknown tool: ${name}` }],
      isError: true,
    };
  }
  try {
    const result = await handler(args || {});
    return { content: [{ type: "text", text: result }] };
  } catch (err) {
    return {
      content: [{ type: "text", text: `Error: ${err.message}` }],
      isError: true,
    };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
console.error("Underground MCP Server v4.1.0 running on stdio");
