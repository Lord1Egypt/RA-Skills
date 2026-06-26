import type { WTTCommandClient } from "./types.js";

type UnknownRecord = Record<string, unknown>;

function asRecord(value: unknown): UnknownRecord | null {
  if (typeof value !== "object" || value === null || Array.isArray(value)) return null;
  return value as UnknownRecord;
}

function asString(value: unknown, fallback = "-"): string {
  return typeof value === "string" && value.trim() ? value : fallback;
}

function asNumber(value: unknown): number | null {
  if (typeof value === "number" && Number.isFinite(value)) return value;
  if (typeof value === "string" && /^\d+$/.test(value)) return Number(value);
  return null;
}

function topicIcon(topicType: string): string {
  switch (topicType) {
    case "broadcast":
      return "📣";
    case "discussion":
      return "💬";
    case "collaborative":
      return "🤝";
    case "p2p":
      return "🔒";
    default:
      return "📌";
  }
}

function contentIcon(contentType: string): string {
  switch (contentType) {
    case "image":
      return "🖼";
    case "audio":
      return "🎵";
    case "video":
      return "🎬";
    case "file":
      return "📎";
    case "link":
      return "🔗";
    default:
      return "💬";
  }
}

function compactText(raw: string, maxLen = 90): string {
  const normalized = raw.replace(/\s+/g, " ").trim();
  if (normalized.length <= maxLen) return normalized;
  return `${normalized.slice(0, maxLen - 1)}…`;
}

function toTopicList(data: unknown): UnknownRecord[] {
  if (!Array.isArray(data)) return [];
  return data.map((item) => asRecord(item)).filter((item): item is UnknownRecord => item !== null);
}

function toMessageList(data: unknown): UnknownRecord[] {
  if (!Array.isArray(data)) return [];
  return data.map((item) => asRecord(item)).filter((item): item is UnknownRecord => item !== null);
}

export function formatHelp(): string {
  return [
    "WTT 命令（plugin 迁移中）",
    "- @wtt list [limit]",
    "- @wtt find <query>",
    "- @wtt join <topic_id>",
    "- @wtt leave <topic_id>",
    "- @wtt publish <topic_id> <content>",
    "- @wtt poll [limit]",
    "- @wtt history <topic_id> [limit]",
    "- @wtt p2p <agent_id> <content>",
    "- @wtt detail <topic_id>",
    "- @wtt subscribed",
    "- @wtt task list | detail <task_id> | create <title> [description] | run <task_id> | review <task_id> <approve|reject|block> [comment]",
    "- @wtt pipeline list | create <name> [description] | run <pipeline_id>",
    "- @wtt delegate list | create <target_agent_id> | remove <target_agent_id>",
    "- @wtt config [auto]",
    "- @wtt bind",
    "- @wtt setup <agent_id> <agent_token> [cloudUrl]",
    "- @wtt update",
    "- @wtt version",
    "- /wtt update",
    "- /wtt version",
    "- /wtt-update",
    "- @wtt help",
  ].join("\n");
}

export function formatTopicCollection(title: string, data: unknown): string {
  const topics = toTopicList(data);
  if (topics.length === 0) return `${title}：暂无结果`;

  const lines: string[] = [`${title}（${topics.length}）`];
  for (const [idx, topic] of topics.entries()) {
    const id = asString(topic.id, "-");
    const name = asString(topic.name, "(未命名)");
    const type = asString(topic.type, "unknown");
    const memberCount = asNumber(topic.member_count);
    const role = asString(topic.my_role, "");
    const desc = asString(topic.description, "");

    const roleText = role && role !== "-" ? ` [${role}]` : "";
    const memberText = memberCount !== null ? ` | 成员 ${memberCount}` : "";

    lines.push(`${idx + 1}. ${topicIcon(type)} ${name}${roleText}`);
    lines.push(`   id: ${id} | 类型 ${type}${memberText}`);
    if (desc && desc !== "-") lines.push(`   ${compactText(desc, 70)}`);
  }

  return lines.join("\n");
}

async function getMessageText(client: WTTCommandClient, message: UnknownRecord): Promise<string> {
  const rawContent = asString(message.content, "");
  if (!rawContent) return "";

  const encrypted = message.encrypted === true;
  if (!encrypted || typeof client.decryptMessage !== "function") return rawContent;

  try {
    return await client.decryptMessage(rawContent);
  } catch {
    return rawContent;
  }
}

export async function formatPoll(data: unknown, client: WTTCommandClient): Promise<string> {
  const payload = asRecord(data);
  if (!payload) return "poll 返回数据格式异常";

  const messages = toMessageList(payload.messages);
  const topics = toTopicList(payload.topics);

  if (messages.length === 0) return "暂无新消息";

  const topicNameById = new Map<string, string>();
  for (const topic of topics) {
    const id = asString(topic.id, "");
    if (!id) continue;
    topicNameById.set(id, asString(topic.name, id.slice(0, 8)));
  }

  const lines: string[] = [`新消息（${messages.length}）`];
  for (const message of messages) {
    const topicId = asString(message.topic_id, "-");
    const topicName = topicNameById.get(topicId) ?? topicId;
    const sender = asString(message.sender_id, "?");
    const contentType = asString(message.content_type, "text");
    const content = compactText(await getMessageText(client, message), 100);
    const prefix = contentType === "text" ? "" : `${contentIcon(contentType)} `;
    lines.push(`- [${topicName}] ${sender}: ${prefix}${content}`);
  }

  return lines.join("\n");
}

export async function formatHistory(data: unknown, client: WTTCommandClient): Promise<string> {
  const messages = toMessageList(data);
  if (messages.length === 0) return "该话题暂无历史消息";

  const lines: string[] = [`历史消息（${messages.length}）`];
  for (const message of messages) {
    const ts = asString(message.created_at, "-");
    const sender = asString(message.sender_id, "?");
    const contentType = asString(message.content_type, "text");
    const content = compactText(await getMessageText(client, message), 110);
    const prefix = contentType === "text" ? "" : `${contentIcon(contentType)} `;
    lines.push(`- ${ts} ${sender}: ${prefix}${content}`);
  }

  return lines.join("\n");
}

export function formatDetail(data: unknown): string {
  const topic = asRecord(data);
  if (!topic) return "topic 详情返回数据格式异常";

  const name = asString(topic.name, "(未命名)");
  const id = asString(topic.id, "-");
  const type = asString(topic.type, "-");
  const visibility = asString(topic.visibility, "-");
  const joinMethod = asString(topic.join_method, "-");
  const memberCount = asNumber(topic.member_count);
  const creator = asString(topic.creator_agent_id, "-");
  const desc = asString(topic.description, "");

  const lines = [
    `${topicIcon(type)} ${name}`,
    `id: ${id}`,
    `类型: ${type} | 可见性: ${visibility}`,
    `加入方式: ${joinMethod} | 成员: ${memberCount ?? "-"}`,
    `创建者: ${creator}`,
  ];

  if (desc && desc !== "-") lines.push(`描述: ${compactText(desc, 120)}`);

  return lines.join("\n");
}

export function formatAcknowledge(action: "join" | "leave" | "publish" | "p2p", data: unknown, target: string): string {
  const payload = asRecord(data) ?? {};
  const msg = asString(payload.message, "");

  if (action === "join") return msg ? `已加入 ${target}（${msg}）` : `已加入 ${target}`;
  if (action === "leave") return msg ? `已离开 ${target}（${msg}）` : `已离开 ${target}`;

  if (action === "publish") {
    const messageId = asString(payload.id, "");
    return messageId ? `已发布到 ${target}（消息ID: ${messageId}）` : `已发布到 ${target}`;
  }

  const messageId = asString(payload.id, "");
  return messageId ? `已发送给 ${target}（消息ID: ${messageId}）` : `已发送给 ${target}`;
}
