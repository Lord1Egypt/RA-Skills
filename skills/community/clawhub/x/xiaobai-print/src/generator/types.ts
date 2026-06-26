export type JsonPrimitive = string | number | boolean | null;
export type JsonValue = JsonPrimitive | JsonValue[] | { [key: string]: JsonValue };

export interface JsonSchema {
  type?: string | string[];
  title?: string;
  description?: string;
  properties?: Record<string, JsonSchema>;
  required?: string[];
  additionalProperties?: boolean | JsonSchema;
  items?: JsonSchema | JsonSchema[];
  enum?: JsonPrimitive[];
  const?: JsonPrimitive;
  default?: JsonValue;
  examples?: JsonValue[];
  format?: string;
  nullable?: boolean;
  oneOf?: JsonSchema[];
  anyOf?: JsonSchema[];
  allOf?: JsonSchema[];
}

export interface McpToolDefinition {
  name: string;
  description: string;
  inputSchema: JsonSchema;
}

export interface GeneratorOptions {
  bridgeBaseUrl: string;
  outputDir: string;
  token?: string;
  splitBy?: "none" | "prefix";
  skillName?: string;
  homepage?: string;
}

export interface ResolvedBridgeUrls {
  rawInputUrl: string;
  baseUrl: string;
  toolCatalogUrl: string;
  toolInvokeBaseUrl: string;
}

export interface ToolArgumentSummary {
  name: string;
  type: string;
  required: boolean;
  description?: string;
}

export interface GeneratedSkill {
  skillName: string;
  description: string;
  tools: McpToolDefinition[];
  skillMarkdown: string;
  invokeScript: string;
  toolsSchemaJson: string;
  resolvedUrls: ResolvedBridgeUrls;
  outputDir: string;
  groupKey: string;
}

export interface GeneratedSkillBundle {
  rootOutputDir: string;
  resolvedUrls: ResolvedBridgeUrls;
  splitBy: "none" | "prefix";
  allTools: McpToolDefinition[];
  allToolsSchemaJson: string;
  skills: GeneratedSkill[];
}
