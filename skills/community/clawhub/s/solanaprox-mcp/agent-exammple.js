#!/usr/bin/env node
/**
 * SolanaProx Agent Example
 * 
 * An AI agent that autonomously pays for its own inference using USDC.
 * No API keys. No accounts. The wallet IS the credential.
 * 
 * Setup:
 *   npm install
 *   SOLANA_WALLET=your_wallet_address node agent-example.js
 */

const SOLANAPROX_URL = process.env.SOLANAPROX_URL || "https://solanaprox.com";
const WALLET = process.env.SOLANA_WALLET;

if (!WALLET) {
  console.error("❌ Set SOLANA_WALLET to your Phantom wallet address");
  process.exit(1);
}

// ─── Core API call ───────────────────────────────────────────────────────────

async function askAI(prompt, model = "claude-sonnet-4-20250514", maxTokens = 512) {
  const res = await fetch(`${SOLANAPROX_URL}/v1/messages`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Wallet-Address": WALLET,
    },
    body: JSON.stringify({
      model,
      max_tokens: maxTokens,
      messages: [{ role: "user", content: prompt }],
    }),
  });

  if (res.status === 402) {
    const err = await res.json();
    throw new Error(`💸 Insufficient balance: ${err.error}. Deposit at ${SOLANAPROX_URL}`);
  }

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }

  const data = await res.json();
  return {
    text: data.content?.[0]?.text || data.choices?.[0]?.message?.content,
    usage: data.usage,
    model: data.model,
  };
}

async function checkBalance() {
  const res = await fetch(`${SOLANAPROX_URL}/api/balance/${WALLET}`);
  if (!res.ok) throw new Error("Failed to check balance");
  return res.json();
}

// ─── Example: Research Agent ─────────────────────────────────────────────────

async function researchAgent(topic) {
  console.log(`\n🤖 Research Agent starting...`);
  console.log(`📋 Topic: ${topic}`);
  console.log(`💳 Wallet: ${WALLET.slice(0, 8)}...${WALLET.slice(-4)}`);

  // Check balance before starting
  const balance = await checkBalance();
  console.log(`💰 Balance: $${balance.total_usd?.toFixed(4)} USDC\n`);

  if (balance.total_usd < 0.01) {
    console.log(`⚠️  Low balance. Deposit USDC at ${SOLANAPROX_URL}`);
    return;
  }

  // Step 1: Generate research questions
  console.log("Step 1: Generating research questions...");
  const questions = await askAI(
    `Generate 3 focused research questions about: "${topic}". 
     Format as a numbered list. Be specific and actionable.`,
    "claude-sonnet-4-20250514",
    256
  );
  console.log(questions.text);

  // Step 2: Answer each question
  console.log("\nStep 2: Researching each question...");
  const answers = await askAI(
    `Based on these questions about "${topic}":
     ${questions.text}
     
     Provide concise, factual answers to each. Focus on key insights.`,
    "claude-sonnet-4-20250514",
    512
  );
  console.log(answers.text);

  // Step 3: Synthesize into summary
  console.log("\nStep 3: Synthesizing research...");
  const summary = await askAI(
    `Synthesize this research about "${topic}" into a 3-sentence executive summary:
     ${answers.text}`,
    "claude-sonnet-4-20250514",
    256
  );
  
  console.log("\n📊 RESEARCH SUMMARY");
  console.log("─".repeat(50));
  console.log(summary.text);
  console.log("─".repeat(50));

  // Final balance check
  const finalBalance = await checkBalance();
  console.log(`\n💳 Remaining balance: $${finalBalance.total_usd?.toFixed(4)} USDC`);
  console.log(`⚡ Powered by SolanaProx | solanaprox.com`);
}

// ─── Example: Code Review Agent ──────────────────────────────────────────────

async function codeReviewAgent(code, language = "javascript") {
  console.log(`\n🔍 Code Review Agent starting...`);
  
  const balance = await checkBalance();
  if (balance.total_usd < 0.005) {
    console.log(`⚠️  Insufficient balance. Deposit at ${SOLANAPROX_URL}`);
    return;
  }

  const review = await askAI(
    `Review this ${language} code for:
     1. Bugs and potential errors
     2. Security issues  
     3. Performance improvements
     4. Best practices
     
     Code:
     \`\`\`${language}
     ${code}
     \`\`\`
     
     Be specific with line references where applicable.`,
    "claude-sonnet-4-20250514",
    1024
  );

  console.log("\n📝 CODE REVIEW");
  console.log("─".repeat(50));
  console.log(review.text);
  console.log("─".repeat(50));
  console.log(`⚡ Tokens used: ${review.usage?.input_tokens || "?"} in / ${review.usage?.output_tokens || "?"} out`);
}

// ─── Run examples ─────────────────────────────────────────────────────────────

async function main() {
  const [,, command, ...rest] = process.argv;

  switch (command) {
    case "research":
      await researchAgent(rest.join(" ") || "the future of AI payments");
      break;
    case "review":
      // Read from stdin for code review
      const code = rest.join("\n") || `
        function fetchUser(id) {
          return fetch('/api/users/' + id)
            .then(r => r.json())
            .catch(e => null)
        }
      `;
      await codeReviewAgent(code);
      break;
    case "balance":
      const bal = await checkBalance();
      console.log(`💰 Balance: $${bal.total_usd?.toFixed(4)} USDC`);
      break;
    default:
      // Demo: run a quick AI call
      console.log("🚀 SolanaProx Agent Demo\n");
      const result = await askAI(
        "In one sentence, explain why paying for AI with USDC is better than API keys."
      );
      console.log("Response:", result.text);
      console.log(`\nTokens: ${result.usage?.input_tokens}in / ${result.usage?.output_tokens}out`);
      console.log(`⚡ Powered by solanaprox.com`);
  }
}

main().catch(console.error);
