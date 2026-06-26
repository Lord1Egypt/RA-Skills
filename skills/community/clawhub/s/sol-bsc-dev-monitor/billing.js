// ═════════════════════════════════════════════════════════════
// SkillPay Billing Integration
// スキルペイ決統合 / 결제 연동 / Интеграция биллинга SkillPay
// ═══════════════════════════════════════════════════════════════════

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

// Check balance / 残高確認 / Проверка баланса
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

// Charge per call / 呼び出し / Списание за вызов
async function chargeUser(userId, amount = 0.005) {
  try {
    const resp = await fetch(`${BILLING_API_URL}/charge`, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({
        user_id: userId,
        skill_id: SKILL_ID,
        amount: amount
      })
    });
    const data = await resp.json();
    return {
      ok: data.success,
      balance: data.balance,
      paymentUrl: data.payment_url
    };
  } catch (error) {
    console.error('Charge error:', error.message);
    return {
      ok: false,
      balance: 0,
      error: error.message
    };
  }
}

// Generate payment link / 入金リンク生成 / Создание ссылки на оплату
async function getPaymentLink(userId, amount = 8) {
  try {
    const resp = await fetch(`${BILLING_API_URL}/payment-link`, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({
        user_id: userId,
        amount: amount
      })
    });
    const data = await resp.json();
    return data.payment_url;
  } catch (error) {
    console.error('Payment link error:', error.message);
    return null;
  }
}

module.exports = {
  checkBalance,
  chargeUser,
  getPaymentLink
};
