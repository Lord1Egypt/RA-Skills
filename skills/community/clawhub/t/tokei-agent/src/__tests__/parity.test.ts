/** @jest-environment node */
// Pins the published surface of tokei-agent: the MCP initialize and tools/list
// replies, every tool's request mapping and result, and every CLI command's
// requests, stdout, stderr and exit code across valid and invalid input.
//
// The snapshots were recorded against the pre-manifest code (TOOL_SPECS in
// mcp.ts, COMMANDS in index.ts). A diff here means the published CLI or MCP
// surface changed. Update the snapshot only for a deliberate, released change.
import { createMcpSession, TOOLS } from "../mcp.js";
import { main } from "../index.js";
import type { Io } from "../index.js";
import type { HttpResponse } from "../http.js";

const RL = { "x-ratelimit-limit": "60", "x-ratelimit-remaining": "59", "x-ratelimit-reset": "1750000000" };

function res(body: unknown, status = 200): HttpResponse {
  return {
    status,
    headers: { get: (name: string) => RL[name.toLowerCase() as keyof typeof RL] ?? null },
    text: async () => JSON.stringify(body),
  };
}

interface Call {
  url: string;
  method: string;
  headers: Record<string, string>;
  body?: string;
}

function harness(opts: { env?: Record<string, string | undefined>; response?: HttpResponse } = {}) {
  const out: string[] = [];
  const err: string[] = [];
  const calls: Call[] = [];
  const response = opts.response ?? res({ ok: true, data: { id: "x" } });
  const io: Io = {
    env: opts.env ?? { TOKEI_API_KEY: "tokei_k_parity" },
    fetchImpl: async (url, init) => {
      calls.push({ url, method: init.method, headers: init.headers, body: init.body });
      return response;
    },
    stdout: (line) => out.push(line),
    stderr: (line) => err.push(line),
    readFile: (path) => {
      if (path === "body.json") return '{"title":"From file","prizes":[{"name":"P","winners":1}]}';
      throw new Error(`ENOENT: no such file, open '${path}'`);
    },
  };
  return { io, out, err, calls };
}

// ---------------------------------------------------------------------------
// MCP

async function rpcLine(io: Io, msg: unknown): Promise<string | undefined> {
  return createMcpSession(io).handleLine(JSON.stringify(msg));
}

function sampleFor(name: string, schema: Record<string, unknown>): unknown {
  if (Array.isArray(schema.enum)) return schema.enum[0];
  const type = Array.isArray(schema.type) ? schema.type[0] : schema.type;
  switch (type) {
    case "integer":
      return 7;
    case "boolean":
      return true;
    case "array": {
      const items = schema.items as Record<string, unknown> | undefined;
      return items && Array.isArray(items.enum) ? [items.enum[0]] : [{ name: "Item", winners: 1 }];
    }
    case "object":
      return { k: "v" };
    default:
      return name.endsWith("_id") ? "id/with space?" : `s_${name}`;
  }
}

function fullArgs(tool: (typeof TOOLS)[number]): Record<string, unknown> {
  const args: Record<string, unknown> = {};
  for (const [name, schema] of Object.entries(tool.inputSchema.properties)) {
    args[name] = sampleFor(name, schema as Record<string, unknown>);
  }
  return args;
}

describe("parity — MCP protocol surface", () => {
  it("initialize reply", async () => {
    const { io } = harness();
    expect(
      await rpcLine(io, {
        jsonrpc: "2.0",
        id: 1,
        method: "initialize",
        params: { protocolVersion: "2025-06-18", capabilities: {}, clientInfo: { name: "t", version: "1" } },
      }),
    ).toMatchSnapshot();
  });

  it("tools/list reply, byte for byte", async () => {
    const { io } = harness();
    expect(await rpcLine(io, { jsonrpc: "2.0", id: 2, method: "tools/list" })).toMatchSnapshot();
  });

  it("tool names in order", () => {
    expect(TOOLS.map((t) => t.name)).toMatchSnapshot();
  });
});

describe("parity — MCP tools/call", () => {
  const generic = TOOLS.filter((t) => t.name !== "media_upload");

  it.each(generic.map((t) => t.name))("%s", async (name) => {
    const tool = TOOLS.find((t) => t.name === name)!;
    const cases: Record<string, Record<string, unknown>> = {
      empty: {},
      full: fullArgs(tool),
      fullPlusUndeclared: { ...fullArgs(tool), zz_undeclared: 1, prizes: [] },
      nullsAndNumbers: Object.fromEntries(
        Object.keys(tool.inputSchema.properties).map((k, i) => [k, i % 2 === 0 ? 12345 : null]),
      ),
    };
    const record: Record<string, unknown> = {};
    for (const [label, args] of Object.entries(cases)) {
      const h = harness({
        response: res({ ok: true, data: { id: "w1", secret: "whsec_abc" } }, 201),
      });
      const reply = await rpcLine(h.io, {
        jsonrpc: "2.0",
        id: 3,
        method: "tools/call",
        params: { name, arguments: args },
      });
      record[label] = { calls: h.calls, reply };
    }

    const noKey = harness({ env: {} });
    record.noKey = {
      calls: noKey.calls,
      reply: await rpcLine(noKey.io, {
        jsonrpc: "2.0",
        id: 4,
        method: "tools/call",
        params: { name, arguments: fullArgs(tool) },
      }),
    };

    const apiError = harness({ response: res({ ok: false, error: { code: "NOT_FOUND" } }, 404) });
    record.apiError = await rpcLine(apiError.io, {
      jsonrpc: "2.0",
      id: 5,
      method: "tools/call",
      params: { name, arguments: fullArgs(tool) },
    });

    expect(record).toMatchSnapshot();
  });

  it("media_upload", async () => {
    const record: Record<string, unknown> = {};
    for (const [label, args] of Object.entries({
      empty: {},
      badExt: { file_path: "notes.txt" },
      noFs: { file_path: "hero.png" },
    })) {
      const h = harness();
      record[label] = await rpcLine(h.io, {
        jsonrpc: "2.0",
        id: 6,
        method: "tools/call",
        params: { name: "media_upload", arguments: args },
      });
    }

    const h = harness();
    h.io.readFileBytes = () => new Uint8Array(150).fill(3);
    h.io.binaryFetchImpl = async (url, init) => {
      // The multipart boundary is random, so the body length is not pinned.
      const filename = /filename="([^"]*)"/.exec(Buffer.from(init.body).toString("latin1"))?.[1];
      record.uploadRequest = { url, method: init.method, filename };
      return res({ success: true, data: { public_url: "https://media.tokei.io/x.png" } }, 201);
    };
    record.upload = await rpcLine(h.io, {
      jsonrpc: "2.0",
      id: 7,
      method: "tools/call",
      params: { name: "media_upload", arguments: { file_path: "dir/hero.png", extra: 1 } },
    });

    expect(record).toMatchSnapshot();
  });

  it("protocol errors", async () => {
    const { io } = harness();
    const lines = [
      "not json",
      "[]",
      JSON.stringify({ jsonrpc: "2.0", id: 1 }),
      JSON.stringify({ jsonrpc: "2.0", id: 1, method: "tools/call", params: { name: "nope" } }),
      JSON.stringify({ jsonrpc: "2.0", id: 1, method: "tools/call", params: { arguments: {} } }),
      JSON.stringify({ jsonrpc: "2.0", id: 1, method: "resources/list" }),
      JSON.stringify({ jsonrpc: "2.0", method: "notifications/initialized" }),
      JSON.stringify({ jsonrpc: "2.0", id: 1, method: "ping" }),
      JSON.stringify({ jsonrpc: "2.0", id: 1, method: "initialize", params: { protocolVersion: "1999-01-01" } }),
    ];
    const session = createMcpSession(io);
    const replies: (string | undefined)[] = [];
    for (const line of lines) replies.push(await session.handleLine(line));
    expect(replies).toMatchSnapshot();
  });
});

// ---------------------------------------------------------------------------
// CLI

const ID = "c 1/2";

const CLI_CASES: string[][] = [
  [],
  ["--help"],
  ["help"],
  ["--version"],
  ["-v"],
  ["nope"],
  ["me"],
  ["me", "--bogus", "x"],
  ["pages:list"],
  ["pages:list", "--status", "active", "--mode", "competition", "--page", "2", "--per-page", "50"],
  ["pages:list", "--per-page", "50", "--page", "2", "--mode", "gamification", "--status", "draft"],
  ["pages:list", "--status", "bad"],
  ["pages:list", "--mode", "bad"],
  ["pages:list", "--page", "0"],
  ["pages:list", "--page", "x"],
  ["pages:list", "--page", "-1"],
  ["pages:list", "--per-page", "101"],
  ["pages:list", "--per-page", "0"],
  ["pages:list", "--status"],
  ["pages:list", "--data", "{}"],
  ["pages:list", "--page", "x", "--status", "bad"],
  ["pages:get"],
  ["pages:get", ID],
  ["pages:get", ID, "--page", "1"],
  ["stats", ID],
  ["stats"],
  ["leaderboard", ID, "--page", "3", "--per-page", "10"],
  ["leaderboard"],
  ["referrals:top", ID, "--per-page", "100"],
  ["winners:list", ID],
  ["winners:list", ID, "--page", "1"],
  ["entries:list", ID, "--email", "a@b.co", "--page", "1", "--per-page", "5"],
  ["entries:list", ID, "--email"],
  ["surveys:list", ID, "--page", "2"],
  ["templates:list"],
  ["actions:catalog"],
  ["actions:catalog", "--type", "twitter_follow"],
  ["actions:catalog", "--type"],
  ["events:catalog", "--type=entry.created"],
  ["pages:clone"],
  ["pages:clone", "--title", "T"],
  [
    "pages:clone",
    "--title", "T",
    "--source", "src-1",
    "--template", "tpl",
    "--description", "D",
    "--prize", "P",
    "--end-date", "2030-01-01T00:00:00Z",
    "--campaign-url", "https://x.co",
    "--image-url", "https://media.tokei.io/a.png",
    "--status", "active",
    "--idempotency-key", "k1",
  ],
  ["pages:clone", "--title", "T", "--status", "completed"],
  ["pages:clone", "--title"],
  ["pages:clone", "--data", '{"title":"Data","extra":1}'],
  ["pages:clone", "--data", '{"title":"Data"}', "--title", "Flag"],
  ["pages:clone", "--data", "@body.json"],
  ["pages:clone", "--data", "@missing.json"],
  ["pages:clone", "--data", "not json"],
  ["pages:clone", "--data", "[1]"],
  ["pages:clone", "--data", "null"],
  ["pages:clone", "--data"],
  ["pages:clone", "--title", "T", "--source_promotion_id", "x"],
  ["pages:update", ID],
  ["pages:update"],
  [
    "pages:update", ID,
    "--title", "T",
    "--description", "D",
    "--start-date", "2030-01-01",
    "--end-date", "2030-02-01",
    "--template", "simple",
    "--custom-css", ".a{}",
    "--dark-mode", "true",
    "--primary-color", "#fff",
    "--card-width", "max-w-7xl",
    "--image-video", "u1",
    "--secondary-image", "u2",
    "--third-image", "u3",
    "--fourth-image", "u4",
    "--fifth-image", "u5",
    "--background-image", "u6",
    "--og-image", "u7",
  ],
  ["pages:update", ID, "--og-image", "u7", "--title", "T", "--dark-mode", "false", "--custom-css", "x"],
  ["pages:update", ID, "--dark-mode", "yes"],
  ["pages:update", ID, "--template", "classic"],
  ["pages:update", ID, "--card-width", "huge"],
  ["pages:update", ID, "--status", "active"],
  ["pages:update", ID, "--dark_mode_enabled", "true"],
  ["pages:update", ID, "--data", '{"prizes":[],"status":"active"}', "--title", "T"],
  ["pages:update", ID, "--data", "{}"],
  ["pages:update", ID, "--title", ""],
  ["pages:publish", ID],
  ["pages:publish"],
  ["pages:publish", ID, "--data", '{"end_date":"2030-01-01","status":"draft"}'],
  ["pages:publish", ID, "--end-date", "2030-01-01"],
  ["pages:unpublish", ID],
  ["pages:unpublish", ID, "--data", '{"prizes":[]}'],
  ["entries:create", ID],
  ["entries:create", ID, "--email", "a@b.co"],
  [
    "entries:create", ID,
    "--email", "a@b.co",
    "--name", "N",
    "--action-type", "api_import",
    "--points", "20000",
    "--value", "Order #1",
  ],
  ["entries:create", ID, "--email", "a@b.co", "--points", "1.5"],
  ["entries:create", ID, "--email", "a@b.co", "--marketing-consent", "true"],
  ["entries:create", ID, "--data", '{"email":"d@b.co","marketing_consent":true}'],
  ["entries:create"],
  ["webhooks:list", "--page", "1", "--per-page", "2"],
  ["webhooks:create"],
  ["webhooks:create", "--url", "https://h.co"],
  ["webhooks:create", "--url", "https://h.co", "--events", "entry.created, contest.ended,,"],
  ["webhooks:create", "--url", "https://h.co", "--events", " , "],
  ["webhooks:create", "--data", '{"url":"https://h.co","events":["entry.created"]}'],
  ["webhooks:delete", "wh/1"],
  ["webhooks:delete"],
  ["media:upload"],
  ["media:upload", "a.png", "--bogus", "x"],
  ["media:upload", "a.png", "--content-type"],
  ["media:upload", "a.txt"],
  ["media:upload", "a.png"],
  ["mcp"],
];

async function runCli(argv: string[], opts: Parameters<typeof harness>[0] = {}) {
  const h = harness(opts);
  const exit = await main(argv, h.io);
  return { exit, out: h.out, err: h.err, calls: h.calls };
}

describe("parity — CLI", () => {
  it.each(CLI_CASES.map((argv) => [argv.join(" ") || "(no args)", argv]))(
    "%s",
    async (_label, argv) => {
      expect(await runCli(argv as string[])).toMatchSnapshot();
    },
  );

  it("missing TOKEI_API_KEY", async () => {
    expect(await runCli(["me"], { env: {} })).toMatchSnapshot();
    expect(await runCli(["pages:update", ID, "--title", "T"], { env: {} })).toMatchSnapshot();
    expect(await runCli(["media:upload", "a.png"], { env: {} })).toMatchSnapshot();
  });

  it("TOKEI_API_URL override with a trailing slash", async () => {
    expect(
      await runCli(["pages:get", ID], { env: { TOKEI_API_KEY: "k", TOKEI_API_URL: "http://localhost:3000/" } }),
    ).toMatchSnapshot();
  });

  it("webhooks:create warns once about a whsec_ secret", async () => {
    expect(
      await runCli(["webhooks:create", "--url", "https://h.co", "--events", "entry.created"], {
        response: res({ ok: true, data: { id: "w1", secret: "whsec_abc" } }, 201),
      }),
    ).toMatchSnapshot();
  });

  it("API error passes through with exit 1", async () => {
    expect(
      await runCli(["pages:get", ID], { response: res({ ok: false, error: { code: "NOT_FOUND" } }, 404) }),
    ).toMatchSnapshot();
  });
});
