/** @jest-environment node */
import { createMcpSession, TOOLS } from "../mcp.js";
import { main, VERSION } from "../index.js";
import type { Io } from "../index.js";
import type { HttpResponse } from "../http.js";

const RL_HEADERS = {
  "X-RateLimit-Limit": "60",
  "X-RateLimit-Remaining": "59",
  "X-RateLimit-Reset": "1750000000",
};

function jsonRes(body: unknown, status = 200): HttpResponse {
  const lower: Record<string, string> = {};
  for (const [k, v] of Object.entries(RL_HEADERS)) lower[k.toLowerCase()] = v;
  return {
    status,
    headers: { get: (name: string) => lower[name.toLowerCase()] ?? null },
    text: async () => JSON.stringify(body),
  };
}

interface Harness {
  io: Io;
  out: string[];
  err: string[];
  calls: { url: string; init: { method: string; headers: Record<string, string>; body?: string } }[];
}

function harness(
  opts: {
    env?: Record<string, string | undefined>;
    response?: HttpResponse | Error;
    stdin?: AsyncIterable<string>;
  } = {},
): Harness {
  const out: string[] = [];
  const err: string[] = [];
  const calls: Harness["calls"] = [];
  const response = opts.response ?? jsonRes({ ok: true });
  const base = {
    env: opts.env ?? { TOKEI_API_KEY: "k" },
    fetchImpl: async (url: string, init: { method: string; headers: Record<string, string>; body?: string }) => {
      calls.push({ url, init });
      if (response instanceof Error) throw response;
      return response;
    },
    stdout: (line: string) => out.push(line),
    stderr: (line: string) => err.push(line),
    ...(opts.stdin ? { stdin: opts.stdin } : {}),
  };
  const io: Io = base as Io;
  return { io, out, err, calls };
}

type McpSession = ReturnType<typeof createMcpSession>;

// Suggested by the spec: JSON-RPC round trip that returns the parsed
// response, or undefined when no response is due.
async function rpc(session: McpSession, msg: unknown): Promise<any> {
  const out = await session.handleLine(JSON.stringify(msg));
  return out === undefined ? undefined : JSON.parse(out);
}

const INITIALIZE_PARAMS = {
  protocolVersion: "2025-06-18",
  capabilities: {},
  clientInfo: { name: "t", version: "1" },
};

describe("createMcpSession — lifecycle / protocol", () => {
  it("initialize echoes a supported protocol version", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    const res = await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "initialize",
      params: INITIALIZE_PARAMS,
    });
    expect(res.jsonrpc).toBe("2.0");
    expect(res.id).toBe(1);
    expect(res.result.protocolVersion).toBe("2025-06-18");
    expect(typeof res.result.capabilities.tools).toBe("object");
    expect(res.result.serverInfo.name).toBe("tokei-agent");
    expect(res.result.serverInfo.version).toBe(VERSION);
    expect(typeof res.result.instructions).toBe("string");
    expect(res.result.instructions.length).toBeGreaterThan(0);
  });

  it('initialize echoes "2024-11-05" when the client sends that version', async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    const res = await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "initialize",
      params: { ...INITIALIZE_PARAMS, protocolVersion: "2024-11-05" },
    });
    expect(res.result.protocolVersion).toBe("2024-11-05");
  });

  it('initialize falls back to "2025-06-18" for an unknown protocolVersion', async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    const res = await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "initialize",
      params: { ...INITIALIZE_PARAMS, protocolVersion: "1999-01-01" },
    });
    expect(res.result.protocolVersion).toBe("2025-06-18");
  });

  it("notifications/initialized gets no response", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    const out = await session.handleLine(
      JSON.stringify({ jsonrpc: "2.0", method: "notifications/initialized" }),
    );
    expect(out).toBeUndefined();
  });

  it("ping returns an empty object result", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    const res = await rpc(session, { jsonrpc: "2.0", id: 2, method: "ping" });
    expect(res).toEqual({ jsonrpc: "2.0", id: 2, result: {} });
  });

  it("unknown method with an id -> JSON-RPC error -32601", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    const res = await rpc(session, { jsonrpc: "2.0", id: 3, method: "bogus/method" });
    expect(res.error.code).toBe(-32601);
    expect(res.id).toBe(3);
  });

  it("unparseable line -> JSON-RPC error -32700 with id: null", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    const out = await session.handleLine("not json{{{");
    expect(out).not.toBeUndefined();
    const res = JSON.parse(out!);
    expect(res.error.code).toBe(-32700);
    expect(res.id).toBeNull();
  });
});

describe("createMcpSession — tools/list", () => {
  it("lists exactly the 21 tools", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    const res = await rpc(session, { jsonrpc: "2.0", id: 1, method: "tools/list" });
    const names = res.result.tools.map((t: any) => t.name).sort();
    expect(names).toEqual(
      [
        "me",
        "pages_list",
        "pages_get",
        "stats",
        "leaderboard",
        "referrals_top",
        "winners_list",
        "entries_list",
        "surveys_list",
        "templates_list",
        "actions_catalog",
        "events_catalog",
        "pages_clone",
        "pages_update",
        "pages_publish",
        "pages_unpublish",
        "entries_create",
        "webhooks_list",
        "webhooks_create",
        "webhooks_delete",
        "media_upload",
      ].sort(),
    );
    for (const tool of res.result.tools as any[]) {
      expect(typeof tool.description).toBe("string");
      expect(tool.description.length).toBeGreaterThan(0);
      expect(tool.inputSchema.type).toBe("object");
    }
  });

  it("every tool has a title and readOnlyHint/destructiveHint annotations (Connectors Directory requirement)", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    const res = await rpc(session, { jsonrpc: "2.0", id: 1, method: "tools/list" });
    for (const tool of res.result.tools as any[]) {
      expect(typeof tool.title).toBe("string");
      expect(tool.title.length).toBeGreaterThan(0);
      expect(typeof tool.annotations?.readOnlyHint).toBe("boolean");
      if (tool.annotations.readOnlyHint === false) {
        expect(typeof tool.annotations.destructiveHint).toBe("boolean");
      }
    }
  });

  // T3b (0.3.5). Deleting a subscription CASCADEs its webhook_deliveries rows
  // (20260611_webhook_delivery_queue.sql:20), and repeating the delete is a
  // harmless 404 — both facts belong in the annotation surface.
  it("webhooks_delete declares idempotentHint and names the delivery cascade", () => {
    const tool = TOOLS.find((t) => t.name === "webhooks_delete")!;
    expect(tool.annotations).toMatchObject({
      readOnlyHint: false,
      destructiveHint: true,
      idempotentHint: true,
    });
    expect(tool.description).toContain("webhook_deliveries");
  });

  // T3c (0.3.5). Tool text describes what the API does; it does not instruct the
  // agent how to behave (Connectors Directory review point).
  it("tool text stays declarative rather than instructing the agent", () => {
    const unpublish = TOOLS.find((t) => t.name === "pages_unpublish")!;
    expect(unpublish.description).not.toContain("Tell your user");
    for (const tool of TOOLS) {
      expect(tool.description).not.toMatch(/slow down/i);
    }
  });

  it("required fields are declared on the relevant tools", () => {
    const byName = (name: string) => TOOLS.find((t) => t.name === name)!;
    expect(byName("pages_get").inputSchema.required).toEqual(["contest_id"]);
    expect(byName("pages_clone").inputSchema.required).toEqual(["title"]);
    expect(byName("webhooks_create").inputSchema.required).toEqual(["url", "events"]);
    expect(byName("entries_create").inputSchema.required).toEqual(["contest_id", "email"]);
    expect(byName("pages_publish").inputSchema.required).toEqual(["contest_id"]);
    expect(byName("pages_unpublish").inputSchema.required).toEqual(["contest_id"]);
    expect(byName("media_upload").inputSchema.required).toEqual(["file_path"]);
    const meRequired = byName("me").inputSchema.required;
    expect(meRequired === undefined || meRequired.length === 0).toBe(true);
    const templatesListRequired = byName("templates_list").inputSchema.required;
    expect(templatesListRequired === undefined || templatesListRequired.length === 0).toBe(true);
    const actionsCatalogRequired = byName("actions_catalog").inputSchema.required;
    expect(actionsCatalogRequired === undefined || actionsCatalogRequired.length === 0).toBe(true);
    const eventsCatalogRequired = byName("events_catalog").inputSchema.required;
    expect(eventsCatalogRequired === undefined || eventsCatalogRequired.length === 0).toBe(true);
    expect(byName("winners_list").inputSchema.required).toEqual(["contest_id"]);
  });

  it("pages_clone advertises a template input (alternative to source_promotion_id)", () => {
    const tool = TOOLS.find((t) => t.name === "pages_clone")!;
    const props = tool.inputSchema.properties as Record<string, any>;
    expect(props.template).toBeDefined();
    expect(props.template.type).toBe("string");
    expect(typeof props.template.description).toBe("string");
    // title is still the only required field — template is optional.
    expect(tool.inputSchema.required).toEqual(["title"]);
  });

  it("pages_update advertises template, dark_mode_enabled, primary_color, and card_width", () => {
    const tool = TOOLS.find((t) => t.name === "pages_update")!;
    const props = tool.inputSchema.properties as Record<string, any>;

    expect(props.template).toBeDefined();
    expect(props.template.enum).toEqual(["basic-new", "showcase", "future", "simple"]);

    expect(props.dark_mode_enabled).toBeDefined();
    expect(props.dark_mode_enabled.type).toBe("boolean");

    expect(props.primary_color).toBeDefined();
    expect(typeof props.primary_color.description).toBe("string");

    expect(props.card_width).toBeDefined();
    expect(props.card_width.enum).toEqual([
      "narrow",
      "medium",
      "wide",
      "xl",
      "max-w-2xl",
      "max-w-3xl",
      "max-w-4xl",
      "max-w-7xl",
    ]);

    // contest_id stays the only required field — the new fields are optional.
    expect(tool.inputSchema.required).toEqual(["contest_id"]);
  });

  it("pages_update advertises entry_methods, including the custom-link row shape", () => {
    // Since 0.3.5 callTool allowlists args against inputSchema.properties, so an
    // undeclared field is DROPPED rather than forwarded — which makes the
    // advertised schema the only way an agent can send entry_methods at all.
    // The custom-link row (no actionType) is the one shape actions_catalog
    // cannot describe, so the description has to carry it.
    const tool = TOOLS.find((t) => t.name === "pages_update")!;
    const props = tool.inputSchema.properties as Record<string, any>;

    expect(props.entry_methods).toBeDefined();
    expect(props.entry_methods.type).toBe("array");
    expect(props.entry_methods.maxItems).toBe(30);
    expect(props.entry_methods.description).toContain("actionType");
    expect(props.entry_methods.description).toContain("link");
    expect(props.entry_methods.description).toContain("actionsRequired");
    expect(tool.description).toContain("entry_methods");
  });

  // Outstanding item 2 of the API wave. marketing_consent is documented public-API
  // surface (docs/using-custom-apis.md) and is accepted by createEntrySchema, but
  // it was never declared here — so 0.3.5's allowlist began silently dropping it.
  // It is not an audit field: marketing-sync-queue.service.ts gates ESP sync on
  // `marketing_consent !== true`, so dropping it means an agent can import 500
  // consented entrants, get 201 on every one, and sync none of them.
  it("entries_create declares marketing_consent, which gates ESP sync", () => {
    const tool = TOOLS.find((t) => t.name === "entries_create")!;
    const props = tool.inputSchema.properties as Record<string, any>;

    expect(props.marketing_consent).toBeDefined();
    expect(props.marketing_consent.type).toBe("boolean");
    // The tool cannot verify consent, so the caller's obligation has to be in words.
    expect(props.marketing_consent.description).toMatch(/consent/i);
  });

  // Outstanding item 3. status stays undeclared on purpose — pages_publish /
  // pages_unpublish are the affordances and pages_publish enforces the
  // future-end_date check a raw status: "active" would bypass. But an agent that
  // sends it now gets a confusing 422 "At least one field is required", so the
  // description has to say where status lives.
  it("pages_update leaves status undeclared and says where it lives instead", () => {
    const tool = TOOLS.find((t) => t.name === "pages_update")!;
    const props = tool.inputSchema.properties as Record<string, any>;

    expect(props.status).toBeUndefined();
    expect(tool.description).toContain("pages_publish");
    expect(tool.description).toContain("pages_unpublish");
  });

  it("pages_update advertises custom_css and the simple template", () => {
    const tool = TOOLS.find((t) => t.name === "pages_update")!;
    const props = tool.inputSchema.properties as Record<string, any>;

    expect(props.custom_css).toBeDefined();
    expect(props.custom_css.type).toEqual(["string", "null"]);
    // Launched 2026-08-10 — the pre-launch gate wording must be GONE, or an
    // agent will refuse to use a field that works.
    expect(props.custom_css.description).not.toContain("re-launch");
    expect(props.template.description).not.toContain("re-launch");
    expect(props.template.enum).toContain("simple");
    expect(props.custom_css.description).toContain("tokei-simple-");
  });

  it("pages_update advertises the seven media fields", () => {
    const tool = TOOLS.find((t) => t.name === "pages_update")!;
    const props = tool.inputSchema.properties as Record<string, any>;

    for (const field of [
      "image_video",
      "secondary_image",
      "third_image",
      "fourth_image",
      "fifth_image",
      "background_image",
      "og_image",
    ]) {
      expect(props[field]).toBeDefined();
      expect(props[field].type).toEqual(["string", "null"]);
      expect(typeof props[field].description).toBe("string");
    }

    // contest_id stays the only required field.
    expect(tool.inputSchema.required).toEqual(["contest_id"]);
  });

  it("media_upload declares file_path (required) and content_type (optional)", () => {
    const tool = TOOLS.find((t) => t.name === "media_upload")!;
    const props = tool.inputSchema.properties as Record<string, any>;
    expect(props.file_path).toBeDefined();
    expect(props.file_path.type).toBe("string");
    expect(props.content_type).toBeDefined();
    expect(props.content_type.type).toBe("string");
    expect(tool.inputSchema.required).toEqual(["file_path"]);
  });
});

describe("createMcpSession — tools/call wiring to the HTTP layer", () => {
  it("me -> GET /me with bearer auth; envelope includes rate_limit", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    const res = await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "me", arguments: {} },
    });
    expect(res.jsonrpc).toBe("2.0");
    expect(res.id).toBe(1);
    const url = new URL(h.calls[0].url);
    expect(url.origin + url.pathname).toBe("https://tokei.io/api/v1/me");
    expect(h.calls[0].init.method).toBe("GET");
    expect(h.calls[0].init.headers["Authorization"]).toBe("Bearer k");
    expect(res.result.isError).toBeFalsy();
    const parsed = JSON.parse(res.result.content[0].text);
    expect(parsed.rate_limit.limit).toBe(60);
  });

  it("pages_list maps query args, integers stringified", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "pages_list", arguments: { status: "active", per_page: 20 } },
    });
    const url = new URL(h.calls[0].url);
    expect(url.pathname).toBe("/api/v1/contests");
    expect(url.searchParams.get("status")).toBe("active");
    expect(url.searchParams.get("per_page")).toBe("20");
  });

  it("pages_get percent-encodes the path param", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "pages_get", arguments: { contest_id: "abc/../x" } },
    });
    const url = new URL(h.calls[0].url);
    expect(url.pathname).toBe("/api/v1/contests/abc%2F..%2Fx");
  });

  it("leaderboard passes page/per_page", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "leaderboard", arguments: { contest_id: "c1", page: 2, per_page: 50 } },
    });
    const url = new URL(h.calls[0].url);
    expect(url.pathname).toBe("/api/v1/contests/c1/leaderboard");
    expect(url.searchParams.get("page")).toBe("2");
    expect(url.searchParams.get("per_page")).toBe("50");
  });

  it("referrals_top passes page/per_page", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "referrals_top", arguments: { contest_id: "c1", page: 2, per_page: 50 } },
    });
    const url = new URL(h.calls[0].url);
    expect(url.pathname).toBe("/api/v1/contests/c1/referrals");
    expect(url.searchParams.get("page")).toBe("2");
    expect(url.searchParams.get("per_page")).toBe("50");
  });

  it("winners_list -> GET /contests/:id/winners, no query params, no body", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "winners_list", arguments: { contest_id: "c1" } },
    });
    const url = new URL(h.calls[0].url);
    expect(url.pathname).toBe("/api/v1/contests/c1/winners");
    expect(url.search).toBe("");
    expect(h.calls[0].init.method).toBe("GET");
    expect(h.calls[0].init.body).toBeUndefined();
  });

  it("winners_list missing contest_id -> isError true, no fetch call", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    const res = await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "winners_list", arguments: {} },
    });
    expect(res.result.isError).toBe(true);
    expect(res.result.content[0].text).toContain("contest_id");
    expect(h.calls).toEqual([]);
  });

  it("templates_list -> GET /templates, no query, no body", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "templates_list", arguments: {} },
    });
    const url = new URL(h.calls[0].url);
    expect(url.origin + url.pathname).toBe("https://tokei.io/api/v1/templates");
    expect(h.calls[0].init.method).toBe("GET");
    expect(h.calls[0].init.body).toBeUndefined();
  });

  it("actions_catalog -> GET /actions/catalog, no query when type omitted, no body", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "actions_catalog", arguments: {} },
    });
    const url = new URL(h.calls[0].url);
    expect(url.origin + url.pathname).toBe("https://tokei.io/api/v1/actions/catalog");
    expect(url.searchParams.get("type")).toBeNull();
    expect(h.calls[0].init.method).toBe("GET");
    expect(h.calls[0].init.body).toBeUndefined();
  });

  it("actions_catalog maps the optional type argument to ?type=", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "actions_catalog", arguments: { type: "twitter_follow" } },
    });
    const url = new URL(h.calls[0].url);
    expect(url.pathname).toBe("/api/v1/actions/catalog");
    expect(url.searchParams.get("type")).toBe("twitter_follow");
  });

  it("events_catalog -> GET /events/catalog, no query when type omitted, no body", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "events_catalog", arguments: {} },
    });
    const url = new URL(h.calls[0].url);
    expect(url.origin + url.pathname).toBe("https://tokei.io/api/v1/events/catalog");
    expect(url.searchParams.get("type")).toBeNull();
    expect(h.calls[0].init.method).toBe("GET");
    expect(h.calls[0].init.body).toBeUndefined();
  });

  it("events_catalog maps the optional type argument to ?type=", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "events_catalog", arguments: { type: "entry.created" } },
    });
    const url = new URL(h.calls[0].url);
    expect(url.pathname).toBe("/api/v1/events/catalog");
    expect(url.searchParams.get("type")).toBe("entry.created");
  });

  it("pages_clone with a template argument POSTs {title, template}", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: {
        name: "pages_clone",
        arguments: { title: "From Template", template: "product-hunt" },
      },
    });
    const url = new URL(h.calls[0].url);
    expect(url.origin + url.pathname).toBe("https://tokei.io/api/v1/promotions");
    expect(h.calls[0].init.method).toBe("POST");
    expect(JSON.parse(h.calls[0].init.body!)).toEqual({
      title: "From Template",
      template: "product-hunt",
    });
  });

  it("pages_update PATCHes body without the path param", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "pages_update", arguments: { contest_id: "c1", title: "T", end_date: null } },
    });
    const url = new URL(h.calls[0].url);
    expect(url.pathname).toBe("/api/v1/contests/c1");
    expect(h.calls[0].init.method).toBe("PATCH");
    expect(JSON.parse(h.calls[0].init.body!)).toEqual({ title: "T", end_date: null });
    expect(h.calls[0].init.headers["Content-Type"]).toBe("application/json");
  });

  it("pages_update passes template/dark_mode_enabled/primary_color/card_width through to the body", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: {
        name: "pages_update",
        arguments: {
          contest_id: "c1",
          template: "showcase",
          dark_mode_enabled: true,
          primary_color: "#7d78c6",
          card_width: "wide",
        },
      },
    });
    const url = new URL(h.calls[0].url);
    expect(url.pathname).toBe("/api/v1/contests/c1");
    expect(h.calls[0].init.method).toBe("PATCH");
    expect(JSON.parse(h.calls[0].init.body!)).toEqual({
      template: "showcase",
      dark_mode_enabled: true,
      primary_color: "#7d78c6",
      card_width: "wide",
    });
  });

  it('pages_publish PATCHes {"status":"active"}', async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "pages_publish", arguments: { contest_id: "c1" } },
    });
    const url = new URL(h.calls[0].url);
    expect(url.pathname).toBe("/api/v1/contests/c1");
    expect(h.calls[0].init.method).toBe("PATCH");
    expect(JSON.parse(h.calls[0].init.body!)).toEqual({ status: "active" });
  });

  it("pages_publish merges an end_date argument without clobbering the fixed status", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: {
        name: "pages_publish",
        arguments: { contest_id: "c1", end_date: "2027-01-01T00:00:00Z" },
      },
    });
    const url = new URL(h.calls[0].url);
    expect(url.pathname).toBe("/api/v1/contests/c1");
    expect(JSON.parse(h.calls[0].init.body!)).toEqual({
      status: "active",
      end_date: "2027-01-01T00:00:00Z",
    });
  });

  // T3a (0.3.5). Before the allowlist, `{ ...fixedBody, ...args }` forwarded any
  // undeclared field straight to PATCH /contests/{id}, where settings.prizes is a
  // wholesale replace — so this exact call wiped the prize list while the tool
  // advertised destructiveHint: false.
  it("pages_publish drops an undeclared prizes argument instead of wiping the prize list", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: {
        name: "pages_publish",
        arguments: { contest_id: "c1", prizes: [], title: "hijacked" },
      },
    });
    expect(JSON.parse(h.calls[0].init.body!)).toEqual({ status: "active" });
  });

  it("pages_unpublish, whose only property is contest_id, sends nothing but the fixed status", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: {
        name: "pages_unpublish",
        arguments: { contest_id: "c1", prizes: [], entry_methods: [], status: "active" },
      },
    });
    expect(JSON.parse(h.calls[0].init.body!)).toEqual({ status: "draft" });
  });

  it("pages_update keeps every declared field while dropping undeclared ones", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: {
        name: "pages_update",
        arguments: { contest_id: "c1", title: "Kept", user_id: "not-mine", id: "not-mine" },
      },
    });
    expect(JSON.parse(h.calls[0].init.body!)).toEqual({ title: "Kept" });
  });

  // Outstanding item 3. Silently swallowing arguments is how marketing_consent
  // went missing for a whole release: the allowlist is right, its silence is not.
  // An agent told which keys were ignored can self-correct.
  it("names the arguments it dropped rather than discarding them in silence", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    const res = await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: {
        name: "pages_update",
        arguments: { contest_id: "c1", title: "Kept", status: "active", nonsense: 1 },
      },
    });
    const notice = res.result.content.map((c: { text: string }) => c.text).join("\n");
    expect(notice).toMatch(/ignored/i);
    expect(notice).toContain("status");
    expect(notice).toContain("nonsense");
    // The drop itself is unchanged — the note is advisory, not a new pass-through.
    expect(JSON.parse(h.calls[0].init.body!)).toEqual({ title: "Kept" });
  });

  it("says nothing extra when every argument was declared", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    const res = await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "pages_update", arguments: { contest_id: "c1", title: "Kept" } },
    });
    expect(res.result.content.length).toBe(1);
  });

  // Outstanding item 2, on the wire: the field has to survive the allowlist.
  it("entries_create forwards marketing_consent to the API", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: {
        name: "entries_create",
        arguments: { contest_id: "c1", email: "a@b.example", marketing_consent: true },
      },
    });
    expect(JSON.parse(h.calls[0].init.body!)).toEqual({
      email: "a@b.example",
      marketing_consent: true,
    });
  });

  it('pages_unpublish PATCHes {"status":"draft"}', async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "pages_unpublish", arguments: { contest_id: "c1" } },
    });
    const url = new URL(h.calls[0].url);
    expect(url.pathname).toBe("/api/v1/contests/c1");
    expect(h.calls[0].init.method).toBe("PATCH");
    expect(JSON.parse(h.calls[0].init.body!)).toEqual({ status: "draft" });
  });

  it("entries_create POSTs the body", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: {
        name: "entries_create",
        arguments: { contest_id: "c1", email: "a@b.co", points: 10, metadata: { src: "x" } },
      },
    });
    const url = new URL(h.calls[0].url);
    expect(url.pathname).toBe("/api/v1/contests/c1/entries");
    expect(h.calls[0].init.method).toBe("POST");
    expect(JSON.parse(h.calls[0].init.body!)).toEqual({
      email: "a@b.co",
      points: 10,
      metadata: { src: "x" },
    });
  });

  it("webhooks_create appends a one-time-secret warning", async () => {
    const h = harness({ response: jsonRes({ success: true, data: { id: "w1", secret: "whsec_abc" } }, 201) });
    const session = createMcpSession(h.io);
    const res = await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "webhooks_create", arguments: { url: "https://x.example/hook", events: ["entry.created"] } },
    });
    expect(res.result.content.length).toBe(2);
    const envelope = JSON.parse(res.result.content[0].text);
    expect(envelope.data.secret).toBe("whsec_abc");
    expect(res.result.content[1].type).toBe("text");
    expect(res.result.content[1].text).toMatch(/only once|cannot be retrieved/i);
  });

  it("webhooks_create without a whsec_ secret -> content has length 1", async () => {
    const h = harness({ response: jsonRes({ success: true, data: { id: "w1" } }, 201) });
    const session = createMcpSession(h.io);
    const res = await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "webhooks_create", arguments: { url: "https://x.example/hook", events: ["entry.created"] } },
    });
    expect(res.result.content.length).toBe(1);
  });

  it("webhooks_delete -> DELETE /api/v1/webhooks/:id", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "webhooks_delete", arguments: { webhook_id: "w1" } },
    });
    const url = new URL(h.calls[0].url);
    expect(url.pathname).toBe("/api/v1/webhooks/w1");
    expect(h.calls[0].init.method).toBe("DELETE");
  });
});

/** The 201 body POST /api/v1/media answers with (Phase 1 item 8). */
const MEDIA_UPLOADED_DATA = {
  bucket: "tokei-media",
  path: "api-uploads/u1/uuid.png",
  public_url: "https://media.tokei.io/api-uploads/u1/uuid.png",
  content_type: "image/png",
  filename: "hero.png",
  size_bytes: 150,
  backend: "r2",
};

describe("createMcpSession — tools/call media_upload", () => {
  it("does ONE multipart POST and returns the public_url", async () => {
    const h = harness();
    const uploadCalls: {
      url: string;
      init: { method: string; headers: Record<string, string>; body: Uint8Array };
    }[] = [];
    (h.io as any).binaryFetchImpl = async (
      url: string,
      init: { method: string; headers: Record<string, string>; body: Uint8Array },
    ) => {
      uploadCalls.push({ url, init });
      return {
        status: 201,
        headers: { get: () => null },
        text: async () => JSON.stringify({ success: true, data: MEDIA_UPLOADED_DATA }),
      };
    };
    (h.io as any).readFileBytes = (_path: string) => new Uint8Array(150).fill(3);

    const session = createMcpSession(h.io);
    const res = await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "media_upload", arguments: { file_path: "hero.png" } },
    });

    expect(res.result.isError).toBe(false);
    // The ticket round-trip is gone: no JSON request at all.
    expect(h.calls).toEqual([]);
    expect(uploadCalls).toHaveLength(1);

    const url = new URL(uploadCalls[0].url);
    expect(url.pathname).toBe("/api/v1/media");
    expect(uploadCalls[0].init.method).toBe("POST");
    expect(uploadCalls[0].init.headers["Content-Type"]).toMatch(
      /^multipart\/form-data; boundary=.+/,
    );
    expect(Buffer.from(uploadCalls[0].init.body).toString("latin1")).toContain(
      'filename="hero.png"',
    );

    const payload = JSON.parse(res.result.content[0].text);
    expect(payload.success).toBe(true);
    expect(payload.data.public_url).toBe(MEDIA_UPLOADED_DATA.public_url);
  });

  it("missing file_path -> tool error, isError true, no HTTP calls", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    const res = await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "media_upload", arguments: {} },
    });
    expect(res.result.isError).toBe(true);
    expect(h.calls).toEqual([]);
  });

  it("Io without readFileBytes/binaryFetchImpl -> tool error mentioning 'not supported', no HTTP calls", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    const res = await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "media_upload", arguments: { file_path: "hero.png" } },
    });
    expect(res.result.isError).toBe(true);
    expect(res.result.content[0].text).toMatch(/not supported in this environment/);
    expect(h.calls).toEqual([]);
  });
});

describe("createMcpSession — tools/call errors", () => {
  it("API error -> isError true, still a JSON-RPC result (not a JSON-RPC error)", async () => {
    const h = harness({
      response: jsonRes({ success: false, error: { code: "NOT_FOUND", message: "nope", status: 404 } }, 404),
    });
    const session = createMcpSession(h.io);
    const res = await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "pages_get", arguments: { contest_id: "missing" } },
    });
    expect(res.error).toBeUndefined();
    expect(res.result.isError).toBe(true);
    const parsed = JSON.parse(res.result.content[0].text);
    expect(parsed.error.code).toBe("NOT_FOUND");
    expect(parsed.rate_limit).toBeDefined();
  });

  it("fetch throws -> isError true with a network_error envelope", async () => {
    const h = harness({ response: new Error("boom") });
    const session = createMcpSession(h.io);
    const res = await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "me", arguments: {} },
    });
    expect(res.result.isError).toBe(true);
    const parsed = JSON.parse(res.result.content[0].text);
    expect(parsed.error.type).toBe("network_error");
  });

  it("unknown tool name -> JSON-RPC error -32602 (protocol error, not a result)", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    const res = await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "bogus_tool", arguments: {} },
    });
    expect(res.result).toBeUndefined();
    expect(res.error.code).toBe(-32602);
  });

  it("missing required argument -> isError true, no fetch call", async () => {
    const h = harness();
    const session = createMcpSession(h.io);
    const res = await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "pages_get", arguments: {} },
    });
    expect(res.result.isError).toBe(true);
    expect(res.result.content[0].text).toContain("contest_id");
    expect(h.calls).toEqual([]);
  });

  it("missing TOKEI_API_KEY -> isError true, no fetch call", async () => {
    const h = harness({ env: {} });
    const session = createMcpSession(h.io);
    const res = await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: "me", arguments: {} },
    });
    expect(res.result.isError).toBe(true);
    expect(res.result.content[0].text).toContain("TOKEI_API_KEY");
    expect(h.calls).toEqual([]);
  });

  it("initialize and tools/list still work without an API key", async () => {
    const h = harness({ env: {} });
    const session = createMcpSession(h.io);
    const initRes = await rpc(session, {
      jsonrpc: "2.0",
      id: 1,
      method: "initialize",
      params: INITIALIZE_PARAMS,
    });
    expect(initRes.result.protocolVersion).toBe("2025-06-18");
    const listRes = await rpc(session, { jsonrpc: "2.0", id: 2, method: "tools/list" });
    expect(listRes.result.tools.length).toBe(21);
  });
});

describe('main(["mcp"]) loop', () => {
  it("runs over io.stdin, writes one response line per request, and exits 0", async () => {
    async function* lines(): AsyncGenerator<string> {
      yield JSON.stringify({
        jsonrpc: "2.0",
        id: 1,
        method: "initialize",
        params: INITIALIZE_PARAMS,
      });
      yield JSON.stringify({ jsonrpc: "2.0", id: 2, method: "tools/list" });
    }
    const h = harness({ stdin: lines() });
    const code = await main(["mcp"], h.io);
    expect(code).toBe(0);
    expect(h.out.length).toBe(2);
    for (const line of h.out) {
      expect(line).not.toContain("\n");
      expect(() => JSON.parse(line)).not.toThrow();
    }
    expect(JSON.parse(h.out[0]).id).toBe(1);
    expect(JSON.parse(h.out[1]).id).toBe(2);
  });

  it("mcp without io.stdin -> usage error, exit 2", async () => {
    const h = harness();
    const code = await main(["mcp"], h.io);
    expect(code).toBe(2);
    expect(h.out).toEqual([]);
    expect(h.err.length).toBe(1);
    expect(JSON.parse(h.err[0]).error.type).toBe("usage_error");
  });
});
