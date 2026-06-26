/**
 * CLI configuration — loads from ~/.x402r/config.json, .env, and env vars.
 * Priority: env vars > .env > config file > arbiter auto-discovery > defaults
 */
export interface CliConfigFile {
    privateKey?: string;
    operatorAddress?: string;
    arbiterUrl?: string;
    courtUrl?: string;
    networkId?: string;
    rpcUrl?: string;
    pinataJwt?: string;
}
interface ArbiterContracts {
    chainId: number;
    rpcUrl: string;
    operatorAddress: string | null;
}
/**
 * Fetch operator address, network, and RPC from the arbiter's /api/contracts endpoint.
 */
export declare function fetchArbiterContracts(arbiterUrl: string): Promise<ArbiterContracts | null>;
/**
 * Load config from ~/.x402r/config.json
 */
export declare function loadConfigFile(): CliConfigFile;
/**
 * Save config to ~/.x402r/config.json
 */
export declare function saveConfigFile(config: CliConfigFile): void;
/**
 * Get resolved config: env vars > .env > config file > defaults
 */
export declare function getConfig(): Required<Pick<CliConfigFile, "networkId" | "arbiterUrl">> & CliConfigFile;
/**
 * Get resolved config with auto-discovery from arbiter.
 * Falls back to local config if arbiter is unreachable.
 */
export declare function getConfigWithDiscovery(): Promise<Required<Pick<CliConfigFile, "networkId" | "arbiterUrl">> & CliConfigFile>;
/**
 * Print current config (masked key)
 */
export declare function printConfig(): Promise<void>;
export {};
