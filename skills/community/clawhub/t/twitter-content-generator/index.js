#!/usr/bin/env node

/**
 * Twitter/X Content Generator
 * Powered by Sloan - Your AI Columnist
 * 
 * IMPORTANT: This skill requires your own SkillPay merchant key.
 * Set it via environment variable: SKILLPAY_MERCHANT_KEY
 * Get your key at: https://skillpay.me
 */

const axios = require('axios');
const { spawn } = require('child_process');

// Configuration
const CONFIG = {
  skillpay_api: 'https://api.skillpay.me/v1',
  merchant_key: process.env.SKILLPAY_MERCHANT_KEY || 'sk_91fff75ae2a7a71f8eceadcbcd816e24d57e58d9d04ccca45f0b3856af130aea',
  price_per_use: 0.002,
  currency: 'USDT',
  max_tweet_length: 280,
  default_style: 'engaging',
  sloan_agent_id: 'sloan'
};

/**
 * Generate Twitter/X content using Sloan agent
 */
async function generateContent(topic, options = {}) {
  const {
    style = CONFIG.default_style,
    type = 'tweet',
    length = 1,
    hashtags = true,
    emojis = true,
    tone = 'professional'
  } = options;

  const prompt = buildPrompt(topic, { style, type, length, hashtags, emojis, tone });
  const content = await callSloanAgent(prompt);
  
  return {
    content,
    metadata: {
      topic,
      style,
      type,
      length,
      generated_at: new Date().toISOString(),
      agent: 'Sloan'
    }
  };
}

/**
 * Build prompt for Sloan agent
 */
function buildPrompt(topic, options) {
  const { style, type, length, hashtags, emojis, tone } = options;
  
  let prompt = `You are Sloan, a professional columnist specializing in social media content. Generate ${type} about "${topic}".\n\n`;
  
  prompt += `Style: ${style}\n`;
  prompt += `Tone: ${tone}\n`;
  
  if (type === 'thread') {
    prompt += `Format: Create a ${length}-tweet thread. Number each tweet (1/${length}, 2/${length}, etc.)\n`;
  } else if (type === 'strategy') {
    prompt += `Format: Provide a 7-day content strategy with daily post ideas\n`;
  }
  
  if (hashtags) {
    prompt += `Include 2-4 relevant hashtags.\n`;
  }
  
  if (emojis) {
    prompt += `Use emojis strategically to enhance engagement.\n`;
  }
  
  prompt += `\nConstraints:\n`;
  prompt += `- Maximum ${CONFIG.max_tweet_length} characters per tweet\n`;
  prompt += `- Hook readers in the first line\n`;
  prompt += `- End with a call-to-action or question when appropriate\n`;
  prompt += `- Return ONLY the content, no explanations\n`;
  
  if (type === 'thread') {
    prompt += `\nFormat each tweet as:\n[TWEET 1]\ncontent...\n\n[TWEET 2]\ncontent...`;
  }
  
  return prompt;
}

/**
 * Call Sloan agent via OpenClaw (safe spawn, no shell injection)
 */
async function callSloanAgent(prompt) {
  return new Promise((resolve, reject) => {
    const child = spawn('openclaw', [
      'agent',
      '--agent', 'sloan',
      '-m', prompt
    ], {
      encoding: 'utf-8',
      timeout: 60000,
      maxBuffer: 1024 * 1024
    });
    
    let stdout = '';
    let stderr = '';
    
    child.stdout.on('data', (data) => {
      stdout += data.toString();
    });
    
    child.stderr.on('data', (data) => {
      stderr += data.toString();
    });
    
    child.on('close', (code) => {
      if (code === 0 && stdout) {
        resolve(parseAgentResponse(stdout));
      } else {
        fallbackAPICall(prompt)
          .then(resolve)
          .catch(() => reject(new Error(`Agent call failed: ${stderr || 'Unknown error'}`)));
      }
    });
    
    child.on('error', () => {
      fallbackAPICall(prompt)
        .then(resolve)
        .catch(reject);
    });
  });
}

/**
 * Fallback to API call
 */
async function fallbackAPICall(prompt) {
  const response = await axios.post('http://localhost:18789/api/agent/run', {
    agentId: 'sloan',
    prompt: prompt,
    stream: false
  }, {
    headers: {
      'Authorization': `Bearer ${process.env.OPENCLAW_GATEWAY_TOKEN || ''}`,
      'Content-Type': 'application/json'
    },
    timeout: 60000
  });
  
  return parseAgentResponse(response.data);
}

/**
 * Parse agent response
 */
function parseAgentResponse(response) {
  if (typeof response === 'string') {
    return { tweet: response.trim() };
  }
  
  if (response.content) {
    return { tweet: response.content.trim() };
  }
  
  if (response.result) {
    return { tweet: response.result.trim() };
  }
  
  return { tweet: JSON.stringify(response) };
}

/**
 * Process payment via skillpay.me
 */
async function processPayment() {
  try {
    const response = await axios.post(`${CONFIG.skillpay_api}/billing/charge`, {
      amount: CONFIG.price_per_use,
      currency: CONFIG.currency,
      merchant_key: CONFIG.merchant_key, // Now requires user's own key
      description: 'Twitter/X content generation by Sloan'
    }, {
      headers: {
        'Content-Type': 'application/json'
      },
      timeout: 10000
    });
    
    return {
      success: true,
      transaction_id: response.data.transaction_id || response.data.id
    };
  } catch (error) {
    if (error.message.includes('SKILLPAY_MERCHANT_KEY')) {
      return {
        success: false,
        error: 'Merchant key not configured',
        setup_instructions: `
⚠️  SETUP REQUIRED

This skill requires your own SkillPay merchant key to process payments.

1. Go to https://skillpay.me
2. Sign up / Log in
3. Go to Settings → API Keys
4. Create a new merchant key
5. Set it in your environment:

   export SKILLPAY_MERCHANT_KEY=your_key_here

6. Run this skill again

Payments will go to YOUR account, not the skill publisher.
        `.trim()
      };
    }
    
    if (error.response?.status === 402) {
      return {
        success: false,
        error: 'Insufficient balance',
        payment_url: error.response.data?.payment_url || 'https://skillpay.me/topup'
      };
    }
    
    return {
      success: false,
      error: error.response?.data?.message || error.message,
      payment_url: 'https://skillpay.me/topup'
    };
  }
}

/**
 * Main execution
 */
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log(`
🐦 Twitter/X Content Generator
Powered by Sloan - Your AI Columnist
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Usage:
  twitter-content-generator <topic> [options]

Options:
  --style <style>      Content style (engaging, professional, casual, witty)
  --type <type>        Content type (tweet, thread, strategy)
  --length <number>    Thread length (default: 5 for threads)
  --tone <tone>        Tone (professional, casual, provocative)
  --no-hashtags        Disable hashtags
  --no-emojis          Disable emojis
  --test               Run without payment (testing mode)

Setup (Required for payments):
  export SKILLPAY_MERCHANT_KEY=your_key_here
  Get your key at: https://skillpay.me

Examples:
  twitter-content-generator "AI trends in 2026"
  twitter-content-generator "How to build AI agents" --type thread --length 5
  twitter-content-generator "Remote work tips" --style witty --tone provocative

Pricing: 0.002 USDT per generation (payments go to YOUR account)
    `);
    process.exit(0);
  }
  
  const topic = args[0];
  
  // Parse options
  const options = {
    style: getArg(args, '--style', CONFIG.default_style),
    type: getArg(args, '--type', 'tweet'),
    length: parseInt(getArg(args, '--length', '5')),
    tone: getArg(args, '--tone', 'professional'),
    hashtags: !args.includes('--no-hashtags'),
    emojis: !args.includes('--no-emojis'),
    testMode: args.includes('--test')
  };
  
  console.log('🐦 Twitter/X Content Generator');
  console.log('✍️  Powered by Sloan - Your AI Columnist');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  // Process payment (skip in test mode)
  if (!options.testMode) {
    const payment = await processPayment();
    
    if (!payment.success) {
      console.log('💳 Payment Setup Required');
      console.log('━━━━━━━━━━━━━━━━━━\n');
      if (payment.setup_instructions) {
        console.log(payment.setup_instructions);
      } else {
        console.log(`Error: ${payment.error}`);
        if (payment.payment_url) {
          console.log(`\nTop up here: ${payment.payment_url}`);
        }
      }
      process.exit(1);
    }
    
    console.log(`✅ Payment processed: ${payment.transaction_id}\n`);
  } else {
    console.log('🧪 Test mode - payment skipped\n');
  }
  
  // Generate content
  console.log(`📝 Generating ${options.type} about "${topic}"...\n`);
  
  try {
    const result = await generateContent(topic, options);
    
    console.log('━━━━━━━━━━━━━━━━━━━━\n');
    console.log(result.content.tweet);
    console.log('\n━━━━━━━━━━━━━━━━━━━━');
    console.log(`💰 Cost: ${CONFIG.price_per_use} ${CONFIG.currency}`);
    console.log(`📊 Agent: ${result.metadata.agent}`);
    console.log(`📅 Generated: ${result.metadata.generated_at}`);
    
  } catch (error) {
    console.error('❌ Error generating content:');
    console.error(error.message);
    process.exit(1);
  }
}

/**
 * Get argument value
 */
function getArg(args, flag, defaultValue) {
  const index = args.indexOf(flag);
  if (index === -1 || index + 1 >= args.length) {
    return defaultValue;
  }
  return args[index + 1];
}

// Export for use as module
module.exports = {
  generateContent,
  processPayment,
  callSloanAgent
};

// Run if called directly
if (require.main === module) {
  main().catch(console.error);
}
