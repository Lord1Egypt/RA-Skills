/** @wendao/agent-sdk 类型定义 */
export interface AgentConfig {
    /** Agent 钱包私钥 (不是 NFT owner 的私钥) */
    agentPrivateKey: string;
    /** BSC RPC URL */
    rpcUrl: string;
    /** NFA tokenId */
    tokenId: number;
    /** 合约地址 */
    contracts: {
        nfa: string;
        vault: string;
        token: string;
    };
    /** 后端 API URL (用于 PK 匹配) */
    apiUrl: string;
    /** JWT (用于 API 认证) */
    jwt?: string;
    /** 策略 */
    strategy: StrategyType | CustomStrategy;
    /** 行动间隔（秒），默认 300 (5分钟) */
    interval?: number;
}
export type StrategyType = "aggressive" | "defensive" | "balanced";
export interface CustomStrategy {
    name: string;
    shouldMeditate: (state: AgentState) => boolean;
    shouldStopMeditation: (state: AgentState) => boolean;
    shouldLevelUp: (state: AgentState) => boolean;
    shouldBreakthrough: (state: AgentState) => boolean;
    shouldPK: (state: AgentState) => {
        should: boolean;
        tier: number;
    };
    distributeSP: (state: AgentState, points: number) => [number, number, number, number, number];
}
export interface Warrior {
    personality: readonly [number, number, number, number, number];
    realm: number;
    level: number;
    xp: bigint;
    baseStats: readonly [number, number, number, number, number];
    unspentSP: number;
    xHandle: string;
    merkleRoot: `0x${string}`;
    referrer: bigint;
    createdAt: bigint;
}
export interface AgentState {
    warrior: Warrior;
    tokenId: number;
    ownerAddress: string;
    agentAddress: string;
    /** $JW 余额 (agent wallet) */
    jwBalance: bigint;
    /** BNB 余额 (agent wallet, for gas) */
    bnbBalance: bigint;
    /** 质押信息（属于 NFA owner，非 agent。Agent 不可调 claimStakingReward） */
    staked: bigint;
    pendingReward: bigint;
    /** 闭关状态 */
    isMeditating: boolean;
    meditationStartTime: number;
    pendingXP: number;
    /** PK 状态 */
    isInPK: boolean;
    /** 当前等级升级所需 XP */
    xpToNextLevel: bigint;
}
export interface ActionLog {
    timestamp: number;
    action: string;
    details: string;
    txHash?: string;
    success: boolean;
}
export interface AgentEvents {
    onAction: (log: ActionLog) => void;
    onError: (error: Error) => void;
    onStateUpdate: (state: AgentState) => void;
}
//# sourceMappingURL=types.d.ts.map