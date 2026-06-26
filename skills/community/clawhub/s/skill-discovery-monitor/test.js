const axios = require('axios');

/**
 * Test script for Skill Discovery Monitor
 */
async function testSkill() {
  const baseURL = 'http://localhost:3000';

  console.log('🧪 Testing Skill Discovery Monitor\n');

  // 1. Health check
  console.log('1. Health Check...');
  try {
    const health = await axios.get(`${baseURL}/health`);
    console.log('✅ Health check passed:', health.data);
  } catch (error) {
    console.error('❌ Health check failed:', error.message);
    return;
  }

  // 2. Test discover endpoint
  console.log('\n2. Testing /discover endpoint...');
  try {
    const discover = await axios.get(`${baseURL}/discover?limit=5`);
    console.log(`✅ Discovered ${discover.data.count} skills`);
    if (discover.data.data.length > 0) {
      console.log(`   Top skill: ${discover.data.data[0].name} (${discover.data.data[0].platform})`);
    }
  } catch (error) {
    console.error('❌ Discover test failed:', error.message);
  }

  // 3. Test platform-specific endpoint
  console.log('\n3. Testing /platform/clawhub endpoint...');
  try {
    const platform = await axios.get(`${baseURL}/platform/clawhub?limit=3`);
    console.log(`✅ Fetched ${platform.data.count} Clawhub skills`);
  } catch (error) {
    console.error('❌ Platform test failed:', error.message);
  }

  // 4. Test notify endpoint (will fail without payment)
  console.log('\n4. Testing /notify endpoint...');
  try {
    const notify = await axios.post(`${baseURL}/notify`, {
      userId: 'test-user-123',
      transactionId: 'test-tx-456',
      channels: {
        telegram: { chatId: 'test-chat-id' }
      },
      limit: 3
    });
    console.log('✅ Notify test:', notify.data);
  } catch (error) {
    console.log('⚠️  Notify test (expected to fail without valid payment):', error.response?.data || error.message);
  }

  // 5. Test subscription
  console.log('\n5. Testing /subscribe endpoint...');
  try {
    const subscribe = await axios.post(`${baseURL}/subscribe`, {
      userId: 'test-user-123',
      channels: {
        telegram: { chatId: 'test-chat-id' }
      },
      preferences: {
        categories: ['ai', 'productivity'],
        platforms: ['clawhub', 'github'],
        limit: 5
      }
    });
    console.log('✅ Subscription created:', subscribe.data);
  } catch (error) {
    console.error('❌ Subscription failed:', error.response?.data || error.message);
  }

  // 6. Check subscription status
  console.log('\n6. Checking subscription status...');
  try {
    const status = await axios.get(`${baseURL}/subscription/test-user-123`);
    console.log('✅ Subscription status:', status.data);
  } catch (error) {
    console.error('❌ Status check failed:', error.response?.data || error.message);
  }

  // 7. Test unsubscribe
  console.log('\n7. Testing /unsubscribe endpoint...');
  try {
    const unsubscribe = await axios.post(`${baseURL}/unsubscribe`, {
      userId: 'test-user-123'
    });
    console.log('✅ Unsubscribed:', unsubscribe.data);
  } catch (error) {
    console.error('❌ Unsubscribe failed:', error.response?.data || error.message);
  }

  console.log('\n✨ Test completed!\n');
}

// Run tests
if (require.main === module) {
  testSkill().catch(console.error);
}

module.exports = testSkill;
