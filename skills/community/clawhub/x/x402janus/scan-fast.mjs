import { createPublicClient, http, formatUnits, maxUint256, getAddress } from 'viem';
import { base } from 'viem/chains';

const client = createPublicClient({ chain: base, transport: http('https://mainnet.base.org') });

const TOKENS = {
  '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913': { symbol: 'USDC', decimals: 6 },
  '0x4200000000000000000000000000000000000006': { symbol: 'WETH', decimals: 18 },
  '0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb': { symbol: 'DAI', decimals: 18 },
  '0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA': { symbol: 'USDbC', decimals: 6 },
  '0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22': { symbol: 'cbETH', decimals: 18 },
  '0xB6fe221Fe9EeF5aBa221c348bA20A1Bf5e73624c': { symbol: 'rETH', decimals: 18 },
  '0x0b3e328455c4059EEb9e3f84b5543F74E24e7E1b': { symbol: 'VIRTUAL', decimals: 18 },
  '0x768BE13e1680b5ebE0024C42c896E3dB59ec0149': { symbol: 'AERO', decimals: 18 },
};

const SPENDERS = {
  '0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD': 'Uniswap Universal Router',
  '0x2626664c2603336E57B271c5C0b26F421741e481': 'Uniswap V3 Router',
  '0xDef1C0ded9bec7F1a1670819833240f027b25EfF': '0x Exchange Proxy',
  '0x1111111254EEB25477B68fb85Ed929f73A960582': '1inch Router v5',
  '0x6131B5fae19EA4f9D964eAc0408E4408b66337b5': 'KyberSwap',
  '0x198EF79F1F515F02dFE9e3115eD9fC07A7a084a0': 'Clanker LiquidityLocker',
  '0x000000000022D473030F116dDEE9F6B43aC78BA3': 'Permit2',
  '0xcF77a3Ba9A5CA399B7c97c74d54e5b1Beb874E43': 'Aerodrome Router',
  '0x6Cb442acF35158D5eDa88fe602221b67B400Be3E': 'Aerodrome V2 Router',
  '0xBE6D8f0d05cC4be24d5167a3eF062215bE6D18a5': 'CowSwap',
  '0x111111125421cA6dc452d289314280a0f8842A65': '1inch Router v6',
  '0xEf740bf4CDa27090BE89766e5c93E6E55361FDe1': 'Virtuals Router',
};

const balAbi = [{ name: 'balanceOf', type: 'function', stateMutability: 'view', inputs: [{ name: '', type: 'address' }], outputs: [{ name: '', type: 'uint256' }] }];
const allowAbi = [{ name: 'allowance', type: 'function', stateMutability: 'view', inputs: [{ name: '', type: 'address' }, { name: '', type: 'address' }], outputs: [{ name: '', type: 'uint256' }] }];

async function scan(address) {
  const addr = getAddress(address);
  const result = {
    address: addr,
    scannedAt: new Date().toISOString(),
    chain: 'base',
    ethBalance: '0',
    tokenBalances: {},
    approvals: [],
    txCount: 0,
    summary: { totalTokensApproved: 0, unlimitedApprovals: 0, highRiskApprovals: 0, healthScore: 100, riskFlags: [] }
  };

  // ETH + tx count
  const [ethBal, txCount] = await Promise.all([
    client.getBalance({ address: addr }),
    client.getTransactionCount({ address: addr })
  ]);
  result.ethBalance = formatUnits(ethBal, 18);
  result.txCount = txCount;

  // Token balances (parallel)
  const balPromises = Object.entries(TOKENS).map(async ([token, info]) => {
    try {
      const bal = await client.readContract({ address: token, abi: balAbi, functionName: 'balanceOf', args: [addr] });
      if (bal > 0n) result.tokenBalances[info.symbol] = formatUnits(bal, info.decimals);
    } catch(e) {}
  });
  await Promise.all(balPromises);

  // Allowance checks (parallel batches to avoid rate limits)
  const allowChecks = [];
  for (const [token, tInfo] of Object.entries(TOKENS)) {
    for (const [spender, sLabel] of Object.entries(SPENDERS)) {
      allowChecks.push({ token, tInfo, spender, sLabel });
    }
  }
  
  // Run in batches of 20
  for (let i = 0; i < allowChecks.length; i += 20) {
    const batch = allowChecks.slice(i, i + 20);
    const promises = batch.map(async ({ token, tInfo, spender, sLabel }) => {
      try {
        const allowance = await client.readContract({ address: token, abi: allowAbi, functionName: 'allowance', args: [addr, spender] });
        if (allowance > 0n) {
          const isUnlimited = allowance >= maxUint256 / 2n;
          result.approvals.push({
            token: getAddress(token), tokenSymbol: tInfo.symbol,
            spender: getAddress(spender), spenderLabel: sLabel,
            value: isUnlimited ? 'UNLIMITED' : formatUnits(allowance, tInfo.decimals),
            isUnlimited,
            riskLevel: isUnlimited ? 'medium' : 'low',
            riskReasons: isUnlimited ? ['Unlimited token approval'] : []
          });
          result.summary.totalTokensApproved++;
          if (isUnlimited) result.summary.unlimitedApprovals++;
        }
      } catch(e) {}
    });
    await Promise.all(promises);
  }

  // Score
  let score = 100;
  score -= result.summary.unlimitedApprovals * 10;
  score -= result.summary.highRiskApprovals * 20;
  result.summary.healthScore = Math.max(0, Math.min(100, score));
  
  return result;
}

scan(process.argv[2]).then(r => console.log(JSON.stringify(r, null, 2))).catch(e => { console.error(e.message); process.exit(1); });
