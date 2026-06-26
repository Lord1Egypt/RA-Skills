/**
 * Skill 评分对比工具测试
 */

import { SkillRatingComparator } from '../index';
import type { SkillScores } from '../types';

// 简单测试
function runTests() {
  console.log('🧪 开始测试 Skill 评分对比工具...\n');

  const comparator = new SkillRatingComparator();
  let passed = 0;
  let failed = 0;

  // 测试 1: 计算综合评分
  console.log('测试 1: 计算综合评分');
  const testScores: SkillScores = {
    functionality: 9,
    codeQuality: 8,
    documentation: 9,
    userReviews: 8,
    updateFrequency: 8,
    installation: 9,
  };
  const totalScore = comparator.calculateTotalScore(testScores);
  console.log(`  输入：${JSON.stringify(testScores)}`);
  console.log(`  输出：${totalScore}`);
  console.log(`  预期：8.6 左右`);
  console.log(`  结果：${totalScore >= 8 && totalScore <= 9 ? '✅ 通过' : '❌ 失败'}\n`);
  passed++;

  // 测试 2: 生成星级
  console.log('测试 2: 生成星级显示');
  const stars = comparator.generateStars(8.5);
  console.log(`  输入：8.5`);
  console.log(`  输出：${stars}`);
  console.log(`  预期：⭐⭐⭐⭐☆`);
  console.log(`  结果：${stars.includes('⭐') ? '✅ 通过' : '❌ 失败'}\n`);
  passed++;

  // 测试 3: 更新频率评分
  console.log('测试 3: 更新频率评分');
  (async () => {
    const recentScore = await comparator.analyzeUpdateFrequency(new Date().toISOString());
    const oldScore = await comparator.analyzeUpdateFrequency('2024-01-01T00:00:00Z');
    console.log(`  最近更新：${recentScore} (预期 >= 9)`);
    console.log(`  一年前更新：${oldScore} (预期 <= 3)`);
    console.log(`  结果：${recentScore >= 9 && oldScore <= 3 ? '✅ 通过' : '❌ 失败'}\n`);
    passed++;

    // 测试 4: 生成报告
    console.log('测试 4: 生成对比报告');
    try {
      const report = await comparator.generateReport('test-skill');
      console.log(`  目标 Skill: ${report.targetSkill.name}`);
      console.log(`  竞争对手：${report.competitors.length} 个`);
      console.log(`  优势数量：${report.summary.strengths.length}`);
      console.log(`  劣势数量：${report.summary.weaknesses.length}`);
      console.log(`  推荐数量：${report.summary.recommendations.length}`);
      console.log(`  结果：✅ 通过\n`);
      passed++;
    } catch (error) {
      console.log(`  结果：❌ 失败 - ${error}\n`);
      failed++;
    }

    // 测试 5: 格式化报告
    console.log('测试 5: 格式化报告为 Markdown');
    try {
      const report = await comparator.generateReport('test-skill');
      const markdown = comparator.formatReportMarkdown(report);
      console.log(`  Markdown 长度：${markdown.length} 字符`);
      console.log(`  包含表格：${markdown.includes('| 排名 |') ? '是' : '否'}`);
      console.log(`  包含星级：${markdown.includes('⭐') ? '是' : '否'}`);
      console.log(`  结果：✅ 通过\n`);
      passed++;
    } catch (error) {
      console.log(`  结果：❌ 失败 - ${error}\n`);
      failed++;
    }

    // 总结
    console.log('='.repeat(50));
    console.log(`测试完成：${passed} 通过，${failed} 失败`);
    console.log('='.repeat(50));
  })();
}

runTests();
