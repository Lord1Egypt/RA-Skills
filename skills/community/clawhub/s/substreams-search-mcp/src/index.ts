#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import { z } from "zod";
import express from "express";
import { parse } from "node-html-parser";
import {
  fetchSubstream,
  createModuleGraph,
  generateMermaidGraph,
  isMapModule,
  isStoreModule,
} from "@substreams/core";
import type { Module } from "@substreams/core/proto";

const REGISTRY_URL = "https://substreams.dev/packages";
const PAGE_SIZE = 24;
const MAX_PAGES = 50;

interface Package {
  name: string;
  url: string;
  creator: string;
  network: string;
  version: string;
  published: string;
  downloads: string;
}

function parseCards(html: string): Package[] {
  const root = parse(html);
  const grid = root.querySelector("#packages-grid");
  if (!grid) return [];

  const packages: Package[] = [];

  for (const link of grid.querySelectorAll("a.block")) {
    const href = link.getAttribute("href");
    if (!href) continue;

    const nameEl = link.querySelector("p.font-semibold");
    const name = nameEl?.text?.trim() || href.split("/")[2] || "";

    const creatorBtn = link.querySelector("button.user-filter-link");
    const creator = creatorBtn?.getAttribute("data-user") || creatorBtn?.text?.trim() || "";

    const networkBtn = link.querySelector("button.network-filter-link");
    const network = networkBtn?.getAttribute("data-network") || "";

    const bottom = link.querySelector("div.absolute");
    let version = "";
    let published = "";
    let downloads = "";

    if (bottom) {
      for (const row of bottom.querySelectorAll("div.flex-row")) {
        const labels = row.querySelectorAll("p");
        if (labels.length < 2) continue;
        const label = labels[0].text.trim().toLowerCase();
        const value = labels[labels.length - 1].text.trim();
        if (label.includes("version")) version = value;
        else if (label.includes("publish")) published = value;
        else if (label.includes("download")) downloads = value;
      }
    }

    packages.push({
      name,
      url: `https://substreams.dev${href}`,
      creator,
      network,
      version,
      published,
      downloads,
    });
  }

  return packages;
}

async function fetchPackages(
  query: string,
  sort: string = "most_downloaded",
  network?: string
): Promise<Package[]> {
  const words = query.trim().split(/\s+/);
  const searchTerm = words[0] || query;
  const extraWords = words.slice(1).map((w) => w.toLowerCase());

  const allPackages: Package[] = [];
  const seenUrls = new Set<string>();

  for (let page = 1; page <= MAX_PAGES; page++) {
    const params = new URLSearchParams({
      search: searchTerm,
      sort,
      page: String(page),
    });
    if (network) params.set("network", network);

    const resp = await fetch(`${REGISTRY_URL}?${params}`);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}: ${resp.statusText}`);

    const html = await resp.text();
    const pagePackages = parseCards(html);

    if (pagePackages.length === 0) break;

    for (const pkg of pagePackages) {
      if (!seenUrls.has(pkg.url)) {
        seenUrls.add(pkg.url);
        allPackages.push(pkg);
      }
    }

    if (pagePackages.length < PAGE_SIZE) break;
  }

  if (extraWords.length > 0) {
    return allPackages.filter((p) =>
      extraWords.every(
        (w) =>
          p.name.toLowerCase().includes(w) ||
          p.creator.toLowerCase().includes(w) ||
          p.network.toLowerCase().includes(w)
      )
    );
  }

  return allPackages;
}

const server = new McpServer({
  name: "substreams-search",
  version: "1.0.0",
});

server.registerTool(
  "search_substreams",
  {
    description:
      "Search the substreams.dev package registry for blockchain data stream packages. " +
      "Multi-word queries filter results to match all words.",
    inputSchema: {
      query: z
        .string()
        .describe("Search term, e.g. 'solana dex' or 'uniswap'"),
      sort: z
        .enum(["most_downloaded", "alphabetical", "most_used", "last_uploaded"])
        .optional()
        .default("most_downloaded")
        .describe("Sort order"),
      network: z
        .string()
        .optional()
        .describe(
          "Filter by blockchain network, e.g. 'ethereum', 'solana', 'arbitrum-one'"
        ),
    },
    annotations: { readOnlyHint: true },
  },
  async ({ query, sort, network }) => {
    const packages = await fetchPackages(query, sort, network);

    const result =
      packages.length === 0
        ? { results: [], message: `No packages found for '${query}'` }
        : { results: packages, count: packages.length };

    return {
      content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
    };
  }
);

// ---------------------------------------------------------------------------
// Package introspection helpers
// ---------------------------------------------------------------------------

function getModuleKind(mod: Module): string {
  switch (mod.kind.case) {
    case "kindMap": return "map";
    case "kindStore": return "store";
    case "kindBlockIndex": return "blockIndex";
    default: return "unknown";
  }
}

function getModuleOutputType(mod: Module): string | undefined {
  if (isMapModule(mod)) return mod.kind.value.outputType;
  if (isStoreModule(mod)) return mod.kind.value.valueType;
  if (mod.kind.case === "kindBlockIndex") return mod.kind.value.outputType;
  return undefined;
}

function getUpdatePolicy(mod: Module): string | undefined {
  if (!isStoreModule(mod)) return undefined;
  const names: Record<number, string> = {
    0: "unset", 1: "set", 2: "set_if_not_exists",
    3: "add", 4: "min", 5: "max", 6: "append", 7: "set_sum",
  };
  return names[mod.kind.value.updatePolicy] ?? "unknown";
}

function formatInput(input: Module["inputs"][number]) {
  switch (input.input.case) {
    case "source":
      return { type: "source", source: input.input.value.type };
    case "map":
      return { type: "map", source: input.input.value.moduleName };
    case "store": {
      const modeNames: Record<number, string> = { 0: "unset", 1: "get", 2: "deltas" };
      return {
        type: "store",
        source: input.input.value.moduleName,
        mode: modeNames[input.input.value.mode] ?? "unknown",
      };
    }
    case "params":
      return { type: "params", source: input.input.value.value || "(default)" };
    default:
      return { type: "unknown", source: "" };
  }
}

async function fetchSpkg(url: string) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 30_000);
  try {
    return await fetchSubstream(url, { signal: controller.signal });
  } catch (error) {
    const msg = error instanceof Error ? error.message : String(error);
    if (msg.includes("wire type") || msg.includes("invalid tag")) {
      throw new Error(
        `The URL did not return a valid .spkg file (got HTML or other non-protobuf content). ` +
        `Make sure the URL points directly to a .spkg binary, e.g. https://spkg.io/{creator}/{package}-{version}.spkg`
      );
    }
    throw error;
  } finally {
    clearTimeout(timeout);
  }
}

function textResult(data: unknown) {
  return {
    content: [{ type: "text" as const, text: JSON.stringify(data, null, 2) }],
  };
}

function errorResult(error: unknown) {
  const message = error instanceof Error ? error.message : String(error);
  return {
    content: [{ type: "text" as const, text: `Error: ${message}` }],
    isError: true,
  };
}

// ---------------------------------------------------------------------------
// Tool: inspect_package
// ---------------------------------------------------------------------------
server.registerTool(
  "inspect_package",
  {
    description:
      "Inspect a Substreams package (.spkg) to see its module graph (DAG), protobuf output types, and manifest metadata. " +
      "Pass a direct URL to a .spkg file (e.g. https://spkg.io/streamingfast/substreams-uniswap-v3-v0.2.10.spkg). " +
      "Returns package info, all modules with their inputs/outputs/dependencies, and a Mermaid diagram of the module graph.",
    inputSchema: {
      url: z.string().describe("Direct URL to a .spkg file"),
    },
    annotations: { readOnlyHint: true },
  },
  async ({ url }) => {
    try {
      const pkg = await fetchSpkg(url);
      const modules = pkg.modules?.modules ?? [];
      const graph = createModuleGraph(modules);

      const packageInfo = pkg.packageMeta.length > 0
        ? {
            name: pkg.packageMeta[0].name,
            version: pkg.packageMeta[0].version,
            doc: pkg.packageMeta[0].doc || undefined,
            url: pkg.packageMeta[0].url || undefined,
          }
        : { name: "unknown", version: "unknown" };

      const moduleDetails = modules.map((mod, index) => {
        const kind = getModuleKind(mod);
        const outputType = getModuleOutputType(mod);
        const updatePolicy = getUpdatePolicy(mod);
        const parents = graph.parentsOf(mod).map((m) => m.name);
        const children = graph.childrenOf(mod).map((m) => m.name);
        const inputs = mod.inputs.map(formatInput);
        const doc = pkg.moduleMeta[index]?.doc || undefined;

        return {
          name: mod.name,
          kind,
          ...(outputType && { outputType }),
          ...(updatePolicy && { updatePolicy }),
          initialBlock: Number(mod.initialBlock),
          inputs,
          dependsOn: parents,
          dependedBy: children,
          ...(doc && { doc }),
        };
      });

      const outputTypes = new Set<string>();
      for (const mod of modules) {
        const t = getModuleOutputType(mod);
        if (t) outputTypes.add(t);
      }

      return textResult({
        package: packageInfo,
        network: pkg.network || undefined,
        sinkModule: pkg.sinkModule || undefined,
        moduleCount: modules.length,
        modules: moduleDetails,
        outputTypes: [...outputTypes],
        protoFiles: pkg.protoFiles.map((f) => f.name).filter(Boolean),
        mermaidGraph: generateMermaidGraph(modules),
      });
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Tool: list_package_modules
// ---------------------------------------------------------------------------
server.registerTool(
  "list_package_modules",
  {
    description:
      "List all modules in a Substreams package (.spkg) with their types and inputs/outputs. " +
      "A lightweight alternative to inspect_package for a quick overview.",
    inputSchema: {
      url: z.string().describe("Direct URL to a .spkg file"),
    },
    annotations: { readOnlyHint: true },
  },
  async ({ url }) => {
    try {
      const pkg = await fetchSpkg(url);
      const modules = (pkg.modules?.modules ?? []).map((mod) => ({
        name: mod.name,
        kind: getModuleKind(mod),
        ...(getModuleOutputType(mod) && { outputType: getModuleOutputType(mod) }),
        ...(getUpdatePolicy(mod) && { updatePolicy: getUpdatePolicy(mod) }),
        inputs: mod.inputs.map(formatInput),
      }));
      return textResult({ moduleCount: modules.length, modules });
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// Sink type mappings
// ---------------------------------------------------------------------------
const SINK_TYPE_MAP: Record<string, { label: string; sinkBinary: string; dsnExample: string }> = {
  "sf.substreams.sink.sql.v1.Service": {
    label: "SQL (PostgreSQL/ClickHouse)",
    sinkBinary: "substreams-sink-sql",
    dsnExample: "psql://user:password@localhost:5432/dbname?sslmode=disable",
  },
  "sf.substreams.sink.entity.v1.Service": {
    label: "Subgraph Entities",
    sinkBinary: "substreams-sink-entity-changes",
    dsnExample: "",
  },
  "sf.substreams.sink.kv.v1.Service": {
    label: "Key-Value Store",
    sinkBinary: "substreams-sink-kv",
    dsnExample: "badger3:///tmp/kv-store",
  },
};

const OUTPUT_TYPE_TO_SINK: Record<string, string> = {
  "proto:sf.substreams.sink.database.v1.DatabaseChanges": "sql",
  "proto:sf.substreams.database.v1.DatabaseChanges": "sql",
  "proto:sf.substreams.sink.entity.v1.EntityChanges": "subgraph",
  "proto:sf.substreams.entity.v1.EntityChanges": "subgraph",
  "proto:sf.substreams.sink.kv.v1.KVOperations": "kv",
};

// Network to endpoint mapping
const NETWORK_ENDPOINTS: Record<string, string> = {
  mainnet: "mainnet.eth.streamingfast.io:443",
  ethereum: "mainnet.eth.streamingfast.io:443",
  polygon: "polygon.substreams.pinax.network:443",
  "arbitrum-one": "arbone.substreams.pinax.network:443",
  arbitrum: "arbone.substreams.pinax.network:443",
  base: "base.substreams.pinax.network:443",
  bsc: "bsc.substreams.pinax.network:443",
  optimism: "optimism.substreams.pinax.network:443",
  solana: "solana.substreams.pinax.network:443",
};

// ---------------------------------------------------------------------------
// Tool: get_sink_config
// ---------------------------------------------------------------------------
server.registerTool(
  "get_sink_config",
  {
    description:
      "Analyze a Substreams package's sink configuration. If the package has an embedded sink config (SQL schema, etc.), " +
      "it extracts and displays it with ready-to-run CLI commands. If no sink is configured but sink-compatible modules exist, " +
      "it identifies them and suggests how to set up sinking. Returns setup commands, schema, and endpoint info.",
    inputSchema: {
      url: z.string().describe("Direct URL to a .spkg file"),
    },
    annotations: { readOnlyHint: true },
  },
  async ({ url }) => {
    try {
      const pkg = await fetchSpkg(url);
      const modules = pkg.modules?.modules ?? [];
      const meta = pkg.packageMeta[0];
      const packageName = meta?.name ?? "unknown";
      const packageVersion = meta?.version ?? "unknown";
      const network = pkg.network || "unknown";
      const endpoint = NETWORK_ENDPOINTS[network] ?? `${network}.substreams.pinax.network:443`;

      // Case 1: Package has an embedded sink config
      if (pkg.sinkModule && pkg.sinkConfig) {
        const sinkTypeUrl = pkg.sinkConfig.typeUrl;
        const sinkInfo = SINK_TYPE_MAP[sinkTypeUrl];

        let embeddedSchema: string | undefined;
        if (sinkTypeUrl.includes("sql")) {
          // SQL sink configs embed the schema as UTF-8
          const raw = new TextDecoder().decode(pkg.sinkConfig.value);
          // Strip leading non-printable bytes (protobuf framing)
          const schemaStart = raw.indexOf("--");
          const createStart = raw.indexOf("CREATE");
          const start = schemaStart >= 0 ? schemaStart : createStart >= 0 ? createStart : -1;
          if (start >= 0) {
            embeddedSchema = raw.substring(start);
          }
        }

        const sinkModule = modules.find((m) => m.name === pkg.sinkModule);
        const sinkOutputType = sinkModule ? getModuleOutputType(sinkModule) : undefined;

        const commands = {
          install: sinkInfo
            ? `brew install streamingfast/tap/${sinkInfo.sinkBinary}`
            : `# Install the sink binary for ${sinkTypeUrl}`,
          setup: sinkInfo
            ? `${sinkInfo.sinkBinary} setup "${sinkInfo.dsnExample}" ${url}`
            : `# Setup sink for ${sinkTypeUrl}`,
          run: sinkInfo
            ? `${sinkInfo.sinkBinary} run "${sinkInfo.dsnExample}" ${url} -e ${endpoint}`
            : `# Run sink for ${sinkTypeUrl}`,
        };

        return textResult({
          status: "sink_configured",
          package: { name: packageName, version: packageVersion },
          network,
          endpoint,
          sink: {
            module: pkg.sinkModule,
            outputType: sinkOutputType,
            type: sinkTypeUrl,
            label: sinkInfo?.label ?? sinkTypeUrl,
          },
          ...(embeddedSchema && { embeddedSchema }),
          commands,
        });
      }

      // Case 2: No sink config, but find sink-compatible modules
      const sinkCompatible = modules
        .filter((mod) => {
          const out = getModuleOutputType(mod);
          return out && OUTPUT_TYPE_TO_SINK[out];
        })
        .map((mod) => {
          const outputType = getModuleOutputType(mod)!;
          const sinkType = OUTPUT_TYPE_TO_SINK[outputType];
          return { module: mod.name, outputType, sinkType };
        });

      if (sinkCompatible.length > 0) {
        const primary = sinkCompatible[0];
        const sinkTypeUrl = primary.sinkType === "sql"
          ? "sf.substreams.sink.sql.v1.Service"
          : primary.sinkType === "subgraph"
          ? "sf.substreams.sink.entity.v1.Service"
          : "sf.substreams.sink.kv.v1.Service";
        const sinkInfo = SINK_TYPE_MAP[sinkTypeUrl];

        return textResult({
          status: "no_sink_config_but_compatible_modules_found",
          package: { name: packageName, version: packageVersion },
          network,
          endpoint,
          compatibleModules: sinkCompatible,
          suggestion: `This package has ${sinkCompatible.length} module(s) that output sink-compatible types but no embedded sink config. ` +
            `You can still sink "${primary.module}" to ${sinkInfo?.label ?? primary.sinkType} by providing your own SQL schema.`,
          commands: sinkInfo
            ? {
                install: `brew install streamingfast/tap/${sinkInfo.sinkBinary}`,
                run: `${sinkInfo.sinkBinary} run "${sinkInfo.dsnExample}" ${url} -e ${endpoint} --output-module ${primary.module}`,
              }
            : undefined,
        });
      }

      // Case 3: No sink-compatible modules at all
      return textResult({
        status: "no_sink_support",
        package: { name: packageName, version: packageVersion },
        network,
        message:
          "This package has no sink-compatible modules. Its modules output custom protobuf types " +
          "that would need a custom consumer (not a standard SQL/subgraph/KV sink).",
        modules: modules.map((m) => ({
          name: m.name,
          outputType: getModuleOutputType(m),
        })),
      });
    } catch (error) {
      return errorResult(error);
    }
  }
);

// ---------------------------------------------------------------------------
// SSE/HTTP Transport (OpenClaw + remote agents)
// ---------------------------------------------------------------------------
function startHttpTransport(port: number) {
  const app = express();
  const sessions = new Map<string, SSEServerTransport>();

  app.get("/sse", async (req, res) => {
    const transport = new SSEServerTransport("/messages", res);
    sessions.set(transport.sessionId, transport);

    res.on("close", () => {
      sessions.delete(transport.sessionId);
    });

    await server.connect(transport);
  });

  app.post("/messages", async (req, res) => {
    const sessionId = req.query.sessionId as string;
    const transport = sessions.get(sessionId);
    if (!transport) {
      res.status(400).json({ error: "Invalid or expired session" });
      return;
    }
    await transport.handlePostMessage(req, res);
  });

  app.get("/health", (_req, res) => {
    res.json({ status: "ok", server: "substreams-search-mcp" });
  });

  app.listen(port, () => {
    console.error(`SSE transport listening on http://localhost:${port}/sse`);
  });
}

// ---------------------------------------------------------------------------
// Start server
// ---------------------------------------------------------------------------
async function main() {
  const httpPort = process.env.MCP_HTTP_PORT || (process.argv.includes("--http") ? "3849" : null);
  const httpOnly = process.argv.includes("--http-only");

  // Start SSE/HTTP transport if requested
  if (httpPort || httpOnly) {
    const port = parseInt(httpPort || "3849", 10);
    startHttpTransport(port);
  }

  // Start stdio transport (default, skip if --http-only)
  if (!httpOnly) {
    const transport = new StdioServerTransport();
    await server.connect(transport);
  }

  console.error("substreams-search-mcp running");
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
