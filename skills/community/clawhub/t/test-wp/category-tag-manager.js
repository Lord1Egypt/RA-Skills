#!/usr/bin/env node

/**
 * WordPress分类和标签管理器
 * 自动处理分类和标签的创建、查询、更新、删除
 */

const axios = require('axios');

const config = {
  wordpressUrl: 'https://your-site.com',
  username: 'admin',
  password: 'your-app-password'
};

class WordPressTaxonomyManager {
  constructor(config) {
    this.config = config;
    this.token = null;
    this.api = null;
    this.categories = []; // 缓存分类
    this.tags = []; // 缓存标签
  }
  
  async initialize() {
    console.log('🚀 初始化WordPress分类标签管理器\n');
    console.log(`站点: ${this.config.wordpressUrl}`);
    console.log(`用户: ${this.config.username}`);
    console.log('='.repeat(70) + '\n');
    
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
      
      // 加载分类和标签
      await this.loadAllTaxonomies();
      
      return true;
      
    } catch (error) {
      console.log(`❌ 初始化失败: ${error.response?.data?.message || error.message}`);
      return false;
    }
  }
  
  async loadAllTaxonomies() {
    console.log('\n2. 📚 加载所有分类和标签...');
    
    try {
      // 加载分类
      const categoriesResponse = await this.api.get('/categories?per_page=100&orderby=count&order=desc');
      this.categories = categoriesResponse.data.map(cat => ({
        id: cat.id,
        name: cat.name,
        slug: cat.slug,
        description: cat.description || '',
        count: cat.count,
        parent: cat.parent || 0,
        link: cat.link
      }));
      console.log(`✅ 加载 ${this.categories.length} 个分类`);
      
      // 加载标签
      const tagsResponse = await this.api.get('/tags?per_page=100&orderby=count&order=desc');
      this.tags = tagsResponse.data.map(tag => ({
        id: tag.id,
        name: tag.name,
        slug: tag.slug,
        description: tag.description || '',
        count: tag.count,
        link: tag.link
      }));
      console.log(`✅ 加载 ${this.tags.length} 个标签`);
      
      this.printTaxonomySummary();
      
    } catch (error) {
      console.log(`⚠️  加载分类/标签失败: ${error.message}`);
      this.categories = [];
      this.tags = [];
    }
  }
  
  printTaxonomySummary() {
    console.log('\n📊 分类标签概览:');
    console.log('-'.repeat(40));
    
    if (this.categories.length > 0) {
      console.log(`\n📁 分类 (${this.categories.length}):`);
      this.categories.slice(0, 5).forEach((cat, index) => {
        console.log(`   ${index + 1}. ${cat.name} (ID: ${cat.id}, 文章数: ${cat.count})`);
      });
      if (this.categories.length > 5) {
        console.log(`   ... 还有 ${this.categories.length - 5} 个分类`);
      }
    }
    
    if (this.tags.length > 0) {
      console.log(`\n🏷️  标签 (${this.tags.length}):`);
      this.tags.slice(0, 5).forEach((tag, index) => {
        console.log(`   ${index + 1}. ${tag.name} (ID: ${tag.id}, 文章数: ${tag.count})`);
      });
      if (this.tags.length > 5) {
        console.log(`   ... 还有 ${this.tags.length - 5} 个标签`);
      }
    }
  }
  
  // ==================== 分类管理方法 ====================
  
  async createCategory(name, options = {}) {
    console.log(`\n📁 创建分类: "${name}"`);
    
    const categoryData = {
      name: name,
      slug: options.slug || name.toLowerCase().replace(/\s+/g, '-'),
      description: options.description || '',
      parent: options.parent || 0
    };
    
    try {
      const response = await this.api.post('/categories', categoryData);
      const newCategory = {
        id: response.data.id,
        name: response.data.name,
        slug: response.data.slug,
        description: response.data.description || '',
        count: response.data.count || 0,
        parent: response.data.parent || 0
      };
      
      // 更新缓存
      this.categories.push(newCategory);
      
      console.log(`✅ 分类创建成功!`);
      console.log(`   ID: ${newCategory.id}`);
      console.log(`   别名: ${newCategory.slug}`);
      console.log(`   父分类: ${newCategory.parent || '无'}`);
      
      return newCategory;
      
    } catch (error) {
      console.log(`❌ 分类创建失败: ${error.response?.data?.message || error.message}`);
      
      // 如果分类已存在，尝试查找
      if (error.response?.data?.code === 'term_exists') {
        console.log(`🔍 分类可能已存在，尝试查找...`);
        const existing = await this.findCategoryByName(name);
        if (existing) {
          console.log(`✅ 找到已存在的分类: ${existing.name} (ID: ${existing.id})`);
          return existing;
        }
      }
      
      return null;
    }
  }
  
  async findCategoryByName(name) {
    const found = this.categories.find(cat => 
      cat.name.toLowerCase() === name.toLowerCase() ||
      cat.slug.toLowerCase() === name.toLowerCase().replace(/\s+/g, '-')
    );
    
    if (found) {
      return found;
    }
    
    // 如果没有在缓存中找到，尝试API搜索
    try {
      const response = await this.api.get(`/categories?search=${encodeURIComponent(name)}`);
      if (response.data.length > 0) {
        const category = response.data[0];
        return {
          id: category.id,
          name: category.name,
          slug: category.slug,
          description: category.description || '',
          count: category.count || 0,
          parent: category.parent || 0
        };
      }
    } catch (error) {
      // 搜索失败，返回null
    }
    
    return null;
  }
  
  async findOrCreateCategory(name, options = {}) {
    console.log(`\n🔍 查找或创建分类: "${name}"`);
    
    // 先查找
    const existing = await this.findCategoryByName(name);
    if (existing) {
      console.log(`✅ 找到已存在的分类: ${existing.name} (ID: ${existing.id})`);
      return existing;
    }
    
    // 不存在则创建
    return await this.createCategory(name, options);
  }
  
  async updateCategory(categoryId, updates) {
    console.log(`\n✏️  更新分类 ID: ${categoryId}`);
    
    try {
      const response = await this.api.put(`/categories/${categoryId}`, updates);
      
      // 更新缓存
      const index = this.categories.findIndex(cat => cat.id === categoryId);
      if (index !== -1) {
        this.categories[index] = {
          ...this.categories[index],
          ...updates
        };
      }
      
      console.log(`✅ 分类更新成功!`);
      return response.data;
      
    } catch (error) {
      console.log(`❌ 分类更新失败: ${error.response?.data?.message || error.message}`);
      return null;
    }
  }
  
  async deleteCategory(categoryId, force = false) {
    console.log(`\n🗑️  删除分类 ID: ${categoryId}`);
    
    try {
      await this.api.delete(`/categories/${categoryId}?force=${force}`);
      
      // 从缓存中移除
      this.categories = this.categories.filter(cat => cat.id !== categoryId);
      
      console.log(`✅ 分类删除成功!`);
      return true;
      
    } catch (error) {
      console.log(`❌ 分类删除失败: ${error.response?.data?.message || error.message}`);
      return false;
    }
  }
  
  // ==================== 标签管理方法 ====================
  
  async createTag(name, options = {}) {
    console.log(`\n🏷️  创建标签: "${name}"`);
    
    const tagData = {
      name: name,
      slug: options.slug || name.toLowerCase().replace(/\s+/g, '-'),
      description: options.description || ''
    };
    
    try {
      const response = await this.api.post('/tags', tagData);
      const newTag = {
        id: response.data.id,
        name: response.data.name,
        slug: response.data.slug,
        description: response.data.description || '',
        count: response.data.count || 0
      };
      
      // 更新缓存
      this.tags.push(newTag);
      
      console.log(`✅ 标签创建成功!`);
      console.log(`   ID: ${newTag.id}`);
      console.log(`   别名: ${newTag.slug}`);
      
      return newTag;
      
    } catch (error) {
      console.log(`❌ 标签创建失败: ${error.response?.data?.message || error.message}`);
      
      // 如果标签已存在，尝试查找
      if (error.response?.data?.code === 'term_exists') {
        console.log(`🔍 标签可能已存在，尝试查找...`);
        const existing = await this.findTagByName(name);
        if (existing) {
          console.log(`✅ 找到已存在的标签: ${existing.name} (ID: ${existing.id})`);
          return existing;
        }
      }
      
      return null;
    }
  }
  
  async findTagByName(name) {
    const found = this.tags.find(tag => 
      tag.name.toLowerCase() === name.toLowerCase() ||
      tag.slug.toLowerCase() === name.toLowerCase().replace(/\s+/g, '-')
    );
    
    if (found) {
      return found;
    }
    
    // 如果没有在缓存中找到，尝试API搜索
    try {
      const response = await this.api.get(`/tags?search=${encodeURIComponent(name)}`);
      if (response.data.length > 0) {
        const tag = response.data[0];
        return {
          id: tag.id,
          name: tag.name,
          slug: tag.slug,
          description: tag.description || '',
          count: tag.count || 0
        };
      }
    } catch (error) {
      // 搜索失败，返回null
    }
    
    return null;
  }
  
  async findOrCreateTag(name, options = {}) {
    console.log(`\n🔍 查找或创建标签: "${name}"`);
    
    // 先查找
    const existing = await this.findTagByName(name);
    if (existing) {
      console.log(`✅ 找到已存在的标签: ${existing.name} (ID: ${existing.id})`);
      return existing;
    }
    
    // 不存在则创建
    return await this.createTag(name, options);
  }
  
  async updateTag(tagId, updates) {
    console.log(`\n✏️  更新标签 ID: ${tagId}`);
    
    try {
      const response = await this.api.put(`/tags/${tagId}`, updates);
      
      // 更新缓存
      const index = this.tags.findIndex(tag => tag.id === tagId);
      if (index !== -1) {
        this.tags[index] = {
          ...this.tags[index],
          ...updates
        };
      }
      
      console.log(`✅ 标签更新成功!`);
      return response.data;
      
    } catch (error) {
      console.log(`❌ 标签更新失败: ${error.response?.data?.message || error.message}`);
      return null;
    }
  }
  
  async deleteTag(tagId, force = false) {
    console.log(`\n🗑️  删除标签 ID: ${tagId}`);
    
    try {
      await this.api.delete(`/tags/${tagId}?force=${force}`);
      
      // 从缓存中移除
      this.tags = this.tags.filter(tag => tag.id !== tagId);
      
      console.log(`✅ 标签删除成功!`);
      return true;
      
    } catch (error) {
      console.log(`❌ 标签删除失败: ${error.response?.data?.message || error.message}`);
      return false;
    }
  }
  
  // ==================== 批量处理方法 ====================
  
  async processCategoriesForPost(categoryNames) {
    console.log(`\n🔧 处理文章分类: ${categoryNames.join(', ')}`);
    
    const categoryIds = [];
    
    for (const categoryName of categoryNames) {
      const category = await this.findOrCreateCategory(categoryName);
      if (category) {
        categoryIds.push(category.id);
        console.log(`   ✅ ${categoryName} -> ID: ${category.id}`);
      } else {
        console.log(`   ❌ ${categoryName} 处理失败`);
      }
    }
    
    return categoryIds;
  }
  
  async processTagsForPost(tagNames) {
    console.log(`\n🔧 处理文章标签: ${tagNames.join(', ')}`);
    
    const tagIds = [];
    
    for (const tagName of tagNames) {
      const tag = await this.findOrCreateTag(tagName);
      if (tag) {
        tagIds.push(tag.id);
        console.log(`   ✅ ${tagName} -> ID: ${tag.id}`);
      } else {
        console.log(`   ❌ ${tagName} 处理失败`);
      }
    }
    
    return tagIds;
  }
  
  // ==================== 演示功能 ====================
  
  async demonstrateTaxonomyManagement() {
    console.log('\n' + '='.repeat(70));
    console.log('🎯 分类标签管理演示\n');
    
    // 1. 创建一些测试分类
    console.log('1. 📁 创建测试分类...');
    const techCategory = await this.createCategory('技术教程', {
      description: '技术相关教程和指南',
      slug: 'tech-tutorials'
    });
    
    const newsCategory = await this.createCategory('新闻动态', {
      description: '最新行业新闻和动态',
      slug: 'news-updates'
    });
    
    // 2. 创建一些测试标签
    console.log('\n2. 🏷️  创建测试标签...');
    const wordpressTag = await this.createTag('WordPress', {
      description: 'WordPress相关内容'
    });
    
    const apiTag = await this.createTag('API开发', {
      description: 'API开发和集成'
    });
    
    const automationTag = await this.createTag('自动化', {
      description: '自动化工具和流程'
    });
    
    // 3. 演示查找或创建
    console.log('\n3. 🔍 演示查找或创建功能...');
    const existingCategory = await this.findOrCreateCategory('技术教程');
    const newCategory = await this.findOrCreateCategory('产品评测', {
      description: '产品评测和比较'
    });
    
    // 4. 演示批量处理
    console.log('\n4. 🔧 演示批量处理文章分类标签...');
    const postCategories = ['技术教程', '产品评测', '编程开发'];
    const postTags = ['WordPress', 'API开发', '自动化', 'JavaScript'];
    
    const categoryIds = await this.processCategoriesForPost(postCategories);
    const tagIds = await this.processTagsForPost(postTags);
    
    console.log(`\n📋 处理结果:`);
    console.log(`   分类IDs: [${categoryIds.join(', ')}]`);
    console.log(`   标签IDs: [${tagIds.join(', ')}]`);
    
    // 5. 演示发布带分类标签的文章
    console.log('\n5. 📝 演示发布带分类标签的文章...');
    
    if (categoryIds.length > 0 && tagIds.length > 0) {
      const postData = {
        title: `分类标签管理演示文章 - ${new Date().toLocaleTimeString()}`,
        content: `# 分类标签管理演示
        
这是一篇演示分类和标签自动管理的测试文章。

## 分类
${postCategories.map((cat, i) => `${i + 1}. ${cat}`).join('\n')}

## 标签  
${postTags.map((tag, i) => `${i + 1}. ${tag}`).join('\n')}

## 功能演示
✅ 自动查找或创建分类
✅ 自动查找或创建标签
✅ 批量处理分类标签
✅ 文章自动分类打标

*演示时间: ${new Date().toLocaleString()}*`,
        status: 'draft',
        excerpt: '分类标签自动管理演示',
        categories: categoryIds,
        tags: tagIds
      };
      
      try {
        const response = await this.api.post('/posts', postData);
        console.log(`✅ 文章发布成功!`);
        console.log(`   文章ID: ${response.data.id}`);
        console.log(`   标题: ${response.data.title.rendered}`);
        
        const postId = response.data.id;
        
        // 6. 清理演示文章
        console.log('\n6. 🧹 清理演示文章...');
        await this.api.delete(`/posts/${postId}?force=true`);
        console.log(`✅ 演示文章已清理`);
        
      } catch (error) {
