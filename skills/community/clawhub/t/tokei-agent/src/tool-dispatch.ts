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

// Guidance appended to both MCP servers' `initialize` instructions (mcp.ts and
// the remote /mcp route). MCP clients never see cli/SKILL.md, so this is the
// only place a connector user's model learns skins, the build recipe and the
// approval rule. Keep it in step with SKILL.md's skin guide and Rule 4.
export const AGENT_GUIDANCE = [
  'Page skins (pages_update "template", templates_list "skin"): "basic-new" (Basic) is the classic giveaway card with entry actions in a vertical list — the closest match when a user asks for a Gleam-style or KickoffLabs-style giveaway, and the default. "showcase" is a two-column, product-forward layout suited to Product Hunt-style launches. "future" is a dark, game-style skin for gaming and tech audiences. "simple" is the Custom template, bare markup styled with custom_css.',
  "To build a page from a description or a screenshot of an existing promotion: (1) templates_list, then pick the closest template by name, tags and skin — never guess a slug; (2) pages_clone it as a draft; (3) actions_catalog, then map each entry button to a writable actionType and that type's config fields — a button with no matching type becomes a custom link row, and a \"Visit Our X\" button becomes a custom link labelled \"Visit our X\" with a lowercase o, because a capital-O \"Visit Our \" label is reserved for the page's campaign-URL button and is a 422 on any other link; (4) pages_get, then pages_update with the complete entry_methods, prizes and reward_thresholds lists plus title, description, end_date and appearance fields; (5) media_upload for images, then set the media slots with pages_update — if the user attached an image and your media_upload takes only source_url, say at once that it needs a public https URL and offer three routes: copy the image address from the source page, upload it in the Tokei dashboard, or use the tokei-agent CLI, whose media_upload takes file_path; never leave a media slot empty without saying why; (6) tell the user what you could not copy. Copy exactly what the screenshot shows and nothing more: replace the template's entry_methods wholesale, never keep template actions the screenshot lacks, and send reward_thresholds as [] unless tiers are visible. A template that ships no matching actions is fine as a base. When a handle, link or app id cannot be read from the screenshot, make a plausible guess and say which values you guessed. Share Feedback (survey), Quick Question and the Secret Code toggle are not entry_methods rows: set them with pages_update's standalone_actions (an enabled Quick Question needs text and 2-6 titled options). Rows of one action type share a single points value, so every duplicate row of a type must send the same points; a non-zero points on such a row is that type's entry value for the whole promotion (max 99). The secret codes themselves, daily-bonus and referral settings, country restrictions, email-provider connections and pixel-exact layouts are set in the Tokei dashboard, not through these tools. Do not tell the user that more points mean better odds of winning.",
  "Ask the user before any call that changes a public page or reaches real people: pages_publish, pages_unpublish, pages_clone with status active, pages_update on an active page, entries_create and webhooks_create. Tokei does not gate these calls, so you are the gate. Read-only tools need no approval.",
].join(" ");
