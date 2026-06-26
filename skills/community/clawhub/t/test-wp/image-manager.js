#!/usr/bin/env node

/**
 * WordPress图片管理器
 * 完整的图片上传、管理、优化功能
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');
const FormData = require('form-data');
const { v4: uuidv4 } = require('uuid');

const config = {
  wordpressUrl: 'https://your-site.com',
  username: 'admin',
  password: 'your-app-password'
};

class WordPressImageManager {
  constructor(config) {
    this.config = config;
    this.token = null;
    this.api = null;
    this.mediaCache = new Map(); // 缓存已上传的媒体文件
  }
  
  async initialize() {
    console.log('🚀 初始化WordPress图片管理器\n');
    console.log(`站点: ${this.config.wordpressUrl}`);
    console.log('='.repeat(70) + '\n');
    
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
      console.log('✅ JWT令牌获取成功!');
      
      // 创建API客户端
      this.api = axios.create({
        baseURL: `${this.config.wordpressUrl}/wp-json/wp/v2`,
        headers: {
          'Authorization': `Bearer ${this.token}`,
          'Content-Type': 'application/json'
        }
      });
      
      // 加载现有媒体
      await this.loadMediaLibrary();
      
      return true;
      
    } catch (error) {
      console.log(`❌ 初始化失败: ${error.response?.data?.message || error.message}`);
      return false;
    }
  }
  
  async loadMediaLibrary(page = 1, perPage = 50) {
    console.log(`\n📚 加载媒体库 (第 ${page} 页)...`);
    
    try {
      const response = await this.api.get(`/media?page=${page}&per_page=${perPage}&orderby=date&order=desc`);
      
      response.data.forEach(media => {
        this.mediaCache.set(media.id, {
          id: media.id,
          title: media.title.rendered,
          url: media.source_url,
          mime_type: media.mime_type,
          date: media.date,
          alt_text: media.alt_text || '',
          caption: media.caption?.rendered || '',
          description: media.description?.rendered || '',
          media_details: media.media_details || {}
        });
      });
      
      console.log(`✅ 加载 ${response.data.length} 个媒体文件`);
      console.log(`   媒体库总计: ${this.mediaCache.size} 个文件`);
      
      // 检查是否有更多页
      const totalPages = parseInt(response.headers['x-wp-totalpages']) || 1;
      if (page < totalPages && this.mediaCache.size < 200) { // 限制加载数量
        await this.loadMediaLibrary(page + 1, perPage);
      }
      
    } catch (error) {
      console.log(`⚠️  加载媒体库失败: ${error.message}`);
    }
  }
  
  async uploadImage(source, options = {}) {
    const uploadId = uuidv4().substring(0, 8);
    console.log(`\n📤 [${uploadId}] 上传图片: ${source.substring(0, 50)}${source.length > 50 ? '...' : ''}`);
    
    let fileBuffer;
    let fileName;
    let mimeType;
    
    try {
      // 判断来源类型
      if (source.startsWith('http://') || source.startsWith('https://')) {
        // 网络图片
        console.log(`   [${uploadId}] 1. 下载网络图片...`);
        const imageResponse = await axios.get(source, {
          responseType: 'arraybuffer',
          timeout: 30000
        });
        
        fileBuffer = Buffer.from(imageResponse.data);
        mimeType = imageResponse.headers['content-type'] || 'image/jpeg';
        fileName = options.filename || `image_${Date.now()}_${uploadId}${this.getFileExtension(mimeType)}`;
        
      } else if (fs.existsSync(source)) {
        // 本地文件
        console.log(`   [${uploadId}] 1. 读取本地文件...`);
        fileBuffer = fs.readFileSync(source);
        fileName = options.filename || path.basename(source);
        mimeType = this.getMimeTypeFromExtension(path.extname(source));
        
      } else if (source.startsWith('data:')) {
        // Base64数据
        console.log(`   [${uploadId}] 1. 解析Base64数据...`);
        const matches = source.match(/^data:([A-Za-z-+\/]+);base64,(.+)$/);
        if (!matches || matches.length !== 3) {
          throw new Error('无效的Base64数据格式');
        }
        
        mimeType = matches[1];
        const base64Data = matches[2];
        fileBuffer = Buffer.from(base64Data, 'base64');
        fileName = options.filename || `base64_${Date.now()}_${uploadId}${this.getFileExtension(mimeType)}`;
        
      } else {
        throw new Error('不支持的图片源类型');
      }
      
      // 验证图片
      console.log(`   [${uploadId}] 2. 验证图片...`);
      const fileSizeKB = Math.round(fileBuffer.length / 1024);
      console.log(`      文件名: ${fileName}`);
      console.log(`      类型: ${mimeType}`);
      console.log(`      大小: ${fileSizeKB}KB`);
      
      // 检查文件大小限制 (默认10MB)
      const maxSizeKB = options.maxSizeKB || 10240;
      if (fileSizeKB > maxSizeKB) {
        throw new Error(`文件太大 (${fileSizeKB}KB > ${maxSizeKB}KB)`);
      }
      
      // 创建FormData
      console.log(`   [${uploadId}] 3. 准备上传数据...`);
      const formData = new FormData();
      formData.append('file', fileBuffer, {
        filename: fileName,
        contentType: mimeType
      });
      
      // 添加元数据
      const metaFields = ['title', 'description', 'alt_text', 'caption'];
      metaFields.forEach(field => {
        if (options[field]) {
          formData.append(field, options[field]);
        }
      });
      
      // 上传到WordPress
      console.log(`   [${uploadId}] 4. 上传到WordPress...`);
      const uploadResponse = await axios.post(
        `${this.config.wordpressUrl}/wp-json/wp/v2/media`,
        formData,
        {
          headers: {
            'Authorization': `Bearer ${this.token}`,
            ...formData.getHeaders()
          },
          maxContentLength: Infinity,
          maxBodyLength: Infinity,
          timeout: 60000
        }
      );
      
      // 处理响应
      const mediaData = uploadResponse.data;
      const mediaInfo = {
        id: mediaData.id,
        title: mediaData.title.rendered,
        url: mediaData.source_url,
        mime_type: mediaData.mime_type,
        date: mediaData.date,
        alt_text: mediaData.alt_text || '',
        caption: mediaData.caption?.rendered || '',
        description: mediaData.description?.rendered || '',
        media_details: mediaData.media_details || {},
        sizes: this.extractImageSizes(mediaData)
      };
      
      // 更新缓存
      this.mediaCache.set(mediaData.id, mediaInfo);
      
      console.log(`✅ [${uploadId}] 图片上传成功!`);
      console.log(`   媒体ID: ${mediaInfo.id}`);
      console.log(`   标题: ${mediaInfo.title}`);
      console.log(`   链接: ${mediaInfo.url}`);
      console.log(`   大小: ${mediaInfo.sizes.original.width}x${mediaInfo.sizes.original.height}`);
      
      if (mediaInfo.media_details?.filesize) {
        console.log(`   文件大小: ${Math.round(mediaInfo.media_details.filesize / 1024)}KB`);
      }
      
      return {
        success: true,
        uploadId: uploadId,
        media: mediaInfo
      };
      
    } catch (error) {
      console.log(`❌ [${uploadId}] 图片上传失败: ${error.response?.data?.message || error.message}`);
      
      // 详细错误信息
      if (error.response) {
        console.log(`   状态码: ${error.response.status}`);
        if (error.response.data?.code) {
          console.log(`   错误代码: ${error.response.data.code}`);
        }
      }
      
      return {
        success: false,
        uploadId: uploadId,
        error: error.message
      };
    }
  }
  
  async uploadMultipleImages(sources, options = {}) {
    console.log(`\n📚 批量上传 ${sources.length} 张图片...`);
    
    const results = {
      total: sources.length,
      success: 0,
      failed: 0,
      media: []
    };
    
    // 设置并发限制
    const concurrency = options.concurrency || 3;
    const batches = [];
    
    for (let i = 0; i < sources.length; i += concurrency) {
      batches.push(sources.slice(i, i + concurrency));
    }
    
    for (let batchIndex = 0; batchIndex < batches.length; batchIndex++) {
      const batch = batches[batchIndex];
      console.log(`\n批次 ${batchIndex + 1}/${batches.length} (${batch.length} 张图片)`);
      
      const batchPromises = batch.map((source, index) => {
        const globalIndex = batchIndex * concurrency + index;
        const itemOptions = {
          ...options,
          filename: options.filenames?.[globalIndex] || `image_${Date.now()}_${globalIndex}`
        };
        
        return this.uploadImage(source, itemOptions);
      });
      
      const batchResults = await Promise.all(batchPromises);
      
      batchResults.forEach(result => {
        if (result.success) {
          results.success++;
          results.media.push(result.media);
        } else {
          results.failed++;
        }
      });
      
      // 批次间延迟
      if (batchIndex < batches.length - 1) {
        await this.delay(1000);
      }
    }
    
    console.log(`\n📊 批量上传完成:`);
    console.log(`   成功: ${results.success} 张`);
    console.log(`   失败: ${results.failed} 张`);
    console.log(`   总计: ${results.total} 张`);
    
    return results;
  }
  
  async findImageByUrl(url) {
    // 在缓存中查找
    for (const [id, media] of this.mediaCache.entries()) {
      if (media.url === url) {
        return media;
      }
    }
    
    // 如果没有找到，尝试搜索
    try {
      const searchUrl = encodeURIComponent(url);
      const response = await this.api.get(`/media?search=${searchUrl}`);
      
      if (response.data.length > 0) {
        const mediaData = response.data[0];
        const mediaInfo = {
          id: mediaData.id,
          title: mediaData.title.rendered,
          url: mediaData.source_url,
          mime_type: mediaData.mime_type,
          date: mediaData.date,
          alt_text: mediaData.alt_text || '',
          caption: mediaData.caption?.rendered || '',
          description: mediaData.description?.rendered || '',
          media_details: mediaData.media_details || {},
          sizes: this.extractImageSizes(mediaData)
        };
        
        // 更新缓存
        this.mediaCache.set(mediaData.id, mediaInfo);
        
        return mediaInfo;
      }
    } catch (error) {
      // 搜索失败
    }
    
    return null;
  }
  
  async updateImageMetadata(mediaId, updates) {
    console.log(`\n✏️  更新图片元数据 ID: ${mediaId}`);
    
    try {
      const response = await this.api.put(`/media/${mediaId}`, updates);
      
      // 更新缓存
      if (this.mediaCache.has(mediaId)) {
        const existing = this.mediaCache.get(mediaId);
        this.mediaCache.set(mediaId, {
          ...existing,
          ...updates
        });
      }
      
      console.log(`✅ 图片元数据更新成功!`);
      return {
        success: true,
        media: response.data
      };
      
    } catch (error) {
      console.log(`❌ 图片元数据更新失败: ${error.response?.data?.message || error.message}`);
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  async deleteImage(mediaId) {
    console.log(`\n🗑️  删除图片 ID: ${mediaId}`);
    
    try {
      await this.api.delete(`/media/${mediaId}?force=true`);
      
      // 从缓存中移除
      this.mediaCache.delete(mediaId);
      
      console.log(`✅ 图片删除成功!`);
      return {
        success: true
      };
      
    } catch (error) {
      console.log(`❌ 图片删除失败: ${error.response?.data?.message || error.message}`);
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  async generateFeaturedImagePost(title, content, imageSource, options = {}) {
    console.log(`\n🎨 生成带特色图片的文章: "${title}"`);
    
    // 上传特色图片
    const imageResult = await this.uploadImage(imageSource, {
      title: `特色图片 - ${title}`,
      alt_text: options.alt_text || `文章 "${title}" 的特色图片`,
      description: options.image_description || `文章 "${title}" 的特色图片`
    });
    
    if (!imageResult.success) {
      console.log(`❌ 特色图片上传失败，无法生成文章`);
      return {
        success: false,
        error: '特色图片上传失败'
      };
    }
    
    const featuredImageId = imageResult.media.id;
    
    // 构建文章内容
    const enhancedContent = `# ${title}
    
${content}

## 文章特色图片
![${imageResult.media.title}](${imageResult.media.url})
*${imageResult.media.caption || '文章特色图片'}*`;
    
    // 发布文章
    const postData = {
      title: title,
      content: enhancedContent,
      status: options.status || 'draft',
      excerpt: options.excerpt || '',
      categories: options.categories || [1],
      featured_media: featuredImageId
    };
    
    try {
      const response = await this.api.post('/posts', postData);
      
      console.log(`✅ 带特色图片的文章发布成功!`);
      console.log(`   文章ID: ${response.data.id}`);
      console.log(`   特色图片ID: ${featuredImageId}`);
      console.log(`   文章链接: ${response.data.link}`);
      
      return {
        success: true,
        postId: response.data.id,
        post: response.data,
        featuredImage: imageResult.media
      };
      
    } catch (error) {
      console.log(`❌ 文章发布失败: ${error.response?.data?.message || error.message}`);
      
      // 清理已上传的图片
      await this.deleteImage(featuredImageId);
      
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  // ==================== 工具方法 ====================
  
  getFileExtension(mimeType) {
    const extensions = {
      'image/jpeg': '.jpg',
      'image/png': '.png',
      'image/gif': '.gif',
      'image/webp': '.webp',
      'image/svg+xml': '.svg'
    };
    
    return extensions[mimeType] || '.jpg';
  }
  
  getMimeTypeFromExtension(extension) {
    const mimeTypes = {
      '.jpg': 'image/jpeg',
      '.jpeg': 'image/jpeg',
      '.png': 'image/png',
      '.gif': 'image/gif',
      '.webp': 'image/webp',
      '.svg': 'image/svg+xml'
    };
    
    return mimeTypes[extension.toLowerCase()] || 'image/jpeg';
  }
  
  extractImageSizes(mediaData) {
    const sizes = {
      original: {
        width: mediaData.media_details?.width || 0,
        height: mediaData.media_details?.height || 0,
        url: mediaData.source_url
      }
    };
    
    if (mediaData.media_details?.sizes) {
      Object.entries(mediaData.media_details.sizes).forEach(([sizeName, sizeInfo]) => {
        sizes[sizeName] = {
          width: sizeInfo.width,
          height: sizeInfo.height,
          url: sizeInfo.source_url,
          mime_type: sizeInfo.mime_type
        };
      });
    }
    
    return sizes;
  }
  
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  printMediaLibrarySummary() {
    console.log('\n📊 媒体库概览:');
    console.log('-'.repeat(40));
    
    const images = Array.from(this.mediaCache.values());
    
    if (images.length === 0) {
      console.log('   媒体库为空');
      return;
    }
    
    console.log(`   总计: ${images.length} 个媒体文件`);
    
    // 按类型统计
    const typeStats = {};
    images.forEach(media => {
      const type = media.mime_type.split('/')[0];
      typeStats[type] = (typeStats[type] || 0) + 1;
    });
    
    console.log(`   类型分布:`);
