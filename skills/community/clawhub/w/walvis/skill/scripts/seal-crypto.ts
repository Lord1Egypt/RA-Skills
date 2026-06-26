/**
 * WALVIS Seal encryption/decryption helpers
 * Uses @mysten/seal SDK for client-side encryption with Sui-based access control.
 *
 * Encryption flow:  space JSON → Seal encrypt → encrypted bytes → upload to Walrus
 * Decryption flow:  download from Walrus → Seal decrypt (requires wallet + seal_approve) → space JSON
 *
 * Usage (CLI):
 *   seal-crypto encrypt <spaceId>              — encrypt + upload space
 *   seal-crypto enable <spaceId>               — create policy + encrypt space
 *   seal-crypto share <spaceId> <address>      — add address to allowlist
 *   seal-crypto unshare <spaceId> <address>    — remove from allowlist
 *   seal-crypto status <spaceId>               — show seal status
 */

import { SealClient, SessionKey } from '@mysten/seal';
import { SuiClient, getFullnodeUrl } from '@mysten/sui/client';
import { Transaction } from '@mysten/sui/transactions';
import { Ed25519Keypair } from '@mysten/sui/keypairs/ed25519';
import { fromHex, toHex } from '@mysten/bcs';
import { readFileSync } from 'fs';
import { readManifest, writeManifest, readSpace, writeSpace } from './storage.js';
import type { Space, SealConfig } from './types.js';

const SEAL_MODULE = 'access_policy';

// Testnet key server object IDs (from Seal docs)
const TESTNET_KEY_SERVERS = [
  '0x73d05d62c18d9374e3ea529e8e0ed6161da1a141a94d3f76ae3fe4e99356db75',
  '0xf5d14a81a982144ae441cd7d64b09027f116a468bd36e7eca494f750591623c8',
];
const TESTNET_SEAL_PACKAGE_ID = '0x299d7d7592c84d08a25ec26c777933d6ab72e51b31a615027186a0a377fe75cb';

function resolveSealPackageId(manifest = readManifest()): string | undefined {
  if (manifest.sealPackageId) return manifest.sealPackageId;
  if (manifest.network === 'testnet') {
    manifest.sealPackageId = TESTNET_SEAL_PACKAGE_ID;
    writeManifest(manifest);
    return manifest.sealPackageId;
  }
  return undefined;
}

function getSuiClient(): SuiClient {
  return new SuiClient({ url: getFullnodeUrl('testnet') });
}

function getSealClient(suiClient: SuiClient): SealClient {
  return new SealClient({
    suiClient,
    serverConfigs: TESTNET_KEY_SERVERS.map((id) => ({
      objectId: id,
      weight: 1,
    })),
    verifyKeyServers: false,
  });
}

function loadKeypair(): Ed25519Keypair {
  // Load from Sui CLI keystore
  const configPath = `${process.env.HOME}/.sui/sui_config/sui.keystore`;
  const keystore = JSON.parse(readFileSync(configPath, 'utf-8')) as string[];
  if (keystore.length === 0) {
    throw new Error('No keys found in ~/.sui/sui_config/sui.keystore');
  }
  return Ed25519Keypair.fromSecretKey(keystore[0]);
}

/**
 * Create a SpaceAccess policy object on Sui for a space.
 * Returns the policy object ID.
 */
export async function createAccessPolicy(
  spaceId: string,
  spaceName: string,
): Promise<string> {
  const manifest = readManifest();
  const packageId = resolveSealPackageId(manifest);
  if (!packageId) {
    throw new Error('sealPackageId not set. Deploy walvis_seal for this network and set manifest.sealPackageId.');
  }

  const suiClient = getSuiClient();
  const keypair = loadKeypair();

  const tx = new Transaction();
  tx.moveCall({
    target: `${packageId}::${SEAL_MODULE}::create_and_share`,
    arguments: [
      tx.pure.vector('u8', new TextEncoder().encode(spaceName)),
    ],
  });

  const result = await suiClient.signAndExecuteTransaction({
    transaction: tx,
    signer: keypair,
    options: { showObjectChanges: true },
  });

  // Find the created SpaceAccess shared object
  const created = result.objectChanges?.find(
    (c) => c.type === 'created' && c.objectType?.includes('SpaceAccess'),
  );
  if (!created || created.type !== 'created') {
    throw new Error('Failed to create SpaceAccess object');
  }

  return created.objectId;
}

/**
 * Encrypt space data using Seal.
 * Returns encrypted bytes and a backup key.
 */
export async function encryptSpaceData(
  spaceJson: string,
  packageId: string,
  policyObjectId: string,
): Promise<{ encryptedBytes: Uint8Array; backupKey: Uint8Array }> {
  const suiClient = getSuiClient();
  const sealClient = getSealClient(suiClient);
  const data = new TextEncoder().encode(spaceJson);

  const { encryptedObject, key } = await sealClient.encrypt({
    threshold: 2,
    packageId,
    id: policyObjectId,
    data,
  });

  return { encryptedBytes: encryptedObject, backupKey: key };
}

/**
 * Decrypt space data using Seal.
 * Requires the caller's wallet to pass seal_approve.
 */
export async function decryptSpaceData(
  encryptedBytes: Uint8Array,
  packageId: string,
  policyObjectId: string,
): Promise<string> {
  const suiClient = getSuiClient();
  const sealClient = getSealClient(suiClient);
  const keypair = loadKeypair();

  // Create a session key
  const sessionKey = await SessionKey.create({
    address: keypair.getPublicKey().toSuiAddress(),
    packageId,
    ttlMin: 10,
    suiClient,
  });

  const message = sessionKey.getPersonalMessage();
  const { signature } = await keypair.signPersonalMessage(message);
  sessionKey.setPersonalMessageSignature(signature);

  // Build the seal_approve transaction
  const tx = new Transaction();
  tx.moveCall({
    target: `${packageId}::${SEAL_MODULE}::seal_approve`,
    arguments: [
      tx.pure.vector('u8', fromHex(policyObjectId)),
      tx.object(policyObjectId),
    ],
  });

  const txBytes = await tx.build({ client: suiClient, onlyTransactionKind: true });

  const decryptedBytes = await sealClient.decrypt({
    data: encryptedBytes,
    sessionKey,
    txBytes,
  });

  return new TextDecoder().decode(decryptedBytes);
}

/**
 * Enable Seal encryption on a space.
 * Creates a policy object, encrypts, and updates manifest.
 */
export async function enableSealOnSpace(spaceId: string): Promise<SealConfig> {
  const manifest = readManifest();
  const space = readSpace(spaceId);

  if (space.seal?.encrypted) {
    throw new Error(`Space "${space.name}" is already encrypted.`);
  }

  const packageId = resolveSealPackageId(manifest);
  if (!packageId) {
    throw new Error('sealPackageId not set. Deploy walvis_seal for this network and set manifest.sealPackageId.');
  }

  // Create the on-chain access policy
  const policyObjectId = await createAccessPolicy(spaceId, space.name);

  const sealConfig: SealConfig = {
    encrypted: true,
    packageId,
    policyObjectId,
    allowlist: [],
  };

  // Update space with seal config
  space.seal = sealConfig;
  space.updatedAt = new Date().toISOString();
  writeSpace(space);

  // Update manifest
  const spaceEntry = manifest.spaces[spaceId];
  if (spaceEntry) {
    spaceEntry.encrypted = true;
    spaceEntry.policyObjectId = policyObjectId;
  }
  writeManifest(manifest);

  return sealConfig;
}

/**
 * Add an address to the space's allowlist on-chain.
 */
export async function addToAllowlist(spaceId: string, address: string): Promise<void> {
  const manifest = readManifest();
  const space = readSpace(spaceId);

  if (!space.seal?.encrypted) {
    throw new Error(`Space "${space.name}" is not encrypted.`);
  }

  const suiClient = getSuiClient();
  const keypair = loadKeypair();

  const tx = new Transaction();
  tx.moveCall({
    target: `${space.seal.packageId}::${SEAL_MODULE}::add_to_allowlist`,
    arguments: [
      tx.object(space.seal.policyObjectId),
      tx.pure.address(address),
    ],
  });

  await suiClient.signAndExecuteTransaction({
    transaction: tx,
    signer: keypair,
  });

  // Update local state
  if (!space.seal.allowlist.includes(address)) {
    space.seal.allowlist.push(address);
  }
  space.updatedAt = new Date().toISOString();
  writeSpace(space);
}

/**
 * Remove an address from the space's allowlist on-chain.
 */
export async function removeFromAllowlist(spaceId: string, address: string): Promise<void> {
  const manifest = readManifest();
  const space = readSpace(spaceId);

  if (!space.seal?.encrypted) {
    throw new Error(`Space "${space.name}" is not encrypted.`);
  }

  const suiClient = getSuiClient();
  const keypair = loadKeypair();

  const tx = new Transaction();
  tx.moveCall({
    target: `${space.seal.packageId}::${SEAL_MODULE}::remove_from_allowlist`,
    arguments: [
      tx.object(space.seal.policyObjectId),
      tx.pure.address(address),
    ],
  });

  await suiClient.signAndExecuteTransaction({
    transaction: tx,
    signer: keypair,
  });

  // Update local state
  space.seal.allowlist = space.seal.allowlist.filter((a) => a !== address);
  space.updatedAt = new Date().toISOString();
  writeSpace(space);
}

/**
 * Get the seal status of a space.
 */
export function getSealStatus(spaceId: string): {
  encrypted: boolean;
  packageId?: string;
  policyObjectId?: string;
  allowlist?: string[];
} {
  const space = readSpace(spaceId);
  if (!space.seal?.encrypted) {
    return { encrypted: false };
  }
  return {
    encrypted: true,
    packageId: space.seal.packageId,
    policyObjectId: space.seal.policyObjectId,
    allowlist: space.seal.allowlist,
  };
}

// ─── CLI entry point ────────────────────────────────────────

const [, , cmd, arg1, arg2] = process.argv;

if (cmd === 'enable') {
  if (!arg1) {
    console.error('Usage: seal-crypto enable <spaceId>');
    process.exit(1);
  }
  try {
    const config = await enableSealOnSpace(arg1);
    console.log(`Seal enabled on space "${arg1}"`);
    console.log(`  Policy Object: ${config.policyObjectId}`);
    console.log(`  Package ID: ${config.packageId}`);
    console.log('Next: run "walrus-sync up" to upload the encrypted space.');
  } catch (err) {
    console.error(`Failed: ${(err as Error).message}`);
    process.exit(1);
  }
} else if (cmd === 'share') {
  if (!arg1 || !arg2) {
    console.error('Usage: seal-crypto share <spaceId> <address>');
    process.exit(1);
  }
  try {
    await addToAllowlist(arg1, arg2);
    console.log(`Added ${arg2} to allowlist for space "${arg1}"`);
  } catch (err) {
    console.error(`Failed: ${(err as Error).message}`);
    process.exit(1);
  }
} else if (cmd === 'unshare') {
  if (!arg1 || !arg2) {
    console.error('Usage: seal-crypto unshare <spaceId> <address>');
    process.exit(1);
  }
  try {
    await removeFromAllowlist(arg1, arg2);
    console.log(`Removed ${arg2} from allowlist for space "${arg1}"`);
  } catch (err) {
    console.error(`Failed: ${(err as Error).message}`);
    process.exit(1);
  }
} else if (cmd === 'status') {
  if (!arg1) {
    console.error('Usage: seal-crypto status <spaceId>');
    process.exit(1);
  }
  const status = getSealStatus(arg1);
  if (!status.encrypted) {
    console.log(`Space "${arg1}" is NOT encrypted.`);
  } else {
    console.log(`Space "${arg1}" — Seal Encrypted`);
    console.log(`  Package: ${status.packageId}`);
    console.log(`  Policy Object: ${status.policyObjectId}`);
    console.log(`  Allowlist: ${status.allowlist?.length ? status.allowlist.join(', ') : '(owner only)'}`);
  }
} else if (cmd) {
  console.error(`Unknown command: ${cmd}. Use: enable | share | unshare | status`);
  process.exit(1);
}
