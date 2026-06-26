export type RuntimeReviewAction = "approve" | "reject" | "block";

export type RuntimeTransitionIntent =
  | { kind: "run" }
  | { kind: "review"; action: RuntimeReviewAction };

export interface RuntimeTransitionResult {
  allowed: boolean;
  fromStatus: string;
  toStatus: string;
  reason: string;
  nextAction: string;
}

const STATUS_ALIASES: Record<string, string> = {
  open: "todo",
  ready: "todo",
  approved: "done",
  rejected: "blocked",
};

const ALLOWED_TRANSITIONS: Record<string, Set<string>> = {
  todo: new Set(["doing", "blocked", "cancelled"]),
  doing: new Set(["review", "blocked", "todo", "cancelled", "done"]),
  review: new Set(["done", "doing", "blocked", "cancelled"]),
  blocked: new Set(["todo", "doing", "cancelled"]),
  done: new Set(["doing"]),
  cancelled: new Set(["todo"]),
};

function normalizeStatus(status: string | undefined): string {
  if (!status) return "unknown";
  const normalized = status.trim().toLowerCase();
  if (!normalized) return "unknown";
  return STATUS_ALIASES[normalized] ?? normalized;
}

function reviewTargetStatus(action: RuntimeReviewAction): string {
  if (action === "approve") return "done";
  if (action === "reject") return "doing";
  return "blocked";
}

function canTransition(fromStatus: string, toStatus: string): boolean {
  if (fromStatus === toStatus) return true;
  const allowed = ALLOWED_TRANSITIONS[fromStatus];
  if (!allowed) return false;
  return allowed.has(toStatus);
}

export function validateTaskTransition(params: {
  currentStatus?: string;
  intent: RuntimeTransitionIntent;
}): RuntimeTransitionResult {
  const fromStatus = normalizeStatus(params.currentStatus);

  if (params.intent.kind === "run") {
    const toStatus = "doing";

    if (canTransition(fromStatus, toStatus)) {
      return {
        allowed: true,
        fromStatus,
        toStatus,
        reason: `状态允许执行 run：${fromStatus} -> ${toStatus}`,
        nextAction: "将任务推进为 doing，并由执行体持续上报进展。",
      };
    }

    if (fromStatus === "unknown") {
      return {
        allowed: false,
        fromStatus,
        toStatus: fromStatus,
        reason: "无法确认任务状态，禁止直接 run。",
        nextAction: "先执行 @wtt task detail <task_id> 核对状态后再重试。",
      };
    }

    return {
      allowed: false,
      fromStatus,
      toStatus: fromStatus,
      reason: `状态不允许 run：${fromStatus} -> ${toStatus}`,
      nextAction: "请先通过任务系统调整状态后再执行 run。",
    };
  }

  const toStatus = reviewTargetStatus(params.intent.action);

  if (canTransition(fromStatus, toStatus)) {
    return {
      allowed: true,
      fromStatus,
      toStatus,
      reason: `review 动作允许：${fromStatus} -> ${toStatus}`,
      nextAction: "可继续调用 review API 落地审查结果。",
    };
  }

  if (fromStatus === "unknown") {
    return {
      allowed: false,
      fromStatus,
      toStatus,
      reason: "无法确认当前状态，禁止直接 review。",
      nextAction: "先执行 @wtt task detail <task_id> 获取最新状态。",
    };
  }

  return {
    allowed: false,
    fromStatus,
    toStatus,
    reason: `review 约束不满足：${fromStatus} -> ${toStatus}`,
    nextAction: "将任务状态调整到允许区间后再执行 review。",
  };
}
