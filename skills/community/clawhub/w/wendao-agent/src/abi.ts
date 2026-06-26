/** 合约 ABI — 仅 Agent 需要的函数 */

export const NFA_ABI = [
  { name: "getWarrior", type: "function", stateMutability: "view", inputs: [{ name: "tokenId", type: "uint256" }], outputs: [{ type: "tuple", components: [
    { name: "personality", type: "uint8[5]" }, { name: "realm", type: "uint8" }, { name: "level", type: "uint8" },
    { name: "xp", type: "uint256" }, { name: "baseStats", type: "uint16[5]" }, { name: "unspentSP", type: "uint16" },
    { name: "xHandle", type: "string" }, { name: "merkleRoot", type: "bytes32" }, { name: "referrer", type: "uint256" }, { name: "createdAt", type: "uint256" },
  ]}] },
  { name: "ownerOf", type: "function", stateMutability: "view", inputs: [{ name: "tokenId", type: "uint256" }], outputs: [{ type: "address" }] },
  { name: "getAgentWallet", type: "function", stateMutability: "view", inputs: [{ name: "tokenId", type: "uint256" }], outputs: [{ type: "address" }] },
  { name: "levelUp", type: "function", stateMutability: "nonpayable", inputs: [{ name: "tokenId", type: "uint256" }], outputs: [] },
  { name: "distributeSP", type: "function", stateMutability: "nonpayable", inputs: [{ name: "tokenId", type: "uint256" }, { name: "allocation", type: "uint16[5]" }], outputs: [] },
  { name: "updateLearningTree", type: "function", stateMutability: "nonpayable", inputs: [{ name: "tokenId", type: "uint256" }, { name: "newRoot", type: "bytes32" }], outputs: [] },
] as const;

export const VAULT_ABI = [
  { name: "stake", type: "function", stateMutability: "nonpayable", inputs: [{ name: "amount", type: "uint256" }], outputs: [] },
  { name: "claimStakingReward", type: "function", stateMutability: "nonpayable", inputs: [], outputs: [] },
  { name: "startMeditation", type: "function", stateMutability: "nonpayable", inputs: [{ name: "tokenId", type: "uint256" }], outputs: [] },
  { name: "stopMeditation", type: "function", stateMutability: "nonpayable", inputs: [{ name: "tokenId", type: "uint256" }], outputs: [] },
  { name: "getMeditationInfo", type: "function", stateMutability: "view", inputs: [{ name: "tokenId", type: "uint256" }], outputs: [{ name: "startTime", type: "uint256" }, { name: "pendingXP", type: "uint256" }] },
  { name: "getStakeInfo", type: "function", stateMutability: "view", inputs: [{ name: "user", type: "address" }], outputs: [{ name: "staked", type: "uint256" }, { name: "pending", type: "uint256" }, { name: "unstakeTime", type: "uint256" }] },
  { name: "depositPK", type: "function", stateMutability: "nonpayable", inputs: [{ name: "tokenId", type: "uint256" }, { name: "tier", type: "uint8" }], outputs: [] },
  { name: "payBreakthrough", type: "function", stateMutability: "nonpayable", inputs: [{ name: "tokenId", type: "uint256" }], outputs: [] },
  { name: "claimSpiritReward", type: "function", stateMutability: "nonpayable", inputs: [], outputs: [] },
  { name: "inPK", type: "function", stateMutability: "view", inputs: [{ name: "", type: "uint256" }], outputs: [{ type: "bool" }] },
  { name: "settlePK", type: "function", stateMutability: "nonpayable", inputs: [
    { name: "winnerId", type: "uint256" }, { name: "loserId", type: "uint256" },
    { name: "tier", type: "uint8" }, { name: "nonce", type: "uint256" }, { name: "signature", type: "bytes" },
  ], outputs: [] },
  // SDK-03: cancelPK for recovery when backend is down
  { name: "cancelPK", type: "function", stateMutability: "nonpayable", inputs: [{ name: "tokenId", type: "uint256" }], outputs: [] },
  { name: "pkDepositTime", type: "function", stateMutability: "view", inputs: [{ name: "", type: "uint256" }], outputs: [{ type: "uint256" }] },
  { name: "pkTierOf", type: "function", stateMutability: "view", inputs: [{ name: "", type: "uint256" }], outputs: [{ type: "uint8" }] },
] as const;

export const TOKEN_ABI = [
  { name: "approve", type: "function", stateMutability: "nonpayable", inputs: [{ name: "spender", type: "address" }, { name: "value", type: "uint256" }], outputs: [{ type: "bool" }] },
  { name: "balanceOf", type: "function", stateMutability: "view", inputs: [{ name: "account", type: "address" }], outputs: [{ type: "uint256" }] },
  { name: "transfer", type: "function", stateMutability: "nonpayable", inputs: [{ name: "to", type: "address" }, { name: "value", type: "uint256" }], outputs: [{ type: "bool" }] },
] as const;
