import { createPublicClient, http, formatUnits, parseAbiItem, maxUint256, getAddress } from 'viem';
import { base } from 'viem/chains';

const client = createPublicClient({ chain: base, transport: http('https://mainnet.base.org') });

const APPROVAL_EVENT = parseAbiItem('event Approval(address indexed owner, address indexed spender, uint256 value)');
const APPROVAL_FOR_ALL_EVENT = parseAbiItem('event ApprovalForAll(address indexed owner, address indexed operator, bool approved)');

const KNOWN_TOKENS = {
  '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913': { symbol: 'USDC', decimals: 6 },
  '0x4200000000000000000000000000000000000006': { symbol: 'WETH', decimals: 18 },
  '0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb': { symbol: 'DAI', decimals: 18 },
  '0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA': { symbol: 'USDbC', decimals: 6 },
  '0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22': { symbol: 'cbETH', decimals: 18 },
  '0xB6fe221Fe9EeF5aBa221c348bA20A1Bf5e73624c': { symbol: 'rETH', decimals: 18 },
};

const KNOWN_ROUTERS = {
  '0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD': 'Uniswap Universal Router',
  '0x2626664c2603336E57B271c5C0b26F421741e481': 'Uniswap V3 Router',
  '0xDef1C0ded9bec7F1a1670819833240f027b25EfF': '0x Exchange Proxy',
  '0x1111111254EEB25477B68fb85Ed929f73A960582': '1inch Router v5',
  '0x6131B5fae19EA4f9D964eAc0408E4408b66337b5': 'KyberSwap',
  '0x198EF79F1F515F02dFE9e3115eD9fC07A7a084a0': 'Clanker LiquidityLocker',
  '0x000000000022D473030F116dDEE9F6B43aC78BA3': 'Permit2',
};

async function scanWallet(address) {
  const addr = getAddress(address);
  const results = {
    address: addr,
    scannedAt: new Date().toISOString(),
    chain: 'base',
    approvals: [],
    nftApprovals: [],
    ethBalance: '0',
    tokenBalances: {},
    summary: {
      totalTokensApproved: 0,
      unlimitedApprovals: 0,
      highRiskApprovals: 0,
      healthScore: 100,
      riskFlags: []
    }
  };

  // Get ETH balance
  const ethBal = await client.getBalance({ address: addr });
  results.ethBalance = formatUnits(ethBal, 18);

  // Check token balances
  for (const [token, info] of Object.entries(KNOWN_TOKENS)) {
    try {
      const bal = await client.readContract({
        address: token,
        abi: [{ name: 'balanceOf', type: 'function', stateMutability: 'view', inputs: [{ name: 'account', type: 'address' }], outputs: [{ name: '', type: 'uint256' }] }],
        functionName: 'balanceOf',
        args: [addr]
      });
      if (bal > 0n) {
        results.tokenBalances[info.symbol] = formatUnits(bal, info.decimals);
      }
    } catch(e) {}
  }

  // Get current block and scan in smaller chunks to avoid 413
  const currentBlock = await client.getBlockNumber();
  const CHUNK_SIZE = 10000n;
  const totalLookback = 100000n; // ~2 days on Base (2s blocks)
  const startBlock = currentBlock - totalLookback;
  
  const allApprovalLogs = [];
  const allNftLogs = [];
  
  for (let from = startBlock; from < currentBlock; from += CHUNK_SIZE) {
    const to = from + CHUNK_SIZE - 1n > currentBlock ? currentBlock : from + CHUNK_SIZE - 1n;
    
    try {
      const logs = await client.getLogs({
        event: APPROVAL_EVENT,
        args: { owner: addr },
        fromBlock: from,
        toBlock: to,
      });
      allApprovalLogs.push(...logs);
    } catch(e) {
      // Try with even smaller range
      try {
        const mid = from + (to - from) / 2n;
        const logs1 = await client.getLogs({ event: APPROVAL_EVENT, args: { owner: addr }, fromBlock: from, toBlock: mid });
        const logs2 = await client.getLogs({ event: APPROVAL_EVENT, args: { owner: addr }, fromBlock: mid + 1n, toBlock: to });
        allApprovalLogs.push(...logs1, ...logs2);
      } catch(e2) {}
    }
    
    try {
      const nftLogs = await client.getLogs({
        event: APPROVAL_FOR_ALL_EVENT,
        args: { owner: addr },
        fromBlock: from,
        toBlock: to,
      });
      allNftLogs.push(...nftLogs);
    } catch(e) {}
  }

  // Also check for approvals over ALL time via allowance checks on known tokens against known routers
  for (const [token, info] of Object.entries(KNOWN_TOKENS)) {
    for (const [router, name] of Object.entries(KNOWN_ROUTERS)) {
      try {
        const allowance = await client.readContract({
          address: token,
          abi: [{ name: 'allowance', type: 'function', stateMutability: 'view', inputs: [{ name: 'owner', type: 'address' }, { name: 'spender', type: 'address' }], outputs: [{ name: '', type: 'uint256' }] }],
          functionName: 'allowance',
          args: [addr, router]
        });
        if (allowance > 0n) {
          const isUnlimited = allowance >= maxUint256 / 2n;
          results.approvals.push({
            token: getAddress(token),
            tokenSymbol: info.symbol,
            spender: getAddress(router),
            spenderLabel: name,
            value: isUnlimited ? 'UNLIMITED' : formatUnits(allowance, info.decimals),
            isUnlimited,
            riskLevel: isUnlimited ? 'medium' : 'low',
            riskReasons: isUnlimited ? ['Unlimited token approval'] : [],
            source: 'allowance_check'
          });
          results.summary.totalTokensApproved++;
          if (isUnlimited) results.summary.unlimitedApprovals++;
        }
      } catch(e) {}
    }
  }

  // Process event-based approvals (add any not already found)
  const approvalMap = new Map();
  for (const log of allApprovalLogs) {
    const key = `${log.address}:${log.args.spender}`;
    const existing = approvalMap.get(key);
    if (!existing || log.blockNumber > existing.blockNumber) {
      approvalMap.set(key, log);
    }
  }
  for (const [key, log] of approvalMap) {
    const value = log.args.value;
    if (value === 0n) continue;
    const existingIdx = results.approvals.findIndex(a => 
      a.token.toLowerCase() === getAddress(log.address).toLowerCase() && 
      a.spender.toLowerCase() === getAddress(log.args.spender).toLowerCase()
    );
    if (existingIdx >= 0) continue; // already have it
    
    const tokenInfo = KNOWN_TOKENS[getAddress(log.address)] || { symbol: log.address.slice(0,10), decimals: 18 };
    const spender = getAddress(log.args.spender);
    const isUnlimited = value >= maxUint256 / 2n;
    const routerName = KNOWN_ROUTERS[spender] || null;
    
    const approval = {
      token: getAddress(log.address),
      tokenSymbol: tokenInfo.symbol,
      spender,
      spenderLabel: routerName || 'Unknown',
      value: isUnlimited ? 'UNLIMITED' : formatUnits(value, tokenInfo.decimals),
      isUnlimited,
      blockNumber: Number(log.blockNumber),
      riskLevel: isUnlimited && !routerName ? 'high' : isUnlimited ? 'medium' : 'low',
      riskReasons: [],
      source: 'event_log'
    };
    if (isUnlimited && !routerName) {
      approval.riskReasons.push('Unlimited approval to unknown contract');
      results.summary.highRiskApprovals++;
    }
    if (isUnlimited) {
      results.summary.unlimitedApprovals++;
      approval.riskReasons.push('Unlimited token approval');
    }
    results.approvals.push(approval);
    results.summary.totalTokensApproved++;
  }

  // NFT approvals
  const nftMap = new Map();
  for (const log of allNftLogs) {
    const key = `${log.address}:${log.args.operator}`;
    const existing = nftMap.get(key);
    if (!existing || log.blockNumber > existing.blockNumber) {
      nftMap.set(key, log);
    }
  }
  for (const [key, log] of nftMap) {
    if (!log.args.approved) continue;
    results.nftApprovals.push({
      collection: getAddress(log.address),
      operator: getAddress(log.args.operator),
      operatorLabel: KNOWN_ROUTERS[getAddress(log.args.operator)] || 'Unknown',
      blockNumber: Number(log.blockNumber),
    });
  }

  // Get tx count for activity assessment
  const txCount = await client.getTransactionCount({ address: addr });
  results.txCount = txCount;

  // Calculate health score
  let score = 100;
  score -= results.summary.unlimitedApprovals * 10;
  score -= results.summary.highRiskApprovals * 20;
  score -= results.nftApprovals.length * 5;
  results.summary.healthScore = Math.max(0, Math.min(100, score));

  return results;
}

const address = process.argv[2];
if (!address) { console.error('Usage: node scan-wallet-case-study.mjs <address>'); process.exit(1); }
scanWallet(address).then(r => console.log(JSON.stringify(r, null, 2))).catch(e => { console.error(e.message); process.exit(1); });
