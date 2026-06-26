#!/usr/bin/env node

/**
 * 发布文章到微信公众号
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');
const FormData = require('form-data');

// 微信 API 客户端
class WeChatAPI {
  constructor(configPath = 'config.json') {
    this.configPath = configPath;
    this.config = this.loadConfig();
    this.accessToken = null;
    this.tokenExpiry = 0;
  }

  loadConfig() {
    const configFiles = [
      this.configPath,
      './config.json',
      '../config.json'
    ];

    let config = null;

    for (const file of configFiles) {
      try {
        if (fs.existsSync(file)) {
          console.log(`✅ 找到配置文件: ${file}`);
          config = JSON.parse(fs.readFileSync(file, 'utf8'));
          break;
        }
      } catch (e) {
        // 继续尝试下一个
      }
    }

    if (!config) {
      console.log('\n❌ 未找到配置文件！');
      console.log('💡 请创建 config.json 文件并填写 AppID 和 AppSecret\n');
      console.log('配置文件示例：');
      console.log('  - config.json (脚本所在目录)\n');
      process.exit(1);
    }

    // 兼容旧版配置
    if (!config.wechat?.accounts && config.wechat?.appId) {
      console.log('⚠️  检测到旧版配置格式');
      const oldConfig = config.wechat;
      config.wechat = {
        defaultAccount: 'default',
        accounts: {
          default: {
            name: '默认账号',
            appId: oldConfig.appId,
            appSecret: oldConfig.appSecret,
            type: 'subscription',
            enabled: true
          }
        },
        apiBaseUrl: oldConfig.apiBaseUrl || 'https://api.weixin.qq.com',
        tokenCacheDir: oldConfig.tokenCacheDir || './.tokens'
      };
    }

    return config;
  }

  getAccountConfig() {
    const wechatConfig = this.config.wechat || {};
    const defaultAccount = wechatConfig.defaultAccount || 'default';
    const accounts = wechatConfig.accounts || {};

    if (!accounts[defaultAccount]) {
      throw new Error(`默认账号 ${defaultAccount} 不存在`);
    }

    return accounts[defaultAccount];
  }

  async getAccessToken() {
    // 检查缓存
    if (this.accessToken && Date.now() < this.tokenExpiry) {
      return this.accessToken;
    }

    // 从文件加载
    const account = this.getAccountConfig();
    const cacheDir = this.config.wechat?.tokenCacheDir || './.tokens';
    const cacheFile = `${cacheDir}/token_cache.json`;

    try {
      if (fs.existsSync(cacheFile)) {
        const cache = JSON.parse(fs.readFileSync(cacheFile, 'utf8'));
        // 提前 5 分钟刷新
        if (Date.now() < cache.expires_at - 5 * 60 * 1000) {
          this.accessToken = cache.access_token;
          this.tokenExpiry = cache.expires_at;
          return this.accessToken;
        }
      }
    } catch (e) {
      console.log(`⚠️  加载 token 缓存失败: ${e.message}`);
    }

    // 从微信服务器获取
    const apiBaseUrl = this.config.wechat?.apiBaseUrl || 'https://api.weixin.qq.com';
    const url = `${apiBaseUrl}/cgi-bin/token`;
    const params = {
      grant_type: 'client_credential',
      appid: account.appId,
      secret: account.appSecret
    };

    const response = await axios.get(url, { params });
    const data = response.data;

    if (data.errcode) {
      throw new Error(`获取 Access Token 失败: ${data.errcode} - ${data.errmsg}`);
    }

    this.accessToken = data.access_token;
    this.tokenExpiry = Date.now() + data.expires_in * 1000;

    // 保存缓存
    fs.mkdirSync(cacheDir, { recursive: true });
    fs.writeFileSync(cacheFile, JSON.stringify({
      access_token: this.accessToken,
      expires_at: this.tokenExpiry
    }, null, 2));

    console.log(`✅ Access Token 获取成功`);
    return this.accessToken;
  }

  async uploadImage(imagePath, isThumb = false) {
    /**
     * 上传图片素材
     *
     * @param {string} imagePath - 图片文件路径
     * @param {boolean} isThumb - true=封面图(type=thumb), false=正文图片(type=image)
     * @returns {Promise<{media_id: string, url: string}>}
     */
    const accessToken = await this.getAccessToken();
    const apiBaseUrl = this.config.wechat?.apiBaseUrl || 'https://api.weixin.qq.com';
    const imageType = isThumb ? 'thumb' : 'image';
    const url = `${apiBaseUrl}/cgi-bin/material/add_material?access_token=${accessToken}&type=${imageType}`;

    if (!fs.existsSync(imagePath)) {
      throw new Error(`图片文件不存在: ${imagePath}`);
    }

    // 检查文件大小
    const fileStats = fs.statSync(imagePath);
    const fileSize = fileStats.size;
    const sizeLimit = isThumb ? 64 * 1024 * 1024 : 2 * 1024 * 1024; // 封面64MB，正文2MB
    if (fileSize > sizeLimit) {
      const sizeMB = sizeLimit / 1024 / 1024;
      throw new Error(`图片大小超过 ${sizeMB}MB 限制: ${(fileSize / 1024 / 1024).toFixed(2)}MB`);
    }

    // 检查文件格式
    const allowedExtensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif'];
    if (isThumb) {
      // 封面图只支持 JPG、PNG
      allowedExtensions.length = 0;
      allowedExtensions.push('.jpg', '.jpeg', '.png');
    }
    const fileExt = path.extname(imagePath).toLowerCase();
    if (!allowedExtensions.includes(fileExt)) {
      throw new Error(`不支持的图片格式: ${fileExt}，支持的格式: ${allowedExtensions.join(', ')}`);
    }

    const imageTypeName = isThumb ? '封面图' : '正文图片';
    console.log(`📤 正在上传${imageTypeName}: ${path.basename(imagePath)} (${(fileSize / 1024).toFixed(2)}KB)`);

    const formData = new FormData();
    const fileStream = fs.createReadStream(imagePath);
    formData.append('media', fileStream);

    const response = await axios.post(url, formData, {
      headers: formData.getHeaders(),
      maxContentLength: Infinity,
      maxBodyLength: Infinity
    });

    const data = response.data;

    if (data.errcode && data.errcode !== 0) {
      throw new Error(`上传${imageTypeName}失败: ${data.errcode} - ${data.errmsg}`);
    }

    console.log(`✅ ${imageTypeName}上传成功`);
    if (data.url) {
      console.log(`   URL: ${data.url}`);
    }

    return {
      media_id: data.media_id,
      url: data.url || ''
    };
  }

  async processContentImages(content, baseDir = '.') {
    /**
     * 处理内容中的本地图片，上传到微信并替换 src
     *
     * @param {string} content - HTML 内容
     * @param {string} baseDir - 图片路径的基础目录
     * @returns {Promise<{content: string, uploadedImages: Object}>}
     */
    const imgPattern = /<img[^>]*src=["']([^"']+)["'][^>]*>/gi;
    const matches = [];
    let match;

    while ((match = imgPattern.exec(content)) !== null) {
      matches.push(match[1]);
    }

    if (matches.length === 0) {
      console.log('✓ 未检测到本地图片，跳过上传\n');
      return { content, uploadedImages: {} };
    }

    console.log(`\n📷 检测到 ${matches.length} 张图片，开始处理...\n`);

    const uploadedImages = {};
    let processedContent = content;

    let imageCounter = 1;
    for (const src of matches) {
      // 跳过已经是 URL 的图片（http/https 开头）
      if (src.startsWith('http://') || src.startsWith('https://')) {
        console.log(`  [${imageCounter}] ${src.substring(0, 50)}... - 已是 URL，跳过`);
        imageCounter++;
        continue;
      }

      // 解析图片路径
      const imagePath = path.isAbsolute(src) ? src : path.join(baseDir, src);

      try {
        // 上传图片
        const result = await this.uploadImage(imagePath, false);

        // 替换 src
        if (result.url) {
          const oldSrcRegex = new RegExp(`src=["'](${src.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})["']`, 'g');
          processedContent = processedContent.replace(oldSrcRegex, `src="${result.url}"`);

          uploadedImages[path.basename(src)] = result;
          console.log(`  [${imageCounter}] ${path.basename(src)} - 已替换为微信 URL`);
        } else {
          console.log(`  [${imageCounter}] ${path.basename(src)} - ⚠️ 未返回 URL，保留原始路径`);
        }
      } catch (e) {
        console.log(`  [${imageCounter}] ${path.basename(src)} - ❌ 上传失败: ${e.message}`);
      }

      imageCounter++;
    }

    console.log(`\n✓ 图片处理完成，成功上传 ${Object.keys(uploadedImages).length} 张\n`);
    return { content: processedContent, uploadedImages };
  }

  async createDraft(title, content, thumbMediaId = '') {
    const accessToken = await this.getAccessToken();
    const apiBaseUrl = this.config.wechat?.apiBaseUrl || 'https://api.weixin.qq.com';
    const url = `${apiBaseUrl}/cgi-bin/draft/add?access_token=${accessToken}`;

    // 生成摘要
    const plainText = content.replace(/<[^>]+>/g, '');
    const digest = plainText.substring(0, 120).trim();

    const article = {
      title,
      author: '作者',
      digest,
      content,
      content_source_url: '',
      thumb_media_id: thumbMediaId,
      need_open_comment: 1,
      only_fans_can_comment: 0,
      show_cover_pic: thumbMediaId ? 1 : 0
    };

    const response = await axios.post(url, { articles: [article] });
    const data = response.data;

    if (data.errcode !== undefined && data.errcode !== 0 && !data.media_id) {
      throw new Error(`创建草稿失败: ${data.errcode} - ${data.errmsg}`);
    }

    return data.media_id;
  }
}

// 主函数
async function main(title, content, configPath = 'config.json', thumbImagePath = '', contentBaseDir = '.') {
  console.log('🚀 开始发布公众号文章...\n');

  try {
    const api = new WeChatAPI(configPath);

    // 显示当前账号
    const account = api.getAccountConfig();
    console.log(`📱 使用账号: ${account.name}\n`);

    console.log(`📝 文章标题: ${title}`);
    console.log(`📊 文章长度: ${content.length} 字符\n`);

    // 上传封面图片
    let thumbMediaId = '';
    if (thumbImagePath) {
      console.log('📷 处理封面图片...');
      const thumbResult = await api.uploadImage(thumbImagePath, true);
      thumbMediaId = thumbResult.media_id;
      console.log('');
    }

    // 处理正文图片
    const { content: processedContent, uploadedImages } = await api.processContentImages(content, contentBaseDir);

    // 创建草稿
    const mediaId = await api.createDraft(title, processedContent, thumbMediaId);

    console.log(`✅ 草稿创建成功！`);
    console.log(`   草稿 ID: ${mediaId}`);
    console.log(`   上传封面: ${thumbMediaId ? '是' : '否'}`);
    console.log(`   上传正文图: ${Object.keys(uploadedImages).length} 张`);
    console.log(`   请登录微信公众号后台查看: https://mp.weixin.qq.com/\n`);

    return mediaId;

  } catch (error) {
    console.error(`\n❌ 发布失败: ${error.message}\n`);
    if (error.response) {
      console.error(`错误详情: ${JSON.stringify(error.response.data, null, 2)}\n`);
    }
    console.log('💡 提示:');
    console.log('   1. 检查 AppID 和 AppSecret 是否正确');
    console.log('   2. 确认公众号类型（订阅号/服务号）');
    console.log('   3. 检查 IP 白名单配置');
    console.log('   4. 检查图片文件是否有效\n');
    process.exit(1);
  }
}

// 命令行启动
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length < 2 || args.includes('--help') || args.includes('-h')) {
    console.log('用法: node publish_article.js <标题> <HTML内容|文件路径> [选项]');
    console.log('');
    console.log('选项:');
    console.log('  --config <path>      配置文件路径 (默认: config.json)');
    console.log('  --thumb <path>       封面图片路径');
    console.log('  --content-dir <dir>  正文图片的基础目录 (默认: 当前目录)');
    console.log('  --from-file          从文件读取内容');
    console.log('');
    console.log('示例:');
    console.log('  node publish_article.js "标题" "<p>内容</p>"');
    console.log('  node publish_article.js "标题" "article.html" --from-file --thumb cover.jpg');
    console.log('  node publish_article.js "标题" content.html --from-file --content-dir ./images');
    process.exit(1);
  }

  const options = {
    title: args[0],
    content: args[1],
    config: 'config.json',
    thumb: '',
    contentDir: '.',
    fromFile: false
  };

  // 解析选项
  for (let i = 2; i < args.length; i++) {
    if (args[i] === '--config' && args[i + 1]) {
      options.config = args[i + 1];
      i++;
    } else if (args[i] === '--thumb' && args[i + 1]) {
      options.thumb = args[i + 1];
      i++;
    } else if (args[i] === '--content-dir' && args[i + 1]) {
      options.contentDir = args[i + 1];
      i++;
    } else if (args[i] === '--from-file') {
      options.fromFile = true;
    }
  }

  // 如果是从文件读取
  let content = options.content;
  if (options.fromFile) {
    content = fs.readFileSync(options.content, 'utf8');
  }

  main(options.title, content, options.config, options.thumb, options.contentDir);
}

module.exports = { WeChatAPI, main };