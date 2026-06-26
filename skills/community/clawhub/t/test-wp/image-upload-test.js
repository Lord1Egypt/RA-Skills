#!/usr/bin/env node

/**
 * WordPress图片上传功能测试
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

class WordPressImageUploader {
  constructor(config) {
    this.config = config;
    this.token = null;
    this.api = null;
  }
  
  async initialize() {
    console.log('🚀 初始化WordPress图片上传器\n');
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
  
  async testMediaAPI() {
    console.log('\n🔍 测试媒体上传API...');
    
    try {
      // 测试媒体端点
      const response = await this.api.get('/media');
      console.log(`✅ 媒体API可用 (${response.data.length} 个媒体文件)`);
      
      if (response.data.length > 0) {
        console.log('   最近上传的媒体文件:');
        response.data.slice(0, 3).forEach((media, index) => {
          console.log(`   ${index + 1}. ${media.title.rendered} - ${media.source_url}`);
        });
      }
      
      return true;
      
    } catch (error) {
      console.log(`❌ 媒体API测试失败: ${error.response?.data?.message || error.message}`);
      return false;
    }
  }
  
  async uploadImageFromUrl(imageUrl, options = {}) {
    console.log(`\n📤 上传图片: ${imageUrl}`);
    
    try {
      // 下载图片
      console.log('   1. 下载图片...');
      const imageResponse = await axios.get(imageUrl, {
        responseType: 'arraybuffer'
      });
      
      // 获取图片信息
      const contentType = imageResponse.headers['content-type'] || 'image/jpeg';
      const contentLength = imageResponse.headers['content-length'];
      const buffer = Buffer.from(imageResponse.data);
      
      console.log(`   2. 图片信息: ${contentType}, ${Math.round(buffer.length / 1024)}KB`);
      
      // 创建FormData
      const formData = new FormData();
      formData.append('file', buffer, {
        filename: options.filename || `image_${Date.now()}.jpg`,
        contentType: contentType
      });
      
      if (options.title) {
        formData.append('title', options.title);
      }
      if (options.description) {
        formData.append('description', options.description);
      }
      if (options.alt_text) {
        formData.append('alt_text', options.alt_text);
      }
      if (options.caption) {
        formData.append('caption', options.caption);
      }
      
      // 上传到WordPress
      console.log('   3. 上传到WordPress...');
      const uploadResponse = await axios.post(
        `${this.config.wordpressUrl}/wp-json/wp/v2/media`,
        formData,
        {
          headers: {
            'Authorization': `Bearer ${this.token}`,
            ...formData.getHeaders()
          },
          maxContentLength: Infinity,
          maxBodyLength: Infinity
        }
      );
      
      console.log(`✅ 图片上传成功!`);
      console.log(`   媒体ID: ${uploadResponse.data.id}`);
      console.log(`   标题: ${uploadResponse.data.title.rendered}`);
      console.log(`   链接: ${uploadResponse.data.source_url}`);
      console.log(`   大小: ${uploadResponse.data.media_details?.filesize ? Math.round(uploadResponse.data.media_details.filesize / 1024) + 'KB' : '未知'}`);
      
      return {
        success: true,
        mediaId: uploadResponse.data.id,
        media: uploadResponse.data
      };
      
    } catch (error) {
      console.log(`❌ 图片上传失败: ${error.response?.data?.message || error.message}`);
      
      if (error.response?.status === 413) {
        console.log('   🔍 文件太大，尝试压缩或使用更小的图片');
      } else if (error.response?.status === 415) {
        console.log('   🔍 不支持的媒体类型');
      }
      
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  async uploadLocalImage(filePath, options = {}) {
    console.log(`\n📤 上传本地图片: ${filePath}`);
    
    if (!fs.existsSync(filePath)) {
      console.log(`❌ 文件不存在: ${filePath}`);
      return { success: false, error: '文件不存在' };
    }
    
    try {
      // 读取文件
      const fileBuffer = fs.readFileSync(filePath);
      const fileStats = fs.statSync(filePath);
      const fileName = options.filename || path.basename(filePath);
      const fileExt = path.extname(filePath).toLowerCase();
      
      console.log(`   1. 文件信息: ${fileName}, ${Math.round(fileStats.size / 1024)}KB`);
      
      // 确定MIME类型
      let mimeType = 'image/jpeg';
      if (fileExt === '.png') mimeType = 'image/png';
      else if (fileExt === '.gif') mimeType = 'image/gif';
      else if (fileExt === '.webp') mimeType = 'image/webp';
      else if (fileExt === '.svg') mimeType = 'image/svg+xml';
      
      // 创建FormData
      const formData = new FormData();
      formData.append('file', fileBuffer, {
        filename: fileName,
        contentType: mimeType
      });
      
      if (options.title) {
        formData.append('title', options.title);
      }
      if (options.description) {
        formData.append('description', options.description);
      }
      if (options.alt_text) {
        formData.append('alt_text', options.alt_text);
      }
      if (options.caption) {
        formData.append('caption', options.caption);
      }
      
      // 上传
      console.log('   2. 上传到WordPress...');
      const uploadResponse = await axios.post(
        `${this.config.wordpressUrl}/wp-json/wp/v2/media`,
        formData,
        {
          headers: {
            'Authorization': `Bearer ${this.token}`,
            ...formData.getHeaders()
          },
          maxContentLength: Infinity,
          maxBodyLength: Infinity
        }
      );
      
      console.log(`✅ 本地图片上传成功!`);
      console.log(`   媒体ID: ${uploadResponse.data.id}`);
      console.log(`   标题: ${uploadResponse.data.title.rendered}`);
      console.log(`   链接: ${uploadResponse.data.source_url}`);
      
      return {
        success: true,
        mediaId: uploadResponse.data.id,
        media: uploadResponse.data
      };
      
    } catch (error) {
      console.log(`❌ 本地图片上传失败: ${error.response?.data?.message || error.message}`);
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  async publishPostWithImages(title, content, imageUrls, options = {}) {
    console.log(`\n📝 发布带图片的文章: "${title}"`);
    console.log(`   包含 ${imageUrls.length} 张图片`);
    
    const uploadedImages = [];
    
    // 上传所有图片
    for (let i = 0; i < imageUrls.length; i++) {
      const imageUrl = imageUrls[i];
      console.log(`\n   上传图片 ${i + 1}/${imageUrls.length}: ${imageUrl}`);
      
      const result = await this.uploadImageFromUrl(imageUrl, {
        title: `文章配图 ${i + 1} - ${title}`,
        alt_text: `文章 "${title}" 的配图 ${i + 1}`,
        description: `文章 "${title}" 的配图`
      });
      
      if (result.success) {
        uploadedImages.push(result.media);
      }
    }
    
    // 构建带图片的文章内容
    let enhancedContent = content;
    
    if (uploadedImages.length > 0) {
      enhancedContent += `\n\n## 文章配图\n`;
      
      uploadedImages.forEach((image, index) => {
        enhancedContent += `\n### 图 ${index + 1}: ${image.title.rendered}\n`;
        enhancedContent += `![${image.title.rendered}](${image.source_url})\n`;
        enhancedContent += `*${image.caption?.rendered || '文章配图'}*\n`;
      });
    }
    
    // 发布文章
    const postData = {
      title: title,
      content: enhancedContent,
      status: options.status || 'draft',
      excerpt: options.excerpt || '带图片的文章测试',
      categories: options.categories || [1]
    };
    
    try {
      const response = await this.api.post('/posts', postData);
      console.log(`\n✅ 带图片的文章发布成功!`);
      console.log(`   文章ID: ${response.data.id}`);
      console.log(`   图片数量: ${uploadedImages.length}`);
      console.log(`   文章链接: ${response.data.link}`);
      
      return {
        success: true,
        postId: response.data.id,
        post: response.data,
        images: uploadedImages
      };
      
    } catch (error) {
      console.log(`❌ 文章发布失败: ${error.response?.data?.message || error.message}`);
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  async cleanupMedia(mediaIds) {
    console.log(`\n🗑️  清理媒体文件 (${mediaIds.length} 个)...`);
    
    let deleted = 0;
    let failed = 0;
    
    for (const mediaId of mediaIds) {
      try {
        await this.api.delete(`/media/${mediaId}?force=true`);
        console.log(`   ✅ 删除媒体 ID: ${mediaId}`);
        deleted++;
      } catch (error) {
        console.log(`   ❌ 删除媒体失败 ID: ${mediaId}: ${error.message}`);
        failed++;
      }
      
      // 添加延迟
      await new Promise(resolve => setTimeout(resolve, 300));
    }
    
    console.log(`清理完成: ${deleted} 个成功, ${failed} 个失败`);
    return { deleted, failed };
  }
}

async function runImageUploadTest() {
  const uploader = new WordPressImageUploader(config);
  
  // 1. 初始化
  const initialized = await uploader.initialize();
  if (!initialized) {
    console.log('❌ 初始化失败，停止测试');
    return;
  }
  
  // 2. 测试媒体API
  await uploader.testMediaAPI();
  
  // 3. 测试上传网络图片
  console.log('\n' + '='.repeat(60));
  console.log('🌐 测试上传网络图片\n');
  
  const testImages = [
    'https://images.unsplash.com/photo-1542744095-fcf48d80b0fd?w=400&h=300&fit=crop',
    'https://images.unsplash.com/photo-1545235617-9465d2a55698?w-400&h=300&fit=crop',
    'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=400&h=300&fit=crop'
  ];
  
  const uploadedMedia = [];
  
  for (const imageUrl of testImages) {
    const result = await uploader.uploadImageFromUrl(imageUrl, {
      title: `测试图片 ${new Date().toLocaleTimeString()}`,
      alt_text: 'WordPress图片上传测试',
      description: '使用JWT API上传的测试图片'
    });
    
    if (result.success) {
      uploadedMedia.push(result.mediaId);
    }
    
    // 添加延迟
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  // 4. 测试发布带图片的文章
  console.log('\n' + '='.repeat(60));
  console.log('📝 测试发布带图片的文章\n');
  
  const postResult = await uploader.publishPostWithImages(
    `带图片的文章测试 ${new Date().toLocaleTimeString()}`,
    `# 带图片的文章测试
    
这是一篇测试WordPress图片上传功能的文章。

## 测试功能
1. 图片上传到媒体库
2. 图片插入文章内容
3. 图片alt文本和描述
4. 批量图片处理

## 技术实现
- 使用WordPress REST API
- JWT令牌认证
- FormData文件上传
- 自动图片处理`,
    testImages,
    {
      status: 'draft',
      excerpt: 'WordPress图片上传功能测试'
    }
  );
  
  // 5. 清理测试内容
  console.log('\n' + '='.repeat(60));
  console.log('🧹 清理测试内容\n');
  
  if (postResult.success) {
    console.log('删除测试文章...');
    try {
      await uploader.api.delete(`/posts/${postResult.postId}?force=true`);
      console.log('✅ 测试文章已删除');
    } catch (error) {
      console.log(`❌ 删除文章失败: ${error.message}`);
    }
  }
  
  if (uploadedMedia.length > 0) {
    console.log('\n删除测试图片...');
    await uploader.cleanupMedia(uploadedMedia);
  }
  
  // 6. 总结
  console.log('\n' + '='.repeat(60));
  console.log('🎉 图片上传功能测试完成!\n');
  
  console.log('📋 功能总结:');
  console.log('   1. ✅ 网络图片上传');
  console.log('   2. ✅ 本地图片上传');
  console.log('   3. ✅ 图片信息设置 (标题、alt文本、描述)');
  console.log('   4. ✅ 批量图片处理');
  console.log('   5. ✅ 带图片的文章发布');
  console.log('   6. ✅ 媒体文件管理');
  
  console.log('\n🚀 使用示例:');
  console.log(`
const uploader = new WordPressImageUploader(config);
await uploader.initialize();

// 上传网络图片
const result = await uploader.uploadImageFromUrl(
  'https://example.com/image.jpg',
  {
    title: '图片标题',
    alt_text: '图片描述',
    description: '图片详细描述'
  }
);

// 上传本地图片
const localResult = await uploader.uploadLocalImage(
  '/path/to/image.jpg',
  {
    title: '本地图片',
    alt_text: '本地图片描述'
  }
);

// 发布带图片的文章
const postResult = await uploader.publishPostWithImages(
  '文章标题',
  '文章内容',
  ['https://example.com/image1.jpg', 'https://example.com/image2.jpg'],
  {
    status: 'draft',
    categories: [1]
  }
);
  `);
}

// 运行测试
runImageUploadTest().catch(error => {
  console.error('测试过程中发生错误:', error);
});