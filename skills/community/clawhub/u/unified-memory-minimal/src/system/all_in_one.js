/**
 * All-in-One CLI Entry Point
 */

import { createApiServer } from '../api/api.js';
import { printAnalytics } from '../quality/analytics.js';
import { printAudit } from '../quality/audit.js';
import { printQualityReport } from '../quality/quality.js';
import { autoTune } from '../core/adaptive.js';
import { printHierarchyReport, rebalanceTiers } from '../core/hierarchy.js';
import { runReflectionCycle } from '../core/reflection.js';
import { preheat } from '../system/preheat.js';
import { printDecayAnalysis } from '../quality/weibull_decay.js';
import { getMemories } from '../storage.js';

function printHelp() {
  console.log('\n🧠 Unified Memory CLI\n');
  console.log('Usage: all <command> [options]\n');
  console.log('Commands:');
  console.log('  store <text>     Store a new memory');
  console.log('  search <query>    Search memories');
  console.log('  list              List all memories');
  console.log('  stats             Show memory statistics');
  console.log('  analytics         Generate analytics report');
  console.log('  quality           Assess memory quality');
  console.log('  audit             Show audit log');
  console.log('  adaptive          Run adaptive tuning');
  console.log('  hierarchy         Show memory hierarchy');
  console.log('  reflect           Run reflection cycle');
  console.log('  decay             Analyze decay');
  console.log('  preheat           Preheat hot memories');
  console.log('  api               Start API server');
  console.log('  full-report       Generate complete report');
  console.log('');
}

export async function runCommand(args) {
  const [cmd, ...rest] = args;
  
  switch (cmd) {
    case 'stats':
      const memories = getMemories({ limit: 100 });
      console.log(`\n📊 Total memories: ${memories.length}\n`);
      break;
    case 'analytics': printAnalytics(); break;
    case 'quality': printQualityReport(); break;
    case 'audit': printAudit(); break;
    case 'adaptive': autoTune(); break;
    case 'hierarchy': printHierarchyReport(); break;
    case 'rebalance': rebalanceTiers(); break;
    case 'reflect': runReflectionCycle(); break;
    case 'decay': printDecayAnalysis(); break;
    case 'preheat': preheat(); break;
    case 'api':
      const port = parseInt(rest.find(a => a.startsWith('--port='))?.split('=')[1] || '37888', 10);
      createApiServer(port);
      break;
    case 'full-report':
      console.log('\n📊 Full Memory Report\n');
      const mems = getMemories({ limit: 100 });
      console.log(`  Total Memories: ${mems.length}`);
      printAnalytics();
      printQualityReport();
      break;
    default:
      console.log(`Unknown command: ${cmd}`);
      printHelp();
  }
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0 || args[0] === 'help') printHelp();
  else runCommand(args).catch(err => { console.error('Error:', err.message); process.exit(1); });
}
