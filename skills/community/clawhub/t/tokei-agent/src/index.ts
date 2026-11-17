// tokei-agent CLI — read and write commands for the Tokei (tokei.io) v1 REST API.
// Zero runtime dependencies: Node 22 native fetch + hand-rolled parsing.

import { parseArgs } from "./args.js";
import { request } from "./http.js";
import type { BinaryFetchLike, FetchLike } from "./http.js";
import { createMcpSession } from "./mcp.js";
import { uploadMedia } from "./media.js";
import { hasOneTimeSecret, readManifest, resolvePath } from "./tool-dispatch.js";
import type { CliSpec, ToolSpec } from "./tool-dispatch.js";
import manifest from "./tool-manifest.json" with { type: "json" };
import { createTerm, failureMessage, formatCount, renderBanner } from "./ui.js";
import type { SummaryRow, Term, TermHost } from "./ui.js";

// Kept in sync with cli/package.json by hand (zero-dep simplicity).
export const VERSION = "0.3.8";

const DEFAULT_BASE_URL = "https://tokei.io";

export interface Io {
  env: Record<string, string | undefined>;
  fetchImpl: FetchLike;
  stdout: (line: string) => void;
  stderr: (line: string) => void;
  // Reads a file for `--data @file.json`. Optional so embedders without a
  // filesystem can omit it.
  readFile?: (path: string) => string;
  // Reads a file as raw bytes for `media:upload <file>`. Optional so
  // embedders without a filesystem can omit it (the command then reports a
  // usage error) — same idiom as readFile.
  readFileBytes?: (path: string) => Uint8Array;
  // Binary-body fetch used by `media:upload`'s multipart POST.
  // Optional so embedders without network access for binary bodies can omit
  // it (the command then reports a usage error) — same idiom as readFile.
  binaryFetchImpl?: BinaryFetchLike;
  // Line stream driving the `mcp` command. Optional so embedders without a
  // stdin can omit it (the command then reports a usage error).
  stdin?: AsyncIterable<string>;
  // Raw stream access for the interactive UI. Optional: when absent — tests,
  // embedders, MCP — the UI is inert and output is byte-identical to the
  // JSON-only behaviour. Distinct from `stdout`, which is a *line* writer.
  term?: TermHost;
}

interface FlagSpec {
  // CLI flag name (e.g. "per-page") and the wire query param (e.g. "per_page").
  name: string;
  param: string;
  kind: "int" | "enum" | "string";
  values?: readonly string[];
  min?: number;
  max?: number;
}

interface BodyFlagSpec {
  // CLI flag name (e.g. "campaign-url") and the wire body field (e.g. "campaign_url").
  name: string;
  field: string;
  kind: "string" | "int" | "enum" | "list" | "bool";
  values?: readonly string[];
  required?: boolean;
}

// One CLI command, derived from its tool-manifest.json entry. Request shape
// (method, path, fixedBody, warnSecretOnce) is read from `tool`.
//
// Every tool with a body also accepts --data '<json>' / --data @file.json,
// merged under individual body flags (flags win). It is passed to the API
// untouched: the API's 422 per-field errors are the validation story, and
// unlike MCP arguments it is not filtered against inputSchema.
interface CommandSpec {
  tool: ToolSpec;
  flags: FlagSpec[];
  bodyFlags: BodyFlagSpec[];
}

// The subset of JSON Schema the manifest's input properties use.
interface PropSchema {
  type?: string | string[];
  enum?: string[];
  minimum?: number;
  maximum?: number;
}

function propSchema(tool: ToolSpec, name: string): PropSchema {
  const schema = tool.def.inputSchema.properties[name];
  if (schema === undefined) {
    throw new Error(`tool-manifest.json: ${tool.def.name} declares no "${name}" property`);
  }
  return schema as PropSchema;
}

function flagName(cli: CliSpec, field: string): string {
  return cli.flagNames?.[field] ?? field.replace(/_/g, "-");
}

// Query flags validate against the schema's enum and integer bounds.
function queryFlag(tool: ToolSpec, cli: CliSpec, param: string): FlagSpec {
  const schema = propSchema(tool, param);
  const name = flagName(cli, param);
  if (schema.enum) return { name, param, kind: "enum", values: schema.enum };
  if (schema.type === "integer") {
    return { name, param, kind: "int", min: schema.minimum, max: schema.maximum };
  }
  return { name, param, kind: "string" };
}

// Body flags check form only (enum membership, digits, true/false). Integer
// bounds are left to the API's 422.
function bodyFlag(tool: ToolSpec, cli: CliSpec, field: string): BodyFlagSpec {
  const schema = propSchema(tool, field);
  const type = Array.isArray(schema.type) ? schema.type[0] : schema.type;
  const kind: BodyFlagSpec["kind"] = schema.enum
    ? "enum"
    : type === "boolean"
      ? "bool"
      : type === "integer"
        ? "int"
        : type === "array"
          ? "list"
          : "string";
  return {
    name: flagName(cli, field),
    field,
    kind,
    values: schema.enum,
    required: tool.def.inputSchema.required?.includes(field) ?? false,
  };
}

// A Map, so a command named after an Object.prototype member ("toString")
// is an unknown command rather than a crash.
const COMMANDS = new Map<string, CommandSpec>();
for (const tool of readManifest(manifest)) {
  const cli = tool.cli;
  if (!cli) continue;
  COMMANDS.set(cli.command, {
    tool,
    flags: (tool.queryParams ?? []).map((param) => queryFlag(tool, cli, param)),
    bodyFlags: (cli.bodyFlags ?? []).map((field) => bodyFlag(tool, cli, field)),
  });
}

// ---------------------------------------------------------------------------
// Presentation only. Kept out of tool-manifest.json, which describes the wire
// protocol and the tools.
//
// Copy uses "page", matching README.md and the pages:* command names — the
// `/contests` path and `contestId` positional are the wire format, and --mode
// also accepts sharing_only/gamification, which are not contests.
//
// One step per real request: the CLI issues exactly one HTTP call per command,
// media:upload included, so there is never more than one tick to show.
// Anything more would be invented progress.
interface CommandCopy {
  pending: string;
  done: string | ((payload: unknown) => string);
}

/**
 * How many records the response covers.
 *
 * Prefers `pagination.total_count` over `data.length`: list endpoints default
 * to 25 per page, so `data.length` silently caps the reported figure at the
 * page size ("25 pages" when there are 30). Falls back to the array length for
 * unpaginated responses.
 */
function dataCount(payload: unknown): number | undefined {
  if (payload === null || typeof payload !== "object") return undefined;
  const total = (payload as { pagination?: { total_count?: unknown } }).pagination?.total_count;
  if (typeof total === "number") return total;
  const data = (payload as { data?: unknown }).data;
  return Array.isArray(data) ? data.length : undefined;
}

function counted(noun: string, fallback: string): (payload: unknown) => string {
  return (payload) => {
    const n = dataCount(payload);
    if (n === undefined) return fallback;
    return `${formatCount(n)} ${n === 1 ? noun : `${noun}s`}`;
  };
}

const COPY: Record<string, CommandCopy> = {
  me: { pending: "Verifying your API key", done: "Signed in" },
  "pages:list": { pending: "Fetching your pages", done: counted("page", "Pages loaded") },
  "pages:get": { pending: "Loading page", done: "Page loaded" },
  "pages:clone": { pending: "Creating page from template", done: "Page created" },
  "pages:update": { pending: "Saving changes", done: "Changes saved" },
  "pages:publish": { pending: "Publishing page", done: "Page is live" },
  "pages:unpublish": { pending: "Returning page to draft", done: "Page is a draft" },
  "templates:list": {
    pending: "Fetching templates",
    done: counted("template", "Templates loaded"),
  },
  "actions:catalog": { pending: "Fetching action catalog", done: "Catalog loaded" },
  "events:catalog": { pending: "Fetching event catalog", done: "Catalog loaded" },
  stats: { pending: "Gathering analytics", done: "Analytics ready" },
  leaderboard: { pending: "Ranking entrants", done: "Leaderboard ready" },
  "referrals:top": {
    pending: "Ranking referrers",
    done: counted("referrer", "Top referrers loaded"),
  },
  "winners:list": {
    pending: "Fetching winners",
    done: counted("selection run", "Winners loaded"),
  },
  "entries:list": { pending: "Fetching entries", done: counted("entry", "Entries loaded") },
  "entries:create": { pending: "Recording entry", done: "Entry recorded" },
  "surveys:list": {
    pending: "Fetching survey responses",
    done: counted("response", "Responses loaded"),
  },
  "webhooks:list": { pending: "Fetching webhooks", done: counted("webhook", "Webhooks loaded") },
  "webhooks:create": { pending: "Registering webhook", done: "Webhook registered" },
  "webhooks:delete": { pending: "Removing webhook", done: "Webhook removed" },
};

/**
 * The account summary shown after `me`. Renders only fields the payload
 * actually contains — /me returns no permission or access flags, so nothing
 * resembling a capability checklist can be shown truthfully.
 */
function renderAccountSummary(term: Term, payload: unknown): void {
  const data =
    payload !== null && typeof payload === "object"
      ? ((payload as { data?: unknown }).data as Record<string, unknown> | undefined)
      : undefined;
  if (!data) return;

  const rows: SummaryRow[] = [];
  const plan = data.plan;
  if (typeof plan === "string") rows.push({ label: "Plan", value: plan.toUpperCase() });

  const usage = data.api_usage as Record<string, unknown> | undefined;
  if (usage && typeof usage.requests_today === "number" && typeof usage.daily_limit === "number") {
    rows.push({
      label: "Requests today",
      value: `${formatCount(usage.requests_today)} / ${formatCount(usage.daily_limit)}`,
    });
  }
  if (typeof data.active_contests === "number") {
    rows.push({ label: "Active pages", value: formatCount(data.active_contests) });
  }
  const rl = (payload as { rate_limit?: { remaining?: unknown; limit?: unknown } }).rate_limit;
  if (rl && typeof rl.remaining === "number" && typeof rl.limit === "number") {
    rows.push({
      label: "Rate limit",
      value: `${formatCount(rl.remaining)} / ${formatCount(rl.limit)} remaining`,
    });
  }

  const email = typeof data.email === "string" ? data.email : undefined;
  term.summary({
    welcome: email ? `Welcome back, ${email}` : undefined,
    rows,
    closing: "Tokei Agent ready",
  });
}

const COMMAND_NAMES = [...COMMANDS.keys()];

class UsageError extends Error {}

function checkKnownFlags(spec: CommandSpec, flags: Record<string, string>): void {
  const known = new Set(spec.flags.map((f) => f.name));
  for (const bf of spec.bodyFlags) known.add(bf.name);
  if (spec.tool.hasBody) known.add("data");
  for (const provided of Object.keys(flags)) {
    if (!known.has(provided)) {
      throw new UsageError(`Unknown flag --${provided} for this command`);
    }
  }
}

function buildQuery(spec: CommandSpec, flags: Record<string, string>): Record<string, string> {
  const query: Record<string, string> = {};
  for (const flag of spec.flags) {
    const raw = flags[flag.name];
    if (raw === undefined) continue;

    if (flag.kind === "int") {
      if (!/^\d+$/.test(raw)) {
        throw new UsageError(`--${flag.name} must be an integer`);
      }
      const n = Number(raw);
      if (flag.min !== undefined && n < flag.min) {
        throw new UsageError(`--${flag.name} must be >= ${flag.min}`);
      }
      if (flag.max !== undefined && n > flag.max) {
        throw new UsageError(`--${flag.name} must be <= ${flag.max}`);
      }
      query[flag.param] = String(n);
    } else if (flag.kind === "enum") {
      if (!flag.values || !flag.values.includes(raw)) {
        throw new UsageError(`--${flag.name} must be one of: ${flag.values?.join(", ")}`);
      }
      query[flag.param] = raw;
    } else {
      if (raw === "") {
        throw new UsageError(`--${flag.name} requires a value`);
      }
      query[flag.param] = raw;
    }
  }
  return query;
}

function parseDataFlag(raw: string, io: Io): Record<string, unknown> {
  if (raw === "") {
    throw new UsageError("--data requires a value: a JSON object or @file.json");
  }
  let text = raw;
  if (raw.startsWith("@")) {
    const path = raw.slice(1);
    if (!io.readFile) {
      throw new UsageError("--data @file is not supported in this environment");
    }
    try {
      text = io.readFile(path);
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      throw new UsageError(`--data: could not read ${path}: ${message}`);
    }
  }
  let parsed: unknown;
  try {
    parsed = JSON.parse(text);
  } catch {
    throw new UsageError("--data must be valid JSON");
  }
  if (parsed === null || typeof parsed !== "object" || Array.isArray(parsed)) {
    throw new UsageError("--data must be a JSON object");
  }
  return { ...(parsed as Record<string, unknown>) };
}

function buildBody(
  spec: CommandSpec,
  flags: Record<string, string>,
  io: Io,
): Record<string, unknown> | undefined {
  const { tool } = spec;
  if (!tool.hasBody) return undefined;

  // fixedBody is the base layer; --data is merged on top of it (and wins on
  // conflict); individual flags are applied last and win over both.
  const body: Record<string, unknown> = { ...(tool.fixedBody ?? {}) };
  if (flags.data !== undefined) {
    Object.assign(body, parseDataFlag(flags.data, io));
  }

  for (const bf of spec.bodyFlags) {
    const raw = flags[bf.name];
    if (raw === undefined) continue;
    if (raw === "") {
      throw new UsageError(`--${bf.name} requires a value`);
    }
    if (bf.kind === "int") {
      if (!/^\d+$/.test(raw)) {
        throw new UsageError(`--${bf.name} must be an integer`);
      }
      body[bf.field] = Number(raw);
    } else if (bf.kind === "enum") {
      if (!bf.values || !bf.values.includes(raw)) {
        throw new UsageError(`--${bf.name} must be one of: ${bf.values?.join(", ")}`);
      }
      body[bf.field] = raw;
    } else if (bf.kind === "bool") {
      if (raw !== "true" && raw !== "false") {
        throw new UsageError(`--${bf.name} must be "true" or "false"`);
      }
      body[bf.field] = raw === "true";
    } else if (bf.kind === "list") {
      const items = raw
        .split(",")
        .map((s) => s.trim())
        .filter((s) => s.length > 0);
      if (items.length === 0) {
        throw new UsageError(`--${bf.name} requires a value`);
      }
      body[bf.field] = items;
    } else {
      body[bf.field] = raw;
    }
  }

  for (const bf of spec.bodyFlags) {
    if (bf.required && body[bf.field] === undefined) {
      throw new UsageError(`--${bf.name} is required (or provide "${bf.field}" via --data)`);
    }
  }
  if (tool.cli?.requireBody && Object.keys(body).length === 0) {
    throw new UsageError("Provide at least one field to update, via flags or --data");
  }
  return body;
}

const HELP = `tokei-agent — control your Tokei (tokei.io) pre-launch campaigns from AI agents and the CLI.

Usage:
  tokei-agent <command> [flags]

Commands (read):
  me                          Show the authenticated account / API key
  pages:list                  List promotions
                                --status draft|active|completed|deleted
                                --mode competition|gamification|sharing_only
                                --page <n>  --per-page <1-100>
  pages:get <contestId>       Get a single promotion
  stats <contestId>           Analytics for a promotion
  leaderboard <contestId>     Leaderboard   --page <n>  --per-page <1-100>
  referrals:top <contestId>   Top referrers, ranked by conversions, plus
                              click/conversion totals. Only entrants who have
                              actually referred someone are listed.
                                --page <n>  --per-page <1-100>
  winners:list <contestId>    Selection-run history for a page (newest first):
                              each run's seed, algorithm version, status, and
                              its persisted winners with entrant identity and
                              prize details. No pagination on this endpoint.
  entries:list <contestId>    List entries  --page <n>  --per-page <1-100>  --email <addr>
  surveys:list <contestId>    Survey responses  --page <n>  --per-page <1-100>
  webhooks:list               List webhook subscriptions  --page <n>  --per-page <1-100>
  templates:list              List the platform's named starting points (id,
                              slug, name, skin, entry_method_count) — clone one
                              by slug with pages:clone --template <slug>.
  actions:catalog             List every entry-action type Tokei supports
                              (label, description, points, platform, whether
                              it's trust-based/verifiable) — same list for
                              every key.
                                --type <actionType>  (unknown type is a 400)
  events:catalog              List every webhook event type Tokei's delivery
                              engine understands (description, payload schema,
                              subscribable) — same list for every key.
                                --type <eventType>  (unknown type is a 400)

Commands (write — need a read+write API key):
  pages:clone                 Create a promotion by cloning one you own; omit
                              --source and --template to clone the platform
                              starter template. Rate limited to 20 clones per
                              day per account.
                                --title <t> (required)  --source <promotionId>
                                --template <slug> (alternative to --source; get
                                slugs from templates:list; --source + --template
                                together is a 422)
                                --description <d>  --prize <name>  --end-date <iso>
                                --campaign-url <url>  --image-url <url>
                                --status draft|active  --idempotency-key <k>  --data
  media:upload <file>         Upload an image or video (one multipart POST) and
                              print a public_url to feed into pages:update's
                              media flags below. ≤4MB per file — the cap applies
                              to video too, not just images.
                              Content type is inferred from the extension
                              (.jpg/.jpeg/.png/.gif/.webp/.mp4/.webm/.mov);
                              override with --content-type <type>.
  pages:update <contestId>    Update a promotion. Simple fields via flags; prizes,
                              reward_thresholds, entry_methods (or a full body)
                              via --data. Each of those three REPLACES the whole
                              list — read with pages:get first, modify, send back.
                              An entry_methods row is either an action row
                              {id?,actionType,label,points?,config?,requireVerification?}
                              (actionType from actions:catalog) or a custom link
                              {id?,label,points?,link,actionsRequired?} with no
                              actionType. id (optional, [A-Za-z0-9_-], max 64
                              chars) gives a row stable identity; duplicate ids
                              in one array are a 422. At most 5 rows may share
                              one actionType for twitter_follow, instagram_follow
                              and facebook_visit_page — every other type is
                              capped at 1; exceeding it is also a 422. E.g.
                                --data '{"entry_methods":[{"label":"Read the
                                Newsletter","points":2,"link":"https://x.com/n"}]}'
                                --title <t>  --description <d>
                                --start-date <iso>  --end-date <iso>
                                --template basic-new|showcase|future|simple
                                ("simple" = the Custom template, bring-your-own-CSS)
                                --custom-css <css> (Custom-template creator CSS,
                                ≤20 KB, sanitised server-side)
                                --dark-mode true|false  --primary-color <hex>
                                --card-width narrow|medium|wide|xl
                                (or max-w-2xl|3xl|4xl|7xl)
                                --image-video <url>  --secondary-image <url>
                                --third-image <url>  --fourth-image <url>
                                --fifth-image <url>  --background-image <url>
                                --og-image <url>  --data
                              (media URLs come from media:upload's public_url)
  pages:publish <contestId>   Publish a page (status -> active). Requires an
                              end_date in the future, already stored or sent
                              in --data, e.g. --data '{"end_date":"..."}'
                              to publish and set the deadline in one call.
  pages:unpublish <contestId> Unpublish a page (status -> draft). Entries are
                              untouched, new ones are blocked, and visitors
                              see a "not open right now" page.
  entries:create <contestId>  Add an entry
                                --email <addr> (required)  --name <n>
                                --action-type <t>  --points <n>  --value <v>  --data
  webhooks:create             Create a webhook subscription. The response shows the
                              whsec_ signing secret ONCE — it cannot be retrieved
                              again, so store it immediately.
                                --url <https-url> (required)
                                --events <e1,e2> (required, e.g. entry.created)  --data
  webhooks:delete <webhookId> Delete a webhook subscription

Commands (other):
  mcp                         Run the MCP stdio server — every command above
                              exposed as an MCP tool (for Claude Code, Claude
                              Desktop, and other MCP clients)

  --help, help                Show this help
  --version, -v               Show the version

--data '<json>' or --data @file.json supplies the request body as raw JSON,
merged under any field flags (flags win). It is sent to the API untouched;
invalid bodies come back as 422 responses with per-field errors.

Environment:
  TOKEI_API_KEY   Required. API key sent as "Authorization: Bearer <key>".
                  Create one at https://tokei.io (Dashboard, Settings, API Keys).
  TOKEI_API_URL   Optional. Base URL override (default https://tokei.io).

Output: JSON on stdout, augmented with a top-level "rate_limit" object.
Exit codes: 0 success, 1 API/network error, 2 usage error.`;

function usageError(io: Io, message: string): number {
  io.stderr(JSON.stringify({ ok: false, error: { type: "usage_error", message } }, null, 2));
  return 2;
}

export async function main(argv: string[], io: Io): Promise<number> {
  const { command, positionals, flags } = parseArgs(argv);

  if ("help" in flags || command === "help") {
    // The wordmark above the help text is the first thing a human sees —
    // `npx tokei-agent --help` is line 1 of the README quickstart. renderBanner
    // returns undefined for pipes, redirects, CI and TOKEI_OUTPUT=json, so the
    // parsed form of this output is unchanged.
    const banner = renderBanner(io.term);
    if (banner !== undefined) io.term!.write(banner);
    io.stdout(HELP);
    return 0;
  }
  if ("version" in flags || "v" in flags) {
    io.stdout(VERSION);
    return 0;
  }

  if (command === undefined) {
    return usageError(
      io,
      `No command given. Valid commands: ${COMMAND_NAMES.join(", ")}, media:upload, mcp`,
    );
  }

  if (command === "mcp") {
    if (!io.stdin) {
      return usageError(io, "mcp needs a stdin line stream (run it via the tokei-agent binary)");
    }
    const session = createMcpSession(io);
    for await (const line of io.stdin) {
      if (line.trim() === "") continue;
      const reply = await session.handleLine(line);
      if (reply !== undefined) io.stdout(reply);
    }
    return 0;
  }

  // media:upload sends file bytes as multipart/form-data rather than a JSON
  // body, so its manifest entry has a handler and no `cli` section, and the
  // command is handled here, ahead of the COMMANDS lookup.
  if (command === "media:upload") {
    const filePath = positionals[0];
    if (filePath === undefined) {
      return usageError(io, "media:upload requires a <file> argument");
    }
    const knownFlags = new Set(["content-type"]);
    for (const provided of Object.keys(flags)) {
      if (!knownFlags.has(provided)) {
        return usageError(io, `Unknown flag --${provided} for this command`);
      }
    }
    if (flags["content-type"] === "") {
      return usageError(io, "--content-type requires a value");
    }

    const apiKey = io.env.TOKEI_API_KEY;
    if (!apiKey) {
      return usageError(io, "TOKEI_API_KEY is not set. Create a key at https://tokei.io and export it.");
    }
    const baseUrl = io.env.TOKEI_API_URL || DEFAULT_BASE_URL;

    const outcome = await uploadMedia({
      filePath,
      contentTypeOverride: flags["content-type"],
      apiKey,
      baseUrl,
      binaryFetchImpl: io.binaryFetchImpl,
      readFileBytes: io.readFileBytes,
    });
    if (outcome.kind === "usage_error") return usageError(io, outcome.message);
    io.stdout(JSON.stringify(outcome.payload, null, 2));
    return outcome.exitCode;
  }

  const spec = COMMANDS.get(command);
  if (!spec) {
    return usageError(io, `Unknown command "${command}". Valid commands: ${COMMAND_NAMES.join(", ")}`);
  }

  let positional: string | undefined;
  const positionalName = spec.tool.cli?.positional;
  if (positionalName) {
    positional = positionals[0];
    if (positional === undefined) {
      return usageError(io, `${command} requires a <${positionalName}> argument`);
    }
  }

  let query: Record<string, string>;
  let body: Record<string, unknown> | undefined;
  try {
    checkKnownFlags(spec, flags);
    query = buildQuery(spec, flags);
    body = buildBody(spec, flags, io);
  } catch (err) {
    if (err instanceof UsageError) return usageError(io, err.message);
    throw err;
  }

  const apiKey = io.env.TOKEI_API_KEY;
  if (!apiKey) {
    return usageError(io, "TOKEI_API_KEY is not set. Create a key at https://tokei.io and export it.");
  }

  const baseUrl = io.env.TOKEI_API_URL || DEFAULT_BASE_URL;

  // Presentation only. `term` is undefined for pipes, redirects, CI, MCP and
  // tests, in which case this whole block collapses to the original single
  // io.stdout() call below.
  const copy = COPY[command];
  const term = copy ? createTerm(io.term) : undefined;
  // The full wordmark is reserved for `me`; routine commands get a step line.
  term?.start(copy!.pending, { logo: command === "me" });

  const { payload, exitCode, status } = await request(
    {
      baseUrl,
      apiKey,
      path: resolvePath(spec.tool, positional),
      query,
      method: spec.tool.method,
      body,
    },
    io.fetchImpl,
  );

  if (term) {
    if (exitCode === 0) {
      const done = copy!.done;
      await term.finish("done", typeof done === "function" ? done(payload) : done);
      if (command === "me") {
        renderAccountSummary(term, payload);
      } else {
        io.stdout(JSON.stringify(payload, null, 2));
      }
    } else {
      // The ✗ line is a summary, never a replacement: the full error object
      // still goes to stdout so it stays inspectable.
      await term.finish("fail", failureMessage(status, payload));
      io.stdout(JSON.stringify(payload, null, 2));
    }
  } else {
    io.stdout(JSON.stringify(payload, null, 2));
  }

  if (spec.tool.warnSecretOnce && exitCode === 0 && hasOneTimeSecret(payload)) {
    io.stderr(
      "Warning: the whsec_ signing secret in this response is shown only once and cannot be retrieved again. Store it securely now.",
    );
  }

  return exitCode;
}
