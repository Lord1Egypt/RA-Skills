#!/usr/bin/env node

/**
 * WordPress批量发布脚本
 * 批量发布多个Markdown文章到WordPress
 */

const fs = require('fs').promises;
const fsSync = require('fs');
const path = require('path');
const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');

// 导入配置和发布函数
const config = require('./config.js');
const { publishPost } = require('./publish.js');
const WordPressAPI = require('./wordpress-api.js');

// 创建API客户端
const wpApi = new WordPressAPI(config);

/**
 * 获取目录中的所有Markdown文件
 * @param {string} dirPath - 目录路径
 * @returns {Array} Markdown文件列表
 */
async function getMarkdownFiles(dirPath) {
  try {
    const files = await fs.readdir(dirPath);
    return files
      .filter(file => file.endsWith('.md'))
      .map(file => path.join(dirPath, file));
  } catch (error) {
    console.error(`❌ 读取目录失败: ${dirPath}`, error.message);
    throw error;
  }
}

/**
 * 批量发布文章
 * @param {Array} files - 文件列表
 * @param {Object} options - 发布选项
 */
async function batchPublish(files, options = {}) {
  console.log(`📚 开始批量发布 ${files.length} 篇文章`);
  
  const results = {
    success: [],
    failed: []
  };
  
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    console.log(`\n📝 处理文章 ${i + 1}/${files.length}: ${path.basename(file)}`);
    
    try {
      const result = await publishPost(file, options);
      results.success.push({
        file: path.basename(file),
        id: result.id,
        title: result.title.rendered,
        url: result.link,
        status: result.status
      });
      
      // 添加延迟避免请求过快
      if (options.delay && i < files.length - 1) {
        console.log(`⏳ 等待 ${options.delay}ms...`);
        await new Promise(resolve => setTimeout(resolve, options.delay));
      }
    } catch (error) {
      results.failed.push({
        file: path.basename(file),
        error: error.message
      });
      
      // 如果设置了最大重试次数
      if (options.maxRetries > 0) {
        let retryCount = 0;
        while (retryCount < options.maxRetries) {
          retryCount++;
          console.log(`🔄 重试 ${retryCount}/${options.maxRetries}: ${path.basename(file)}`);
          
          try {
            await new Promise(resolve => setTimeout(resolve, options.retryDelay || 1000));
            const result = await publishPost(file, options);
            results.success.push({
              file: path.basename(file),
              id: result.id,
              title: result.title.rendered,
              url: result.link,
              status: result.status
            });
            results.failed.pop(); // 从失败列表中移除
            break;
          } catch (retryError) {
            if (retryCount === options.maxRetries) {
              console.error(`❌ 重试失败: ${path.basename(file)}`);
            }
          }
        }
      }
    }
  }
  
  return results;
}

/**
 * 生成报告
 * @param {Object} results - 发布结果
 */
function generateReport(results) {
  console.log('\n' + '='.repeat(50));
  console.log('📊 批量发布报告');
  console.log('='.repeat(50));
  
  console.log(`✅ 成功: ${results.success.length} 篇`);
  console.log(`❌ 失败: ${results.failed.length} 篇`);
  
  if (results.success.length > 0) {
    console.log('\n📈 成功发布的文章:');
    results.success.forEach((item, index) => {
      console.log(`  ${index + 1}. ${item.title}`);
      console.log(`     文件: ${item.file}`);
      console.log(`     ID: ${item.id}`);
      console.log(`     状态: ${item.status}`);
      console.log(`     链接: ${item.url}`);
      console.log();
    });
  }
  
  if (results.failed.length > 0) {
    console.log('\n📉 失败的文章:');
    results.failed.forEach((item, index) => {
      console.log(`  ${index + 1}. ${item.file}`);
      console.log(`     错误: ${item.error}`);
      console.log();
    });
  }
  
  console.log('='.repeat(50));
  
  // 保存报告到文件
  const report = {
    timestamp: new Date().toISOString(),
    total: results.success.length + results.failed.length,
    success: results.success.length,
    failed: results.failed.length,
    details: {
      success: results.success,
      failed: results.failed
    }
  };
  
  const reportFile = `batch-publish-report-${Date.now()}.json`;
  fs.writeFile(reportFile, JSON.stringify(report, null, 2));
  console.log(`📄 详细报告已保存到: ${reportFile}`);
}

/**
 * 主函数
 */
async function main() {
  const argv = yargs(hideBin(process.argv))
    .option('dir', {
      alias: 'd',
      type: 'string',
      description: '文章目录路径',
      default: config.posts.directory
    })
    .option('status', {
      alias: 's',
      type: 'string',
      description: '文章状态 (draft/publish/pending/private)',
      default: config.wordpress.defaultStatus
    })
    .option('delay', {
      type: 'number',
      description: '文章之间的延迟（毫秒）',
      default: config.publish.delayBetweenPosts
    })
    .option('max-retries', {
      type: 'number',
      description: '最大重试次数',
      default: config.publish.maxRetries
    })
    .option('retry-delay', {
      type: 'number',
      description: '重试延迟（毫秒）',
      default: config.publish.retryDelay
    })
    .option('test', {
      type: 'boolean',
      description: '测试模式（不实际发布）',
      default: false
    })
    .option('pattern', {
      alias: 'p',
      type: 'string',
      description: '文件匹配模式（正则表达式）'
    })
    .help()
    .alias('help', 'h')
    .argv;
  
  try {
    // 检查目录是否存在
    if (!fsSync.existsSync(argv.dir)) {
      console.error(`❌ 目录不存在: ${argv.dir}`);
      console.log(`创建目录: ${argv.dir}`);
      await fs.mkdir(argv.dir, { recursive: true });
    }
    
    // 获取Markdown文件
    let files = await getMarkdownFiles(argv.dir);
    
    // 应用文件匹配模式
    if (argv.pattern) {
      const regex = new RegExp(argv.pattern);
      files = files.filter(file => regex.test(path.basename(file)));
    }
    
    if (files.length === 0) {
      console.log(`📁 目录中没有找到Markdown文件: ${argv.dir}`);
      console.log('请将.md文件放入该目录，或使用 --dir 指定其他目录');
      process.exit(0);
    }
    
    console.log(`📁 找到 ${files.length} 个Markdown文件:`);
    files.forEach((file, index) => {
      console.log(`  ${index + 1}. ${path.basename(file)}`);
    });
    
    // 测试API连接
    console.log('\n🔗 测试WordPress API连接...');
    const connected = await wpApi.testConnection();
    if (!connected) {
      console.error('❌ 无法连接到WordPress，请检查配置');
      process.exit(1);
    }
    
    if (argv.test) {
      console.log('🧪 测试模式：只显示文件列表，不发布');
      console.log('发布选项:', {
        status: argv.status,
        delay: argv.delay,
        maxRetries: argv.maxRetries,
        retryDelay: argv.retryDelay
      });
    } else {
      // 确认发布
      console.log('\n⚠️  即将发布以上文章到WordPress');
      console.log(`   状态: ${argv.status}`);
      console.log(`   延迟: ${argv.delay}ms`);
      console.log(`   最大重试次数: ${argv.maxRetries}`);
      
      const readline = require('readline').createInterface({
        input: process.stdin,
        output: process.stdout
      });
      
      const answer = await new Promise(resolve => {
        readline.question('是否继续？(y/N): ', resolve);
      });
      
      readline.close();
      
      if (answer.toLowerCase() !== 'y') {
        console.log('操作已取消');
        process.exit(0);
      }
      
      // 批量发布
      const results = await batchPublish(files, {
        status: argv.status,
        delay: argv.delay,
        maxRetries: argv.maxRetries,
        retryDelay: argv.retryDelay
      });
      
      // 生成报告
      generateReport(results);
    }
    
    console.log('\n🎉 批量处理完成！');
  } catch (error) {
    console.error('❌ 批量发布失败:', error.message);
    process.exit(1);
  }
}

// 运行主函数
if (require.main === module) {
  main();
}

module.exports = {
  getMarkdownFiles,
  batchPublish,
  generateReport
};