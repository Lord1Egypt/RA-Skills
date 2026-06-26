import { AgentFactionPosition, AgentProfile, AllianceCluster, FactionListResult, FactionPower, FactionStatus, NearbyResult, RivalFaction, WorldEvent, WorldStats } from '../types';
export interface Intel {
    getAgentFactions(wallet: string): Promise<AgentFactionPosition[]>;
    getAgentProfile(wallet: string): Promise<AgentProfile>;
    getAgentSolLamports(wallet: string): Promise<number>;
    getAllies(mints: string[], holderLimit?: number): Promise<AllianceCluster[]>;
    getAscendedFactions(limit?: number): Promise<FactionListResult>;
    getFactionPower(mint: string): Promise<FactionPower>;
    getFactionLeaderboard(opts?: {
        status?: FactionStatus;
        limit?: number;
    }): Promise<FactionPower[]>;
    getFactionRivals(mint: string, opts?: {
        limit?: number;
    }): Promise<RivalFaction[]>;
    getNearbyFactions(wallet: string, opts?: {
        depth?: number;
        limit?: number;
    }): Promise<NearbyResult>;
    getRisingFactions(limit?: number): Promise<FactionListResult>;
    getWorldFeed(opts?: {
        limit?: number;
        factionLimit?: number;
    }): Promise<WorldEvent[]>;
    getWorldStats(): Promise<WorldStats>;
}
