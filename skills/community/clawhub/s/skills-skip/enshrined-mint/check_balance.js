#!/usr/bin/env node
/**
 * Check USDe/USDC Balance on Tempo
 */

const { ethers } = require('ethers');

const RPC = 'https://rpc.moderato.tempo.xyz';
const USDE_TOKEN = '0x20C0000000000000000000000000000000000001';
const USDC_TOKEN = '0x20C0000000000000000000000000000000000000';

const ABI = [
    'function balanceOf(address account) returns (uint256)'
];

async function main() {
    const privateKey = process.env.PRIVATE_KEY;
    
    if (!privateKey) {
        console.log('❌ PRIVATE_KEY not set');
        process.exit(1);
    }
    
    const provider = new ethers.JsonRpcProvider(RPC);
    const wallet = new ethers.Wallet(privateKey, provider);
    
    console.log('🔷 TEMPO WALLET BALANCE');
    console.log('═══════════════════════════════');
    console.log(`👛 Address: ${wallet.address}`);
    console.log('');
    
    try {
        // USDC Balance
        const usdcBal = await provider.call({
            to: USDC_TOKEN,
            data: '0x70a08231000000000000000000000000' + wallet.address.slice(2)
        });
        console.log(`💵 USDC: ${ethers.formatUnits(usdcBal, 18)}`);
        
        // USDe Balance
        const usdeBal = await provider.call({
            to: USDE_TOKEN,
            data: '0x70a08231000000000000000000000000' + wallet.address.slice(2)
        });
        console.log(`💵 USDe: ${ethers.formatUnits(usdeBal, 18)}`);
        
    } catch (err) {
        console.log('❌ Error:', err.message);
    }
}

main();
