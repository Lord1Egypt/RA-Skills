#!/usr/bin/env node

/**
 * 发布英文文章带图片（修复版）
 */

const axios = require('axios');
const FormData = require('form-data');

const config = {
  wordpressUrl: 'https://your-site.com',
  username: 'admin',
  password: 'your-app-password'
};

class EnglishArticlePublisher {
  constructor(config) {
    this.config = config;
    this.token = null;
    this.api = null;
  }
  
  async initialize() {
    console.log('🚀 初始化英文文章发布器\n');
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
  
  async uploadImage(imageUrl, options = {}) {
    console.log(`\n📤 上传图片: ${imageUrl.substring(0, 50)}...`);
    
    try {
      // 下载图片
      const imageResponse = await axios.get(imageUrl, {
        responseType: 'arraybuffer'
      });
      
      const buffer = Buffer.from(imageResponse.data);
      const contentType = imageResponse.headers['content-type'] || 'image/jpeg';
      
      // 创建FormData
      const formData = new FormData();
      formData.append('file', buffer, {
        filename: options.filename || `image_${Date.now()}.jpg`,
        contentType: contentType
      });
      
      if (options.title) formData.append('title', options.title);
      if (options.alt_text) formData.append('alt_text', options.alt_text);
      if (options.description) formData.append('description', options.description);
      
      // 上传
      const uploadResponse = await axios.post(
        `${this.config.wordpressUrl}/wp-json/wp/v2/media`,
        formData,
        {
          headers: {
            'Authorization': `Bearer ${this.token}`,
            ...formData.getHeaders()
          }
        }
      );
      
      console.log(`✅ 图片上传成功! ID: ${uploadResponse.data.id}`);
      return uploadResponse.data;
      
    } catch (error) {
      console.log(`❌ 图片上传失败: ${error.message}`);
      return null;
    }
  }
  
  async findOrCreateTag(tagName) {
    console.log(`🔍 查找或创建标签: "${tagName}"`);
    
    try {
      // 先搜索标签
      const searchResponse = await this.api.get(`/tags?search=${encodeURIComponent(tagName)}`);
      
      if (searchResponse.data.length > 0) {
        console.log(`✅ 找到已存在的标签: ${tagName} (ID: ${searchResponse.data[0].id})`);
        return searchResponse.data[0].id;
      }
      
      // 创建新标签
      const createResponse = await this.api.post('/tags', {
        name: tagName,
        slug: tagName.toLowerCase().replace(/\s+/g, '-')
      });
      
      console.log(`✅ 创建新标签: ${tagName} (ID: ${createResponse.data.id})`);
      return createResponse.data.id;
      
    } catch (error) {
      console.log(`❌ 标签处理失败: ${error.message}`);
      return null;
    }
  }
  
  async publishEnglishArticle() {
    console.log('\n' + '='.repeat(60));
    console.log('📝 发布英文文章\n');
    
    // 1. 上传特色图片
    const featuredImageUrl = 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=1200&h=800&fit=crop';
    console.log('1. 上传特色图片...');
    
    const featuredImage = await this.uploadImage(featuredImageUrl, {
      title: 'Featured Image - AI Technology',
      alt_text: 'Artificial Intelligence technology concept',
      description: 'Featured image for AI technology article'
    });
    
    if (!featuredImage) {
      console.log('⚠️  特色图片上传失败，继续发布文章...');
    }
    
    // 2. 上传文章内容图片
    const contentImageUrls = [
      'https://images.unsplash.com/photo-1542744095-fcf48d80b0fd?w=800&h=600&fit=crop',
      'https://images.unsplash.com/photo-1545235617-9465d2a55698?w=800&h=600&fit=crop'
    ];
    
    const contentImages = [];
    console.log('\n2. 上传文章内容图片...');
    
    for (let i = 0; i < contentImageUrls.length; i++) {
      const image = await this.uploadImage(contentImageUrls[i], {
        title: `Content Image ${i + 1} - AI Development`,
        alt_text: `AI development illustration ${i + 1}`
      });
      
      if (image) {
        contentImages.push(image);
      }
      
      // 延迟避免请求过快
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    // 3. 处理标签
    console.log('\n3. 处理文章标签...');
    const tagNames = ['Artificial Intelligence', 'AI', 'Technology', 'Future Trends', '2026'];
    const tagIds = [];
    
    for (const tagName of tagNames) {
      const tagId = await this.findOrCreateTag(tagName);
      if (tagId) {
        tagIds.push(tagId);
      }
      await new Promise(resolve => setTimeout(resolve, 300));
    }
    
    console.log(`✅ 处理完成 ${tagIds.length}/${tagNames.length} 个标签`);
    
    // 4. 构建文章内容
    console.log('\n4. 构建文章内容...');
    
    let articleContent = `# The Future of Artificial Intelligence: Trends and Predictions for 2026

Artificial Intelligence continues to revolutionize industries and transform the way we live and work. As we move into 2026, several key trends are shaping the AI landscape.

## Key AI Trends for 2026

### 1. Generative AI Maturation
Generative AI models are becoming more sophisticated, moving beyond text generation to complex multimodal outputs.`;

    // 添加第一张内容图片
    if (contentImages.length > 0) {
      articleContent += `\n\n![AI Development Illustration](${contentImages[0].source_url})
*Figure 1: AI development and neural networks*`;
    }

    articleContent += `

### 2. Edge AI Expansion
AI processing is moving closer to data sources, reducing latency and improving privacy. Edge devices with AI capabilities are becoming more common in IoT ecosystems.

### 3. AI Ethics and Governance
Increased focus on ethical AI development, transparency, and regulatory compliance will shape how organizations implement AI solutions.`;

    // 添加第二张内容图片
    if (contentImages.length > 1) {
      articleContent += `\n\n![AI Technology Applications](${contentImages[1].source_url})
*Figure 2: AI technology applications across industries*`;
    }

    articleContent += `

## Industry Applications

### Healthcare
AI-powered diagnostics and personalized treatment plans are improving patient outcomes and reducing healthcare costs.

### Finance
Fraud detection, algorithmic trading, and personalized financial advice are being enhanced by AI technologies.

### Manufacturing
Predictive maintenance, quality control, and supply chain optimization are benefiting from AI implementation.

## Challenges and Considerations

While AI offers tremendous potential, several challenges remain:

1. **Data Privacy**: Ensuring compliance with data protection regulations
2. **Bias Mitigation**: Addressing algorithmic bias in AI systems
3. **Skill Gap**: Developing AI talent and expertise
4. **Integration**: Seamlessly integrating AI with existing systems

## Looking Ahead

The AI landscape in 2026 will be characterized by:

- **More accessible AI tools** for non-technical users
- **Increased automation** across business processes
- **Enhanced human-AI collaboration**
- **Stronger regulatory frameworks**

## Conclusion

Artificial Intelligence continues to evolve at a rapid pace. Organizations that strategically adopt and implement AI technologies will gain significant competitive advantages. The key to success lies in balancing innovation with ethical considerations and practical implementation.

*Published on: ${new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}*
*Author: AI Content Assistant*`;

    // 5. 发布文章
    console.log('\n5. 发布文章...');
    
    const postData = {
      title: 'The Future of Artificial Intelligence: Trends and Predictions for 2026',
      content: articleContent,
      status: 'publish', // 直接发布
      excerpt: 'Explore the latest trends and predictions in Artificial Intelligence for 2026, including generative AI, edge computing, and industry applications.',
      categories: [1], // 默认分类
      tags: tagIds.length > 0 ? tagIds : [] // 使用标签ID
    };
    
    // 如果有特色图片，添加到文章数据
    if (featuredImage) {
      postData.featured_media = featuredImage.id;
    }
    
    try {
      const response = await this.api.post('/posts', postData);
      
      console.log('\n' + '='.repeat(60));
      console.log('🎉 文章发布成功!\n');
      
      const articleInfo = {
        id: response.data.id,
        title: response.data.title.rendered,
        link: response.data.link,
        status: response.data.status,
        date: response.data.date,
        featuredImage: featuredImage ? {
          id: featuredImage.id,
          url: featuredImage.source_url
        } : null,
        contentImages: contentImages.map(img => ({
          id: img.id,
          url: img.source_url
        })),
        tags: tagNames
      };
      
      console.log('📋 文章信息:');
      console.log(`   文章ID: ${articleInfo.id}`);
      console.log(`   标题: ${articleInfo.title}`);
      console.log(`   状态: ${articleInfo.status}`);
      console.log(`   发布日期: ${new Date(articleInfo.date).toLocaleString()}`);
      console.log(`   特色图片: ${articleInfo.featuredImage ? '有' : '无'}`);
      console.log(`   内容图片: ${articleInfo.contentImages.length} 张`);
      console.log(`   标签: ${articleInfo.tags.join(', ')}`);
      
      console.log('\n🔗 文章链接:');
      console.log(`   ${articleInfo.link}`);
      
      return articleInfo;
      
    } catch (error) {
      console.log(`❌ 文章发布失败: ${error.response?.data?.message || error.message}`);
      
      if (error.response?.data?.code === 'rest_invalid_param') {
        console.log('🔍 参数错误详情:', JSON.stringify(error.response.data.data.params, null, 2));
      }
      
      return null;
    }
  }
}

async function main() {
  const publisher = new EnglishArticlePublisher(config);
  
  // 初始化
  const initialized = await publisher.initialize();
  if (!initialized) {
    console.log('❌ 初始化失败，无法发布文章');
    return;
  }
  
  // 发布文章
  const article = await publisher.publishEnglishArticle();
  
  if (article) {
    console.log('\n' + '='.repeat(60));
    console.log('✅ 英文文章发布完成!\n');
    
    // 准备发送给用户的消息
    const message = `🎉 英文文章发布成功！

📝 文章标题: ${article.title}
🔗 文章链接: ${article.link}
📅 发布时间: ${new Date(article.date).toLocaleString()}
🖼️  特色图片: ${article.featuredImage ? '已设置' : '无'}
📸 内容图片: ${article.contentImages.length} 张
🏷️  标签: ${article.tags.join(', ')}

文章已直接发布（非草稿状态），可以立即访问。`;
    
    console.log(message);
    
    // 返回文章信息用于发送消息
    return article;
    
  } else {
    console.log('❌ 文章发布失败');
    return null;
  }
}

// 运行
main().catch(error => {
  console.error('发布过程中发生错误:', error);
});