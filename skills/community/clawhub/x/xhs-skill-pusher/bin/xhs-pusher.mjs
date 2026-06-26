#!/usr/bin/env node
/**
 * xhs-pusher CLI工具
 * 小红书内容发布统一接口
 */

import { program } from 'commander';
import chalk from 'chalk';
import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.join(__dirname, '..');

// 颜色定义
const colors = {
  info: chalk.blue,
  success: chalk.green,
  warning: chalk.yellow,
  error: chalk.red,
  bold: chalk.bold
};

// 日志函数
const log = {
  info: (msg) => console.log(colors.info('[INFO]'), msg),
  success: (msg) => console.log(colors.success('✅'), msg),
  warning: (msg) => console.log(colors.warning('⚠️'), msg),
  error: (msg) => console.log(colors.error('❌'), msg),
  bold: (msg) => console.log(colors.bold(msg))
};

// 显示横幅
function showBanner() {
  console.log('');
  colors.bold('🚀 xhs-pusher - 小红书内容发布工具');
  console.log('规范化cookie管理 + xhs-kit自动化发布');
  console.log('');
}

// 检查依赖
function checkDependencies() {
  try {
    // 检查xhs-kit
    execSync('which xhs-kit', { stdio: 'ignore' });
    return true;
  } catch (error) {
    log.error('xhs-kit未安装');
    log.info('请安装: pip install xhs-kit');
    return false;
  }
}

// Cookie管理命令
function setupCookieCommands() {
  const cookie = program.command('cookie')
    .description('Cookie管理命令');

  // 列出所有cookie
  cookie.command('list')
    .description('列出所有cookie文件')
    .action(() => {
      showBanner();
      log.info('列出所有cookie文件...');
      
      const cookieDir = path.join(PROJECT_ROOT, 'xhs_cookies');
      if (!fs.existsSync(cookieDir)) {
        log.warning('Cookie目录不存在');
        log.info('使用命令初始化: mkdir -p xhs_cookies/archive');
        return;
      }

      try {
        execSync(`cd "${PROJECT_ROOT}" && ./scripts/xhs_final.sh --list-cookies`, {
          stdio: 'inherit'
        });
      } catch (error) {
        log.error('执行失败');
      }
    });

  // 保存cookie
  cookie.command('save')
    .description('保存新cookie')
    .requiredOption('--name <name>', 'cookie名称（如：new_main）')
    .requiredOption('--cookie <cookie>', 'cookie字符串')
    .option('--desc <description>', '描述信息')
    .option('--set-active', '设置为当前激活cookie')
    .action((options) => {
      showBanner();
      
      const args = [
        './scripts/xhs_save_cookie.sh',
        '--name', options.name,
        '--cookie', `"${options.cookie}"`
      ];

      if (options.desc) {
        args.push('--desc', options.desc);
      }

      if (options.setActive) {
        args.push('--set-active');
      }

      try {
        execSync(`cd "${PROJECT_ROOT}" && ${args.join(' ')}`, {
          stdio: 'inherit'
        });
      } catch (error) {
        log.error('保存失败');
      }
    });

  // 查看cookie信息
  cookie.command('info <name>')
    .description('查看cookie详细信息')
    .action((name) => {
      showBanner();
      
      try {
        execSync(`cd "${PROJECT_ROOT}" && ./scripts/xhs_manage.sh info "${name}"`, {
          stdio: 'inherit'
        });
      } catch (error) {
        log.error('查看失败');
      }
    });

  // 使用指定cookie
  cookie.command('use <name>')
    .description('使用指定cookie（设置为active）')
    .action((name) => {
      showBanner();
      
      try {
        execSync(`cd "${PROJECT_ROOT}" && ./scripts/xhs_manage.sh use "${name}"`, {
          stdio: 'inherit'
        });
      } catch (error) {
        log.error('切换失败');
      }
    });

  // 检查状态
  cookie.command('status')
    .description('查看当前状态')
    .action(() => {
      showBanner();
      
      try {
        execSync(`cd "${PROJECT_ROOT}" && ./scripts/xhs_manage.sh status`, {
          stdio: 'inherit'
        });
      } catch (error) {
        log.error('检查失败');
      }
    });
}

// 发布命令
function setupPublishCommands() {
  const publish = program.command('publish')
    .description('发布内容命令');

  // 基本发布
  publish.command('post')
    .description('发布小红书内容')
    .requiredOption('--title <title>', '笔记标题')
    .requiredOption('--content <content>', '笔记内容')
    .requiredOption('--image <image...>', '图片路径（可多个）')
    .option('--tag <tag...>', '标签（可多个）')
    .option('--schedule <time>', '定时发布时间')
    .option('--show-browser', '显示浏览器窗口')
    .option('--debug-only', '仅验证，不实际发布')
    .option('--cookie <cookie>', 'cookie文件路径（默认：xhs_cookies/active.json）')
    .action((options) => {
      showBanner();
      
      if (!checkDependencies()) {
        return;
      }

      const cookieFile = options.cookie || 'xhs_cookies/active.json';
      const args = [
        './scripts/xhs_final.sh',
        '--cookie', cookieFile,
        '--title', `"${options.title}"`,
        '--content', `"${options.content}"`
      ];

      // 添加图片
      if (Array.isArray(options.image)) {
        options.image.forEach(image => {
          args.push('--image', image);
        });
      } else {
        args.push('--image', options.image);
      }

      // 添加标签
      if (options.tag) {
        if (Array.isArray(options.tag)) {
          options.tag.forEach(tag => {
            args.push('--tag', tag);
          });
        } else {
          args.push('--tag', options.tag);
        }
      }

      // 添加其他选项
      if (options.schedule) {
        args.push('--schedule', options.schedule);
      }

      if (options.showBrowser) {
        args.push('--show-browser');
      }

      if (options.debugOnly) {
        args.push('--debug-only');
      }

      try {
        execSync(`cd "${PROJECT_ROOT}" && ${args.join(' ')}`, {
          stdio: 'inherit'
        });
      } catch (error) {
        log.error('发布失败');
      }
    });

  // 检查发布状态
  publish.command('status')
    .description('检查发布状态')
    .option('--cookie <cookie>', 'cookie文件路径')
    .action((options) => {
      showBanner();
      
      const cookieFile = options.cookie || 'xhs_cookies/active.json';
      
      try {
        execSync(`cd "${PROJECT_ROOT}" && ./scripts/xhs_final.sh --cookie "${cookieFile}" --check-status`, {
          stdio: 'inherit'
        });
      } catch (error) {
        log.error('检查失败');
      }
    });
}

// 初始化命令
function setupInitCommands() {
  program.command('init')
    .description('初始化项目')
    .action(() => {
      showBanner();
      
      log.info('初始化xhs-skill-pusher项目...');
      
      // 创建目录结构
      const dirs = [
        'xhs_cookies',
        'xhs_cookies/archive',
        'scripts',
        'docs',
        'logs'
      ];

      dirs.forEach(dir => {
        const dirPath = path.join(PROJECT_ROOT, dir);
        if (!fs.existsSync(dirPath)) {
          fs.ensureDirSync(dirPath);
          log.success(`创建目录: ${dir}`);
        }
      });

      // 复制脚本文件
      const scripts = [
        'xhs_save_cookie.sh',
        'xhs_final.sh',
        'xhs_manage.sh',
        'xhs_simple.sh'
      ];

      // 检查脚本是否存在，如果不存在则创建示例
      scripts.forEach(script => {
        const scriptPath = path.join(PROJECT_ROOT, 'scripts', script);
        if (!fs.existsSync(scriptPath)) {
          // 创建简单的示例脚本
          const content = `#!/bin/bash
# ${script} - 请从工作空间复制实际脚本
echo "请从工作空间复制实际的 ${script} 脚本到此处"
echo "实际脚本位置: ~/.openclaw/workspace/${script}"
exit 1
`;
          fs.writeFileSync(scriptPath, content, { mode: 0o755 });
          log.warning(`创建示例脚本: scripts/${script}`);
          log.info(`请复制实际脚本: cp ~/.openclaw/workspace/${script} scripts/`);
        }
      });

      // 创建文档
      const docs = [
        ['XHS_FINAL_SOLUTION.md', '# 完整解决方案文档\n\n请从工作空间复制实际文档。'],
        ['QUICK_START.md', '# 快速开始指南\n\n请从工作空间复制实际文档。']
      ];

      docs.forEach(([filename, content]) => {
        const docPath = path.join(PROJECT_ROOT, 'docs', filename);
        if (!fs.existsSync(docPath)) {
          fs.writeFileSync(docPath, content);
          log.warning(`创建示例文档: docs/${filename}`);
        }
      });

      log.success('初始化完成！');
      console.log('');
      log.bold('下一步:');
      log.info('1. 复制脚本文件: cp ~/.openclaw/workspace/xhs_*.sh scripts/');
      log.info('2. 安装Python依赖: pip install xhs-kit');
      log.info('3. 保存第一个cookie: node ./bin/xhs-pusher.mjs cookie save --name test --cookie "..."');
      console.log('');
    });
}

// 主函数
async function main() {
  program
    .name('xhs-pusher')
    .description('小红书内容发布工具 - 规范化cookie管理 + xhs-kit自动化发布')
    .version('1.0.0');

  // 设置命令
  setupCookieCommands();
  setupPublishCommands();
  setupInitCommands();

  // 显示帮助信息
  program.on('--help', () => {
    console.log('');
    log.bold('示例:');
    console.log('  $ xhs-pusher cookie list                    # 列出所有cookie');
    console.log('  $ xhs-pusher cookie save --name new_main \\');
    console.log('      --cookie "a1=xxx;webId=yyy"             # 保存新cookie');
    console.log('  $ xhs-pusher publish post \\');
    console.log('      --title "标题" --content "内容" \\');
    console.log('      --image photo.jpg                       # 发布内容');
    console.log('  $ xhs-pusher init                          # 初始化项目');
    console.log('');
    log.bold('文档:');
    console.log('  完整文档: docs/XHS_FINAL_SOLUTION.md');
    console.log('  快速开始: docs/QUICK_START.md');
    console.log('');
  });

  // 解析参数
  program.parse(process.argv);

  // 如果没有参数，显示帮助
  if (process.argv.length <= 2) {
    showBanner();
    program.help();
  }
}

// 运行主函数
main().catch(error => {
  log.error(`程序错误: ${error.message}`);
  process.exit(1);
});