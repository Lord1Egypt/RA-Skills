#!/usr/bin/env node

/**
 * Spin-Sales技能基础使用示例
 * 演示如何使用SPIN销售法进行完整的销售对话流程
 */

import SpinSalesSkill from '../index.js';

async function runBasicDemo() {
  console.log("🎯 Spin-Sales技能基础使用示例");
  console.log("=" .repeat(50));
  
  // 初始化技能
  const spinSales = new SpinSalesSkill();
  await spinSales.initialize();
  
  // 1. 执行开场白
  console.log("\n🚀 步骤1: 执行开场白");
  const openingResult = await spinSales.executeOpening();
  if (openingResult.success) {
    console.log("✅ 开场白执行成功");
    console.log("📝 开场白内容:", openingResult.message);
  } else {
    console.error("❌ 开场白执行失败:", openingResult.error);
    return;
  }
  
  // 2. 执行现状调研(S阶段)
  console.log("\n📊 步骤2: 执行现状调研(S阶段)");
  const situationResult = await spinSales.executeStage("situation");
  if (situationResult.success) {
    console.log("✅ 现状调研执行成功");
    console.log("📋 提问数量:", situationResult.questions.length);
    situationResult.questions.forEach((section, index) => {
      console.log(`  ${index + 1}. ${section.section}: ${section.questions.length}个问题`);
    });
  } else {
    console.error("❌ 现状调研执行失败:", situationResult.error);
    return;
  }
  
  // 3. 执行痛点挖掘(P阶段)
  console.log("\n🎯 步骤3: 执行痛点挖掘(P阶段)");
  const problemResult = await spinSales.executeStage("problem");
  if (problemResult.success) {
    console.log("✅ 痛点挖掘执行成功");
    console.log("📋 提问数量:", problemResult.questions.length);
  } else {
    console.error("❌ 痛点挖掘执行失败:", problemResult.error);
    return;
  }
  
  // 4. 执行影响放大(I阶段)
  console.log("\n💥 步骤4: 执行影响放大(I阶段)");
  const implicationResult = await spinSales.executeStage("implication");
  if (implicationResult.success) {
    console.log("✅ 影响放大执行成功");
    console.log("📋 提问数量:", implicationResult.questions.length);
  } else {
    console.error("❌ 影响放大执行失败:", implicationResult.error);
    return;
  }
  
  // 5. 执行价值确认(N阶段)
  console.log("\n💰 步骤5: 执行价值确认(N阶段)");
  const needPayoffResult = await spinSales.executeStage("need-payoff");
  if (needPayoffResult.success) {
    console.log("✅ 价值确认执行成功");
    console.log("📋 提问数量:", needPayoffResult.questions.length);
  } else {
    console.error("❌ 价值确认执行失败:", needPayoffResult.error);
    return;
  }
  
  // 6. 生成行动计划
  console.log("\n📋 步骤6: 生成行动计划");
  const actionPlanResult = await spinSales.generateActionPlan();
  if (actionPlanResult.success) {
    console.log("✅ 行动计划生成成功");
    console.log("📋 计划包含", actionPlanResult.actionPlan.tasks.length, "个任务");
    
    // 打印行动计划表格
    console.log("\n📊 行动计划表格:");
    console.log("| 目标 | 任务 | 负责人 | 截止日期 | 成功标准 |");
    console.log("|------|------|--------|----------|----------|");
    actionPlanResult.actionPlan.tasks.forEach(task => {
      console.log(`| ${task.goal} | ${task.task} | ${task.owner} | ${task.deadline} | ${task.metric} |`);
    });
  } else {
    console.error("❌ 行动计划生成失败:", actionPlanResult.error);
    return;
  }
  
  // 7. 显示最终状态
  console.log("\n🎉 最终状态:");
  const status = spinSales.getStatus();
  console.log("📊 当前阶段:", status.currentStage);
  console.log("💬 对话历史:", status.conversationHistory, "条记录");
  console.log("📋 行动计划:", status.actionPlan);
  console.log("🔄 下一个阶段:", status.nextStage);
  
  console.log("\n✅ Spin-Sales技能基础使用示例完成！");
}

// 运行示例
if (import.meta.url === `file://${process.argv[1]}`) {
  runBasicDemo().catch(console.error);
}

export { runBasicDemo };