import type {
  ParsedWTTCommand,
  WTTCommandClient,
  WTTCommandExecutionContext,
} from "./types.js";
import {
  formatAcknowledge,
  formatDetail,
  formatHelp,
  formatHistory,
  formatPoll,
  formatTopicCollection,
} from "./formatter.js";
import { handleConfigCommand } from "./config.js";
import { handleBindCommand } from "./bind.js";
import { handleSetupCommand } from "./setup.js";
import { handleTaskCommand } from "./task.js";
import { handlePipelineCommand } from "./pipeline.js";
import { handleDelegateCommand } from "./delegate.js";
import { handleUpdateCommand } from "./update.js";
import { handleVersionCommand } from "./version.js";

export async function executeWTTCommand(
  command: ParsedWTTCommand,
  client: WTTCommandClient | undefined,
  ctx: WTTCommandExecutionContext,
): Promise<string> {
  switch (command.name) {
    case "help":
      return formatHelp();

    case "invalid": {
      const hint = command.usage ? `\n用法: ${command.usage}` : "\n输入 @wtt help 查看支持命令";
      return `命令格式错误：${command.reason}${hint}`;
    }

    case "config":
      return handleConfigCommand(command.mode, ctx);

    case "bind":
      return handleBindCommand(ctx);

    case "setup":
      return handleSetupCommand(command, ctx);

    case "update":
      return handleUpdateCommand(ctx);

    case "version":
      return handleVersionCommand(ctx);

    case "task":
      return handleTaskCommand(command, ctx);

    case "pipeline":
      return handlePipelineCommand(command, ctx);

    case "delegate":
      return handleDelegateCommand(command, ctx);

    case "list": {
      const data = await requireClient(client, "list").list(command.limit);
      return formatTopicCollection("公开话题", data);
    }

    case "find": {
      const data = await requireClient(client, "find").find(command.query);
      return formatTopicCollection(`搜索结果（${command.query}）`, data);
    }

    case "join": {
      const data = await requireClient(client, "join").join(command.topicId);
      return formatAcknowledge("join", data, command.topicId);
    }

    case "leave": {
      const data = await requireClient(client, "leave").leave(command.topicId);
      return formatAcknowledge("leave", data, command.topicId);
    }

    case "publish": {
      const data = await requireClient(client, "publish").publish(command.topicId, command.content);
      return formatAcknowledge("publish", data, command.topicId);
    }

    case "poll": {
      const c = requireClient(client, "poll");
      const data = await c.poll(command.limit);
      return formatPoll(data, c);
    }

    case "history": {
      const c = requireClient(client, "history");
      const data = await c.history(command.topicId, command.limit);
      return formatHistory(data, c);
    }

    case "p2p": {
      const data = await requireClient(client, "p2p").p2p(command.agentId, command.content, true);
      return formatAcknowledge("p2p", data, command.agentId);
    }

    case "detail": {
      const data = await requireClient(client, "detail").detail(command.topicId);
      return formatDetail(data);
    }

    case "subscribed": {
      const data = await requireClient(client, "subscribed").subscribed();
      return formatTopicCollection("已订阅话题", data);
    }

    default:
      return formatHelp();
  }
}

function requireClient(client: WTTCommandClient | undefined, command: string): WTTCommandClient {
  if (!client) throw new Error(`命令 ${command} 需要可用的 WTT 客户端`);
  return client;
}
