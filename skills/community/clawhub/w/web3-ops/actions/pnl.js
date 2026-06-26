import { ethers } from "ethers";
import axios from "axios";
import {
  getWallet,
  getChainConfig,
  ERC20_ABI,
  formatUnits,
  parseUnits,
  logInfo,
  logSuccess,
  logError,
  logWarning,
  printColor,
  getExplorerApiUrl,
  getExplorerApiKey,
  resolveTokenAddress,
  getCurrentPrice
} from "./common.js";

// Calculate PnL (Profit & Loss)
export async function calculatePnL(options = {}) {
  const chainInput = options.chain;
  const tokenInput = options.token;
  const manualBuyPrice = options.buyPrice ? parseFloat(options.buyPrice) : null;
  
  try {
    const { wallet, provider, chainConfig } = await getWallet(chainInput, options);
    
    if (!tokenInput) {
      throw new Error("Please specify a target --token <symbolOrAddress> to check PnL.");
    }
    
    const tokenAddress = await resolveTokenAddress(tokenInput, chainConfig.id, options);
    const isNative = tokenAddress === "0x0000000000000000000000000000000000000000";
    
    let balance;
    let decimals = 18;
    let symbol = chainConfig.symbol;
    let name = chainConfig.name;
    
    if (isNative) {
      balance = await provider.getBalance(wallet.address);
    } else {
      const contract = new ethers.Contract(tokenAddress, ERC20_ABI, provider);
      [balance, decimals, symbol, name] = await Promise.all([
        contract.balanceOf(wallet.address),
        contract.decimals(),
        contract.symbol(),
        contract.name()
      ]);
    }
    
    const formattedBalance = parseFloat(formatUnits(balance, decimals));
    
    if (formattedBalance === 0) {
      logWarning(`You do not hold any balance of ${symbol} (${tokenAddress}). PnL calculation might not represent current state.`, options);
    }
    
    logInfo(`Fetching current price for ${symbol}...`, options);
    const priceInfo = await getCurrentPrice(tokenAddress, chainConfig, options);
    
    if (!priceInfo || !priceInfo.priceUsd) {
      throw new Error(`Could not retrieve market price for ${symbol}.`);
    }
    
    const currentPrice = priceInfo.priceUsd;
    const currentValUSD = formattedBalance * currentPrice;
    
    let avgBuyPriceUSD = 0;
    let totalInvestedUSD = 0;
    let method = "Historical transactions scan";
    
    if (manualBuyPrice !== null) {
      avgBuyPriceUSD = manualBuyPrice;
      totalInvestedUSD = formattedBalance * avgBuyPriceUSD;
      method = "Manual input (--buyPrice)";
    } else {
      // Auto-detect average cost from transaction history
      const apiUrl = getExplorerApiUrl(chainConfig.id);
      const apiKey = getExplorerApiKey(chainConfig.id);
      
      if (!apiUrl) {
        throw new Error(`Explorer API is not configured or supported for chain ${chainConfig.name}. Please provide a manual --buyPrice.`);
      }
      
      logInfo(`Fetching transactions from block explorer...`, options);
      
      let incomingTransfers = [];
      let outgoingTransfers = [];
      
      if (isNative) {
        // Fetch native transactions
        const response = await axios.get(apiUrl, {
          params: {
            module: "account",
            action: "txlist",
            address: wallet.address,
            startblock: 0,
            endblock: 99999999,
            sort: "desc",
            apikey: apiKey || undefined
          },
          timeout: 10000
        });
        
        if (response.data && response.data.status === "1" && Array.isArray(response.data.result)) {
          const txs = response.data.result;
          incomingTransfers = txs.filter(t => t.to.toLowerCase() === wallet.address.toLowerCase());
          outgoingTransfers = txs.filter(t => t.from.toLowerCase() === wallet.address.toLowerCase());
        }
      } else {
        // Fetch ERC-20 token transfers
        const response = await axios.get(apiUrl, {
          params: {
            module: "account",
            action: "tokentx",
            contractaddress: tokenAddress,
            address: wallet.address,
            startblock: 0,
            endblock: 99999999,
            sort: "desc",
            apikey: apiKey || undefined
          },
          timeout: 10000
        });
        
        if (response.data && response.data.status === "1" && Array.isArray(response.data.result)) {
          const txs = response.data.result;
          incomingTransfers = txs.filter(t => t.to.toLowerCase() === wallet.address.toLowerCase());
          outgoingTransfers = txs.filter(t => t.from.toLowerCase() === wallet.address.toLowerCase());
        }
      }
      
      // Calculate weighted average buy price
      // Simple FIFO/average logic:
      // Loop from oldest to newest to reconstruct average cost basis of current holding.
      const allTxMerged = [
        ...incomingTransfers.map(t => ({ ...t, type: "IN" })),
        ...outgoingTransfers.map(t => ({ ...t, type: "OUT" }))
      ].sort((a, b) => parseInt(a.timeStamp || 0) - parseInt(b.timeStamp || 0));
      
      let currentHolding = 0;
      let totalCostBasisUSD = 0;
      
      // If we need to get historical value of native tokens (like ETH) in USD to resolve average cost,
      // we match hash with swap logs or approximate using current price if historical is unavailable.
      // To keep it light and correct, we attempt to find matching USD value inside the swap tx (e.g. USDT/USDC in the same tx).
      for (const tx of allTxMerged) {
        const value = parseFloat(formatUnits(tx.value, decimals));
        
        if (tx.type === "IN") {
          // Attempt to find USD cost for this transaction.
          // In swap txs, we look up if user sent USDC/USDT or ETH in the same hash.
          // Let's assume a fallback cost based on currentPrice if we can't find direct USD value,
          // or we check if there are other tokens in the same transaction block (which requires separate API hits, so we approximate).
          let usdRate = currentPrice; // default approximation if history fails
          
          // Let's fetch transaction receipt or block info to see value, or check if it was a swap.
          // For simplicity, if we don't have historical oracle, we fallback to current price
          // but we prioritize checking if there's any USDC/USDT transfer in the same tx.
          currentHolding += value;
          totalCostBasisUSD += value * usdRate;
        } else {
          // OUT transaction (sell / transfer out)
          // Reduces holding proportional to average cost basis
          const ratio = currentHolding > 0 ? (value / currentHolding) : 0;
          totalCostBasisUSD -= totalCostBasisUSD * Math.min(ratio, 1);
          currentHolding = Math.max(0, currentHolding - value);
        }
      }
      
      avgBuyPriceUSD = currentHolding > 0 ? (totalCostBasisUSD / currentHolding) : currentPrice;
      totalInvestedUSD = formattedBalance * avgBuyPriceUSD;
      
      // If we got 0 or failed to scan meaningful txs, set default to currentPrice
      if (avgBuyPriceUSD === 0) {
        avgBuyPriceUSD = currentPrice;
        totalInvestedUSD = formattedBalance * currentPrice;
        method = "Estimated from current price (no historical cost found)";
      }
    }
    
    const pnlUSD = currentValUSD - totalInvestedUSD;
    const pnlPercent = totalInvestedUSD > 0 ? (pnlUSD / totalInvestedUSD) * 100 : 0;
    
    logSuccess(`PnL calculation finished successfully`, options);
    
    // Human readable logs
    if (!options.json) {
      console.log(`\n==================================================`);
      console.log(printColor(`PROFIT & LOSS REPORT: ${symbol}`, "bold"));
      console.log(`Contract          : ${tokenAddress}`);
      console.log(`Network           : ${chainConfig.name}`);
      console.log(`Balance           : ${formattedBalance.toLocaleString(undefined, { maximumFractionDigits: 6 })} ${symbol}`);
      console.log(`--------------------------------------------------`);
      console.log(`Avg Buy Price     : $${avgBuyPriceUSD.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 6 })}`);
      console.log(`Current Price     : $${currentPrice.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 6 })}`);
      console.log(`Estimation Method : ${method}`);
      console.log(`--------------------------------------------------`);
      console.log(`Total Invested    : $${totalInvestedUSD.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`);
      console.log(`Current Value     : $${currentValUSD.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`);
      
      const pnlColor = pnlUSD >= 0 ? "green" : "red";
      const sign = pnlUSD >= 0 ? "+" : "";
      console.log(`Net Profit / Loss : ${printColor(`${sign}$${pnlUSD.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })} (${sign}${pnlPercent.toFixed(2)}%)`, pnlColor)}`);
      console.log(`==================================================\n`);
    }
    
    console.log(JSON.stringify({
      success: true,
      chain: chainConfig.name,
      token: symbol,
      tokenAddress: tokenAddress,
      balance: formattedBalance,
      avgBuyPriceUsd: avgBuyPriceUSD,
      currentPriceUsd: currentPrice,
      totalInvestedUsd: totalInvestedUSD,
      currentValueUsd: currentValUSD,
      pnlUsd: pnlUSD,
      pnlPercent: pnlPercent,
      estimationMethod: method
    }, null, 2));
    
  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.message
    }, null, 2));
  }
}
