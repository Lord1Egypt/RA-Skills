#!/usr/bin/env node
/**
 * Mint USDe on Tempo via Enshrined Exchange
 * 
 * Contract: 0x20C0000000000000000000000000000000000001 (AlphaUSD/USDe on Tempo)
 * RPC: https://rpc.moderato.tempo.xyz
 * 
 * Usage:
 *   PRIVATE_KEY=0x... node mint_usde.js --amount 100 --action mint
 *   PRIVATE_KEY=0x... node mint_usde.js --amount 100 --action redeem
 */

const { ethers } = require('ethers');
const args = require('minimist')(process.argv.slice(2));

const RPC = 'https://rpc.moderato.tempo.xyz';
const USDE_TOKEN = '0x20C0000000000000000000000000000000000001';  // USDe on Tempo
const USDC_TOKEN = '0x20C0000000000000000000000000000000000000'; // USDC on Tempo

// USDe contract ABI (simplified for mint/redeem)
const USDE_ABI = [
    'function mint(address to, uint256 amount) returns (bool)',
    'function redeem(address to, uint256 amount) returns (bool)',
    'function balanceOf(address account) returns (uint256)',
    'function transfer(address to, uint256 amount) returns (bool)',
    'function approve(address spender, uint256 amount) returns (bool)',
    'function allowance(address owner, address spender) returns (uint256)'
];

async function main() {
    const privateKey = process.env.PRIVATE_KEY;
    const amount = args.amount || 100; // Default 100 USDe
    const action = args.action || 'mint'; // mint or redeem
    
    if (!privateKey) {
        console.log('❌ PRIVATE_KEY not set');
        console.log('Usage: PRIVATE_KEY=0x... node mint_usde.js --amount 100 --action mint');
        process.exit(1);
    }
    
    const provider = new ethers.JsonRpcProvider(RPC);
    const wallet = new ethers.Wallet(privateKey, provider);
    
    console.log('🔷 ENSHRIINED.EXCHANGE - Mint/Redeem USDe');
    console.log('═══════════════════════════════════════════');
    console.log(`📝 Action: ${action.toUpperCase()}`);
    console.log(`💰 Amount: ${amount} USDe`);
    console.log(`👛 Wallet: ${wallet.address}`);
    console.log('');
    
    try {
        // Get token contract
        const usdeContract = new ethers.Contract(USDE_TOKEN, USDE_ABI, wallet);
        
        if (action === 'mint') {
            // For minting, you need to have USDC and approve
            const amountWei = ethers.parseUnits(amount.toString(), 18);
            
            console.log('📋 Step 1: Approve USDC for minting...');
            const usdcContract = new ethers.Contract(USDC_TOKEN, USDE_ABI, wallet);
            
            // Check USDC balance
            const usdcBalance = await usdcContract.balanceOf(wallet.address);
            console.log(`💵 USDC Balance: ${ethers.formatUnits(usdcBalance, 18)}`);
            
            if (usdcBalance < amountWei) {
                console.log('❌ Insufficient USDC balance for minting');
                process.exit(1);
            }
            
            // Approve
            const approveTx = await usdcContract.approve(USDE_TOKEN, amountWei);
            await approveTx.wait();
            console.log('✅ USDC Approved!');
            
            console.log('📋 Step 2: Mint USDe...');
            const mintTx = await usdeContract.mint(wallet.address, amountWei);
            const receipt = await mintTx.wait();
            
            console.log('');
            console.log('✅ MINT SUCCESSFUL!');
            console.log(`📜 TX: https:// explorer.tempo.xyz/tx/${mintTx.hash}`);
            
        } else if (action === 'redeem') {
            // Redeem USDe for USDC
            const amountWei = ethers.parseUnits(amount.toString(), 18);
            
            console.log('📋 Checking USDe balance...');
            const usdeBalance = await usdeContract.balanceOf(wallet.address);
            console.log(`💵 USDe Balance: ${ethers.formatUnits(usdeBalance, 18)}`);
            
            if (usdeBalance < amountWei) {
                console.log('❌ Insufficient USDe balance for redeeming');
                process.exit(1);
            }
            
            console.log('📋 Redeeming USDe...');
            const redeemTx = await usdeContract.redeem(wallet.address, amountWei);
            const receipt = await redeemTx.wait();
            
            console.log('');
            console.log('✅ REDEEM SUCCESSFUL!');
            console.log(`📜 TX: https://explorer.tempo.xyz/tx/${redeemTx.hash}`);
        }
        
        // Check final balances
        console.log('');
        console.log('📊 Final Balances:');
        const finalUsdc = await new ethers.Contract(USDC_TOKEN, USDE_ABI, wallet).balanceOf(wallet.address);
        const finalUsde = await usdeContract.balanceOf(wallet.address);
        console.log(`   USDC: ${ethers.formatUnits(finalUsdc, 18)}`);
        console.log(`   USDe: ${ethers.formatUnits(finalUsde, 18)}`);
        
    } catch (err) {
        console.log('❌ Error:', err.message || err);
    }
}

main();
