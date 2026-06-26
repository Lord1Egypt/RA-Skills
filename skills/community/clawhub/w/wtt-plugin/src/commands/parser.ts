import type { ParsedWTTCommand } from "./types.js";

const PREFIX_RE = /^@wtt(?:\s+([\s\S]*))?$/i;
const SLASH_WTT_PREFIX_RE = /^\/wtt(?:\s+([\s\S]*))?$/i;
const SLASH_WTT_UPDATE_RE = /^\/wtt[-_]update(?:\s+([\s\S]*))?$/i;

export function normalizeWTTCommandText(text: string): string | null {
  const raw = text.trim();
  if (!raw) return null;

  const mentionMatch = raw.match(PREFIX_RE);
  if (mentionMatch) {
    const body = (mentionMatch[1] ?? "").trim();
    return body ? `@wtt ${body}` : "@wtt";
  }

  const slashMatch = raw.match(SLASH_WTT_PREFIX_RE);
  if (slashMatch) {
    const body = (slashMatch[1] ?? "").trim();
    return body ? `@wtt ${body}` : "@wtt";
  }

  const slashUpdateMatch = raw.match(SLASH_WTT_UPDATE_RE);
  if (slashUpdateMatch) {
    const body = (slashUpdateMatch[1] ?? "").trim();
    return body ? `@wtt update ${body}` : "@wtt update";
  }

  return null;
}

function splitFirst(input: string): [string, string] {
  const trimmed = input.trim();
  if (!trimmed) return ["", ""];
  const firstSpace = trimmed.search(/\s/);
  if (firstSpace < 0) return [trimmed, ""];
  return [trimmed.slice(0, firstSpace), trimmed.slice(firstSpace).trim()];
}

function splitFirstArgument(input: string): [string, string] {
  const trimmed = input.trim();
  if (!trimmed) return ["", ""];

  const quote = trimmed[0];
  if (quote === '"' || quote === "'") {
    let idx = 1;
    while (idx < trimmed.length) {
      if (trimmed[idx] === quote && trimmed[idx - 1] !== "\\") {
        const value = trimmed.slice(1, idx);
        const rest = trimmed.slice(idx + 1).trim();
        return [value, rest];
      }
      idx += 1;
    }
  }

  return splitFirst(trimmed);
}

function parsePositiveInt(raw: string): number | null {
  if (!raw) return null;
  if (!/^\d+$/.test(raw)) return null;
  const n = Number(raw);
  if (!Number.isSafeInteger(n) || n <= 0) return null;
  return n;
}

function parseTaskCommand(args: string): ParsedWTTCommand {
  const [subRaw, subArgs] = splitFirst(args);
  const sub = subRaw.toLowerCase();

  if (!sub) {
    return {
      name: "invalid",
      reason: "缺少 task 子命令",
      usage: "@wtt task <list|detail|create|run|review>",
    };
  }

  if (sub === "list" || sub === "ls") return { name: "task", action: "list" };

  if (sub === "detail") {
    const [taskId] = splitFirst(subArgs);
    if (!taskId) return { name: "invalid", reason: "缺少 task_id", usage: "@wtt task detail <task_id>" };
    return { name: "task", action: "detail", taskId };
  }

  if (sub === "create" || sub === "new") {
    const [title, rest] = splitFirstArgument(subArgs);
    if (!title) {
      return {
        name: "invalid",
        reason: "缺少任务标题",
        usage: "@wtt task create <title> [description]",
      };
    }
    return { name: "task", action: "create", title, description: rest || undefined };
  }

  if (sub === "run") {
    const [taskId] = splitFirst(subArgs);
    if (!taskId) return { name: "invalid", reason: "缺少 task_id", usage: "@wtt task run <task_id>" };
    return { name: "task", action: "run", taskId };
  }

  if (sub === "review") {
    const [taskId, rest] = splitFirst(subArgs);
    const [actionRaw, comment] = splitFirst(rest);
    const action = actionRaw.toLowerCase();

    if (!taskId || !action) {
      return {
        name: "invalid",
        reason: "review 需要 task_id 和动作",
        usage: "@wtt task review <task_id> <approve|reject|block> [comment]",
      };
    }

    if (action !== "approve" && action !== "reject" && action !== "block") {
      return {
        name: "invalid",
        reason: `不支持的 review 动作: ${actionRaw}`,
        usage: "@wtt task review <task_id> <approve|reject|block> [comment]",
      };
    }

    return {
      name: "task",
      action: "review",
      taskId,
      reviewAction: action,
      comment: comment || undefined,
    };
  }

  return {
    name: "invalid",
    reason: `不支持的 task 子命令: ${subRaw}`,
    usage: "@wtt task <list|detail|create|run|review>",
  };
}

function parsePipelineCommand(args: string): ParsedWTTCommand {
  const [subRaw, subArgs] = splitFirst(args);
  const sub = subRaw.toLowerCase();

  if (!sub) {
    return {
      name: "invalid",
      reason: "缺少 pipeline 子命令",
      usage: "@wtt pipeline <list|create|run>",
    };
  }

  if (sub === "list" || sub === "ls") return { name: "pipeline", action: "list" };

  if (sub === "create" || sub === "new") {
    const [nameArg, rest] = splitFirstArgument(subArgs);
    if (!nameArg) {
      return {
        name: "invalid",
        reason: "缺少流水线名称",
        usage: "@wtt pipeline create <name> [description]",
      };
    }
    return { name: "pipeline", action: "create", nameArg, description: rest || undefined };
  }

  if (sub === "run") {
    const [pipelineId] = splitFirst(subArgs);
    if (!pipelineId) {
      return {
        name: "invalid",
        reason: "缺少 pipeline_id",
        usage: "@wtt pipeline run <pipeline_id>",
      };
    }
    return { name: "pipeline", action: "run", pipelineId };
  }

  return {
    name: "invalid",
    reason: `不支持的 pipeline 子命令: ${subRaw}`,
    usage: "@wtt pipeline <list|create|run>",
  };
}

function parseDelegateCommand(args: string): ParsedWTTCommand {
  const [subRaw, subArgs] = splitFirst(args);
  const sub = subRaw.toLowerCase();

  if (!sub) {
    return {
      name: "invalid",
      reason: "缺少 delegate 子命令",
      usage: "@wtt delegate <list|create|remove>",
    };
  }

  if (sub === "list" || sub === "ls") return { name: "delegate", action: "list" };

  if (sub === "create" || sub === "add") {
    const [targetAgentId] = splitFirst(subArgs);
    if (!targetAgentId) {
      return {
        name: "invalid",
        reason: "缺少 target_agent_id",
        usage: "@wtt delegate create <target_agent_id>",
      };
    }
    return { name: "delegate", action: "create", targetAgentId };
  }

  if (sub === "remove" || sub === "delete") {
    const [targetAgentId] = splitFirst(subArgs);
    if (!targetAgentId) {
      return {
        name: "invalid",
        reason: "缺少 target_agent_id",
        usage: "@wtt delegate remove <target_agent_id>",
      };
    }
    return { name: "delegate", action: "remove", targetAgentId };
  }

  return {
    name: "invalid",
    reason: `不支持的 delegate 子命令: ${subRaw}`,
    usage: "@wtt delegate <list|create|remove>",
  };
}

export function parseWTTCommandText(text: string): ParsedWTTCommand | null {
  const normalized = normalizeWTTCommandText(text);
  if (!normalized) return null;

  const match = normalized.match(PREFIX_RE);
  if (!match) return null;

  const body = (match[1] ?? "").trim();
  if (!body) return { name: "help" };

  const [verbRaw, args] = splitFirst(body);
  const verb = verbRaw.toLowerCase();

  if (verb === "help") return { name: "help" };
  if (verb === "version" || verb === "ver") return { name: "version" };
  if (verb === "subscribed") return { name: "subscribed" };
  if (verb === "bind") return { name: "bind" };
  if (verb === "update" || verb === "upgrade") return { name: "update" };

  if (verb === "setup" || verb === "pair") {
    const [agentId, rest] = splitFirst(args);
    const [token, cloudUrl] = splitFirst(rest);
    if (!agentId || !token) {
      return {
        name: "invalid",
        reason: "setup 需要 agent_id 和 agent_token",
        usage: "@wtt setup <agent_id> <agent_token> [cloudUrl]",
      };
    }
    return {
      name: "setup",
      agentId,
      token,
      cloudUrl: cloudUrl || undefined,
    };
  }

  if (verb === "config" || verb === "cfg") {
    if (!args) return { name: "config", mode: "show" };
    const mode = args.toLowerCase();
    if (mode === "auto" || mode === "init" || mode === "setup") {
      return { name: "config", mode: "auto" };
    }
    return { name: "invalid", reason: `不支持的 config 子命令: ${args}`, usage: "@wtt config [auto]" };
  }

  if (verb === "whoami") return { name: "config", mode: "show" };

  if (verb === "task") return parseTaskCommand(args);
  if (verb === "pipeline" || verb === "pipe") return parsePipelineCommand(args);
  if (verb === "delegate") return parseDelegateCommand(args);

  if (verb === "list") {
    if (!args) return { name: "list" };
    const limit = parsePositiveInt(args);
    if (!limit) return { name: "invalid", reason: "list 的 limit 必须是正整数", usage: "@wtt list [limit]" };
    return { name: "list", limit };
  }

  if (verb === "find") {
    if (!args) return { name: "invalid", reason: "缺少查询关键词", usage: "@wtt find <query>" };
    return { name: "find", query: args };
  }

  if (verb === "join") {
    const [topicId] = splitFirst(args);
    if (!topicId) return { name: "invalid", reason: "缺少 topic_id", usage: "@wtt join <topic_id>" };
    return { name: "join", topicId };
  }

  if (verb === "leave") {
    const [topicId] = splitFirst(args);
    if (!topicId) return { name: "invalid", reason: "缺少 topic_id", usage: "@wtt leave <topic_id>" };
    return { name: "leave", topicId };
  }

  if (verb === "publish") {
    const [topicId, content] = splitFirst(args);
    if (!topicId || !content) {
      return { name: "invalid", reason: "publish 需要 topic_id 和内容", usage: "@wtt publish <topic_id> <content>" };
    }
    return { name: "publish", topicId, content };
  }

  if (verb === "poll") {
    if (!args) return { name: "poll" };
    const limit = parsePositiveInt(args);
    if (!limit) return { name: "invalid", reason: "poll 的 limit 必须是正整数", usage: "@wtt poll [limit]" };
    return { name: "poll", limit };
  }

  if (verb === "history") {
    const [topicId, rest] = splitFirst(args);
    if (!topicId) return { name: "invalid", reason: "缺少 topic_id", usage: "@wtt history <topic_id> [limit]" };
    if (!rest) return { name: "history", topicId };
    const limit = parsePositiveInt(rest);
    if (!limit) {
      return { name: "invalid", reason: "history 的 limit 必须是正整数", usage: "@wtt history <topic_id> [limit]" };
    }
    return { name: "history", topicId, limit };
  }

  if (verb === "p2p") {
    const [agentId, content] = splitFirst(args);
    if (!agentId || !content) {
      return { name: "invalid", reason: "p2p 需要 agent_id 和内容", usage: "@wtt p2p <agent_id> <content>" };
    }
    return { name: "p2p", agentId, content };
  }

  if (verb === "detail") {
    const [topicId] = splitFirst(args);
    if (!topicId) return { name: "invalid", reason: "缺少 topic_id", usage: "@wtt detail <topic_id>" };
    return { name: "detail", topicId };
  }

  return { name: "invalid", reason: `不支持的命令: ${verb}`, usage: "@wtt help" };
}

export function isWTTCommandText(text: string): boolean {
  return normalizeWTTCommandText(text) !== null;
}
