const BILLING_API_URL = "https://skillpay.me";
const API_KEY = "sk_187d1b61740f75f3376e45acc2c45c408980294f16c6fa75df8d826b8f6d9174";
const SKILL_ID = "1c276e55-d742-42e5-9220-84ce214f87df";
const PRICE_PER_CALL = 0.001;

const headers = { "X-API-Key": API_KEY, "Content-Type": "application/json" };

export async function charge(userId) {
  try {
    const res = await fetch(`${BILLING_API_URL}/api/v1/billing/charge`, {
      method: "POST",
      headers,
      body: JSON.stringify({ user_id: userId, skill_id: SKILL_ID, amount: PRICE_PER_CALL }),
      signal: AbortSignal.timeout(10000),
    });

    const data = await res.json();

    if (data.success) {
      return { success: true, balance: data.balance };
    }

    return {
      success: false,
      balance: data.balance ?? null,
      payment_url: data.payment_url || null,
      error: data.message || `Charge failed (HTTP ${res.status})`,
    };
  } catch (err) {
    return { success: false, error: `Billing request failed: ${err.message}` };
  }
}

export async function getBalance(userId) {
  try {
    const res = await fetch(
      `${BILLING_API_URL}/api/v1/billing/balance?user_id=${encodeURIComponent(userId)}`,
      { headers: { "X-API-Key": API_KEY }, signal: AbortSignal.timeout(10000) },
    );
    const data = await res.json();
    return { success: true, balance: data.balance };
  } catch (err) {
    return { success: false, error: err.message };
  }
}

export async function getPaymentLink(userId, amount = 8) {
  try {
    const res = await fetch(`${BILLING_API_URL}/api/v1/billing/payment-link`, {
      method: "POST",
      headers,
      body: JSON.stringify({ user_id: userId, amount }),
      signal: AbortSignal.timeout(10000),
    });

    const data = await res.json();
    return { success: true, payment_url: data.payment_url };
  } catch (err) {
    return { success: false, error: err.message };
  }
}
