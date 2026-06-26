#!/usr/bin/env node

const axios = require('axios');
const { spawn } = require('child_process');

const CONFIG = {
  skillpay_api: 'https://api.skillpay.me/v1',
  merchant_key: process.env.SKILLPAY_MERCHANT_KEY || 'sk_91fff75ae2a7a71f8eceadcbcd816e24d57e58d9d04ccca45f0b3856af130aea',
  price_per_use: 0.002,
  currency: 'USDT'
};

async function generateIdeas(topic, options = {}) {
  const prompt = `You are Sloan, a YouTube content strategist. Generate 5 viral video ideas for "${topic}".

For each idea, provide:
1. **Title** (optimized for CTR, 50-60 chars)
2. **Hook** (first 30 seconds that grabs attention)
3. **Format** (tutorial, reaction, listicle, vlog, challenge)
4. **Keywords** (3-5 SEO keywords)

Guidelines:
- Use power words: Ultimate, Exposed, Secret, Revealed
- Include numbers when relevant
- Create curiosity gap
- Appeal to emotion (fear, excitement, curiosity)
${options.niche ? `- Niche: ${options.niche}` : ''}
${options.outline ? '- Include brief content outline (3-5 bullet points)' : ''}

Format:
**Idea 1: [Title]**
Hook: [First 30 seconds]
Format: [Type]
Keywords: [keyword1, keyword2, ...]
${options.outline ? 'Outline:\n- Point 1\n- Point 2\n...' : ''}

Return 5 ideas total.`;

  const result = await new Promise((resolve, reject) => {
    const child = spawn('openclaw', ['agent', '--agent', 'sloan', '-m', prompt], {
      encoding: 'utf-8',
      timeout: 60000
    });
    let stdout = '';
    child.stdout.on('data', (d) => stdout += d);
    child.on('close', (code) => code === 0 ? resolve(stdout) : reject(new Error('Agent failed')));
  });
  
  return { ideas: result.trim() };
}

async function processPayment() {
  try {
    const response = await axios.post(`${CONFIG.skillpay_api}/billing/charge`, {
      amount: CONFIG.price_per_use,
      currency: CONFIG.currency,
      merchant_key: CONFIG.merchant_key,
      description: 'YouTube video ideas by Sloan'
    }, { headers: { 'Content-Type': 'application/json' }, timeout: 10000 });
    
    return { success: true, transaction_id: response.data.transaction_id || response.data.id };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.message || error.message,
      payment_url: 'https://skillpay.me/topup'
    };
  }
}

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes('--help')) {
    console.log(`
🎬 YouTube Video Ideas Generator
Powered by Sloan
━━━━━━━━━━━━━━━━━━━━

Usage:
  youtube-video-ideas <topic> [options]

Options:
  --niche <niche>    Target niche (tech, gaming, lifestyle)
  --outline          Include content outline
  --test             Test mode (skip payment)

Examples:
  youtube-video-ideas "AI agents"
  youtube-video-ideas "productivity" --niche tech --outline

Pricing: 0.002 USDT per generation
    `);
    process.exit(0);
  }
  
  const topic = args[0];
  const options = {
    niche: args.includes('--niche') ? args[args.indexOf('--niche') + 1] : null,
    outline: args.includes('--outline'),
    testMode: args.includes('--test')
  };
  
  console.log('🎬 YouTube Video Ideas Generator');
  console.log('━━━━━━━━━━━━━━━━━━━━\n');
  
  if (!options.testMode) {
    const payment = await processPayment();
    if (!payment.success) {
      console.log(`💳 Payment Required: ${payment.error}`);
      if (payment.payment_url) console.log(`Top up: ${payment.payment_url}`);
      process.exit(1);
    }
    console.log(`✅ Payment: ${payment.transaction_id}\n`);
  } else {
    console.log('🧪 Test mode\n');
  }
  
  console.log(`Generating ideas for "${topic}"...\n`);
  
  const result = await generateIdeas(topic, options);
  
  console.log('━━━━━━━━━━━━━━━━━━━━\n');
  console.log(result.ideas);
  console.log('\n━━━━━━━━━━━━━━━━━━━━');
  console.log(`💰 Cost: ${CONFIG.price_per_use} ${CONFIG.currency}`);
}

if (require.main === module) main().catch(console.error);
module.exports = { generateIdeas, processPayment };
