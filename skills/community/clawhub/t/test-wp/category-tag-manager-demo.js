#!/usr/bin/env node

/**
 * WordPress分类标签管理演示
 */

const axios = require('axios');

const config = {
  wordpressUrl: 'https://your-site.com',
  username: 'admin',
  password: 'your-app-password'
};

class TaxonomyManager {
  constructor(config) {
    this.config = config;
    this.token = null;
    this.api = null;
    this.categories = [];
    this.tags = [];
  }
  
  async initialize() {
    console.log('🚀 初始化分类标签管理器\n');
    console.log(`站点: ${this.config.wordpressUrl}`);
    console.log('='.repeat(60) + '\n');
    
    try {
      // 获取JWT令牌
      const tokenResponse = await axios.post(
        `${this.config.wordpressUrl}/wp-json/jwt-auth/v1/token`,
        {
          username: this.config.username,
          password: this.config.password
        },
        {
          headers: { 'Content-Type': 'application/json' }
        }
      );
      
      this.token = tokenResponse.data.token;
      
      // 创建API客户端
      this.api = axios.create({
        baseURL: `${this.config.wordpressUrl}/wp-json/wp/v2`,
        headers: {
          'Authorization': `Bearer ${this.token}`,
          'Content-Type': 'application/json'
        }
      });
      
      // 加载现有分类标签
      await this.loadTaxonomies();
      
      console.log('✅ 初始化成功!');
      return true;
      
    } catch (error) {
      console.log(`❌ 初始化失败: ${error.message}`);
      return false;
    }
  }
  
  async loadTaxonomies() {
    try {
      // 加载分类
      const catsResponse = await this.api.get('/categories?per_page=50');
      this.categories = catsResponse.data.map(cat => ({
        id: cat.id,
        name: cat.name,
        slug: cat.slug,
        count: cat.count
      }));
      
      // 加载标签
      const tagsResponse = await this.api.get('/tags?per_page=50');
      this.tags = tagsResponse.data.map(tag => ({
        id: tag.id,
        name: tag.name,
        slug: tag.slug,
        count: tag.count
      }));
      
    } catch (error) {
      console.log(`⚠️  加载分类标签失败: ${error.message}`);
    }
  }
  
  async findOrCreateCategory(name) {
    // 先查找
    const existing = this.categories.find(cat => 
      cat.name.toLowerCase() === name.toLowerCase() ||
      cat.slug.toLowerCase() === name.toLowerCase().replace(/\s+/g, '-')
    );
    
    if (existing) {
      return existing;
    }
    
    // 创建新分类
    try {
      const response = await this.api.post('/categories', {
        name: name,
        slug: name.toLowerCase().replace(/\s+/g, '-')
      });
      
      const newCategory = {
        id: response.data.id,
        name: response.data.name,
        slug: response.data.slug,
        count: response.data.count || 0
      };
      
      this.categories.push(newCategory);
      return newCategory;
      
    } catch (error) {
      console.log(`❌ 创建分类失败: ${error.response?.data?.message || error.message}`);
      return null;
    }
  }
  
  async findOrCreateTag(name) {
    // 先查找
    const existing = this.tags.find(tag => 
      tag.name.toLowerCase() === name.toLowerCase() ||
      tag.slug.toLowerCase() === name.toLowerCase().replace(/\s+/g, '-')
    );
    
    if (existing) {
      return existing;
    }
    
    // 创建新标签
    try {
      const response = await this.api.post('/tags', {
        name: name,
        slug: name.toLowerCase().replace(/\s+/g, '-')
      });
      
      const newTag = {
        id: response.data.id,
        name: response.data.name,
        slug: response.data.slug,
        count: response.data.count || 0
      };
      
      this.tags.push(newTag);
      return newTag;
      
    } catch (error) {
      console.log(`❌ 创建标签失败: ${error.response?.data?.message || error.message}`);
      return null;
    }
  }
  
  async processPostTaxonomies(categoryNames, tagNames) {
    console.log(`\n🔧 处理文章分类标签...`);
    console.log(`   分类: ${categoryNames.join(', ')}`);
    console.log(`   标签: ${tagNames.join(', ')}`);
    
    const categoryIds = [];
    const tagIds = [];
    
    // 处理分类
    for (const catName of categoryNames) {
      const category = await this.findOrCreateCategory(catName);
      if (category) {
        categoryIds.push(category.id);
        console.log(`   📁 ${catName} -> ID: ${category.id}`);
      }
    }
    
    // 处理标签
    for (const tagName of tagNames) {
      const tag = await this.findOrCreateTag(tagName);
      if (tag) {
        tagIds.push(tag.id);
        console.log(`   🏷️  ${tagName} -> ID: ${tag.id}`);
      }
    }
    
    return { categoryIds, tagIds };
  }
  
  async publishWithTaxonomies(title, content, categoryNames, tagNames) {
    console.log(`\n📝 发布带分类标签的文章: "${title}"`);
    
    // 处理分类标签
    const { categoryIds, tagIds } = await this.processPostTaxonomies(categoryNames, tagNames);
    
    // 准备文章数据
    const postData = {
      title: title,
      content: content,
      status: 'draft',
      excerpt: '自动分类标签测试',
      categories: categoryIds.length > 0 ? categoryIds : [1], // 默认未分类
      tags: tagIds
    };
    
    try {
      const response = await this.api.post('/posts', postData);
      console.log(`✅ 文章发布成功!`);
      console.log(`   文章ID: ${response.data.id}`);
      console.log(`   分类IDs: [${categoryIds.join(', ')}]`);
      console.log(`   标签IDs: [${tagIds.join(', ')}]`);
      
      return {
        success: true,
        postId: response.data.id,
        post: response.data
      };
      
    } catch (error) {
      console.log(`❌ 文章发布失败: ${error.response?.data?.message || error.message}`);
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  printTaxonomySummary() {
    console.log('\n📊 当前分类标签状态:');
    console.log('-'.repeat(40));
    
    console.log(`📁 分类 (${this.categories.length}):`);
    this.categories.forEach((cat, index) => {
      console.log(`   ${index + 1}. ${cat.name} (ID: ${cat.id}, 文章数: ${cat.count})`);
    });
    
    console.log(`\n🏷️  标签 (${this.tags.length}):`);
    this.tags.forEach((tag, index) => {
      console.log(`   ${index + 1}. ${tag.name} (ID: ${tag.id}, 文章数: ${tag.count})`);
    });
  }
}

async function runDemo() {
  const manager = new TaxonomyManager(config);
  
  // 1. 初始化
  const initialized = await manager.initialize();
  if (!initialized) {
    console.log('❌ 初始化失败，停止演示');
    return;
  }
  
  // 2. 显示当前状态
  manager.printTaxonomySummary();
  
  // 3. 演示自动分类标签处理
  console.log('\n' + '='.repeat(60));
  console.log('🎯 演示自动分类标签处理\n');
  
  const testPosts = [
    {
      title: 'WordPress API开发教程',
      content: 'WordPress REST API开发详细教程...',
      categories: ['技术教程', '编程开发'],
      tags: ['WordPress', 'API', '开发', '教程']
    },
    {
      title: '人工智能最新进展',
      content: '人工智能领域最新研究进展...',
      categories: ['技术教程', '人工智能'],
      tags: ['AI', '机器学习', '深度学习', '技术']
    },
    {
      title: '云计算成本优化',
      content: '如何优化云计算成本...',
      categories: ['技术教程', '云计算'],
      tags: ['云计算', 'AWS', '成本优化', 'DevOps']
    }
  ];
  
  const publishedPosts = [];
  
  for (const post of testPosts) {
    const result = await manager.publishWithTaxonomies(
      `${post.title} - ${new Date().toLocaleTimeString()}`,
      post.content,
      post.categories,
      post.tags
    );
    
    if (result.success) {
      publishedPosts.push(result.postId);
    }
    
    // 添加延迟
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  // 4. 显示更新后的状态
  console.log('\n' + '='.repeat(60));
  console.log('🔄 重新加载分类标签状态...\n');
  await manager.loadTaxonomies();
  manager.printTaxonomySummary();
  
  // 5. 清理测试文章
  console.log('\n' + '='.repeat(60));
  console.log('🧹 清理测试文章...\n');
  
  let cleaned = 0;
  for (const postId of publishedPosts) {
    try {
      await manager.api.delete(`/posts/${postId}?force=true`);
      console.log(`✅ 删除文章 ID: ${postId}`);
      cleaned++;
    } catch (error) {
      console.log(`❌ 删除文章失败 ID: ${postId}: ${error.message}`);
    }
    
    await new Promise(resolve => setTimeout(resolve, 300));
  }
  
  console.log(`\n清理完成: ${cleaned} 篇文章已删除`);
  
  // 6. 最终状态
  console.log('\n' + '='.repeat(60));
  console.log('🎉 分类标签管理演示完成!\n');
  
  console.log('📋 功能总结:');
  console.log('   1. ✅ 自动查找或创建分类');
  console.log('   2. ✅ 自动查找或创建标签');
  console.log('   3. ✅ 批量处理文章分类标签');
  console.log('   4. ✅ 文章自动分类打标');
  console.log('   5. ✅ 分类标签状态管理');
  
  console.log('\n🚀 使用示例:');
  console.log(`
const manager = new TaxonomyManager(config);
await manager.initialize();

// 发布带分类标签的文章
const result = await manager.publishWithTaxonomies(
  '文章标题',
  '文章内容',
  ['技术教程', '编程开发'],  // 分类
  ['WordPress', 'API', '教程'] // 标签
);

if (result.success) {
  console.log('文章已发布，ID:', result.postId);
}
  `);
}

// 运行演示
runDemo().catch(error => {
  console.error('演示过程中发生错误:', error);
});