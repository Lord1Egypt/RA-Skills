require('dotenv/config');

const { Bot } = require('grammy');
const { z } = require('zod');

const envSchema = z.object({
  TELEGRAM_BOT_TOKEN: z.string().min(40),
  BILLING_URL: z.string().url().default('http://127.0.0.1:3033'),
  BILLING_TOKEN: z.string().min(16),
  LAMPORTS_PER_CREDIT: z.coerce.number().int().positive().default(100000),
});

const env = envSchema.parse(process.env);

async function billing(path, body) {
  const res = await fetch(`${env.BILLING_URL}${path}`, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'x-api-token': env.BILLING_TOKEN,
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`billing ${path} failed: ${res.status} ${text}`);
  }
  return res.json();
}

function formatLamports(lamports) {
  return `${lamports} lamports (~${(lamports / 1e9).toFixed(9)} SOL)`;
}

function pricingLine() {
  return `Pricing: 100 credits = 0.01 SOL (1 credit = ${env.LAMPORTS_PER_CREDIT} lamports).`;
}

const bot = new Bot(env.TELEGRAM_BOT_TOKEN);

bot.command(['start', 'help'], async (ctx) => {
  await ctx.reply(
    `This agent is pay-to-use.\n\n` +
    `Commands:\n` +
    `/deposit - get your personal funding address\n` +
    `/confirm <lamports> - after you send SOL, confirm amount to credit\n` +
    `/balance - show credits\n\n` +
    pricingLine()
  );
});

bot.command('deposit', async (ctx) => {
  const uid = String(ctx.from.id);
  const out = await billing('/deposit-wallet', { telegramUserId: uid });
  await ctx.reply(
    `Send SOL to your personal funding address:\n` +
    `${out.depositAddress}\n\n` +
    `Then run: /confirm <lamports>\n` +
    `Example for 0.01 SOL: /confirm 10000000\n\n` +
    pricingLine()
  );
});

bot.command('balance', async (ctx) => {
  const uid = String(ctx.from.id);
  const out = await billing('/balance', { telegramUserId: uid });
  await ctx.reply(`Balance: ${out.balanceCredits} credits`);
});

bot.command('confirm', async (ctx) => {
  const uid = String(ctx.from.id);
  const parts = (ctx.message.text || '').trim().split(/\s+/);
  const lamports = Number(parts[1]);
  if (!Number.isFinite(lamports) || lamports <= 0) {
    await ctx.reply(`Usage: /confirm <lamports>  (example: /confirm 10000000)`);
    return;
  }

  await ctx.reply(`Waiting for deposit of at least ${formatLamports(lamports)}... (up to ~2 minutes)`);
  const out = await billing('/fund-and-credit', { telegramUserId: uid, depositLamports: lamports });

  if (out.status === 'timeout') {
    await ctx.reply(`No deposit detected yet. Address:\n${out.depositAddress}\nTry /confirm ${lamports} again after you send.`);
    return;
  }

  if (out.status === 'invoice_not_verified_yet') {
    await ctx.reply(
      `Deposit detected. I paid the Pump invoice tx.\n` +
      `Signature: ${out.signature}\n` +
      `Memo: ${out.memo}\n\n` +
      `Not verified yet—run /confirm ${lamports} again in ~10s.`
    );
    return;
  }

  if (out.status === 'credited') {
    await ctx.reply(
      `Credited.\n` +
      `Added: ${out.creditsAdded} credits\n` +
      `Balance: ${out.balanceCredits} credits\n` +
      `Pump invoice signature: ${out.signature}`
    );
    return;
  }

  await ctx.reply(`Unexpected response: ${JSON.stringify(out)}`);
});

bot.on('message:text', async (ctx) => {
  const text = (ctx.message.text || '').trim();
  if (text.startsWith('/')) return; // commands handled above

  const uid = String(ctx.from.id);
  const bal = await billing('/balance', { telegramUserId: uid }).catch(() => ({ balanceCredits: 0 }));
  if (!bal.balanceCredits || bal.balanceCredits <= 0) {
    await ctx.reply(
      `You need credits to use this agent.\n\n` +
      `1) /deposit\n` +
      `2) Send SOL\n` +
      `3) /confirm <lamports>\n\n` +
      pricingLine()
    );
    return;
  }

  // Demo spend 1 credit per message
  await billing('/spend', { telegramUserId: uid, credits: 1 });
  const after = await billing('/balance', { telegramUserId: uid }).catch(() => ({ balanceCredits: '?' }));
  await ctx.reply(`(demo) Spent 1 credit. Balance now: ${after.balanceCredits}. Next: wire this to real tasks.`);
});

(async () => {
  await bot.api.setMyCommands([
    { command: 'deposit', description: 'Get your funding address' },
    { command: 'confirm', description: 'Confirm deposit + credit' },
    { command: 'balance', description: 'Show credits' },
    { command: 'help', description: 'Help' },
  ]);

  await bot.start({ drop_pending_updates: true });
})();
