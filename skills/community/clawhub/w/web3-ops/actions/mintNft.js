import { ethers } from "ethers";
import axios from "axios";
import {
  getWallet,
  parseUnits,
  logInfo,
  logSuccess,
  logError,
  logWarning,
  printColor,
  getExplorerApiUrl,
  getExplorerApiKey
} from "./common.js";

// Helper to parse NFT marketplace URLs
export function parseNftUrl(url) {
  try {
    const urlObj = new URL(url);
    const host = urlObj.hostname.toLowerCase();
    
    // OpenSea: opensea.io/assets/ethereum/0x.../123 or opensea.io/item/ethereum/0x.../123
    if (host.includes("opensea.io")) {
      const parts = urlObj.pathname.split("/").filter(Boolean);
      if ((parts[0] === "assets" || parts[0] === "item") && parts.length >= 3) {
        return {
          chain: parts[1],
          contractAddress: parts[2],
          tokenId: parts[3] || null
        };
      }
    }
    
    // Zora: zora.co/collect/base:0x.../123 or zora.co/collect/base:0x...
    if (host.includes("zora.co")) {
      const parts = urlObj.pathname.split("/").filter(Boolean);
      if (parts[0] === "collect" && parts.length >= 2) {
        const collectPart = parts[1];
        const [chain, contractAddress] = collectPart.split(":");
        const tokenId = parts[2] || null;
        return {
          chain,
          contractAddress,
          tokenId
        };
      }
    }
    
    // Rarible: rarible.com/token/base/0x...:123 or rarible.com/token/0x...:123?chain=base
    if (host.includes("rarible.com")) {
      const parts = urlObj.pathname.split("/").filter(Boolean);
      if (parts[0] === "token" && parts.length >= 2) {
        if (parts.length >= 3) {
          const chain = parts[1];
          const [contractAddress, tokenId] = parts[2].split(":");
          return { chain, contractAddress, tokenId };
        } else {
          const [contractAddress, tokenId] = parts[1].split(":");
          const chain = urlObj.searchParams.get("chain") || "ethereum";
          return { chain, contractAddress, tokenId };
        }
      }
    }
  } catch (err) {
    // Suppress parsing errors if not a valid URL
  }
  return null;
}

// Fetch verified contract ABI from block explorer (Etherscan V2 or Blockscout keyless fallback)
async function fetchContractAbi(contractAddress, chainId, options = {}) {
  const apiKey = getExplorerApiKey(chainId);
  
  // 1. Try Blockscout first if no API key is set (keyless / rate-limit free)
  if (!apiKey) {
    const blockscoutUrl = getBlockscoutApiUrl(chainId);
    if (blockscoutUrl) {
      try {
        logInfo(`Fetching verified ABI from Blockscout (keyless): ${blockscoutUrl}...`, options);
        const response = await axios.get(blockscoutUrl, {
          params: {
            module: "contract",
            action: "getabi",
            address: contractAddress
          },
          timeout: 6000
        });
        if (response.data && response.data.status === "1" && response.data.result) {
          return JSON.parse(response.data.result);
        }
      } catch (err) {
        logWarning(`Blockscout query failed: ${err.message}`, options);
      }
    }
  }

  // 2. Fallback or primary to Etherscan/chain-specific API if key is available or Blockscout failed
  const explorerUrl = getExplorerApiUrl(chainId);
  if (explorerUrl) {
    try {
      let finalUrl = explorerUrl;
      const params = {
        module: "contract",
        action: "getabi",
        address: contractAddress,
        apikey: apiKey || undefined
      };
      
      // If it is Etherscan mainnet, use the v2 API to avoid the deprecated v1 endpoint
      if (chainId === 1 || chainId === 11155111) {
        finalUrl = "https://api.etherscan.io/v2/api";
        params.chainid = chainId;
      }
      
      logInfo(`Fetching verified ABI from Etherscan-based explorer: ${finalUrl}...`, options);
      const response = await axios.get(finalUrl, {
        params,
        timeout: 6000
      });
      
      if (response.data && response.data.status === "1" && response.data.result) {
        return JSON.parse(response.data.result);
      } else {
        logWarning(`Explorer API response: ${response.data.result || response.data.message}`, options);
      }
    } catch (err) {
      logWarning(`Explorer API query failed: ${err.message}`, options);
    }
  }

  return null;
}

function getBlockscoutApiUrl(chainId) {
  const mapping = {
    1: "https://eth.blockscout.com/api",
    11155111: "https://eth-sepolia.blockscout.com/api",
    42161: "https://arbitrum.blockscout.com/api",
    10: "https://optimism.blockscout.com/api",
    8453: "https://base.blockscout.com/api",
    137: "https://polygon.blockscout.com/api",
    534352: "https://scroll.blockscout.com/api",
    324: "https://zksync.blockscout.com/api",
    59144: "https://linea.blockscout.com/api",
    56: "https://bsc.blockscout.com/api"
  };
  return mapping[chainId] || "";
}

// Smart detection of mint function from ABI
function detectMintFunction(abi, userQuantity = 1, walletAddress = "", tokenId = null) {
  const mintPatterns = [/mint/i, /claim/i, /purchase/i, /buy/i];
  const candidates = [];
  
  for (const item of abi) {
    if (item.type === "function") {
      if (item.stateMutability !== "view" && item.stateMutability !== "pure") {
        const matchesName = mintPatterns.some(pat => pat.test(item.name));
        if (matchesName) {
          candidates.push(item);
        }
      }
    }
  }
  
  if (candidates.length === 0) return null;
  
  // Sort candidates to find the best match (exact mint/claim first)
  candidates.sort((a, b) => {
    const nameA = a.name.toLowerCase();
    const nameB = b.name.toLowerCase();
    
    if (nameA === "mint" && nameB !== "mint") return -1;
    if (nameB === "mint" && nameA !== "mint") return 1;
    if (nameA === "claim" && nameB !== "claim") return -1;
    if (nameB === "claim" && nameA !== "claim") return 1;
    
    if (nameA.includes("mint") && !nameB.includes("mint")) return -1;
    if (nameB.includes("mint") && !nameA.includes("mint")) return 1;
    if (nameA.includes("claim") && !nameB.includes("claim")) return -1;
    if (nameB.includes("claim") && !nameA.includes("claim")) return 1;
    
    return 0;
  });
  
  const selected = candidates[0];
  const inputTypes = selected.inputs.map(i => i.type).join(",");
  const functionSig = `${selected.name}(${inputTypes})`;
  
  const args = [];
  for (const input of selected.inputs) {
    const type = input.type;
    const name = input.name.toLowerCase();
    
    if (type.includes("address")) {
      args.push(walletAddress);
    } else if (type.includes("uint") || type.includes("int")) {
      if ((name.includes("id") || name.includes("token")) && tokenId !== null) {
        args.push(Number(tokenId));
      } else {
        args.push(userQuantity);
      }
    } else if (type === "bool") {
      args.push(true);
    } else if (type === "bytes") {
      args.push("0x");
    } else {
      args.push("");
    }
  }
  
  return {
    functionSig,
    args
  };
}

export async function mintNft(options = {}) {
  try {
    const {
      chain,
      contract: contractAddress,
      function: functionSig,
      args: rawArgs,
      value = "0",
      simulate
    } = options;

    let targetChain = chain;
    let targetContract = contractAddress;
    let targetTokenId = null;

    const parsedUrl = parseNftUrl(contractAddress);
    if (parsedUrl) {
      targetChain = parsedUrl.chain;
      targetContract = parsedUrl.contractAddress;
      targetTokenId = parsedUrl.tokenId;
      logInfo(`Parsed NFT Marketplace URL: Chain = ${targetChain}, Contract = ${targetContract}, Token ID = ${targetTokenId || "None"}`, options);
    }

    if (!targetChain) {
      throw new Error("Blockchain network is required. Please specify --chain <chain> or use a marketplace URL.");
    }

    if (!ethers.isAddress(targetContract)) {
      throw new Error(`NFT contract address "${targetContract}" is not a valid EVM address.`);
    }

    const { wallet, chainConfig } = await getWallet(targetChain, options);
    
    let finalFunctionSig = functionSig;
    let finalArgs = rawArgs;

    // Detect mint function from ABI if function is not manually specified
    if (!finalFunctionSig) {
      logInfo(`Fetching verified contract ABI from explorer for ${targetContract}...`, options);
      const abi = await fetchContractAbi(targetContract, chainConfig.id, options);
      if (abi) {
        const detected = detectMintFunction(abi, 1, wallet.address, targetTokenId);
        if (detected) {
          finalFunctionSig = detected.functionSig;
          finalArgs = JSON.stringify(detected.args);
          logInfo(`Auto-detected mint function: "${finalFunctionSig}" with arguments: ${finalArgs}`, options);
        } else {
          logWarning(`No matching mint/claim functions found in ABI.`, options);
        }
      } else {
        logWarning(`Could not fetch verified ABI from explorer.`, options);
      }

      // Default fallback if detection failed
      if (!finalFunctionSig) {
        finalFunctionSig = "mint(uint256)";
        finalArgs = "[1]";
        logWarning(`Falling back to default: "${finalFunctionSig}" with arguments: ${finalArgs}`, options);
      }
    }

    // Default arguments logic if function was specified but args were not
    if (finalFunctionSig && !finalArgs) {
      const match = finalFunctionSig.match(/\((.*)\)/);
      if (match && match[1].trim() !== "") {
        const types = match[1].split(",").map(t => t.trim());
        const inferred = types.map(type => {
          if (type.includes("address")) return wallet.address;
          if (type.includes("uint") || type.includes("int")) {
            if (targetTokenId !== null) return Number(targetTokenId);
            return 1;
          }
          if (type === "bool") return true;
          if (type === "bytes") return "0x";
          return "";
        });
        finalArgs = JSON.stringify(inferred);
      } else {
        finalArgs = "[]";
      }
      logInfo(`Inferred arguments: ${finalArgs}`, options);
    }

    // Parse arguments
    let parsedArgs = [];
    try {
      parsedArgs = JSON.parse(finalArgs);
      if (!Array.isArray(parsedArgs)) {
        parsedArgs = [parsedArgs];
      }
    } catch (e) {
      if (finalArgs.includes(",")) {
        parsedArgs = finalArgs.split(",").map(item => item.trim());
      } else {
        parsedArgs = [finalArgs];
      }
    }

    const valueWei = parseUnits(value, 18);

    if (!options.json) {
      console.log(`\n==================================================`);
      console.log(printColor("NFT MINTING REQUEST", "bold"));
      console.log(`==================================================`);
      console.log(`Network    : ${chainConfig.name}`);
      console.log(`Contract   : ${targetContract}`);
      console.log(`Function   : ${finalFunctionSig}`);
      console.log(`Arguments  : ${JSON.stringify(parsedArgs)}`);
      console.log(`Value (${chainConfig.symbol}): ${value}`);
      console.log(`Wallet     : ${wallet.address}`);
      if (simulate) {
        console.log(`Simulation : ${printColor("TRUE (DRY-RUN)", "yellow")}`);
      }
      console.log(`==================================================\n`);
    }

    let cleanSig = finalFunctionSig.trim();
    if (!cleanSig.startsWith("function ")) {
      cleanSig = `function ${cleanSig}`;
    }
    if (!cleanSig.includes("payable")) {
      cleanSig = `${cleanSig} payable`;
    }

    const abi = [cleanSig];
    const contract = new ethers.Contract(targetContract, abi, wallet);
    
    const match = finalFunctionSig.match(/([a-zA-Z0-9_]+)\s*\(/);
    if (!match) {
      throw new Error(`Failed to parse function name from signature "${finalFunctionSig}". Correct format example: "mint(uint256)"`);
    }
    const functionName = match[1];

    if (simulate) {
      logInfo(`Simulating NFT mint calling "${functionName}" (dry run)...`, options);
      const estimatedGas = await contract[functionName].estimateGas(...parsedArgs, {
        value: valueWei
      });
      logSuccess("NFT mint simulation succeeded.", options);
      console.log(JSON.stringify({
        success: true,
        simulated: true,
        action: "nft_mint",
        chain: chainConfig.name,
        contract: targetContract,
        estimatedGas: estimatedGas.toString()
      }, null, 2));
      return;
    }

    logInfo(`Calling function "${functionName}" on NFT contract...`, options);

    const txResponse = await contract[functionName](...parsedArgs, {
      value: valueWei
    });

    logInfo(`Mint transaction submitted. Tx Hash: ${txResponse.hash}`, options);
    logInfo("Waiting for block confirmation...", options);
    
    const receipt = await txResponse.wait(1);
    logSuccess("Transaction confirmed successfully.", options);

    console.log(JSON.stringify({
      success: true,
      action: "nft_mint",
      chain: chainConfig.name,
      contract: targetContract,
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
