require('dotenv/config');

const { z } = require('zod');

const envSchema = z.object({
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

module.exports = {
  id: 'telegram-demo-billing',

  // OpenClaw plugin entrypoint style: expose onMessage hook.
  // If your OpenClaw telegram plugin expects a different shape, tell me and I’ll adapt.
  async onMessage(ctx) {
    // ctx is expected to include:
    // - ctx.text
    // - ctx.sender?.id (telegram user id)
    // - ctx.reply(text)

    const text = (ctx.text || '').trim();
    const senderId = String(ctx.sender?.id || ctx.senderId || '');
    if (!senderId) return;

    // Default intercept: require funding
    if (!text.startsWith('/')) {
      const bal = await billing('/balance', { telegramUserId: senderId }).catch(() => ({ balanceCredits: 0 }));
      if (!bal.balanceCredits || bal.balanceCredits <= 0) {
        await ctx.reply(
          `This agent is pay-to-use.\n\n` +
          `To add credits:\n` +
          `1) /deposit (get your personal funding address)\n` +
          `2) Send SOL to that address\n` +
          `3) /confirm <lamports> (I’ll convert it into credits)\n\n` +
          `Pricing: 100 credits = 0.01 SOL (1 credit = 100,000 lamports).\n` +
          `Check balance: /balance`
        );
        return;
      }

      // Demo: spend 1 credit per message (you can change this)
      await billing('/spend', { telegramUserId: senderId, credits: 1 });
      await ctx.reply(`(demo) Spent 1 credit. Your message was received. Now wire this to real tasks.`);
      return;
    }

    const [cmdRaw, ...args] = text.split(/\s+/);
    const cmd = cmdRaw.toLowerCase();

    if (cmd === '/start' || cmd === '/help') {
      await ctx.reply(
        `Commands:\n` +
        `/deposit - get your personal funding address\n` +
        `/confirm <lamports> - after you send SOL, confirm amount to credit\n` +
        `/balance - show credits\n\n` +
        `Pricing: 100 credits = 0.01 SOL (1 credit = 100,000 lamports).`
      );
      return;
    }

    if (cmd === '/deposit') {
      const out = await billing('/deposit-wallet', { telegramUserId: senderId });
      await ctx.reply(
        `Send SOL to your personal funding address:\n` +
        `${out.depositAddress}\n\n` +
        `Then run: /confirm <lamports>\n` +
        `Example for 0.01 SOL: /confirm 10000000`
      );
      return;
    }

    if (cmd === '/confirm') {
      const lamports = Number(args[0]);
      if (!Number.isFinite(lamports) || lamports <= 0) {
        await ctx.reply(`Usage: /confirm <lamports>  (example: /confirm 10000000)`);
        return;
      }
      await ctx.reply(`Waiting for deposit of at least ${formatLamports(lamports)}... (up to ~2 minutes)`);
      const out = await billing('/fund-and-credit', { telegramUserId: senderId, depositLamports: lamports });

      if (out.status === 'timeout') {
        await ctx.reply(`No deposit detected yet. Address:\n${out.depositAddress}\nTry /confirm ${lamports} again after you send.`);
        return;
      }

      if (out.status === 'invoice_not_verified_yet') {
        await ctx.reply(
          `Deposit detected. I paid the Pump invoice tx.\n` +
          `Signature: ${out.signature}\n` +
          `Memo: ${out.memo}\n\n` +
          `Not verified yet—try again in ~10s with: /confirm ${lamports}`
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
      return;
    }

    if (cmd === '/balance') {
      const out = await billing('/balance', { telegramUserId: senderId });
      await ctx.reply(`Balance: ${out.balanceCredits} credits`);
      return;
    }

    await ctx.reply(`Unknown command. Use /help`);
  },
};
