import { Connection, Keypair } from '@solana/web3.js';
export type LogLevel = 'debug' | 'info' | 'warn' | 'error';
export type LogFormat = 'text' | 'json';
export type Logger = (level: LogLevel, msg: string, extra?: Record<string, unknown>) => void;
export interface BotConfig {
    rpcUrl: string;
    vaultCreator: string;
    privateKey: string | null;
    scanIntervalMs: number;
    logLevel: LogLevel;
    logFormat: LogFormat;
    scanLimit: number;
    minAgentBalanceLamports: number;
}
export interface BotStats {
    cycles: number;
    liquidations: number;
    failures: number;
    rpcRetries: number;
    startedAt: number;
    lastError: string | null;
}
export interface ScanContext {
    connection: Connection;
    log: Logger;
    vaultCreator: string;
    agentKeypair: Keypair;
    agentPk: string;
    scanLimit: number;
    minBalance: number;
    stats: BotStats;
    isShutdownRequested: () => boolean;
}
//# sourceMappingURL=types.d.ts.map