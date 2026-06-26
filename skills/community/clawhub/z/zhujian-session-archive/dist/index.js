import { join } from "node:path";
import { homedir } from "node:os";
import { createSessionArchiveDb } from "./db.js";
import { SessionArchiveEngine } from "./engine.js";
function resolveDbPath(dbPath) {
    if (dbPath && dbPath.trim())
        return dbPath.trim();
    return join(homedir(), ".openclaw", "session-archive.db");
}
const sessionArchivePlugin = {
    id: "session-archive",
    name: "Session Archive",
    description: "Archive every conversation message to SQLite in real-time via hooks",
    configSchema: {
        parse(value) {
            const raw = value && typeof value === "object" && !Array.isArray(value)
                ? value
                : {};
            return {
                dbPath: typeof raw.dbPath === "string" ? raw.dbPath.trim() : undefined,
            };
        },
    },
    register(api) {
        const pluginConfig = api.pluginConfig && typeof api.pluginConfig === "object" && !Array.isArray(api.pluginConfig)
            ? api.pluginConfig
            : undefined;
        const dbPath = typeof pluginConfig?.dbPath === "string" ? String(pluginConfig.dbPath) : undefined;
        const db = createSessionArchiveDb(dbPath);
        const engine = new SessionArchiveEngine(db);
        // 注册为 session-archive engine（备用，如果 slots 指向我们）
        api.registerContextEngine("session-archive", () => engine);
        // 通过 agent_end hook 监听消息（每次对话结束时）
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        api.on("agent_end", async (event, ctx) => {
            // 忽略心跳
            if (ctx?.trigger === "heartbeat")
                return;
            const sessionKey = ctx?.sessionKey || "unknown";
            const sessionId = ctx?.sessionId || ctx?.sessionKey || "unknown";
            try {
                const messages = event?.messages || [];
                // eslint-disable-next-line @typescript-eslint/no-explicit-any
                for (const msg of messages) {
                    const message = msg;
                    const stored = toStoredMessage(message);
                    db.insertMessage({
                        sessionKey,
                        sessionId,
                        role: stored.role,
                        content: stored.content,
                        model: stored.model,
                        tokens: stored.tokenCount,
                        createdAt: Date.now(),
                        channel: ctx?.channelId || "",
                        accountId: "",
                        messageId: typeof message.messageId === "string" ? message.messageId : undefined,
                        messageType: stored.messageType,
                        toolName: stored.toolName,
                        mediaPath: stored.mediaPath,
                        tokensInput: stored.tokensInput,
                        tokensOutput: stored.tokensOutput,
                    });
                    // 记录 token 使用（仅 assistant 消息）
                    if (message.role === "assistant") {
                        const tokenData = extractTokenData(message);
                        db.insertTokenUsage({
                            sessionKey,
                            sessionId,
                            model: tokenData.model,
                            promptTokens: tokenData.promptTokens,
                            completionTokens: tokenData.completionTokens,
                            totalTokens: tokenData.totalTokens,
                            costUsd: tokenData.costUsd,
                            source: tokenData.source,
                            isEstimated: tokenData.isEstimated,
                            timestamp: tokenData.timestamp,
                            createdAt: Date.now(),
                        });
                    }
                }
            }
            catch (err) {
                api.logger.error(`[session-archive] Hook error: ${err}`);
            }
        });
        // 通过 before_agent_start hook 记录用户消息（更实时）
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        api.on("before_agent_start", async (event, ctx) => {
            if (ctx?.trigger === "heartbeat")
                return;
            if (!event?.messages || event.messages.length === 0)
                return;
            const sessionKey = ctx?.sessionKey || "unknown";
            const sessionId = ctx?.sessionId || ctx?.sessionKey || "unknown";
            try {
                // 只处理用户消息（在 agent 开始前）
                // eslint-disable-next-line @typescript-eslint/no-explicit-any
                for (const msg of event.messages) {
                    const message = msg;
                    if (message.role !== "user")
                        continue;
                    const stored = toStoredMessage(message);
                    db.insertMessage({
                        sessionKey,
                        sessionId,
                        role: "user",
                        content: stored.content,
                        model: undefined,
                        tokens: undefined,
                        createdAt: Date.now(),
                        channel: ctx?.channelId || "",
                        accountId: "",
                        messageId: typeof message.messageId === "string" ? message.messageId : undefined,
                        messageType: stored.messageType,
                    });
                }
            }
            catch (err) {
                api.logger.error(`[session-archive] before_agent_start hook error: ${err}`);
            }
        });
        api.logger.info(`[session-archive] Plugin loaded (db=${resolveDbPath(dbPath)}, hooks=true)`);
    },
};
function extractMessageContent(content) {
    if (typeof content === "string")
        return content;
    if (Array.isArray(content)) {
        const texts = [];
        for (const part of content) {
            if (part && typeof part === "object") {
                const record = part;
                if (record.type === "text" && typeof record.text === "string") {
                    texts.push(record.text);
                }
            }
        }
        return texts.join("\n");
    }
    if (content == null)
        return "";
    return JSON.stringify(content);
}
function toDbRole(role) {
    if (role === "tool" || role === "toolResult")
        return "tool";
    if (role === "system")
        return "system";
    if (role === "user")
        return "user";
    return "assistant";
}
function extractTokenData(message) {
    const model = message.model || "unknown";
    const usage = message.usage;
    if (usage && (usage.input || usage.output || usage.totalTokens)) {
        return {
            model,
            promptTokens: usage.input,
            completionTokens: usage.output,
            totalTokens: usage.totalTokens,
            costUsd: usage.cost?.total,
            source: "api",
            isEstimated: 0,
            timestamp: message.timestamp || new Date().toISOString(),
        };
    }
    const content = extractMessageContent(message.content);
    const estimated = Math.max(Math.ceil(content.length / 4), 50);
    return {
        model,
        promptTokens: estimated,
        completionTokens: estimated,
        totalTokens: estimated * 2,
        costUsd: undefined,
        source: "estimated",
        isEstimated: 1,
        timestamp: message.timestamp || new Date().toISOString(),
    };
}
function toStoredMessage(message) {
    const content = extractMessageContent(message.content);
    let model;
    let tokenCount;
    let tokensInput;
    let tokensOutput;
    if (message.model && typeof message.model === "string") {
        model = message.model;
    }
    const usage = message.usage;
    if (usage) {
        if (typeof usage.total_tokens === "number") {
            tokenCount = usage.total_tokens;
        }
        else if (typeof usage.completion_tokens === "number" && typeof usage.prompt_tokens === "number") {
            tokenCount = usage.completion_tokens + usage.prompt_tokens;
            tokensInput = usage.prompt_tokens;
            tokensOutput = usage.completion_tokens;
        }
    }
    let messageType;
    let toolName;
    let mediaPath;
    if (Array.isArray(message.content)) {
        for (const part of message.content) {
            if (part && typeof part === "object") {
                const record = part;
                if (record.type === "tool_use" && typeof record.name === "string") {
                    toolName = record.name;
                    messageType = "tool";
                }
                else if (record.type === "tool_result" && record.content) {
                    messageType = "tool_result";
                }
                else if (record.type === "image" || record.type === "image_url") {
                    messageType = "image";
                }
                else if (record.type === "video") {
                    messageType = "video";
                }
                else if (record.type === "audio") {
                    messageType = "audio";
                }
                else if (record.type === "text") {
                    messageType = "text";
                }
            }
        }
    }
    else if (typeof message.content === "string") {
        if (message.content.includes("[media attached:")) {
            const match = message.content.match(/\[media attached:([^\]]+)\]/);
            if (match) {
                mediaPath = match[1];
                if (mediaPath.includes(".mp3") || mediaPath.includes(".wav")) {
                    messageType = "voice";
                }
                else if (mediaPath.includes(".jpg") || mediaPath.includes(".png") || mediaPath.includes(".webp")) {
                    messageType = "image";
                }
                else if (mediaPath.includes(".mp4")) {
                    messageType = "video";
                }
                else {
                    messageType = "file";
                }
            }
        }
        else {
            messageType = "text";
        }
    }
    return {
        role: toDbRole(String(message.role)),
        content,
        model,
        tokenCount,
        messageType,
        toolName,
        mediaPath,
        tokensInput,
        tokensOutput,
    };
}
export default sessionArchivePlugin;
