import { ethers } from "ethers";
import dotenv from "dotenv";
import path from "path";
import { fileURLToPath } from "url";
import axios from "axios";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load .env from root of skill directory
dotenv.config({ path: path.join(__dirname, "../.env") });

// ANSI Terminal Colors
export const COLORS = {
  reset: "\x1b[0m",
  green: "\x1b[32m",
  red: "\x1b[31m",
  yellow: "\x1b[33m",
  cyan: "\x1b[36m",
  gray: "\x1b[90m",
  bold: "\x1b[1m"
};

export function printColor(text, color = "reset") {
  return `${COLORS[color] || ""}${text}${COLORS.reset}`;
}

export function logInfo(message, options = {}) {
  if (!options.json) {
    console.error(printColor(`ℹ ${message}`, "cyan"));
  }
}

export function logSuccess(message, options = {}) {
  if (!options.json) {
    console.error(printColor(`✔ ${message}`, "green"));
  }
}

export function logWarning(message, options = {}) {
  if (!options.json) {
    console.error(printColor(`⚠ ${message}`, "yellow"));
  }
}

export function logError(message, options = {}) {
  if (!options.json) {
    console.error(printColor(`✖ ${message}`, "red"));
  }
}

export const SUPPORTED_CHAINS = {
  ethereum: {
    id: 1,
    name: "Ethereum Mainnet",
    symbol: "ETH",
    rpc: process.env.ETH_RPC_URL || "https://1rpc.io/eth",
    rpcs: [
      process.env.ETH_RPC_URL,
      "https://1rpc.io/eth",
      "https://rpc.ankr.com/eth",
      "https://ethereum-rpc.publicnode.com",
      "https://cloudflare-eth.com"
    ].filter(Boolean),
    explorer: "https://etherscan.io"
  },
  arbitrum: {
    id: 42161,
    name: "Arbitrum One",
    symbol: "ETH",
    rpc: process.env.ARB_RPC_URL || "https://1rpc.io/arb",
    rpcs: [
      process.env.ARB_RPC_URL,
      "https://1rpc.io/arb",
      "https://rpc.ankr.com/arbitrum",
      "https://arbitrum-one-rpc.publicnode.com",
      "https://arb1.arbitrum.io/rpc"
    ].filter(Boolean),
    explorer: "https://arbiscan.io"
  },
  base: {
    id: 8453,
    name: "Base",
    symbol: "ETH",
    rpc: process.env.BASE_RPC_URL || "https://1rpc.io/base",
    rpcs: [
      process.env.BASE_RPC_URL,
      "https://1rpc.io/base",
      "https://rpc.ankr.com/base",
      "https://base-rpc.publicnode.com",
      "https://mainnet.base.org"
    ].filter(Boolean),
    explorer: "https://basescan.org"
  },
  optimism: {
    id: 10,
    name: "OP Mainnet",
    symbol: "ETH",
    rpc: process.env.OP_RPC_URL || "https://1rpc.io/op",
    rpcs: [
      process.env.OP_RPC_URL,
      "https://1rpc.io/op",
      "https://rpc.ankr.com/optimism",
      "https://optimism-rpc.publicnode.com",
      "https://mainnet.optimism.io"
    ].filter(Boolean),
    explorer: "https://optimistic.etherscan.io"
  },
  polygon: {
    id: 137,
    name: "Polygon PoS",
    symbol: "POL",
    rpc: process.env.POLYGON_RPC_URL || "https://1rpc.io/polygon",
    rpcs: [
      process.env.POLYGON_RPC_URL,
      "https://1rpc.io/polygon",
      "https://rpc.ankr.com/polygon",
      "https://polygon-bor-rpc.publicnode.com",
      "https://polygon-rpc.com"
    ].filter(Boolean),
    explorer: "https://polygonscan.com"
  },
  bsc: {
    id: 56,
    name: "BNB Smart Chain",
    symbol: "BNB",
    rpc: process.env.BSC_RPC_URL || "https://1rpc.io/bnb",
    rpcs: [
      process.env.BSC_RPC_URL,
      "https://1rpc.io/bnb",
      "https://rpc.ankr.com/bsc",
      "https://bsc-rpc.publicnode.com",
      "https://bsc-dataseed.binance.org"
    ].filter(Boolean),
    explorer: "https://bscscan.com"
  },
  avalanche: {
    id: 43114,
    name: "Avalanche C-Chain",
    symbol: "AVAX",
    rpc: process.env.AVAX_RPC_URL || "https://1rpc.io/avax",
    rpcs: [
      process.env.AVAX_RPC_URL,
      "https://1rpc.io/avax",
      "https://rpc.ankr.com/avalanche",
      "https://avalanche-c-chain-rpc.publicnode.com",
      "https://api.avax.network/ext/bc/C/rpc"
    ].filter(Boolean),
    explorer: "https://snowtrace.io"
  },
  linea: {
    id: 59144,
    name: "Linea",
    symbol: "ETH",
    rpc: process.env.LINEA_RPC_URL || "https://1rpc.io/linea",
    rpcs: [
      process.env.LINEA_RPC_URL,
      "https://1rpc.io/linea",
      "https://linea-rpc.publicnode.com",
      "https://rpc.linea.build"
    ].filter(Boolean),
    explorer: "https://lineascan.build"
  },
  scroll: {
    id: 534352,
    name: "Scroll",
    symbol: "ETH",
    rpc: process.env.SCROLL_RPC_URL || "https://1rpc.io/scroll",
    rpcs: [
      process.env.SCROLL_RPC_URL,
      "https://1rpc.io/scroll",
      "https://scroll-rpc.publicnode.com",
      "https://rpc.scroll.io"
    ].filter(Boolean),
    explorer: "https://scrollscan.com"
  },
  zksync: {
    id: 324,
    name: "zkSync Era",
    symbol: "ETH",
    rpc: process.env.ZKSYNC_RPC_URL || "https://1rpc.io/zksync2",
    rpcs: [
      process.env.ZKSYNC_RPC_URL,
      "https://1rpc.io/zksync2",
      "https://zksync-era-rpc.publicnode.com",
      "https://mainnet.era.zksync.io"
    ].filter(Boolean),
    explorer: "https://era.zksync.network"
  },
  sonic: {
    id: 146,
    name: "Sonic Mainnet",
    symbol: "S",
    rpc: process.env.SONIC_RPC_URL || "https://rpc.soniclabs.com",
    rpcs: [
      process.env.SONIC_RPC_URL,
      "https://rpc.soniclabs.com",
      "https://sonic.drpc.org"
    ].filter(Boolean),
    explorer: "https://sonicscan.org"
  },
  berachain: {
    id: 80084,
    name: "Berachain bArtio Testnet",
    symbol: "BERA",
    rpc: process.env.BERACHAIN_RPC_URL || "https://bartio.rpc.berachain.com",
    rpcs: [
      process.env.BERACHAIN_RPC_URL,
      "https://bartio.rpc.berachain.com",
      "https://berachain-bartio.drpc.org"
    ].filter(Boolean),
    explorer: "https://bartio.beratrail.io"
  },
  sepolia: {
    id: 11155111,
    name: "Ethereum Sepolia Testnet",
    symbol: "ETH",
    rpc: process.env.SEPOLIA_RPC_URL || "https://ethereum-sepolia-rpc.publicnode.com",
    rpcs: [
      process.env.SEPOLIA_RPC_URL,
      "https://ethereum-sepolia-rpc.publicnode.com",
      "https://rpc.sepolia.org"
    ].filter(Boolean),
    explorer: "https://sepolia.etherscan.io"
  },
  "base-sepolia": {
    id: 84532,
    name: "Base Sepolia Testnet",
    symbol: "ETH",
    rpc: process.env.BASE_SEPOLIA_RPC_URL || "https://sepolia.base.org",
    rpcs: [
      process.env.BASE_SEPOLIA_RPC_URL,
      "https://sepolia.base.org",
      "https://base-sepolia.blockpi.network/v1/rpc/public"
    ].filter(Boolean),
    explorer: "https://sepolia.basescan.org"
  }
};

// Common token addresses mapped by Chain ID
export const TOKEN_MAP = {
  // Ethereum Mainnet (1)
  1: {
    ETH: "0x0000000000000000000000000000000000000000",
    WETH: "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    USDC: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    USDT: "0xdAC17F958D2ee523a2206206994597C13D831ec7"
  },
  // Arbitrum One (42161)
  42161: {
    ETH: "0x0000000000000000000000000000000000000000",
    WETH: "0x82aF49447D8a07e3bd95BD0d56f352415231C111",
    USDC: "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
    "USDC.E": "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8",
    USDT: "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9"
  },
  // Base (8453)
  8453: {
    ETH: "0x0000000000000000000000000000000000000000",
    WETH: "0x4200000000000000000000000000000000000006",
    USDC: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    USDT: "0xf55BEC9cbd4732f1F4143f647652e924540d9d64"
  },
  // OP Mainnet (10)
  10: {
    ETH: "0x0000000000000000000000000000000000000000",
    WETH: "0x4200000000000000000000000000000000000006",
    USDC: "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85",
    USDT: "0x94b008aA00579c1307b0EF2c499aD98a8ce58e58"
  },
  // Polygon PoS (137)
  137: {
    MATIC: "0x0000000000000000000000000000000000000000",
    POL: "0x0000000000000000000000000000000000000000",
    USDC: "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",
    USDT: "0xc2132D05D31c914a87C6611C10748AEb04B58e8F"
  },
  // BNB Smart Chain (56)
  56: {
    BNB: "0x0000000000000000000000000000000000000000",
    WBNB: "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
    USDC: "0x8AC76a51cc950d9822D68b83fE1Ad97B32CD580d",
    USDT: "0x55d398326f99059fF775485246999027B3197955"
  }
};

// ABI standard
export const ERC20_ABI = [
  "function name() view returns (string)",
  "function symbol() view returns (string)",
  "function decimals() view returns (uint8)",
  "function balanceOf(address owner) view returns (uint256)",
  "function transfer(address to, uint256 value) returns (bool)",
  "function approve(address spender, uint256 value) returns (bool)",
  "function allowance(address owner, address spender) view returns (uint256)"
];

export const ERC721_ABI = [
  "function name() view returns (string)",
  "function symbol() view returns (string)",
  "function balanceOf(address owner) view returns (uint256)",
  "function ownerOf(uint256 tokenId) view returns (address)",
  "function safeTransferFrom(address from, address to, uint256 tokenId) external",
  "function mint(uint256 quantity) payable",
  "function claim(address receiver, uint256 quantity, address tokenId, uint256 pricePerToken, tuple(bytes32[] proof, uint256 quantityLimitPerWallet, uint256 pricePerToken, address currency) allowlistProof, bytes data) payable"
];

// Explorer API Base URLs
export function getExplorerApiUrl(chainId) {
  const mapping = {
    1: "https://api.etherscan.io/api",
    42161: "https://api.arbiscan.io/api",
    8453: "https://api.basescan.org/api",
    10: "https://api-optimistic.etherscan.io/api",
    137: "https://api.polygonscan.com/api",
    56: "https://api.bscscan.com/api",
    43114: "https://api.snowtrace.io/api",
    59144: "https://api.lineascan.build/api",
    534352: "https://api.scrollscan.com/api",
    146: "https://api.sonicscan.org/api",
    80084: "https://api.routescan.io/v2/network/testnet/evm/80084/etherscan/api",
    11155111: "https://api-sepolia.etherscan.io/api",
    84532: "https://api-sepolia.basescan.org/api"
  };
  return mapping[chainId] || "";
}

// Explorer API keys from process.env
export function getExplorerApiKey(chainId) {
  const mapping = {
    1: process.env.ETHERSCAN_API_KEY,
    42161: process.env.ARBISCAN_API_KEY,
    8453: process.env.BASESCAN_API_KEY,
    10: process.env.OPTIMISM_API_KEY,
    137: process.env.POLYGONSCAN_API_KEY,
    56: process.env.BSCSCAN_API_KEY,
    43114: process.env.SNOWTRACE_API_KEY,
    59144: process.env.LINEASCAN_API_KEY,
    534352: process.env.SCROLLSCAN_API_KEY,
    146: process.env.SONICSCAN_API_KEY,
    11155111: process.env.ETHERSCAN_API_KEY,
    84532: process.env.BASESCAN_API_KEY
  };
  return mapping[chainId] || "";
}

// Helper to normalize chain names
export function getChainConfig(chainInput) {
  if (!chainInput) return SUPPORTED_CHAINS.ethereum;
  const normalized = chainInput.toLowerCase().trim();
  
  // Direct match
  if (SUPPORTED_CHAINS[normalized]) {
    return SUPPORTED_CHAINS[normalized];
  }
  
  // Loose matching/aliases
  if (normalized === "eth" || normalized === "mainnet") return SUPPORTED_CHAINS.ethereum;
  if (normalized === "arb" || normalized === "arbitrumone") return SUPPORTED_CHAINS.arbitrum;
  if (normalized === "op" || normalized === "optimistic") return SUPPORTED_CHAINS.optimism;
  if (normalized === "matic") return SUPPORTED_CHAINS.polygon;
  if (normalized === "binance" || normalized === "bnb") return SUPPORTED_CHAINS.bsc;
  if (normalized === "avax") return SUPPORTED_CHAINS.avalanche;
  if (normalized === "sepolia") return SUPPORTED_CHAINS.sepolia;
  if (normalized === "base-sepolia" || normalized === "basesepolia") return SUPPORTED_CHAINS["base-sepolia"];
  
  // Try matching chain ID
  const chainId = parseInt(normalized);
  if (!isNaN(chainId)) {
    const matched = Object.values(SUPPORTED_CHAINS).find(c => c.id === chainId);
    if (matched) return matched;
    // Return fallback for custom chain ID if we can't find it
    return {
      id: chainId,
      name: `Chain ID ${chainId}`,
      symbol: "ETH",
      rpc: "https://rpc.ankr.com/multichain", // generic fallback
      explorer: ""
    };
  }

  throw new Error(`Chain "${chainInput}" is not supported. Supported chains include: eth, arbitrum, base, optimism, polygon, bsc, avalanche, sonic, sepolia, base-sepolia, etc.`);
}

// Anti-MEV Secure Private RPC Endpoints mapped by Chain ID
export const ANTI_MEV_RPCS = {
  1: "https://rpc.flashbots.net", // Ethereum Mainnet
  56: "https://bsc-private.bloxroute.com", // BNB Smart Chain (bloxroute)
  137: "https://polygon-private.bloxroute.com" // Polygon (bloxroute)
};

// Get Signer & Provider (supports options.rpc and options.antiMev)
export async function getWallet(chainInput, options = {}) {
  const chainConfig = getChainConfig(chainInput);
  
  let rpcUrls = [];
  if (options.rpc) {
    rpcUrls = [options.rpc];
  } else if (options.antiMev && ANTI_MEV_RPCS[chainConfig.id]) {
    logInfo(`MEV Protection active. Routing transactions via secure RPC: ${ANTI_MEV_RPCS[chainConfig.id]}`, options);
    rpcUrls = [ANTI_MEV_RPCS[chainConfig.id], ...(chainConfig.rpcs || [chainConfig.rpc])];
  } else {
    rpcUrls = [...(chainConfig.rpcs || [chainConfig.rpc])];
  }
  
  let provider;
  let successRpcUrl = null;
  
  const tryUrls = async (urls) => {
    for (const url of urls) {
      try {
        logInfo(`Trying RPC endpoint: ${url}...`, options);
        
        const possibleProvider = new ethers.JsonRpcProvider(url, chainConfig.id, {
          staticNetwork: true
        });
        
        const timeoutMs = options.rpcTimeout || 3500;
        const checkPromise = possibleProvider.getBlockNumber();
        const timeoutPromise = new Promise((_, reject) =>
          setTimeout(() => reject(new Error("RPC request timeout")), timeoutMs)
        );
        
        await Promise.race([checkPromise, timeoutPromise]);
        
        provider = possibleProvider;
        successRpcUrl = url;
        break;
      } catch (err) {
        logWarning(`RPC endpoint failed: ${url} (${err.message})`, options);
      }
    }
  };
  
  // Try local lists first
  await tryUrls(rpcUrls);
  
  // If failed and no explicit --rpc was passed, try fetching from chainid.network (Chainlist)
  if (!provider && !options.rpc) {
    logInfo(`Local RPCs failed. Fetching alternative RPC list from Chainlist (chainid.network)...`, options);
    try {
      const response = await axios.get("https://chainid.network/chains.json", { timeout: 6000 });
      if (response.data && Array.isArray(response.data)) {
        const chainData = response.data.find(c => c.chainId === chainConfig.id);
        if (chainData && Array.isArray(chainData.rpc)) {
          const dynamicUrls = chainData.rpc
            .filter(url => url && url.startsWith("http") && !url.includes("${"))
            .map(url => url.trim());
          
          if (dynamicUrls.length > 0) {
            logInfo(`Found ${dynamicUrls.length} alternative RPCs on Chainlist. Trying them...`, options);
            await tryUrls(dynamicUrls);
          }
        }
      }
    } catch (err) {
      logWarning(`Failed to fetch Chainlist database: ${err.message}`, options);
    }
  }
  
  if (!provider) {
    throw new Error(`All configured RPC endpoints for ${chainConfig.name} failed to respond or are blocked. Please check your internet connection or configure a working custom RPC in your .env file.`);
  }
  
  // Cache the working RPC
  chainConfig.rpc = successRpcUrl;
  
  const privateKey = process.env.PRIVATE_KEY;
  const mnemonic = process.env.MNEMONIC;
  
  let wallet;
  if (privateKey && privateKey !== "0x0000000000000000000000000000000000000000" && privateKey.trim() !== "") {
    wallet = new ethers.Wallet(privateKey, provider);
  } else if (mnemonic && mnemonic.trim() !== "") {
    wallet = ethers.Wallet.fromPhrase(mnemonic, provider);
  } else {
    throw new Error("Wallet configuration not found. Please set PRIVATE_KEY or MNEMONIC in your .env file.");
  }
  
  return { wallet, provider, chainConfig };
}

// Resolve token symbol or return hex address as-is (with dynamic Li.Fi API resolution fallback)
export async function resolveTokenAddress(tokenSymbolOrAddress, chainId, options = {}) {
  if (!tokenSymbolOrAddress) return null;
  const input = tokenSymbolOrAddress.trim();
  
  if (ethers.isAddress(input)) {
    return ethers.getAddress(input.toLowerCase());
  }
  
  const symbolUpper = input.toUpperCase();
  
  // Check native tokens
  const chainConfig = Object.values(SUPPORTED_CHAINS).find(c => c.id === chainId);
  const nativeSymbol = chainConfig ? chainConfig.symbol.toUpperCase() : "ETH";
  
  if (["ETH", "MATIC", "POL", "BNB", "AVAX", "NATIVE", "S", "BERA", nativeSymbol].includes(symbolUpper)) {
    return "0x0000000000000000000000000000000000000000";
  }

  // Check local mapping
  const chainTokens = TOKEN_MAP[chainId];
  if (chainTokens && chainTokens[symbolUpper]) {
    return ethers.getAddress(chainTokens[symbolUpper].toLowerCase());
  }

  // Fallback to Li.Fi API for dynamic resolution
  logInfo(`Resolving contract address for symbol "${input}" on chain ID ${chainId}...`, options);
  try {
    const response = await axios.get("https://li.quest/v1/token", {
      params: {
        chain: chainId,
        token: input
      }
    });
    if (response.data && response.data.address) {
      const resolvedAddress = ethers.getAddress(response.data.address.toLowerCase());
      logInfo(`Resolved "${input}" to ${resolvedAddress}`, options);
      return resolvedAddress;
    }
  } catch (error) {
    // Suppress heavy logs but print clean error
    logWarning(`Failed to resolve token symbol "${input}" via Li.Fi: ${error.message}. Attempting direct address lookup...`, options);
  }

  throw new Error(`Token symbol "${input}" could not be resolved on chain ID ${chainId}. Please provide the 0x contract address directly.`);
}

// Format units helper
export function formatUnits(value, decimals = 18) {
  return ethers.formatUnits(value, decimals);
}

// Parse units helper
export function parseUnits(value, decimals = 18) {
  return ethers.parseUnits(value.toString(), decimals);
}

// Fetch current token price in USD from DexScreener
export async function getCurrentPrice(tokenAddress, chainConfig, options = {}) {
  const isNative = tokenAddress === "0x0000000000000000000000000000000000000000";
  
  // If native, resolve to wrapped token if possible for DexScreener query, or look up WETH/WBNB
  let queryAddress = tokenAddress;
  if (isNative) {
    // Look up wrapped version in TOKEN_MAP
    if (chainConfig.id === 1) queryAddress = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"; // WETH
    else if (chainConfig.id === 8453) queryAddress = "0x4200000000000000000000000000000000000006"; // WETH Base
    else if (chainConfig.id === 42161) queryAddress = "0x82aF49447D8a07e3bd95BD0d56f352415231C111"; // WETH Arb
    else if (chainConfig.id === 137) queryAddress = "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"; // WMATIC
    else if (chainConfig.id === 56) queryAddress = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"; // WBNB
    else {
      // Return fallback native price approximation from Li.Fi or CoinGecko if available
      return await getNativePriceFallback(chainConfig.symbol, options);
    }
  }

  try {
    const url = `https://api.dexscreener.com/latest/dex/tokens/${queryAddress}`;
    const response = await axios.get(url, { timeout: 5000 });
    if (response.data && response.data.pairs && response.data.pairs.length > 0) {
      // Find pair with high liquidity
      const sortedPairs = response.data.pairs.sort((a, b) => (b.liquidity?.usd || 0) - (a.liquidity?.usd || 0));
      const bestPair = sortedPairs[0];
      return {
        priceUsd: parseFloat(bestPair.priceUsd || 0),
        symbol: bestPair.baseToken.symbol,
        name: bestPair.baseToken.name,
        liquidityUsd: bestPair.liquidity?.usd || 0,
        fdv: bestPair.fdv || 0,
        priceChange24h: bestPair.priceChange?.h24 || 0
      };
    }
  } catch (err) {
    logWarning(`Failed to fetch price from DexScreener: ${err.message}`, options);
  }
  
  // Fallback via Li.Fi
  try {
    const response = await axios.get("https://li.quest/v1/token", {
      params: {
        chain: chainConfig.id,
        token: queryAddress
      },
      timeout: 5000
    });
    if (response.data && response.data.priceUSD) {
      return {
        priceUsd: parseFloat(response.data.priceUSD),
        symbol: response.data.symbol,
        name: response.data.name,
        liquidityUsd: 0,
        fdv: 0,
        priceChange24h: 0
      };
    }
  } catch (err) {
    // Fail silently
  }

  return null;
}

// Fallback to get native asset price
async function getNativePriceFallback(symbol, options = {}) {
  try {
    // DexScreener search by query
    const url = `https://api.dexscreener.com/latest/dex/search?q=${symbol}`;
    const response = await axios.get(url, { timeout: 5000 });
    if (response.data && response.data.pairs) {
      const nativePair = response.data.pairs.find(p => p.baseToken.symbol.toUpperCase() === symbol.toUpperCase());
      if (nativePair) {
        return {
          priceUsd: parseFloat(nativePair.priceUsd || 0),
          symbol: symbol,
          name: symbol,
          priceChange24h: nativePair.priceChange?.h24 || 0
        };
      }
    }
  } catch (err) {}
  return { priceUsd: 0, symbol, name: symbol };
}
