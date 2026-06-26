#!/usr/bin/env node
const fs = require('fs');
const os = require('os');
const path = require('path');

const SKILL_ROOT = path.resolve(__dirname, '..');
const INSTALL_HINT = `Install runtime deps with: cd ${SKILL_ROOT} && npm install`;

function requireOrExplain(name) {
  try {
    return require(name);
  } catch (err) {
    console.error(`Missing dependency: ${name}`);
    console.error(INSTALL_HINT);
    process.exit(1);
  }
}

const nacl = requireOrExplain('tweetnacl');
const bs58mod = requireOrExplain('bs58');
const bs58 = bs58mod.default || bs58mod;
const web3 = requireOrExplain('@solana/web3.js');
const splToken = requireOrExplain('@solana/spl-token');
const { Keypair, Connection, LAMPORTS_PER_SOL, PublicKey, Transaction, TransactionInstruction, sendAndConfirmTransaction } = web3;
const { getAssociatedTokenAddress, TOKEN_PROGRAM_ID } = splToken;

const RPC_URL = process.env.SOLANA_RPC_URL || 'https://api.devnet.solana.com';
const ROCKPAPERCLAW_PROGRAM_ID = 'awaejXXFTty2WaXrXtSRi23BmtW9UJknjQwmMJps9Tg';
const ROCKPAPERCLAW_USDC_MINT = '4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU';
const ROCKPAPERCLAW_DEPOSIT_DISCRIMINATOR = Buffer.from([242, 35, 198, 137, 82, 225, 242, 182]);

function inferNetwork(rpcUrl) {
  const url = String(rpcUrl || '').toLowerCase();
  if (url.includes('devnet')) return 'devnet';
  if (url.includes('testnet')) return 'testnet';
  if (url.includes('mainnet')) return 'mainnet-beta';
  return 'custom';
}

function expandUserPath(value) {
  if (!value) return value;
  if (value === '~') return os.homedir();
  if (value.startsWith('~/')) return path.join(os.homedir(), value.slice(2));
  return value;
}

function defaultGeneratedKeypairPath() {
  const network = inferNetwork(RPC_URL);
  return path.join(os.homedir(), '.openclaw', 'wallets', `solana-${network}.json`);
}

function candidateKeypairPaths() {
  const home = os.homedir();
  const envPath = expandUserPath(process.env.SOLANA_WALLET_KEYPAIR);
  return [
    envPath,
    path.join(home, '.config/solana/id.json'),
    path.join(home, '.solana/id.json'),
    path.join(home, '.openclaw/wallets/solana-devnet.json'),
    path.join(home, '.openclaw/wallets/solana.json'),
  ].filter(Boolean);
}

function resolveKeypairPath() {
  for (const p of candidateKeypairPaths()) {
    try {
      if (fs.existsSync(p)) return p;
    } catch {}
  }
  console.error('No Solana keypair file found.');
  console.error('Set SOLANA_WALLET_KEYPAIR to a 64-byte keypair JSON file, create one with `create-wallet`, or place one in a common default path such as ~/.config/solana/id.json');
  process.exit(1);
}

function ensureParentDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true, mode: 0o700 });
  try { fs.chmodSync(path.dirname(filePath), 0o700); } catch {}
}

function writeKeypairFile(filePath, secretKeyArray) {
  ensureParentDir(filePath);
  fs.writeFileSync(filePath, JSON.stringify(secretKeyArray) + '\n', { mode: 0o600 });
  try { fs.chmodSync(filePath, 0o600); } catch {}
}

function createWallet(targetPath) {
  const overwrite = process.env.SOLANA_WALLET_OVERWRITE === '1';
  if (fs.existsSync(targetPath) && !overwrite) {
    throw new Error(`Refusing to overwrite existing keypair: ${targetPath}. Set SOLANA_WALLET_OVERWRITE=1 to replace it.`);
  }
  const kp = Keypair.generate();
  writeKeypairFile(targetPath, Array.from(kp.secretKey));
  return kp;
}

function loadKeypair(filePath) {
  const raw = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  if (!Array.isArray(raw) || raw.length !== 64) {
    throw new Error(`Invalid Solana keypair file: ${filePath}`);
  }
  return Keypair.fromSecretKey(Uint8Array.from(raw));
}

function decodeSignature(sigText) {
  try {
    return Buffer.from(sigText, 'base64');
  } catch {}
  try {
    return Buffer.from(bs58.decode(sigText));
  } catch {}
  throw new Error('Signature must be valid base64 or base58');
}

function parsePublicKey(label, value) {
  try {
    return new PublicKey(value);
  } catch {
    throw new Error(`Invalid ${label}: ${value}`);
  }
}

function encodeRockPaperClawDeposit(agentId, amount) {
  const agentIdBytes = Buffer.from(agentId, 'utf8');
  if (agentIdBytes.length === 0 || agentIdBytes.length > 36) {
    throw new Error('agentId must be between 1 and 36 UTF-8 bytes');
  }

  const amountBigInt = BigInt(amount);
  if (amountBigInt <= 0n) {
    throw new Error('Deposit amount must be a positive integer number of micro-USDC');
  }

  const lengthBytes = Buffer.alloc(4);
  lengthBytes.writeUInt32LE(agentIdBytes.length, 0);

  const amountBytes = Buffer.alloc(8);
  amountBytes.writeBigUInt64LE(amountBigInt, 0);

  return Buffer.concat([
    ROCKPAPERCLAW_DEPOSIT_DISCRIMINATOR,
    lengthBytes,
    agentIdBytes,
    amountBytes,
  ]);
}

function parseRockPaperClawDepositArgs(args) {
  const positional = [];
  const options = {};

  for (let index = 0; index < args.length; index += 1) {
    const value = args[index];

    if (value === '--execute') {
      options.execute = true;
      continue;
    }

    if (value === '--program-id' || value === '--usdc-mint' || value === '--commitment' || value === '--keypair') {
      const nextValue = args[index + 1];
      if (!nextValue) {
        throw new Error(`Missing value for ${value}`);
      }
      options[value.slice(2)] = nextValue;
      index += 1;
      continue;
    }

    positional.push(value);
  }

  if (positional.length < 2) {
    throw new Error('rockpaperclaw-deposit requires <agentId> <amountMicroUsdc>');
  }

  const agentId = positional[0];
  const amountText = positional[1];
  if (!/^\d+$/.test(amountText)) {
    throw new Error('Deposit amount must be an integer number of micro-USDC');
  }

  return {
    agentId,
    amount: amountText,
    programId: options['program-id'] || ROCKPAPERCLAW_PROGRAM_ID,
    usdcMint: options['usdc-mint'] || ROCKPAPERCLAW_USDC_MINT,
    keypair: expandUserPath(options.keypair || process.env.SOLANA_WALLET_KEYPAIR),
    commitment: options.commitment || 'confirmed',
    execute: options.execute === true,
  };
}

function resolveTransactionKeypairPath(explicitPath) {
  if (!explicitPath) {
    throw new Error('Fund-moving commands require an explicit keypair via --keypair or SOLANA_WALLET_KEYPAIR');
  }

  if (!fs.existsSync(explicitPath)) {
    throw new Error(`Keypair file not found: ${explicitPath}`);
  }

  return explicitPath;
}

async function getTokenBalanceOrThrow(connection, address) {
  try {
    return await connection.getTokenAccountBalance(address, 'confirmed');
  } catch {
    throw new Error(
      `No token account found at ${address.toBase58()}. ` +
      'Fund the wallet with canonical devnet USDC for the RockPaperClaw mint before depositing.'
    );
  }
}

function usage() {
  console.error(`Usage:
  solana_wallet.cjs create-wallet [keypairPath]
  solana_wallet.cjs address
  solana_wallet.cjs balance
  solana_wallet.cjs airdrop [solAmount]
  solana_wallet.cjs sign-message <message>
  solana_wallet.cjs verify-message <message> <signature>
  solana_wallet.cjs rockpaperclaw-deposit <agentId> <amountMicroUsdc> --keypair <path> [--program-id <programId>] [--usdc-mint <mint>] [--commitment <level>] [--execute]
`);
  process.exit(2);
}

async function main() {
  const [cmd, ...args] = process.argv.slice(2);
  if (!cmd) usage();

  const network = inferNetwork(RPC_URL);

  if (cmd === 'create-wallet') {
    const keypairPath = expandUserPath(args[0] || process.env.SOLANA_WALLET_KEYPAIR || defaultGeneratedKeypairPath());
    const kp = createWallet(keypairPath);
    console.log(JSON.stringify({
      network,
      rpcUrl: RPC_URL,
      address: kp.publicKey.toBase58(),
      keypairPath,
      created: true,
    }, null, 2));
    return;
  }

  const conn = new Connection(RPC_URL, 'confirmed');

  if (cmd === 'rockpaperclaw-deposit') {
    const parsed = parseRockPaperClawDepositArgs(args);
    const transactionKeypairPath = resolveTransactionKeypairPath(parsed.keypair);
    const txKeypair = loadKeypair(transactionKeypairPath);
    const programId = parsePublicKey('program id', parsed.programId);
    const usdcMint = parsePublicKey('USDC mint', parsed.usdcMint);
    const amountBigInt = BigInt(parsed.amount);
    const [configPda] = PublicKey.findProgramAddressSync([Buffer.from('config')], programId);
    const [vaultPda] = PublicKey.findProgramAddressSync([Buffer.from('vault'), usdcMint.toBuffer()], programId);
    const depositorTokenAccount = await getAssociatedTokenAddress(usdcMint, txKeypair.publicKey);
    const beforeBalance = await getTokenBalanceOrThrow(conn, depositorTokenAccount);
    const beforeAmount = BigInt(beforeBalance.value.amount);

    if (beforeAmount < amountBigInt) {
      throw new Error(
        `Insufficient USDC balance in ${depositorTokenAccount.toBase58()}: ` +
        `have ${beforeBalance.value.amount} micro-USDC, need ${parsed.amount}`
      );
    }

    const preview = {
      network,
      rpcUrl: RPC_URL,
      address: txKeypair.publicKey.toBase58(),
      keypairPath: transactionKeypairPath,
      agentId: parsed.agentId,
      amountMicroUsdc: parsed.amount,
      amountUsdc: Number(parsed.amount) / 1_000_000,
      expectedChips: Number(parsed.amount) / 10_000,
      programId: programId.toBase58(),
      usdcMint: usdcMint.toBase58(),
      configPda: configPda.toBase58(),
      vaultPda: vaultPda.toBase58(),
      depositorTokenAccount: depositorTokenAccount.toBase58(),
      tokenBalanceBefore: beforeBalance.value.amount,
      executionMode: parsed.execute ? 'execute' : 'preview',
      note: parsed.execute
        ? 'Executing deposit transaction.'
        : 'Preview only. Verify these values against rockpaperclaw get_deposit_info, then rerun with --execute to send funds.',
    };

    if (!parsed.execute) {
      console.log(JSON.stringify(preview, null, 2));
      return;
    }

    const instruction = new TransactionInstruction({
      programId,
      keys: [
        { pubkey: txKeypair.publicKey, isSigner: true, isWritable: true },
        { pubkey: usdcMint, isSigner: false, isWritable: false },
        { pubkey: configPda, isSigner: false, isWritable: false },
        { pubkey: vaultPda, isSigner: false, isWritable: true },
        { pubkey: depositorTokenAccount, isSigner: false, isWritable: true },
        { pubkey: TOKEN_PROGRAM_ID, isSigner: false, isWritable: false },
      ],
      data: encodeRockPaperClawDeposit(parsed.agentId, parsed.amount),
    });

    const transaction = new Transaction().add(instruction);
    const signature = await sendAndConfirmTransaction(conn, transaction, [txKeypair], {
      commitment: parsed.commitment,
    });
    const afterBalance = await getTokenBalanceOrThrow(conn, depositorTokenAccount);

    console.log(JSON.stringify({
      ...preview,
      tokenBalanceAfter: afterBalance.value.amount,
      signature,
      note: 'Deposit submitted. Poll RockPaperClaw get_profile until the chip balance reflects the webhook credit.',
    }, null, 2));
    return;
  }

  const keypairPath = resolveKeypairPath();
  const kp = loadKeypair(keypairPath);

  if (cmd === 'address') {
    console.log(JSON.stringify({
      network,
      rpcUrl: RPC_URL,
      address: kp.publicKey.toBase58(),
      keypairPath,
    }, null, 2));
    return;
  }

  if (cmd === 'balance') {
    const lamports = await conn.getBalance(kp.publicKey, 'confirmed');
    console.log(JSON.stringify({
      network,
      rpcUrl: RPC_URL,
      address: kp.publicKey.toBase58(),
      lamports,
      sol: lamports / LAMPORTS_PER_SOL,
    }, null, 2));
    return;
  }

  if (cmd === 'airdrop') {
    const solAmount = Number(args[0] || '1');
    if (!Number.isFinite(solAmount) || solAmount <= 0) {
      throw new Error('Airdrop amount must be a positive number of SOL');
    }
    const lamports = Math.round(solAmount * LAMPORTS_PER_SOL);
    const signature = await conn.requestAirdrop(kp.publicKey, lamports);
    await conn.confirmTransaction(signature, 'confirmed');
    const after = await conn.getBalance(kp.publicKey, 'confirmed');
    console.log(JSON.stringify({
      network,
      rpcUrl: RPC_URL,
      address: kp.publicKey.toBase58(),
      requestedSol: solAmount,
      airdropSignature: signature,
      lamports: after,
      sol: after / LAMPORTS_PER_SOL,
    }, null, 2));
    return;
  }

  if (cmd === 'sign-message') {
    const message = args.join(' ');
    if (!message) throw new Error('Message is required');
    const msgBytes = Buffer.from(message, 'utf8');
    const signature = nacl.sign.detached(msgBytes, kp.secretKey);
    console.log(JSON.stringify({
      network,
      address: kp.publicKey.toBase58(),
      message,
      signatureBase64: Buffer.from(signature).toString('base64'),
      signatureBase58: bs58.encode(Buffer.from(signature)),
    }, null, 2));
    return;
  }

  if (cmd === 'verify-message') {
    const [message, sig] = args;
    if (!message || !sig) throw new Error('Message and signature are required');
    const ok = nacl.sign.detached.verify(
      Buffer.from(message, 'utf8'),
      decodeSignature(sig),
      kp.publicKey.toBytes(),
    );
    console.log(JSON.stringify({
      network,
      address: kp.publicKey.toBase58(),
      message,
      valid: ok,
    }, null, 2));
    return;
  }

  usage();
}

main().catch((err) => {
  console.error(err && err.stack ? err.stack : String(err));
  process.exit(1);
});
