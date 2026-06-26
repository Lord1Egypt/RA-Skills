import type { TaskRunDetailPayload } from "../runtime/index.js";
import type { WTTCloudClient } from "../ws-client.js";

export type WTTCommandName =
  | "list"
  | "find"
  | "join"
  | "leave"
  | "publish"
  | "poll"
  | "history"
  | "p2p"
  | "detail"
  | "subscribed"
  | "task"
  | "pipeline"
  | "delegate"
  | "config"
  | "bind"
  | "setup"
  | "update"
  | "version"
  | "help";

export type ParsedWTTCommand =
  | { name: "list"; limit?: number }
  | { name: "find"; query: string }
  | { name: "join"; topicId: string }
  | { name: "leave"; topicId: string }
  | { name: "publish"; topicId: string; content: string }
  | { name: "poll"; limit?: number }
  | { name: "history"; topicId: string; limit?: number }
  | { name: "p2p"; agentId: string; content: string }
  | { name: "detail"; topicId: string }
  | { name: "subscribed" }
  | { name: "task"; action: "list" }
  | { name: "task"; action: "detail"; taskId: string }
  | { name: "task"; action: "create"; title: string; description?: string }
  | { name: "task"; action: "run"; taskId: string }
  | { name: "task"; action: "review"; taskId: string; reviewAction: "approve" | "reject" | "block"; comment?: string }
  | { name: "pipeline"; action: "list" }
  | { name: "pipeline"; action: "create"; nameArg: string; description?: string }
  | { name: "pipeline"; action: "run"; pipelineId: string }
  | { name: "delegate"; action: "list" }
  | { name: "delegate"; action: "create"; targetAgentId: string }
  | { name: "delegate"; action: "remove"; targetAgentId: string }
  | { name: "config"; mode: "show" | "auto" }
  | { name: "bind" }
  | { name: "setup"; agentId: string; token: string; cloudUrl?: string }
  | { name: "update" }
  | { name: "version" }
  | { name: "help" }
  | { name: "invalid"; reason: string; usage?: string };

export type WTTCommandClient = Pick<
  WTTCloudClient,
  | "connected"
  | "list"
  | "find"
  | "join"
  | "leave"
  | "publish"
  | "poll"
  | "history"
  | "p2p"
  | "detail"
  | "subscribed"
  | "decryptMessage"
>;

export interface WTTCommandAccountContext {
  accountId: string;
  name?: string;
  source?: string;
  cloudUrl?: string;
  agentId?: string;
  token?: string;
  enabled?: boolean;
  configured?: boolean;
}

export interface WTTFetchResponseLike {
  ok: boolean;
  status: number;
  statusText?: string;
  json: () => Promise<unknown>;
  text: () => Promise<string>;
}

export type WTTFetchLike = (
  input: string,
  init?: {
    method?: string;
    headers?: Record<string, string>;
    body?: string;
    signal?: AbortSignal;
  },
) => Promise<WTTFetchResponseLike>;

export interface WTTTaskInferenceRuntimeRequest {
  taskId: string;
  prompt: string;
  task: TaskRunDetailPayload;
  accountId: string;
}

export interface WTTTaskInferenceUsage {
  promptTokens?: number;
  completionTokens?: number;
  cacheReadTokens?: number;
  cacheWriteTokens?: number;
  totalTokens?: number;
  source?: string;
  provider?: string;
  model?: string;
}

export interface WTTTaskInferenceRuntimeResult {
  outputText: string;
  provider?: string;
  usage?: WTTTaskInferenceUsage;
  raw?: unknown;
}

export interface WTTSessionRuntimeMetrics {
  source?: string;
  queueDepth?: number;
  queueMode?: string;
  sessionKey?: string;
  inflight?: boolean;
}

export interface WTTCommandRuntimeHooks {
  dispatchTaskInference?: (
    params: WTTTaskInferenceRuntimeRequest,
  ) => Promise<WTTTaskInferenceRuntimeResult>;
  getSessionRuntimeMetrics?: (params: {
    taskId: string;
    topicId?: string;
    accountId: string;
  }) => Promise<WTTSessionRuntimeMetrics | undefined>;
}

export interface WTTCommandExecutionContext {
  accountId: string;
  account?: WTTCommandAccountContext;
  clientConnected?: boolean;
  client?: WTTCommandClient;
  fetchImpl?: WTTFetchLike;
  runtimeHooks?: WTTCommandRuntimeHooks;
}

export interface WTTCommandProcessResult {
  handled: boolean;
  response?: string;
  accountId?: string;
  command?: ParsedWTTCommand["name"];
}
