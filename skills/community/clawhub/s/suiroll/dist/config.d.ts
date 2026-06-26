/**
 * SUIROLL Configuration
 * Configuration for Sui network and contract addresses
 */
export type TokenType = 'SUI' | 'USDC';
export interface SuirollConfig {
    network: 'mainnet' | 'testnet';
    packageId: string;
    registryObjectId: string;
    gasBudget: number;
    usdcAddress: string;
}
export declare const config: Record<string, SuirollConfig>;
/**
 * Moltbook Configuration
 */
export declare const moltbookConfig: {
    apiBase: string;
    defaultAudience: string;
    sessionFile: string;
};
/**
 * Get configuration for a specific network
 */
export declare function getConfig(network: 'mainnet' | 'testnet'): SuirollConfig;
/**
 * Set package ID after deployment
 */
export declare function setPackageId(network: 'mainnet' | 'testnet', packageId: string): void;
/**
 * Set registry object ID after deployment
 */
export declare function setRegistryObjectId(network: 'mainnet' | 'testnet', registryObjectId: string): void;
//# sourceMappingURL=config.d.ts.map