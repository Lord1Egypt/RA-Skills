import Database from "better-sqlite3";
export interface ArchiveMessage {
    id?: number;
    sessionKey: string;
    sessionId: string;
    role: "user" | "assistant" | "system" | "tool";
    content: string;
    model?: string;
    tokens?: number;
    createdAt: number;
    channel?: string;
    accountId?: string;
    messageId?: string;
    messageType?: string;
    toolName?: string;
    mediaPath?: string;
    parentSessionKey?: string;
    tokensInput?: number;
    tokensOutput?: number;
    costUsd?: number;
}
export interface Operation {
    id?: number;
    sessionKey?: string;
    operationType: string;
    target: string;
    details?: string;
    result?: string;
    operator?: string;
    createdAt: number;
}
export interface TokenUsage {
    id?: number;
    sessionKey?: string;
    sessionId?: string;
    model: string;
    promptTokens?: number;
    completionTokens?: number;
    totalTokens?: number;
    costUsd?: number;
    source?: string;
    isEstimated?: number;
    timestamp?: string;
    createdAt: number;
}
export interface SessionArchiveDb {
    insertMessage(msg: ArchiveMessage): void;
    insertOperation(op: Operation): void;
    insertTokenUsage(tu: TokenUsage): void;
    getMessages(sessionKey: string, limit?: number): ArchiveMessage[];
    getMessagesBySessionId(sessionId: string, limit?: number): ArchiveMessage[];
    getOperations(sessionKey?: string, operationType?: string, limit?: number): Operation[];
    getTokenUsage(sessionKey?: string, model?: string, limit?: number): TokenUsage[];
    close(): void;
    db: Database.Database;
}
export declare function createSessionArchiveDb(dbPath?: string): SessionArchiveDb;
