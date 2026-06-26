/**
 * 小红书图文生成技能
 * 基于热点话题自动生成小红书风格的图文内容（文案 + HTML + 图片）
 */

import { existsSync, mkdirSync, writeFileSync, readFileSync } from 'fs';
import { dirname, join, resolve } from 'path';
import { fileURLToPath } from 'url';
import { exec } from 'child_process';
import { promisify } from 'util';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const execAsync = promisify(exec);

/**
 * 默认配置
 */
const DEFAULT_CONFIG = {
  pageWidth: 375,
  pageHeight: 667,
  selector: '.page',
  templates: {
    gossip: '吃瓜爆料型',
    knowledge: '干货科普型',
    recommendation: '种草推荐型'
  }
};

/**
 * 生成小红书图文
 * @param {Object} options - 配置选项
 * @param {string} options.topic - 话题名称
 * @param {string} options.hotData - 热点数据（可选）
 * @param {string} options.template - 模板类型（gossip/knowledge/recommendation）
 * @param {string} options.outputDir - 输出目录
 * @param {number} options.pages - 内页数量（2-4）
 * @returns {Promise<Object>} 生成结果
 */
export async function generateXiaohongshuArticle(options = {}) {
  const {
    topic = '默认话题',
    hotData = null,
    template = 'gossip',
    outputDir = './xiaohongshu-output',
    pages = 3
  } = options;

  console.log('🚀 开始生成小红书图文...\n');
  
  try {
    // 1. 创建输出目录
    const topicDir = join(outputDir, topic);
    const imagesDir = join(topicDir, 'images');
    
    if (!existsSync(topicDir)) {
      mkdirSync(topicDir, { recursive: true });
      console.log(`📁 创建目录：${topicDir}`);
    }
    
    if (!existsSync(imagesDir)) {
      mkdirSync(imagesDir, { recursive: true });
      console.log(`📁 创建图片目录：${imagesDir}`);
    }

    // 2. 生成文案
    console.log('📝 生成文案...');
    const copywriting = await generateCopywriting({ topic, hotData, template });
    const copywritingPath = join(topicDir, 'copywriting.md');
    writeFileSync(copywritingPath, copywriting.content, 'utf-8');
    console.log(`✅ 文案已保存：${copywritingPath}`);

    // 3. 生成 HTML
    console.log('\n🎨 生成 HTML...');
    const htmlContent = await generateHTML({ topic, copywriting, template, pages });
    const htmlPath = join(topicDir, `${topic}.html`);
    writeFileSync(htmlPath, htmlContent, 'utf-8');
    console.log(`✅ HTML 已保存：${htmlPath}`);

    // 4. 转换为图片
    console.log('\n📸 转换为图片...');
    const imagesResult = await convertToImages({
      htmlFile: htmlPath,
      outputDir: imagesDir
    });
    
    console.log(`✅ 图片已保存：${imagesDir}`);

    // 5. 返回结果
    const result = {
      success: true,
      topic,
      outputDir: topicDir,
      files: {
        html: htmlPath,
        copywriting: copywritingPath,
        images: imagesResult.images
      },
      stats: {
        pageCount: imagesResult.count,
        totalSize: imagesResult.totalSize
      }
    };

    console.log('\n✨ 生成完成！\n');
    console.log('📊 生成结果:', JSON.stringify(result, null, 2));
    
    return result;
    
  } catch (error) {
    console.error('❌ 生成失败:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

/**
 * 生成文案
 */
async function generateCopywriting({ topic, hotData, template }) {
  // 根据模板类型生成不同风格的文案
  const templates = {
    gossip: generateGossipCopywriting,
    knowledge: generateKnowledgeCopywriting,
    recommendation: generateRecommendationCopywriting
  };
  
  const generator = templates[template] || templates.gossip;
  return await generator({ topic, hotData });
}

/**
 * 吃瓜爆料型文案生成
 */
async function generateGossipCopywriting({ topic, hotData }) {
  const title = `${topic}❗️网友破防了😭`;
  
  const content = `# ${title}

## 正文

家人们谁懂啊！！${topic} 终于来了🎉
来看看大家都怎么说👇

---

🔥 热搜第一：${topic}

💬 评论区炸锅了：
- 「这也太真实了」
- 「破防了家人们」
- 「你怎么看？」

---

❓ 互动话题：
你对这件事怎么看？
评论区聊聊👇

#${topic.replace(/\s/g, '')} #热点 #吃瓜 #网友热议 #话题讨论
`;

  return { title, content, template: 'gossip' };
}

/**
 * 干货科普型文案生成
 */
async function generateKnowledgeCopywriting({ topic, hotData }) {
  const title = `${topic}💡一篇看懂`;
  
  const content = `# ${title}

## 正文

超实用的${topic}指南来了📚
建议收藏慢慢看👇

---

📌 核心知识点：
1. 第一点
2. 第二点
3. 第三点

---

💡 实用建议：
- 建议 1
- 建议 2
- 建议 3

---

❓ 有问题吗？
评论区问我👇

#${topic.replace(/\s/g, '')} #干货 #科普 #知识分享 #学习
`;

  return { title, content, template: 'knowledge' };
}

/**
 * 种草推荐型文案生成
 */
async function generateRecommendationCopywriting({ topic, hotData }) {
  const title = `${topic}🛒真香警告`;
  
  const content = `# ${title}

## 正文

挖到宝了！！${topic}真的绝了✨
用完忍不住来分享👇

---

🌟 使用体验：
- 优点 1
- 优点 2
- 优点 3

---

💰 购买建议：
- 适合人群
- 入手渠道
- 价格参考

---

❓ 有其他问题吗？
评论区问我👇

#${topic.replace(/\s/g, '')} #种草 #推荐 #好物分享 #真香
`;

  return { title, content, template: 'recommendation' };
}

/**
 * 生成 HTML
 */
async function generateHTML({ topic, copywriting, template, pages }) {
  // 根据模板选择样式
  const styles = {
    gossip: {
      primaryColor: '#FF6B35',
      secondaryColor: '#FFD700',
      gradient: 'linear-gradient(135deg, #FF6B35 0%, #FFD700 100%)'
    },
    knowledge: {
      primaryColor: '#00C072',
      secondaryColor: '#00E68A',
      gradient: 'linear-gradient(135deg, #00C072 0%, #00E68A 100%)'
    },
    recommendation: {
      primaryColor: '#FF69B4',
      secondaryColor: '#FFB6C1',
      gradient: 'linear-gradient(135deg, #FF69B4 0%, #FFB6C1 100%)'
    }
  };
  
  const style = styles[template] || styles.gossip;
  
  // 生成基础 HTML 结构
  const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${copywriting.title} - 小红书图文</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #f5f5f5;
        }
        .page {
            width: ${DEFAULT_CONFIG.pageWidth}px;
            height: ${DEFAULT_CONFIG.pageHeight}px;
            background: white;
            margin: 20px auto;
            position: relative;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .cover {
            background: ${style.gradient};
            padding: 50px 25px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .cover-icon { font-size: 60px; margin-bottom: 20px; }
        .cover-title {
            font-size: 28px;
            font-weight: 900;
            color: white;
            text-align: center;
            line-height: 1.3;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
            margin-bottom: 18px;
        }
        .cover-subtitle {
            font-size: 14px;
            color: white;
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 20px;
            text-align: center;
            font-weight: 600;
        }
        .cover-badge {
            position: absolute;
            top: 25px;
            right: 20px;
            background: ${style.secondaryColor};
            color: ${style.primaryColor};
            padding: 6px 14px;
            border-radius: 14px;
            font-size: 11px;
            font-weight: 800;
        }
        .cover-hot {
            position: absolute;
            top: 25px;
            left: 20px;
            background: rgba(255,255,255,0.95);
            color: ${style.primaryColor};
            padding: 5px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
        }
        .inner-page { padding: 30px 18px; }
        .page-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 18px;
        }
        .page-number {
            background: ${style.gradient};
            color: white;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            font-weight: 700;
            flex-shrink: 0;
        }
        .page-title { font-size: 17px; font-weight: 700; color: #333; flex: 1; }
        
        .comment-card, .info-card {
            background: #f8f8f8;
            border-radius: 12px;
            padding: 14px;
            margin-bottom: 10px;
            border-left: 3px solid ${style.primaryColor};
        }
        .comment-user {
            font-size: 12px;
            font-weight: 700;
            color: #333;
            margin-bottom: 6px;
        }
        .comment-text {
            font-size: 12px;
            color: #666;
            line-height: 1.5;
        }
        .comment-likes {
            font-size: 11px;
            color: #999;
            margin-top: 6px;
        }
        
        .info-box {
            background: linear-gradient(135deg, #FFF5F5 0%, #FFF0F0 100%);
            border: 2px solid #FF6B6B;
            border-radius: 16px;
            padding: 18px;
            margin-bottom: 12px;
        }
        .info-title {
            font-size: 15px;
            font-weight: 700;
            color: #FF6B6B;
            margin-bottom: 12px;
        }
        .info-item {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px dashed rgba(255, 107, 107, 0.3);
            font-size: 13px;
        }
        .info-item:last-child { border-bottom: none; }
        
        .question-box {
            background: ${style.gradient};
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            color: white;
            margin-top: 15px;
        }
        .question-text { font-size: 15px; font-weight: 700; margin-bottom: 8px; }
        .question-cta { font-size: 13px; opacity: 0.9; }
        
        .tag-pill {
            display: inline-block;
            background: ${style.primaryColor};
            color: white;
            font-size: 10px;
            padding: 3px 10px;
            border-radius: 10px;
            margin-right: 6px;
        }
        
        .bottom-note {
            text-align: center;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #eee;
            font-size: 11px;
            color: #999;
        }
    </style>
</head>
<body>
    <!-- 封面页 -->
    <div class="page cover">
        <div class="cover-hot">🔥 热搜</div>
        <div class="cover-badge">热门</div>
        <div class="cover-icon">😭</div>
        <div class="cover-title">${topic}<br>破防了！</div>
        <div class="cover-subtitle">网友：这也太真实了</div>
    </div>

    <!-- 内页 1：评论 -->
    <div class="page inner-page">
        <div class="page-header">
            <div class="page-number">1</div>
            <div class="page-title">评论区炸锅了💬</div>
        </div>
        
        <div class="comment-card">
            <div class="comment-user">📌 网友 A</div>
            <div class="comment-text">
                "这也太真实了吧！"
            </div>
            <div class="comment-likes">❤️ 点赞</div>
        </div>
        
        <div class="comment-card">
            <div class="comment-user">📌 网友 B</div>
            <div class="comment-text">
                "破防了家人们"
            </div>
            <div class="comment-likes">❤️ 点赞</div>
        </div>
        
        <div class="comment-card">
            <div class="comment-user">📌 网友 C</div>
            <div class="comment-text">
                "你怎么看？"
            </div>
            <div class="comment-likes">❤️ 评论区见</div>
        </div>
        
        <div style="text-align: center; margin-top: 12px;">
            <span class="tag-pill">🔥 热度爆炸</span>
            <span class="tag-pill">💬 评论炸锅</span>
        </div>
    </div>

    <!-- 内页 2：信息 -->
    <div class="page inner-page">
        <div class="page-header">
            <div class="page-number">2</div>
            <div class="page-title">详细信息📊</div>
        </div>
        
        <div class="info-box">
            <div class="info-title">📌 核心信息</div>
            <div class="info-item">
                <span>关键点 1</span>
                <span>详情</span>
            </div>
            <div class="info-item">
                <span>关键点 2</span>
                <span>详情</span>
            </div>
            <div class="info-item">
                <span>关键点 3</span>
                <span>详情</span>
            </div>
        </div>
    </div>

    <!-- 内页 3：互动 -->
    <div class="page inner-page">
        <div class="page-header">
            <div class="page-number">3</div>
            <div class="page-title">互动时间🙋</div>
        </div>
        
        <div class="question-box">
            <div class="question-text">❓ 你怎么看？</div>
            <div class="question-cta">评论区聊聊👇</div>
        </div>
        
        <div class="bottom-note">
            关注我，持续追踪热点 🔥<br>
            <span style="font-size: 10px;">数据来源：网络热点</span>
        </div>
    </div>
</body>
</html>`;

  return html;
}

/**
 * 转换为图片
 * 调用 html-pages-to-images 技能
 */
async function convertToImages({ htmlFile, outputDir }) {
  try {
    // 动态导入 html-pages-to-images 的 lib 函数
    const { convertPagesToImages } = await import('../html-pages-to-images/lib/convert-pages.js');
    
    // 执行转换
    const result = await convertPagesToImages({
      htmlFile,
      outputDir,
      pageWidth: DEFAULT_CONFIG.pageWidth,
      pageHeight: DEFAULT_CONFIG.pageHeight,
      selector: DEFAULT_CONFIG.selector
    });
    
    console.log(`✅ 成功转换 ${result.count} 个页面`);
    
    return {
      images: result.images,
      count: result.count,
      totalSize: result.totalSize || 0
    };
    
  } catch (error) {
    throw new Error(`图片转换失败：${error.message}`);
  }
}

/**
 * 主函数（命令行入口）
 */
async function main() {
  const args = process.argv.slice(2);
  const options = {};
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--topic' && args[i + 1]) {
      options.topic = args[i + 1];
      i++;
    } else if (args[i] === '--template' && args[i + 1]) {
      options.template = args[i + 1];
      i++;
    } else if (args[i] === '--output-dir' && args[i + 1]) {
      options.outputDir = args[i + 1];
      i++;
    } else if (args[i] === '--pages' && args[i + 1]) {
      options.pages = parseInt(args[i + 1]);
      i++;
    }
  }
  
  const result = await generateXiaohongshuArticle(options);
  
  if (!result.success) {
    console.error('生成失败:', result.error);
    process.exit(1);
  }
}

// 命令行执行
if (process.argv[1] && process.argv[1].includes('index.js')) {
  main().catch(console.error);
}
