import {
  createPublicClient,
  encodeAbiParameters,
  formatEther,
  getAddress,
  http,
  keccak256,
} from 'viem';
import { base } from 'viem/chains';

import { vaultAbi } from './abi.mjs';
import { requireRpc } from './config.mjs';

export function createChainClient(config) {
  requireRpc(config);
  return createPublicClient({
    chain: base,
    transport: http(config.rpcUrl),
  });
}
export const CLAIM_INTENT_TYPES = {
  ClaimIntent: [
    { name: 'user', type: 'address' },
    { name: 'nonce', type: 'uint256' },
    { name: 'deadline', type: 'uint64' },
    { name: 'tokenIdsHash', type: 'bytes32' },
  ],
};

export function claimDomain(chainId, vault) {
  return {
    name: 'UrufuClaims',
    version: '1',
    chainId,
    verifyingContract: vault,
  };
}

export function hashClaimTokenIds(tokenIds) {
  return keccak256(encodeAbiParameters([{ type: 'uint256[]' }], [[...tokenIds]]));
}

export async function readClaimNonce(client, vault, user) {  return client.readContract({
    address: vault,
    abi: vaultAbi,
    functionName: 'claimNonce',
    args: [getAddress(user)],
  });
}

export async function previewYieldForChibis(client, vault, chibis) {
  let totalUruWei = 0n;
  let totalWethWei = 0n;
  const eligible = [];

  for (const chibi of chibis) {
    const tokenId = BigInt(chibi.tokenId);
    const fn = chibi.role === 'wolf' ? 'pendingWolfYield' : 'pendingSheepYield';
    const [uruOut, wethOut] = await client.readContract({
      address: vault,
      abi: vaultAbi,
      functionName: fn,
      args: [tokenId],
    });

    if (uruOut > 0n || wethOut > 0n) {
      totalUruWei += uruOut;
      totalWethWei += wethOut;
      eligible.push(tokenId);
    }
  }

  return { totalUruWei, totalWethWei, tokenIds: eligible };
}

export function formatYieldReport(preview) {
  return {
    uru: formatEther(preview.totalUruWei),
    weth: formatEther(preview.totalWethWei),
    eligibleCount: preview.tokenIds.length,
  };
}

export async function signClaimIntent(account, config, tokenIds, nonce) {
  const tokenIdsHash = hashClaimTokenIds(tokenIds);
  const intentDeadline = BigInt(Math.floor(Date.now() / 1000) + config.claimIntentTtlSeconds);
  const message = {
    user: getAddress(config.wallet),
    nonce,
    deadline: intentDeadline,
    tokenIdsHash,
  };

  const intentSignature = await account.signTypedData({
    domain: claimDomain(config.chainId, config.vault),
    types: CLAIM_INTENT_TYPES,
    primaryType: 'ClaimIntent',
    message,
  });

  return { tokenIdsHash, intentDeadline, intentSignature, message };
}

export async function relayClaim(config, tokenIds, nonce, signed) {
  const res = await fetch(`${config.siteUrl}/api/gasless/claim`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chainId: config.chainId,
      contract: config.vault,
      user: getAddress(config.wallet),
      tokenIds: tokenIds.map((id) => id.toString()),
      nonce: nonce.toString(),
      tokenIdsHash: signed.tokenIdsHash,
      intentDeadline: signed.intentDeadline.toString(),
      intentSignature: signed.intentSignature,
    }),
  });

  const text = await res.text();
  let body;
  try {
    body = JSON.parse(text);
  } catch {
    body = { error: text };
  }

  if (!res.ok) {
    const err = new Error(body.error || res.statusText || 'claim relay failed');
    err.status = res.status;
    throw err;
  }
  return body;
}

export function chunkTokenIds(tokenIds, maxBatch) {
  const chunks = [];
  for (let i = 0; i < tokenIds.length; i += maxBatch) {
    chunks.push(tokenIds.slice(i, i + maxBatch));
  }
  return chunks;
}
