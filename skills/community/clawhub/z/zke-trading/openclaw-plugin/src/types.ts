export type JsonSchema = Record<string, unknown>;

export type ToolSpec = {
  name: string;
  description: string;
  inputSchema: JsonSchema;
  execute: (input: Record<string, any>, ctx?: any) => Promise<any>;
};

export type PluginConfig = {
  tradingHome?: string;
  pythonBin?: string;
};
