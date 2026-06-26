#!/usr/bin/env node
/**
 * 测试 Skills CLI Wrapper
 */

const { skillsList, skillsFind, parseFindOutput } = require('./skills-cli');

async function main() {
  console.log('=== Skills CLI Wrapper 测试 ===\n');

  // 测试 1: list
  console.log('1. 测试 skillsList()');
  console.log('-'.repeat(50));
  try {
    const installed = await skillsList({ global: true });
    console.log(`✅ 找到 ${installed.length} 个已安装 skill:`);
    installed.forEach((s) => console.log(`   - ${s.name}`));
  } catch (e) {
    console.error('❌ 失败:', e.message);
  }

  // 测试 2: find
  console.log('\n2. 测试 skillsFind("react")');
  console.log('-'.repeat(50));
  try {
    const results = await skillsFind('react');
    console.log(`✅ 找到 ${results.length} 个结果:`);
    results.slice(0, 3).forEach((r) => {
      console.log(`   - ${r.fullName} (${r.installs} installs)`);
    });
  } catch (e) {
    console.error('❌ 失败:', e.message);
  }

  // 测试 3: parseFindOutput
  console.log('\n3. 测试 parseFindOutput()');
  console.log('-'.repeat(50));
  const sampleOutput = `
[38;5;145mvercel-labs/json-render@react[0m [36m728 installs[0m
[38;5;102m└ https://skills.sh/vercel-labs/json-render/react[0m
[38;5;145mvercel-labs/agent-skills@best-practices[0m [36m1520 installs[0m
`;
  const parsed = parseFindOutput(sampleOutput);
  console.log(`✅ 解析 ${parsed.length} 条:`);
  parsed.forEach((p) => console.log(`   - ${p.fullName}: ${p.installs}`));
}

main().catch(console.error);
