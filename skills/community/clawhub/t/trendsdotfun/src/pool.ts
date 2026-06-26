import {
    Connection,
    Keypair,
    PublicKey,
    sendAndConfirmTransaction,
    LAMPORTS_PER_SOL,
    Transaction,
} from "@solana/web3.js";
// import type BN from "bn.js"; // Disable static import to avoid type issues if d.ts fails

// 默认配置
const DEFAULT_RPC_ENDPOINT = "https://api.mainnet-beta.solana.com";
const DEFAULT_POOL_CONFIG = "7UQpAg2GfvwnBhuNAF5g9ujjDmkq7rPnF7Xogs4xE9AA";

/**
 * 使用 DBC SDK 创建资金池
 */
export async function createPool(params: {
    keypair: Keypair;
    tokenName: string;
    tokenSymbol: string;
    uri: string;
    mintKeypair: Keypair;
    firstBuyLamports?: number;
    rpcUrl?: string;
    poolConfig?: string;
}): Promise<{ txHash: string; mintAddress: string }> {
    console.log("🏊 正在创建 DBC 资金池...");

    // 动态导入 DBC SDK 和 bn.js
    const { PoolService } = await import(
        "@meteora-ag/dynamic-bonding-curve-sdk"
    );
    // @ts-ignore
    const BN = (await import("bn.js")).default || (await import("bn.js"));

    const rpcEndpoint = params.rpcUrl || DEFAULT_RPC_ENDPOINT;
    const poolConfigKey = new PublicKey(params.poolConfig || DEFAULT_POOL_CONFIG);

    const connection = new Connection(rpcEndpoint, "confirmed");
    const payer = params.keypair;
    const baseMint = params.mintKeypair;

    // 创建 PoolService client
    const poolService = new PoolService(connection, "confirmed");

    console.log(`  Pool Config: ${poolConfigKey.toBase58()}`);
    console.log(`  RPC: ${rpcEndpoint}`);
    console.log(`  Token Name: ${params.tokenName}`);
    console.log(`  Token Symbol: ${params.tokenSymbol}`);
    console.log(`  URI: ${params.uri}`);
    console.log(`  BaseMint: ${baseMint.publicKey.toBase58()}`);

    const firstBuyLamports = params.firstBuyLamports || 0;

    if (firstBuyLamports > 0) {
        // 创建池子 + 首次购买
        const { createPoolTx, swapBuyTx } = await poolService.createPoolWithFirstBuy({
            createPoolParam: {
                name: params.tokenName,
                symbol: params.tokenSymbol,
                uri: params.uri,
                payer: payer.publicKey,
                poolCreator: payer.publicKey,
                config: poolConfigKey,
                baseMint: baseMint.publicKey,
            },
            firstBuyParam: {
                buyer: payer.publicKey,
                buyAmount: new BN(firstBuyLamports),
                minimumAmountOut: new BN(0),
                referralTokenAccount: null,
            },
        });

        // 发送创建池子交易
        const poolTxHash = await sendAndConfirmTransaction(
            connection,
            createPoolTx,
            [payer, baseMint], // 需要 baseMint 签名 (初始化 mint)
            { commitment: "confirmed" }
        );
        console.log(`  创建池子交易: ${poolTxHash}`);

        // 发送首次购买交易
        if (swapBuyTx) {
            const buyTxHash = await sendAndConfirmTransaction(
                connection,
                swapBuyTx,
                [payer],
                { commitment: "confirmed" }
            );
            console.log(`  首次购买交易: ${buyTxHash}`);
        }

        console.log(`✅ 资金池创建成功!`);
        return { txHash: poolTxHash, mintAddress: baseMint.publicKey.toBase58() };
    } else {
        // 仅创建池子，不购买
        const tx = await poolService.createPool({
            name: params.tokenName,
            symbol: params.tokenSymbol,
            uri: params.uri,
            payer: payer.publicKey,
            poolCreator: payer.publicKey,
            config: poolConfigKey,
            baseMint: baseMint.publicKey,
        });

        const txHash = await sendAndConfirmTransaction(
            connection,
            tx,
            [payer, baseMint], // 需要 baseMint 签名
            { commitment: "confirmed" }
        );

        console.log(`✅ 资金池创建成功!`);
        console.log(`  交易哈希: ${txHash}`);
        return { txHash, mintAddress: baseMint.publicKey.toBase58() };
    }
}
