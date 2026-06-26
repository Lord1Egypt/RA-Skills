#!/usr/bin/env node

/**
 * 批量发布多篇文章测试
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
    this.publishedPosts = []; // 存储已发布的文章ID
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
      console.log(`   令牌: ${this.token.substring(0, 30)}...`);
      
      // 创建API客户端
      this.api = axios.create({
        baseURL: `${this.config.wordpressUrl}/wp-json/wp/v2`,
        headers: {
          'Authorization': `Bearer ${this.token}`,
          'Content-Type': 'application/json'
        }
      });
      
      return true;
      
    } catch (error) {
      console.log(`❌ 初始化失败: ${error.response?.data?.message || error.message}`);
      return false;
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
          await this.delay(500); // 500ms延迟
        }
        
      } catch (error) {
        results.failed++;
        results.posts.push({
          title: post.title,
          success: false,
          error: error.response?.data?.message || error.message
        });
        
        console.log(`   ❌ 发布失败: ${error.response?.data?.message || error.message}`);
      }
    }
    
    return results;
  }
  
  async cleanup() {
    console.log('\n' + '='.repeat(60));
    console.log('🗑️  清理测试文章...\n');
    
    if (this.publishedPosts.length === 0) {
      console.log('没有需要清理的文章');
      return;
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
      
      // 添加延迟
      await this.delay(300);
    }
    
    console.log(`\n清理完成: ${deleted} 篇成功, ${failed} 篇失败`);
    return { deleted, failed };
  }
  
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  generateTestPosts(count = 5) {
    console.log(`\n🎨 生成 ${count} 篇测试文章...`);
    
    const posts = [];
    const categories = [
      '技术教程', '产品评测', '行业分析', '使用技巧', '新闻动态',
      '编程开发', '人工智能', '网络安全', '数据分析', '云计算'
    ];
    
    const tags = [
      'WordPress', 'JWT', 'API', '自动化', '测试',
      '开发', '编程', '技术', '教程', '示例'
    ];
    
    for (let i = 1; i <= count; i++) {
      const category = categories[Math.floor(Math.random() * categories.length)];
      const tag1 = tags[Math.floor(Math.random() * tags.length)];
      const tag2 = tags[Math.floor(Math.random() * tags.length)];
      
      const post = {
        title: `批量测试文章 ${i}: ${category} - ${new Date().toLocaleTimeString()}`,
        content: `# ${category} - 批量测试文章 ${i}
        
## 文章信息
- **编号**: ${i}
- **分类**: ${category}
- **标签**: ${tag1}, ${tag2}
- **发布时间**: ${new Date().toISOString()}
- **测试类型**: 批量发布测试

## 内容摘要
这是一篇使用JWT令牌自动发布的测试文章，用于验证WordPress批量发布功能。

### 测试要点
1. ✅ JWT令牌认证
2. ✅ 批量发布功能
3. ✅ 文章内容格式化
4. ✅ 分类和标签设置

### 技术细节
- **认证方式**: JWT令牌
- **发布方式**: WordPress REST API
- **文章状态**: 草稿
- **发布工具**: OpenClaw自动发布系统

## 总结
批量发布测试第 ${i} 篇文章成功完成。

*测试时间: ${new Date().toLocaleString()}*`,
        status: 'draft',
        excerpt: `批量测试文章 ${i} - ${category} - JWT自动发布测试`,
        categories: [1], // 未分类
        tags: [tag1, tag2]
      };
      
      posts.push(post);
      console.log(`   生成: "${post.title}"`);
    }
    
    return posts;
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
    
    // 计算平均发布时间
    const successfulPosts = results.posts.filter(p => p.success && p.duration);
    if (successfulPosts.length > 0) {
      const totalDuration = successfulPosts.reduce((sum, post) => sum + post.duration, 0);
      const avgDuration = Math.round(totalDuration / successfulPosts.length);
      console.log(`\n⏱️  性能统计:`);
      console.log(`   平均发布时间: ${avgDuration}ms`);
      console.log(`   最快: ${Math.min(...successfulPosts.map(p => p.duration))}ms`);
      console.log(`   最慢: ${Math.max(...successfulPosts.map(p => p.duration))}ms`);
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
  const testPosts = publisher.generateTestPosts(5); // 生成5篇测试文章
  
  // 3. 批量发布
  const results = await publisher.publishBatch(testPosts);
  
  // 4. 打印总结
  publisher.printSummary(results);
  
  // 5. 询问是否清理
  console.log('\n' + '='.repeat(60));
  const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  readline.question('是否清理测试文章？(y/n): ', async (answer) => {
    if (answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes') {
      await publisher.cleanup();
    } else {
      console.log('保留测试文章');
      console.log('文章列表:');
      publisher.publishedPosts.forEach((post, index) => {
        console.log(`${index + 1}. ${post.title} - ${post.link}`);
      });
    }
    
    readline.close();
    console.log('\n🎯 批量发布测试完成!');
  });
}

// 运行批量测试
runBatchTest().catch(error => {
  console.error('批量测试过程中发生错误:', error);
});