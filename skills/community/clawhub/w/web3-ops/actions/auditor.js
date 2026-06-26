import axios from "axios";
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
  SUPPORTED_CHAINS
} from "./common.js";

// Check security of a token contract address using GoPlus Security API
export async function analyzeTokenSecurity(options = {}) {
  const chainInput = options.chain;
  const tokenInput = options.token;

  try {
    const { chainConfig } = await getWallet(chainInput, options);
    
    if (!tokenInput) {
      throw new Error("Please specify a target --token <symbolOrAddress> to analyze.");
    }

    let tokenAddress = await resolveTokenAddress(tokenInput, chainConfig.id, options);
    
    if (tokenAddress === "0x0000000000000000000000000000000000000000") {
      // Native token is safe by default
      console.log(JSON.stringify({
        success: true,
        chain: chainConfig.name,
        tokenAddress: tokenAddress,
        token: chainConfig.symbol,
        securityScore: 100,
        isHoneypot: false,
        buyTaxPercent: 0,
        sellTaxPercent: 0,
        risks: [],
        summary: "Native token of the network is secure by architecture."
      }, null, 2));
      return;
    }

    // Check if tokenAddress is actually a liquidity pair address on DexScreener
    const chainKey = Object.keys(SUPPORTED_CHAINS).find(
      key => SUPPORTED_CHAINS[key].id === chainConfig.id
    );
    
    let isPairAddress = false;
    let originalQueryAddress = tokenAddress;
    let pairDetails = null;

    if (chainKey) {
      try {
        const dexPairUrl = `https://api.dexscreener.com/latest/dex/pairs/${chainKey}/${tokenAddress}`;
        const dexResponse = await axios.get(dexPairUrl, { timeout: 5000 });
        if (
          dexResponse.data &&
          (dexResponse.data.pair || (dexResponse.data.pairs && dexResponse.data.pairs.length > 0))
        ) {
          const pair = dexResponse.data.pair || dexResponse.data.pairs[0];
          if (pair.pairAddress.toLowerCase() === tokenAddress.toLowerCase()) {
            isPairAddress = true;
            pairDetails = {
              baseSymbol: pair.baseToken.symbol,
              quoteSymbol: pair.quoteToken.symbol,
              dexId: pair.dexId
            };
            
            logWarning(
              `[Warning] Alamat ${tokenAddress} adalah Liquidity Pool Pair (${pair.baseToken.symbol}/${pair.quoteToken.symbol} di ${pair.dexId}).`,
              options
            );
            logInfo(
              `Hinata secara otomatis mengalihkan audit ke token utama: ${pair.baseToken.name} (${pair.baseToken.symbol}) - ${pair.baseToken.address}`,
              options
            );
            
            // Redirect target audit address to the actual base token address
            tokenAddress = ethers.getAddress(pair.baseToken.address.toLowerCase());
          }
        }
      } catch (err) {
        // Suppress errors to not break execution if DexScreener is down
      }
    }

    logInfo(`Contacting GoPlus Security API for token audit (${tokenAddress})...`, options);
    
    const url = `https://api.gopluslabs.io/api/v1/token_security/${chainConfig.id}?contract_addresses=${tokenAddress}`;
    const response = await axios.get(url, { timeout: 8000 });
    
    if (!response.data || response.data.code !== 1 || !response.data.result || !response.data.result[tokenAddress.toLowerCase()]) {
      throw new Error("GoPlus Security API failed to return data for this token.");
    }
    
    const auditData = response.data.result[tokenAddress.toLowerCase()];
    
    // Parse individual risk metrics
    const isHoneypot = auditData.is_honeypot === "1";
    const buyTax = parseFloat(auditData.buy_tax || 0) * 100;
    const sellTax = parseFloat(auditData.sell_tax || 0) * 100;
    const ownerAddress = auditData.owner_address;
    const isMintable = auditData.is_mintable === "1";
    const isProxy = auditData.is_proxy === "1";
    const ownerChangeBalance = auditData.owner_change_balance === "1";
    const slippageModifiable = auditData.slippage_modifiable === "1";
    const transferPausable = auditData.transfer_pausable === "1";
    const cannotSellAll = auditData.cannot_sell_all === "1";
    
    const isOwnerRenounced = !ownerAddress || 
      ownerAddress === "0x0000000000000000000000000000000000000000" ||
      ownerAddress.toLowerCase() === "0x0000000000000000000000000000000000000001" ||
      ownerAddress.toLowerCase() === "0x000000000000000000000000000000000000dead";
      
    // Calculate custom security score
    let score = 100;
    const risks = [];
    
    if (isHoneypot) {
      score -= 100;
      risks.push({ severity: "CRITICAL", type: "HONEYPOT", desc: "Token cannot be sold. This is a scam honeypot contract." });
    }
    if (ownerChangeBalance) {
      score -= 50;
      risks.push({ severity: "CRITICAL", type: "OWNER_MODIFY_BALANCE", desc: "Contract owner has the ability to directly change or drain user balances." });
    }
    if (buyTax > 15 || sellTax > 15) {
      score -= 25;
      risks.push({ severity: "HIGH", type: "HIGH_TAX", desc: `Extremely high trading tax (Buy: ${buyTax}%, Sell: ${sellTax}%).` });
    }
    if (cannotSellAll) {
      score -= 25;
      risks.push({ severity: "HIGH", type: "CANNOT_SELL_ALL", desc: "Restrictions apply to selling the maximum holding balance." });
    }
    if (transferPausable) {
      score -= 15;
      risks.push({ severity: "MEDIUM", type: "TRANSFER_PAUSABLE", desc: "Contract owner can pause/freeze all trading at any time." });
    }
    if (slippageModifiable) {
      score -= 15;
      risks.push({ severity: "MEDIUM", type: "SLIPPAGE_MODIFIABLE", desc: "Contract owner can dynamically modify trading slippage parameters." });
    }
    if (isProxy) {
      score -= 10;
      risks.push({ severity: "MEDIUM", type: "PROXY_CONTRACT", desc: "This is a proxy contract; implementation code can be changed in the future." });
    }
    if (isMintable) {
      score -= 10;
      risks.push({ severity: "LOW", type: "MINTABLE", desc: "Owner can mint additional tokens, causing potential dilution." });
    }
    if (!isOwnerRenounced) {
      score -= 15;
      risks.push({ severity: "LOW", type: "OWNERSHIP_NOT_RENOUNCED", desc: `Contract owner exists (${ownerAddress}) and can invoke admin controls.` });
    }
    
    score = Math.max(0, score);
    
    logSuccess(`Token security audit complete`, options);
    
    if (!options.json) {
      console.log(`\n==================================================`);
      console.log(printColor(`SMART CONTRACT SECURITY AUDIT`, "bold"));
      console.log(`Token     : ${auditData.token_symbol || tokenInput} (${auditData.token_name || "Unknown"})`);
      console.log(`Address   : ${tokenAddress}`);
      console.log(`Network   : ${chainConfig.name}`);
      
      let scoreColor = "green";
      if (score < 50) scoreColor = "red";
      else if (score < 80) scoreColor = "yellow";
      
      console.log(`Security Score: ${printColor(`${score}/100`, scoreColor)}`);
      console.log(`--------------------------------------------------`);
      console.log(`Honeypot Check    : ${isHoneypot ? printColor("HONEYPOT DETECTED (DANGER)", "red") : printColor("Safe (Sellable)", "green")}`);
      console.log(`Trading Tax       : Buy: ${buyTax}%, Sell: ${sellTax}%`);
      console.log(`Proxy Contract    : ${isProxy ? "Yes (Owner modifiable)" : "No"}`);
      console.log(`Mintable Supply   : ${isMintable ? "Yes (Owner can mint)" : "No"}`);
      console.log(`Ownership Status  : ${isOwnerRenounced ? printColor("Renounced (Safe)", "green") : printColor("Active (Owner Exists)", "yellow")}`);
      
      if (risks.length > 0) {
        console.log(`--------------------------------------------------`);
        console.log(printColor(`RISK FINDINGS (${risks.length}):`, "bold"));
        for (const risk of risks) {
          let riskColor = "gray";
          if (risk.severity === "CRITICAL") riskColor = "red";
          else if (risk.severity === "HIGH") riskColor = "red";
          else if (risk.severity === "MEDIUM") riskColor = "yellow";
          
          console.log(` [${printColor(risk.severity, riskColor)}] ${risk.desc}`);
        }
      } else {
        console.log(`--------------------------------------------------`);
        console.log(printColor("✔ No dangerous risks found on the smart contract.", "green"));
      }
      console.log(`==================================================\n`);
    }
    
    console.log(JSON.stringify({
      success: true,
      chain: chainConfig.name,
      tokenAddress: tokenAddress,
      tokenSymbol: auditData.token_symbol || tokenInput,
      tokenName: auditData.token_name || "Unknown",
      securityScore: score,
      isHoneypot: isHoneypot,
      buyTaxPercent: buyTax,
      sellTaxPercent: sellTax,
      isProxy: isProxy,
      isMintable: isMintable,
      isOwnerRenounced: isOwnerRenounced,
      ownerAddress: ownerAddress,
      risks: risks,
      isPairAddress: isPairAddress,
      originalQueryAddress: originalQueryAddress,
      pairDetails: pairDetails
    }, null, 2));

  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.message
    }, null, 2));
  }
}
