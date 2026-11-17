export type BasicAuth = { user: string; pass: string };

export type StructuredError = {
  code: string;
  message: string;
  retriable: boolean;
  service: string;
  endpoint: string;
  status?: number;
};

export type RpcRequest = {
  jsonrpc: '2.0';
  id: string | number;
  method: string;
  params: Record<string, unknown>;
};
