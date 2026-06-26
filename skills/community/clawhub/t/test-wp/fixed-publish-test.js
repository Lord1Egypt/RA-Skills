#!/usr/bin/env node

/**
 * 修复参数后的发布测试
 * 使用正确的WordPress API参数格式
 */

const axios = require('axios');

const config = {
  url: 'https://your-site.com',
  username: 'admin',
  password: 'your-app-password'
};

class WordPressPublisher {
  constructor(config) {
    this.config = config;
    this.api = axios.create({
      baseURL: `${config.url}/wp-json/wp/v2`,
      auth: {
        username: config.username,
        password: config.password
      },
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'OpenClaw-WordPress-Publisher/1.0'
      },
      timeout: 10000
    });
  }
  
  async testConnection() {
    console.log('🔍 测试WordPress连接...');
    
    try {
      // 测试1: API基础连接
      const apiTest = await this.api.get('/');
      console.log('✅ WordPress REST API连接成功');
      
      // 测试2: 用户认证
      const userTest = await this.api.get('/users/me');
      console.log(`✅ 用户认证成功: ${userTest.data.name}`);
      console.log(`   角色: ${userTest.data.roles?.join(', ') || '未知'}`);
      console.log(`   ID: ${userTest.data.id}`);
      
      return {
        success: true,
        user: userTest.data
      };
    } catch (error) {
      console.log('❌ 连接测试失败:', error.response?.data?.message || error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  async getOrCreateTag(tagName) {
    console.log(`🔍 查找或创建标签: "${tagName}"`);
    
    try {
      // 先搜索现有标签
      const searchResponse = await this.api.get(`/tags?search=${encodeURIComponent(tagName)}&per_page=1`);
      
      if (searchResponse.data && searchResponse.data.length > 0) {
        console.log(`✅ 找到现有标签: ${searchResponse.data[0].name} (ID: ${searchResponse.data[0].id})`);
        return searchResponse.data[0].id;
      }
      
      // 创建新标签
      console.log(`📝 创建新标签: "${tagName}"`);
      const createResponse = await this.api.post('/tags', {
        name: tagName,
        slug: tagName.toLowerCase().replace(/\s+/g, '-')
      });
      
      console.log(`✅ 标签创建成功: ${createResponse.data.name} (ID: ${createResponse.data.id})`);
      return createResponse.data.id;
      
    } catch (error) {
      console.log(`❌ 标签操作失败: ${error.response?.data?.message || error.message}`);
      return null;
    }
  }
  
  async publishArticle(article) {
    console.log('\n📝 发布文章...');
    console.log(`标题: "${article.title}"`);
    console.log(`状态: ${article.status}`);
    
    // 处理标签 - 获取或创建标签ID
    const tagIds = [];
    if (article.tags && article.tags.length > 0) {
      for (const tagName of article.tags) {
        const tagId = await this.getOrCreateTag(tagName);
        if (tagId) {
          tagIds.push(tagId);
        }
      }
    }
    
    // 准备文章数据（使用正确的格式）
    const postData = {
      title: article.title,
      content: article.content,
      status: article.status || 'draft',
      excerpt: article.excerpt || '',
      categories: article.categories || [1], // 默认未分类
      tags: tagIds // 使用标签ID数组
    };
    
    // 移除空字段
    Object.keys(postData).forEach(key => {
      if (postData[key] === undefined || postData[key] === null || 
          (Array.isArray(postData[key]) && postData[key].length === 0)) {
        delete postData[key];
      }
    });
    
    console.log('\n📦 发送的文章数据:');
    console.log(JSON.stringify(postData, null, 2));
    
    try {
      const response = await this.api.post('/posts', postData);
      
      console.log('\n🎉 文章发布成功!');
      console.log(`文章ID: ${response.data.id}`);
      console.log(`标题: ${response.data.title.rendered}`);
      console.log(`状态: ${response.data.status}`);
      console.log(`链接: ${response.data.link}`);
      console.log(`创建时间: ${response.data.date}`);
      
      if (response.data._links && response.data._links.self) {
        console.log(`API链接: ${response.data._links.self[0].href}`);
      }
      
      return {
        success: true,
        postId: response.data.id,
        post: response.data
      };
      
    } catch (error) {
      console.log('\n❌ 文章发布失败:');
      
      if (error.response) {
        console.log(`状态码: ${error.response.status}`);
        console.log(`错误: ${error.response.data?.message || '未知错误'}`);
        console.log(`错误代码: ${error.response.data?.code || '未知'}`);
        
        if (error.response.data?.data?.params) {
          console.log('\n参数错误详情:');
          console.log(JSON.stringify(error.response.data.data.params, null, 2));
        }
        
        if (error.response.data?.data?.details) {
          console.log('\n详细错误:');
          console.log(JSON.stringify(error.response.data.data.details, null, 2));
        }
      } else {
        console.log(`错误: ${error.message}`);
      }
      
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  async deleteArticle(postId) {
    if (!postId) return false;
    
    console.log(`\n🗑️  删除文章 ${postId}...`);
    
    try {
      await this.api.delete(`/posts/${postId}?force=true`);
      console.log('✅ 文章删除成功');
      return true;
    } catch (error) {
      console.log(`❌ 删除失败: ${error.message}`);
      return false;
    }
  }
}

async function runTest() {
  console.log('🚀 WordPress JWT发布测试 (修复版)\n');
  console.log(`站点: ${config.url}`);
  console.log(`用户: ${config.username}`);
  console.log('='.repeat(60) + '\n');
  
  const publisher = new WordPressPublisher(config);
  
  // 1. 测试连接
  const connection = await publisher.testConnection();
  if (!connection.success) {
    console.log('\n❌ 无法连接到WordPress，停止测试');
    return;
  }
  
  // 2. 准备测试文章
  const testArticle = {
    title: `JWT自动发布测试 ${Date.now()}`,
    content: `# JWT自动发布成功测试
    
这是一个通过修复后的API成功发布的测试文章。

## 测试详情
- **发布时间**: ${new Date().toISOString()}
- **发布方式**: WordPress REST API
- **认证方法**: Basic Auth
- **文章状态**: draft

## 功能验证
✅ 认证通过
✅ 参数格式正确  
✅ 标签处理正常
✅ 文章创建成功

## 技术栈
- WordPress 6.9.4
- REST API v2
- Basic Auth认证
- OpenClaw自动化

*本文由OpenClaw自动生成并发布*`,
    status: 'draft',
    excerpt: 'JWT自动发布功能成功测试',
    categories: [1], // 未分类ID
    tags: ['JWT测试', 'API自动化', 'WordPress'] // 标签名称，会自动转换为ID
  };
  
  // 3. 发布文章
  const publishResult = await publisher.publishArticle(testArticle);
  
  // 4. 清理测试文章
  if (publishResult.success) {
    // 等待2秒让文章完全创建
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 可以选择是否删除测试文章
    const shouldDelete = true; // 设为false可以保留文章
    if (shouldDelete) {
      await publisher.deleteArticle(publishResult.postId);
    } else {
      console.log(`\n📌 测试文章保留，ID: ${publishResult.postId}`);
      console.log(`   链接: ${publishResult.post.link}`);
    }
  }
  
  console.log('\n' + '='.repeat(60));
  
  if (publishResult.success) {
    console.log('🎉 成功! JWT自动发布功能测试通过\n');
    
    console.log('📋 成功配置:');
    console.log(`
const axios = require('axios');

// WordPress配置
const config = {
  url: '${config.url}',
  username: '${config.username}',
  password: '${config.password}'  // 当前密码可用!
};

// 创建API客户端
const api = axios.create({
  baseURL: \`\${config.url}/wp-json/wp/v2\`,
  auth: {
    username: config.username,
    password: config.password
  },
  headers: {
    'Content-Type': 'application/json'
  }
});

// 注意: 标签需要传递ID，不是名称
// 可以先获取或创建标签，然后使用标签ID数组

// 发布文章示例
const postData = {
  title: '文章标题',
  content: '文章内容',
  status: 'draft', // 或 'publish'
  categories: [1], // 分类ID
  tags: [1, 2, 3]  // 标签ID数组
};

const response = await api.post('/posts', postData);
    `);
  } else {
    console.log('❌ 发布失败，需要进一步调试\n');
    
    console.log('🔧 下一步:');
    console.log('1. 检查错误信息中的具体参数问题');
    console.log('2. 验证用户权限和角色');
    console.log('3. 测试简化版本（不带标签）');
  }
  
  console.log('\n🎯 测试完成');
}

// 运行测试
runTest().catch(error => {
  console.error('测试过程中发生未捕获的错误:', error);
});