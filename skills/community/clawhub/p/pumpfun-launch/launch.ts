import dotenv from "dotenv";
import {
  Connection,
  Keypair,
  LAMPORTS_PER_SOL,
  PublicKey,
} from "@solana/web3.js";
import { AnchorProvider } from "@coral-xyz/anchor";
import NodeWallet from "@coral-xyz/anchor/dist/cjs/nodewallet";
import { PumpFunSDK } from "pumpdotfun-sdk";
import bs58 from "bs58";
import * as fs from "fs";
import * as path from "path";
import * as crypto from "crypto";
import * as readline from "readline";

dotenv.config({ path: path.join(import.meta.dir, ".env") });

// ── Helpers ──────────────────────────────────────────────

function parseArgs(): Record<string, string> {
  const args: Record<string, string> = {};
  const argv = process.argv.slice(2);
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith("--")) {
      const key = argv[i].slice(2);
      if (key === "dry-run") {
        args["dryRun"] = "true";
      } else if (i + 1 < argv.length && !argv[i + 1].startsWith("--")) {
        args[key] = argv[i + 1];
        i++;
      } else {
        args[key] = "true";
      }
    }
  }
  return args;
}

function prompt(question: string): Promise<string> {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise((resolve) => rl.question(question, (a) => { rl.close(); resolve(a); }));
}

// ── Wallet Management ────────────────────────────────────

function encryptKey(privateKey: Uint8Array, password: string): string {
  const salt = crypto.randomBytes(16);
  const key = crypto.scryptSync(password, salt, 32);
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv("aes-256-cbc", key, iv);
  const encrypted = Buffer.concat([cipher.update(privateKey), cipher.final()]);
  return JSON.stringify({
    salt: salt.toString("hex"),
    iv: iv.toString("hex"),
    data: encrypted.toString("hex"),
  });
}

function decryptKey(encryptedJson: string, password: string): Uint8Array {
  const { salt, iv, data } = JSON.parse(encryptedJson);
  const key = crypto.scryptSync(password, Buffer.from(salt, "hex"), 32);
  const decipher = crypto.createDecipheriv("aes-256-cbc", key, Buffer.from(iv, "hex"));
  return new Uint8Array(Buffer.concat([decipher.update(Buffer.from(data, "hex")), decipher.final()]));
}

async function loadWallet(): Promise<Keypair> {
  // 1. Environment variable
  if (process.env.WALLET_PRIVATE_KEY) {
    try {
      return Keypair.fromSecretKey(bs58.decode(process.env.WALLET_PRIVATE_KEY));
    } catch {
      throw new Error("Invalid WALLET_PRIVATE_KEY in .env");
    }
  }

  // 2. Encrypted file
  const walletPath = path.join(import.meta.dir, ".wallet.key");
  if (fs.existsSync(walletPath)) {
    const password = await prompt("Wallet password: ");
    try {
      const raw = fs.readFileSync(walletPath, "utf-8");
      return Keypair.fromSecretKey(decryptKey(raw, password));
    } catch {
      throw new Error("Wrong password or corrupted wallet file");
    }
  }

  // 3. Generate new wallet
  console.log("No wallet found. Generating a new one...");
  const kp = Keypair.generate();
  const password = await prompt("Set a password to encrypt your wallet: ");
  fs.writeFileSync(walletPath, encryptKey(kp.secretKey, password));
  console.log(`Wallet saved to .wallet.key`);
  console.log(`Public key: ${kp.publicKey.toBase58()}`);
  console.log(`Fund this wallet with SOL before launching tokens.`);
  return kp;
}

// ── Provider Setup ───────────────────────────────────────

function getProvider(): AnchorProvider {
  const rpcUrl = process.env.HELIUS_RPC_URL;
  if (!rpcUrl) throw new Error("Set HELIUS_RPC_URL in .env");
  const connection = new Connection(rpcUrl, "confirmed");
  const wallet = new NodeWallet(Keypair.generate());
  return new AnchorProvider(connection, wallet, { commitment: "confirmed" });
}

// ── Image Loading ────────────────────────────────────────

async function loadImage(imagePath: string): Promise<Blob> {
  if (imagePath.startsWith("http://") || imagePath.startsWith("https://")) {
    const res = await fetch(imagePath);
    if (!res.ok) throw new Error(`Failed to fetch image: ${res.status}`);
    return await res.blob();
  }
  const resolved = path.resolve(imagePath);
  if (!fs.existsSync(resolved)) throw new Error(`Image not found: ${resolved}`);
  const buffer = fs.readFileSync(resolved);
  const ext = path.extname(resolved).toLowerCase();
  const mime = ext === ".png" ? "image/png" : ext === ".gif" ? "image/gif" : "image/jpeg";
  return new Blob([buffer], { type: mime });
}

// ── Token Status Check ───────────────────────────────────

async function checkStatus(mintAddress: string) {
  const provider = getProvider();
  const sdk = new PumpFunSDK(provider);

  console.log(`\nChecking token: ${mintAddress}`);
  const mint = new PublicKey(mintAddress);
  const bondingCurve = await sdk.getBondingCurveAccount(mint);

  if (!bondingCurve) {
    console.log("❌ No bonding curve found — token may not exist on pump.fun");
    return;
  }

  console.log("✅ Token found on pump.fun");
  console.log(`   Virtual SOL reserves: ${Number(bondingCurve.virtualSolReserves) / LAMPORTS_PER_SOL} SOL`);
  console.log(`   Virtual token reserves: ${Number(bondingCurve.virtualTokenReserves) / 1e6}`);
  console.log(`   Real SOL reserves: ${Number(bondingCurve.realSolReserves) / LAMPORTS_PER_SOL} SOL`);
  console.log(`   Real token reserves: ${Number(bondingCurve.realTokenReserves) / 1e6}`);
  console.log(`   Complete (graduated): ${bondingCurve.complete}`);
  console.log(`   Link: https://pump.fun/${mintAddress}`);
}

// ── Token Launch ─────────────────────────────────────────

async function launch(args: Record<string, string>) {
  const { name, symbol, description, image, buy, slippage, dryRun } = args;
  const priorityFee = parseInt(args["priority-fee"] || "250000");

  if (!name || !symbol || !description || !image) {
    console.error("Missing required args: --name, --symbol, --description, --image");
    process.exit(1);
  }

  const buyAmountSol = parseFloat(buy || "0");
  const slippageBps = BigInt(parseInt(slippage || "500"));

  console.log("\n🚀 Pump.fun Token Launch");
  console.log("========================");
  console.log(`  Name:        ${name}`);
  console.log(`  Symbol:      ${symbol}`);
  console.log(`  Description: ${description}`);
  console.log(`  Image:       ${image}`);
  console.log(`  Buy amount:  ${buyAmountSol} SOL`);
  console.log(`  Slippage:    ${slippageBps} bps`);
  console.log(`  Priority:    ${priorityFee} micro-lamports`);
  console.log(`  Mode:        ${dryRun ? "🧪 DRY RUN" : "🔴 LIVE"}`);
  console.log();

  if (dryRun === "true") {
    console.log("✅ Dry run complete — parameters validated.");
    console.log("   Remove --dry-run to launch for real.");

    // Still validate image loads
    try {
      const blob = await loadImage(image);
      console.log(`   Image loaded: ${blob.size} bytes (${blob.type})`);
    } catch (e: any) {
      console.error(`   ❌ Image error: ${e.message}`);
    }
    return;
  }

  // Load wallet
  const wallet = await loadWallet();
  console.log(`Wallet: ${wallet.publicKey.toBase58()}`);

  // Check balance
  const provider = getProvider();
  const connection = provider.connection;
  const balance = await connection.getBalance(wallet.publicKey);
  console.log(`Balance: ${balance / LAMPORTS_PER_SOL} SOL`);

  if (balance < 0.02 * LAMPORTS_PER_SOL) {
    console.error("❌ Insufficient balance. Need at least 0.02 SOL for fees.");
    process.exit(1);
  }

  // Load image
  console.log("Uploading metadata to IPFS...");
  const imageBlob = await loadImage(image);

  // Create SDK and launch
  const sdk = new PumpFunSDK(provider);
  const mintKeypair = Keypair.generate();

  console.log(`Mint address: ${mintKeypair.publicKey.toBase58()}`);
  console.log("Sending transaction...");

  try {
    const result = await sdk.createAndBuy(
      wallet,
      mintKeypair,
      {
        name,
        symbol,
        description,
        file: imageBlob,
      },
      BigInt(Math.floor(buyAmountSol * LAMPORTS_PER_SOL)),
      slippageBps,
      { unitLimit: 250000, unitPrice: priorityFee }
    );

    if (result.success) {
      console.log("\n🎉 TOKEN LAUNCHED SUCCESSFULLY!");
      console.log(`   Mint:      ${mintKeypair.publicKey.toBase58()}`);
      console.log(`   Signature: ${result.signature}`);
      console.log(`   Link:      https://pump.fun/${mintKeypair.publicKey.toBase58()}`);
      console.log(`   Solscan:   https://solscan.io/tx/${result.signature}`);
    } else {
      console.error("\n❌ Launch failed:", result.error);
    }
  } catch (e: any) {
    console.error("\n❌ Error:", e.message);
    if (e.logs) console.error("Logs:", e.logs);
  }
}

// ── Wallet Setup (standalone) ────────────────────────────

async function setupWallet() {
  const walletPath = path.join(import.meta.dir, ".wallet.key");
  
  if (fs.existsSync(walletPath)) {
    console.log("Wallet already exists. Loading...");
    const password = await prompt("Wallet password: ");
    try {
      const raw = fs.readFileSync(walletPath, "utf-8");
      const kp = Keypair.fromSecretKey(decryptKey(raw, password));
      console.log(`\n✅ Wallet loaded`);
      console.log(`   Address: ${kp.publicKey.toBase58()}`);
      
      // Check balance
      const rpcUrl = process.env.HELIUS_RPC_URL;
      if (rpcUrl) {
        const connection = new Connection(rpcUrl, "confirmed");
        const balance = await connection.getBalance(kp.publicKey);
        console.log(`   Balance: ${balance / LAMPORTS_PER_SOL} SOL`);
      }
      return;
    } catch {
      throw new Error("Wrong password or corrupted wallet file");
    }
  }

  console.log("🔑 Generating new Solana wallet...\n");
  const kp = Keypair.generate();
  const password = await prompt("Set a password to encrypt your wallet: ");
  if (!password) {
    console.error("❌ Password required.");
    process.exit(1);
  }
  const confirm = await prompt("Confirm password: ");
  if (password !== confirm) {
    console.error("❌ Passwords don't match.");
    process.exit(1);
  }
  
  fs.writeFileSync(walletPath, encryptKey(kp.secretKey, password));
  
  console.log(`\n✅ Wallet created and encrypted`);
  console.log(`   Address: ${kp.publicKey.toBase58()}`);
  console.log(`   Saved to: .wallet.key (AES-256 encrypted)`);
  console.log(`\n⚡ Send SOL to this address to start launching tokens.`);
  console.log(`   Minimum ~0.02 SOL for gas, plus whatever you want for initial buys.`);
}

// ── Main ─────────────────────────────────────────────────

const args = parseArgs();

if (args.wallet || args.setup) {
  await setupWallet();
} else if (args.status) {
  await checkStatus(args.status);
} else {
  await launch(args);
}
