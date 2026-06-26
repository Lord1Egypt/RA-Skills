import assert from "node:assert/strict";
import { fork } from "node:child_process";
import { once } from "node:events";
import { createServer, type IncomingMessage, type ServerResponse } from "node:http";
import { AddressInfo } from "node:net";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

type StartedServer = {
  server: ReturnType<typeof createServer>;
  url: string;
};

type SpawnedApp = import("node:child_process").ChildProcess;
type ToolTextContent = { type: "text"; text: string };

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

async function startServer(
  handler: (req: IncomingMessage, res: ServerResponse<IncomingMessage>) => void,
): Promise<StartedServer> {
  const server = createServer(handler);
  server.listen(0, "127.0.0.1");
  await once(server, "listening");
  const address = server.address() as AddressInfo;
  return { server, url: `http://127.0.0.1:${address.port}` };
}

async function stopServer(server: ReturnType<typeof createServer>) {
  server.close();
  await once(server, "close");
}

async function waitForAppReady(process: SpawnedApp): Promise<void> {
  let stderr = "";
  process.stderr?.setEncoding("utf8");
  await new Promise<void>((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error(`Timed out waiting for app startup.\nstderr:\n${stderr}`)), 15000);
    const onStderr = (chunk: string) => {
      stderr += chunk;
      if (stderr.includes("videomp3word-mcp listening on")) {
        cleanup();
        resolve();
      }
    };
    const onExit = (code: number | null, signal: NodeJS.Signals | null) => {
      cleanup();
      reject(new Error(`App exited before startup. code=${code} signal=${signal}\nstderr:\n${stderr}`));
    };
    const cleanup = () => {
      clearTimeout(timeout);
      process.stderr?.off("data", onStderr);
      process.off("exit", onExit);
    };
    process.stderr?.on("data", onStderr);
    process.on("exit", onExit);
  });
}

async function stopProcess(process: SpawnedApp) {
  if (process.exitCode !== null || process.killed) return;
  process.kill("SIGTERM");
  await once(process, "exit");
}

function createClient(baseUrl: string, headers?: HeadersInit) {
  const transport = new StreamableHTTPClientTransport(new URL("/mcp", baseUrl), {
    requestInit: headers ? { headers } : undefined,
  });
  const client = new Client({ name: "smoke-test-client", version: "1.0.0" }, { capabilities: {} });
  return { client, transport };
}

function getToolText(result: unknown): string {
  assert.ok(result && typeof result === "object");
  const content = (result as { content?: unknown }).content;
  assert.ok(Array.isArray(content));
  const textItem = content.find((item): item is ToolTextContent => {
    if (!item || typeof item !== "object") return false;
    const textContent = item as Partial<ToolTextContent>;
    return textContent.type === "text" && typeof textContent.text === "string";
  });
  assert.ok(textItem);
  return textItem.text;
}

test("structured knowledge endpoint and MCP tool work end-to-end", async () => {
  const accessKey = "smoke-access-key";
  const sessionCookie = "session=smoke-cookie";
  let upstreamCalls = 0;

  const upstream = await startServer(async (req, res) => {
    const url = new URL(req.url || "/", "http://127.0.0.1");
    if ((url.pathname === "/api/video2word" || url.pathname === "/api/mp32word") && req.method === "POST") {
      upstreamCalls += 1;
      assert.equal(req.headers.cookie, sessionCookie);
      res.setHeader("content-type", "application/x-ndjson");
      res.write(`${JSON.stringify({ type: "stdout", data: "Alice will send the roadmap by next Friday. The team discussed AI workflows, semantic chunking, and action items." })}\n`);
      res.end(`${JSON.stringify({ type: "exit", code: 0 })}\n`);
      return;
    }
    res.statusCode = 404;
    res.end("not found");
  });

  const appServer = createServer();
  appServer.listen(0, "127.0.0.1");
  await once(appServer, "listening");
  const appAddress = appServer.address() as AddressInfo;
  const appPort = appAddress.port;
  await stopServer(appServer);

  const baseUrl = `http://127.0.0.1:${appPort}`;
  const app = fork("dist/index.js", [], {
    cwd: repoRoot,
    env: {
      HOST: "127.0.0.1",
      PORT: String(appPort),
      PUBLIC_BASE_URL: baseUrl,
      VIDEOMP3WORD_BASE_URL: upstream.url,
      VIDEOMP3WORD_ALLOWED_UPSTREAM_HOSTS: "127.0.0.1",
      VIDEOMP3WORD_SESSION_COOKIE: sessionCookie,
      MCP_ACCESS_KEYS: accessKey,
    },
    stdio: ["ignore", "pipe", "pipe", "ipc"],
  });

  try {
    await waitForAppReady(app);

    const healthResponse = await fetch(`${baseUrl}/health`);
    assert.equal(healthResponse.status, 200);
    const healthJson = await healthResponse.json() as { ok: boolean; name: string; auth_required: boolean };
    assert.equal(healthJson.ok, true);
    assert.equal(healthJson.name, "videomp3word-mcp");
    assert.equal(healthJson.auth_required, true);

    const unauthorizedResponse = await fetch(`${baseUrl}/video_to_knowledge`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ media_url: "https://example.com/demo.mp4", outputs: ["summary"], mode: "balanced" }),
    });
    assert.equal(unauthorizedResponse.status, 401);

    const endpointResponse = await fetch(`${baseUrl}/video_to_knowledge`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        authorization: `Bearer ${accessKey}`,
      },
      body: JSON.stringify({
        media_url: "https://example.com/demo.mp4",
        outputs: ["summary", "qa", "flashcards", "tasks", "topics"],
        mode: "balanced",
        export_formats: ["json", "markdown", "notion"],
      }),
    });
    assert.equal(endpointResponse.status, 200);
    const endpointJson = await endpointResponse.json() as {
      summary: string;
      topics: string[];
      action_items: Array<{ owner: string }>;
      qa_pairs: Array<{ question: string }>;
      flashcards: Array<{ front: string }>;
      trace: { steps: Array<{ step: string; cached: boolean }>; models_used: string[] };
      exports: Record<string, unknown>;
    };
    assert.match(endpointJson.summary, /roadmap|semantic chunking|AI workflows/i);
    assert.ok(endpointJson.topics.length > 0);
    assert.ok(endpointJson.action_items.length > 0);
    assert.ok(endpointJson.qa_pairs.length > 0);
    assert.ok(endpointJson.flashcards.length > 0);
    assert.equal(typeof endpointJson.exports.json, "string");
    assert.equal(typeof endpointJson.exports.markdown, "string");
    assert.ok(Array.isArray((endpointJson.exports.notion as { blocks?: unknown[] }).blocks));
    assert.deepEqual(endpointJson.trace.steps.map((step) => step.step), [
      "ingest_media",
      "transcribe_media",
      "segment_transcript",
      "extract_semantics",
      "generate_knowledge",
      "evaluate_knowledge",
    ]);

    const cachedResponse = await fetch(`${baseUrl}/video_to_knowledge`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        authorization: `Bearer ${accessKey}`,
      },
      body: JSON.stringify({
        media_url: "https://example.com/demo.mp4",
        outputs: ["summary", "qa", "flashcards", "tasks", "topics"],
        mode: "balanced",
      }),
    });
    assert.equal(cachedResponse.status, 200);
    const cachedJson = await cachedResponse.json() as { trace: { steps: Array<{ step: string; cached: boolean }> } };
    assert.equal(cachedJson.trace.steps[0]?.cached, true);
    assert.equal(cachedJson.trace.steps[1]?.cached, true);
    assert.equal(upstreamCalls, 1);

    const authorizedAccess = createClient(baseUrl, { Authorization: `Bearer ${accessKey}` });
    await authorizedAccess.client.connect(authorizedAccess.transport);
    const toolResult = await authorizedAccess.client.callTool({
      name: "video_to_knowledge",
      arguments: {
        media_url: "https://example.com/demo.mp4",
        outputs: ["summary", "topics"],
        mode: "fast",
      },
    });
    const toolPayload = JSON.parse(getToolText(toolResult)) as { summary: string; topics: string[]; trace: { resource_ids: { knowledge_unit_id: string } } };
    assert.ok(toolPayload.summary.length > 0);
    assert.ok(toolPayload.topics.length > 0);
    assert.ok(toolPayload.trace.resource_ids.knowledge_unit_id.length > 0);
    await authorizedAccess.transport.close();
  } finally {
    await stopProcess(app);
    await stopServer(upstream.server);
  }
});

test("startup fails without required session cookie", async () => {
  const app = fork("dist/index.js", [], {
    cwd: repoRoot,
    env: {
      HOST: "127.0.0.1",
      PORT: "0",
      MCP_ACCESS_KEYS: "smoke-access-key",
    },
    stdio: ["ignore", "pipe", "pipe", "ipc"],
  });

  let stderr = "";
  app.stderr?.setEncoding("utf8");
  app.stderr?.on("data", (chunk: string) => {
    stderr += chunk;
  });

  const [code, signal] = (await once(app, "exit")) as [number | null, NodeJS.Signals | null];
  assert.notEqual(code, 0);
  assert.equal(signal, null);
  assert.match(stderr, /VIDEOMP3WORD_SESSION_COOKIE is required/i);
});

test("startup fails when upstream base URL uses insecure remote http", async () => {
  const app = fork("dist/index.js", [], {
    cwd: repoRoot,
    env: {
      HOST: "127.0.0.1",
      PORT: "0",
      VIDEOMP3WORD_BASE_URL: "http://videomp3word.com",
      VIDEOMP3WORD_SESSION_COOKIE: "session=smoke-cookie",
      MCP_ACCESS_KEYS: "smoke-access-key",
    },
    stdio: ["ignore", "pipe", "pipe", "ipc"],
  });

  let stderr = "";
  app.stderr?.setEncoding("utf8");
  app.stderr?.on("data", (chunk: string) => {
    stderr += chunk;
  });

  const [code, signal] = (await once(app, "exit")) as [number | null, NodeJS.Signals | null];
  assert.notEqual(code, 0);
  assert.equal(signal, null);
  assert.match(stderr, /VIDEOMP3WORD_BASE_URL must use https outside local development/i);
});
