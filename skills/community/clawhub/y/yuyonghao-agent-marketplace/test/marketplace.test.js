/**
 * Agent Marketplace Test Suite
 */

const { CatalogManager, RatingSystem, SearchEngine, RegistryManager } = require('../src');

class TestRunner {
  constructor() {
    this.tests = [];
    this.passed = 0;
    this.failed = 0;
  }

  test(name, fn) {
    this.tests.push({ name, fn });
  }

  async run() {
    console.log('\n🧪 Running Agent Marketplace Tests\n');
    console.log('=' .repeat(50));
    
    for (const { name, fn } of this.tests) {
      try {
        await fn();
        console.log(`✅ PASS: ${name}`);
        this.passed++;
      } catch (error) {
        console.log(`❌ FAIL: ${name}`);
        console.log(`   Error: ${error.message}`);
        this.failed++;
      }
    }
    
    console.log('=' .repeat(50));
    console.log(`\n📊 Results: ${this.passed} passed, ${this.failed} failed`);
    console.log(`Success Rate: ${((this.passed / this.tests.length) * 100).toFixed(1)}%\n`);
    
    return this.failed === 0;
  }

  assert(condition, message) {
    if (!condition) throw new Error(message || 'Assertion failed');
  }

  assertEquals(actual, expected, message) {
    if (actual !== expected) throw new Error(message || `Expected ${expected}, got ${actual}`);
  }
}

const runner = new TestRunner();

// Test 1: CatalogManager Creation
runner.test('CatalogManager should be created', () => {
  const cm = new CatalogManager({
    registry: 'https://clawhub.com/registry',
    dataDir: './test-cache'
  });
  
  runner.assert(cm, 'CatalogManager should be created');
});

// Test 2: RatingSystem Creation
runner.test('RatingSystem should be created', () => {
  const rs = new RatingSystem();
  runner.assert(rs, 'RatingSystem should be created');
});

// Test 3: SearchEngine Creation
runner.test('SearchEngine should be created', () => {
  const se = new SearchEngine();
  runner.assert(se, 'SearchEngine should be created');
});

// Test 4: RegistryManager Creation
runner.test('RegistryManager should be created', () => {
  const rm = new RegistryManager({ registry: 'https://clawhub.com' });
  runner.assert(rm, 'RegistryManager should be created');
});

// Test 5: CatalogManager Config
runner.test('CatalogManager should accept config', () => {
  const cm = new CatalogManager({
    registry: 'https://test.com',
    dataDir: './test-dir'
  });
  
  runner.assertEquals(cm.registry, 'https://test.com', 'Should accept registry config');
});

// Test 6: RatingSystem Config
runner.test('RatingSystem should accept config', () => {
  const rs = new RatingSystem({ dataDir: './test-ratings' });
  
  runner.assert(typeof rs.dataDir === 'string', 'Should have dataDir');
});

// Test 7: SearchEngine Config
runner.test('SearchEngine should accept config', () => {
  const se = new SearchEngine({ dataDir: './test-search' });
  
  runner.assert(typeof se.dataDir === 'string', 'Should have dataDir');
});

// Test 8: RegistryManager Config
runner.test('RegistryManager should accept config', () => {
  const rm = new RegistryManager({ registry: 'https://registry.example.com', timeout: 5000 });
  
  runner.assertEquals(rm.registryUrl, 'https://registry.example.com', 'Should have registry URL');
});

// Test 9: CatalogManager has methods
runner.test('CatalogManager should have required methods', () => {
  const cm = new CatalogManager({ dataDir: './test-cache' });
  
  runner.assert(typeof cm.getCategories === 'function', 'Should have getCategories method');
});

// Test 10: RatingSystem has methods
runner.test('RatingSystem should have required methods', () => {
  const rs = new RatingSystem();
  
  runner.assert(typeof rs.submitRating === 'function', 'Should have submitRating method');
});

// Test 11: SearchEngine has methods
runner.test('SearchEngine should have required methods', () => {
  const se = new SearchEngine();
  
  runner.assert(typeof se.search === 'function', 'Should have search method');
});

// Test 12: RegistryManager has methods
runner.test('RegistryManager should have required methods', () => {
  const rm = new RegistryManager({ registry: 'https://test.com' });
  
  runner.assert(typeof rm.listSkills === 'function', 'Should have listSkills method');
});

// Run tests
runner.run().then(success => {
  process.exit(success ? 0 : 1);
});
