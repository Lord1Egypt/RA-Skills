#!/usr/bin/env node

/**
 * TikTok Shop Automation - CLI Entry Point
 * 跨境电商自动化套件命令行工具
 */

import { Command } from 'commander';
import chalk from 'chalk';
import ora from 'ora';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 导入各功能模块
import { publishVideo } from './commands/video.js';
import { addAccount, listAccounts, switchAccount } from './commands/account.js';
import { importProducts, createProduct, syncInventory } from './commands/product.js';
import { syncOrders, fulfillOrders } from './commands/order.js';
import { dailyReport, adAnalytics, trackCompetitors } from './commands/analytics.js';
import { initConfig } from './commands/init.js';

const program = new Command();

program
  .name('tiktok-shop-automation')
  .description(chalk.green('🚀 TikTok Shop 跨境电商自动化套件'))
  .version('1.0.0');

// 初始化命令
program
  .command('init')
  .description('初始化配置')
  .action(async () => {
    const spinner = ora('初始化配置...').start();
    try {
      await initConfig();
      spinner.succeed(chalk.green('✓ 初始化完成'));
    } catch (error) {
      spinner.fail(chalk.red(`✗ 初始化失败：${error.message}`));
      process.exit(1);
    }
  });

// 账号管理
program
  .command('add-account')
  .description('添加 TikTok 账号')
  .requiredOption('--username <username>', 'TikTok 用户名')
  .requiredOption('--cookie <cookie>', 'Session Cookie')
  .option('--region <region>', '地区 (US/UK/SEA/ID)', 'US')
  .action(async (options) => {
    const spinner = ora('添加账号...').start();
    try {
      await addAccount(options);
      spinner.succeed(chalk.green(`✓ 账号 ${options.username} 添加成功`));
    } catch (error) {
      spinner.fail(chalk.red(`✗ 添加失败：${error.message}`));
      process.exit(1);
    }
  });

program
  .command('list-accounts')
  .description('列出所有账号')
  .action(async () => {
    try {
      await listAccounts();
    } catch (error) {
      console.error(chalk.red(`✗ 错误：${error.message}`));
      process.exit(1);
    }
  });

program
  .command('switch-account')
  .description('切换账号')
  .argument('<username>', '要切换的账号用户名')
  .action(async (username) => {
    const spinner = ora('切换账号...').start();
    try {
      await switchAccount(username);
      spinner.succeed(chalk.green(`✓ 已切换到账号 ${username}`));
    } catch (error) {
      spinner.fail(chalk.red(`✗ 切换失败：${error.message}`));
      process.exit(1);
    }
  });

// 视频发布
program
  .command('publish-video')
  .description('发布视频到 TikTok')
  .requiredOption('--video-path <path>', '视频文件路径')
  .option('--description <text>', '视频描述')
  .option('--tags <tags>', '标签 (逗号分隔)')
  .option('--schedule <time>', '定时发布时间 (ISO 8601)')
  .option('--account <username>', '指定账号 (默认当前账号)')
  .action(async (options) => {
    const spinner = ora('发布视频...').start();
    try {
      const result = await publishVideo(options);
      spinner.succeed(chalk.green('✓ 视频发布成功'));
      console.log(chalk.blue(`📹 视频 ID: ${result.videoId}`));
      console.log(chalk.blue(`🔗 链接：${result.videoUrl}`));
    } catch (error) {
      spinner.fail(chalk.red(`✗ 发布失败：${error.message}`));
      process.exit(1);
    }
  });

// 商品管理
program
  .command('import-products')
  .description('批量导入商品')
  .requiredOption('--file <path>', 'CSV 文件路径')
  .option('--shop <shop_id>', '店铺 ID')
  .option('--auto-publish', '自动上架')
  .action(async (options) => {
    const spinner = ora('导入商品...').start();
    try {
      const result = await importProducts(options);
      spinner.succeed(chalk.green(`✓ 成功导入 ${result.count} 个商品`));
    } catch (error) {
      spinner.fail(chalk.red(`✗ 导入失败：${error.message}`));
      process.exit(1);
    }
  });

program
  .command('create-product')
  .description('创建单个商品')
  .requiredOption('--title <title>', '商品标题')
  .requiredOption('--price <price>', '价格')
  .option('--stock <quantity>', '库存数量', '100')
  .option('--images <path>', '商品图片路径')
  .option('--description <text>', '商品描述')
  .action(async (options) => {
    const spinner = ora('创建商品...').start();
    try {
      const result = await createProduct(options);
      spinner.succeed(chalk.green('✓ 商品创建成功'));
      console.log(chalk.blue(`🏷️  商品 ID: ${result.productId}`));
    } catch (error) {
      spinner.fail(chalk.red(`✗ 创建失败：${error.message}`));
      process.exit(1);
    }
  });

program
  .command('sync-inventory')
  .description('同步库存')
  .option('--erp-system <system>', 'ERP 系统 (odoo/店小秘/马帮)')
  .option('--auto-update', '自动更新库存')
  .action(async (options) => {
    const spinner = ora('同步库存...').start();
    try {
      await syncInventory(options);
      spinner.succeed(chalk.green('✓ 库存同步完成'));
    } catch (error) {
      spinner.fail(chalk.red(`✗ 同步失败：${error.message}`));
      process.exit(1);
    }
  });

// 订单管理
program
  .command('sync-orders')
  .description('同步订单')
  .option('--target <target>', '同步目标 (feishu-bitable/csv/api)')
  .option('--app-token <token>', '飞书多维表格 App Token')
  .option('--table-id <id>', '飞书多维表格 Table ID')
  .option('--auto-sync', '自动同步')
  .option('--interval <minutes>', '同步间隔 (分钟)', '15')
  .action(async (options) => {
    const spinner = ora('同步订单...').start();
    try {
      await syncOrders(options);
      spinner.succeed(chalk.green('✓ 订单同步完成'));
    } catch (error) {
      spinner.fail(chalk.red(`✗ 同步失败：${error.message}`));
      process.exit(1);
    }
  });

program
  .command('fulfill-orders')
  .description('批量发货')
  .option('--order-ids <ids>', '订单 ID 列表 (逗号分隔)')
  .option('--carrier <carrier>', '物流公司 (fedex/ups/dhl)')
  .option('--tracking-prefix <prefix>', '运单号前缀')
  .option('--auto-notify', '自动通知买家')
  .action(async (options) => {
    const spinner = ora('处理发货...').start();
    try {
      const result = await fulfillOrders(options);
      spinner.succeed(chalk.green(`✓ 成功发货 ${result.count} 个订单`));
    } catch (error) {
      spinner.fail(chalk.red(`✗ 发货失败：${error.message}`));
      process.exit(1);
    }
  });

// 数据分析
program
  .command('daily-report')
  .description('生成日报')
  .option('--date <date>', '日期 (YYYY-MM-DD)', new Date().toISOString().split('T')[0])
  .option('--format <format>', '输出格式 (pdf/csv/html)', 'pdf')
  .option('--email <email>', '发送邮件到')
  .action(async (options) => {
    const spinner = ora('生成日报...').start();
    try {
      const report = await dailyReport(options);
      spinner.succeed(chalk.green('✓ 日报生成成功'));
      console.log(chalk.blue(`📊 报告路径：${report.path}`));
    } catch (error) {
      spinner.fail(chalk.red(`✗ 生成失败：${error.message}`));
      process.exit(1);
    }
  });

program
  .command('ad-analytics')
  .description('广告数据分析')
  .option('--campaign-id <id>', '广告活动 ID')
  .option('--metrics <metrics>', '指标 (roas,ctr,cpc)')
  .option('--period <period>', '时间范围 (last_7_days/last_30_days/today)')
  .action(async (options) => {
    const spinner = ora('分析广告数据...').start();
    try {
      const analytics = await adAnalytics(options);
      spinner.succeed(chalk.green('✓ 分析完成'));
      console.log(chalk.blue('\n📈 关键指标:'));
      console.log(`   ROAS: ${analytics.roas}`);
      console.log(`   CTR: ${analytics.ctr}%`);
      console.log(`   CPC: $${analytics.cpc}`);
    } catch (error) {
      spinner.fail(chalk.red(`✗ 分析失败：${error.message}`));
      process.exit(1);
    }
  });

program
  .command('track-competitors')
  .description('监控竞品')
  .requiredOption('--shops <shops>', '竞品店铺列表 (逗号分隔)')
  .option('--metrics <metrics>', '监控指标 (price,bestseller,reviews)')
  .option('--alert <type>', '预警类型 (new-product/price-change)')
  .action(async (options) => {
    const spinner = ora('监控竞品...').start();
    try {
      await trackCompetitors(options);
      spinner.succeed(chalk.green('✓ 竞品监控已启动'));
    } catch (error) {
      spinner.fail(chalk.red(`✗ 监控失败：${error.message}`));
      process.exit(1);
    }
  });

// 解析命令行参数
program.parse(process.argv);

// 如果没有提供任何参数，显示帮助信息
if (!process.argv.slice(2).length) {
  program.outputHelp();
}
