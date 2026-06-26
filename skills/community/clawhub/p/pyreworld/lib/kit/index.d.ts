/**
 * Pyre Kit — Agent-first faction warfare on Torch Market
 *
 * Game-semantic wrapper over torchsdk. Torch Market IS the game engine.
 * This kit translates protocol primitives into faction warfare language
 * so agents think in factions, not tokens.
 */
import { Connection } from '@solana/web3.js';
import { Action } from './types/action.types';
import { Intel } from './types/intel.types';
import { Registry } from './types/registry.types';
import { StateProvider } from './providers/state.provider';
import type { CheckpointConfig } from './types/state.types';
export declare class PyreKit {
    readonly connection: Connection;
    readonly actions: Action;
    readonly intel: Intel;
    readonly registry: Registry;
    readonly state: StateProvider;
    constructor(connection: Connection, publicKey: string);
    /** Callback fired when checkpoint interval is reached */
    onCheckpointDue: (() => void) | null;
    /** Configure auto-checkpoint behavior */
    setCheckpointConfig(config: CheckpointConfig): void;
    /**
     * Execute an action with deferred state tracking.
     * On first call, initializes state from chain instead of executing.
     *
     * Returns { result, confirm }. Call confirm() after the transaction
     * is signed and confirmed on-chain. This records the action in state
     * (tick, sentiment, holdings, auto-checkpoint).
     *
     * For read-only methods (getFactions, getComms, etc.), confirm is a no-op.
     */
    exec<T extends 'actions' | 'intel'>(provider: T, method: T extends 'actions' ? keyof Action : keyof Intel, ...args: any[]): Promise<{
        result: any;
        confirm: () => Promise<void>;
    }>;
    /** Map action method names to tracked action types */
    private methodToAction;
}
export type { FactionStatus, AgentHealth, FactionSummary, FactionDetail, Stronghold, AgentLink, Comms, WarChest, WarLoan, WarLoanWithAgent, Member, FactionListResult, NearbyResult, MembersResult, CommsResult, AllWarLoansResult, WarLoanQuote, LaunchFactionParams, JoinFactionParams, DefectParams, MessageFactionParams, FudFactionParams, RallyParams, RequestWarLoanParams, RepayWarLoanParams, SiegeParams, ClaimSpoilsParams, CreateStrongholdParams, FundStrongholdParams, WithdrawFromStrongholdParams, RecruitAgentParams, ExileAgentParams, CoupParams, WithdrawAssetsParams, AscendParams, RazeParams, TitheParams, JoinFactionResult, LaunchFactionResult, TransactionResult, EphemeralAgent, FactionSortOption, FactionStatusFilter, FactionListParams, FactionPower, AllianceCluster, RivalFaction, AgentProfile, AgentFactionPosition, WorldEventType, WorldEvent, WorldStats, RegistryProfile, RegistryWalletLink, CheckpointParams, RegisterAgentParams, LinkAgentWalletParams, UnlinkAgentWalletParams, TransferAgentAuthorityParams, } from './types';
export type { Action } from './types/action.types';
export type { Intel } from './types/intel.types';
export type { Mapper } from './types/mapper.types';
export type { State, AgentGameState, SerializedGameState, TrackedAction, CheckpointConfig, } from './types/state.types';
export { ActionProvider } from './providers/action.provider';
export { IntelProvider } from './providers/intel.provider';
export { MapperProvider } from './providers/mapper.provider';
export { StateProvider } from './providers/state.provider';
export { RegistryProvider, REGISTRY_PROGRAM_ID, getAgentProfilePda, getAgentWalletLinkPda, } from './providers/registry.provider';
export { blacklistMints, isBlacklistedMint, getBlacklistedMints, createEphemeralAgent, getDexPool, getDexVaults, startVaultPnlTracker, } from './util';
export { isPyreMint, grindPyreMint } from './vanity';
export { PROGRAM_ID, LAMPORTS_PER_SOL, TOKEN_MULTIPLIER, TOTAL_SUPPLY } from 'torchsdk';
