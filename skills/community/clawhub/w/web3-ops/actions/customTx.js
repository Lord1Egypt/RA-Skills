import { ethers } from "ethers";
import {
  getWallet,
  parseUnits,
  logInfo,
  logSuccess,
  logError,
  logWarning,
  printColor
} from "./common.js";

export async function executeCustomTx(options = {}) {
  try {
    const {
      chain,
      to,
      data = "0x",
      value = "0",
      gasLimit,
      simulate
    } = options;

    if (!ethers.isAddress(to)) {
      throw new Error(`Target address "to" (${to}) is not a valid EVM address.`);
    }

    if (!data.startsWith("0x")) {
      throw new Error(`Transaction calldata must be a valid hex string starting with "0x".`);
    }

    const { wallet, chainConfig } = await getWallet(chain, options);
    const valueWei = parseUnits(value, 18);

    if (!options.json) {
      console.log(`\n==================================================`);
      console.log(printColor("CUSTOM TRANSACTION EXECUTION", "bold"));
      console.log(`==================================================`);
      console.log(`Network    : ${chainConfig.name}`);
      console.log(`Target (To): ${to}`);
      console.log(`Value (${chainConfig.symbol}): ${value}`);
      console.log(`Data (Hex) : ${data.substring(0, 66)}${data.length > 66 ? "..." : ""}`);
      console.log(`Wallet     : ${wallet.address}`);
      if (simulate) {
        console.log(`Simulation : ${printColor("TRUE (DRY-RUN)", "yellow")}`);
      }
      console.log(`==================================================\n`);
    }

    const txRequest = {
      to: to,
      data: data,
      value: valueWei
    };

    if (gasLimit) {
      txRequest.gasLimit = BigInt(gasLimit);
    }

    if (simulate) {
      logInfo("Simulating custom transaction (dry run)...", options);
      const estimatedGas = await wallet.estimateGas(txRequest);
      logSuccess("Custom transaction simulation succeeded.", options);
      console.log(JSON.stringify({
        success: true,
        simulated: true,
        action: "custom_tx",
        chain: chainConfig.name,
        target: to,
        estimatedGas: estimatedGas.toString()
      }, null, 2));
      return;
    }

    logInfo("Sending custom transaction...", options);
    const txResponse = await wallet.sendTransaction(txRequest);

    logInfo(`Transaction submitted. Tx Hash: ${txResponse.hash}`, options);
    logInfo("Waiting for block confirmation...", options);
    
    const receipt = await txResponse.wait(1);
    logSuccess("Transaction confirmed successfully.", options);

    console.log(JSON.stringify({
      success: true,
      action: "custom_tx",
      chain: chainConfig.name,
      txHash: receipt.hash,
      explorer: `${chainConfig.explorer}/tx/${receipt.hash}`
    }, null, 2));

  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.message
    }, null, 2));
  }
}
