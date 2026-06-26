export interface SessionBindingPlaceholder {
  kind: "placeholder";
  taskId: string;
  accountId: string;
  createdAt: string;
  sessionsSpawnReady: false;
  sessionsSendReady: false;
  note: string;
}

export function createSessionBindingPlaceholder(params: {
  taskId: string;
  accountId: string;
  now?: Date;
}): SessionBindingPlaceholder {
  return {
    kind: "placeholder",
    taskId: params.taskId,
    accountId: params.accountId,
    createdAt: (params.now ?? new Date()).toISOString(),
    sessionsSpawnReady: false,
    sessionsSendReady: false,
    note: "legacy sessions_* 依赖已移除；当前由插件内部执行器队列驱动。",
  };
}

export function describeSessionBindingNextAction(binding: SessionBindingPlaceholder): string {
  return [
    `会话绑定: ${binding.kind}`,
    `spawn: ${binding.sessionsSpawnReady ? "ready" : "n/a"}`,
    `send: ${binding.sessionsSendReady ? "ready" : "n/a"}`,
    "后续动作: 在内部执行器中接入真实执行体（保持 queue/heartbeat/summary 语义）。",
  ].join(" | ");
}
