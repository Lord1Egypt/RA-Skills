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

export const config: Record<string, SuirollConfig> = {
  testnet: {
    network: 'testnet',
    packageId: '0x983baae94dc5ff06ebd57d7cc221f09ec8ec1c01f9e49065c70611716aee6bda',
    registryObjectId: '0x414519308218f10e98c155bf952fbd0f308b45f9b79e56796d60d7aa4a00a312',
    gasBudget: 10000000, // 0.01 SUI
    usdcAddress: '0xa1ec7fc00a6f40db9693ad1415d0c193ad3906494428cf252621037bd7117e29::usdc::USDC',
  },
  mainnet: {
    network: 'mainnet',
    packageId: '0x0000000000000000000000000000000000000000000000000000000000000000', // TODO: Update after deployment
    registryObjectId: '0x0000000000000000000000000000000000000000000000000000000000000000', // TODO: Update after deployment
    gasBudget: 10000000, // 0.01 SUI,
    usdcAddress: '0x...::usdc::USDC', // TODO: Update after mainnet deployment
  },
};

/**
 * Moltbook Configuration
 */
export const moltbookConfig = {
  apiBase: 'https://www.moltbook.com/api/v1',
  defaultAudience: 'suiroll.app',
  sessionFile: `${process.env.HOME || '~'}/.config/suiroll/moltbook-session.json`,
};

/**
 * Get configuration for a specific network
 */
export function getConfig(network: 'mainnet' | 'testnet'): SuirollConfig {
  return config[network];
}

/**
 * Set package ID after deployment
 */
export function setPackageId(network: 'mainnet' | 'testnet', packageId: string): void {
  config[network].packageId = packageId;
}

/**
 * Set registry object ID after deployment
 */
export function setRegistryObjectId(network: 'mainnet' | 'testnet', registryObjectId: string): void {
  config[network].registryObjectId = registryObjectId;
}
