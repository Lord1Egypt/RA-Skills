/**
 * Seal decryption for WALVIS web frontend
 * Handles encrypted space decryption using @mysten/seal SDK + wallet connection
 */

import { SealClient, SessionKey } from '@mysten/seal';
import { SuiClient, getFullnodeUrl } from '@mysten/sui/client';
import { Transaction } from '@mysten/sui/transactions';
import { fromHex } from '@mysten/bcs';
import type { Space } from './types';

const SEAL_MODULE = 'access_policy';

// Testnet key server object IDs (from Seal docs)
const TESTNET_KEY_SERVERS = [
  '0x73d05d62c18d9374e3ea529e8e0ed6161da1a141a94d3f76ae3fe4e99356db75',
  '0xf5d14a81a982144ae441cd7d64b09027f116a468bd36e7eca494f750591623c8',
];

let sealClient: SealClient | null = null;

function getSealClient(suiClient: SuiClient): SealClient {
  if (!sealClient) {
    sealClient = new SealClient({
      suiClient,
      serverConfigs: TESTNET_KEY_SERVERS.map((id) => ({
        objectId: id,
        weight: 1,
      })),
      verifyKeyServers: false,
    });
  }
  return sealClient;
}

export interface DecryptResult {
  success: true;
  space: Space;
}

export interface DecryptError {
  success: false;
  error: string;
  code: 'NO_WALLET' | 'NO_ACCESS' | 'DECRYPT_FAILED' | 'INVALID_DATA';
}

export type DecryptOutcome = DecryptResult | DecryptError;

/**
 * Fetch encrypted blob from Walrus and decrypt using Seal.
 * Requires a connected wallet with signPersonalMessage capability.
 */
export async function fetchAndDecryptSpace(
  blobId: string,
  packageId: string,
  policyObjectId: string,
  walletAddress: string,
  signPersonalMessage: (input: { message: Uint8Array }) => Promise<{ signature: string }>,
): Promise<DecryptOutcome> {
  try {
    const suiClient = new SuiClient({ url: getFullnodeUrl('testnet') });
    const client = getSealClient(suiClient);

    // 1. Fetch encrypted blob from Walrus
    const res = await fetch(
      `https://aggregator.walrus-testnet.walrus.space/v1/blobs/${blobId}`,
    );
    if (!res.ok) {
      return { success: false, error: `Failed to fetch blob: ${res.status}`, code: 'DECRYPT_FAILED' };
    }
    const encryptedBytes = new Uint8Array(await res.arrayBuffer());

    // 2. Create session key
    const sessionKey = await SessionKey.create({
      address: walletAddress,
      packageId,
      ttlMin: 10,
      suiClient,
    });

    const message = sessionKey.getPersonalMessage();
    const { signature } = await signPersonalMessage({ message });
    sessionKey.setPersonalMessageSignature(signature);

    // 3. Build seal_approve transaction
    const tx = new Transaction();
    tx.moveCall({
      target: `${packageId}::${SEAL_MODULE}::seal_approve`,
      arguments: [
        tx.pure.vector('u8', fromHex(policyObjectId)),
        tx.object(policyObjectId),
      ],
    });

    const txBytes = await tx.build({ client: suiClient, onlyTransactionKind: true });

    // 4. Decrypt
    const decryptedBytes = await client.decrypt({
      data: encryptedBytes,
      sessionKey,
      txBytes,
    });

    // 5. Parse decrypted JSON
    const spaceJson = new TextDecoder().decode(decryptedBytes);
    const space = JSON.parse(spaceJson) as Space;

    return { success: true, space };
  } catch (err) {
    const message = (err as Error).message || 'Unknown error';
    if (message.includes('NoAccess') || message.includes('ENotAllowed')) {
      return { success: false, error: 'Your wallet does not have access to this space.', code: 'NO_ACCESS' };
    }
    return { success: false, error: message, code: 'DECRYPT_FAILED' };
  }
}

/**
 * Check if a space entry in the manifest is encrypted.
 */
export function isEncryptedSpace(
  spaceEntry: { encrypted?: boolean; policyObjectId?: string },
): boolean {
  return spaceEntry.encrypted === true && !!spaceEntry.policyObjectId;
}
