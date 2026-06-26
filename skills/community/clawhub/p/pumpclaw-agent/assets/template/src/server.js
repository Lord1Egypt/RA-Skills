import 'dotenv/config';
import Fastify from 'fastify';
import rateLimit from '@fastify/rate-limit';
import Database from 'better-sqlite3';
import bs58 from 'bs58';
import { z } from 'zod';
import {
  Connection,
  Keypair,
  PublicKey,
  Transaction,
} from '@solana/web3.js';
import { PumpAgent } from '@pump-fun/agent-payments-sdk';

const envSchema = z.object({
  RPC_URL: z.string().url(),
  AGENT_TOKEN_MINT_ADDRESS: z.string().min(32),
  CURRENCY_MINT: z.string().min(32),
  LAMPORTS_PER_CREDIT: z.coerce.number().int().positive(),
  TREASURY_SECRET_KEY_BASE58: z.string().min(40),
  PORT: z.coerce.number().int().positive().default(3033),
  API_TOKEN: z.string().min(16),
  DB_PATH: z.string().default('./demo.db'),
});

const env = envSchema.parse(process.env);

const connection = new Connection(env.RPC_URL, 'confirmed');
const agentMint = new PublicKey(env.AGENT_TOKEN_MINT_ADDRESS);
const currencyMint = new PublicKey(env.CURRENCY_MINT);

const treasury = (() => {
  const secret = bs58.decode(env.TREASURY_SECRET_KEY_BASE58);
  return Keypair.fromSecretKey(secret);
})();

const pumpAgent = new PumpAgent(agentMint, 'mainnet', connection);

const db = new Database(env.DB_PATH);

db.exec(`
CREATE TABLE IF NOT EXISTS users (
  telegram_user_id TEXT PRIMARY KEY,
  created_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS deposit_wallets (
  telegram_user_id TEXT PRIMARY KEY,
  deposit_pubkey TEXT NOT NULL,
  deposit_secret_b58 TEXT NOT NULL,
  created_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS credits (
  telegram_user_id TEXT PRIMARY KEY,
  balance_credits INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS invoices (
  memo TEXT PRIMARY KEY,
  telegram_user_id TEXT NOT NULL,
  amount_lamports INTEGER NOT NULL,
  start_time INTEGER NOT NULL,
  end_time INTEGER NOT NULL,
  signature TEXT,
  status TEXT NOT NULL,
  created_at INTEGER NOT NULL
);
`);

function authHook(req, reply, done) {
  const token = req.headers['x-api-token'];
  if (token !== env.API_TOKEN) return reply.code(401).send({ error: 'unauthorized' });
  done();
}

function nowSec() {
  return Math.floor(Date.now() / 1000);
}

function ensureUser(telegramUserId) {
  db.prepare('INSERT OR IGNORE INTO users (telegram_user_id, created_at) VALUES (?, ?)')
    .run(telegramUserId, Date.now());
  db.prepare('INSERT OR IGNORE INTO credits (telegram_user_id, balance_credits) VALUES (?, 0)')
    .run(telegramUserId);
}

function getOrCreateDepositWallet(telegramUserId) {
  ensureUser(telegramUserId);
  const row = db.prepare('SELECT deposit_pubkey, deposit_secret_b58 FROM deposit_wallets WHERE telegram_user_id=?')
    .get(telegramUserId);
  if (row) return row;

  // demo: generate a new keypair per user and store secret in sqlite
  const kp = Keypair.generate();
  const secretB58 = bs58.encode(kp.secretKey);
  db.prepare('INSERT INTO deposit_wallets (telegram_user_id, deposit_pubkey, deposit_secret_b58, created_at) VALUES (?,?,?,?)')
    .run(telegramUserId, kp.publicKey.toBase58(), secretB58, Date.now());
  return { deposit_pubkey: kp.publicKey.toBase58(), deposit_secret_b58: secretB58 };
}

async function waitForDeposit(pubkeyStr, lamports, timeoutMs = 120_000) {
  const pubkey = new PublicKey(pubkeyStr);
  const start = Date.now();
  const startBal = await connection.getBalance(pubkey, 'confirmed');

  while (Date.now() - start < timeoutMs) {
    await new Promise(r => setTimeout(r, 2500));
    const bal = await connection.getBalance(pubkey, 'confirmed');
    if (bal - startBal >= lamports) {
      return { receivedLamports: bal - startBal, balance: bal };
    }
  }
  return null;
}

async function buildAndPayInvoice({ depositKeypair, amountLamports }) {
  const memo = String(Math.floor(Math.random() * 900000000000) + 100000);
  const startTime = nowSec();
  const endTime = startTime + 3600; // 1 hour validity

  const ixs = await pumpAgent.buildAcceptPaymentInstructions({
    user: depositKeypair.publicKey,
    currencyMint,
    amount: String(amountLamports),
    memo,
    startTime: String(startTime),
    endTime: String(endTime),
  });

  const { blockhash } = await connection.getLatestBlockhash('confirmed');
  const tx = new Transaction({ recentBlockhash: blockhash, feePayer: depositKeypair.publicKey });
  tx.add(...ixs);

  // Sign with the deposit wallet (server-controlled)
  tx.sign(depositKeypair);

  const sig = await connection.sendRawTransaction(tx.serialize(), {
    skipPreflight: false,
    preflightCommitment: 'confirmed',
  });
  await connection.confirmTransaction({ signature: sig, blockhash, lastValidBlockHeight: (await connection.getLatestBlockhash('confirmed')).lastValidBlockHeight }, 'confirmed');

  return { memo, startTime, endTime, signature: sig };
}

async function verifyInvoicePaid({ userPubkey, amountLamports, memo, startTime, endTime }) {
  return pumpAgent.validateInvoicePayment({
    user: userPubkey,
    currencyMint,
    amount: Number(amountLamports),
    memo: Number(memo),
    startTime: Number(startTime),
    endTime: Number(endTime),
  });
}

const fastify = Fastify({ logger: true });

await fastify.register(rateLimit, {
  max: 60,
  timeWindow: '1 minute',
});

fastify.addHook('onRequest', (req, reply, done) => {
  if (req.url.startsWith('/health')) return done();
  return authHook(req, reply, done);
});

fastify.get('/health', async () => ({ ok: true }));

// 1) create/get deposit wallet
fastify.post('/deposit-wallet', async (req) => {
  const body = z.object({ telegramUserId: z.string().min(1) }).parse(req.body);
  const w = getOrCreateDepositWallet(body.telegramUserId);
  return { depositAddress: w.deposit_pubkey };
});

// 2) wait for user deposit, then pay invoice from that deposit wallet, then credit
fastify.post('/fund-and-credit', async (req) => {
  const body = z.object({
    telegramUserId: z.string().min(1),
    depositLamports: z.coerce.number().int().positive(),
  }).parse(req.body);

  ensureUser(body.telegramUserId);
  const w = getOrCreateDepositWallet(body.telegramUserId);

  const deposit = await waitForDeposit(w.deposit_pubkey, body.depositLamports);
  if (!deposit) {
    return { status: 'timeout', depositAddress: w.deposit_pubkey };
  }

  const depositKeypair = Keypair.fromSecretKey(bs58.decode(w.deposit_secret_b58));

  const { memo, startTime, endTime, signature } = await buildAndPayInvoice({
    depositKeypair,
    amountLamports: body.depositLamports,
  });

  db.prepare('INSERT OR REPLACE INTO invoices (memo, telegram_user_id, amount_lamports, start_time, end_time, signature, status, created_at) VALUES (?,?,?,?,?,?,?,?)')
    .run(memo, body.telegramUserId, body.depositLamports, startTime, endTime, signature, 'sent', Date.now());

  const paid = await verifyInvoicePaid({
    userPubkey: depositKeypair.publicKey,
    amountLamports: body.depositLamports,
    memo,
    startTime,
    endTime,
  });

  if (!paid) {
    return { status: 'invoice_not_verified_yet', memo, signature, depositAddress: w.deposit_pubkey };
  }

  const creditsToAdd = Math.floor(body.depositLamports / env.LAMPORTS_PER_CREDIT);
  db.prepare('UPDATE credits SET balance_credits = balance_credits + ? WHERE telegram_user_id=?')
    .run(creditsToAdd, body.telegramUserId);
  db.prepare('UPDATE invoices SET status=? WHERE memo=?').run('verified', memo);

  const bal = db.prepare('SELECT balance_credits FROM credits WHERE telegram_user_id=?').get(body.telegramUserId);

  return {
    status: 'credited',
    creditsAdded: creditsToAdd,
    balanceCredits: bal.balance_credits,
    memo,
    signature,
    depositAddress: w.deposit_pubkey,
  };
});

fastify.post('/balance', async (req) => {
  const body = z.object({ telegramUserId: z.string().min(1) }).parse(req.body);
  ensureUser(body.telegramUserId);
  const bal = db.prepare('SELECT balance_credits FROM credits WHERE telegram_user_id=?').get(body.telegramUserId);
  return { balanceCredits: bal.balance_credits };
});

fastify.post('/spend', async (req) => {
  const body = z.object({ telegramUserId: z.string().min(1), credits: z.coerce.number().int().positive() }).parse(req.body);
  ensureUser(body.telegramUserId);
  const cur = db.prepare('SELECT balance_credits FROM credits WHERE telegram_user_id=?').get(body.telegramUserId);
  if (cur.balance_credits < body.credits) return { ok: false, error: 'insufficient_credits', balanceCredits: cur.balance_credits };
  db.prepare('UPDATE credits SET balance_credits = balance_credits - ? WHERE telegram_user_id=?')
    .run(body.credits, body.telegramUserId);
  const after = db.prepare('SELECT balance_credits FROM credits WHERE telegram_user_id=?').get(body.telegramUserId);
  return { ok: true, balanceCredits: after.balance_credits };
});

fastify.listen({ port: env.PORT, host: '127.0.0.1' });
