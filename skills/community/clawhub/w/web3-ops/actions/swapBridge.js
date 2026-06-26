import { ethers } from "ethers";
import axios from "axios";
import {
  getWallet,
  ERC20_ABI,
  parseUnits,
  formatUnits,
  getChainConfig,
  resolveTokenAddress,
  logInfo,
  logSuccess,
  logError,
  logWarning,
  printColor,
  TOKEN_MAP
} from "./common.js";

// Helper to approve tokens if allowance is insufficient
async function ensureAllowance(wallet, tokenAddress, spenderAddress, amountWei, options = {}) {
  if (tokenAddress === "0x0000000000000000000000000000000000000000" || tokenAddress.toLowerCase() === "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee") {
    return; // Native tokens don't need approvals
  }

  const tokenContract = new ethers.Contract(tokenAddress, ERC20_ABI, wallet);
  const allowance = await tokenContract.allowance(wallet.address, spenderAddress);
  
  if (allowance < amountWei) {
    if (options.simulate) {
      logInfo(`[Simulation] Would submit approval transaction for spender ${spenderAddress}...`, options);
      return;
    }
    logInfo(`Submitting approval (Approve) transaction for spender ${spenderAddress}...`, options);
    const tx = await tokenContract.approve(spenderAddress, ethers.MaxUint256);
    logInfo(`Approval transaction sent: ${tx.hash}. Waiting for confirmation...`, options);
    await tx.wait(1);
    logSuccess("Approval confirmed successfully.", options);
  }
}

// ---------------------------------------------------------
// 1. LI.FI SWAP & BRIDGE (MODE AUTO)
// ---------------------------------------------------------
async function runLifiQuote(wallet, fromChainId, toChainId, fromToken, toToken, amountWei, slippage, options = {}) {
  logInfo("Contacting Li.Fi API to fetch the best route...", options);
  
  const params = {
    fromChain: fromChainId,
    toChain: toChainId,
    fromToken: fromToken,
    toToken: toToken,
    fromAmount: amountWei.toString(),
    fromAddress: wallet.address,
    slippage: slippage || 0.005
  };

  const response = await axios.get("https://li.quest/v1/quote", { params });
  const quote = response.data;

  // Check token allowance if needed
  const approvalAddress = quote.estimate.approvalAddress;
  if (approvalAddress && approvalAddress !== ethers.ZeroAddress) {
    await ensureAllowance(wallet, fromToken, approvalAddress, amountWei, options);
  }

  const txRequest = quote.transactionRequest;

  if (options.simulate) {
    logInfo(`Simulating Li.Fi swap/bridge route (${quote.toolDetails.name}) (dry run)...`, options);
    const estimatedGas = await wallet.estimateGas({
      to: txRequest.to,
      data: txRequest.data,
      value: txRequest.value
    });
    return {
      hash: "0x0000000000000000000000000000000000000000",
      simulated: true,
      estimatedGas: estimatedGas.toString(),
      toolName: quote.toolDetails.name
    };
  }

  logInfo(`Sending swap/bridge transaction using Li.Fi route (${quote.toolDetails.name})...`, options);
  
  const txResponse = await wallet.sendTransaction({
    to: txRequest.to,
    data: txRequest.data,
    value: txRequest.value,
    gasLimit: txRequest.gasLimit ? (BigInt(txRequest.gasLimit) * 12n / 10n) : undefined // 20% buffer
  });

  return txResponse;
}

// ---------------------------------------------------------
// 2. RELAY BRIDGE & SWAP (MODE MANUAL - PROVIDER RELAY)
// ---------------------------------------------------------
async function runRelayQuote(wallet, fromChainId, toChainId, fromToken, toToken, amountWei, options = {}) {
  logInfo("Contacting Relay.link API to fetch transaction route...", options);
  
  const payload = {
    user: wallet.address,
    originChainId: fromChainId,
    destinationChainId: toChainId,
    originCurrency: fromToken,
    destinationCurrency: toToken,
    amount: amountWei.toString(),
    tradeType: "EXACT_INPUT"
  };

  const response = await axios.post("https://api.relay.link/quote", payload);
  const quote = response.data;

  if (!quote.steps || quote.steps.length === 0) {
    throw new Error("Relay API did not return a valid route for this request.");
  }

  let lastTxResponse;
  let simulatedGas = 0n;

  for (const step of quote.steps) {
    logInfo(`Processing Relay step: ${step.action} - ${step.description}`, options);
    for (const item of step.items) {
      if (item.status === "todo" && item.kind === "transaction") {
        const txData = item.data;
        
        // Ensure approval if origin token is ERC-20
        if (fromToken !== "0x0000000000000000000000000000000000000000" && txData.to.toLowerCase() !== fromToken.toLowerCase()) {
          await ensureAllowance(wallet, fromToken, txData.to, amountWei, options);
        }

        if (options.simulate) {
          logInfo(`Simulating Relay step transaction (${step.action})...`, options);
          const stepGas = await wallet.estimateGas({
            to: txData.to,
            data: txData.data,
            value: txData.value
          });
          simulatedGas += stepGas;
          lastTxResponse = {
            hash: "0x0000000000000000000000000000000000000000",
            simulated: true,
            estimatedGas: simulatedGas.toString()
          };
        } else {
          logInfo(`Sending transaction for Relay step (${step.action})...`, options);
          lastTxResponse = await wallet.sendTransaction({
            to: txData.to,
            data: txData.data,
            value: txData.value,
            gasLimit: txData.gasLimit ? (BigInt(txData.gasLimit) * 12n / 10n) : undefined
          });
          // Wait for step confirmation before proceeding to next steps
          if (quote.steps.length > 1) {
            logInfo("Waiting for current step confirmation...", options);
            await lastTxResponse.wait(1);
          }
        }
      }
    }
  }

  return lastTxResponse;
}

// ---------------------------------------------------------
// 3. UNISWAP V3 SWAP DIRECT CONTRACT CALL
// ---------------------------------------------------------
async function runUniswapV3Swap(wallet, chainId, fromToken, toToken, amountWei, slippage, options = {}) {
  // Uniswap V3 Router Standard Address (Matches on most EVM chains)
  const UNISWAP_V3_ROUTER = "0xE592427A0AEce92De3Edee1F18E0157C05861564";
  
  logInfo(`Using direct contract interaction with Uniswap V3 SwapRouter (${UNISWAP_V3_ROUTER})...`, options);
  
  // Resolve WETH addresses if native tokens are involved
  const resolvedFrom = fromToken === "0x0000000000000000000000000000000000000000" ? await resolveTokenAddress("WETH", chainId, options) : fromToken;
  const resolvedTo = toToken === "0x0000000000000000000000000000000000000000" ? await resolveTokenAddress("WETH", chainId, options) : toToken;

  const abi = [
    "function exactInputSingle((address tokenIn, address tokenOut, uint24 proxyFee, address recipient, uint256 deadline, uint256 amountIn, uint256 amountOutMinimum, uint160 sqrtPriceLimitX96)) external payable returns (uint256 amountOut)"
  ];
  
  const router = new ethers.Contract(UNISWAP_V3_ROUTER, abi, wallet);
  const deadline = Math.floor(Date.now() / 1000) + 60 * 20; // 20 minutes deadline
  
  if (fromToken !== "0x0000000000000000000000000000000000000000") {
    await ensureAllowance(wallet, fromToken, UNISWAP_V3_ROUTER, amountWei, options);
  }

  const params = {
    tokenIn: resolvedFrom,
    tokenOut: resolvedTo,
    fee: 3000, // 0.3% fee tier
    recipient: wallet.address,
    deadline: deadline,
    amountIn: amountWei,
    amountOutMinimum: 0, // min amount out
    sqrtPriceLimitX96: 0
  };

  const isNativeIn = fromToken === "0x0000000000000000000000000000000000000000";

  if (options.simulate) {
    logInfo("Simulating Uniswap V3 swap single call...", options);
    const estimatedGas = await router.exactInputSingle.estimateGas(params, {
      value: isNativeIn ? amountWei : 0
    });
    return {
      hash: "0x0000000000000000000000000000000000000000",
      simulated: true,
      estimatedGas: estimatedGas.toString()
    };
  }
  
  const tx = await router.exactInputSingle(params, {
    value: isNativeIn ? amountWei : 0
  });

  return tx;
}

// ---------------------------------------------------------
// 4. PANCAKESWAP V3 SWAP DIRECT CONTRACT CALL
// ---------------------------------------------------------
async function runPancakeSwapV3Swap(wallet, chainId, fromToken, toToken, amountWei, options = {}) {
  // PancakeSwap SmartRouter V3 Address
  const PANCAKE_V3_ROUTER = "0x13f4EA83D0bd40E75c8222255bc855a974568Dd4";
  
  logInfo(`Using direct contract interaction with PancakeSwap V3 Router (${PANCAKE_V3_ROUTER})...`, options);
  
  const resolvedFrom = fromToken === "0x0000000000000000000000000000000000000000" ? await resolveTokenAddress("WETH", chainId, options) : fromToken;
  const resolvedTo = toToken === "0x0000000000000000000000000000000000000000" ? await resolveTokenAddress("WETH", chainId, options) : toToken;

  const abi = [
    "function exactInputSingle((address tokenIn, address tokenOut, uint24 fee, address recipient, uint256 deadline, uint256 amountIn, uint256 amountOutMinimum, uint160 sqrtPriceLimitX96)) external payable returns (uint256 amountOut)"
  ];
  
  const router = new ethers.Contract(PANCAKE_V3_ROUTER, abi, wallet);
  const deadline = Math.floor(Date.now() / 1000) + 60 * 20;

  if (fromToken !== "0x0000000000000000000000000000000000000000") {
    await ensureAllowance(wallet, fromToken, PANCAKE_V3_ROUTER, amountWei, options);
  }

  const params = {
    tokenIn: resolvedFrom,
    tokenOut: resolvedTo,
    fee: 2500, // 0.25% fee tier
    recipient: wallet.address,
    deadline: deadline,
    amountIn: amountWei,
    amountOutMinimum: 0,
    sqrtPriceLimitX96: 0
  };

  const isNativeIn = fromToken === "0x0000000000000000000000000000000000000000";

  if (options.simulate) {
    logInfo("Simulating PancakeSwap V3 swap single call...", options);
    const estimatedGas = await router.exactInputSingle.estimateGas(params, {
      value: isNativeIn ? amountWei : 0
    });
    return {
      hash: "0x0000000000000000000000000000000000000000",
      simulated: true,
      estimatedGas: estimatedGas.toString()
    };
  }

  const tx = await router.exactInputSingle(params, {
    value: isNativeIn ? amountWei : 0
  });

  return tx;
}

// ---------------------------------------------------------
// MAIN EXPORT FUNCTION FOR CLI
// ---------------------------------------------------------
export async function swapOrBridge(options) {
  try {
    const {
      chain,
      fromChain,
      toChain,
      fromToken: rawFromToken,
      toToken: rawToToken,
      amount,
      mode = "auto",
      provider = "lifi",
      slippage = "0.5",
      simulate
    } = options;

    const originChainName = fromChain || chain;
    const destChainName = toChain || chain || fromChain;
    
    if (!originChainName) {
      throw new Error("Source network (--chain or --fromChain) is required.");
    }

    const { wallet, chainConfig } = await getWallet(originChainName, options);
    const destChainConfig = getChainConfig(destChainName);

    // Resolve token addresses dynamically (Li.Fi API fallback)
    const fromTokenAddress = await resolveTokenAddress(rawFromToken, chainConfig.id, options);
    const toTokenAddress = await resolveTokenAddress(rawToToken, destChainConfig.id, options);
    
    // Determine decimals of input token to parse input amount
    let decimals = 18;
    if (fromTokenAddress !== "0x0000000000000000000000000000000000000000") {
      const tokenContract = new ethers.Contract(fromTokenAddress, ERC20_ABI, wallet.provider);
      decimals = await tokenContract.decimals();
    }
    const amountWei = parseUnits(amount, decimals);
    const slippageFloat = parseFloat(slippage) / 100;

    const isBridge = chainConfig.id !== destChainConfig.id;

    if (!options.json) {
      console.log(`\n==================================================`);
      console.log(printColor("WEB3 ON-CHAIN SWAP/BRIDGE REQUEST", "bold"));
      console.log(`==================================================`);
      console.log(`Action     : ${isBridge ? "BRIDGE (Cross-Chain)" : "SWAP (Same-Chain)"}`);
      console.log(`Source     : ${amount} ${rawFromToken} on ${chainConfig.name}`);
      console.log(`Target     : ${rawToToken} on ${destChainConfig.name}`);
      console.log(`Wallet     : ${wallet.address}`);
      console.log(`Mode       : ${mode.toUpperCase()}`);
      if (mode === "manual") {
        console.log(`Provider   : ${provider.toUpperCase()}`);
      }
      if (simulate) {
        console.log(`Simulation : ${printColor("TRUE (DRY-RUN)", "yellow")}`);
      }
      console.log(`==================================================\n`);
    }

    let txResponse;

    if (mode === "auto") {
      // Auto routing uses Li.Fi aggregator
      txResponse = await runLifiQuote(wallet, chainConfig.id, destChainConfig.id, fromTokenAddress, toTokenAddress, amountWei, slippageFloat, options);
    } else {
      // Manual routing
      const providerLower = provider.toLowerCase();
      
      if (isBridge) {
        if (providerLower === "relay") {
          txResponse = await runRelayQuote(wallet, chainConfig.id, destChainConfig.id, fromTokenAddress, toTokenAddress, amountWei, options);
        } else if (providerLower === "lifi") {
          txResponse = await runLifiQuote(wallet, chainConfig.id, destChainConfig.id, fromTokenAddress, toTokenAddress, amountWei, slippageFloat, options);
        } else {
          throw new Error(`Provider "${provider}" does not support cross-chain bridging. Supported options: relay, lifi`);
        }
      } else {
        if (providerLower === "uniswap" || providerLower === "uniswapv3") {
          txResponse = await runUniswapV3Swap(wallet, chainConfig.id, fromTokenAddress, toTokenAddress, amountWei, slippageFloat, options);
        } else if (providerLower === "pancakeswap") {
          txResponse = await runPancakeSwapV3Swap(wallet, chainConfig.id, fromTokenAddress, toTokenAddress, amountWei, options);
        } else if (providerLower === "relay") {
          txResponse = await runRelayQuote(wallet, chainConfig.id, destChainConfig.id, fromTokenAddress, toTokenAddress, amountWei, options);
        } else if (providerLower === "lifi") {
          txResponse = await runLifiQuote(wallet, chainConfig.id, destChainConfig.id, fromTokenAddress, toTokenAddress, amountWei, slippageFloat, options);
        } else {
          throw new Error(`Provider "${provider}" is not supported for Swap. Options: lifi, relay, uniswap, pancakeswap`);
        }
      }
    }

    if (simulate) {
      logSuccess("Transaction simulation completed successfully (no errors detected).", options);
      console.log(JSON.stringify({
        success: true,
        simulated: true,
        action: isBridge ? "bridge" : "swap",
        provider: mode === "auto" ? "lifi" : provider,
        estimatedGas: txResponse.estimatedGas || "unknown",
        toolUsed: txResponse.toolName || provider
      }, null, 2));
      return;
    }

    logInfo(`Transaction submitted to network. Tx Hash: ${txResponse.hash}`, options);
    logInfo("Waiting for block confirmation...", options);
    
    const receipt = await txResponse.wait(1);
    logSuccess("Transaction confirmed successfully.", options);
    
    console.log(JSON.stringify({
      success: true,
      action: isBridge ? "bridge" : "swap",
      provider: mode === "auto" ? "lifi" : provider,
      txHash: receipt.hash,
      from: receipt.from,
      explorer: `${chainConfig.explorer}/tx/${receipt.hash}`
    }, null, 2));

  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.response?.data?.message || error.message
    }, null, 2));
  }
}
