import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { renderAllToolsSchemaJson, renderInvokeScript, renderSkillMarkdown, renderToolsSchemaJson } from "./render.js";
import type {
  GeneratedSkill,
  GeneratedSkillBundle,
  GeneratorOptions,
  JsonSchema,
  McpToolDefinition,
  ResolvedBridgeUrls,
} from "./types.js";

function isObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function formatError(error: unknown): string {
  return error instanceof Error ? error.message : String(error);
}

function normalizeUrl(input: string): URL {
  try {
    return new URL(input);
  } catch (error) {
    throw new Error(`Invalid bridge URL "${input}": ${formatError(error)}`);
  }
}

function joinUrl(origin: string, pathname: string): string {
  return pathname ? `${origin}${pathname}` : origin;
}

export function resolveBridgeUrls(rawInputUrl: string): ResolvedBridgeUrls {
  const url = normalizeUrl(rawInputUrl);
  const trimmedPath = url.pathname.replace(/\/+$/, "");

  let bridgePath = trimmedPath;
  if (bridgePath.endsWith("/mcp/tools")) {
    bridgePath = bridgePath.slice(0, -"/mcp/tools".length);
  } else if (bridgePath.endsWith("/mcp")) {
    bridgePath = bridgePath.slice(0, -"/mcp".length);
  }

  const baseUrl = joinUrl(url.origin, bridgePath);

  return {
    rawInputUrl,
    baseUrl,
    toolCatalogUrl: `${baseUrl}/mcp/tools`,
    toolInvokeBaseUrl: `${baseUrl}/mcp/tools`,
  };
}

function toKebabCase(value: string): string {
  return value
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function deriveBaseSkillName(outputDir: string, explicitSkillName?: string): string {
  if (explicitSkillName) {
    return toKebabCase(explicitSkillName) || "generated-mcp-skill";
  }

  const folderName = path.basename(path.resolve(outputDir));
  return toKebabCase(folderName) || "generated-mcp-skill";
}

async function fetchJson(url: string, init?: RequestInit): Promise<unknown> {
  const response = await fetch(url, init);
  const body = await response.text();

  if (!response.ok) {
    const message = body.trim() || response.statusText;
    throw new Error(`${response.status} ${response.statusText}: ${message}`);
  }

  try {
    return body ? JSON.parse(body) : null;
  } catch (error) {
    throw new Error(`Expected JSON response from ${url}: ${formatError(error)}`);
  }
}

function extractTools(payload: unknown): unknown[] {
  if (Array.isArray(payload)) {
    return payload;
  }

  if (isObject(payload) && Array.isArray(payload.tools)) {
    return payload.tools;
  }

  throw new Error("Bridge response does not contain a tools array.");
}

function normalizeSchema(schema: unknown): JsonSchema {
  if (!isObject(schema)) {
    return {
      type: "object",
      additionalProperties: true,
      description: "No input schema was returned by the bridge.",
    };
  }

  return schema as JsonSchema;
}

function normalizeTool(tool: unknown, index: number): McpToolDefinition {
  if (!isObject(tool)) {
    throw new Error(`Tool at index ${index} is not an object.`);
  }

  if (typeof tool.name !== "string" || tool.name.trim() === "") {
    throw new Error(`Tool at index ${index} is missing a valid name.`);
  }

  return {
    name: tool.name.trim(),
    description:
      typeof tool.description === "string" && tool.description.trim() !== ""
        ? tool.description.trim()
        : `MCP tool ${tool.name.trim()}.`,
    inputSchema: normalizeSchema(tool.inputSchema),
  };
}

async function fetchBridgeTools(resolvedUrls: ResolvedBridgeUrls, token?: string): Promise<McpToolDefinition[]> {
  const headers = new Headers({ Accept: "application/json" });
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const payload = await fetchJson(resolvedUrls.toolCatalogUrl, {
    method: "GET",
    headers,
  });

  const tools = extractTools(payload).map(normalizeTool).sort((left, right) => left.name.localeCompare(right.name));
  if (tools.length === 0) {
    throw new Error("Bridge returned an empty tool list.");
  }

  return tools;
}

function groupKeyFromToolName(name: string): string {
  if (name.includes("_") || name.includes("-")) {
    const prefix = name.split(/[_-]/).find(Boolean);
    return toKebabCase(prefix ?? "general") || "general";
  }

  const camelPrefix = name.match(/^[A-Z]?[a-z]+/)?.[0];
  return toKebabCase(camelPrefix ?? name) || "general";
}

function groupTools(
  tools: McpToolDefinition[],
  splitBy: "none" | "prefix",
): Array<{ groupKey: string; tools: McpToolDefinition[] }> {
  if (splitBy === "none") {
    return [{ groupKey: "all", tools }];
  }

  const groups = new Map<string, McpToolDefinition[]>();
  for (const tool of tools) {
    const groupKey = groupKeyFromToolName(tool.name);
    const existing = groups.get(groupKey) ?? [];
    existing.push(tool);
    groups.set(groupKey, existing);
  }

  return [...groups.entries()]
    .sort(([left], [right]) => left.localeCompare(right))
    .map(([groupKey, groupedTools]) => ({
      groupKey,
      tools: groupedTools.sort((left, right) => left.name.localeCompare(right.name)),
    }));
}

function describeSkill(
  baseSkillName: string,
  groupKey: string,
  tools: McpToolDefinition[],
  splitBy: "none" | "prefix",
): { skillName: string; description: string } {
  if (splitBy === "none") {
    return {
      skillName: baseSkillName,
      description: `Use this skill when the user needs capabilities exposed by the local MCP bridge. It wraps ${tools.length} MCP tool${tools.length === 1 ? "" : "s"} behind a local Node.js wrapper.`,
    };
  }

  return {
    skillName: `${baseSkillName}-${groupKey}`,
    description: `Use this skill when the user needs ${groupKey}-related capabilities exposed by the local MCP bridge. It wraps ${tools.length} MCP tool${tools.length === 1 ? "" : "s"} behind a local Node.js wrapper.`,
  };
}

function buildSkillOutputDir(
  rootOutputDir: string,
  splitBy: "none" | "prefix",
  skillName: string,
): string {
  if (splitBy === "none") {
    return rootOutputDir;
  }

  return path.join(rootOutputDir, skillName);
}

export async function generateOpenClawSkills(options: GeneratorOptions): Promise<GeneratedSkillBundle> {
  const splitBy = options.splitBy ?? "none";
  const resolvedUrls = resolveBridgeUrls(options.bridgeBaseUrl);
  const tools = await fetchBridgeTools(resolvedUrls, options.token);
  const baseSkillName = deriveBaseSkillName(options.outputDir, options.skillName);
  const groups = groupTools(tools, splitBy);
  const rootOutputDir = path.resolve(options.outputDir);

  const skills: GeneratedSkill[] = groups.map(({ groupKey, tools: groupedTools }) => {
    const { skillName, description } = describeSkill(baseSkillName, groupKey, groupedTools, splitBy);
    return {
      skillName,
      description,
      tools: groupedTools,
      skillMarkdown: renderSkillMarkdown({
        skillName,
        description,
        tools: groupedTools,
        resolvedUrls,
        homepage: options.homepage,
      }),
      invokeScript: renderInvokeScript(resolvedUrls),
      toolsSchemaJson: renderToolsSchemaJson({
        skillName,
        description,
        resolvedUrls,
        tools: groupedTools,
      }),
      resolvedUrls,
      outputDir: buildSkillOutputDir(rootOutputDir, splitBy, skillName),
      groupKey,
    };
  });

  const bundle: GeneratedSkillBundle = {
    rootOutputDir,
    resolvedUrls,
    splitBy,
    allTools: tools,
    allToolsSchemaJson: "",
    skills,
  };

  bundle.allToolsSchemaJson = renderAllToolsSchemaJson(bundle);
  return bundle;
}

async function writeSkillPackage(skill: GeneratedSkill) {
  const scriptsDir = path.join(skill.outputDir, "scripts");
  const schemaDir = path.join(skill.outputDir, "schema");

  await mkdir(scriptsDir, { recursive: true });
  await mkdir(schemaDir, { recursive: true });

  await Promise.all([
    writeFile(path.join(skill.outputDir, "SKILL.md"), skill.skillMarkdown, "utf8"),
    writeFile(path.join(scriptsDir, "invoke.js"), skill.invokeScript, {
      encoding: "utf8",
      mode: 0o755,
    }),
    writeFile(path.join(schemaDir, "tools.json"), skill.toolsSchemaJson, "utf8"),
  ]);
}

export async function writeOpenClawSkills(options: GeneratorOptions): Promise<GeneratedSkillBundle> {
  const bundle = await generateOpenClawSkills(options);

  await Promise.all(bundle.skills.map((skill) => writeSkillPackage(skill)));

  if (bundle.splitBy !== "none") {
    const rootSchemaDir = path.join(bundle.rootOutputDir, "schema");
    await mkdir(rootSchemaDir, { recursive: true });
    await writeFile(path.join(rootSchemaDir, "tools.json"), bundle.allToolsSchemaJson, "utf8");
  }

  return bundle;
}
