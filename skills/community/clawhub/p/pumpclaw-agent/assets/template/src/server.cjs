require('dotenv/config');

const Fastify = require('fastify');
const rateLimit = require('@fastify/rate-limit');
const Database = require('better-sqlite3');
const bs58 = require('bs58').default;
const { z } = require('zod');
const {
  Connection,
  Keypair,
  PublicKey,
  Transaction,
} = require('@solana/web3.js');
const { PumpAgent } = require('@pump-fun/agent-payments-sdk');

const envSchema = z.object({
  SOLANA_RPC_URL: z.string().url(),
  AGENT_TOKEN_MINT_ADDRESS: z.string().min(32),
  CURRENCY_MINT: z.string().min(32),
  LAMPORTS_PER_CREDIT: z.coerce.number().int().positive(),
  TREASURY_SECRET_KEY_BASE58: z.string().min(40),
  PORT: z.coerce.number().int().positive().default(3033),
  API_TOKEN: z.string().min(16),
  DB_PATH: z.string().default('./demo.db'),
});

const env = envSchema.parse(process.env);

const connection = new Connection(env.SOLANA_RPC_URL, 'confirmed');
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

  // DEMO: generate a new keypair per user and store secret in sqlite
  const kp = Keypair.generate();
  const secretB58 = bs58.encode(kp.secretKey);
  db.prepare('INSERT INTO deposit_wallets (telegram_user_id, deposit_pubkey, deposit_secret_b58, created_at) VALUES (?,?,?,?)')
    .run(telegramUserId, kp.publicKey.toBase58(), secretB58, Date.now());
  return { deposit_pubkey: kp.publicKey.toBase58(), deposit_secret_b58: secretB58 };
}

async function waitForDeposit(pubkeyStr, lamports, timeoutMs = 120_000) {
  const pubkey = new PublicKey(pubkeyStr);
  const start = Date.now();

  // FIX: if funds are already there (deposit happened before /confirm), accept.
  const initial = await connection.getBalance(pubkey, 'confirmed');
  if (initial >= lamports) {
    return { receivedLamports: initial, balance: initial, mode: 'absolute' };
  }

  while (Date.now() - start < timeoutMs) {
    await new Promise(r => setTimeout(r, 2500));
    const bal = await connection.getBalance(pubkey, 'confirmed');
    if (bal >= lamports) {
      return { receivedLamports: bal, balance: bal, mode: 'absolute' };
    }
  }
  return null;
}

async function buildAndPayInvoice({ payerKeypair, amountLamports }) {
  const memo = String(Math.floor(Math.random() * 900000000000) + 100000);
  const startTime = nowSec();
  const endTime = startTime + 3600; // 1 hour

  const ixs = await pumpAgent.buildAcceptPaymentInstructions({
    user: payerKeypair.publicKey,
    currencyMint,
    amount: String(amountLamports),
    memo,
    startTime: String(startTime),
    endTime: String(endTime),
  });

  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash('confirmed');
  const tx = new Transaction({ recentBlockhash: blockhash, feePayer: payerKeypair.publicKey });
  tx.add(...ixs);
  tx.sign(payerKeypair);

  const sig = await connection.sendRawTransaction(tx.serialize(), {
    skipPreflight: false,
    preflightCommitment: 'confirmed',
  });

  await connection.confirmTransaction({ signature: sig, blockhash, lastValidBlockHeight }, 'confirmed');

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

fastify.register(rateLimit, {
  max: 60,
  timeWindow: '1 minute',
});

fastify.addHook('onRequest', (req, reply, done) => {
  if (req.url.startsWith('/health')) return done();
  return authHook(req, reply, done);
});

fastify.get('/health', async () => ({ ok: true }));

// Create/get deposit wallet
fastify.post('/deposit-wallet', async (req) => {
  const body = z.object({ telegramUserId: z.string().min(1) }).parse(req.body);
  const w = getOrCreateDepositWallet(body.telegramUserId);
  return { depositAddress: w.deposit_pubkey };
});

// Wait for deposit to the per-user wallet, then pay a Pump invoice FROM THAT WALLET.
fastify.post('/fund-and-credit', async (req) => {
  const body = z.object({
    telegramUserId: z.string().min(1),
    depositLamports: z.coerce.number().int().positive(),
    timeoutMs: z.coerce.number().int().positive().optional(),
  }).parse(req.body);

  ensureUser(body.telegramUserId);
  const w = getOrCreateDepositWallet(body.telegramUserId);

  // If we already have a verified invoice for this exact amount, just report current balance.
  const existingVerified = db.prepare(
    'SELECT memo, signature FROM invoices WHERE telegram_user_id=? AND amount_lamports=? AND status=? ORDER BY created_at DESC LIMIT 1'
  ).get(body.telegramUserId, body.depositLamports, 'verified');
  if (existingVerified) {
    const bal = db.prepare('SELECT balance_credits FROM credits WHERE telegram_user_id=?').get(body.telegramUserId);
    return {
      status: 'credited',
      creditsAdded: 0,
      balanceCredits: bal.balance_credits,
      memo: existingVerified.memo,
      signature: existingVerified.signature,
      depositAddress: w.deposit_pubkey,
    };
  }

  // If we already created an invoice for this exact amount but it wasn't verified yet, retry verification first.
  // If the existing tx failed on-chain, ignore it and create a fresh invoice.
  const existing = db.prepare(
    'SELECT memo, signature, start_time, end_time, status FROM invoices WHERE telegram_user_id=? AND amount_lamports=? ORDER BY created_at DESC LIMIT 1'
  ).get(body.telegramUserId, body.depositLamports);

  const payerKeypair = Keypair.fromSecretKey(bs58.decode(w.deposit_secret_b58));

  if (existing && existing.status === 'sent') {
    let failedOnChain = false;
    try {
      const st = await connection.getSignatureStatus(existing.signature, { searchTransactionHistory: true });
      failedOnChain = Boolean(st?.value?.err);
    } catch {}

    if (!failedOnChain) {
      const paid = await verifyInvoicePaid({
        userPubkey: payerKeypair.publicKey,
        amountLamports: body.depositLamports,
        memo: existing.memo,
        startTime: existing.start_time,
        endTime: existing.end_time,
      });

      if (paid) {
        const creditsToAdd = Math.floor(body.depositLamports / env.LAMPORTS_PER_CREDIT);
        db.prepare('UPDATE credits SET balance_credits = balance_credits + ? WHERE telegram_user_id=?')
          .run(creditsToAdd, body.telegramUserId);
        db.prepare('UPDATE invoices SET status=? WHERE memo=?').run('verified', existing.memo);
        const bal = db.prepare('SELECT balance_credits FROM credits WHERE telegram_user_id=?').get(body.telegramUserId);
        return {
          status: 'credited',
          creditsAdded: creditsToAdd,
          balanceCredits: bal.balance_credits,
          memo: existing.memo,
          signature: existing.signature,
          depositAddress: w.deposit_pubkey,
        };
      }

      return {
        status: 'invoice_not_verified_yet',
        memo: existing.memo,
        signature: existing.signature,
        depositAddress: w.deposit_pubkey,
      };
    }

    // mark failed and continue to create a new invoice
    db.prepare('UPDATE invoices SET status=? WHERE memo=?').run('failed', existing.memo);
  }

  const deposit = await waitForDeposit(w.deposit_pubkey, body.depositLamports, body.timeoutMs ?? 120_000);
  if (!deposit) {
    return { status: 'timeout', depositAddress: w.deposit_pubkey };
  }

  const { memo, startTime, endTime, signature } = await buildAndPayInvoice({
    payerKeypair,
    amountLamports: body.depositLamports,
  });

  // Note: amount_lamports stores the *deposit* lamports request (used for credit calculation)
  db.prepare('INSERT OR REPLACE INTO invoices (memo, telegram_user_id, amount_lamports, start_time, end_time, signature, status, created_at) VALUES (?,?,?,?,?,?,?,?)')
    .run(memo, body.telegramUserId, body.depositLamports, startTime, endTime, signature, 'sent', Date.now());

  const paid = await verifyInvoicePaid({
    userPubkey: payerKeypair.publicKey,
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
