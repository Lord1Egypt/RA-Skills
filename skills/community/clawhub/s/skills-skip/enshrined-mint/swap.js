#!/usr/bin/env node
/**
 * Swap Stablecoins on Tempo via Enshrined Exchange
 * 
 * Exchange Contract: 0xdec0000000000000000000000000000000000000
 * RPC: https://rpc.moderato.tempo.xyz
 * 
 * Usage:
 *   PRIVATE_KEY=0x... node swap.js --amount 100 --from USDC --to USDe
 */

const { ethers } = require('ethers');
const args = require('minimist')(process.argv.slice(2));

const RPC = 'https://rpc.moderato.tempo.xyz';
const EXCHANGE = '0xdec0000000000000000000000000000000000000';

// Token addresses on Tempo
const TOKENS = {
    USDC: '0x20C0000000000000000000000000000000000000',
    USDe: '0x20C0000000000000000000000000000000000001',
    pathUSD: '0x20C0000000000000000000000000000000000002'
};

const EXCHANGE_ABI = [
    'function swapExactAmountIn(address tokenIn, address tokenOut, uint128 amount, uint128 minAmountOut) returns (uint128)',
    'function swapExactAmountOut(address tokenIn, address tokenOut, uint128 amount, uint128 maxAmountIn) returns (uint128)',
    'function getBalance(address user, address token) returns (uint256)',
    'function getOrderBookDepth(address tokenIn, address tokenOut) returns (uint256)'
];

async function main() {
    const privateKey = process.env.PRIVATE_KEY;
    const amount = args.amount || 100;
    const fromToken = (args.from || 'USDC').toUpperCase();
    const toToken = (args.to || 'USDe').toUpperCase();
    
    if (!privateKey) {
        console.log('❌ PRIVATE_KEY not set');
        console.log('Usage: PRIVATE_KEY=0x... node swap.js --amount 100 --from USDC --to USDe');
        process.exit(1);
    }
    
    if (!TOKENS[fromToken] || !TOKENS[toToken]) {
        console.log('❌ Invalid token. Available: USDC, USDe, pathUSD');
        process.exit(1);
    }
    
    const provider = new ethers.JsonRpcProvider(RPC);
    const wallet = new ethers.Wallet(privateKey, provider);
    
    console.log('🔷 ENSHRIINED.EXCHANGE - Swap');
    console.log('═══════════════════════════════════════════');
    console.log(`💱 Swap: ${amount} ${fromToken} → ${toToken}`);
    console.log(`👛 Wallet: ${wallet.address}`);
    console.log('');
    
    try {
        const exchange = new ethers.Contract(EXCHANGE, EXCHANGE_ABI, wallet);
        const tokenIn = TOKENS[fromToken];
        const tokenOut = TOKENS[toToken];
        const amountWei = ethers.parseUnits(amount.toString(), 6); // Stablecoins 6 decimals
        
        // Check balances
        const balanceIn = await exchange.getBalance(wallet.address, tokenIn);
        console.log(`${fromToken} Balance: ${ethers.formatUnits(balanceIn, 6)}`);
        
        if (balanceIn < amountWei) {
            console.log(`❌ Insufficient ${fromToken} balance`);
            process.exit(1);
        }
        
        // Approve
        const tokenContract = new ethers.Contract(tokenIn, [
            'function approve(address spender, uint256 amount) returns (bool)'
        ], wallet);
        
        console.log(`📋 Approving ${fromToken}...`);
        const approveTx = await tokenContract.approve(EXCHANGE, amountWei);
        await approveTx.wait();
        console.log('✅ Approved!');
        
        // Swap
        console.log(`💱 Swapping ${amount} ${fromToken} → ${toToken}...`);
        const swapTx = await exchange.swapExactAmountIn(tokenIn, tokenOut, amountWei, 0);
        const receipt = await swapTx.wait();
        
        console.log('');
        console.log('✅ SWAP SUCCESSFUL!');
        console.log(`📜 TX: https://explorer.tempo.xyz/tx/${swapTx.hash}`);
        
        // Final balance
        const balanceOut = await exchange.getBalance(wallet.address, tokenOut);
        console.log(`${toToken} Balance: ${ethers.formatUnits(balanceOut, 6)}`);
        
    } catch (err) {
        console.log('❌ Error:', err.message || err);
    }
}

main();
