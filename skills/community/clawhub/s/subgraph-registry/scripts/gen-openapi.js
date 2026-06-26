#!/usr/bin/env node

/**
 * gen-openapi.js
 *
 * Generates the OpenAPI 3.1 spec for subgraph-registry by importing the
 * declarative TOOLS array + REST_ROUTES table from src/index.js. Single
 * source of truth: if a tool is added to src/index.js, the next run of
 * this script captures it automatically.
 *
 * Outputs:
 *   openapi.yaml          — committed alongside the source code
 *   data/openapi.json     — bundled in the npm tarball + served at
 *                           /.well-known/openapi.json by the HTTP transport
 *
 * Wired into CI via .github/workflows/update-registry.yml (regenerated
 * on every release) and .github/workflows/test.yml (drift check fails
 * the PR if openapi.yaml is stale).
 */

import { writeFileSync, mkdirSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const REPO_ROOT = join(__dirname, "..");

// Importing src/index.js spawns nothing thanks to the `_isMain` guard
// at the bottom of that file. We get TOOLS + REST_ROUTES as plain
// exports.
const { TOOLS, REST_ROUTES } = await import(join(REPO_ROOT, "src", "index.js"));

const pkg = JSON.parse(
  await import("fs").then((m) =>
    m.readFileSync(join(REPO_ROOT, "package.json"), "utf8"),
  ),
);

// ── OpenAPI document scaffold ──────────────────────────────
const spec = {
  openapi: "3.1.0",
  info: {
    title: "Subgraph Registry",
    description:
      "Agent-friendly subgraph discovery on The Graph Network. 14,700+ classified subgraphs with semantic search, reliability scoring, schema-evolution tracking, and x402 query URLs ($0.01 USDC on Base, no API key).",
    version: pkg.version,
    license: { name: "MIT" },
    contact: {
      name: "PaulieB14",
      url: "https://github.com/PaulieB14/subgraph-registry",
    },
  },
  servers: [
    {
      url: "http://localhost:3848",
      description: "Local MCP HTTP transport (default port)",
    },
  ],
  paths: {},
  components: {
    schemas: {
      ToolError: {
        type: "object",
        properties: {
          error: { type: "string" },
        },
        required: ["error"],
      },
    },
  },
};

// Build a short summary from the description: prefer the first
// sentence, then fall back to a word-boundary truncation under 120
// chars. Avoids the mid-word cut "...identifies the protocol_type and ent"
// that Swagger UI renders awkwardly.
function shortSummary(desc) {
  if (!desc) return "";
  const firstSentence = desc.split(/(?<=\.)\s/)[0];
  if (firstSentence && firstSentence.length <= 120) return firstSentence;
  if (desc.length <= 120) return desc;
  // Word-boundary truncation
  const cut = desc.slice(0, 120);
  const lastSpace = cut.lastIndexOf(" ");
  return (lastSpace > 60 ? cut.slice(0, lastSpace) : cut).trimEnd() + "…";
}

// ── MCP tools → POST /mcp/tools/{name} ─────────────────────
// Each tool's JSON Schema inputSchema drops directly into the request
// body schema — MCP tool schemas are OpenAPI-compatible by design.
for (const tool of TOOLS) {
  spec.paths[`/mcp/tools/${tool.name}`] = {
    post: {
      operationId: `tool_${tool.name}`,
      summary: shortSummary(tool.description),
      description: tool.description,
      tags: ["mcp-tools"],
      requestBody: {
        required:
          Array.isArray(tool.inputSchema?.required) &&
          tool.inputSchema.required.length > 0,
        content: {
          "application/json": {
            schema: tool.inputSchema || { type: "object" },
          },
        },
      },
      responses: {
        200: {
          description: "Tool result (JSON-encoded)",
          content: {
            "application/json": {
              schema: { type: "object" },
            },
          },
        },
        400: {
          description: "Invalid input",
          content: {
            "application/json": {
              schema: { $ref: "#/components/schemas/ToolError" },
            },
          },
        },
      },
    },
  };
}

// ── REST routes → declarative inventory ────────────────────
for (const r of REST_ROUTES) {
  // OpenAPI uses {brace} path params; src/index.js uses Express :colon.
  // REST_ROUTES already stores the OpenAPI form so no conversion needed.
  if (!spec.paths[r.path]) spec.paths[r.path] = {};
  spec.paths[r.path][r.method] = {
    operationId: `rest_${r.method}_${r.path
      .replace(/[^a-zA-Z0-9]+/g, "_")
      .replace(/^_+|_+$/g, "")}`,
    summary: r.summary,
    tags: ["rest"],
    ...(r.parameters ? { parameters: r.parameters } : {}),
    responses: {
      200: {
        description: r.response?.description || "Success",
        content: {
          "application/json": {
            schema: r.response || { type: "object" },
          },
        },
      },
      404: {
        description: "Not found",
        content: {
          "application/json": {
            schema: { $ref: "#/components/schemas/ToolError" },
          },
        },
      },
    },
  };
}

// ── Write JSON + YAML ──────────────────────────────────────
mkdirSync(join(REPO_ROOT, "data"), { recursive: true });
const jsonPath = join(REPO_ROOT, "data", "openapi.json");
writeFileSync(jsonPath, JSON.stringify(spec, null, 2) + "\n");

// Minimal YAML emitter — avoids pulling in a dep just for this. Keys
// in the spec are always strings; values are strings, numbers, bools,
// arrays, or objects. Strings that contain YAML-significant chars get
// JSON-quoted (which YAML accepts).
function toYaml(value, indent = 0) {
  const pad = "  ".repeat(indent);
  if (value === null) return "null";
  if (typeof value === "boolean" || typeof value === "number") {
    return String(value);
  }
  if (typeof value === "string") {
    // Always quote with JSON-style — safe for all unicode + special chars.
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) {
    if (value.length === 0) return "[]";
    return value
      .map((item) => {
        const rendered = toYaml(item, indent + 1);
        if (typeof item === "object" && item !== null) {
          // Multi-line object under array dash.
          const lines = rendered.split("\n");
          return `${pad}- ${lines[0].trimStart()}${lines
            .slice(1)
            .map((l) => "\n" + l)
            .join("")}`;
        }
        return `${pad}- ${rendered}`;
      })
      .join("\n");
  }
  if (typeof value === "object") {
    const keys = Object.keys(value);
    if (keys.length === 0) return "{}";
    return keys
      .map((k) => {
        const v = value[k];
        const safeKey = /^[A-Za-z_][A-Za-z0-9_./-]*$/.test(k)
          ? k
          : JSON.stringify(k);
        if (
          v === null ||
          typeof v === "boolean" ||
          typeof v === "number" ||
          typeof v === "string"
        ) {
          return `${pad}${safeKey}: ${toYaml(v, indent + 1)}`;
        }
        if (Array.isArray(v) && v.length === 0) return `${pad}${safeKey}: []`;
        if (
          typeof v === "object" &&
          !Array.isArray(v) &&
          Object.keys(v).length === 0
        ) {
          return `${pad}${safeKey}: {}`;
        }
        return `${pad}${safeKey}:\n${toYaml(v, indent + 1)}`;
      })
      .join("\n");
  }
  return JSON.stringify(value);
}

const yamlPath = join(REPO_ROOT, "openapi.yaml");
const banner =
  "# Auto-generated by scripts/gen-openapi.js — do not edit by hand.\n" +
  "# Source: src/index.js TOOLS[] + REST_ROUTES[]. Regenerate via\n" +
  "#   node scripts/gen-openapi.js\n";
writeFileSync(yamlPath, banner + toYaml(spec) + "\n");

console.log(`wrote ${jsonPath}`);
console.log(`wrote ${yamlPath}`);
console.log(
  `tools: ${TOOLS.length}, rest routes: ${REST_ROUTES.length}, total paths: ${Object.keys(spec.paths).length}`,
);
