/**
 * SUIROLL Signer Utilities
 * Helper functions for transaction signing using @mysten/sui v1 SDK
 */

import { SuiClient, getFullnodeUrl } from '@mysten/sui/client';
import { Ed25519Keypair } from '@mysten/sui/keypairs/ed25519';
import { decodeSuiPrivateKey } from '@mysten/sui/cryptography';
import { Transaction } from '@mysten/sui/transactions';

export type Network = 'mainnet' | 'testnet';

/**
 * Get Sui client for a specific network
 */
export function getClient(network: Network = 'testnet'): SuiClient {
  const rpcUrl = getFullnodeUrl(network);
  return new SuiClient({ url: rpcUrl });
}

/**
 * Get keypair from environment variable.
 * Supports:
 * - Sui bech32 private key (starts with `suiprivkey...`) [recommended]
 * - Hex string (optionally prefixed with 0x) representing 32-byte ed25519 secret key
 */
export function getKeypair(): Ed25519Keypair {
  const privateKey = process.env.SUI_PRIVATE_KEY;

  if (!privateKey) {
    throw new Error(
      'SUI_PRIVATE_KEY not set. Please export your private key:\n' +
        '  export SUI_PRIVATE_KEY=suiprivkey...\n' +
        'or (legacy) hex 32-byte secret:\n' +
        '  export SUI_PRIVATE_KEY=0x...'
    );
  }

  if (privateKey.startsWith('suiprivkey')) {
    const parsed = decodeSuiPrivateKey(privateKey);
    return Ed25519Keypair.fromSecretKey(parsed.secretKey);
  }

  const cleaned = privateKey.startsWith('0x') ? privateKey.slice(2) : privateKey;
  return Ed25519Keypair.fromSecretKey(Buffer.from(cleaned, 'hex'));
}

/**
 * Build, sign, and execute a transaction.
 */
export async function executeTransaction(tx: Transaction, network: Network = 'testnet') {
  const client = getClient(network);
  const keypair = getKeypair();

  // Get sender address from keypair
  const sender = keypair.getPublicKey().toSuiAddress();
  tx.setSender(sender);

  const bytes = await tx.build({ client });
  const signed = await keypair.signTransaction(bytes);

  return await client.executeTransactionBlock({
    transactionBlock: signed.bytes,
    signature: signed.signature,
    options: { showEffects: true, showEvents: true },
    requestType: 'WaitForEffectsCert',
  });
}
