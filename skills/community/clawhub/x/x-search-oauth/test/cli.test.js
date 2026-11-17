import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, rmSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { formatSearchResult, loginDeviceCode, parseArgs, runSearch } from "../src/cli.js";

function tempAuthPath() {
  const dir = mkdtempSync(join(tmpdir(), "xso-test-"));
  return { dir, path: join(dir, "auth.json") };
}

test("parseArgs accepts compact direct search options", () => {
  const parsed = parseArgs(["--query", "OpenClaw xAI", "--handle", "openclaw,@grok", "--from-date", "2026-05-20", "--json"]);
  assert.equal(parsed.command, "search");
  assert.equal(parsed.query, "OpenClaw xAI");
  assert.deepEqual(parsed.allowedXHandles, ["openclaw", "grok"]);
  assert.equal(parsed.fromDate, "2026-05-20");
  assert.equal(parsed.json, true);
});

test("parseArgs accepts positional search query", () => {
  const parsed = parseArgs(["OpenClaw xAI", "--from-date", "2026-05-20"]);
  assert.equal(parsed.command, "search");
  assert.equal(parsed.query, "OpenClaw xAI");
  assert.equal(parsed.fromDate, "2026-05-20");
});

test("loginDeviceCode stores token response", async () => {
  const { dir, path } = tempAuthPath();
  const calls = [];
  const fetchImpl = async (url, init) => {
    assert.equal(init.redirect, "error");
    calls.push(String(url));
    if (String(url).includes(".well-known")) return json({ device_authorization_endpoint: "https://auth.x.ai/device", token_endpoint: "https://auth.x.ai/token" });
    if (String(url).endsWith("/device")) return json({ device_code: "dev", user_code: "USER-CODE", verification_uri: "https://auth.x.ai/activate", expires_in: 300, interval: 1 });
    return json({ access_token: "access", refresh_token: "refresh", expires_in: 3600 });
  };
  let output = "";
  const credential = await loginDeviceCode({ fetchImpl, stdout: { write: (text) => { output += text; } }, sleep: async () => {}, now: () => 1000, configPath: path });
  assert.equal(credential.accessToken, "access");
  assert.match(output, /USER-CODE/);
  assert.equal(calls.length, 3);
  rmSync(dir, { recursive: true, force: true });
});

test("runSearch calls xAI Responses API with x_search tool", async () => {
  const { dir, path } = tempAuthPath();
  const { writeFileSync } = await import("node:fs");
  writeFileSync(path, JSON.stringify({ accessToken: "access", refreshToken: "refresh", expires: 9999999999999, tokenEndpoint: "https://auth.x.ai/token" }));
  let requestBody;
  const fetchImpl = async (_url, init) => {
    assert.equal(init.redirect, "error");
    requestBody = JSON.parse(init.body);
    assert.equal(init.headers.Authorization, "Bearer access");
    return json({ output: [{ type: "message", content: [{ type: "output_text", text: "Observed result", annotations: [{ type: "url_citation", url: "https://x.com/openclaw/status/1" }] }] }] });
  };
  const result = await runSearch({ options: parseArgs(["--query", "OpenClaw xAI", "--handle", "openclaw"]), fetchImpl, now: () => 1000, configPath: path });
  assert.equal(requestBody.tools[0].type, "x_search");
  assert.deepEqual(requestBody.tools[0].allowed_x_handles, ["openclaw"]);
  assert.equal(result.content, "Observed result");
  assert.deepEqual(result.citations, ["https://x.com/openclaw/status/1"]);
  rmSync(dir, { recursive: true, force: true });
});

test("formatSearchResult prints content and citations", () => {
  const text = formatSearchResult({ query: "q", model: "m", tookMs: 10, content: "Body", citations: ["https://x.com/a/status/1"] }, { json: false, raw: false });
  assert.match(text, /# query: q \| model: m \| took: 10ms/);
  assert.match(text, /Body/);
  assert.match(text, /1\. https:\/\/x.com\/a\/status\/1/);
});

function json(body, ok = true, status = 200) {
  return { ok, status, statusText: ok ? "OK" : "ERR", json: async () => body };
}

test("legacy gateway credential flags are rejected", () => {
  for (const flag of ["--gateway-token", "--gateway-url"]) {
    assert.throws(() => parseArgs(["query", flag, "synthetic"]), /unknown option/);
  }
});

test("stored refresh endpoint cannot receive credentials outside xAI", async () => {
  const { dir, path } = tempAuthPath();
  const { writeFileSync } = await import("node:fs");
  try {
    for (const endpoint of ["https://example.invalid/token", "http://auth.x.ai/token", "https://auth.x.ai.evil.invalid/token", "https://user:pass@auth.x.ai/token"]) {
      writeFileSync(path, JSON.stringify({accessToken: "synthetic", refreshToken: "synthetic", expires: 1, tokenEndpoint: endpoint}));
      let calls = 0;
      await assert.rejects(runSearch({options: parseArgs(["query"]), fetchImpl: async () => { calls++; throw new Error("unexpected fetch"); }, now: () => 1000, configPath: path}), /untrusted/);
      assert.equal(calls, 0);
    }
  } finally { rmSync(dir, { recursive: true, force: true }); }
});
