import { ethers } from 'ethers';
import exoskeletons from '../sites/exoskeletons.js';

/**
 * Exo Identity Middleware.
 *
 * Auto-resolves Exoskeleton identity for a wallet address.
 * Attaches identity to a Reach instance so it's available as reach.identity.
 */

const RPC = 'https://base-rpc.publicnode.com';

/**
 * Resolve Exo identity for a wallet address.
 * Returns the profile of the first owned Exo, or null if the wallet has none.
 *
 * @param {string} walletAddress - Ethereum address
 * @param {ethers.Provider} [provider] - Optional provider override
 * @returns {object|null} Identity object with name, bio, reputation, elo, etc.
 */
export async function resolveIdentity(walletAddress, provider) {
  const p = provider || new ethers.JsonRpcProvider(RPC);

  const owns = await exoskeletons.hasExo(walletAddress, p);
  if (!owns) return null;

  const tokenIds = await exoskeletons.getOwnedExos(walletAddress, p);
  if (tokenIds.length === 0) return null;

  // Use the first Exo as primary identity
  const primaryId = tokenIds[0];
  const profile = await exoskeletons.getProfile(primaryId, p);
  const reputation = await exoskeletons.getReputation(primaryId, p);
  const elo = await exoskeletons.getELO(primaryId, p);

  return {
    walletAddress,
    primaryExoId: primaryId,
    allExoIds: tokenIds,
    name: profile.name,
    bio: profile.bio,
    config: profile.config,
    reputation: reputation || profile.reputation,
    elo: elo?.elo || profile.elo,
    eloStats: elo,
    modules: profile.modules,
    walletBalance: profile.walletBalance,
  };
}

/**
 * Attach an identity object to a Reach instance.
 * Makes it available as reach.identity.
 *
 * @param {object} reach - Reach instance
 * @param {object|null} identity - Identity from resolveIdentity()
 */
export function attachIdentity(reach, identity) {
  reach.identity = identity;
}

export default { resolveIdentity, attachIdentity };
