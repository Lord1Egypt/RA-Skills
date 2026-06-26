import { Keypair } from "@solana/web3.js";
import nacl from "tweetnacl";
import bs58 from "bs58";

// SIWS message 格式模板
const DOMAIN = "trends.fun";
const URI = "https://trends.fun/login";
const VERSION = "1";
const CHAIN_ID = "mainnet-beta";
const STATEMENT = "Sign in to the app.";

/**
 * 生成随机 nonce
 */
function generateNonce(): string {
    return Math.floor(Math.random() * 100000000).toString();
}

/**
 * 构造 SIWS message
 */
function buildSiwsMessage(address: string): string {
    const nonce = generateNonce();
    const issuedAt = new Date().toISOString();

    // 按照 SIWS 标准格式构造 message
    const message = [
        `${DOMAIN} wants you to sign in with your Solana account:`,
        address,
        "",
        STATEMENT,
        "",
        `URI: ${URI}`,
        `Version: ${VERSION}`,
        `Chain ID: ${CHAIN_ID}`,
        `Nonce: ${nonce}`,
        `Issued At: ${issuedAt}`,
    ].join("\n");

    return message;
}

/**
 * 使用 keypair 签名 SIWS message 并调用 verify 接口获取 JWT token
 */
export async function login(keypair: Keypair): Promise<string> {
    const address = keypair.publicKey.toBase58();
    const message = buildSiwsMessage(address);

    // 使用 Ed25519 签名
    const messageBytes = new TextEncoder().encode(message);
    const signature = nacl.sign.detached(messageBytes, keypair.secretKey);
    const signatureBase58 = bs58.encode(signature);

    console.log("🔐 正在进行 SIWS 签名登录...");

    // 调用 verify 接口
    const resp = await fetch("https://api.trends.fun/v1/siws/verify", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Origin: "https://trends.fun",
            Referer: "https://trends.fun/",
        },
        body: JSON.stringify({
            message,
            signature: signatureBase58,
        }),
    });

    if (!resp.ok) {
        throw new Error(`SIWS verify 失败: ${resp.status} ${resp.statusText}`);
    }

    const result = (await resp.json()) as {
        status: string;
        data: {
            address: string;
            token_type: string;
            token: string;
            refresh_token: string;
        };
        error_code?: number;
        error_msg?: string;
    };
    if (result.status !== "success") {
        throw new Error(
            `SIWS verify 错误: ${result.error_msg || "未知错误"} (code: ${result.error_code})`
        );
    }

    console.log("✅ 登录成功，获取到 Bearer Token");
    return result.data.token;
}
