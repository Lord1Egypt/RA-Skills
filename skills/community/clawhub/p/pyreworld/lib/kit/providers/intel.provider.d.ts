import { Connection } from '@solana/web3.js';
import { AgentFactionPosition, AgentProfile, AllianceCluster, FactionListResult, FactionPower, FactionStatus, NearbyResult, WorldEvent, WorldStats, RivalFaction } from '../types';
import { Intel } from '../types/intel.types';
import { Action } from '../types/action.types';
export declare class IntelProvider implements Intel {
    private connection;
    private actionProvider;
    constructor(connection: Connection, actionProvider: Action);
    getAgentFactions(wallet: string): Promise<AgentFactionPosition[]>;
    getRisingFactions(limit?: number): Promise<FactionListResult>;
    getAscendedFactions(limit?: number): Promise<FactionListResult>;
    getNearbyFactions(wallet: string, { depth, limit }?: {
        depth?: number;
        limit?: number;
    }): Promise<NearbyResult>;
    getAgentProfile(wallet: string): Promise<AgentProfile>;
    getAgentSolLamports(wallet: string): Promise<number>;
    getAllies(mints: string[], holderLimit?: number): Promise<AllianceCluster[]>;
    getFactionPower(mint: string): Promise<FactionPower>;
    getFactionLeaderboard({ status, limit, }: {
        status?: FactionStatus;
        limit?: number;
    }): Promise<FactionPower[]>;
    getFactionRivals(mint: string, { limit }: {
        limit?: number;
    }): Promise<RivalFaction[]>;
    getWorldFeed({ limit, factionLimit, }: {
        limit?: number;
        factionLimit?: number;
    }): Promise<WorldEvent[]>;
    getWorldStats(): Promise<WorldStats>;
    private computePowerScore;
    private computePowerScoreFromSummary;
    private getPyreHolders;
}
