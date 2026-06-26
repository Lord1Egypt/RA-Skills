// Smarter Content - Intelligent multi-platform content generator
// Main content generation logic

const { execSync } = require('child_process');

// Platform-specific style guidelines
const platformGuidelines = {
    'wechat': {
        name: '微信公众号',
        characteristics: [
            '短段落，适合手机阅读',
            '多用小标题，层次清晰',
            '开头必须吸引人，3秒抓住注意力',
            '结尾引导互动（点赞、留言、转发）',
            '段落之间空行，呼吸感强',
            '口语化，像和朋友聊天'
        ],
        seo: {
            needTitle: true,
            needDescription: true,
            needKeywords: true
        }
    },
    'zhihu': {
        name: '知乎',
        characteristics: [
            '长文分析，结构严谨',
            '开头直接点题，说明回答背景',
            '论点+论据层次分明',
            '可以放数据和引用',
            '结尾可以总结升华',
            '专业感强，逻辑清晰'
        ],
        seo: {
            needTitle: true,
            needDescription: true,
            needKeywords: true
        }
    },
    'xiaohongshu': {
        name: '小红书',
        characteristics: [
            '短句为主，多用换行',
            'emoji 点缀，活泼轻松',
            '开头一句话 hook 抓住眼球',
            '常用清单/分点结构',
            '结尾加相关标签（5-10个）',
            '种草风格，亲切口语化'
        ],
        seo: {
            needTitle: true,
            needTags: true
        }
    },
    'blog': {
        name: '个人博客',
        characteristics: [
            '技术内容结构完整',
            '代码块正确格式化',
            '开头介绍背景，结尾总结',
            '可以深入技术细节',
            'SEO 友好，标题包含关键词'
        ],
        seo: {
            needTitle: true,
            needDescription: true,
            needKeywords: true,
            needTOC: true
        }
    },
    'clawhub': {
        name: 'ClawHub 技能',
        characteristics: [
            'SKILL.md 格式规范',
            'frontmatter 正确填写 name/description',
            '使用说明清晰简洁',
            '代码示例正确可运行',
            '符合 OpenClaw 技能规范'
        ],
        seo: {
            needDescription: true
        }
    }
};

function getPlatformGuidelines(platform) {
    const key = Object.keys(platformGuidelines).find(k => 
        platform.toLowerCase().includes(k) || platformGuidelines[k].name.includes(platform)
    );
    return key ? platformGuidelines[key] : platformGuidelines.blog;
}

function extractKeywords(topic, searchResults) {
    // Extract common keywords from search results
    const words = topic.toLowerCase().split(/\s+/);
    const keywordSet = new Set(words);
    
    searchResults.forEach(result => {
        const content = `${result.title} ${result.snippet}`.toLowerCase();
        content.split(/\s+/).forEach(word => {
            if (word.length > 3) keywordSet.add(word);
        });
    });
    
    return Array.from(keySet).slice(0, 10);
}

function factCheckContent(content) {
    // Run ai-fact-checker on the generated content
    try {
        const cmd = `node ai-fact-checker/scripts/fact-check.js "${content.replace(/"/g, '\\"')}"`;
        const result = execSync(cmd, { encoding: 'utf8', maxBuffer: 1024 * 1024 });
        return JSON.parse(result);
    } catch (e) {
        console.warn('Fact check failed:', e.message);
        return null;
    }
}

function applyPlatformFormat(content, platform, keywords) {
    const guide = getPlatformGuidelines(platform);
    let output = content;
    
    // Add tags for Xiaohongshu
    if (platform === 'xiaohongshu' && keywords) {
        const tags = keywords.slice(0, 8).map(k => `#${k.replace(/\s+/g, '')}`).join(' ');
        output += '\n\n' + tags;
    }
    
    return output;
}

function generateOutline(topic, platform, searchResults) {
    const guide = getPlatformGuidelines(platform);
    const keywords = extractKeywords(topic, searchResults);
    
    // Generate outline based on platform
    let outline = `# ${topic}\n\n`;
    
    if (guide.seo.needDescription) {
        outline += `**简介**: [一句话介绍文章内容]\n\n`;
    }
    
    outline += `## 目录\n`;
    outline += `1. 背景介绍\n`;
    outline += `2. 核心观点\n`;
    outline += `3. 详细分析\n`;
    outline += `4. 总结建议\n\n`;
    
    return { outline, keywords };
}

module.exports = {
    getPlatformGuidelines,
    getPlatformGuidelines,
    extractKeywords,
    factCheckContent,
    applyPlatformFormat,
    generateOutline
};
