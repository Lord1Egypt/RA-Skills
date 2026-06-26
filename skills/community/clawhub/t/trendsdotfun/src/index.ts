#!/usr/bin/env node

import { Connection, Keypair, LAMPORTS_PER_SOL } from "@solana/web3.js";
import { Command } from "commander";
import * as fs from "fs";
import * as path from "path";
import bs58 from "bs58";
import { login } from "./auth.js";
import { getUploadUrl, uploadImage, getMintAddress, uploadContent } from "./api.js";
import { createPool } from "./pool.js";

// 默认配置
const DEFAULT_RPC_ENDPOINT = "https://api.mainnet-beta.solana.com";
const DEFAULT_POOL_CONFIG = "7UQpAg2GfvwnBhuNAF5g9ujjDmkq7rPnF7Xogs4xE9AA";
const MIN_SOL_BALANCE = 0.02;

// 参数长度限制
const MAX_NAME_LENGTH = 32;
const MAX_SYMBOL_LENGTH = 32;
const MAX_DESC_LENGTH = 150;

/**
 * 从 ~/.config/solana/id.json 加载 Solana keypair
 */
function loadKeypair(): Keypair {
    const idPath = path.join(
        process.env.HOME || process.env.USERPROFILE || "~",
        ".config",
        "solana",
        "id.json"
    );

    if (!fs.existsSync(idPath)) {
        throw new Error(`密钥文件不存在: ${idPath}`);
    }

    const raw = fs.readFileSync(idPath, "utf-8");
    const secretKey = new Uint8Array(JSON.parse(raw));
    return Keypair.fromSecretKey(secretKey);
}

const program = new Command();

program
    .name("trends-coin-create")
    .description("在 trends.fun 上创建 coin 并部署 DBC 资金池")
    .requiredOption("--name <name>", "Token 名称")
    .requiredOption("--symbol <symbol>", "Token 符号 (ticker)")
    .requiredOption("--imagePath <path>", "本地图片路径")
    .requiredOption("--mode <number>", "模式 (1=Profile, 2=Tweet)", parseInt)
    .option("--url <url>", "关联 URL（推文链接或个人主页）")
    .option("--desc <description>", "Token 描述", "")
    .option("--first-buy <sol>", "首次购买 SOL 数量", parseFloat, 0)
    .action(async (opts) => {
        try {
            // 参数长度校验（与前端一致）
            if (opts.name.length > MAX_NAME_LENGTH) {
                console.error(`❌ Token 名称过长: ${opts.name.length} 字符, 最大 ${MAX_NAME_LENGTH} 字符`);
                process.exit(1);
            }
            if (opts.symbol.length > MAX_SYMBOL_LENGTH) {
                console.error(`❌ Token 符号过长: ${opts.symbol.length} 字符, 最大 ${MAX_SYMBOL_LENGTH} 字符`);
                process.exit(1);
            }
            if (opts.desc && opts.desc.length > MAX_DESC_LENGTH) {
                console.error(`❌ Token 描述过长: ${opts.desc.length} 字符, 最大 ${MAX_DESC_LENGTH} 字符`);
                process.exit(1);
            }

            // 从环境变量读取可选配置
            const rpcUrl = process.env.SOLANA_RPC_URL || DEFAULT_RPC_ENDPOINT;
            const poolConfig = process.env.TRENDS_POOL_CONFIG || DEFAULT_POOL_CONFIG;

            // 1. 加载密钥对
            console.log("🔑 加载 Solana 密钥对...");
            const keypair = loadKeypair();
            console.log(`   地址: ${keypair.publicKey.toBase58()}`);

            // 1.5 检测 SOL 余额
            console.log("💰 检测 SOL 余额...");
            const connection = new Connection(rpcUrl, "confirmed");
            const balanceLamports = await connection.getBalance(keypair.publicKey);
            const balanceSol = balanceLamports / LAMPORTS_PER_SOL;
            console.log(`   余额: ${balanceSol} SOL`);

            if (balanceSol < MIN_SOL_BALANCE) {
                console.error(`\n❌ SOL 余额不足! 当前: ${balanceSol} SOL, 最低要求: ${MIN_SOL_BALANCE} SOL`);
                console.error(`   请先向地址 ${keypair.publicKey.toBase58()} 充值至少 ${MIN_SOL_BALANCE} SOL`);
                process.exit(1);
            }
            console.log(`✅ 余额充足 (>= ${MIN_SOL_BALANCE} SOL)`);

            // 2. SIWS 签名登录
            const token = await login(keypair);

            // 3. 获取 IPFS 上传 URL
            const imageName = path.basename(opts.imagePath);
            const { url: uploadUrl } = await getUploadUrl(token, imageName);

            // 4. 上传图片到 IPFS
            const imageUrl = await uploadImage(uploadUrl, opts.imagePath);

            // 5. 获取 mint 地址
            // const mintAddr = await getMintAddress(token);
            const mintKeypair = Keypair.generate();
            const mintAddr = mintKeypair.publicKey.toBase58();
            console.log(`✨ 生成新 Mint 地址: ${mintAddr}`);

            // 6. 上传 coin tick 内容
            const ipfsUri = await uploadContent(token, {
                mintAddr,
                ticker: opts.symbol,
                name: opts.name,
                imageUrl,
                description: opts.desc,
                mode: opts.mode,
                url: opts.url,
            });

            // 7. 创建 DBC 资金池
            const firstBuyLamports = opts.firstBuy > 0
                ? Math.floor(opts.firstBuy * LAMPORTS_PER_SOL)
                : 0;

            const { txHash } = await createPool({
                keypair,
                tokenName: opts.name,
                tokenSymbol: opts.symbol,
                uri: ipfsUri,
                mintKeypair: mintKeypair,
                firstBuyLamports,
                rpcUrl,
                poolConfig,
            });

            console.log("\n🎉 Coin 创建完成!");
            console.log("=".repeat(50));
            console.log(`  Token Name:   ${opts.name}`);
            console.log(`  Token Symbol: ${opts.symbol}`);
            console.log(`  Mint Address: ${mintAddr}`);
            console.log(`  IPFS URI:     ${ipfsUri}`);
            console.log(`  Image URL:    ${imageUrl}`);
            console.log(`  TX Hash:      ${txHash}`);
            console.log("=".repeat(50));
        } catch (err) {
            console.error("\n❌ 错误:", err);
            process.exit(1);
        }
    });

program.parse();
