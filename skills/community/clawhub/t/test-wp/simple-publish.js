#!/usr/bin/env node

/**
 * 简单的WordPress文章发布脚本
 * 使用环境变量配置认证信息
 * 
 * 使用方法:
 * 1. 设置环境变量:
 *    export WORDPRESS_URL="https://your-site.com"
 *    export WORDPRESS_USERNAME="your-username"
 *    export WORDPRESS_PASSWORD="your-app-password"
 * 
 * 2. 运行脚本:
 *    node simple-publish.js "文章标题" "文章内容"
 */

const axios = require('axios');

// 从环境变量获取配置
const config = {
  url: process.env.WORDPRESS_URL || 'https://your-site.com',
  username: process.env.WORDPRESS_USERNAME || 'admin',
  password: process.env.WORDPRESS_PASSWORD || 'HnK3 o7xu KHNy DFtV 2fpZ 7uwG',
  
  // 默认文章设置
  defaultStatus: process.env.DEFAULT_STATUS || 'draft',
  defaultCategory: parseInt(process.env.DEFAULT_CATEGORY) || 1
};

// 创建API客户端
const api = axios.create({
  baseURL: `${config.url}/wp-json/wp/v2`,
  auth: {
    username: config.username,
    password: config.password
  },
  headers: {
    'Content-Type': 'application/json'
  }
});

async function publishPost(title, content, options = {}) {
  console.log('📝 开始发布文章到WordPress...\n');
  console.log(`站点: ${config.url}`);
  console.log(`用户: ${config.username}`);
  console.log(`状态: ${options.status || config.defaultStatus}`);
  console.log('---\n');
  
  try {
    // 验证配置
    if (!config.url || !config.username || !config.password) {
      throw new Error('缺少必要的配置信息。请设置环境变量：WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_PASSWORD');
    }
    
    // 测试连接
    console.log('1. 测试API连接...');
    try {
      const testResponse = await api.get('/');
      console.log(`✅ API连接成功: ${testResponse.data.name}`);
    } catch (error) {
      console.log('❌ API连接失败:', error.message);
      throw error;
    }
    
    // 准备文章数据
    const postData = {
      title: title,
      content: content,
      status: options.status || config.defaultStatus,
      excerpt: options.excerpt || '',
      categories: options.categories || [config.defaultCategory],
      tags: options.tags || [],
      meta: options.meta || {}
    };
    
    // 发布文章
    console.log('\n2. 发布文章...');
    console.log(`标题: "${title}"`);
    console.log(`状态: ${postData.status}`);
    
    const response = await api.post('/posts', postData);
    
    console.log('\n✅ 文章发布成功！');
    console.log(`文章ID: ${response.data.id}`);
    console.log(`标题: ${response.data.title.rendered}`);
    console.log(`状态: ${response.data.status}`);
    console.log(`链接: ${response.data.link}`);
    console.log(`创建时间: ${response.data.date}`);
    
    return {
      success: true,
      postId: response.data.id,
      title: response.data.title.rendered,
      status: response.data.status,
      link: response.data.link,
      date: response.data.date
    };
    
  } catch (error) {
    console.error('\n❌ 文章发布失败:');
    
    if (error.response) {
      console.log(`状态码: ${error.response.status}`);
      console.log(`错误信息: ${error.response.data?.message || '未知错误'}`);
      console.log(`错误代码: ${error.response.data?.code || '未知'}`);
      
      // 提供具体建议
      if (error.response.status === 401) {
        console.log('\n🔧 建议:');
        console.log('1. 检查用户名和密码是否正确');
        console.log('2. 确认使用的是应用程序密码而不是登录密码');
        console.log('3. 在WordPress中创建应用程序密码:');
        console.log('   用户 → 个人资料 → 应用程序密码');
      } else if (error.response.status === 403) {
        console.log('\n🔧 建议:');
        console.log('1. 检查用户是否有发布文章的权限');
        console.log('2. 确认用户角色（需要作者或以上权限）');
      }
    } else {
      console.log(`错误: ${error.message}`);
    }
    
    return {
      success: false,
      error: error.message,
      statusCode: error.response?.status,
      errorCode: error.response?.data?.code
    };
  }
}

// 命令行接口
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.log('📖 使用方法:');
    console.log('  node simple-publish.js "文章标题" "文章内容" [选项]');
    console.log('\n📋 选项:');
    console.log('  环境变量:');
    console.log('    WORDPRESS_URL        WordPress站点URL');
    console.log('    WORDPRESS_USERNAME   WordPress用户名');
    console.log('    WORDPRESS_PASSWORD   应用程序密码');
    console.log('    DEFAULT_STATUS       默认状态 (draft/publish)');
    console.log('    DEFAULT_CATEGORY     默认分类ID');
    console.log('\n📝 示例:');
    console.log('  export WORDPRESS_URL="https://your-site.com"');
    console.log('  export WORDPRESS_USERNAME="admin"');
    console.log('  export WORDPRESS_PASSWORD="xxxx xxxx xxxx xxxx"');
    console.log('  node simple-publish.js "测试标题" "测试内容"');
    process.exit(1);
  }
  
  const title = args[0];
  const content = args[1];
  const options = {
    status: process.env.DEFAULT_STATUS || 'draft',
    excerpt: args[2] || ''
  };
  
  publishPost(title, content, options).then(result => {
    if (result.success) {
      console.log('\n🎉 发布完成！');
      process.exit(0);
    } else {
      console.log('\n❌ 发布失败');
      process.exit(1);
    }
  });
}

module.exports = { publishPost };