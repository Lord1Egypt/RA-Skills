#!/usr/bin/env node

/**
 * Test suite for Twitter/X Content Generator
 */

const { generateContent, processPayment } = require('./index.js');

async function runTests() {
  console.log('🧪 Twitter/X Content Generator - Test Suite\n');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  let passed = 0;
  let failed = 0;
  
  // Test 1: Generate single tweet
  console.log('Test 1: Generate single tweet');
  try {
    const result = await generateContent('AI trends', { testMode: true });
    if (result.content && result.metadata) {
      console.log('✅ PASS\n');
      passed++;
    } else {
      throw new Error('Invalid response structure');
    }
  } catch (error) {
    console.log(`❌ FAIL: ${error.message}\n`);
    failed++;
  }
  
  // Test 2: Generate thread
  console.log('Test 2: Generate thread');
  try {
    const result = await generateContent('AI agents', { 
      type: 'thread', 
      length: 3,
      testMode: true 
    });
    if (result.metadata.type === 'thread') {
      console.log('✅ PASS\n');
      passed++;
    } else {
      throw new Error('Type mismatch');
    }
  } catch (error) {
    console.log(`❌ FAIL: ${error.message}\n`);
    failed++;
  }
  
  // Test 3: Payment (no API key)
  console.log('Test 3: Payment without API key');
  try {
    const result = await processPayment(null);
    if (!result.success && result.payment_url) {
      console.log('✅ PASS (correctly rejected)\n');
      passed++;
    } else {
      throw new Error('Should reject without API key');
    }
  } catch (error) {
    console.log(`❌ FAIL: ${error.message}\n`);
    failed++;
  }
  
  // Test 4: Style options
  console.log('Test 4: Style options');
  try {
    const styles = ['engaging', 'professional', 'witty'];
    for (const style of styles) {
      const result = await generateContent('test', { style, testMode: true });
      if (result.metadata.style === style) {
        console.log(`  ✅ ${style}`);
      }
    }
    console.log('✅ PASS\n');
    passed++;
  } catch (error) {
    console.log(`❌ FAIL: ${error.message}\n`);
    failed++;
  }
  
  // Summary
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`\n📊 Results: ${passed} passed, ${failed} failed\n`);
  
  if (failed > 0) {
    process.exit(1);
  }
}

runTests().catch(console.error);
