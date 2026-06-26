import type { Stronghold } from '../types';
/** Action types tracked by the state provider */
export type TrackedAction = 'join' | 'defect' | 'rally' | 'launch' | 'message' | 'reinforce' | 'war_loan' | 'repay_loan' | 'siege' | 'ascend' | 'raze' | 'tithe' | 'infiltrate' | 'fud';
/** Snapshot of objective on-chain game state for an agent */
export interface AgentGameState {
    /** Agent wallet public key */
    publicKey: string;
    /** Monotonic tick counter — increments on each successful action */
    tick: number;
    /** Cumulative action counts keyed by action type */
    actionCounts: Record<TrackedAction, number>;
    /** Mints with active war loans */
    activeLoans: Set<string>;
    /** Mints this agent founded */
    founded: string[];
    /** Mints already rallied (can only rally once) */
    rallied: Set<string>;
    /** Mints already voted on (first buy requires strategy vote) */
    voted: Set<string>;
    /** Sentiment per faction: mint → score (-10 to +10), derived from actions */
    sentiment: Map<string, number>;
    /** Recent action descriptions for LLM context / memory block */
    recentHistory: string[];
    /** Personality summary from on-chain registry checkpoint (null if no profile) */
    personalitySummary: string | null;
    /** Total SOL spent (from registry checkpoint, lamports) */
    totalSolSpent: number;
    /** Total SOL received (from registry checkpoint, lamports) */
    totalSolReceived: number;
    /** Whether state has been initialized from chain */
    initialized: boolean;
}
/** Serializable form of AgentGameState for persistence */
export interface SerializedGameState {
    publicKey: string;
    vaultCreator: string | null;
    tick: number;
    actionCounts: Record<TrackedAction, number>;
    holdings: Record<string, number>;
    activeLoans: string[];
    founded: string[];
    rallied: string[];
    voted: string[];
    sentiment: Record<string, number>;
    recentHistory: string[];
    personalitySummary: string | null;
    totalSolSpent: number;
    totalSolReceived: number;
}
/** Configuration for auto-checkpoint behavior */
export interface CheckpointConfig {
    /** Checkpoint every N ticks (default: 25) */
    interval: number;
    /** Personality summary string provider — called at checkpoint time */
    getPersonalitySummary?: () => string;
    /** SOL spent/received provider — called at checkpoint time */
    getSolTotals?: () => {
        spent: number;
        received: number;
    };
}
/** State provider interface — objective game state tracking */
export interface State {
    /** Current game state (null before init) */
    readonly state: AgentGameState | null;
    /** Whether state has been initialized */
    readonly initialized: boolean;
    /** Current tick count */
    readonly tick: number;
    /**
     * Initialize state from chain.
     * Loads action counts from registry checkpoint.
     * Vault and holdings are resolved lazily on first access.
     */
    init(): Promise<AgentGameState>;
    /**
     * Record a successful action — increments tick, updates action counts,
     * updates sentiment, appends to history.
     */
    record(action: TrackedAction, mint?: string, description?: string): Promise<void>;
    /** Get vault creator key (lazy — resolves on first call, cached after) */
    getVaultCreator(): Promise<string | null>;
    /** Get stronghold info (lazy — resolves on first call, cached after) */
    getStronghold(): Promise<Stronghold | null>;
    /** Get token holdings fresh from chain (wallet + vault) */
    getHoldings(): Promise<Map<string, number>>;
    /** Get token balance for a specific mint (fresh from chain) */
    getBalance(mint: string): Promise<number>;
    /** Get sentiment score for a faction (-10 to +10) */
    getSentiment(mint: string): number;
    /** Get all sentiment entries */
    readonly sentimentMap: ReadonlyMap<string, number>;
    /** Get recent action history (for LLM memory block) */
    readonly history: readonly string[];
    /** Check if agent has voted on a faction */
    hasVoted(mint: string): boolean;
    /** Check if agent has rallied a faction */
    hasRallied(mint: string): boolean;
    /** Mark a faction as voted */
    markVoted(mint: string): void;
    /** Mark a faction as rallied */
    markRallied(mint: string): void;
    /** Serialize state for persistence */
    serialize(): SerializedGameState;
    /** Hydrate from a previously serialized state (skips chain reconstruction) */
    hydrate(saved: SerializedGameState): void;
}
