#!/usr/bin/env node

/**
 * 批量发布多篇文章测试（修复版）
 * 修复标签参数问题
 */

const axios = require('axios');

const config = {
  wordpressUrl: 'https://your-site.com',
  username: 'admin',
  password: 'your-app-password'
};

class WordPressBatchPublisher {
  constructor(config) {
    this.config = config;
    this.token = null;
    this.api = null;
    this.publishedPosts = [];
    this.categories = []; // 存储分类信息
    this.tags = []; // 存储标签信息
  }
  
  async initialize() {
    console.log('🚀 初始化WordPress批量发布器\n');
    console.log(`站点: ${this.config.wordpressUrl}`);
    console.log(`用户: ${this.config.username}`);
    console.log('='.repeat(60) + '\n');
    
    // 获取JWT令牌
    console.log('1. 🔐 获取JWT令牌...');
    try {
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
      console.log(`✅ JWT令牌获取成功!`);
      
      // 创建API客户端
      this.api = axios.create({
        baseURL: `${this.config.wordpressUrl}/wp-json/wp/v2`,
        headers: {
          'Authorization': `Bearer ${this.token}`,
          'Content-Type': 'application/json'
        }
      });
      
      // 获取分类和标签信息
      await this.loadCategoriesAndTags();
      
      return true;
      
    } catch (error) {
      console.log(`❌ 初始化失败: ${error.response?.data?.message || error.message}`);
      return false;
    }
  }
  
  async loadCategoriesAndTags() {
    console.log('\n2. 📚 加载分类和标签信息...');
    
    try {
      // 获取分类
      const categoriesResponse = await this.api.get('/categories?per_page=100');
      this.categories = categoriesResponse.data.map(cat => ({
        id: cat.id,
        name: cat.name,
        slug: cat.slug
      }));
      console.log(`✅ 加载 ${this.categories.length} 个分类`);
      
      // 获取标签
      const tagsResponse = await this.api.get('/tags?per_page=100');
      this.tags = tagsResponse.data.map(tag => ({
        id: tag.id,
        name: tag.name,
        slug: tag.slug
      }));
      console.log(`✅ 加载 ${this.tags.length} 个标签`);
      
    } catch (error) {
      console.log(`⚠️  加载分类/标签失败: ${error.message}`);
      this.categories = [{ id: 1, name: '未分类', slug: 'uncategorized' }];
      this.tags = [];
    }
  }
  
  async publishBatch(posts) {
    console.log(`\n📝 开始批量发布 ${posts.length} 篇文章...`);
    console.log('-'.repeat(40));
    
    const results = {
      success: 0,
      failed: 0,
      posts: []
    };
    
    for (let i = 0; i < posts.length; i++) {
      const post = posts[i];
      const postNumber = i + 1;
      
      console.log(`\n${postNumber}/${posts.length}: 发布 "${post.title}"`);
      
      try {
        const startTime = Date.now();
        const response = await this.api.post('/posts', post);
        const endTime = Date.now();
        const duration = endTime - startTime;
        
        const publishedPost = {
          id: response.data.id,
          title: response.data.title.rendered,
          status: response.data.status,
          link: response.data.link,
          duration: duration
        };
        
        this.publishedPosts.push(publishedPost);
        results.success++;
        results.posts.push({
          ...publishedPost,
          success: true
        });
        
        console.log(`   ✅ 发布成功!`);
        console.log(`      文章ID: ${publishedPost.id}`);
        console.log(`      状态: ${publishedPost.status}`);
        console.log(`      耗时: ${duration}ms`);
        
        // 添加延迟，避免请求过快
        if (i < posts.length - 1) {
          await this.delay(500);
        }
        
      } catch (error) {
        results.failed++;
        results.posts.push({
          title: post.title,
          success: false,
          error: error.response?.data?.message || error.message,
          details: error.response?.data?.data || {}
        });
        
        console.log(`   ❌ 发布失败: ${error.response?.data?.message || error.message}`);
        
        if (error.response?.data?.data?.params) {
          console.log(`      参数错误: ${JSON.stringify(error.response.data.data.params)}`);
        }
      }
    }
    
    return results;
  }
  
  generateTestPosts(count = 5) {
    console.log(`\n🎨 生成 ${count} 篇测试文章...`);
    
    const posts = [];
    const postTitles = [
      'JWT自动发布测试：技术教程',
      'WordPress API批量发布实践',
      '人工智能在内容创作中的应用',
      '云计算技术发展趋势分析',
      '网络安全最佳实践指南',
      '数据分析方法与工具介绍',
      '编程开发技巧与经验分享',
      '自动化测试流程优化',
      '产品评测：最新技术工具',
      '行业分析：数字化转型趋势'
    ];
    
    for (let i = 1; i <= count; i++) {
      const titleIndex = Math.min(i - 1, postTitles.length - 1);
      const title = `${postTitles[titleIndex]} ${i} - ${new Date().toLocaleTimeString()}`;
      
      // 使用有效的分类ID（默认使用分类1：未分类）
      const categoryIds = [1];
      
      // 如果有其他分类，随机选择一个
      if (this.categories.length > 1) {
        const randomCategory = this.categories[Math.floor(Math.random() * this.categories.length)];
        if (randomCategory.id !== 1) {
          categoryIds.push(randomCategory.id);
        }
      }
      
      const post = {
        title: title,
        content: `# ${title}
        
## 文章信息
- **编号**: ${i}
- **分类**: ${categoryIds.map(id => this.categories.find(c => c.id === id)?.name || id).join(', ')}
- **发布时间**: ${new Date().toISOString()}
- **测试类型**: 批量发布测试

## 内容摘要
这是一篇使用JWT令牌自动发布的测试文章，用于验证WordPress批量发布功能。

### 测试要点
1. ✅ JWT令牌认证
2. ✅ 批量发布功能  
3. ✅ 文章内容格式化
4. ✅ 分类设置

### 技术细节
- **认证方式**: JWT令牌
- **发布方式**: WordPress REST API
- **文章状态**: 草稿
- **发布工具**: OpenClaw自动发布系统

## 详细内容
这是第 ${i} 篇批量测试文章。通过JWT认证，我们可以实现：
1. 自动化文章发布
2. 定时发布功能
3. 批量内容管理
4. 多平台同步

### 使用场景
- 博客内容自动化管理
- 新闻网站内容发布
- 产品文档自动更新
- 营销内容批量发布

## 总结
批量发布测试第 ${i} 篇文章成功完成。

*测试时间: ${new Date().toLocaleString()}*`,
        status: 'draft',
        excerpt: `批量测试文章 ${i} - JWT自动发布测试`,
        categories: categoryIds
        // 注意：暂时不添加标签，避免参数错误
      };
      
      posts.push(post);
      console.log(`   生成: "${post.title}"`);
    }
    
    return posts;
  }
  
  async cleanup() {
    console.log('\n' + '='.repeat(60));
    console.log('🗑️  清理测试文章...\n');
    
    if (this.publishedPosts.length === 0) {
      console.log('没有需要清理的文章');
      return { deleted: 0, failed: 0 };
    }
    
    let deleted = 0;
    let failed = 0;
    
    for (const post of this.publishedPosts) {
      console.log(`删除文章: ${post.title} (ID: ${post.id})`);
      
      try {
        await this.api.delete(`/posts/${post.id}?force=true`);
        console.log(`   ✅ 删除成功`);
        deleted++;
      } catch (error) {
        console.log(`   ❌ 删除失败: ${error.message}`);
        failed++;
      }
      
      await this.delay(300);
    }
    
    console.log(`\n清理完成: ${deleted} 篇成功, ${failed} 篇失败`);
    return { deleted, failed };
  }
  
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  printSummary(results) {
    console.log('\n' + '='.repeat(60));
    console.log('📊 批量发布结果总结\n');
    
    console.log(`发布统计:`);
    console.log(`   成功: ${results.success} 篇`);
    console.log(`   失败: ${results.failed} 篇`);
    console.log(`   总计: ${results.posts.length} 篇`);
    
    if (results.success > 0) {
      console.log(`\n✅ 成功发布的文章:`);
      results.posts.filter(p => p.success).forEach((post, index) => {
        console.log(`   ${index + 1}. ${post.title}`);
        console.log(`      ID: ${post.id}, 状态: ${post.status}, 耗时: ${post.duration}ms`);
      });
    }
    
    if (results.failed > 0) {
      console.log(`\n❌ 失败的文章:`);
      results.posts.filter(p => !p.success).forEach((post, index) => {
        console.log(`   ${index + 1}. ${post.title}`);
        console.log(`      错误: ${post.error}`);
      });
    }
    
    // 性能统计
    const successfulPosts = results.posts.filter(p => p.success && p.duration);
    if (successfulPosts.length > 0) {
      const totalDuration = successfulPosts.reduce((sum, post) => sum + post.duration, 0);
      const avgDuration = Math.round(totalDuration / successfulPosts.length);
      console.log(`\n⏱️  性能统计:`);
      console.log(`   平均发布时间: ${avgDuration}ms`);
      console.log(`   最快: ${Math.min(...successfulPosts.map(p => p.duration))}ms`);
      console.log(`   最慢: ${Math.max(...successfulPosts.map(p => p.duration))}ms`);
      console.log(`   总耗时: ${totalDuration}ms`);
    }
  }
}

async function runBatchTest() {
  const publisher = new WordPressBatchPublisher(config);
  
  // 1. 初始化
  const initialized = await publisher.initialize();
  if (!initialized) {
    console.log('❌ 初始化失败，停止测试');
    return;
  }
  
  // 2. 生成测试文章
  const testPosts = publisher.generateTestPosts(5);
  
  // 3. 批量发布
  const results = await publisher.publishBatch(testPosts);
  
  // 4. 打印总结
  publisher.printSummary(results);
  
  // 5. 询问是否清理
  console.log('\n' + '='.repeat(60));
  
  // 使用简单的输入方式
  console.log('是否清理测试文章？(输入 y 清理，其他键保留):');
  
  // 设置超时，避免等待太久
  setTimeout(async () => {
    console.log('\n⏰ 超时，默认保留测试文章');
    console.log('\n文章列表:');
    publisher.publishedPosts.forEach((post, index) => {
      console.log(`${index + 1}. ${post.title} - ${post.link}`);
    });
    console.log('\n🎯 批量发布测试完成!');
    process.exit(0);
  }, 10000);
  
  // 监听输入
  process.stdin.setEncoding('utf8');
  process.stdin.once('data', async (data) => {
    const answer = data.toString().trim().toLowerCase();
    
    if (answer === 'y' || answer === 'yes') {
      await publisher.cleanup();
    } else {
      console.log('保留测试文章');
      console.log('\n文章列表:');
      publisher.publishedPosts.forEach((post, index) => {
        console.log(`${index + 1}. ${post.title} - ${post.link}`);
      });
    }
    
    console.log('\n🎯 批量发布测试完成!');
    process.exit(0);
  });
}

// 运行批量测试
runBatchTest().catch(error => {
  console.error('批量测试过程中发生错误:', error);
  process.exit(1);
});