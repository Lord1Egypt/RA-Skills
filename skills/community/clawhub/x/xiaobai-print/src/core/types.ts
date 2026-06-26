export type JsonSchema = {
  type: string;
  properties?: Record<string, unknown>;
  required?: string[];
  additionalProperties?: boolean;
  items?: unknown;
  description?: string;
};

export interface ToolDefinition {
  name: string;
  description: string;
  inputSchema: JsonSchema;
}

export interface RemoteConfig {
  token?: string;
  remoteUrl?: string;
}

export interface ToolResultText {
  type: "text";
  text: string;
}

export interface ToolInvocationResult {
  content: Array<ToolResultText | Record<string, unknown>>;
  isError?: boolean;
  [key: string]: unknown;
}
