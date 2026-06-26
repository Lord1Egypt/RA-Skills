/**
 * WordPress REST API 客户端
 * 用于与WordPress站点进行交互
 */

const axios = require('axios');
const fs = require('fs').promises;
const path = require('path');
const FormData = require('form-data');

class WordPressAPI {
  constructor(config) {
    this.config = config;
    this.baseURL = `${config.wordpress.url}${config.wordpress.apiBase}`;
    
    // 创建axios实例
    this.client = axios.create({
      baseURL: this.baseURL,
      auth: {
        username: config.wordpress.username,
        password: config.wordpress.password
      },
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      timeout: 30000 // 30秒超时
    });
    
    // 响应拦截器
    this.client.interceptors.response.use(
      response => response,
      error => {
        console.error('WordPress API错误:', error.message);
        if (error.response) {
          console.error('状态码:', error.response.status);
          console.error('响应数据:', error.response.data);
        }
        return Promise.reject(error);
      }
    );
  }
  
  /**
   * 测试API连接
   */
  async testConnection() {
    try {
      const response = await this.client.get('/');
      console.log('✅ WordPress API连接成功');
      console.log('API版本:', response.data.namespace);
      return true;
    } catch (error) {
      console.error('❌ WordPress API连接失败:', error.message);
      return false;
    }
  }
  
  /**
   * 创建文章
   */
  async createPost(postData) {
    try {
      const response = await this.client.post('/posts', postData);
      console.log(`✅ 文章创建成功: ${response.data.id} - ${response.data.title.rendered}`);
      return response.data;
    } catch (error) {
      console.error('❌ 文章创建失败:', error.message);
      throw error;
    }
  }
  
  /**
   * 更新文章
   */
  async updatePost(postId, postData) {
    try {
      const response = await this.client.put(`/posts/${postId}`, postData);
      console.log(`✅ 文章更新成功: ${postId}`);
      return response.data;
    } catch (error) {
      console.error('❌ 文章更新失败:', error.message);
      throw error;
    }
  }
  
  /**
   * 删除文章
   */
  async deletePost(postId, force = false) {
    try {
      const response = await this.client.delete(`/posts/${postId}`, {
        params: { force }
      });
      console.log(`✅ 文章删除成功: ${postId}`);
      return response.data;
    } catch (error) {
      console.error('❌ 文章删除失败:', error.message);
      throw error;
    }
  }
  
  /**
   * 获取文章列表
   */
  async getPosts(options = {}) {
    try {
      const params = {
        per_page: options.perPage || 10,
        page: options.page || 1,
        status: options.status || 'any',
        orderby: options.orderBy || 'date',
        order: options.order || 'desc'
      };
      
      if (options.search) {
        params.search = options.search;
      }
      
      if (options.categories) {
        params.categories = options.categories;
      }
      
      if (options.tags) {
        params.tags = options.tags;
      }
      
      const response = await this.client.get('/posts', { params });
      
      // 获取分页信息
      const total = parseInt(response.headers['x-wp-total'] || 0);
      const totalPages = parseInt(response.headers['x-wp-totalpages'] || 0);
      
      return {
        posts: response.data,
        pagination: {
          total,
          totalPages,
          currentPage: params.page,
          perPage: params.per_page
        }
      };
    } catch (error) {
      console.error('❌ 获取文章列表失败:', error.message);
      throw error;
    }
  }
  
  /**
   * 上传媒体文件
   */
  async uploadMedia(filePath, altText = '', caption = '') {
    try {
      // 读取文件
      const fileBuffer = await fs.readFile(filePath);
      const fileName = path.basename(filePath);
      
      // 创建FormData
      const formData = new FormData();
      formData.append('file', fileBuffer, fileName);
      formData.append('alt_text', altText);
      formData.append('caption', caption);
      
      // 上传文件
      const response = await axios.post(
        `${this.baseURL}/media`,
        formData,
        {
          auth: {
            username: this.config.wordpress.username,
            password: this.config.wordpress.password
          },
          headers: {
            ...formData.getHeaders(),
            'Content-Disposition': `attachment; filename="${fileName}"`
          },
          timeout: 60000 // 60秒超时
        }
      );
      
      console.log(`✅ 媒体文件上传成功: ${response.data.id} - ${response.data.source_url}`);
      return response.data;
    } catch (error) {
      console.error('❌ 媒体文件上传失败:', error.message);
      throw error;
    }
  }
  
  /**
   * 获取分类列表
   */
  async getCategories() {
    try {
      const response = await this.client.get('/categories', {
        params: { per_page: 100 }
      });
      return response.data;
    } catch (error) {
      console.error('❌ 获取分类列表失败:', error.message);
      throw error;
    }
  }
  
  /**
   * 创建分类
   */
  async createCategory(name, slug = '', description = '') {
    try {
      const response = await this.client.post('/categories', {
        name,
        slug: slug || name.toLowerCase().replace(/\s+/g, '-'),
        description
      });
      console.log(`✅ 分类创建成功: ${response.data.id} - ${response.data.name}`);
      return response.data;
    } catch (error) {
      console.error('❌ 分类创建失败:', error.message);
      throw error;
    }
  }
  
  /**
   * 获取标签列表
   */
  async getTags() {
    try {
      const response = await this.client.get('/tags', {
        params: { per_page: 100 }
      });
      return response.data;
    } catch (error) {
      console.error('❌ 获取标签列表失败:', error.message);
      throw error;
    }
  }
  
  /**
   * 创建标签
   */
  async createTag(name, slug = '', description = '') {
    try {
      const response = await this.client.post('/tags', {
        name,
        slug: slug || name.toLowerCase().replace(/\s+/g, '-'),
        description
      });
      console.log(`✅ 标签创建成功: ${response.data.id} - ${response.data.name}`);
      return response.data;
    } catch (error) {
      console.error('❌ 标签创建失败:', error.message);
      throw error;
    }
  }
  
  /**
   * 获取用户信息
   */
  async getUsers() {
    try {
      const response = await this.client.get('/users');
      return response.data;
    } catch (error) {
      console.error('❌ 获取用户列表失败:', error.message);
      throw error;
    }
  }
  
  /**
   * 批量处理文章
   */
  async batchProcess(posts, options = {}) {
    const results = {
      success: [],
      failed: []
    };
    
    for (let i = 0; i < posts.length; i++) {
      const post = posts[i];
      console.log(`处理文章 ${i + 1}/${posts.length}: ${post.title || '未命名'}`);
      
      try {
        const result = await this.createPost(post);
        results.success.push({
          id: result.id,
          title: result.title.rendered,
          url: result.link
        });
        
        // 添加延迟避免请求过快
        if (options.delay && i < posts.length - 1) {
          await new Promise(resolve => setTimeout(resolve, options.delay));
        }
      } catch (error) {
        results.failed.push({
          title: post.title || '未命名',
          error: error.message
        });
        
        // 如果设置了最大重试次数
        if (options.maxRetries > 0) {
          let retryCount = 0;
          while (retryCount < options.maxRetries) {
            retryCount++;
            console.log(`重试 ${retryCount}/${options.maxRetries}: ${post.title || '未命名'}`);
            
            try {
              await new Promise(resolve => setTimeout(resolve, options.retryDelay || 1000));
              const result = await this.createPost(post);
              results.success.push({
                id: result.id,
                title: result.title.rendered,
                url: result.link
              });
              results.failed.pop(); // 从失败列表中移除
              break;
            } catch (retryError) {
              if (retryCount === options.maxRetries) {
                console.error(`重试失败: ${post.title || '未命名'}`);
              }
            }
          }
        }
      }
    }
    
    return results;
  }
}

module.exports = WordPressAPI;