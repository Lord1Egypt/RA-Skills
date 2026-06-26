#!/usr/bin/env node

const { Connection, PublicKey, Keypair, SystemProgram, Transaction, sendAndConfirmTransaction, LAMPORTS_PER_SOL } = require('@solana/web3.js');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

const CONFIG = {
  SOLANA_RPC: process.env.SOLANA_RPC || 'https://api.mainnet-beta.solana.com',
  JUPITER_API: 'https://quote-api.jup.ag/v6',
  MONITOR_INTERVAL: 10000,
  DEFAULT_DURATION: 3600,
  WSOL_MINT: 'So11111111111111111111111111111111111112'
};

const LOG_DIR = path.join(__dirname, 'logs-sol');
const DETECTIONS_DIR = path.join(__dirname, 'detections-sol');

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
  
  const logFile = path.join(LOG_DIR, 'sol-monitor.log');
  fs.appendFileSync(logFile, logMessage + '\n');
}

async function monitorSOL(input) {
  const { address, duration, autoBuy } = input;
  const monitorDuration = duration || CONFIG.DEFAULT_DURATION;
  const startTime = Date.now();
  
  const connection = new Connection(CONFIG.SOLANA_RPC);
  
  log(`📊 Starting Solana monitoring for address: ${address}`);
  log(`📊 Monitoring duration: ${monitorDuration} seconds`);
  log(`📊 Mode: Monitor only - no auto-buy`);
  log(`📊 User can manually buy using Jupiter Aggregator`);
  
  let lastSlot = 0;
  let slotsScanned = 0;
  let detections = loadDetections();
  
  const endTime = startTime + (monitorDuration * 1000);
  
  while (Date.now() < endTime) {
    try {
      const currentSlot = await connection.getSlot();
      
      if (currentSlot > lastSlot) {
        for (let i = lastSlot + 1; i <= currentSlot; i++) {
          const block = await connection.getBlock(i);
          
          if (block && block.transactions && block.transactions.length > 0) {
            for (const tx of block.transactions) {
              const detected = await checkTransaction(tx, address, connection);
              
              if (detected) {
                log(`🎉 Detection found! Slot: ${i}, Signature: ${detected.signature}`);
                
                const detection = {
                  chain: 'SOL',
                  slot: i,
                  signature: detected.signature,
                  timestamp: new Date().toISOString(),
                  from: detected.from,
                  to: detected.to,
                  tokenMint: detected.tokenMint,
                  tokenSymbol: detected.tokenSymbol,
                  amount: detected.amount,
                  decimals: detected.decimals
                };
                
                detections.push(detection);
                saveDetections(detections);
                
                log(`✅ Detection logged for token: ${detected.tokenSymbol}`);
                log(`💰 User can buy at: https://jup.ag`);
              }
            }
          }
        }
        
        lastSlot = currentSlot;
        slotsScanned += currentSlot - lastSlot;
      }
      
      await new Promise(resolve => setTimeout(resolve, CONFIG.MONITOR_INTERVAL));
      
    } catch (error) {
      log(`❌ Error checking slot ${lastSlot}: ${error.message}`);
    }
  }
  
  const actualDuration = ((Date.now() - startTime) / 1000).toFixed(2);
  
  log(`📊 Solana monitoring completed`);
  log(`📊 Duration: ${actualDuration} seconds`);
  log(`📊 Slots scanned: ${slotsScanned}`);
  log(`📊 Total detections: ${detections.length}`);
  log(`📊 Mode: Monitor only - no auto-buy`);
  
  return {
    success: true,
    chain: 'SOL',
    monitoring: {
      address,
      startTime: new Date(startTime).toISOString(),
      endTime: new Date().toISOString(),
      duration: monitorDuration,
      actualDuration,
      slotsScanned,
      detections
    }
  };
}

async function checkTransaction(tx, targetAddress, connection) {
  try {
    const transaction = await connection.getTransaction(tx.transaction.signature);
    
    if (transaction && transaction.meta && transaction.meta.preBalances && transaction.meta.postBalances) {
      const preBalances = transaction.meta.preBalances;
      const postBalances = transaction.meta.postBalances;
      
      // Find sender's balance
      const senderBalance = preBalances.find(b => b.address === targetAddress);
      
      if (senderBalance) {
        // Check if balance decreased (token transfer out)
        for (const account of postBalances) {
          if (account.address !== targetAddress) {
            // Check for new token in this account
            const preBalance = preBalances.find(b => b.address === account.address);
            
            if (preBalance && preBalance.tokenAmounts && account.tokenAmounts) {
              for (const tokenAmount of account.tokenAmounts) {
                // Find if this is a new token (not in sender's preBalance)
                const preToken = preBalance.tokenAmounts.find(t => t.mint === tokenAmount.mint);
                
                if (!preToken && tokenAmount.uiTokenAmount && tokenAmount.uiTokenAmount.amount > 0) {
                  // New token received by target address
                  log(`💰 New token detected!`);
                  
                  const tokenInfo = await getTokenInfo(tokenAmount.mint);
                  
                  return {
                    signature: tx.transaction.signature,
                    from: targetAddress,
                    to: account.address,
                    tokenMint: tokenAmount.mint,
                    tokenSymbol: tokenInfo.symbol,
                    amount: tokenAmount.uiTokenAmount.amount,
                    decimals: tokenAmount.uiTokenAmount.decimals || 9
                  };
                }
              }
            }
          }
        }
      }
    }
    
    return null;
  } catch (error) {
    return null;
  }
}

async function getTokenInfo(mintAddress) {
  try {
    const accountInfo = await connection.getAccountInfo(mintAddress);
    if (accountInfo && accountInfo.data) {
      const data = accountInfo.data;
      
      // Try to parse token name and symbol
      // Standard Solana Token Account layout:
      // - 32 bytes: padding
      - 4 bytes: mint authority
      - 4 bytes: freeze authority
      - 1 byte: decimals
      - 1 byte: reserved
      - 1 byte: state
      - 32 bytes: name
      // ... (more fields)
      
      if (data.length > 44) {
        const decimals = data[44];
        const nameLength = data[45];
        const symbolLength = data[46];
        
        let name = 'Unknown';
        let symbol = 'UNKNOWN';
        
        if (nameLength > 0 && nameLength <= 32) {
          const nameBytes = data.slice(52, 52 + nameLength);
          name = nameBytes.toString('utf8').replace(/\0/g, '');
        }
        
        if (symbolLength > 0 && symbolLength <= 10) {
          const symbolBytes = data.slice(52 + nameLength, 52 + nameLength + symbolLength);
          symbol = symbolBytes.toString('utf8').replace(/\0/g, '');
        }
        
        return { name, symbol, decimals };
      }
    }
  } catch (error) {
    log(`❌ Error getting token info: ${error.message}`);
  }
  
  return { name: 'Unknown', symbol: 'UNKNOWN', decimals: 9 };
}

module.exports = { monitorSOL };

if (require.main === module) {
  const action = process.argv[2] || 'monitor';
  const address = process.argv[3];
  const chain = process.argv[4] || 'SOL';
  const duration = process.argv[5] ? parseInt(process.argv[5]) : undefined;
  
  monitorSOL({ address, chain, duration }).then(result => {
    console.log(JSON.stringify(result, null, 2));
  }).catch(error => {
    console.error('Error:', error);
    process.exit(1);
  });
}
