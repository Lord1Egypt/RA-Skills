#!/usr/bin/env node

/**
 * WordPress文章发布脚本
 * 将Markdown文章发布到WordPress
 */

const fs = require('fs').promises;
const fsSync = require('fs');
const path = require('path');
const marked = require('marked');
const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');

// 导入配置和API
const config = require('./config.js');
const WordPressAPI = require('./wordpress-api.js');

// 创建API客户端
const wpApi = new WordPressAPI(config);

/**
 * 解析Markdown文件
 * @param {string} filePath - Markdown文件路径
 * @returns {Object} 文章数据和元数据
 */
async function parseMarkdownFile(filePath) {
  try {
    const content = await fs.readFile(filePath, 'utf-8');
    
    // 解析Front Matter（YAML格式的元数据）
    const frontMatterRegex = /^---\s*\n([\s\S]*?)\n---\s*\n([\s\S]*)$/;
    const match = content.match(frontMatterRegex);
    
    let metadata = {};
    let markdownContent = content;
    
    if (match) {
      const frontMatter = match[1];
      markdownContent = match[2];
      
      // 简单解析YAML（实际项目中应该使用yaml库）
      frontMatter.split('\n').forEach(line => {
        const colonIndex = line.indexOf(':');
        if (colonIndex > 0) {
          const key = line.substring(0, colonIndex).trim();
          let value = line.substring(colonIndex + 1).trim();
          
          // 处理数组值
          if (value.startsWith('[') && value.endsWith(']')) {
            value = value.slice(1, -1).split(',').map(item => item.trim());
          }
          
          metadata[key] = value;
        }
      });
    }
    
    // 转换Markdown为HTML
    const htmlContent = marked.parse(markdownContent, config.posts.markdownOptions);
    
    // 提取标题（从第一个h1或使用元数据）
    let title = metadata.title;
    if (!title) {
      const titleMatch = markdownContent.match(/^#\s+(.+)$/m);
      if (titleMatch) {
        title = titleMatch[1];
      } else {
        title = path.basename(filePath, '.md');
      }
    }
    
    // 提取摘要（从第一段或使用元数据）
    let excerpt = metadata.excerpt;
    if (!excerpt) {
      const firstParagraph = markdownContent.match(/^(?!\s*#|!|>|\s*$)(.+)$/m);
      if (firstParagraph) {
        excerpt = firstParagraph[1].substring(0, 150) + '...';
      }
    }
    
    return {
      metadata,
      title,
      excerpt: excerpt || '',
      content: htmlContent,
      rawMarkdown: markdownContent
    };
  } catch (error) {
    console.error(`❌ 解析Markdown文件失败: ${filePath}`, error.message);
    throw error;
  }
}

/**
 * 处理分类和标签
 * @param {Object} metadata - 文章元数据
 * @returns {Object} 分类和标签ID
 */
async function processCategoriesAndTags(metadata) {
  const categories = [];
  const tags = [];
  
  // 处理分类
  if (metadata.categories) {
    const categoryList = Array.isArray(metadata.categories) 
      ? metadata.categories 
      : [metadata.categories];
    
    for (const categoryName of categoryList) {
      try {
        // 先获取现有分类
        const existingCategories = await wpApi.getCategories();
        const existingCategory = existingCategories.find(cat => 
          cat.name.toLowerCase() === categoryName.toLowerCase()
        );
        
        if (existingCategory) {
          categories.push(existingCategory.id);
        } else {
          // 创建新分类
          const newCategory = await wpApi.createCategory(categoryName);
          categories.push(newCategory.id);
        }
      } catch (error) {
        console.warn(`⚠️ 处理分类失败 "${categoryName}":`, error.message);
      }
    }
  }
  
  // 处理标签
  if (metadata.tags) {
    const tagList = Array.isArray(metadata.tags) 
      ? metadata.tags 
      : [metadata.tags];
    
    for (const tagName of tagList) {
      try {
        // 先获取现有标签
        const existingTags = await wpApi.getTags();
        const existingTag = existingTags.find(tag => 
          tag.name.toLowerCase() === tagName.toLowerCase()
        );
        
        if (existingTag) {
          tags.push(existingTag.id);
        } else {
          // 创建新标签
          const newTag = await wpApi.createTag(tagName);
          tags.push(newTag.id);
        }
      } catch (error) {
        console.warn(`⚠️ 处理标签失败 "${tagName}":`, error.message);
      }
    }
  }
  
  return { categories, tags };
}

/**
 * 上传特色图片
 * @param {string} imagePath - 图片路径
 * @returns {number|null} 媒体ID
 */
async function uploadFeaturedImage(imagePath) {
  try {
    if (!fsSync.existsSync(imagePath)) {
      console.warn(`⚠️ 特色图片不存在: ${imagePath}`);
      return null;
    }
    
    const media = await wpApi.uploadMedia(imagePath);
    return media.id;
  } catch (error) {
    console.error(`❌ 上传特色图片失败: ${imagePath}`, error.message);
    return null;
  }
}

/**
 * 发布文章
 * @param {string} filePath - Markdown文件路径
 * @param {Object} options - 发布选项
 */
async function publishPost(filePath, options = {}) {
  try {
    console.log(`📝 处理文章: ${filePath}`);
    
    // 1. 解析Markdown文件
    const article = await parseMarkdownFile(filePath);
    
    // 2. 处理分类和标签
    const { categories, tags } = await processCategoriesAndTags(article.metadata);
    
    // 3. 上传特色图片
    let featuredMediaId = null;
    if (article.metadata.featured_image) {
      const imagePath = path.isAbsolute(article.metadata.featured_image)
        ? article.metadata.featured_image
        : path.join(path.dirname(filePath), article.metadata.featured_image);
      
      featuredMediaId = await uploadFeaturedImage(imagePath);
    }
    
    // 4. 准备文章数据
    const postData = {
      title: article.title,
      content: article.content,
      excerpt: article.excerpt,
      status: options.status || article.metadata.status || config.wordpress.defaultStatus,
      categories: categories.length > 0 ? categories : [config.posts.defaultCategory],
      tags: tags.length > 0 ? tags : config.posts.defaultTags
    };
    
    // 只有在指定了作者ID时才包含author字段
    if (config.wordpress.defaultAuthor !== null) {
      postData.author = config.wordpress.defaultAuthor;
    }
    
    // 添加可选字段
    if (article.metadata.slug) {
      postData.slug = article.metadata.slug;
    }
    
    if (article.metadata.date) {
      postData.date = article.metadata.date;
    }
    
    if (featuredMediaId) {
      postData.featured_media = featuredMediaId;
    }
    
    // 5. 发布文章
    const result = await wpApi.createPost(postData);
    
    console.log(`✅ 文章发布成功！`);
    console.log(`   ID: ${result.id}`);
    console.log(`   标题: ${result.title.rendered}`);
    console.log(`   状态: ${result.status}`);
    console.log(`   链接: ${result.link}`);
    
    return result;
  } catch (error) {
    console.error(`❌ 发布文章失败: ${filePath}`, error.message);
    throw error;
  }
}

/**
 * 主函数
 */
async function main() {
  const argv = yargs(hideBin(process.argv))
    .option('file', {
      alias: 'f',
      type: 'string',
      description: 'Markdown文件路径',
      demandOption: true
    })
    .option('status', {
      alias: 's',
      type: 'string',
      description: '文章状态 (draft/publish/pending/private)',
      default: config.wordpress.defaultStatus
    })
    .option('test', {
      type: 'boolean',
      description: '测试模式（不实际发布）',
      default: false
    })
    .help()
    .alias('help', 'h')
    .argv;
  
  try {
    // 检查文件是否存在
    if (!fsSync.existsSync(argv.file)) {
      console.error(`❌ 文件不存在: ${argv.file}`);
      process.exit(1);
    }
    
    // 测试API连接
    console.log('🔗 测试WordPress API连接...');
    const connected = await wpApi.testConnection();
    if (!connected) {
      console.error('❌ 无法连接到WordPress，请检查配置');
      process.exit(1);
    }
    
    if (argv.test) {
      console.log('🧪 测试模式：只解析文件，不发布');
      const article = await parseMarkdownFile(argv.file);
      console.log('解析结果:', JSON.stringify(article, null, 2));
    } else {
      // 发布文章
      await publishPost(argv.file, { status: argv.status });
    }
    
    console.log('🎉 操作完成！');
  } catch (error) {
    console.error('❌ 操作失败:', error.message);
    process.exit(1);
  }
}

// 运行主函数
if (require.main === module) {
  main();
}

module.exports = {
  parseMarkdownFile,
  publishPost,
  WordPressAPI
};