import { ethers } from 'ethers';

/**
 * Exoskeletons site skill.
 *
 * Read Exo profiles, check ownership, query reputation, ELO, Board history.
 * All reads go direct to Base mainnet via JSON-RPC — no browser needed.
 */

const RPC = 'https://base-rpc.publicnode.com';

const ADDRESSES = {
  core: '0x8241BDD5009ed3F6C99737D2415994B58296Da0d',
  reader: '0x334F8F78D0255228d388036560f1D1516fBD09a5',
  reputationOracle: '0xB4eEeaEcAdDb9F3fbcD1f529533a832afb6C60b4',
  outlier: '0x8F7403D5809Dd7245dF268ab9D596B3299A84B5C',
  board: '0x27a62eD97C9CC0ce71AC20bdb6E002c0ca040213',
  escrow: '0x2574BD275d5ba939c28654745270C37554387ee5',
  marketplace: '0x0E760171da676c219F46f289901D0be1CBD06188',
};

// Minimal ABIs — only the view functions we call
const CORE_ABI = [
  'function balanceOf(address owner) view returns (uint256)',
  'function tokenOfOwnerByIndex(address owner, uint256 index) view returns (uint256)',
  'function ownerOf(uint256 tokenId) view returns (address)',
  'function totalSupply() view returns (uint256)',
];

const READER_ABI = [
  'function getProfile(uint256 tokenId) view returns (string name, string bio, bytes config, uint256 reputation, uint256 elo, bytes32[] modules, uint256 walletBalance)',
];

const REPUTATION_ABI = [
  'function getReputation(uint256 tokenId) view returns (uint256)',
  'function getScore(uint256 tokenId, bytes32 scoreType) view returns (int256)',
];

const OUTLIER_ABI = [
  'function getPlayerStats(address player) view returns (uint256 elo, uint256 gamesPlayed, uint256 wins, uint256 losses)',
];

const BOARD_ABI = [
  'function listingCount() view returns (uint256)',
  'function listings(uint256 id) view returns (address provider, string title, string description, uint256 price, uint8 status, uint256 createdAt)',
];

const ESCROW_ABI = [
  'function escrowCount() view returns (uint256)',
  'function escrows(uint256 id) view returns (address client, address provider, uint256 amount, uint8 status, uint256 listingId, uint256 createdAt, uint256 completedAt)',
];

function getProvider() {
  return new ethers.JsonRpcProvider(RPC);
}

/**
 * Read any Exo's full profile from chain via ExoReader.
 *
 * @param {number} tokenId - Exoskeleton token ID
 * @param {ethers.Provider} [provider] - Optional provider override
 * @returns {object} { name, bio, config, reputation, elo, modules, walletBalance }
 */
export async function getProfile(tokenId, provider) {
  const p = provider || getProvider();
  const reader = new ethers.Contract(ADDRESSES.reader, READER_ABI, p);

  try {
    const result = await reader.getProfile(tokenId);
    return {
      tokenId,
      name: result.name,
      bio: result.bio,
      config: result.config,
      reputation: Number(result.reputation),
      elo: Number(result.elo),
      modules: result.modules,
      walletBalance: result.walletBalance.toString(),
    };
  } catch (e) {
    // ExoReader may not have getProfile — fall back to Core
    const core = new ethers.Contract(ADDRESSES.core, [
      'function getIdentity(uint256 tokenId) view returns (string name, string bio, bytes visualConfig, string customVisualKey, uint256 mintedAt, bool genesis)',
    ], p);
    const identity = await core.getIdentity(tokenId);
    return {
      tokenId,
      name: identity.name,
      bio: identity.bio,
      config: identity.visualConfig,
      reputation: 0,
      elo: 0,
      modules: [],
      walletBalance: '0',
    };
  }
}

/**
 * Check if an address owns at least one Exoskeleton.
 *
 * @param {string} address - Wallet address
 * @param {ethers.Provider} [provider]
 * @returns {boolean}
 */
export async function hasExo(address, provider) {
  const p = provider || getProvider();
  const core = new ethers.Contract(ADDRESSES.core, CORE_ABI, p);
  const balance = await core.balanceOf(address);
  return Number(balance) > 0;
}

/**
 * Get all Exoskeleton token IDs owned by an address.
 *
 * @param {string} address - Wallet address
 * @param {ethers.Provider} [provider]
 * @returns {number[]} Array of token IDs
 */
export async function getOwnedExos(address, provider) {
  const p = provider || getProvider();
  const core = new ethers.Contract(ADDRESSES.core, CORE_ABI, p);
  const balance = Number(await core.balanceOf(address));
  if (balance === 0) return [];

  const ids = [];
  for (let i = 0; i < balance; i++) {
    const tokenId = await core.tokenOfOwnerByIndex(address, i);
    ids.push(Number(tokenId));
  }
  return ids;
}

/**
 * Get composite reputation score for an Exoskeleton.
 *
 * @param {number} tokenId
 * @param {ethers.Provider} [provider]
 * @returns {number} Reputation score
 */
export async function getReputation(tokenId, provider) {
  const p = provider || getProvider();
  try {
    const oracle = new ethers.Contract(ADDRESSES.reputationOracle, REPUTATION_ABI, p);
    const rep = await oracle.getReputation(tokenId);
    return Number(rep);
  } catch {
    // Oracle may not have getReputation, try composite-reputation score key
    try {
      const oracle = new ethers.Contract(ADDRESSES.reputationOracle, REPUTATION_ABI, p);
      const key = ethers.keccak256(ethers.toUtf8Bytes('composite-reputation'));
      const score = await oracle.getScore(tokenId, key);
      return Number(score);
    } catch {
      return 0;
    }
  }
}

/**
 * Get ELO rating from Agent Outlier for an Exo's TBA.
 *
 * @param {number} tokenId
 * @param {ethers.Provider} [provider]
 * @returns {object} { elo, gamesPlayed, wins, losses } or null if not a player
 */
export async function getELO(tokenId, provider) {
  const p = provider || getProvider();

  // First get the TBA address for this Exo
  const walletContract = new ethers.Contract(
    ADDRESSES.core,
    ['function tokenWallet(uint256 tokenId) view returns (address)'],
    p
  );

  try {
    const tba = await walletContract.tokenWallet(tokenId);
    if (!tba || tba === ethers.ZeroAddress) return null;

    const outlier = new ethers.Contract(ADDRESSES.outlier, OUTLIER_ABI, p);
    const stats = await outlier.getPlayerStats(tba);
    return {
      elo: Number(stats.elo),
      gamesPlayed: Number(stats.gamesPlayed),
      wins: Number(stats.wins),
      losses: Number(stats.losses),
    };
  } catch {
    return null;
  }
}

/**
 * Get Board/Escrow history for an address (completed jobs).
 *
 * @param {string} address - Provider or client address
 * @param {ethers.Provider} [provider]
 * @returns {object[]} Array of completed escrow records
 */
export async function getBoardHistory(address, provider) {
  const p = provider || getProvider();
  const escrow = new ethers.Contract(ADDRESSES.escrow, ESCROW_ABI, p);

  try {
    const count = Number(await escrow.escrowCount());
    const history = [];

    // Scan escrows for this address (as client or provider)
    // Limit scan to last 100 to avoid excessive RPC calls
    const start = Math.max(0, count - 100);
    for (let i = start; i < count; i++) {
      try {
        const e = await escrow.escrows(i);
        const addr = address.toLowerCase();
        if (e.client.toLowerCase() === addr || e.provider.toLowerCase() === addr) {
          history.push({
            id: i,
            client: e.client,
            provider: e.provider,
            amount: e.amount.toString(),
            status: Number(e.status),
            listingId: Number(e.listingId),
            createdAt: Number(e.createdAt),
            completedAt: Number(e.completedAt),
          });
        }
      } catch {
        // Skip individual escrow read failures
      }
    }

    return history;
  } catch {
    return [];
  }
}

export default {
  getProfile,
  hasExo,
  getOwnedExos,
  getReputation,
  getELO,
  getBoardHistory,
  ADDRESSES,
};
