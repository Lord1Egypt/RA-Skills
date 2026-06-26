/**
 * Test Script for SkillPay Billing Integration
 * 
 * Run: node scripts/test-billing.js
 */

const BILLING_API_URL = 'https://skillpay.me';
const BILLING_API_KEY = 'sk_20cb7dd70ceaa244814a9e9a0e990a2781fab10e163fd2f9499f5bb1e7a6eaef';
const SKILL_ID = '6387f3fa-cceb-4a60-afd4-fc1f4eb2d7c3';

// Test user ID (use a dummy ID for testing)
const TEST_USER_ID = 'test-user-' + Date.now();

console.log('═══════════════════════════════════════════════════');
console.log('SkillPay Billing Integration Test');
console.log('═══════════════════════════════════════════════════');
console.log(`Skill ID: ${SKILL_ID}`);
console.log(`Test User: ${TEST_USER_ID}`);
console.log('═══════════════════════════════════════════════════\n');

// Test 1: Check Balance
async function testCheckBalance() {
  console.log('📋 Test 1: Check Balance');
  try {
    const resp = await fetch(
      `${BILLING_API_URL}/api/v1/billing/balance?user_id=${TEST_USER_ID}`,
      { headers: { 'X-API-Key': BILLING_API_KEY } }
    );
    const data = await resp.json();
    console.log('   Response:', JSON.stringify(data, null, 2));
    console.log('   Status:', resp.status === 200 ? '✅ PASS' : '❌ FAIL');
    return data;
  } catch (error) {
    console.log('   Error:', error.message);
    console.log('   Status: ❌ FAIL');
    return null;
  }
  console.log('');
}

// Test 2: Charge User
async function testChargeUser() {
  console.log('📋 Test 2: Charge User ($0.9 USDT)');
  try {
    const resp = await fetch(`${BILLING_API_URL}/api/v1/billing/charge`, {
      method: 'POST',
      headers: {
        'X-API-Key': BILLING_API_KEY,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: TEST_USER_ID,
        skill_id: SKILL_ID,
        amount: 0.9,
      }),
    });
    const data = await resp.json();
    console.log('   Response:', JSON.stringify(data, null, 2));
    console.log('   Status:', data.success ? '✅ PASS (Charged)' : '⚠️ EXPECTED (Insufficient balance for test user)');
    return data;
  } catch (error) {
    console.log('   Error:', error.message);
    console.log('   Status: ❌ FAIL');
    return null;
  }
  console.log('');
}

// Test 3: Get Payment Link
async function testPaymentLink() {
  console.log('📋 Test 3: Get Payment Link');
  try {
    const resp = await fetch(`${BILLING_API_URL}/api/v1/billing/payment-link`, {
      method: 'POST',
      headers: {
        'X-API-Key': BILLING_API_KEY,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        user_id: TEST_USER_ID, 
        amount: 10 
      }),
    });
    const data = await resp.json();
    console.log('   Response:', JSON.stringify(data, null, 2));
    console.log('   Status:', data.payment_url ? '✅ PASS' : '❌ FAIL');
    if (data.payment_url) {
      console.log('   Payment URL:', data.payment_url);
    }
    return data;
  } catch (error) {
    console.log('   Error:', error.message);
    console.log('   Status: ❌ FAIL');
    return null;
  }
  console.log('');
}

// Test 4: Check Access (Buyout)
async function testCheckAccess() {
  console.log('📋 Test 4: Check Access (Buyout Status)');
  try {
    const resp = await fetch(
      `${BILLING_API_URL}/api/v1/billing/access?user_id=${TEST_USER_ID}&skill_id=${SKILL_ID}`,
      { headers: { 'X-API-Key': BILLING_API_KEY } }
    );
    const data = await resp.json();
    console.log('   Response:', JSON.stringify(data, null, 2));
    console.log('   Status:', resp.status === 200 ? '✅ PASS' : '❌ FAIL');
    return data;
  } catch (error) {
    console.log('   Error:', error.message);
    console.log('   Status: ❌ FAIL (API may not support /access endpoint)');
    return null;
  }
  console.log('');
}

// Run all tests
async function runTests() {
  await testCheckBalance();
  await testChargeUser();
  await testPaymentLink();
  await testCheckAccess();
  
  console.log('═══════════════════════════════════════════════════');
  console.log('Test Complete');
  console.log('═══════════════════════════════════════════════════');
}

runTests().catch(console.error);
