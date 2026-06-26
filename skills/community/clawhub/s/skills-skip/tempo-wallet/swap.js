const { ethers } = require('ethers');

const RPC = 'https://rpc.moderato.tempo.xyz';
const EXCHANGE = '0xdec0000000000000000000000000000000000000';
const USDC = '0x20C0000000000000000000000000000000000000';
const PATHUSD = '0x20C0000000000000000000000000000000000002';

const EXCHANGE_ABI = [
    'function swapExactAmountIn(address tokenIn, address tokenOut, uint128 amount, uint128 minAmountOut) returns (uint128)'
];

const TOKEN_ABI = [
    'function balanceOf(address) view returns (uint256)',
    'function approve(address, uint256) returns (bool)'
];

async function main() {
    const PRIVATE_KEY = '0x552cc8396e0603b4d9afb7ae0c5d21e9265fbda5401c41efb0a5e593435b717f';
    const provider = new ethers.JsonRpcProvider(RPC);
    const wallet = new ethers.Wallet(PRIVATE_KEY, provider);
    
    console.log('🔄 Swapping USDC → pathUSD');
    console.log('Wallet:', wallet.address);
    
    try {
        const amount = ethers.parseUnits('0.1', 6);
        
        const usdc = new ethers.Contract(USDC, TOKEN_ABI, provider);
        const balance = await usdc.balanceOf(wallet.address);
        console.log('USDC Balance:', ethers.formatUnits(balance, 6));
        
        if (balance < amount) {
            console.log('❌ Insufficient USDC');
            return;
        }
        
        console.log('📋 Approving...');
        const approveTx = await usdc.connect(wallet).approve(EXCHANGE, amount);
        await approveTx.wait();
        console.log('✅ Approved!');
        
        console.log('💱 Swapping...');
        const exchange = new ethers.Contract(EXCHANGE, EXCHANGE_ABI, wallet);
        const swapTx = await exchange.swapExactAmountIn(USDC, PATHUSD, amount, 0);
        const receipt = await swapTx.wait();
        
        console.log('✅ SWAPPED!');
        console.log('TX:', receipt.hash);
        
    } catch (e) {
        console.log('❌ Error:', e.message);
    }
}

main();
