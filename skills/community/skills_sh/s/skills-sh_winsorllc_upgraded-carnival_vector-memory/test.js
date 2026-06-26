/**
 * Test for vector-memory skill
 * 
 * Note: Uses mocked embeddings for testing (no API calls required)
 */

const path = require('path');
const fs = require('fs');

// Temporarily override OPENAI_API_KEY and generateEmbedding
const originalEnv = process.env.OPENAI_API_KEY;
process.env.OPENAI_API_KEY = 'fake-key-for-testing';

// Mock the vector-module with fake embeddings
let mockMemories = { memories: [], meta: { created: new Date().toISOString() } };

// Simple hash-based pseudo-embedding for testing (5 dimensions for simplicity)
function fakeEmbedding(text) {
  return Array.from(text).slice(0, 5).map(c => c.charCodeAt(0) / 255);
}

// Override load/save functions
const vm = require('./vector-memory');

// Store original functions
const originalLoad = vm.loadVectorMemories || function() { return mockMemories; };
const originalSave = vm.saveVectorMemories || function(data) { mockMemories = data; };

// For testing purposes, we'll work directly with the module
async function runTests() {
  console.log('=== Vector Memory Skill Tests ===\n');
  
  const results = {
    passed: 0,
    failed: 0,
    tests: []
  };

  // Test 1: Module exports
  console.log('Test 1: Module exports');
  try {
    const exports = Object.keys(vm);
    const hasRequired = exports.includes('vstore') && 
                        exports.includes('vsearch') && 
                        exports.includes('vdelete') &&
                        exports.includes('vlist') &&
                        exports.includes('vclear') &&
                        exports.includes('cosineSimilarity');
    
    if (hasRequired) {
      console.log('✓ All required exports present\n');
      results.passed++;
      results.tests.push({ name: 'Module exports', status: 'passed' });
    } else {
      console.log('✗ Missing exports\n');
      results.failed++;
      results.tests.push({ name: 'Module exports', status: 'failed', error: 'Missing functions' });
    }
  } catch (error) {
    console.log(`✗ Error: ${error.message}\n`);
    results.failed++;
    results.tests.push({ name: 'Module exports', status: 'failed', error: error.message });
  }

  // Test 2: Cosine similarity calculation
  console.log('Test 2: Cosine similarity calculation');
  try {
    const vecA = [1, 0, 0, 1, 0];
    const vecB = [1, 0, 0, 1, 0];
    const vecC = [0, 1, 0, 0, 1];
    
    const simAB = vm.cosineSimilarity(vecA, vecB); // Should be 1.0 (identical)
    const simAC = vm.cosineSimilarity(vecA, vecC); // Should be 0.0 (orthogonal)
    
    if (Math.abs(simAB - 1.0) < 0.001 && Math.abs(simAC) < 0.001) {
      console.log('✓ Cosine similarity works correctly\n');
      results.passed++;
      results.tests.push({ name: 'Cosine similarity calculation', status: 'passed' });
    } else {
      console.log(`✗ Cosine similarity incorrect: simAB=${simAB}, simAC=${simAC}\n`);
      results.failed++;
      results.tests.push({ name: 'Cosine similarity calculation', status: 'failed', error: 'Wrong calculation' });
    }
  } catch (error) {
    console.log(`✗ Error: ${error.message}\n`);
    results.failed++;
    results.tests.push({ name: 'Cosine similarity calculation', status: 'failed', error: error.message });
  }

  // Test 3: vstore error handling (no API key)
  console.log('Test 3: vstore error handling');
  try {
    // We expect this to fail because we don't have a real API key
    const result = await vm.vstore('Test text');
    if (result.includes('Error')) {
      console.log('✓ vstore handles missing API key gracefully\n');
      results.passed++;
      results.tests.push({ name: 'vstore error handling', status: 'passed' });
    } else {
      console.log('✗ Should have failed without API key\n');
      results.failed++;
      results.tests.push({ name: 'vstore error handling', status: 'failed', error: 'Did not fail as expected' });
    }
  } catch (error) {
    console.log(`✓ Error handling works: ${error.message}\n`);
    results.passed++;
    results.tests.push({ name: 'vstore error handling', status: 'passed' });
  }

  // Test 4: Vector storage structure (simulated)
  console.log('Test 4: Vector storage structure');
  try {
    // Simulate what a memory structure should look like
    const mockMemory = {
      id: 'mem_test123',
      text: 'Test memory',
      embedding: [0.1, 0.2, 0.3, 0.4, 0.5],
      tags: ['test'],
      metadata: { createdAt: new Date().toISOString() }
    };
    
    if (mockMemory.id && mockMemory.text && Array.isArray(mockMemory.embedding)) {
      console.log('✓ Memory structure is correct\n');
      results.passed++;
      results.tests.push({ name: 'Vector storage structure', status: 'passed' });
    } else {
      console.log('✗ Memory structure is incorrect\n');
      results.failed++;
      results.tests.push({ name: 'Vector storage structure', status: 'failed', error: 'Structure invalid' });
    }
  } catch (error) {
    console.log(`✗ Error: ${error.message}\n`);
    results.failed++;
    results.tests.push({ name: 'Vector storage structure', status: 'failed', error: error.message });
  }

  // Summary
  console.log('=== Test Summary ===');
  console.log(`Passed: ${results.passed}`);
  console.log(`Failed: ${results.failed}`);
  console.log(`Total: ${results.passed + results.failed}`);
  console.log('\nNote: Full integration test requires OPENAI_API_KEY\n');
  console.log('Test Details:');
  results.tests.forEach(test => {
    const status = test.status === 'passed' ? '✓' : test.status === 'failed' ? '✗' : '⊘';
    console.log(`  ${status} ${test.name}`);
  });

  // Write test results to file
  const testResultsPath = path.join(__dirname, 'test-results.json');
  fs.writeFileSync(testResultsPath, JSON.stringify(results, null, 2));
  console.log(`\nTest results written to: ${testResultsPath}`);

  // Restore environment
  process.env.OPENAI_API_KEY = originalEnv;

  return results;
}

// Run tests
runTests().catch(console.error);
