import type {
  GeneratedSkillBundle,
  JsonPrimitive,
  JsonSchema,
  JsonValue,
  McpToolDefinition,
  ResolvedBridgeUrls,
  ToolArgumentSummary,
} from "./types.js";

function formatJsonValue(value: JsonPrimitive | JsonValue): string {
  return JSON.stringify(value);
}

function getSchemaTypes(schema: JsonSchema): string[] {
  if (Array.isArray(schema.type)) {
    return schema.type;
  }

  if (schema.type) {
    return [schema.type];
  }

  if (schema.oneOf?.length) {
    return schema.oneOf.flatMap(getSchemaTypes);
  }

  if (schema.anyOf?.length) {
    return schema.anyOf.flatMap(getSchemaTypes);
  }

  if (schema.allOf?.length) {
    return schema.allOf.flatMap(getSchemaTypes);
  }

  if (schema.properties || schema.additionalProperties !== undefined) {
    return ["object"];
  }

  if (schema.items) {
    return ["array"];
  }

  return ["unknown"];
}

function getArrayItemSchema(items: JsonSchema | JsonSchema[] | undefined): JsonSchema | undefined {
  if (!items) {
    return undefined;
  }

  return Array.isArray(items) ? items[0] : items;
}

export function describeSchemaType(schema: JsonSchema): string {
  if (schema.const !== undefined) {
    return `const ${formatJsonValue(schema.const)}`;
  }

  if (schema.enum?.length) {
    const values = schema.enum.map(formatJsonValue).join(", ");
    return `${getSchemaTypes(schema).join(" | ")} (one of: ${values})`;
  }

  if (schema.oneOf?.length) {
    return schema.oneOf.map(describeSchemaType).join(" | ");
  }

  if (schema.anyOf?.length) {
    return schema.anyOf.map(describeSchemaType).join(" | ");
  }

  if (schema.allOf?.length) {
    return schema.allOf.map(describeSchemaType).join(" & ");
  }

  const normalizedTypes = getSchemaTypes(schema).map((type) => {
    if (type === "array") {
      const itemSchema = getArrayItemSchema(schema.items);
      return itemSchema ? `array<${describeSchemaType(itemSchema)}>` : "array<unknown>";
    }

    if (type === "object" && schema.additionalProperties && !schema.properties) {
      return "object<string, unknown>";
    }

    return type;
  });

  const uniqueTypes = [...new Set(normalizedTypes)];

  if (schema.nullable && !uniqueTypes.includes("null")) {
    uniqueTypes.push("null");
  }

  return uniqueTypes.join(" | ");
}

export function summarizeToolArguments(schema: JsonSchema): ToolArgumentSummary[] {
  const properties = schema.properties ?? {};
  const required = new Set(schema.required ?? []);

  return Object.entries(properties).map(([name, propertySchema]) => ({
    name,
    type: describeSchemaType(propertySchema),
    required: required.has(name),
    description: propertySchema.description?.trim(),
  }));
}

function renderArgumentLines(tool: McpToolDefinition): string {
  const argumentsSummary = summarizeToolArguments(tool.inputSchema);
  if (argumentsSummary.length === 0) {
    return "- none";
  }

  return argumentsSummary
    .map((argument) => {
      const suffix = argument.description ? `: ${argument.description}` : "";
      return `- ${argument.name} (${argument.type}, ${argument.required ? "required" : "optional"})${suffix}`;
    })
    .join("\n");
}

function escapeFrontmatterString(value: string): string {
  return value.replace(/\\/g, "\\\\").replace(/"/g, '\\"');
}

function renderToolSection(tool: McpToolDefinition): string {
  return [
    `### ${tool.name}`,
    tool.description || "No description provided.",
    "",
    "Arguments:",
    renderArgumentLines(tool),
    "",
  ].join("\n");
}

export function renderSkillMarkdown(input: {
  skillName: string;
  description: string;
  tools: McpToolDefinition[];
  resolvedUrls: ResolvedBridgeUrls;
  homepage?: string;
}): string {
  const metadata = JSON.stringify({
    openclaw: {
      emoji: "🧰",
      requires: {
        bins: ["node"],
        env: ["MY_MCP_TOKEN"],
      },
      primaryEnv: "MY_MCP_TOKEN",
      ...(input.homepage ? { homepage: input.homepage } : {}),
    },
  });

  return [
    "---",
    `name: ${input.skillName}`,
    `description: "${escapeFrontmatterString(input.description)}"`,
    "allowed-tools: Bash, Read",
    `metadata: ${metadata}`,
    "---",
    "",
    `# ${input.skillName}`,
    "",
    input.description,
    "",
    `This skill targets the local MCP bridge at \`${input.resolvedUrls.baseUrl}\` by default. Tool schemas are cached in \`{baseDir}/schema/tools.json\`.`,
    "",
    "## Available tools",
    "",
    ...input.tools.map((tool) => renderToolSection(tool)),
    "## How to invoke",
    "",
    "When you need one of the tools above, run:",
    "",
    "`node {baseDir}/scripts/invoke.js <tool-name> '<json-args>'`",
    "",
    "Pass valid JSON as the second argument.",
    "Do not invent fields not present in the tool schema.",
    "If the skill is unavailable, configure `skills.entries." + input.skillName + ".apiKey` first.",
    "Optionally set `skills.entries." + input.skillName + ".env.MY_MCP_BASE_URL` to point at your local bridge.",
    "",
  ].join("\n");
}

export function renderInvokeScript(resolvedUrls: ResolvedBridgeUrls): string {
  return `#!/usr/bin/env node
const DEFAULT_BASE_URL = ${JSON.stringify(resolvedUrls.baseUrl)};

function normalizeBaseUrl(value) {
  return value.replace(/\\/+$/, "");
}

async function main() {
  const [, , toolName, rawArgs] = process.argv;

  if (!toolName) {
    console.error("Missing tool name");
    process.exit(1);
  }

  let args = {};
  if (rawArgs) {
    try {
      args = JSON.parse(rawArgs);
    } catch (error) {
      console.error(\`Invalid JSON arguments: \${error instanceof Error ? error.message : String(error)}\`);
      process.exit(4);
    }
  }

  if (!args || typeof args !== "object" || Array.isArray(args)) {
    console.error("Arguments must be a JSON object");
    process.exit(4);
  }

  const token = process.env.MY_MCP_TOKEN;
  if (!token) {
    console.error("Missing MY_MCP_TOKEN");
    process.exit(2);
  }

  const baseUrl = normalizeBaseUrl(process.env.MY_MCP_BASE_URL || DEFAULT_BASE_URL || "http://127.0.0.1:8787");
  const response = await fetch(\`\${baseUrl}/mcp/tools/\${encodeURIComponent(toolName)}\`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      authorization: \`Bearer \${token}\`,
    },
    body: JSON.stringify({ arguments: args }),
  });

  const text = await response.text();
  if (!response.ok) {
    console.error(text || \`Request failed: \${response.status} \${response.statusText}\`);
    process.exit(3);
  }

  process.stdout.write(text.endsWith("\\n") ? text : \`\${text}\\n\`);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.stack || error.message : String(error));
  process.exit(10);
});
`;
}

export function renderToolsSchemaJson(input: {
  skillName: string;
  description: string;
  resolvedUrls: ResolvedBridgeUrls;
  tools: McpToolDefinition[];
}): string {
  return `${JSON.stringify(
    {
      generatedAt: new Date().toISOString(),
      skillName: input.skillName,
      description: input.description,
      bridge: input.resolvedUrls,
      tools: input.tools,
    },
    null,
    2,
  )}\n`;
}

export function renderAllToolsSchemaJson(bundle: GeneratedSkillBundle): string {
  return `${JSON.stringify(
    {
      generatedAt: new Date().toISOString(),
      splitBy: bundle.splitBy,
      bridge: bundle.resolvedUrls,
      skills: bundle.skills.map((skill) => ({
        skillName: skill.skillName,
        groupKey: skill.groupKey,
        outputDir: skill.outputDir,
        toolCount: skill.tools.length,
      })),
      tools: bundle.allTools,
    },
    null,
    2,
  )}\n`;
}
