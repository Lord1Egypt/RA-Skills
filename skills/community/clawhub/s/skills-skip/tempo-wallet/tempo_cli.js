#!/usr/bin/env node
/**
 * Tempo Wallet CLI
 * 
 * Complete wallet operations: send, receive, swap, check balance
 */

const { ethers } = require('ethers');
const args = require('minimist')(process.argv.slice(2));

const RPC = 'https://rpc.moderato.tempo.xyz';
const EXCHANGE = '0xdec0000000000000000000000000000000000000';

const TOKENS = {
    USDC:    '0x20C0000000000000000000000000000000000000',
    USDe:    '0x20C0000000000000000000000000000000000001',
    pathUSD: '0x20C0000000000000000000000000000000000002'
};

const TOKEN_ABI = [
    'function balanceOf(address) view returns (uint256)',
    'function transfer(address, uint256) returns (bool)',
    'function approve(address, uint256) returns (bool)'
];

const EXCHANGE_ABI = [
    'function swapExactAmountIn(address, address, uint128, uint128) returns (uint128)'
];

async function main() {
    const privateKey = process.env.PRIVATE_KEY;
    const action = args.action || 'help';
    
    if (!privateKey && action !== 'help') {
        console.log('❌ PRIVATE_KEY not set');
        console.log('Usage: PRIVATE_KEY=0x... node tempo_cli.js --action <command>');
        process.exit(1);
    }
    
    const provider = new ethers.JsonRpcProvider(RPC);
    const wallet = privateKey ? new ethers.Wallet(privateKey, provider) : null;
    
    console.log('🔷 TEMPO WALLET CLI');
    console.log('══════════════════════════════\n');
    
    switch (action) {
        case 'balance':
            await checkBalance(wallet);
            break;
        case 'send':
            await sendToken(wallet, args.amount, args.token || 'USDC', args.to);
            break;
        case 'swap':
            await swapToken(wallet, args.from, args.to, args.amount);
            break;
        case 'receive':
            console.log(`📥 Receive Address:\n   ${wallet.address}\n`);
            break;
        case 'help':
        default:
            showHelp();
    }
}

async function checkBalance(wallet) {
    console.log(`👛 Address: ${wallet.address}\n`);
    
    for (const [symbol, addr] of Object.entries(TOKENS)) {
        try {
            const token = new ethers.Contract(addr, TOKEN_ABI, provider);
            const balance = await token.balanceOf(wallet.address);
            console.log(`💰 ${symbol}: ${ethers.formatUnits(balance, 6)}`);
        } catch (e) {
            console.log(`💰 ${symbol}: Error`);
        }
    }
}

async function sendToken(wallet, amount, tokenSymbol, to) {
    if (!amount || !to) {
        console.log('❌ Missing --amount or --to');
        console.log('Usage: --action send --amount 1 --token USDC --to 0x...');
        return;
    }
    
    const tokenAddr = TOKENS[tokenSymbol.toUpperCase()];
    if (!tokenAddr) {
        console.log(`❌ Unknown token: ${tokenSymbol}`);
        return;
    }
    
    console.log(`📤 Sending ${amount} ${tokenSymbol} to ${to}`);
    
    try {
        const token = new ethers.Contract(tokenAddr, TOKEN_ABI, wallet);
        const amountWei = ethers.parseUnits(amount.toString(), 6);
        
        const balance = await token.balanceOf(wallet.address);
        if (balance < amountWei) {
            console.log(`❌ Insufficient balance`);
            return;
        }
        
        const tx = await token.transfer(to, amountWei);
        console.log(`⏳ TX: ${tx.hash}`);
        await tx.wait();
        
        console.log(`✅ Sent!`);
    } catch (e) {
        console.log(`❌ Error: ${e.message}`);
    }
}

async function swapToken(wallet, fromSymbol, toSymbol, amount) {
    if (!fromSymbol || !toSymbol || !amount) {
        console.log('❌ Missing --from, --to, or --amount');
        console.log('Usage: --action swap --from USDC --to USDe --amount 100');
        return;
    }
    
    const fromAddr = TOKENS[fromSymbol.toUpperCase()];
    const toAddr = TOKENS[toSymbol.toUpperCase()];
    
    console.log(`💱 Swapping ${amount} ${fromSymbol} → ${toSymbol}`);
    
    try {
        const exchange = new ethers.Contract(EXCHANGE, EXCHANGE_ABI, wallet);
        const fromToken = new ethers.Contract(fromAddr, TOKEN_ABI, wallet);
        
        const amountWei = ethers.parseUnits(amount.toString(), 6);
        
        await fromToken.approve(EXCHANGE, amountWei);
        const tx = await exchange.swapExactAmountIn(fromAddr, toAddr, amountWei, 0);
        await tx.wait();
        
        console.log(`✅ Swapped!`);
    } catch (e) {
        console.log(`❌ Error: ${e.message}`);
    }
}

function showHelp() {
    console.log(`
🔷 TEMPO WALLET CLI

Usage:
  PRIVATE_KEY=0x... node tempo_cli.js --action <command> [options]

Commands:
  balance    Check all token balances
  send      Send tokens
  swap      Swap on Enshrined Exchange
  receive   Show receive address
  help      Show this help

Examples:
  # Check balance
  PRIVATE_KEY=0x... node tempo_cli.js --action balance

  # Send 1 USDC
  PRIVATE_KEY=0x... node tempo_cli.js --action send --amount 1 --to 0x...

  # Swap USDC → USDe
  PRIVATE_KEY=0x... node tempo_cli.js --action swap --from USDC --to USDe --amount 100

Tokens: USDC, USDe, pathUSD
`);
}

main().catch(console.error);
