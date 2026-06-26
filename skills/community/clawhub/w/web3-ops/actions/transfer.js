import { ethers } from "ethers";
import {
  getWallet,
  ERC20_ABI,
  parseUnits,
  formatUnits,
  logInfo,
  logSuccess,
  logError,
  logWarning,
  resolveTokenAddress
} from "./common.js";

export async function transfer(options = {}) {
  const {
    chain: chainInput,
    to: toAddress,
    amount: amountInput,
    token: tokenInput,
    simulate
  } = options;

  try {
    const { wallet, provider, chainConfig } = await getWallet(chainInput, options);
    
    if (!ethers.isAddress(toAddress)) {
      throw new Error(`Recipient address "${toAddress}" is not a valid EVM address.`);
    }

    // Resolve token address dynamically (if provided)
    const tokenAddress = tokenInput ? await resolveTokenAddress(tokenInput, chainConfig.id, options) : null;
    const isNative = !tokenAddress || tokenAddress === "0x0000000000000000000000000000000000000000";

    let decimals = 18;
    let symbol = chainConfig.symbol;
    let amountUnits;

    if (isNative) {
      amountUnits = parseUnits(amountInput, 18);
    } else {
      const tokenContract = new ethers.Contract(tokenAddress, ERC20_ABI, provider);
      [decimals, symbol] = await Promise.all([
        tokenContract.decimals(),
        tokenContract.symbol()
      ]);
      amountUnits = parseUnits(amountInput, decimals);
    }

    // Handle Simulation Mode
    if (simulate) {
      logInfo("Simulating transfer (dry run)...", options);
      let estimatedGas;
      
      if (isNative) {
        estimatedGas = await wallet.estimateGas({
          to: toAddress,
          value: amountUnits
        });
      } else {
        const tokenContract = new ethers.Contract(tokenAddress, ERC20_ABI, wallet);
        estimatedGas = await tokenContract.transfer.estimateGas(toAddress, amountUnits);
      }

      logSuccess("Transfer simulation succeeded.", options);
      console.log(JSON.stringify({
        success: true,
        simulated: true,
        chain: chainConfig.name,
        from: wallet.address,
        to: toAddress,
        amount: amountInput,
        symbol: symbol,
        tokenAddress: isNative ? "0x0000000000000000000000000000000000000000" : tokenAddress,
        estimatedGas: estimatedGas.toString()
      }, null, 2));
      return;
    }

    // Executing actual transfer
    let txResponse;
    logInfo(`Sending ${amountInput} ${symbol} to ${toAddress} on ${chainConfig.name}...`, options);

    if (isNative) {
      txResponse = await wallet.sendTransaction({
        to: toAddress,
        value: amountUnits
      });
    } else {
      const tokenContract = new ethers.Contract(tokenAddress, ERC20_ABI, wallet);
      txResponse = await tokenContract.transfer(toAddress, amountUnits);
    }

    logInfo(`Transaction sent. Tx Hash: ${txResponse.hash}`, options);
    logInfo("Waiting for block confirmation...", options);
    
    const receipt = await txResponse.wait(1);
    logSuccess("Transaction confirmed successfully.", options);
    
    console.log(JSON.stringify({
      success: true,
      chain: chainConfig.name,
      txHash: receipt.hash,
      from: receipt.from,
      to: toAddress,
      amount: amountInput,
      symbol: symbol,
      tokenAddress: isNative ? "0x0000000000000000000000000000000000000000" : tokenAddress,
      explorer: `${chainConfig.explorer}/tx/${receipt.hash}`
    }, null, 2));
  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.message
    }, null, 2));
  }
}
