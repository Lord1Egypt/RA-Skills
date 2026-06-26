const fs = require('fs');
const path = require('path');

/**
 * 生成新闻摘要HTML的通用函数
 * @param {Object} options - 配置选项
 * @param {string} options.topic - 主题标识（如: 'ai-news', 'physics-engine'）
 * @param {string} options.topicName - 主题显示名称（如: 'AI行业技术', '物理引擎技术'）
 * @param {string} options.dataFile - 数据文件名（在output/data/目录下）
 * @param {boolean} options.withCategories - 是否包含分类导航
 */
function generateNewsHtml(options) {
    const { topic, topicName, dataFile, withCategories = false } = options;

    // 创建目录结构
    const baseDir = path.join(__dirname, 'output');
    const topicDir = path.join(baseDir, topic);
    const dataDir = path.join(baseDir, 'data');

    // 确保目录存在
    [baseDir, topicDir, dataDir, path.join(baseDir, 'analysis')].forEach(dir => {
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }
    });

    // 读取新闻数据
    const dataPath = path.join(dataDir, dataFile);
    if (!fs.existsSync(dataPath)) {
        console.error(`数据文件不存在: ${dataPath}`);
        process.exit(1);
    }

    const newsData = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

    // 生成HTML文件名
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
    const outputPath = path.join(topicDir, `${topic}_${timestamp}.html`);

    let html;

    if (withCategories) {
        html = generateCategorizedHtml(newsData, topicName, topic);
    } else {
        html = generateSimpleHtml(newsData, topicName, topic);
    }

    fs.writeFileSync(outputPath, html, 'utf8');
    console.log(`✓ HTML文件已生成: ${outputPath}`);
    console.log(`✓ 目录: output/${topic}/`);

    return outputPath;
}

function generateSimpleHtml(newsData, topicName, topic) {
    // ... (简单HTML模板，不带分类)
    return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${topicName}新闻摘要</title>
    <style>
        /* ... CSS样式 ... */
    </style>
</head>
<body>
    <div class="header">
        <h1>${topicName}新闻摘要</h1>
        <p>最近3-5天内的技术突破与行业动态</p>
    </div>
    <div class="container">
        ${newsData.map((item, index) => generateNewsCard(item, index, topic)).join('')}
    </div>
</body>
</html>`;
}

function generateCategorizedHtml(newsData, topicName, topic) {
    // 按分类组织新闻
    const categories = {};
    newsData.forEach(item => {
        if (!categories[item.category]) {
            categories[item.category] = [];
        }
        categories[item.category].push(item);
    });

    return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${topicName}新闻摘要</title>
    <style>
        /* ... 完整CSS样式 ... */
    </style>
</head>
<body>
    <div class="header">
        <h1>${topicName}新闻摘要</h1>
        <p>最近3-5天内的技术突破与行业动态</p>
        <div class="stats">
            <span class="badge">共 ${newsData.length} 条技术新闻</span>
            <span class="badge">${Object.keys(categories).length} 个分类</span>
        </div>
    </div>
    <div class="main-container">
        <aside class="sidebar">
            <h2>📑 目录导航</h2>
            <ul class="category-nav">
                ${Object.keys(categories).map(category => `
                <li class="category-item">
                    <a href="#${encodeURIComponent(category)}" class="category-link">
                        ${category}
                        <span class="category-count">${categories[category].length}</span>
                    </a>
                </li>
                `).join('')}
            </ul>
        </aside>
        <main class="content">
            ${Object.keys(categories).map(category => `
            <section id="${encodeURIComponent(category)}" class="category-section">
                <div class="category-header">
                    <h2>${category}</h2>
                    <p>${categories[category].length} 条相关新闻</p>
                </div>
                <div class="news-grid">
                    ${categories[category].map((item, index) => generateNewsCard(item, index, topic)).join('')}
                </div>
            </section>
            `).join('')}
        </main>
    </div>
    <div class="footer">
        <p>🤖 由 Claude Code 生成 | 目录: output/${topic}/ | AI解读: output/analysis/</p>
    </div>
</body>
</html>`;
}

function generateNewsCard(item, index, topic) {
    return `
    <div class="news-card">
        <div class="news-title">${item.title}</div>
        <div class="news-meta">
            <span class="source">📰 ${item.source}</span>
            <span class="time">⏰ ${item.time}</span>
            <span class="authority ${item.authority.toLowerCase()}">${getAuthorityText(item.authority)}</span>
        </div>
        <div class="news-summary">${item.summary}</div>
        <div class="news-actions">
            <a href="${item.url}" target="_blank" class="btn btn-primary">查看原文</a>
            <button class="btn btn-secondary" onclick="analyzeNews('${topic}', '${item.title.replace(/'/g, "\\'")}', '${item.url}', \`${item.summary.replace(/`/g, '\\`')}\`, '${item.source}', '${item.time}')">AI解读</button>
        </div>
    </div>`;
}

function getAuthorityText(authority) {
    const authorityMap = {
        'high': '权威来源',
        'medium': '一般来源',
        'low': '待验证'
    };
    return authorityMap[authority.toLowerCase()] || '未知';
}

module.exports = { generateNewsHtml };
