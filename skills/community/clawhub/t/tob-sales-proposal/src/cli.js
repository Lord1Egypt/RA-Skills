#!/usr/bin/env node

const { Command } = require('commander');
const inquirer = require('inquirer');
const chalk = require('chalk');
const fs = require('fs-extra');
const path = require('path');
const ProposalGenerator = require('./generator');

const program = new Command();

program
  .name('tob-sales-proposal')
  .description('ToB销售提案生成器 - 基于19年实战经验')
  .version('1.2.0');

program
  .option('-c, --client <name>', '客户名称')
  .option('-i, --industry <industry>', '所属行业')
  .option('-p, --product <product>', '产品/解决方案')
  .option('--painpoints <points>', '核心痛点（逗号分隔）')
  .option('-b, --budget <range>', '预算范围')
  .option('-t, --timeline <duration>', '项目周期')
  .option('-r, --rfp <path>', 'RFP文件路径')
  .option('--quick', '快速模式（保留兼容，使用命令行参数直接生成）', false)
  .option('-o, --output <path>', '输出文件路径', './proposal.html')
  .option('-f, --format <format>', '输出格式：html', 'html')
  .option('--interactive', '交互模式', false)
  .action(async (options) => {
    try {
      console.log(chalk.blue('📄 ToB 销售提案生成器'));
      console.log(chalk.gray('基于19年实战经验 | 作者：李宁\n'));

      let config = options;

      // 交互模式
      if (!options.client || options.interactive) {
        config = await runInteractive();
      }

      // 验证必填项
      if (!config.client || !config.industry) {
        console.error(chalk.red('❌ 错误：客户名称和行业为必填项'));
        process.exit(1);
      }

      // 生成提案
      const generator = new ProposalGenerator(config);
      const proposal = await generator.generate();

      // 保存文件
      await fs.writeFile(config.output, proposal);
      
      console.log(chalk.green(`✅ 提案已生成: ${path.resolve(config.output)}`));
      console.log(chalk.gray(`📊 包含分页: 痛点对齐、方案对齐、实施路径、ROI与案例`));
      console.log(chalk.gray(`💡 页面底部已加入“复制内容给 AI 生成 PPT”提示`));
      
    } catch (error) {
      console.error(chalk.red('❌ 生成失败:', error.message));
      process.exit(1);
    }
  });

async function runInteractive() {
  const industries = [
    '金融', '零售', '制造', '能源', '政务', 
    '医疗', '教育', '物流', '房地产', '其他'
  ];

  const products = [
    '智能客服系统', 'RAG知识库', 'CRM系统', 'SCRM系统',
    '供应链管理系统', '数据中台', '业务中台', 'ERP系统',
    '智能营销平台', 'BI分析平台', '其他'
  ];

  const answers = await inquirer.prompt([
    {
      type: 'input',
      name: 'client',
      message: '客户名称:',
      validate: (input) => input.trim() !== '' || '客户名称不能为空'
    },
    {
      type: 'list',
      name: 'industry',
      message: '所属行业:',
      choices: industries
    },
    {
      type: 'list',
      name: 'product',
      message: '产品/解决方案:',
      choices: products
    },
    {
      type: 'input',
      name: 'painpoints',
      message: '核心痛点（用逗号分隔）:',
      default: '数据孤岛,效率低下'
    },
    {
      type: 'input',
      name: 'budget',
      message: '预算范围:',
      default: '50-100万'
    },
    {
      type: 'input',
      name: 'timeline',
      message: '期望交付周期:',
      default: '3个月'
    },
    {
      type: 'input',
      name: 'output',
      message: '输出文件路径:',
      default: './proposal.html'
    }
  ]);

  return answers;
}

program.parse();
