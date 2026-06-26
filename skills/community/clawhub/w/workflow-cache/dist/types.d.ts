export interface OpenClawContext {
    workspace: WorkspaceAPI;
    browser: BrowserAPI;
    lobster: LobsterAPI;
    sessions: SessionsAPI;
    gateway: GatewayAPI;
    config: SkillConfig;
    logger: Logger;
}
export interface WorkspaceAPI {
    getNodeId(): string;
}
export interface BrowserAPI {
    getCurrentUrl(): Promise<string>;
    getDomSkeletonHash(): Promise<string>;
    invoke(action: string, args: Record<string, unknown>): Promise<BrowserResult>;
}
export interface BrowserResult {
    success: boolean;
    error?: string;
    data?: unknown;
}
export interface LobsterAPI {
    execute(workflow: LobsterWorkflow): Promise<LobsterExecutionResult>;
    validate(workflow: LobsterWorkflow): boolean;
}
export interface LobsterExecutionResult {
    success: boolean;
    steps_completed: number;
    total_steps: number;
    error?: string;
    failed_step_id?: string;
}
export interface SessionsAPI {
    getHistory(sessionId: string): Promise<SessionHistory>;
    getCurrentSessionId(): string;
}
export interface SessionHistory {
    session_id: string;
    intent: string;
    actions: ActionTrace[];
    status: "success" | "failure" | "in_progress";
    started_at: string;
    completed_at?: string;
}
export interface ActionTrace {
    tool: string;
    action: string;
    args: Record<string, unknown>;
    result: {
        success: boolean;
        error?: string;
    };
    timestamp: string;
}
export interface GatewayAPI {
    passthrough(): void;
    respond(message: string): void;
}
export interface SkillConfig {
    get<T>(key: string): T;
}
export interface Logger {
    info(msg: string, ...args: unknown[]): void;
    warn(msg: string, ...args: unknown[]): void;
    error(msg: string, ...args: unknown[]): void;
    debug(msg: string, ...args: unknown[]): void;
}
export interface LobsterStep {
    id: string;
    command: string;
    env?: Record<string, string>;
    timeout_ms?: number;
}
export interface LobsterArgs {
    [key: string]: {
        type: "string" | "number" | "boolean";
        default?: string | number | boolean;
        required?: boolean;
    };
}
export interface LobsterWorkflow {
    name: string;
    args: LobsterArgs;
    steps: LobsterStep[];
}
export interface MatchRequest {
    intent: string;
    intent_embedding?: number[];
    url: string;
    dom_skeleton_hash?: string;
    node_id: string;
}
export interface MatchResponse {
    hit: boolean;
    macro?: {
        macro_id: string;
        trigger_context: {
            intent_embedding: number[];
            url_regex: string;
            dom_skeleton_hash?: string;
        };
        lobster_workflow: LobsterWorkflow;
        metadata: {
            author_node: string;
            success_rate: number;
            success_count: number;
            failure_count: number;
            last_verified: string;
            created_at: string;
        };
        status: string;
    };
    match_score?: number;
    match_method?: string;
}
export interface ContributeRequest {
    node_id: string;
    intent: string;
    url: string;
    dom_skeleton_hash?: string;
    lobster_workflow: LobsterWorkflow;
    intent_embedding?: number[];
    session_id: string;
}
export interface ContributeResponse {
    accepted: boolean;
    macro_id?: string;
    reason?: string;
}
export interface ReportFailureRequest {
    macro_id: string;
    node_id: string;
    error_type: "selector_not_found" | "timeout" | "unexpected_state" | "other";
    error_detail?: string;
}
