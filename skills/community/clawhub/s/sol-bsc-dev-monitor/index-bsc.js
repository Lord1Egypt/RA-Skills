#!/usr/bin/env node

const { ethers } = require('ethers');
const fs = require('fs');
const path = require('path');

const CONFIG = {
  BSC_RPC: process.env.BSC_RPC || 'https://bsc-dataseed.binance.org',
  MONITOR_INTERVAL: 3000, // 3 seconds
  DEFAULT_DURATION: 3600,
  WBNB_ADDRESS: '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
};

const LOG_DIR = path.join(__dirname, 'logs-bsc');
const DETECTIONS_DIR = path.join(__dirname, 'detections-bsc');

if (!fs.existsSync(LOG_DIR)) fs.mkdirSync(LOG_DIR, { recursive: true });
if (!fs.existsSync(DETECTIONS_DIR)) fs.mkdirSync(DETECTIONS_DIR, { recursive: true });

function loadDetections() {
  const detectionsFile = path.join(DETECTIONS_DIR, 'detections.json');
  if (fs.existsSync(detectionsFile)) {
    try {
      const data = fs.readFileSync(detectionsFile, 'utf8');
      return JSON.parse(data);
    } catch (error) {
      return [];
    }
  }
  return [];
}

function saveDetections(detections) {
  const detectionsFile = path.join(DETECTIONS_DIR, 'detections.json');
  const trimmedDetections = detections.slice(-1000);
  try {
    fs.writeFileSync(
      detectionsFile,
      JSON.stringify(trimmedDetections, null, 2)
    );
  } catch (error) {
    console.log(`Error saving detections: ${error.message}`);
  }
}

function log(message, level = 'INFO') {
  const timestamp = new Date().toISOString();
  const logMessage = `[${timestamp}] [${level}] ${message}`;
  console.log(logMessage);
  
  const logFile = path.join(LOG_DIR, 'bsc-monitor.log');
  fs.appendFileSync(logFile, logMessage + '\n');
}

async function monitorBSC(input) {
  const { address, duration } = input;
  const monitorDuration = duration || CONFIG.DEFAULT_DURATION;
  const startTime = Date.now();
  
  log(`📊 Starting BSC monitoring for address: ${address}`);
  log(`📊 Monitoring duration: ${monitorDuration} seconds`);
  log(`📊 Mode: Monitor only - no auto-buy`);
  log(`📊 User can manually buy using PancakeSwap`);
  
  const provider = new ethers.JsonRpcProvider(CONFIG.BSC_RPC);
  
  let lastBlockNumber = await provider.getBlockNumber();
  log(`📊 Starting block number: ${lastBlockNumber}`);
  
  const endTime = startTime + (monitorDuration * 1000);
  let blocksScanned = 0;
  let detections = loadDetections();
  
  while (Date.now() < endTime) {
    try {
      const currentBlock = await provider.getBlock('latest');
      const currentBlockNumber = currentBlock.number;
      
      if (currentBlockNumber > lastBlockNumber) {
        for (let i = lastBlockNumber + 1; i <= currentBlockNumber; i++) {
          const block = await provider.getBlock(i, true);
          
          if (block && block.transactions) {
            for (const tx of block.transactions) {
              const detected = await checkTransaction(tx, address, provider);
              
              if (detected) {
                log(`🎉 Detection found! Block: ${i}, Hash: ${tx.hash}`);
                
                const detection = {
                  chain: 'BSC',
                  blockNumber: i,
                  hash: tx.hash,
                  from: tx.from,
                  to: tx.to,
                  tokenAddress: tx.to,
                  timestamp: new Date().toISOString()
                };
                
                detections.push(detection);
                saveDetections(detections);
                
                log(`✅ Detection logged for token: ${tx.to}`);
                log(`💰 User can buy at: https://exchange.pancakeswap.finance/#/swap`)
              }
            }
          }
        }
        
        lastBlockNumber = currentBlockNumber;
        blocksScanned += currentBlockNumber - lastBlockNumber;
      }
      
      await new Promise(resolve => setTimeout(resolve, CONFIG.MONITOR_INTERVAL));
      
    } catch (error) {
      log(`❌ Error checking block ${lastBlockNumber}: ${error.message}`);
      lastBlockNumber++;
    }
  }
  
  const actualDuration = ((Date.now() - startTime) / 1000).toFixed(2);
  
  log(`📊 BSC monitoring completed`);
  log(`📊 Duration: ${actualDuration} seconds`);
  log(`📊 Blocks scanned: ${blocksScanned}`);
  log(`📊 Total detections: ${detections.length}`);
  log(`📊 Mode: Monitor only - no auto-buy`);
  
  return {
    success: true,
    chain: 'BSC',
    monitoring: {
      address,
      startTime: new Date(startTime).toISOString(),
      endTime: new Date().toISOString(),
      duration: monitorDuration,
      actualDuration,
      blocksScanned,
      detections
    }
  };
}

async function checkTransaction(tx, targetAddress, provider) {
  try {
    // Check if transaction is from target address to a contract (token)
    if (tx.from.toLowerCase() === targetAddress.toLowerCase()) {
      if (tx.to && tx.to !== targetAddress) {
        log(`💰 Transaction from ${tx.from} to ${tx.to}`);
        
        const tokenInfo = await getTokenInfo(tx.to, provider);
        
        return {
          hash: tx.hash,
          from: tx.from,
          to: tx.to,
          tokenAddress: tx.to,
          tokenName: tokenInfo.name,
          tokenSymbol: tokenInfo.symbol,
          decimals: tokenInfo.decimals
        };
      }
    }
    
    return null;
  } catch (error) {
    return null;
  }
}

async function getTokenInfo(tokenAddress, provider) {
  try {
    const tokenContract = new ethers.Contract(
      tokenAddress,
      [
        'function name() external view returns (string)',
        'function symbol() external view returns (string)',
        'function decimals() external view returns (uint8)'
      ],
      provider
    );
    
    const [name, symbol, decimals] = await Promise.all([
      tokenContract.name().catch(() => Promise.resolve('Unknown')),
      tokenContract.symbol().catch(() => Promise.resolve('UNKNOWN')),
      tokenContract.decimals().catch(() => Promise.resolve(18))
    ]);
    
    return { name, symbol, decimals };
  } catch (error) {
    log(`❌ Error getting token info: ${error.message}`);
    return { name: 'Unknown', symbol: 'UNKNOWN', decimals: 18 };
  }
}

module.exports = { monitorBSC };

if (require.main === module) {
  const action = process.argv[2] || 'monitor';
  const address = process.argv[3];
  const chain = process.argv[4] || 'BSC';
  const duration = process.argv[5] ? parseInt(process.argv[5]) : undefined;
  
  monitorBSC({ address, chain, duration }).then(result => {
    console.log(JSON.stringify(result, null, 2));
  }).catch(error => {
    console.error('Error:', error);
    process.exit(1);
  });
}
