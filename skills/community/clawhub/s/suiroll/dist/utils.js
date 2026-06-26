/**
 * SUIROLL Sui Client Wrapper
 * Helper functions for Sui blockchain interaction
 */
import { Ed25519Keypair } from '@mysten/sui/keypairs/ed25519';
import { getFullnodeUrl, SuiClient } from '@mysten/sui/client';
import { config } from './config.js';
/**
 * Get Sui client for a specific network
 */
export function getClient(network = 'testnet') {
    const rpcUrl = getFullnodeUrl(network);
    return new SuiClient({ url: rpcUrl });
}
/**
 * Get keypair from environment or generate new one
 */
export function getKeypair() {
    const privateKey = process.env.SUI_PRIVATE_KEY;
    if (privateKey) {
        return Ed25519Keypair.fromSecretKey(Buffer.from(privateKey.replace(/^0x/, ''), 'hex'));
    }
    // Generate new keypair for development
    console.log('⚠️  No SUI_PRIVATE_KEY found in environment');
    console.log('   Generating new keypair for development...\n');
    const keypair = Ed25519Keypair.generate();
    console.log('📝 New keypair generated:');
    console.log(`   Address: ${keypair.getPublicKey().toSuiAddress()}`);
    console.log(`   Private Key: ${keypair.getSecretKey()}`);
    console.log('\n💾 Save this keypair securely!');
    console.log('   Export: export SUI_PRIVATE_KEY=<private-key>\n');
    return keypair;
}
/**
 * Validate Sui address format
 */
export function isValidSuiAddress(address) {
    try {
        const cleaned = address.replace(/^0x/, '');
        if (cleaned.length !== 64)
            return false;
        return /^[0-9a-fA-F]+$/.test(cleaned);
    }
    catch {
        return false;
    }
}
/**
 * Validate Object ID format
 */
export function isValidObjectId(id) {
    return isValidSuiAddress(id);
}
/**
 * Format MIST to SUI (1 SUI = 10^9 MIST)
 */
export function mistToSui(mist) {
    const mistAmount = typeof mist === 'string' ? parseInt(mist, 10) : mist;
    return (mistAmount / 1_000_000_000).toFixed(9);
}
/**
 * Format SUI to MIST
 */
export function suiToMist(sui) {
    return Math.floor(sui * 1_000_000_000).toString();
}
/**
 * Parse USDC amount (assuming 6 decimals)
 */
export function parseUSDC(amount) {
    const [whole, fraction] = amount.split('.');
    const paddedFraction = (fraction || '0').padEnd(6, '0').slice(0, 6);
    return BigInt(whole) * BigInt(1_000_000) + BigInt(paddedFraction);
}
/**
 * Format USDC amount
 */
export function formatUSDC(amount) {
    const whole = amount / BigInt(1_000_000);
    const fraction = amount % BigInt(1_000_000);
    return `${whole}.${fraction.toString().padStart(6, '0')}`;
}
/**
 * Get configuration for a specific network
 */
export function getNetworkConfig(network) {
    return config[network];
}
//# sourceMappingURL=utils.js.map