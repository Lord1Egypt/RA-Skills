// Type aliases for the system SDK types (imported from the system openclaw)
// The local npm install may differ; these are resolved at runtime from the
// system openclaw that OpenClaw itself loads.
export class SessionArchiveEngine {
    info = {
        id: "session-archive",
        name: "Session Archive Engine",
        version: "0.4.0",
    };
    db;
    constructor(db) {
        this.db = db;
    }
    // 公开方法：记录操作
    recordOperation(op) {
        this.db.insertOperation({
            sessionKey: op.sessionKey,
            operationType: op.operationType,
            target: op.target,
            details: op.details ? JSON.stringify(op.details) : undefined,
            result: op.result ?? "success",
            operator: op.operator ?? "system",
            createdAt: Date.now(),
        });
    }
    // 公开方法：记录 Token 使用（兼容新旧格式）
    recordTokenUsage(params) {
        const totalTokens = params.totalTokens ??
            ((params.promptTokens ?? 0) + (params.completionTokens ?? 0));
        this.db.insertTokenUsage({
            sessionKey: params.sessionKey,
            sessionId: params.sessionId,
            model: params.model,
            promptTokens: params.promptTokens,
            completionTokens: params.completionTokens,
            totalTokens,
            costUsd: params.costUsd,
            source: params.source ?? 'unknown',
            isEstimated: params.isEstimated ?? 0,
            timestamp: new Date().toISOString(),
            createdAt: Date.now(),
        });
    }
    // 公开方法：查询操作记录
    getOperations(sessionKey, operationType, limit) {
        return this.db.getOperations(sessionKey, operationType, limit);
    }
    // 公开方法：查询 Token 使用
    getTokenUsage(sessionKey, model, limit) {
        return this.db.getTokenUsage(sessionKey, model, limit);
    }
    async ingest(params) {
        if (params.isHeartbeat)
            return { ingested: false };
        const stored = toStoredMessage(params.message);
        const sessionKey = params.sessionKey ?? params.sessionId;
        this.db.insertMessage({
            sessionKey,
            sessionId: params.sessionId,
            role: stored.role,
            content: stored.content,
            model: stored.model,
            tokens: stored.tokenCount,
            createdAt: Date.now(),
            // 新增元数据
            channel: stored.channel,
            accountId: stored.accountId,
            messageId: stored.messageId,
            messageType: stored.messageType,
            toolName: stored.toolName,
            mediaPath: stored.mediaPath,
            tokensInput: stored.tokensInput,
            tokensOutput: stored.tokensOutput,
        });
        // 实时记录 Token 使用（仅 assistant 消息）
        if (params.message.role === 'assistant') {
            const tokenData = extractTokenData(params.message);
            this.db.insertTokenUsage({
                sessionKey,
                sessionId: params.sessionId,
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
        return { ingested: true };
    }
    async ingestBatch(params) {
        if (params.isHeartbeat || params.messages.length === 0) {
            return { ingestedCount: 0 };
        }
        const sessionKey = params.sessionKey ?? params.sessionId;
        const now = Date.now();
        for (const msg of params.messages) {
            const stored = toStoredMessage(msg);
            this.db.insertMessage({
                sessionKey,
                sessionId: params.sessionId,
                role: stored.role,
                content: stored.content,
                model: stored.model,
                tokens: stored.tokenCount,
                createdAt: now,
                channel: stored.channel,
                accountId: stored.accountId,
                messageId: stored.messageId,
                messageType: stored.messageType,
                toolName: stored.toolName,
                mediaPath: stored.mediaPath,
                tokensInput: stored.tokensInput,
                tokensOutput: stored.tokensOutput,
            });
            // 实时记录 Token 使用（仅 assistant 消息）
            if (msg.role === 'assistant') {
                const tokenData = extractTokenData(msg);
                this.db.insertTokenUsage({
                    sessionKey,
                    sessionId: params.sessionId,
                    model: tokenData.model,
                    promptTokens: tokenData.promptTokens,
                    completionTokens: tokenData.completionTokens,
                    totalTokens: tokenData.totalTokens,
                    costUsd: tokenData.costUsd,
                    source: tokenData.source,
                    isEstimated: tokenData.isEstimated,
                    timestamp: tokenData.timestamp,
                    createdAt: now,
                });
            }
        }
        return { ingestedCount: params.messages.length };
    }
    async assemble(params) {
        return {
            messages: params.messages,
            estimatedTokens: estimateTokens(params.messages),
        };
    }
    async compact(params) {
        // Session-archive is a pure side-effect engine; it never compacts context.
        return { ok: true, compacted: false };
    }
}
// ── Helpers ──────────────────────────────────────────────────────────────────
function estimateTokens(messages) {
    let total = 0;
    for (const msg of messages) {
        if ("content" in msg) {
            total += estimateContentTokens(msg.content);
        }
    }
    return total;
}
function estimateContentTokens(content) {
    if (typeof content === "string")
        return Math.ceil(content.length / 4);
    if (Array.isArray(content)) {
        let total = 0;
        for (const part of content) {
            if (part && typeof part === "object") {
                const record = part;
                const text = typeof record.text === "string"
                    ? record.text
                    : typeof record.thinking === "string"
                        ? record.thinking
                        : "";
                if (text)
                    total += Math.ceil(text.length / 4);
            }
        }
        return total;
    }
    if (content == null)
        return 0;
    return Math.ceil(JSON.stringify(content).length / 4);
}
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
// 从消息中提取 Token 数据（动态检测是否有真实 usage）
function extractTokenData(message) {
    const model = message.model || 'unknown';
    const usage = message.usage;
    // 1. 有 usage 且有真实数据 → 用 API 数据
    if (usage && (usage.input || usage.output || usage.totalTokens)) {
        return {
            model,
            promptTokens: usage.input ?? undefined,
            completionTokens: usage.output ?? undefined,
            totalTokens: usage.totalTokens ?? undefined,
            costUsd: usage.cost?.total ?? undefined,
            source: 'api',
            isEstimated: 0,
            timestamp: message.timestamp || new Date().toISOString(),
        };
    }
    // 2. 无 usage 或 数据为空 → 估算
    const content = extractMessageContent(message.content);
    const estimated = Math.max(Math.ceil(content.length / 4), 50);
    return {
        model,
        promptTokens: estimated,
        completionTokens: estimated,
        totalTokens: estimated * 2,
        costUsd: undefined,
        source: 'estimated',
        isEstimated: 1,
        timestamp: message.timestamp || new Date().toISOString(),
    };
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
function toStoredMessage(message) {
    const content = "content" in message ? extractMessageContent(message.content) : "";
    // Extract model and tokenCount from message
    let model;
    let tokenCount;
    let tokensInput;
    let tokensOutput;
    // Check for model in various locations
    if ("model" in message && typeof message.model === "string") {
        model = message.model;
    }
    // Check for tokenCount in usage object
    if ("usage" in message && message.usage && typeof message.usage === "object") {
        const usage = message.usage;
        if (typeof usage.total_tokens === "number") {
            tokenCount = usage.total_tokens;
        }
        else if (typeof usage.completion_tokens === "number" && typeof usage.prompt_tokens === "number") {
            tokenCount = usage.completion_tokens + usage.prompt_tokens;
            tokensInput = usage.prompt_tokens;
            tokensOutput = usage.completion_tokens;
        }
    }
    // Alternative token count location
    if (tokenCount === undefined && "tokenCount" in message && typeof message.tokenCount === "number") {
        tokenCount = message.tokenCount;
    }
    // Extract message type and tool name
    let messageType;
    let toolName;
    let mediaPath;
    if ("content" in message && Array.isArray(message.content)) {
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
    else if ("content" in message && typeof message.content === "string") {
        // Check for media path in text content
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
        role: toDbRole(message.role),
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
