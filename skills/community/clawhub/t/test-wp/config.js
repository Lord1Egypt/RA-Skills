/**
 * WordPress发布配置示例
 * 复制此文件为 config.js 并填写你的配置
 */

module.exports = {
  // WordPress配置
  wordpress: {
    // WordPress站点URL（必需）
    url: process.env.WORDPRESS_URL || 'https://your-wordpress-site.com',
    
    // WordPress用户名（必需）
    username: process.env.WORDPRESS_USERNAME || 'admin',
    
    // WordPress应用程序密码（必需）
    // 在WordPress后台：用户 → 个人资料 → 应用程序密码
    password: process.env.WORDPRESS_PASSWORD || 'xxxx xxxx xxxx xxxx',
    
    // API端点（通常不需要修改）
    apiBase: '/wp-json/wp/v2',
    
    // 默认文章状态
    // draft: 草稿, publish: 发布, pending: 待审核, private: 私密
    defaultStatus: process.env.DEFAULT_STATUS || 'draft',
    
    // 默认作者ID（1通常是管理员）
    defaultAuthor: parseInt(process.env.DEFAULT_AUTHOR) || 1,
    
    // 媒体文件设置
    mediaPath: process.env.MEDIA_PATH || './media',
    supportedFormats: ['jpg', 'jpeg', 'png', 'gif', 'webp', 'pdf', 'doc', 'docx']
  },
  
  // 文章配置
  posts: {
    // 文章目录
    directory: process.env.POSTS_DIR || './posts',
    
    // 默认分类ID（1通常是未分类）
    defaultCategory: parseInt(process.env.DEFAULT_CATEGORY) || 1,
    
    // 默认标签（数组）
    defaultTags: process.env.DEFAULT_TAGS ? process.env.DEFAULT_TAGS.split(',') : [],
    
    // Markdown转换选项
    markdownOptions: {
      gfm: true,        // GitHub风格Markdown
      breaks: true,     // 将换行符转换为<br>
      sanitize: false   // 不清理HTML
    }
  },
  
  // 发布设置
  publish: {
    // 批量处理大小
    batchSize: parseInt(process.env.BATCH_SIZE) || 5,
    
    // 文章之间的延迟（毫秒）
    delayBetweenPosts: parseInt(process.env.DELAY_BETWEEN_POSTS) || 2000,
    
    // 最大重试次数
    maxRetries: parseInt(process.env.MAX_RETRIES) || 3,
    
    // 重试延迟（毫秒）
    retryDelay: parseInt(process.env.RETRY_DELAY) || 1000
  },
  
  // 日志设置
  logging: {
    // 日志级别：debug, info, warn, error
    level: process.env.LOG_LEVEL || 'info',
    
    // 日志文件路径
    file: process.env.LOG_FILE || './logs/wordpress-publish.log',
    
    // 是否输出到控制台
    console: process.env.LOG_CONSOLE !== 'false'
  }
};

// 环境变量示例：
// WORDPRESS_URL=https://your-site.com
// WORDPRESS_USERNAME=admin
// WORDPRESS_PASSWORD=xxxx xxxx xxxx xxxx
// POSTS_DIR=./posts
// DEFAULT_STATUS=draft
// DEFAULT_CATEGORY=1
// BATCH_SIZE=5
// DELAY_BETWEEN_POSTS=2000
// LOG_LEVEL=info