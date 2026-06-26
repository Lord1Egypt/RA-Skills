import axios from "axios";
import { ethers } from "ethers";
import {
  getWallet,
  getChainConfig,
  ERC20_ABI,
  formatUnits,
  logInfo,
  logSuccess,
  logWarning,
  logError,
  printColor,
  getExplorerApiUrl,
  getExplorerApiKey,
  resolveTokenAddress,
  getCurrentPrice
} from "./common.js";

export async function trackWhales(options = {}) {
  const chainInput = options.chain;
  const tokenInput = options.token;
  const minUsdThreshold = options.minUsd ? parseFloat(options.minUsd) : 50000; // default $50,000
  const forceAlert = options.alert || false;

  try {
    const { chainConfig, provider } = await getWallet(chainInput, options);
    
    if (!tokenInput) {
      throw new Error("Please specify a target --token <symbolOrAddress> to track whale movements.");
    }

    const tokenAddress = await resolveTokenAddress(tokenInput, chainConfig.id, options);
    const isNative = tokenAddress === "0x0000000000000000000000000000000000000000";
    
    logInfo(`Fetching token metadata and current price...`, options);
    const priceInfo = await getCurrentPrice(tokenAddress, chainConfig, options);
    
    if (!priceInfo || !priceInfo.priceUsd) {
      throw new Error(`Could not retrieve token price for ${tokenInput}.`);
    }

    const currentPrice = priceInfo.priceUsd;
    const symbol = priceInfo.symbol || tokenInput;
    
    let decimals = 18;
    if (!isNative) {
      const contract = new ethers.Contract(tokenAddress, ERC20_ABI, provider);
      decimals = Number(await contract.decimals());
    }

    const apiUrl = getExplorerApiUrl(chainConfig.id);
    const apiKey = getExplorerApiKey(chainConfig.id);
    
    if (!apiUrl) {
      throw new Error(`Explorer API is not configured or supported for chain ${chainConfig.name}.`);
    }

    logInfo(`Scanning recent transactions for whale movements (Threshold: > $${minUsdThreshold.toLocaleString()})...`, options);
    
    let txs = [];
    if (isNative) {
      const response = await axios.get(apiUrl, {
        params: {
          module: "account",
          action: "txlist",
          address: "0x0000000000000000000000000000000000000000", // dummy to search general chain txs is not supported directly in txlist, we must query target token transactions
          // Instead of querying general txlist (which requires block search), we fetch recent txs for the wrapped token or from popular pools to see swaps
          // For native token, we can scan txlist of the wrapped native version (WETH/WBNB) to capture whale wraps/swaps:
          contractaddress: chainConfig.id === 1 ? "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2" : undefined, 
          sort: "desc",
          offset: 100,
          apikey: apiKey || undefined
        },
        timeout: 8000
      });
      if (response.data && response.data.status === "1" && Array.isArray(response.data.result)) {
        txs = response.data.result;
      }
    } else {
      const response = await axios.get(apiUrl, {
        params: {
          module: "account",
          action: "tokentx",
          contractaddress: tokenAddress,
          sort: "desc",
          offset: 150, // scan last 150 transfer events
          apikey: apiKey || undefined
        },
        timeout: 8000
      });
      if (response.data && response.data.status === "1" && Array.isArray(response.data.result)) {
        txs = response.data.result;
      }
    }

    const whaleTxs = [];
    
    for (const tx of txs) {
      const value = parseFloat(formatUnits(tx.value, decimals));
      const valueUsd = value * currentPrice;
      
      if (valueUsd >= minUsdThreshold) {
        whaleTxs.push({
          hash: tx.hash,
          from: tx.from,
          to: tx.to,
          amount: value,
          valueUsd: valueUsd,
          timeStamp: parseInt(tx.timeStamp || 0),
          ageSeconds: Math.floor(Date.now() / 1000) - parseInt(tx.timeStamp || 0)
        });
      }
    }

    // Sort by newest transaction
    const sortedWhales = whaleTxs.sort((a, b) => b.timeStamp - a.timeStamp);
    
    let isAlertTriggered = false;
    let alertMsg = "";
    if (forceAlert && sortedWhales.length > 0) {
      const newestWhale = sortedWhales[0];
      // Only alert if transaction is fresh (e.g. less than 1 hour old / 3600s)
      if (newestWhale.ageSeconds <= 3600) {
        isAlertTriggered = true;
        alertMsg = `🐋 WHALE ALERT: Transfer of ${newestWhale.amount.toLocaleString()} ${symbol} ($${newestWhale.valueUsd.toLocaleString(undefined, { maximumFractionDigits: 2 })}) detected! Tx: ${newestWhale.hash}`;
      }
    }

    logSuccess(`Whale tracking scan complete`, options);
    
    if (!options.json) {
      console.log(`\n==================================================`);
      console.log(printColor(`WHALE TRANSFERS TRACKER: ${symbol}`, "bold"));
      console.log(`Token CA      : ${tokenAddress}`);
      console.log(`Min Threshold : $${minUsdThreshold.toLocaleString()}`);
      console.log(`Network       : ${chainConfig.name}`);
      console.log(`--------------------------------------------------`);
      
      if (sortedWhales.length === 0) {
        console.log(`No recent whale transfers detected above $${minUsdThreshold.toLocaleString()} in the last 150 events.`);
      } else {
        console.log(printColor(`Found ${sortedWhales.length} Recent Large Transactions:`, "bold"));
        for (const tx of sortedWhales) {
          const timeStr = tx.ageSeconds < 60 ? "just now" : `${Math.floor(tx.ageSeconds / 60)} minutes ago`;
          console.log(`\n • Value: ${printColor(`$${tx.valueUsd.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`, "green")} (${tx.amount.toLocaleString()} ${symbol})`);
          console.log(`   From : ${tx.from}`);
          console.log(`   To   : ${tx.to}`);
          console.log(`   Hash : ${tx.hash}`);
          console.log(`   Time : ${timeStr}`);
        }
      }
      
      if (isAlertTriggered) {
        console.log(`--------------------------------------------------`);
        console.log(printColor(alertMsg, "yellow"));
      }
      console.log(`==================================================\n`);
    }

    console.log(JSON.stringify({
      success: true,
      chain: chainConfig.name,
      token: symbol,
      tokenAddress: tokenAddress,
      thresholdUsd: minUsdThreshold,
      whaleTransactionsCount: sortedWhales.length,
      whaleTransactions: sortedWhales,
      alertTriggered: isAlertTriggered,
      alertMessage: alertMsg
    }, null, 2));

  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.message
    }, null, 2));
  }
}
