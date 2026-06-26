#!/usr/bin/env node

/**
 * WordPress图片管理器演示
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');
const FormData = require('form-data');

const config = {
  wordpressUrl: 'https://your-site.com',
  username: 'admin',
  password: 'your-app-password'
};

class ImageManagerDemo {
  constructor(config) {
    this.config = config;
    this.token = null;
    this.api = null;
  }
  
  async initialize() {
    console.log('🚀 初始化图片管理器演示\n');
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
      
      return true;
      
    } catch (error) {
      console.log(`❌ 初始化失败: ${error.response?.data?.message || error.message}`);
      return false;
    }
  }
  
  async uploadImage(source, options = {}) {
    console.log(`\n📤 上传图片: ${source.substring(0, 60)}${source.length > 60 ? '...' : ''}`);
    
    try {
      let fileBuffer;
      let fileName;
      let mimeType;
      
      // 判断来源类型
      if (source.startsWith('http')) {
        // 网络图片
        const imageResponse = await axios.get(source, {
          responseType: 'arraybuffer'
        });
        
        fileBuffer = Buffer.from(imageResponse.data);
        mimeType = imageResponse.headers['content-type'] || 'image/jpeg';
        fileName = options.filename || `image_${Date.now()}.jpg`;
        
      } else {
        // 本地文件
        if (!fs.existsSync(source)) {
          console.log(`❌ 文件不存在: ${source}`);
          return null;
        }
        
        fileBuffer = fs.readFileSync(source);
        fileName = options.filename || path.basename(source);
        const ext = path.extname(source).toLowerCase();
        mimeType = this.getMimeType(ext);
      }
      
      // 创建FormData
      const formData = new FormData();
      formData.append('file', fileBuffer, {
        filename: fileName,
        contentType: mimeType
      });
      
      if (options.title) formData.append('title', options.title);
      if (options.alt_text) formData.append('alt_text', options.alt_text);
      if (options.description) formData.append('description', options.description);
      if (options.caption) formData.append('caption', options.caption);
      
      // 上传
      const response = await axios.post(
        `${this.config.wordpressUrl}/wp-json/wp/v2/media`,
        formData,
        {
          headers: {
            'Authorization': `Bearer ${this.token}`,
            ...formData.getHeaders()
          }
        }
      );
      
      console.log(`✅ 图片上传成功!`);
      console.log(`   媒体ID: ${response.data.id}`);
      console.log(`   标题: ${response.data.title.rendered}`);
      console.log(`   链接: ${response.data.source_url}`);
      
      return response.data;
      
    } catch (error) {
      console.log(`❌ 图片上传失败: ${error.response?.data?.message || error.message}`);
      return null;
    }
  }
  
  getMimeType(extension) {
    const types = {
      '.jpg': 'image/jpeg',
      '.jpeg': 'image/jpeg',
      '.png': 'image/png',
      '.gif': 'image/gif',
      '.webp': 'image/webp',
      '.svg': 'image/svg+xml'
    };
    return types[extension] || 'image/jpeg';
  }
  
  async publishPostWithFeaturedImage(title, content, imageSource, options = {}) {
    console.log(`\n🎨 发布带特色图片的文章: "${title}"`);
    
    // 上传特色图片
    const imageResult = await this.uploadImage(imageSource, {
      title: `特色图片 - ${title}`,
      alt_text: options.alt_text || `文章 "${title}" 的特色图片`
    });
    
    if (!imageResult) {
      console.log('❌ 特色图片上传失败');
      return null;
    }
    
    // 发布文章
    const postData = {
      title: title,
      content: content,
      status: options.status || 'draft',
      excerpt: options.excerpt || '',
      categories: options.categories || [1],
      featured_media: imageResult.id
    };
    
    try {
      const response = await this.api.post('/posts', postData);
      
      console.log(`✅ 文章发布成功!`);
      console.log(`   文章ID: ${response.data.id}`);
      console.log(`   特色图片ID: ${imageResult.id}`);
      
      return {
        post: response.data,
        image: imageResult
      };
      
    } catch (error) {
      console.log(`❌ 文章发布失败: ${error.response?.data?.message || error.message}`);
      return null;
    }
  }
  
  async publishPostWithGallery(title, content, imageSources, options = {}) {
    console.log(`\n🖼️  发布带图片画廊的文章: "${title}" (${imageSources.length} 张图片)`);
    
    const uploadedImages = [];
    
    // 上传所有图片
    for (let i = 0; i < imageSources.length; i++) {
      const source = imageSources[i];
      const imageResult = await this.uploadImage(source, {
        title: `图 ${i + 1} - ${title}`,
        alt_text: `文章 "${title}" 的图 ${i + 1}`
      });
      
      if (imageResult) {
        uploadedImages.push(imageResult);
      }
      
      // 延迟避免请求过快
      await this.delay(500);
    }
    
    if (uploadedImages.length === 0) {
      console.log('❌ 没有图片上传成功');
      return null;
    }
    
    // 构建带画廊的内容
    let galleryContent = `# ${title}\n\n${content}\n\n## 图片画廊\n\n`;
    
    uploadedImages.forEach((image, index) => {
      galleryContent += `### 图 ${index + 1}: ${image.title.rendered}\n`;
      galleryContent += `![${image.title.rendered}](${image.source_url})\n`;
      galleryContent += `*${image.caption?.rendered || '文章配图'}*\n\n`;
    });
    
    // 发布文章
    const postData = {
      title: title,
      content: galleryContent,
      status: options.status || 'draft',
      excerpt: options.excerpt || '',
      categories: options.categories || [1]
    };
    
    try {
      const response = await this.api.post('/posts', postData);
      
      console.log(`✅ 带画廊的文章发布成功!`);
      console.log(`   文章ID: ${response.data.id}`);
      console.log(`   图片数量: ${uploadedImages.length}`);
      
      return {
        post: response.data,
        images: uploadedImages
      };
      
    } catch (error) {
      console.log(`❌ 文章发布失败: ${error.response?.data?.message || error.message}`);
      return null;
    }
  }
  
  async updateImageMetadata(mediaId, updates) {
    console.log(`\n✏️  更新图片元数据 ID: ${mediaId}`);
    
    try {
      const response = await this.api.put(`/media/${mediaId}`, updates);
      console.log(`✅ 图片元数据更新成功!`);
      return response.data;
    } catch (error) {
      console.log(`❌ 更新失败: ${error.response?.data?.message || error.message}`);
      return null;
    }
  }
  
  async deleteMedia(mediaId) {
    console.log(`\n🗑️  删除媒体文件 ID: ${mediaId}`);
    
    try {
      await this.api.delete(`/media/${mediaId}?force=true`);
      console.log(`✅ 媒体文件删除成功!`);
      return true;
    } catch (error) {
      console.log(`❌ 删除失败: ${error.response?.data?.message || error.message}`);
      return false;
    }
  }
  
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

async function runDemo() {
  const demo = new ImageManagerDemo(config);
  
  // 1. 初始化
  const initialized = await demo.initialize();
  if (!initialized) {
    console.log('❌ 初始化失败，停止演示');
    return;
  }
  
  // 2. 演示1: 上传单张图片
  console.log('\n' + '='.repeat(70));
  console.log('🎯 演示1: 上传单张图片\n');
  
  const testImageUrl = 'https://images.unsplash.com/photo-1542744095-fcf48d80b0fd?w=800&h=600&fit=crop';
  const uploadedImage = await demo.uploadImage(testImageUrl, {
    title: '演示图片 - 风景',
    alt_text: '美丽的风景图片',
    description: '用于演示的风景图片'
  });
  
  // 3. 演示2: 更新图片元数据
  if (uploadedImage) {
    console.log('\n' + '='.repeat(70));
    console.log('🎯 演示2: 更新图片元数据\n');
    
    await demo.updateImageMetadata(uploadedImage.id, {
      caption: '更新后的图片说明',
      alt_text: '更新后的替代文本'
    });
  }
  
  // 4. 演示3: 发布带特色图片的文章
  console.log('\n' + '='.repeat(70));
  console.log('🎯 演示3: 发布带特色图片的文章\n');
  
  const featuredImageUrl = 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=600&fit=crop';
  
  const featuredPost = await demo.publishPostWithFeaturedImage(
    `特色图片文章演示 ${new Date().toLocaleTimeString()}`,
    `# 带特色图片的文章
    
这是一篇演示WordPress特色图片功能的文章。

## 功能特点
1. 自动上传特色图片
2. 图片自动设置为文章特色图片
3. 完整的图片元数据管理
4. 文章与图片关联

## 技术实现
- WordPress REST API
- JWT认证
- 媒体上传功能
- 文章特色图片设置`,
    featuredImageUrl,
    {
      status: 'draft',
      excerpt: '特色图片功能演示'
    }
  );
  
  // 5. 演示4: 发布带图片画廊的文章
  console.log('\n' + '='.repeat(70));
  console.log('🎯 演示4: 发布带图片画廊的文章\n');
  
  const galleryImages = [
    'https://images.unsplash.com/photo-1542744095-fcf48d80b0fd?w=400&h=300&fit=crop',
    'https://images.unsplash.com/photo-1545235617-9465d2a55698?w=400&h=300&fit=crop',
    'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=400&h=300&fit=crop',
    'https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=400&h=300&fit=crop'
  ];
  
  const galleryPost = await demo.publishPostWithGallery(
    `图片画廊文章演示 ${new Date().toLocaleTimeString()}`,
    `# 带图片画廊的文章
    
这是一篇演示WordPress图片画廊功能的文章。

## 画廊功能
1. 批量上传多张图片
2. 自动插入文章内容
3. 图片标题和说明
4. 响应式图片显示`,
    galleryImages,
    {
      status: 'draft',
      excerpt: '图片画廊功能演示'
    }
  );
  
  // 6. 清理演示内容
  console.log('\n' + '='.repeat(70));
  console.log('🧹 清理演示内容\n');
  
  const mediaToDelete = [];
  
  if (uploadedImage) {
    mediaToDelete.push(uploadedImage.id);
  }
  
  if (featuredPost) {
    console.log(`删除特色图片文章 ID: ${featuredPost.post.id}`);
    try {
      await demo.api.delete(`/posts/${featuredPost.post.id}?force=true`);
      console.log('✅ 文章删除成功');
    } catch (error) {
      console.log(`❌ 文章删除失败: ${error.message}`);
    }
    
    if (featuredPost.image) {
      mediaToDelete.push(featuredPost.image.id);
    }
  }
  
  if (galleryPost) {
    console.log(`\n删除画廊文章 ID: ${galleryPost.post.id}`);
    try {
      await demo.api.delete(`/posts/${galleryPost.post.id}?force=true`);
      console.log('✅ 文章删除成功');
    } catch (error) {
      console.log(`❌ 文章删除失败: ${error.message}`);
    }
    
    if (galleryPost.images) {
      galleryPost.images.forEach(image => {
        mediaToDelete.push(image.id);
      });
    }
  }
  
  // 删除媒体文件
  console.log(`\n删除 ${mediaToDelete.length} 个媒体文件...`);
  for (const mediaId of mediaToDelete) {
    await demo.deleteMedia(mediaId);
    await demo.delay(300);
  }
  
  // 7. 总结
  console.log('\n' + '='.repeat(70));
  console.log('🎉 图片管理器演示完成!\n');
  
  console.log('📋 功能总结:');
  console.log('   1. ✅ 网络图片上传');
  console.log('   2. ✅ 图片元数据管理');
  console.log('   3. ✅ 特色图片设置');
  console.log('   4. ✅ 图片画廊创建');
  console.log('   5. ✅ 批量图片处理');
  console.log('   6. ✅ 媒体文件管理');
  
  console.log('\n🚀 完整的工作流程:');
  console.log(`
1. 获取JWT令牌
2. 上传图片到媒体库
3. 设置图片元数据 (标题、alt文本、描述)
4. 发布文章时关联图片
5. 管理媒体文件 (更新、删除)
  `);
  
  console.log('\n🔧 实际应用场景:');
  console.log('   - 博客文章配图');
  console.log('   - 产品图片上传');
  console.log('   - 新闻图片管理');
  console.log('   - 社交媒体内容');
  console.log('   - 自动化内容发布');
}

// 运行演示
runDemo().catch(error => {
  console.error('演示过程中发生错误:', error);
});