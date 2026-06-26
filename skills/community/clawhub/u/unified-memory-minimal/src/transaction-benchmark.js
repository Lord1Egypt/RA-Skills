/**
 * Transaction System Performance Benchmark
 */

import { TransactionManager } from './transaction-system.js';

async function runBenchmark() {
  console.log('⚡ Transaction System Benchmark\n');
  
  const iterations = [10, 100, 500, 1000];
  
  for (const n of iterations) {
    const tm = new TransactionManager({
      walDir: `/tmp/bench-wal-${n}`,
      enableDeadlockDetection: false
    });
    
    const start = Date.now();
    
    // Batch transaction commits
    for (let i = 0; i < n; i++) {
      const txId = await tm.begin();
      await tm.execute(txId, { type: 'insert', memoryId: `mem_${i}`, data: { content: `Memory ${i}` } });
      await tm.commit(txId);
    }
    
    const duration = Date.now() - start;
    const tps = (n / duration * 1000).toFixed(2);
    const avgLatency = (duration / n).toFixed(2);
    
    console.log(`  ${n} transactions: ${duration}ms total, ${tps} TPS, ${avgLatency}ms avg latency`);
    
    tm.close();
  }
  
  console.log('\n✅ Benchmark completed');
}

runBenchmark().catch(console.error);
