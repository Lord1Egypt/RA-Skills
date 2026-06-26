import type { ContextEngine, ContextEngineInfo } from "openclaw/plugin-sdk";
import type { AgentMessage } from "@mariozechner/pi-agent-core";
import type { SessionArchiveDb } from "./db.js";
export declare class SessionArchiveEngine implements ContextEngine {
    readonly info: ContextEngineInfo;
    private readonly db;
    constructor(db: SessionArchiveDb);
    recordOperation(op: {
        sessionKey?: string;
        operationType: string;
        target: string;
        details?: string;
        result?: string;
        operator?: string;
    }): void;
    recordTokenUsage(params: {
        sessionKey?: string;
        sessionId?: string;
        model: string;
        promptTokens?: number;
        completionTokens?: number;
        totalTokens?: number;
        costUsd?: number;
        source?: string;
        isEstimated?: number;
    }): void;
    getOperations(sessionKey?: string, operationType?: string, limit?: number): import("./db.js").Operation[];
    getTokenUsage(sessionKey?: string, model?: string, limit?: number): import("./db.js").TokenUsage[];
    ingest(params: {
        sessionId: string;
        sessionKey?: string;
        message: AgentMessage;
        isHeartbeat?: boolean;
    }): Promise<{
        ingested: boolean;
    }>;
    ingestBatch(params: {
        sessionId: string;
        sessionKey?: string;
        messages: AgentMessage[];
        isHeartbeat?: boolean;
    }): Promise<{
        ingestedCount: number;
    }>;
    assemble(params: {
        sessionId: string;
        sessionKey?: string;
        messages: AgentMessage[];
        tokenBudget?: number;
    }): Promise<{
        messages: AgentMessage[];
        estimatedTokens: number;
    }>;
    compact(params: {
        sessionId: string;
        sessionKey?: string;
        sessionFile: string;
        tokenBudget?: number;
        force?: boolean;
        currentTokenCount?: number;
        compactionTarget?: "budget" | "threshold";
        customInstructions?: string;
        runtimeContext?: Record<string, unknown>;
    }): Promise<{
        ok: boolean;
        compacted: boolean;
    }>;
}
