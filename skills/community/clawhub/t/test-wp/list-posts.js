#!/usr/bin/env node

/**
 * WordPress文章列表脚本
 * 列出WordPress站点中的文章
 */

const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');

// 导入配置和API
const config = require('./config.js');
const WordPressAPI = require('./wordpress-api.js');

// 创建API客户端
const wpApi = new WordPressAPI(config);

/**
 * 格式化日期
 * @param {string} dateString - ISO日期字符串
 * @returns {string} 格式化后的日期
 */
function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
}

/**
 * 显示文章列表
 * @param {Array} posts - 文章列表
 * @param {Object} pagination - 分页信息
 */
function displayPosts(posts, pagination) {
  console.log('\n' + '='.repeat(80));
  console.log('📰 WordPress文章列表');
  console.log('='.repeat(80));
  
  if (posts.length === 0) {
    console.log('📭 没有找到文章');
    return;
  }
  
  console.log(`📊 显示 ${posts.length} 篇文章 (共 ${pagination.total} 篇)`);
  console.log(`📄 第 ${pagination.currentPage}/${pagination.totalPages} 页`);
  console.log();
  
  posts.forEach((post, index) => {
    console.log(`🔸 文章 #${index + 1 + (pagination.currentPage - 1) * pagination.perPage}`);
    console.log(`   ID: ${post.id}`);
    console.log(`   标题: ${post.title.rendered}`);
    console.log(`   状态: ${post.status}`);
    console.log(`   作者: ${post.author}`);
    console.log(`   日期: ${formatDate(post.date)}`);
    console.log(`   修改: ${formatDate(post.modified)}`);
    
    if (post.categories && post.categories.length > 0) {
      console.log(`   分类: ${post.categories.join(', ')}`);
    }
    
    if (post.tags && post.tags.length > 0) {
      console.log(`   标签: ${post.tags.join(', ')}`);
    }
    
    console.log(`   链接: ${post.link}`);
    
    // 显示摘要（如果有）
    if (post.excerpt && post.excerpt.rendered) {
      const excerpt = post.excerpt.rendered
        .replace(/<[^>]*>/g, '')
        .substring(0, 100);
      if (excerpt) {
        console.log(`   摘要: ${excerpt}...`);
      }
    }
    
    console.log();
  });
  
  console.log('='.repeat(80));
  console.log('📋 分页信息:');
  console.log(`   总文章数: ${pagination.total}`);
  console.log(`   总页数: ${pagination.totalPages}`);
  console.log(`   当前页: ${pagination.currentPage}`);
  console.log(`   每页数量: ${pagination.perPage}`);
  console.log('='.repeat(80));
}

/**
 * 主函数
 */
async function main() {
  const argv = yargs(hideBin(process.argv))
    .option('status', {
      alias: 's',
      type: 'string',
      description: '文章状态 (any, publish, draft, pending, private, trash)',
      default: 'any'
    })
    .option('per-page', {
      alias: 'p',
      type: 'number',
      description: '每页显示数量',
      default: 10
    })
    .option('page', {
      type: 'number',
      description: '页码',
      default: 1
    })
    .option('search', {
      type: 'string',
      description: '搜索关键词'
    })
    .option('categories', {
      alias: 'c',
      type: 'string',
      description: '分类ID（逗号分隔）'
    })
    .option('tags', {
      alias: 't',
      type: 'string',
      description: '标签ID（逗号分隔）'
    })
    .option('orderby', {
      type: 'string',
      description: '排序字段 (date, title, id, author, modified)',
      default: 'date'
    })
    .option('order', {
      type: 'string',
      description: '排序方向 (asc, desc)',
      default: 'desc'
    })
    .option('export', {
      alias: 'e',
      type: 'string',
      description: '导出文件路径（JSON格式）'
    })
    .help()
    .alias('help', 'h')
    .argv;
  
  try {
    // 测试API连接
    console.log('🔗 测试WordPress API连接...');
    const connected = await wpApi.testConnection();
    if (!connected) {
      console.error('❌ 无法连接到WordPress，请检查配置');
      process.exit(1);
    }
    
    // 准备查询参数
    const options = {
      status: argv.status,
      perPage: argv['per-page'],
      page: argv.page,
      orderBy: argv.orderby,
      order: argv.order
    };
    
    if (argv.search) {
      options.search = argv.search;
    }
    
    if (argv.categories) {
      options.categories = argv.categories.split(',').map(id => parseInt(id.trim()));
    }
    
    if (argv.tags) {
      options.tags = argv.tags.split(',').map(id => parseInt(id.trim()));
    }
    
    // 获取文章列表
    console.log('📡 获取文章列表...');
    const result = await wpApi.getPosts(options);
    
    // 显示文章列表
    displayPosts(result.posts, result.pagination);
    
    // 导出到文件（如果需要）
    if (argv.export) {
      const exportData = {
        timestamp: new Date().toISOString(),
        query: options,
        pagination: result.pagination,
        posts: result.posts.map(post => ({
          id: post.id,
          title: post.title.rendered,
          status: post.status,
          date: post.date,
          modified: post.modified,
          author: post.author,
          categories: post.categories,
          tags: post.tags,
          link: post.link,
          excerpt: post.excerpt?.rendered?.replace(/<[^>]*>/g, '') || ''
        }))
      };
      
      await fs.writeFile(argv.export, JSON.stringify(exportData, null, 2));
      console.log(`📄 文章列表已导出到: ${argv.export}`);
    }
    
    console.log('🎉 操作完成！');
  } catch (error) {
    console.error('❌ 获取文章列表失败:', error.message);
    process.exit(1);
  }
}

// 运行主函数
if (require.main === module) {
  main();
}

module.exports = {
  displayPosts
};