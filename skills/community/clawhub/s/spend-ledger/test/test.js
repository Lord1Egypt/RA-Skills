import { describe, it, before, after } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, rmSync, writeFileSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";

import {
  appendTransaction,
  readAllTransactions,
  queryTransactions,
  summarize,
  groupBy,
  verifyChain,
  toCSV,
  hashInput,
} from "../server/transactions.js";

import { detectPayment } from "../server/detectors.js";

describe("transactions", () => {
  let tmpDir;
  let logPath;

  before(() => {
    tmpDir = mkdtempSync(join(tmpdir(), "spend-ledger-test-"));
    logPath = join(tmpDir, "test.jsonl");
  });

  after(() => {
    rmSync(tmpDir, { recursive: true, force: true });
  });

  it("appends a transaction with hash chain and new fields", () => {
    const txn1 = appendTransaction(
      {
        service: { url: "https://api.example.com/data", name: "Example", category: "research" },
        amount: { value: "0.05", currency: "USDC", chain: "base" },
        tx_hash: "0xabc123",
        idempotency_key: "idem_001",
        context: {
          skill: "stock-research",
          tool_name: "agent-wallet-cli",
          input_hash: "deadbeef",
        },
        execution_time_ms: 450,
        failure_type: null,
        status: "confirmed",
        source: "auto",
      },
      logPath
    );

    assert.ok(txn1.id.startsWith("txn_"));
    assert.ok(txn1.timestamp);
    assert.equal(txn1.prev_hash, "sha256:genesis");
    assert.equal(txn1.amount.value, "0.05");
    assert.equal(txn1.idempotency_key, "idem_001");
    assert.equal(txn1.execution_time_ms, 450);
    assert.equal(txn1.failure_type, null);
    assert.equal(txn1.source, "auto");
    assert.equal(txn1.context.input_hash, "deadbeef");
  });

  it("chains hashes correctly", () => {
    const txn2 = appendTransaction(
      {
        service: { name: "AlphaClaw" },
        amount: { value: "0.10", currency: "USDC" },
      },
      logPath
    );

    assert.notEqual(txn2.prev_hash, "sha256:genesis");
    assert.ok(txn2.prev_hash.startsWith("sha256:"));
    assert.equal(txn2.source, "auto"); // default
  });

  it("deduplicates by tx_hash", () => {
    const dup = appendTransaction(
      {
        service: { name: "Duplicate" },
        amount: { value: "0.01" },
        tx_hash: "0xabc123", // same as txn1
      },
      logPath
    );
    assert.equal(dup, null);
  });

  it("deduplicates by idempotency_key", () => {
    const dup = appendTransaction(
      {
        service: { name: "Duplicate" },
        amount: { value: "0.01" },
        idempotency_key: "idem_001", // same as txn1
      },
      logPath
    );
    assert.equal(dup, null);
  });

  it("allows different tx_hash", () => {
    const txn3 = appendTransaction(
      {
        service: { name: "Different" },
        amount: { value: "0.02" },
        tx_hash: "0xunique999",
      },
      logPath
    );
    assert.ok(txn3);
    assert.equal(txn3.tx_hash, "0xunique999");
  });

  it("reads all transactions", () => {
    const all = readAllTransactions(logPath);
    assert.equal(all.length, 3); // txn1, txn2, txn3 (2 dups rejected)
  });

  it("queries with filters", () => {
    const byService = queryTransactions({ service: "alpha" }, logPath);
    assert.equal(byService.length, 1);

    const bySkill = queryTransactions({ skill: "stock" }, logPath);
    assert.equal(bySkill.length, 1);
  });

  it("queries by source", () => {
    appendTransaction(
      { service: { name: "Manual" }, amount: { value: "1.00" }, source: "manual" },
      logPath
    );
    const manual = queryTransactions({ source: "manual" }, logPath);
    assert.equal(manual.length, 1);
    assert.equal(manual[0].service.name, "Manual");
  });

  it("summarizes daily", () => {
    const all = readAllTransactions(logPath);
    const summary = summarize(all, "daily");
    assert.equal(summary.grand_count, 4);
    assert.ok(summary.grand_total > 0);
  });

  it("groups by service", () => {
    const all = readAllTransactions(logPath);
    const groups = groupBy(all, "service");
    assert.ok(groups.length >= 2);
    // Sorted by total desc
    assert.ok(groups[0].total >= groups[1].total);
  });

  it("verifies hash chain", () => {
    const result = verifyChain(logPath);
    assert.equal(result.valid, true);
    assert.equal(result.total, 4);
  });

  it("exports to CSV with new columns", () => {
    const all = readAllTransactions(logPath);
    const csv = toCSV(all);
    const lines = csv.split("\n");
    assert.ok(lines[0].includes("execution_time_ms"));
    assert.ok(lines[0].includes("failure_type"));
    assert.ok(lines[0].includes("source"));
  });

  it("handles empty log", () => {
    const emptyPath = join(tmpDir, "empty.jsonl");
    assert.deepEqual(readAllTransactions(emptyPath), []);
    assert.deepEqual(verifyChain(emptyPath), { valid: true, brokenAt: null, total: 0 });
  });

  it("hashInput produces consistent hashes", () => {
    const h1 = hashInput("test args");
    const h2 = hashInput("test args");
    const h3 = hashInput("different args");
    assert.equal(h1, h2);
    assert.notEqual(h1, h3);
  });

  it("hashInput handles objects", () => {
    const h = hashInput({ foo: "bar" });
    assert.ok(h.length === 64); // sha256 hex
  });
});

describe("detectors", () => {
  it("detects agent-wallet-cli x402", () => {
    const result = detectPayment(
      "agent-wallet-cli",
      "x402 POST https://api.stockdata.com/report/AAPL --max-amount 0.10",
      JSON.stringify({
        amount: "0.08",
        currency: "USDC",
        chain: "base",
        tx_hash: "0xdef456",
        status: "confirmed",
      })
    );

    assert.ok(result);
    assert.equal(result.tool_name, "agent-wallet-cli");
    assert.equal(result.amount.value, "0.08");
    assert.equal(result.service.url, "https://api.stockdata.com/report/AAPL");
    assert.equal(result.tx_hash, "0xdef456");
    assert.equal(result.failure_type, null);
  });

  it("detects v402", () => {
    const result = detectPayment(
      "v402-pay",
      "https://research.example.com/query",
      JSON.stringify({
        amount: "0.03",
        currency: "USDC",
        signature: "sig_abc",
      })
    );

    assert.ok(result);
    assert.equal(result.tool_name, "v402");
    assert.equal(result.amount.value, "0.03");
    assert.equal(result.tx_hash, "sig_abc");
  });

  it("detects generic x402 via response header", () => {
    const result = detectPayment(
      "some-http-tool",
      "GET https://paywalled.example.com/data",
      JSON.stringify({
        headers: { "X-PAYMENT-RESPONSE": "true" },
        x402: { amount: "0.01", tx_hash: "0x999" },
        amount: "0.01",
        tx_hash: "0x999",
      })
    );

    assert.ok(result);
    assert.equal(result.amount.value, "0.01");
  });

  it("returns null for non-payment tool calls", () => {
    const result = detectPayment(
      "read-file",
      "/home/user/document.txt",
      "file contents here"
    );
    assert.equal(result, null);
  });

  it("detects payment-skill", () => {
    const result = detectPayment(
      "payment-skill",
      "pay https://service.example.com/api",
      JSON.stringify({
        amount: "0.25",
        hash: "0xpay123",
      })
    );

    assert.ok(result);
    assert.equal(result.tool_name, "payment-skill");
    assert.equal(result.amount.value, "0.25");
  });

  it("detects heuristic: stripe tool name", () => {
    const result = detectPayment(
      "stripe_create_charge",
      JSON.stringify({ amount: 1299, currency: "usd", recipient: "shop@example.com" }),
      JSON.stringify({
        status: "succeeded",
        amount: "12.99",
        currency: "USD",
        tx_hash: "ch_1ABC123def456ghi789jkl",
      })
    );

    assert.ok(result);
    assert.equal(result._detector, "heuristic");
    assert.equal(result.amount.value, "12.99");
  });

  it("detects heuristic: payment args + result confirmation", () => {
    const result = detectPayment(
      "custom-api-tool",
      JSON.stringify({ amount: 5.00, currency: "USD", recipient: "vendor@example.com" }),
      JSON.stringify({
        status: "completed",
        amount: "5.00",
        currency: "USD",
        hash: "0xaaa111bbb222",
      })
    );

    assert.ok(result);
    assert.equal(result._detector, "heuristic");
    assert.equal(result.amount.value, "5.00");
  });

  it("heuristic avoids false positive: price lookup without payment", () => {
    const result = detectPayment(
      "price-lookup",
      JSON.stringify({ symbol: "AAPL" }),
      JSON.stringify({ price: "150.25", currency: "USD" })
    );

    // Should NOT match — no payment tool name, no payment args pattern
    assert.equal(result, null);
  });

  it("detects failure_type: post_payment", () => {
    const result = detectPayment(
      "agent-wallet-cli",
      "x402 POST https://api.example.com/data",
      JSON.stringify({
        status: "failed",
        tx_hash: "0xfailed_but_paid",
        amount: "0.10",
      })
    );

    assert.ok(result);
    assert.equal(result.status, "failed");
    assert.equal(result.failure_type, "post_payment");
  });

  it("detects failure_type: pre_payment", () => {
    const result = detectPayment(
      "agent-wallet-cli",
      "x402 POST https://api.example.com/data",
      JSON.stringify({
        status: "error",
        error: "insufficient funds",
      })
    );

    assert.ok(result);
    assert.equal(result.status, "failed");
    assert.equal(result.failure_type, "pre_payment");
  });

  it("extracts idempotency_key", () => {
    const result = detectPayment(
      "v402-pay",
      "https://api.example.com/data",
      JSON.stringify({
        amount: "0.05",
        idempotency_key: "req_unique_123",
        signature: "sig_xyz",
      })
    );

    assert.ok(result);
    assert.equal(result.idempotency_key, "req_unique_123");
  });
});

describe("server API", () => {
  let serverProcess;
  let tmpDir;
  const port = 18921; // Use different port for tests

  before(async () => {
    tmpDir = mkdtempSync(join(tmpdir(), "spend-ledger-server-test-"));
    // Start server with custom port and log path
    const { spawn } = await import("node:child_process");
    serverProcess = spawn("node", ["server/server.js"], {
      cwd: join(import.meta.url.replace("file://", ""), "../../"),
      env: {
        ...process.env,
        SPEND_LEDGER_PORT: String(port),
        SPEND_LEDGER_LOG: join(tmpDir, "txns.jsonl"),
        SPEND_LEDGER_SUGGESTIONS: join(tmpDir, "tracked.json"),
        SPEND_LEDGER_SUBMISSIONS: join(tmpDir, "submissions.jsonl"),
      },
    });
    // Wait for server to start
    await new Promise((r) => setTimeout(r, 500));
  });

  after(() => {
    if (serverProcess) serverProcess.kill();
    rmSync(tmpDir, { recursive: true, force: true });
  });

  it("POST /api/transactions logs a manual transaction", async () => {
    const res = await fetch(`http://127.0.0.1:${port}/api/transactions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        service: { name: "TestService", url: "https://test.example.com" },
        amount: { value: "1.50", currency: "USDC", chain: "base" },
        tx_hash: "0xmanual123",
      }),
    });
    assert.equal(res.status, 201);
    const data = await res.json();
    assert.equal(data.transaction.source, "manual");
    assert.equal(data.transaction.amount.value, "1.50");
  });

  it("POST /api/transactions rejects duplicate tx_hash", async () => {
    const res = await fetch(`http://127.0.0.1:${port}/api/transactions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        service: { name: "Dup" },
        amount: { value: "0.01" },
        tx_hash: "0xmanual123",
      }),
    });
    assert.equal(res.status, 409);
  });

  it("GET /api/transactions returns logged transactions", async () => {
    const res = await fetch(`http://127.0.0.1:${port}/api/transactions`);
    const data = await res.json();
    assert.equal(data.count, 1);
    assert.equal(data.transactions[0].service.name, "TestService");
  });

  it("POST /api/tracked-tools adds a pattern", async () => {
    const res = await fetch(`http://127.0.0.1:${port}/api/tracked-tools`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        tool_name_pattern: "my_custom_pay.*",
        description: "Custom payment tool",
        send_to_maintainers: true,
      }),
    });
    assert.equal(res.status, 201);
    const data = await res.json();
    assert.equal(data.submitted, true);
  });

  it("GET /api/tracked-tools lists patterns", async () => {
    const res = await fetch(`http://127.0.0.1:${port}/api/tracked-tools`);
    const data = await res.json();
    assert.equal(data.tools.length, 1);
    assert.equal(data.tools[0].tool_name_pattern, "my_custom_pay.*");
  });

  it("DELETE /api/tracked-tools/:pattern removes a pattern", async () => {
    const res = await fetch(
      `http://127.0.0.1:${port}/api/tracked-tools/${encodeURIComponent("my_custom_pay.*")}`,
      { method: "DELETE" }
    );
    assert.equal(res.status, 200);

    const listRes = await fetch(`http://127.0.0.1:${port}/api/tracked-tools`);
    const data = await listRes.json();
    assert.equal(data.tools.length, 0);
  });
});
