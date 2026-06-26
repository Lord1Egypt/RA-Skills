#!/usr/bin/env node

/**
 * tour-compare - 跟团游商品对比助手
 * 
 * 用法:
 *   node src/index.js compare <商品 1> <商品 2> [...]
 *   node src/index.js recommend --destination <目的地> --budget <预算> --group <人群>
 *   node src/index.js analyze <商品链接>
 */

import { Command } from 'commander';
import chalk from 'chalk';
import { compareProducts } from './analyzer/comparator.js';
import { recommendProducts } from './analyzer/recommender.js';
import { analyzeProduct } from './analyzer/analyzer.js';
import { renderComparison, renderRecommendation, renderAnalysis } from './ui/renderer.js';
import { fetchProduct, fetchProducts, extractUrls } from './crawler/ota-crawler.js';

const program = new Command();

program
  .name('tour-compare')
  .description('跟团游商品对比助手 - 对比 OTA 平台旅游产品，智能推荐')
  .version('0.1.0');

// 对比模式
program
  .command('compare')
  .description('对比多个旅游商品')
  .argument('<products...>', '商品信息（JSON 或链接）')
  .option('--group <group>', '出行人群：老人/亲子/蜜月/学生', null)
  .option('--output <format>', '输出格式：markdown/text/json', 'markdown')
  .option('--no-fetch', '禁用自动抓取，强制使用 JSON 模式')
  .option('--export <path>', '导出对比报告为图片 (PNG)')
  .action(async (products, options) => {
    console.log(chalk.blue('📊 开始对比旅游商品...\n'));
    
    // 分离 JSON 和 URL
    const jsonProducts = [];
    const urlProducts = [];
    
    products.forEach(p => {
      try {
        jsonProducts.push(JSON.parse(p));
      } catch (e) {
        // 不是 JSON，当作 URL 处理
        if (p.startsWith('http')) {
          urlProducts.push(p);
        } else {
          console.log(chalk.yellow(`⚠️  无法解析："${p}"，请检查格式`));
        }
      }
    });
    
    // 处理 URL 抓取
    let fetchedProducts = [];
    if (urlProducts.length > 0 && options.fetch !== false) {
      try {
        console.log(chalk.cyan(`🕷️  正在抓取 ${urlProducts.length} 个链接...\n`));
        const { results, errors } = await fetchProducts(urlProducts);
        fetchedProducts = results;
        
        if (errors.length > 0 && results.length === 0) {
          console.log(chalk.red('\n❌ 所有链接抓取失败，请检查网络或改用 JSON 格式'));
          process.exit(1);
        }
      } catch (error) {
        console.log(chalk.yellow(`⚠️  抓取失败：${error.message}`));
        console.log(chalk.yellow('提示：可使用 --no-fetch 强制使用 JSON 模式\n'));
      }
    }
    
    // 合并商品列表
    const allProducts = [...jsonProducts, ...fetchedProducts];
    
    if (allProducts.length === 0) {
      console.log(chalk.red('❌ 没有有效的商品数据\n'));
      console.log('用法示例:');
      console.log(chalk.gray('  对比链接:'));
      console.log(chalk.gray('  ./scripts/compare.sh compare https://ctrip.com/p/123 https://fliggy.com/p/456\n'));
      console.log(chalk.gray('  对比 JSON:'));
      console.log(chalk.gray('  ./scripts/compare.sh compare \'{"platform":"携程","title":"云南 6 日游","price":3299,"rating":4.8}\' \'{"platform":"飞猪","title":"云南 6 日游","price":2899,"rating":4.6}\'\n'));
      process.exit(1);
    }
    
    const result = compareProducts(allProducts, options.group);
    console.log(renderComparison(result, options.output));
    
    // 导出图片
    if (options.export) {
      try {
        const { generateComparisonImage } = await import('./export/image-exporter.js');
        generateComparisonImage(result, options.export);
      } catch (error) {
        console.log(chalk.yellow(`\n⚠️  图片导出失败：${error.message}`));
        console.log(chalk.yellow('提示：请先安装 canvas 库：npm install canvas\n'));
      }
    }
  });

// 推荐模式
program
  .command('recommend')
  .description('根据需求推荐旅游商品')
  .requiredOption('--destination <dest>', '目的地')
  .option('--budget <amount>', '预算（元）', null)
  .option('--group <group>', '出行人群：老人/亲子/蜜月/学生', null)
  .option('--days <days>', '行程天数', null)
  .option('--preferences <prefs>', '偏好（逗号分隔）', null)
  .action(async (options) => {
    console.log(chalk.blue('🎯 正在为您搜索推荐...\n'));
    
    const result = recommendProducts({
      destination: options.destination,
      budget: options.budget ? parseInt(options.budget) : null,
      group: options.group,
      days: options.days ? parseInt(options.days) : null,
      preferences: options.preferences ? options.preferences.split(',') : []
    });
    
    console.log(renderRecommendation(result));
  });

// 分析模式
program
  .command('analyze')
  .description('深度分析单个旅游商品')
  .argument('<product>', '商品信息或链接')
  .option('--deep', '深度分析模式')
  .action(async (product, options) => {
    console.log(chalk.blue('🔍 正在分析商品...\n'));
    
    let productData;
    try {
      productData = JSON.parse(product);
    } catch (e) {
      console.log(chalk.yellow('⚠️  链接分析功能开发中，请使用 JSON 格式\n'));
      process.exit(1);
    }
    
    const result = analyzeProduct(productData, { deep: options.deep });
    console.log(renderAnalysis(result));
  });

// 帮助信息
program
  .command('help')
  .description('显示帮助信息')
  .action(() => {
    program.help();
  });

// 无命令时显示帮助
if (process.argv.length <= 2) {
  program.help();
}

program.parse();
