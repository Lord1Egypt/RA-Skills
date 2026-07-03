export const minterAbi = [
  {
    type: 'function',
    name: 'phaseCount',
    stateMutability: 'view',
    inputs: [],
    outputs: [{ type: 'uint32' }],
  },
  {
    type: 'function',
    name: 'phases',
    stateMutability: 'view',
    inputs: [{ name: '', type: 'uint256' }],
    outputs: [
      { name: 'payment', type: 'uint8' },
      { name: 'price', type: 'uint256' },
      { name: 'maxMints', type: 'uint32' },
      { name: 'maxPerWallet', type: 'uint32' },
      { name: 'startTimestamp', type: 'uint64' },
      { name: 'endTimestamp', type: 'uint64' },
      { name: 'merkleRoot', type: 'bytes32' },
      { name: 'curveDeltaWad', type: 'uint256' },
      { name: 'curveFloorPrice', type: 'uint256' },
      { name: 'curveCeilingPrice', type: 'uint256' },
    ],
  },
  {
    type: 'function',
    name: 'phaseMintCount',
    stateMutability: 'view',
    inputs: [{ name: 'phaseId', type: 'uint32' }],
    outputs: [{ type: 'uint32' }],
  },
  {
    type: 'function',
    name: 'walletPhaseMintCount',
    stateMutability: 'view',
    inputs: [
      { name: 'phaseId', type: 'uint32' },
      { name: 'wallet', type: 'address' },
    ],
    outputs: [{ type: 'uint32' }],
  },
  {
    type: 'function',
    name: 'mintNonce',
    stateMutability: 'view',
    inputs: [{ name: 'user', type: 'address' }],
    outputs: [{ type: 'uint256' }],
  },
  {
    type: 'function',
    name: 'mintParamsHash',
    stateMutability: 'view',
    inputs: [
      { name: 'phaseId', type: 'uint32' },
      { name: 'quantity', type: 'uint32' },
      { name: 'maxPayment', type: 'uint256' },
    ],
    outputs: [{ type: 'bytes32' }],
  },
  {
    type: 'function',
    name: 'currentMintPrice',
    stateMutability: 'view',
    inputs: [
      { name: 'phaseId', type: 'uint32' },
      { name: 'quantity', type: 'uint32' },
    ],
    outputs: [{ type: 'uint256' }],
  },
  {
    type: 'function',
    name: 'mintBatchWithTickets',
    stateMutability: 'payable',
    inputs: [
      { name: 'phaseId', type: 'uint32' },
      { name: 'merkleProof', type: 'bytes32[]' },
      {
        name: 'tickets',
        type: 'tuple[]',
        components: [
          { name: 'action', type: 'uint8' },
          { name: 'user', type: 'address' },
          { name: 'nonce', type: 'uint256' },
          { name: 'deadline', type: 'uint64' },
          { name: 'serverSeed', type: 'bytes32' },
          { name: 'paramsHash', type: 'bytes32' },
        ],
      },
      { name: 'signatures', type: 'bytes[]' },
      { name: 'maxPayment', type: 'uint256' },
    ],
    outputs: [{ name: 'tokenIds', type: 'uint256[]' }],
  },
];
export const erc20Abi = [
  {
    type: 'function',
    name: 'allowance',
    stateMutability: 'view',
    inputs: [
      { name: 'owner', type: 'address' },
      { name: 'spender', type: 'address' },
    ],
    outputs: [{ type: 'uint256' }],
  },
  {
    type: 'function',
    name: 'approve',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'spender', type: 'address' },
      { name: 'amount', type: 'uint256' },
    ],
    outputs: [{ type: 'bool' }],
  },
  {
    type: 'function',
    name: 'balanceOf',
    stateMutability: 'view',
    inputs: [{ name: 'account', type: 'address' }],
    outputs: [{ type: 'uint256' }],
  },
];

export const vaultAbi = [
  {
    type: 'function',
    name: 'claimNonce',
    stateMutability: 'view',
    inputs: [{ name: 'user', type: 'address' }],
    outputs: [{ type: 'uint256' }],
  },
  {
    type: 'function',
    name: 'pendingSheepYield',
    stateMutability: 'view',
    inputs: [{ name: 'chibiId', type: 'uint256' }],
    outputs: [
      { name: 'uruOut', type: 'uint256' },
      { name: 'wethOut', type: 'uint256' },
    ],
  },
  {
    type: 'function',
    name: 'pendingWolfYield',
    stateMutability: 'view',
    inputs: [{ name: 'chibiId', type: 'uint256' }],
    outputs: [
      { name: 'uruOut', type: 'uint256' },
      { name: 'wethOut', type: 'uint256' },
    ],
  },
];

export const coreAbi = [
  {
    type: 'function',
    name: 'roleOf',
    stateMutability: 'view',
    inputs: [{ name: 'tokenId', type: 'uint256' }],
    outputs: [{ type: 'uint8' }],
  },
];
