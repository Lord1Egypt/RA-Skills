import test from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { setTimeout as delay } from "node:timers/promises";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SERVICE_PATH = path.resolve(__dirname, "..", "scripts", "vaibot-guard-service.mjs");
const POLICY_PATH = path.resolve(__dirname, "..", "references", "policy.default.json");

const PORT = 39200 + Math.floor(Math.random() * 2000);
const TOKEN = "test-guard-token";

const tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), "vaibot-guard-skill-"));
const logDir = path.join(tmpRoot, ".vaibot-guard");
fs.mkdirSync(logDir, { recursive: true });

const env = {
  ...process.env,
  VAIBOT_GUARD_HOST: "127.0.0.1",
  VAIBOT_GUARD_PORT: String(PORT),
  VAIBOT_GUARD_TOKEN: TOKEN,
  VAIBOT_POLICY_PATH: POLICY_PATH,
  VAIBOT_WORKSPACE: tmpRoot,
  VAIBOT_GUARD_LOG_DIR: logDir,
  VAIBOT_PROVE_MODE: "off",
};

const server = spawn(process.execPath, [SERVICE_PATH], {
  env,
  stdio: ["ignore", "pipe", "pipe"],
});

async function waitForHealth() {
  const url = `http://127.0.0.1:${PORT}/health`;
  for (let i = 0; i < 40; i++) {
    try {
      const res = await fetch(url);
      if (res.ok) return true;
    } catch {
      // ignore
    }
    await delay(100);
  }
  return false;
}

async function postJson(pathname, body) {
  const res = await fetch(`http://127.0.0.1:${PORT}${pathname}`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      authorization: `Bearer ${TOKEN}`,
    },
    body: JSON.stringify(body),
  });
  const data = await res.json().catch(() => ({}));
  return { status: res.status, data };
}

const ready = await waitForHealth();
assert.equal(ready, true, "guard service should start");

process.on("exit", () => {
  if (!server.killed) server.kill("SIGTERM");
});

test("/health responds ok", async () => {
  const res = await fetch(`http://127.0.0.1:${PORT}/health`);
  const data = await res.json();
  assert.equal(res.status, 200);
  assert.equal(data.ok, true);
});

test("/v1/decide/tool allows low-risk read", async () => {
  const payload = {
    sessionId: "test-session",
    toolName: "read",
    params: { path: "README.md" },
    workspaceDir: tmpRoot,
  };
  const { status, data } = await postJson("/v1/decide/tool", payload);
  assert.equal(status, 200);
  assert.equal(data.ok, true);
  assert.equal(data.decision.decision, "allow");
});

test("approval flow resolves and redeems", async () => {
  const payload = {
    sessionId: "test-session",
    toolName: "message.send",
    params: { text: "hello" },
    workspaceDir: tmpRoot,
  };
  const first = await postJson("/v1/decide/tool", payload);
  assert.equal(first.status, 200);
  assert.equal(first.data.decision.decision, "approve");
  const approvalId = first.data.decision.approvalId;
  assert.ok(approvalId);

  const list = await postJson("/v1/approvals/list", { sessionId: "test-session" });
  assert.equal(list.status, 200);
  assert.ok(Array.isArray(list.data.approvals));
  assert.ok(list.data.approvals.find((a) => a.approvalId === approvalId));

  const resolve = await postJson("/v1/approvals/resolve", { approvalId, action: "approve" });
  assert.equal(resolve.status, 200);
  assert.equal(resolve.data.status, "approved");

  const redeemed = await postJson("/v1/decide/tool", {
    ...payload,
    approval: { approvalId },
  });
  assert.equal(redeemed.status, 200);
  assert.equal(redeemed.data.decision.decision, "allow");
});

test("/v1/finalize/tool accepts result", async () => {
  const pre = await postJson("/v1/decide/tool", {
    sessionId: "test-session",
    toolName: "read",
    params: { path: "README.md" },
    workspaceDir: tmpRoot,
  });
  const runId = pre.data.runId;
  assert.ok(runId);

  const fin = await postJson("/v1/finalize/tool", {
    sessionId: "test-session",
    runId,
    result: { ok: true, durationMs: 10, result: { data: "ok" } },
  });
  assert.equal(fin.status, 200);
  assert.equal(fin.data.ok, true);
});

test.after(() => {
  if (!server.killed) server.kill("SIGTERM");
});
