const axios = require('axios');

// 加载环境变量
const path = require('path');
const dotenv = require('dotenv');
const envPath = path.resolve(__dirname, '.env');
dotenv.config({ path: envPath });

// 简单的 Markdown 转 HTML（针对微信公众号优化 - 简洁版）
function markdownToHtml(markdown) {
  let html = markdown
    // 标题
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    // 粗体
    .replace(/\*\*(.*?)\*\*/gim, '<b>$1</b>')
    // 行内代码
    .replace(/`(.*?)`/gim, '<code style="background:#f5f5f5;padding:2px 6px;border-radius:3px;">$1</code>')
    // 代码块
    .replace(/```(\w*)\n([\s\S]*?)```/gim, '<pre style="background:#f5f5f5;padding:15px;border-radius:5px;overflow-x:auto;"><code>$2</code></pre>')
    // 列表
    .replace(/^\d+\.\s+(.*$)/gim, '<p>👉 $1</p>')
    // 分割线
    .replace(/^---$/gim, '<hr/>')
    // 段落（双换行）
    .replace(/\n\n/gim, '</p><p>')
    // 普通换行
    .replace(/\n/gim, '<br/>');
  
  // 包裹在最外层
  html = '<p>' + html + '</p>';
  
  return html;
}

class WeChatMP {
  constructor() {
    this.appId = process.env.WECHAT_APPID;
    this.appSecret = process.env.WECHAT_APPSECRET;
    this.tokenUrl = 'https://api.weixin.qq.com/cgi-bin/token';
    this.draftUrl = 'https://api.weixin.qq.com/cgi-bin/draft/add';
    this.publishUrl = 'https://api.weixin.qq.com/cgi-bin/freepublish/batchpublish';
  }

  // 获取 access_token
  async getAccessToken() {
    try {
      const response = await axios.get(this.tokenUrl, {
        params: {
          grant_type: 'client_credential',
          appid: this.appId,
          secret: this.appSecret
        }
      });
      
      if (response.data.access_token) {
        return response.data.access_token;
      } else {
        throw new Error(`获取 token 失败：${response.data.errmsg}`);
      }
    } catch (error) {
      throw new Error(`网络错误：${error.message}`);
    }
  }

  // 上传永久素材（图片）- 用于草稿箱
  async uploadImage(imagePath) {
    const token = await this.getAccessToken();
    const fs = require('fs');
    const FormData = require('form-data');
    
    const form = new FormData();
    form.append('media', fs.createReadStream(imagePath));
    form.append('title', 'cover_image');
    form.append('introduction', 'cover image for article');
    
    // 使用永久素材接口
    const response = await axios.post(
      `https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=${token}&type=image`,
      form,
      { headers: form.getHeaders() }
    );
    
    if (response.data.media_id) {
      console.log(`✅ 图片上传成功，media_id: ${response.data.media_id}`);
      return response.data.media_id;
    } else {
      throw new Error(`上传图片失败：${response.data.errmsg}`);
    }
  }

  // 创建草稿
  async createDraft(title, content, author = '卡哥 AI 实操', thumbImagePath = null, saveHtml = false) {
    const token = await this.getAccessToken();
    
    // 将 Markdown 转换为 HTML
    const htmlContent = markdownToHtml(content);
    
    // 调试：输出 HTML 长度
    console.log(`📊 HTML 内容长度：${htmlContent.length} 字符`);
    
    // 保存 HTML 到本地（用于调试或手动复制）
    if (saveHtml) {
      const fs = require('fs');
      const htmlPath = path.join(__dirname, 'output.html');
      fs.writeFileSync(htmlPath, htmlContent, 'utf-8');
      console.log(`💾 HTML 已保存到：${htmlPath}`);
    }
    
    // 上传缩略图（如果提供）
    let thumbMediaId = '';
    if (thumbImagePath) {
      console.log(`📷 上传缩略图：${thumbImagePath}`);
      thumbMediaId = await this.uploadImage(thumbImagePath);
    }
    
    const draftData = {
      articles: [{
        title: title,
        author: author,
        content: htmlContent,
        thumb_media_id: thumbMediaId,
        show_cover_pic: thumbMediaId ? 1 : 0,
        need_open_comment: 0,
        only_fans_can_comment: 0,
        digest: title.substring(0, 50)
      }]
    };

    console.log('📦 提交草稿数据...');
    const response = await axios.post(`${this.draftUrl}?access_token=${token}`, draftData);
    
    if (response.data.media_id) {
      return response.data.media_id;
    } else {
      throw new Error(`创建草稿失败：${response.data.errmsg}`);
    }
  }

  // 发布文章
  async publish(mediaId) {
    const token = await this.getAccessToken();
    
    const publishData = {
      media_id: mediaId
    };

    const response = await axios.post(`${this.publishUrl}?access_token=${token}`, publishData);
    
    if (response.data.publish_id) {
      return response.data.publish_id;
    } else {
      throw new Error(`发布失败：${response.data.errmsg}`);
    }
  }

  // 完整发布流程
  async publishArticle(title, content, author, coverImage, saveHtml = false) {
    console.log(`📝 创建草稿：${title}`);
    const mediaId = await this.createDraft(title, content, author, coverImage, saveHtml);
    console.log(`✅ 草稿创建成功，media_id: ${mediaId}`);
    
    console.log(`🚀 发布文章...`);
    const publishId = await this.publish(mediaId);
    console.log(`✅ 发布成功，publish_id: ${publishId}`);
    
    return { mediaId, publishId };
  }
}

// CLI 入口
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  const mp = new WeChatMP();
  
  try {
    if (command === 'token') {
      const token = await mp.getAccessToken();
      console.log(`Access Token: ${token}`);
    } else if (command === 'publish') {
      const title = args.find((a, i) => args[i - 1] === '--title');
      const content = args.find((a, i) => args[i - 1] === '--content');
      const contentFile = args.find((a, i) => args[i - 1] === '--file');
      const author = args.find((a, i) => args[i - 1] === '--author') || '卡哥 AI 实操';
      const coverImage = args.find((a, i) => args[i - 1] === '--cover') || path.join(__dirname, 'cover.jpg');
      const saveHtml = args.includes('--save-html');
      
      // 从文件读取内容或从命令行读取
      let articleContent = '';
      if (contentFile) {
        const fs = require('fs');
        articleContent = fs.readFileSync(contentFile, 'utf-8');
        console.log(`📄 从文件读取内容：${contentFile}`);
      } else if (content) {
        articleContent = content;
      } else {
        console.error('缺少参数：--content 或 --file 是必需的');
        process.exit(1);
      }
      
      if (!title) {
        console.error('缺少参数：--title 是必需的');
        process.exit(1);
      }
      
      await mp.publishArticle(title, articleContent, author, coverImage, saveHtml);
    } else {
      console.log('用法：node index.js <token|publish> [options]');
      console.log('');
      console.log('选项:');
      console.log('  --title     文章标题');
      console.log('  --content   文章内容');
      console.log('  --author    作者名称（可选）');
    }
  } catch (error) {
    console.error(`❌ 错误：${error.message}`);
    process.exit(1);
  }
}

module.exports = WeChatMP;

if (require.main === module) {
  main();
}
