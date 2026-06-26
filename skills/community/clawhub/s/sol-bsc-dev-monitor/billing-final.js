// ═══════════════════════════════════════════════════════════
// SkillPay Billing Integration
// スキルペイ決統合 / 결제 연동 / Интеграция биллинга

const axios = require('axios');

// Billing API URL / 課金API URL / Ссылка на API биллинга
const BILLING_API_URL = 'https://skillpay.me/api/v1/billing';
const API_KEY = 'sk_f072a786149bc07fc8730b4683dc00f3e050e72441922284ca803cdee2b994b5';
const SKILL_ID = '282279e4-5370-4b9e-b5e7-9e07f0b3dc5c';

// Headers / ヘッダー / Заголовки
const headers = {
  'X-API-Key': API_KEY,
  'Content-Type': 'application/json'
};

// Check balance / 查余额 / 残高 / 잔액 / Проверка баланса
async function checkBalance(userId) {
  try {
    const resp = await fetch(`${BILLING_API_URL}/balance?user_id=${userId}`, {
      method: 'GET',
      headers
    });
    
    const data = await resp.json();
    return data.balance || 0;
  } catch (error) {
    console.error('Balance check error:', error.message);
    return 0;
  }
}

// Charge per call / 扣费 / 每次调用扣费 / 呼び出しとの課金 / Списание за вызов
async function chargeUser(userId, amount = 0.005) {
  try {
    const resp = await fetch(`${BILLING_API_URL}/charge`, {
      method: 'POST',
      headers: {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: userId,
        skill_id: SKILL_ID,
        amount
      })
    });
    
    const data = await resp.json();
    
    if (data.success) {
      return { ok: true, balance: data.balance };
    }
    
    return { 
      ok: false, 
      balance: data.balance, 
      payment_url: data.payment_url 
    };
  } catch (error) {
    console.error('Billing error:', error.message);
    return { ok: false, error: error.message };
  }
}

// Generate payment link / 充值链接 / 入金リンク / 결제 링크 / Ссылка на оплату
async function getPaymentLink(userId, amount = 8) {
  try {
    const resp = await fetch(`${BILLING_API_URL}/payment-link`, {
      method: 'POST',
      headers: {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: userId,
        amount
      })
    });
    
    const data = await resp.json();
    return data.payment_url;
  } catch (error) {
    console.error('Payment link error:', error.message);
    return null;
  }
}

// Check and charge for monitoring session
async function checkAndCharge(userId) {
  const charge = await chargeUser(userId);
  
  if (charge.ok) {
    // ✅ Execute your skill / 执行你的 Skill
    return { success: true, balance: charge.balance };
  }
  
  // ❌ Insufficient / 余额不足 → payment link
  // 需要充值（最低 8 USDT = 8000 tokens）
  const paymentLink = await getPaymentLink(userId);
  
  return { 
    success: false, 
    balance: charge.balance,
    paymentUrl: paymentLink,
    message: `余额不足。最低充值: 8 USDT (8000 tokens)\n` +
             `充值链接: ${paymentLink}`
  };
}

module.exports = {
  checkBalance,
  chargeUser,
  getPaymentLink,
  checkAndCharge
};
