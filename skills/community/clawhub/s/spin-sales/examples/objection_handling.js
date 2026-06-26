#!/usr/bin/env node

/**
 * Spin-Skills技能异议处理示例
 * 演示如何处理常见的销售异议
 */

import SpinSalesSkill from '../index.js';

// 常见异议类型
const OBJECTION_SCENARIOS = [
  {
    type: "budget",
    objection: "你们的价格太贵了，超出了我们的预算",
    context: "在价值确认阶段，客户提出价格异议"
  },
  {
    type: "time", 
    objection: "我们现在很忙，没时间做决策",
    context: "在影响放大阶段，客户提出时间异议"
  },
  {
    type: "trust",
    objection: "我对你们的经验有些疑虑，能保证成功吗？",
    context: "在痛点挖掘阶段，客户提出信任异议"
  },
  {
    type: "feature",
    objection: "这个功能我们现有产品也可以实现啊",
    context: "在现状调研阶段，客户提出功能替代异议"
  }
];

async function runObjectionDemo() {
  console.log("🛡️ Spin-Sales技能异议处理示例");
  console.log("=" .repeat(50));
  
  // 初始化技能
  const spinSales = new SpinSalesSkill();
  await spinSales.initialize();
  
  // 模拟SPIN流程进行到某个阶段
  await spinSales.executeStage("situation");
  await spinSales.executeStage("problem");
  
  console.log("\n🎯 当前进度: 已完成S-P阶段，准备进入I阶段");
  console.log("📋 模拟对话历史已建立");
  
  // 测试各种异议场景
  for (const scenario of OBJECTION_SCENARIOS) {
    console.log(`\n🔄 测试${scenario.type}异议:`);
    console.log(`💬 客户说: "${scenario.objection}"`);
    console.log(`📍 上下文: ${scenario.context}`);
    
    // 处理异议
    const result = await spinSales.handleObjection(scenario.objection);
    
    if (result.success) {
      console.log("✅ 异议处理成功");
      console.log("📝 顾问回应:");
      console.log(result.response);
      
      if (result.continueFlow) {
        console.log("🔄 继续SPIN流程...");
      }
    } else {
      console.error("❌ 异议处理失败:", result.error);
    }
    
    console.log("-" .repeat(30));
  }
  
  // 演示异议处理后的流程继续
  console.log("\n🚀 继续完成剩余SPIN流程:");
  
  // 继续I阶段
  const implicationResult = await spinSales.executeStage("implication");
  if (implicationResult.success) {
    console.log("✅ 影响放大阶段完成");
  }
  
  // 继续N阶段
  const needPayoffResult = await spinSales.executeStage("need-payoff");
  if (needPayoffResult.success) {
    console.log("✅ 价值确认阶段完成");
  }
  
  // 生成最终行动计划
  const actionPlanResult = await spinSales.generateActionPlan();
  if (actionPlanResult.success) {
    console.log("✅ 行动计划生成完成");
    
    console.log("\n📊 最终行动计划:");
    actionPlanResult.actionPlan.tasks.forEach((task, index) => {
      console.log(`${index + 1}. ${task.goal}`);
      console.log(`   任务: ${task.task}`);
      console.log(`   负责人: ${task.owner}`);
      console.log(`   截止日期: ${task.deadline}`);
      console.log(`   成功标准: ${task.metric}`);
      console.log();
    });
  }
  
  console.log("✅ 异议处理示例完成！");
}

// 运行示例
if (import.meta.url === `file://${process.argv[1]}`) {
  runObjectionDemo().catch(console.error);
}

export { runObjectionDemo };