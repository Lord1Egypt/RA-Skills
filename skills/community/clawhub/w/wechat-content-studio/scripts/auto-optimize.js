#!/usr/bin/env node

/**
 * 自动优化排版模块（仅排版，不发布）
 * 排版已由 wechat-typeset-pro 接管，本模块做 Markdown 级别的预处理优化
 */

import fs from 'fs';

/**
 * 自动优化文章排版（仅排版，不发布）
 * @param {string} articlePath - 文章路径
 * @param {Object} options - 优化选项
 * @returns {boolean} 是否优化成功
 */
export async function autoOptimizeLayout(articlePath, options = {}) {
  const { maxIterations = 5 } = options;
  
  console.log('\n🎨 开始自动优化排版...');
  console.log('━'.repeat(50));
  
  let currentVersion = 0;
  let success = false;
  
  while (currentVersion < maxIterations && !success) {
    currentVersion++;
    console.log(`\n🔄 第 ${currentVersion}/${maxIterations} 次优化迭代`);
    
    try {
      console.log('\n✍️  执行排版优化...');
      await optimizeArticleLayout(articlePath, currentVersion);
      success = true;
      console.log('✨ 排版优化完成！');
    } catch (error) {
      console.error(`❌ 第 ${currentVersion} 次优化失败:`, error.message);
      if (currentVersion === maxIterations) {
        console.log('💡 已达到最大迭代次数，停止优化');
      }
    }
  }
  
  console.log('\n' + '━'.repeat(50));
  console.log('📊 优化总结:');
  console.log(`  - 迭代次数：${currentVersion}`);
  console.log(`  - 优化结果：${success ? '✅ 成功' : '❌ 失败'}`);
  console.log('━'.repeat(50));
  
  return success;
}

/**
 * 优化文章排版
 * @param {string} articlePath - 文章路径
 * @param {number} version - 优化版本
 */
async function optimizeArticleLayout(articlePath, version) {
  let content = fs.readFileSync(articlePath, 'utf-8');
  
  const optimizations = [
    () => {
      content = content.replace(/## (一、|二、|三、|四、|五、|六、|七、)/g, '## 🔹 $1');
      content = content.replace(/## (总结)/g, '## 💎 $1');
      console.log('  ✅ 添加章节 emoji');
    },
    () => {
      content = content.replace(/(\d+)%/g, '**$1%**');
      content = content.replace(/(从 \d+% 到 \d+%)/g, '**$1**');
      console.log('  ✅ 加粗关键数据');
    },
    () => {
      content = content.replace(/^(面试官 | 他 | 用户 | 客服):/gm, '> $1:');
      console.log('  ✅ 优化对话格式');
    },
    () => {
      content = content.replace(/\n(## )/g, '\n---\n\n$1');
      console.log('  ✅ 添加分隔线');
    },
    () => {
      content = content.replace(/\n{4,}/g, '\n\n\n');
      content = content.replace(/  +\n/g, '\n');
      console.log('  ✅ 清理格式');
    }
  ];
  
  if (version <= optimizations.length) {
    optimizations[version - 1]();
    fs.writeFileSync(articlePath, content, 'utf-8');
  }
}

// 命令行接口
if (process.argv[1] && process.argv[1].includes('auto-optimize.js')) {
  const args = process.argv.slice(2);
  const articlePath = args[0];
  
  if (!articlePath) {
    console.error('用法：node auto-optimize.js <article.md> [options]');
    console.error('选项:');
    console.error('  --max-iterations <n>  最大迭代次数 (默认：5)');
    process.exit(1);
  }
  
  const options = { maxIterations: 5 };
  
  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--max-iterations' && args[i + 1]) {
      options.maxIterations = parseInt(args[++i]);
    }
  }
  
  autoOptimizeLayout(articlePath, options)
    .then(success => {
      process.exit(success ? 0 : 1);
    })
    .catch(error => {
      console.error('优化失败:', error.message);
      process.exit(1);
    });
}
