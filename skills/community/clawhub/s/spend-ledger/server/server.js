#!/usr/bin/env node

import { createServer } from "node:http";
import {
  readFileSync,
  writeFileSync,
  existsSync,
  mkdirSync,
  appendFileSync,
} from "node:fs";
import { resolve, dirname } from "node:path";
import {
  appendTransaction,
  queryTransactions,
  summarize,
  groupBy,
  verifyChain,
  toCSV,
} from "./transactions.js";
import { SUGGESTIONS_PATH } from "./detectors.js";
import { syncPatterns, submitPattern, loadConfig } from "./patterns-sync.js";

const PORT = parseInt(process.env.SPEND_LEDGER_PORT || "18920", 10);
const HOST = "127.0.0.1";

const DASHBOARD_PATH = resolve(
  new URL("./index.html", import.meta.url).pathname
);

const SUBMISSIONS_PATH = resolve(
  process.env.SPEND_LEDGER_SUBMISSIONS ||
    new URL("../data/submissions.jsonl", import.meta.url).pathname
);

function parseQuery(url) {
  const u = new URL(url, "http://localhost");
  const params = {};
  for (const [k, v] of u.searchParams) params[k] = v;
  return { pathname: u.pathname, params };
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => resolve(Buffer.concat(chunks).toString()));
    req.on("error", reject);
  });
}

function json(res, data, status = 200) {
  const body = JSON.stringify(data);
  res.writeHead(status, {
    "Content-Type": "application/json",
    "Content-Length": Buffer.byteLength(body),
    // No CORS headers — this server binds to 127.0.0.1 only and has no
    // legitimate cross-origin callers. A wildcard would let any webpage read
    // transaction data from a running dashboard via cross-origin fetch.
  });
  res.end(body);
}

function html(res, content, status = 200) {
  res.writeHead(status, {
    "Content-Type": "text/html; charset=utf-8",
    "Content-Length": Buffer.byteLength(content),
  });
  res.end(content);
}

function csvResponse(res, content, filename) {
  res.writeHead(200, {
    "Content-Type": "text/csv",
    "Content-Disposition": `attachment; filename="${filename}"`,
    "Content-Length": Buffer.byteLength(content),
  });
  res.end(content);
}

function notFound(res) {
  json(res, { error: "not found" }, 404);
}

// --- Tracked tools persistence ---

function loadTrackedTools() {
  if (!existsSync(SUGGESTIONS_PATH)) return [];
  try {
    return JSON.parse(readFileSync(SUGGESTIONS_PATH, "utf-8"));
  } catch {
    return [];
  }
}

function saveTrackedTools(tools) {
  const dir = dirname(SUGGESTIONS_PATH);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  writeFileSync(SUGGESTIONS_PATH, JSON.stringify(tools, null, 2), { mode: 0o600 });
}

function appendSubmissionEntry(entry) {
  const dir = dirname(SUBMISSIONS_PATH);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  const line = JSON.stringify({
    ...entry,
    submitted_at: new Date().toISOString(),
  });
  appendFileSync(SUBMISSIONS_PATH, line + "\n", { mode: 0o600 });
}

// --- Server ---

const server = createServer(async (req, res) => {
  const { pathname, params } = parseQuery(req.url);

  try {
    // --- GET routes ---
    if (req.method === "GET") {
      if (pathname === "/" || pathname === "/index.html") {
        const dashboardHtml = readFileSync(DASHBOARD_PATH, "utf-8");
        html(res, dashboardHtml);
        return;
      }

      if (pathname === "/api/transactions") {
        const txns = queryTransactions({
          from: params.from,
          to: params.to,
          service: params.service,
          skill: params.skill,
          status: params.status,
          source: params.source,
        });
        json(res, { transactions: txns, count: txns.length });
        return;
      }

      if (/^\/api\/summary\/(daily|weekly|monthly)$/.test(pathname)) {
        const period = pathname.split("/").pop();
        const txns = queryTransactions({ from: params.from, to: params.to });
        json(res, summarize(txns, period));
        return;
      }

      if (pathname === "/api/summary/by-service") {
        const txns = queryTransactions({ from: params.from, to: params.to });
        json(res, { groups: groupBy(txns, "service") });
        return;
      }

      if (pathname === "/api/summary/by-skill") {
        const txns = queryTransactions({ from: params.from, to: params.to });
        json(res, { groups: groupBy(txns, "skill") });
        return;
      }

      if (pathname === "/api/summary/by-tool") {
        const txns = queryTransactions({ from: params.from, to: params.to });
        json(res, { groups: groupBy(txns, "tool") });
        return;
      }

      if (pathname === "/api/balance") {
        json(res, { balance: null, message: "Wallet balance integration not yet configured" });
        return;
      }

      if (pathname === "/api/verify") {
        json(res, verifyChain());
        return;
      }

      if (pathname === "/api/export") {
        const format = params.format || "csv";
        const txns = queryTransactions({ from: params.from, to: params.to });
        if (format === "json") {
          json(res, { transactions: txns });
        } else {
          const filename = `spend-ledger-${new Date().toISOString().slice(0, 10)}.csv`;
          csvResponse(res, toCSV(txns), filename);
        }
        return;
      }

      if (pathname === "/api/tracked-tools") {
        json(res, { tools: loadTrackedTools() });
        return;
      }
    }

    // --- POST routes ---
    if (req.method === "POST") {
      const body = await readBody(req);
      let data;
      try {
        data = JSON.parse(body);
      } catch {
        json(res, { error: "invalid JSON" }, 400);
        return;
      }

      // Manual transaction logging
      if (pathname === "/api/transactions") {
        if (!data.service?.name && !data.service?.url) {
          json(res, { error: "service.name or service.url required" }, 400);
          return;
        }
        data.source = "manual";
        const record = appendTransaction(data);
        if (!record) {
          json(res, { error: "duplicate transaction (same tx_hash or idempotency_key)" }, 409);
          return;
        }
        json(res, { transaction: record }, 201);
        return;
      }

      // Add a tracked tool pattern
      if (pathname === "/api/tracked-tools") {
        if (!data.tool_name_pattern) {
          json(res, { error: "tool_name_pattern required" }, 400);
          return;
        }
        const tools = loadTrackedTools();
        const existing = tools.find(
          (t) => t.tool_name_pattern === data.tool_name_pattern
        );
        if (existing) {
          json(res, { error: "pattern already tracked" }, 409);
          return;
        }

        const entry = {
          tool_name_pattern: data.tool_name_pattern,
          description: data.description || "",
          category: data.category || null,
          added_at: new Date().toISOString(),
        };

        tools.push(entry);
        saveTrackedTools(tools);

        // If user opted to share with maintainers, POST to the community API
        let submitted = false;
        if (data.send_to_maintainers) {
          appendSubmissionEntry({
            type: "tracked-tool-suggestion",
            tool_name_pattern: entry.tool_name_pattern,
            description: entry.description,
            category: entry.category,
          });
          submitted = await submitPattern({
            tool_name_pattern: entry.tool_name_pattern,
            description: entry.description,
            category: entry.category,
          });
        }

        json(res, { tool: entry, submitted }, 201);
        return;
      }
    }

    // --- DELETE routes ---
    if (req.method === "DELETE") {
      if (pathname.startsWith("/api/tracked-tools/")) {
        const pattern = decodeURIComponent(pathname.slice("/api/tracked-tools/".length));
        const tools = loadTrackedTools();
        const idx = tools.findIndex((t) => t.tool_name_pattern === pattern);
        if (idx === -1) {
          json(res, { error: "pattern not found" }, 404);
          return;
        }
        tools.splice(idx, 1);
        saveTrackedTools(tools);
        json(res, { removed: pattern });
        return;
      }
    }

    notFound(res);
  } catch (err) {
    console.error("Request error:", err);
    json(res, { error: "internal server error" }, 500);
  }
});

server.listen(PORT, HOST, () => {
  console.log(`spend-ledger dashboard running at http://${HOST}:${PORT}`);
});

// Sync community patterns on startup, then refresh every 24 hours.
// Download-only (no payment data sent). Disable with sync_community_patterns: false in data/config.json.
const _cfg = loadConfig();
if (_cfg.sync_community_patterns !== false) {
  syncPatterns();
  setInterval(syncPatterns, 24 * 60 * 60 * 1000);
}
