import { ethers } from "ethers";
import axios from "axios";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

import {
  getWallet,
  getChainConfig,
  ERC20_ABI,
  formatUnits,
  logInfo,
  logSuccess,
  logError,
  logWarning,
  printColor,
  getExplorerApiUrl,
  getExplorerApiKey,
  TOKEN_MAP,
  resolveTokenAddress,
  getCurrentPrice
} from "./common.js";

// Get configured wallet address
export async function getAddress(options = {}) {
  try {
    const chainInput = options.chain || "ethereum";
    const { wallet } = await getWallet(chainInput, options);
    console.log(JSON.stringify({
      success: true,
      address: wallet.address
    }, null, 2));
  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.message
    }, null, 2));
  }
}

// Check native or ERC-20 token balance
export async function getBalance(options = {}) {
  const chainInput = options.chain;
  const tokenInput = options.token;
  
  try {
    const { wallet, provider, chainConfig } = await getWallet(chainInput, options);
    
    if (!tokenInput) {
      // Check Native Balance
      const balance = await provider.getBalance(wallet.address);
      const balanceFormatted = formatUnits(balance, 18);
      const priceInfo = await getCurrentPrice("0x0000000000000000000000000000000000000000", chainConfig, options);
      const priceUsd = priceInfo ? priceInfo.priceUsd : null;
      const valueUsd = priceUsd ? parseFloat(balanceFormatted) * priceUsd : null;

      logSuccess(`Native balance checked successfully`, options);
      
      console.log(JSON.stringify({
        success: true,
        chain: chainConfig.name,
        address: wallet.address,
        balance: balanceFormatted,
        symbol: chainConfig.symbol,
        tokenAddress: "0x0000000000000000000000000000000000000000",
        priceUsd: priceUsd,
        valueUsd: valueUsd
      }, null, 2));
    } else {
      // Resolve Token Address dynamically
      const tokenAddress = await resolveTokenAddress(tokenInput, chainConfig.id, options);
      
      if (tokenAddress === "0x0000000000000000000000000000000000000000") {
        // Native balance resolved
        const balance = await provider.getBalance(wallet.address);
        const balanceFormatted = formatUnits(balance, 18);
        const priceInfo = await getCurrentPrice("0x0000000000000000000000000000000000000000", chainConfig, options);
        const priceUsd = priceInfo ? priceInfo.priceUsd : null;
        const valueUsd = priceUsd ? parseFloat(balanceFormatted) * priceUsd : null;

        console.log(JSON.stringify({
          success: true,
          chain: chainConfig.name,
          address: wallet.address,
          balance: balanceFormatted,
          symbol: chainConfig.symbol,
          tokenAddress: "0x0000000000000000000000000000000000000000",
          priceUsd: priceUsd,
          valueUsd: valueUsd
        }, null, 2));
        return;
      }
      
      const tokenContract = new ethers.Contract(tokenAddress, ERC20_ABI, provider);
      const [balance, decimals, symbol, name] = await Promise.all([
        tokenContract.balanceOf(wallet.address),
        tokenContract.decimals(),
        tokenContract.symbol(),
        tokenContract.name()
      ]);
      const balanceFormatted = formatUnits(balance, decimals);
      const priceInfo = await getCurrentPrice(tokenAddress, chainConfig, options);
      const priceUsd = priceInfo ? priceInfo.priceUsd : null;
      const valueUsd = priceUsd ? parseFloat(balanceFormatted) * priceUsd : null;

      logSuccess(`Token balance checked successfully`, options);
      console.log(JSON.stringify({
        success: true,
        chain: chainConfig.name,
        address: wallet.address,
        tokenAddress: tokenAddress,
        tokenName: name,
        balance: balanceFormatted,
        symbol: symbol,
        priceUsd: priceUsd,
        valueUsd: valueUsd
      }, null, 2));
    }
  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.message
    }, null, 2));
  }
}

// Reusable helper to scan portfolio for a single chain
async function scanChainPortfolio(chainInput, options = {}) {
  const { wallet, provider, chainConfig } = await getWallet(chainInput, options);
  
  // 1. Fetch native token balance
  const nativeBalancePromise = provider.getBalance(wallet.address).then(bal => ({
    symbol: chainConfig.symbol,
    decimals: 18,
    balance: bal,
    tokenAddress: "0x0000000000000000000000000000000000000000",
    isNative: true
  }));
  
  // 2. Discover token addresses using Block Explorer API
  const tokenAddresses = new Set();
  const apiUrl = getExplorerApiUrl(chainConfig.id);
  
  if (apiUrl) {
    const apiKey = getExplorerApiKey(chainConfig.id);
    try {
      const response = await axios.get(apiUrl, {
        params: {
          module: "account",
          action: "tokentx",
          address: wallet.address,
          sort: "desc",
          offset: 100, // scan last 100 events
          apikey: apiKey || undefined
        },
        timeout: 8000
      });
      
      if (response.data && Array.isArray(response.data.result)) {
        for (const tx of response.data.result) {
          if (tx.contractAddress && ethers.isAddress(tx.contractAddress)) {
            tokenAddresses.add(ethers.getAddress(tx.contractAddress.toLowerCase()));
          }
        }
      }
    } catch (err) {
      // Fail silently for explorer API issues during multi-scan
    }
  }
  
  // Merge popular token list for this chain from default map
  const chainTokens = TOKEN_MAP[chainConfig.id] || {};
  for (const key of Object.keys(chainTokens)) {
    const addr = chainTokens[key];
    if (addr && addr !== "0x0000000000000000000000000000000000000000") {
      tokenAddresses.add(ethers.getAddress(addr.toLowerCase()));
    }
  }
  
  // 3. Query all balances in parallel
  const addressesArray = Array.from(tokenAddresses);
  
  const balancePromises = addressesArray.map(async (address) => {
    try {
      const contract = new ethers.Contract(address, ERC20_ABI, provider);
      const [bal, decimals, symbol] = await Promise.all([
        contract.balanceOf(wallet.address),
        contract.decimals(),
        contract.symbol()
      ]);
      return {
        symbol: symbol,
        decimals: Number(decimals),
        balance: bal,
        tokenAddress: address,
        isNative: false
      };
    } catch (err) {
      // Silently skip failed queries
      return null;
    }
  });
  
  const allResults = await Promise.all([nativeBalancePromise, ...balancePromises]);
  
  const activeTokens = await Promise.all(
    allResults
      .filter(item => item !== null && item.balance > 0n)
      .map(async (item) => {
        const balanceFormatted = formatUnits(item.balance, item.decimals);
        let priceUsd = null;
        let valueUsd = null;
        try {
          const priceInfo = await getCurrentPrice(item.tokenAddress, chainConfig, options);
          if (priceInfo) {
            priceUsd = priceInfo.priceUsd;
            valueUsd = parseFloat(balanceFormatted) * priceUsd;
          }
        } catch (err) {
          // Ignore price fetching issues
        }
        return {
          symbol: item.symbol,
          balance: balanceFormatted,
          tokenAddress: item.tokenAddress,
          isNative: item.isNative,
          priceUsd: priceUsd,
          valueUsd: valueUsd
        };
      })
  );

  return {
    chainName: chainConfig.name,
    address: wallet.address,
    portfolio: activeTokens
  };
}

// Scan portfolio for active balances (single or all chains)
export async function getPortfolio(options = {}) {
  const chainInput = options.chain || "all";
  const normalizedChain = chainInput.toLowerCase().trim();
  
  try {
    if (normalizedChain === "all" || normalizedChain === "multi") {
      const chainsToScan = ["ethereum", "arbitrum", "base", "optimism", "polygon", "bsc", "avalanche", "linea", "scroll", "zksync"];
      logInfo(`Scanning portfolio across all chains (${chainsToScan.join(", ")}) for configured wallet...`, options);
      
      const scanPromises = chainsToScan.map(async (chainKey) => {
        try {
          const res = await scanChainPortfolio(chainKey, { ...options, rpcTimeout: 3500 });
          return {
            chain: chainKey,
            chainName: res.chainName,
            address: res.address,
            portfolio: res.portfolio
          };
        } catch (err) {
          return {
            chain: chainKey,
            error: err.message
          };
        }
      });
      
      const results = await Promise.all(scanPromises);
      
      // Output results
      if (!options.json) {
        console.log(`\n==================================================`);
        console.log(printColor("MULTICHAIN PORTFOLIO SUMMARY", "bold"));
        const firstSuccess = results.find(r => r.portfolio && r.address);
        const walletAddress = firstSuccess ? firstSuccess.address : "0x...";
        console.log(`Address: ${walletAddress}`);
        console.log(`==================================================`);
        
        for (const res of results) {
          const name = res.chainName || res.chain.toUpperCase();
          console.log(`\n[ ${printColor(name, "cyan")} ]`);
          if (res.error) {
            console.log(printColor(`  Error scanning chain: ${res.error}`, "red"));
          } else if (!res.portfolio || res.portfolio.length === 0) {
            console.log(`  No active token balances found.`);
          } else {
            for (const token of res.portfolio) {
              const symStr = printColor(token.symbol.padEnd(8), "cyan");
              const balFormatted = Number(token.balance).toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 6 }).padStart(12);
              const usdValStr = token.valueUsd !== null ? ` ($${token.valueUsd.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })})` : " (Price N/A)";
              const balStr = printColor(balFormatted + usdValStr, "green");
              const caStr = token.isNative ? "" : printColor(` (CA: ${token.tokenAddress})`, "gray");
              console.log(`  ${symStr}: ${balStr}${caStr}`);
            }
          }
        }
        console.log(`\n==================================================\n`);
      }
      
      console.log(JSON.stringify({
        success: true,
        portfolio: results.reduce((acc, curr) => {
          if (!curr.error) {
            acc[curr.chainName] = curr.portfolio;
          } else {
            acc[curr.chain] = { error: curr.error };
          }
          return acc;
        }, {})
      }, null, 2));
      
    } else {
      // Single chain scan
      const res = await scanChainPortfolio(chainInput, options);
      
      if (!options.json) {
        console.log(`\n==================================================`);
        console.log(printColor(`PORTFOLIO SUMMARY: ${res.chainName}`, "bold"));
        console.log(`Address: ${res.address}`);
        console.log(`==================================================`);
        if (res.portfolio.length === 0) {
          console.log(`No active token balances found (all balances are 0).`);
        } else {
          for (const token of res.portfolio) {
            const symStr = printColor(token.symbol.padEnd(8), "cyan");
            const balFormatted = Number(token.balance).toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 6 }).padStart(12);
            const usdValStr = token.valueUsd !== null ? ` ($${token.valueUsd.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })})` : " (Price N/A)";
            const balStr = printColor(balFormatted + usdValStr, "green");
            const caStr = token.isNative ? "" : printColor(` (CA: ${token.tokenAddress})`, "gray");
            console.log(`${symStr}: ${balStr}${caStr}`);
          }
        }
        console.log(`==================================================\n`);
      }
      
      console.log(JSON.stringify({
        success: true,
        chain: res.chainName,
        address: res.address,
        portfolio: res.portfolio
      }, null, 2));
    }
  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.message
    }, null, 2));
  }
}

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Generate new random wallet and save to .env
export async function createNewWallet(options = {}) {
  const envPath = path.join(__dirname, "../.env");
  const force = !!options.force;

  try {
    let envContent = "";
    let hasPrivateKey = false;
    let hasMnemonic = false;

    if (fs.existsSync(envPath)) {
      envContent = fs.readFileSync(envPath, "utf8");
      
      // Check for non-empty PRIVATE_KEY
      const pkMatch = envContent.match(/^PRIVATE_KEY\s*=\s*["']?([^"'\r\n]+)["']?/m);
      if (pkMatch && pkMatch[1] && pkMatch[1].trim() !== "" && pkMatch[1].trim() !== "0x0000000000000000000000000000000000000000") {
        hasPrivateKey = true;
      }
      
      // Check for non-empty MNEMONIC
      const mnemonicMatch = envContent.match(/^MNEMONIC\s*=\s*["']?([^"'\r\n]+)["']?/m);
      if (mnemonicMatch && mnemonicMatch[1] && mnemonicMatch[1].trim() !== "") {
        hasMnemonic = true;
      }
    }

    if ((hasPrivateKey || hasMnemonic) && !force) {
      throw new Error("A wallet is already configured in `.env`. To prevent accidental loss of funds or keys, wallet generation is blocked. Use `--force` if you are absolutely sure you want to overwrite it.");
    }

    // Generate random wallet
    const randomWallet = ethers.Wallet.createRandom();
    const address = randomWallet.address;
    const privateKey = randomWallet.privateKey;
    const mnemonicPhrase = randomWallet.mnemonic.phrase;

    const pkLine = `PRIVATE_KEY="${privateKey}"`;
    const mnemonicLine = `MNEMONIC="${mnemonicPhrase}"`;

    let newEnvContent = envContent;

    const setEnvVar = (content, key, newLine) => {
      const regex = new RegExp(`^${key}\\s*=.*$`, "m");
      if (regex.test(content)) {
        return content.replace(regex, newLine);
      } else {
        return content.trim() === "" ? newLine : `${content.trim()}\n${newLine}`;
      }
    };

    newEnvContent = setEnvVar(newEnvContent, "PRIVATE_KEY", pkLine);
    newEnvContent = setEnvVar(newEnvContent, "MNEMONIC", mnemonicLine);

    // Write to .env
    fs.writeFileSync(envPath, newEnvContent, { mode: 0o600 });

    if (!options.json) {
      console.log(`\n==================================================`);
      console.log(printColor("🆕 NEW EVM WALLET GENERATED & CONFIGURED", "green"));
      console.log(`==================================================`);
      console.log(`Address     : ${address}`);
      console.log(`Private Key : ${privateKey}`);
      console.log(`Mnemonic    : ${mnemonicPhrase}`);
      console.log(`==================================================`);
      console.log(printColor("🔒 SECURITY WARNINGS:", "yellow"));
      console.log(`1. Your private key and mnemonic have been saved directly to \`.env\`.`);
      console.log(`2. Backup these credentials immediately. They are the ONLY way to recover your assets.`);
      console.log(`3. Never share your private key/mnemonic with anyone, including AI prompts.`);
      console.log(`4. CLEAR YOUR TERMINAL HISTORY NOW to wipe these keys from scrollback history.`);
      console.log(`==================================================\n`);
    }

    console.log(JSON.stringify({
      success: true,
      address: address,
      privateKey: privateKey,
      mnemonic: mnemonicPhrase,
      savedToEnv: true
    }, null, 2));

  } catch (error) {
    if (!options.json) {
      logError(error.message, options);
    }
    console.error(JSON.stringify({
      success: false,
      error: error.message
    }, null, 2));
    process.exit(1);
  }
}

