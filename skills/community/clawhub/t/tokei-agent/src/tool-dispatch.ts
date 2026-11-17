// Shared tool dispatch for tokei-agent's tool manifest (tool-manifest.json).
// Turns a manifest entry plus call arguments into one /api/v1 request, and the
// API's reply back into an MCP tool result.
//
// This module imports nothing, not even types. The local stdio server
// (mcp.ts) and the remote /mcp route in the Next.js app both import it by
// relative path, so it must load under NodeNext, the Next bundlers and jest
// alike. It does no I/O; callers own fetch, auth and the base URL.

export type HttpMethod = "GET" | "POST" | "PATCH" | "DELETE";

export interface ToolDef {
  name: string;
  title?: string;
  description: string;
  inputSchema: {
    type: "object";
    properties: Record<string, unknown>;
    required?: string[];
  };
  annotations?: {
    readOnlyHint?: boolean;
    destructiveHint?: boolean;
    idempotentHint?: boolean;
  };
}

/** How the CLI exposes a tool. Flags and their validation derive from def.inputSchema. */
export interface CliSpec {
  // Command name, e.g. "pages:list".
  command: string;
  // Usage name of the positional that fills pathParam, e.g. "contestId".
  positional?: string;
  // Body fields settable by individual flags, in flag-processing order. Every
  // tool with hasBody also accepts --data, which is sent untouched.
  bodyFlags?: string[];
  // Flag names that differ from the field name with "_" replaced by "-".
  flagNames?: Record<string, string>;
  // Usage error when the merged body has no fields.
  requireBody?: boolean;
}

export interface ToolSpec {
  def: ToolDef;
  // Default GET.
  method?: HttpMethod;
  // Path under /api/v1. "{<pathParam>}" marks where the encoded value goes.
  path: string;
  // Argument that fills the path placeholder; never sent in the body.
  pathParam?: string;
  // Arguments copied into the query string, in this order, values stringified.
  queryParams?: string[];
  // Declared arguments (minus pathParam) are sent as the JSON body.
  hasBody?: boolean;
  // Body fields sent on every call; caller arguments win on conflict.
  fixedBody?: Record<string, unknown>;
  // Flag a whsec_ signing secret in a successful reply as shown only once.
  warnSecretOnce?: boolean;
  // Names a runtime-specific handler (e.g. media_upload's multipart POST)
  // that replaces the generic single-request path.
  handler?: string;
  // Absent for tools the CLI handles outside the generic command path.
  cli?: CliSpec;
}

export interface ToolResult {
  content: { type: "text"; text: string }[];
  isError: boolean;
}

export interface ToolRequest {
  method?: HttpMethod;
  path: string;
  query?: Record<string, string>;
  body?: Record<string, unknown>;
  // Arguments left out of the body because inputSchema does not declare them.
  dropped: string[];
}

/** Types the JSON import. The manifest's shape is pinned by tests, not checked here. */
export function readManifest(json: { tools: unknown[] }): ToolSpec[] {
  return json.tools as ToolSpec[];
}

/** Fills the path placeholder. Values are percent-encoded so they stay inside one segment. */
export function resolvePath(spec: ToolSpec, value: string | undefined): string {
  if (spec.pathParam === undefined) return spec.path;
  return spec.path.replace(`{${spec.pathParam}}`, encodeURIComponent(value!));
}

/** The first required argument the call is missing, if any. */
export function missingRequired(spec: ToolSpec, args: Record<string, unknown>): string | undefined {
  return (spec.def.inputSchema.required ?? []).find((name) => args[name] === undefined);
}

export function buildToolRequest(spec: ToolSpec, args: Record<string, unknown>): ToolRequest {
  const pathValue = spec.pathParam !== undefined ? String(args[spec.pathParam]) : undefined;

  let query: Record<string, string> | undefined;
  if (spec.queryParams) {
    query = {};
    for (const name of spec.queryParams) {
      const value = args[name];
      if (value !== undefined && value !== null) query[name] = String(value);
    }
  }

  let body: Record<string, unknown> | undefined;
  const dropped: string[] = [];
  if (spec.hasBody) {
    // Only declared inputSchema.properties may reach the body. Without this an
    // undeclared field rode straight through to PATCH /contests/{id}, where
    // settings.prizes is a wholesale replace (src/features/public-api/model/contest-patch.ts),
    // so `pages_publish { contest_id, prizes: [] }` wiped the prize list under
    // destructiveHint: false. fixedBody is the base layer; declared caller
    // arguments still win on conflict.
    const declared = spec.def.inputSchema.properties;
    const allowed: Record<string, unknown> = {};
    for (const [name, value] of Object.entries(args)) {
      if (Object.prototype.hasOwnProperty.call(declared, name)) allowed[name] = value;
      else dropped.push(name);
    }
    body = { ...(spec.fixedBody ?? {}), ...allowed };
    if (spec.pathParam !== undefined) delete body[spec.pathParam];
  }

  return { method: spec.method, path: resolvePath(spec, pathValue), query, body, dropped };
}

/** True when a reply carries a whsec_ signing secret at data.secret. */
export function hasOneTimeSecret(payload: unknown): boolean {
  const data =
    payload !== null && typeof payload === "object" ? (payload as { data?: unknown }).data : undefined;
  const secret =
    data !== null && typeof data === "object" ? (data as { secret?: unknown }).secret : undefined;
  return typeof secret === "string" && secret.startsWith("whsec_");
}

export function toolResult(
  spec: ToolSpec,
  payload: unknown,
  exitCode: number,
  dropped: string[],
): ToolResult {
  const content: ToolResult["content"] = [{ type: "text", text: JSON.stringify(payload, null, 2) }];

  if (spec.warnSecretOnce && exitCode === 0 && hasOneTimeSecret(payload)) {
    content.push({
      type: "text",
      text: "The whsec_ signing secret above is shown only once and cannot be retrieved again. Store it securely now.",
    });
  }

  // The allowlist drops arguments, but dropping them in silence is how
  // `marketing_consent` stayed unreachable for a whole release while every
  // call returned 201. Naming the ignored keys lets a caller self-correct.
  if (dropped.length > 0) {
    content.push({
      type: "text",
      text: `Ignored undeclared arguments, which were not sent to the API: ${dropped.join(", ")}. Check this tool's inputSchema for the field you meant.`,
    });
  }

  return { content, isError: exitCode !== 0 };
}

// Tool-level failures (bad arguments, missing key, API errors) are isError
// results, so the calling model can read them and correct course. JSON-RPC
// errors are reserved for protocol misuse (unknown method/tool, parse errors).
export function toolError(message: string): ToolResult {
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify({ ok: false, error: { type: "usage_error", message } }, null, 2),
      },
    ],
    isError: true,
  };
}
