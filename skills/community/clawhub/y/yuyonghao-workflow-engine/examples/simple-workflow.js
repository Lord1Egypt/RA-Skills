/**
 * Workflow Engine - 简单顺序工作流示例
 */

import { WorkflowEngine } from '../src/workflow-engine.js';

async function main() {
  console.log('🔄 Simple Sequential Workflow Example\n');

  const engine = new WorkflowEngine();

  // 创建一个简单的数据处理工作流
  const workflow = engine.createSequentialWorkflow('Data Processing', [
    {
      name: 'Fetch Data',
      execute: async (context) => {
        console.log('📥 Fetching data...');
        await new Promise(r => setTimeout(r, 500));
        context.data = { users: ['Alice', 'Bob', 'Charlie'] };
        return { fetched: 3 };
      }
    },
    {
      name: 'Process Data',
      execute: async (context) => {
        console.log('⚙️ Processing data...');
        await new Promise(r => setTimeout(r, 500));
        context.data.processed = context.data.users.map(u => u.toUpperCase());
        return { processed: 3 };
      }
    },
    {
      name: 'Save Results',
      execute: async (context) => {
        console.log('💾 Saving results...');
        await new Promise(r => setTimeout(r, 500));
        console.log('Results:', context.data.processed);
        return { saved: true };
      }
    }
  ]);

  console.log('Workflow created:', workflow.name);
  console.log('Nodes:', workflow.nodes.size);
  console.log('');

  // 执行工作流
  const result = await engine.execute(workflow.id, {});

  console.log('\n✅ Workflow completed!');
  console.log('Status:', result.status);
  console.log('Duration:', result.duration, 'ms');
  console.log('Results:', JSON.stringify(result.results, null, 2));
}

main().catch(console.error);
