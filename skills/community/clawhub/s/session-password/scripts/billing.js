/**
 * SkillPay Billing Integration for Session Password
 * 
 * Pricing Model:
 * - Buyout: 29 USDT (one-time, lifetime access)
 * - Per-call: 0.9 USDT (if not purchased)
 * 
 * Skill ID: 6387f3fa-cceb-4a60-afd4-fc1f4eb2d7c3
 * API: BNB Chain USDT payment
 */

const BILLING_API_URL = 'https://skillpay.me';
const BILLING_API_KEY = 'sk_20cb7dd70ceaa244814a9e9a0e990a2781fab10e163fd2f9499f5bb1e7a6eaef';
const SKILL_ID = '6387f3fa-cceb-4a60-afd4-fc1f4eb2d7c3';

// Pricing
const PRICE_PER_CALL = 0.01; // USDT - per call

// ═══════════════════════════════════════════════════
// Core Billing Functions
// ═══════════════════════════════════════════════════

// ① Check balance / 查余额
async function checkBalance(userId) {
  const resp = await fetch(
    `${BILLING_API_URL}/api/v1/billing/balance?user_id=${userId}`,
    { headers: { 'X-API-Key': BILLING_API_KEY } }
  );
  const data = await resp.json();
  return data.balance; // USDT amount
}

// ② Check if user has purchased (buyout) / 检查是否已买断
async function checkPurchased(userId) {
  const resp = await fetch(
    `${BILLING_API_URL}/api/v1/billing/access?user_id=${userId}&skill_id=${SKILL_ID}`,
    { headers: { 'X-API-Key': BILLING_API_KEY } }
  );
  const data = await resp.json();
  return data.has_access === true; // true = already purchased
}

// ③ Charge per call / 每次调用扣费
async function chargeUser(userId, amount = PRICE_PER_CALL) {
  const resp = await fetch(`${BILLING_API_URL}/api/v1/billing/charge`, {
    method: 'POST',
    headers: {
      'X-API-Key': BILLING_API_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: userId,
      skill_id: SKILL_ID,
      amount: amount,
    }),
  });
  const data = await resp.json();

  if (data.success) {
    return { ok: true, balance: data.balance };
  }

  // Insufficient balance → get payment link
  return { ok: false, balance: data.balance, paymentUrl: data.payment_url };
}



// ⑤ Generate payment link / 生成充值链接
async function getPaymentLink(userId, amount = 10) {
  const resp = await fetch(`${BILLING_API_URL}/api/v1/billing/payment-link`, {
    method: 'POST',
    headers: {
      'X-API-Key': BILLING_API_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id: userId, amount }),
  });
  const data = await resp.json();
  return data.payment_url; // BNB Chain USDT payment link
}

// ═══════════════════════════════════════════════════
// Main Handler - Smart Billing Logic
// ═══════════════════════════════════════════════════

/**
 * Handle billing for skill execution
 * 
 * Logic:
 * 1. Charge 0.01 USDT per call
 * 2. Insufficient balance → Return payment link
 * 
 * @param {string} userId - User identifier
 * @returns {Promise<{allowed: boolean, message: string, paymentUrl?: string}>}
 */
async function handleBilling(userId) {
  try {
    // Charge per call
    const result = await chargeUser(userId, PRICE_PER_CALL);
    
    if (result.ok) {
      return { 
        allowed: true, 
        message: `✅ Charged $${PRICE_PER_CALL} USDT. Session Password activated.` 
      };
    }

    // Insufficient balance
    const paymentUrl = await getPaymentLink(userId, 5);
    
    return { 
      allowed: false,
      balance: result.balance,
      paymentUrl,
      message: `❌ Insufficient balance.\n\n📊 Pricing:\n• Per call: $${PRICE_PER_CALL} USDT\n\n💳 Recharge: ${paymentUrl}`
    };
  } catch (error) {
    console.error('Billing error:', error);
    // Graceful degradation - allow access if billing fails
    return { 
      allowed: true, 
      message: '⚠️ Billing system unavailable. Access granted.' 
    };
  }
}

/**
 * Get pricing info for display
 */
function getPricingInfo() {
  return {
    perCall: PRICE_PER_CALL,
    currency: 'USDT',
    chain: 'BNB Chain'
  };
}

module.exports = {
  checkBalance,
  checkPurchased,
  chargeUser,
  getPaymentLink,
  handleBilling,
  getPricingInfo,
  SKILL_ID,
  PRICE_PER_CALL
};
