#!/usr/bin/env node
/**
 * Check Base Wallet Balance
 * Usage: node check-balance.js [ADDRESS]
 */

const { ethers } = require('ethers');

const RPC = 'https://mainnet.base.org';

async function main() {
    const address = process.argv[2] || process.env.WALLET_ADDRESS;
    
    if (!address) {
        console.log('Usage: node check-balance.js [ADDRESS]');
        console.log('Or set WALLET_ADDRESS environment variable');
        return;
    }
    
    const provider = new ethers.JsonRpcProvider(RPC);
    
    try {
        const balance = await provider.getBalance(address);
        const balanceEth = ethers.formatEther(balance);
        
        console.log('📊 Base Wallet Balance');
        console.log('─────────────────────');
        console.log(`Address: ${address}`);
        console.log(`Balance: ${balanceEth} ETH`);
        console.log(`RPC: ${RPC}`);
    } catch (err) {
        console.error('Error:', err.message);
    }
}

main();
