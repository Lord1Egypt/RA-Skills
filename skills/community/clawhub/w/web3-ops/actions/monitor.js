import { ethers } from "ethers";
import {
  getWallet,
  getChainConfig,
  logInfo,
  logSuccess,
  logWarning,
  logError,
  printColor,
  resolveTokenAddress,
  TOKEN_MAP,
  getCurrentPrice
} from "./common.js";
import { swapOrBridge } from "./swapBridge.js";

// Sleep helper
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

export async function runPriceMonitor(options = {}) {
  const chainInput = options.chain;
  const tokenInput = options.token;
  const amountToSell = options.amount;
  const cutlossInput = options.cutloss;
  const takeprofitInput = options.takeprofit;
  const maxChecks = options.maxChecks ? parseInt(options.maxChecks) : 60; // default 60 checks (~20 mins at 20s interval)
  const intervalMs = options.interval ? parseInt(options.interval) * 1000 : 20000; // default 20 seconds
  const forceAlert = options.alert || false;

  try {
    const { chainConfig } = await getWallet(chainInput, options);
    
    if (!tokenInput) {
      throw new Error("Please specify the target --token to monitor.");
    }
    if (!amountToSell) {
      throw new Error("Please specify the swap --amount to sell if target is reached.");
    }
    if (!cutlossInput && !takeprofitInput) {
      throw new Error("Please configure at least one target trigger: --cutloss <value> or --takeprofit <value>.");
    }

    const tokenAddress = await resolveTokenAddress(tokenInput, chainConfig.id, options);
    
    if (tokenAddress === "0x0000000000000000000000000000000000000000") {
      throw new Error("Monitoring native token price for cutloss/takeprofit is currently not supported. Target ERC-20 token instead.");
    }

    // Resolve stablecoin target (USDC)
    let usdcAddress = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"; // Base USDC default
    const chainTokens = TOKEN_MAP[chainConfig.id];
    if (chainTokens && chainTokens.USDC) {
      usdcAddress = chainTokens.USDC;
    } else {
      usdcAddress = await resolveTokenAddress("USDC", chainConfig.id, options);
    }

    logInfo(`Initializing price monitor for ${tokenInput}...`, options);
    const initialPriceInfo = await getCurrentPrice(tokenAddress, chainConfig, options);
    
    if (!initialPriceInfo || !initialPriceInfo.priceUsd) {
      throw new Error(`Failed to fetch current price for ${tokenInput} to initialize targets.`);
    }

    const initialPrice = initialPriceInfo.priceUsd;
    const symbol = initialPriceInfo.symbol || tokenInput;
    
    // Parse targets (support percentage e.g., -10% or +20% and nominal numbers)
    let cutlossTarget = null;
    let takeprofitTarget = null;

    if (cutlossInput) {
      if (cutlossInput.toString().endsWith("%")) {
        const pct = parseFloat(cutlossInput.toString().replace("%", ""));
        // E.g., -10% -> 0.9 * initialPrice
        cutlossTarget = initialPrice * (1 + pct / 100);
      } else {
        cutlossTarget = parseFloat(cutlossInput);
      }
    }

    if (takeprofitInput) {
      if (takeprofitInput.toString().endsWith("%")) {
        const pct = parseFloat(takeprofitInput.toString().replace("%", ""));
        // E.g., +20% -> 1.2 * initialPrice
        takeprofitTarget = initialPrice * (1 + pct / 100);
      } else {
        takeprofitTarget = parseFloat(takeprofitInput);
      }
    }

    if (!options.json) {
      console.log(`\n==================================================`);
      console.log(printColor(`ACTIVE PRICE MONITOR STARTED: ${symbol}`, "bold"));
      console.log(`Token Address    : ${tokenAddress}`);
      console.log(`Target Exit      : ${usdcAddress} (USDC)`);
      console.log(`Initial Price    : $${initialPrice.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 6 })}`);
      if (cutlossTarget) console.log(`Cutloss Limit    : $${cutlossTarget.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 6 })} (${cutlossInput})`);
      if (takeprofitTarget) console.log(`Takeprofit Limit : $${takeprofitTarget.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 6 })} (${takeprofitInput})`);
      console.log(`Polling Interval : ${intervalMs / 1000} seconds (Max ${maxChecks} checks)`);
      console.log(`==================================================\n`);
    }

    let checkCount = 0;
    let triggerType = null;
    let exitPrice = 0;

    while (checkCount < maxChecks) {
      checkCount++;
      
      const priceInfo = await getCurrentPrice(tokenAddress, chainConfig, options);
      if (priceInfo && priceInfo.priceUsd) {
        const currentPrice = priceInfo.priceUsd;
        
        if (!options.json) {
          const timeStr = new Date().toLocaleTimeString();
          let statusText = printColor("HOLDING...", "yellow");
          console.log(`[${timeStr}] Check #${checkCount}/${maxChecks} | Price: $${currentPrice.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 6 })} | Status: ${statusText}`);
        }

        // Check Cutloss condition
        if (cutlossTarget !== null && currentPrice <= cutlossTarget) {
          triggerType = "CUTLOSS";
          exitPrice = currentPrice;
          break;
        }

        // Check Takeprofit condition
        if (takeprofitTarget !== null && currentPrice >= takeprofitTarget) {
          triggerType = "TAKEPROFIT";
          exitPrice = currentPrice;
          break;
        }
      } else {
        logWarning(`Failed to fetch current price at check #${checkCount}, retrying in next iteration...`, options);
      }

      await sleep(intervalMs);
    }

    if (triggerType) {
      logSuccess(`TARGET ${triggerType} TRIGGERED! Current Price: $${exitPrice.toLocaleString()}`, options);
      
      let alertMsg = `🚨 MONITOR ALERT: ${symbol} has triggered ${triggerType} exit at $${exitPrice}! Swapping ${amountToSell} to USDC.`;
      
      // Execute the swap
      const swapOpts = {
        ...options,
        fromToken: tokenAddress,
        toToken: usdcAddress,
        amount: amountToSell.toString(),
        mode: "auto",
        json: options.json // preserve format preference
      };
      
      logInfo(`Initiating automated trade swap via Li.Fi router...`, options);
      const swapResult = await swapOrBridge(swapOpts);
      
      console.log(JSON.stringify({
        success: true,
        monitorTriggered: true,
        trigger: triggerType,
        exitPriceUsd: exitPrice,
        amountSold: amountToSell,
        alertTriggered: forceAlert,
        alertMessage: alertMsg,
        swap: swapResult
      }, null, 2));

    } else {
      logWarning(`Monitoring timeout reached (${maxChecks} checks completed). No limits triggered.`, options);
      console.log(JSON.stringify({
        success: true,
        monitorTriggered: false,
        summary: "Timeout reached without triggering exit conditions.",
        checksCompleted: checkCount
      }, null, 2));
    }

  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.message
    }, null, 2));
  }
}
