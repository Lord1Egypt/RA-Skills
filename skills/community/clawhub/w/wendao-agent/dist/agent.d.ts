import { LearningTree } from "./learning-tree.js";
import type { AgentConfig, AgentState, ActionLog } from "./types.js";
export declare class WenDaoAgent {
    private config;
    private strategy;
    private account;
    private publicClient;
    private walletClient;
    private running;
    private logs;
    learningTree: LearningTree;
    private successCount;
    private jwt;
    private onAction?;
    private onError?;
    private onStateUpdate?;
    constructor(config: AgentConfig);
    /** 注册事件回调 */
    on(event: "action", cb: (log: ActionLog) => void): this;
    on(event: "error", cb: (error: Error) => void): this;
    on(event: "stateUpdate", cb: (state: AgentState) => void): this;
    /** 读取链上完整状态 */
    getState(): Promise<AgentState>;
    /** 执行单次决策循环 */
    tick(): Promise<ActionLog[]>;
    /** 自动获取 Agent JWT（通过签名验证身份） */
    private authenticate;
    /** 启动 Agent 循环 */
    start(): Promise<void>;
    /** 停止 Agent */
    stop(): void;
    /** 获取行动日志 */
    getLogs(): ActionLog[];
    private execLevelUp;
    private execDistributeSP;
    private execBreakthrough;
    private execStartMeditation;
    private execStopMeditation;
    private execPKRecover;
    private execPK;
}
//# sourceMappingURL=agent.d.ts.map