const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

/**
 * 生成新闻摘要HTML，每次查询创建独立的时间戳目录
 * @param {string} topicName - 查询主题名称（如：'AI技术新闻'、'物理引擎技术'）
 * @param {Array} newsData - 新闻数据数组
 * @param {boolean} withCategories - 是否包含分类导航
 */
function generateNewsHtml(topicName, newsData, withCategories = false) {
    // 生成时间戳目录名
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19).replace('T', '_');
    const dirName = `${timestamp}_${topicName}`;

    // 创建目录结构
    const baseDir = path.join(__dirname, 'output');
    const queryDir = path.join(baseDir, dirName);
    const analysisDir = path.join(queryDir, 'analysis');

    // 确保目录存在
    [baseDir, queryDir, analysisDir].forEach(dir => {
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }
    });

    // 保存原始数据
    const dataPath = path.join(queryDir, 'data.json');
    fs.writeFileSync(dataPath, JSON.stringify(newsData, null, 2), 'utf8');

    // 生成HTML文件
    const htmlPath = path.join(queryDir, 'summary.html');

    let html;
    if (withCategories && newsData.some(item => item.category)) {
        html = generateCategorizedHtml(newsData, topicName, dirName);
    } else {
        html = generateSimpleHtml(newsData, topicName, dirName);
    }

    fs.writeFileSync(htmlPath, html, 'utf8');

    console.log(`✓ 新闻摘要已生成`);
    console.log(`  目录: output/${dirName}/`);
    console.log(`  文件: summary.html, data.json`);

    return { htmlPath, queryDir, dirName };
}

function generateCategorizedHtml(newsData, topicName, dirName) {
    // 按分类组织新闻
    const categories = {};
    newsData.forEach(item => {
        const cat = item.category || '未分类';
        if (!categories[cat]) {
            categories[cat] = [];
        }
        categories[cat].push(item);
    });

    return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${topicName} - 新闻摘要</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "PingFang SC", "Microsoft YaHei", sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .header {
            max-width: 1400px;
            margin: 0 auto 30px;
            text-align: center;
            color: white;
        }
        .header h1 {
            font-size: 36px;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .header p {
            font-size: 16px;
            opacity: 0.9;
        }
        .stats {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
            font-size: 14px;
            flex-wrap: wrap;
        }
        .badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
        }
        .main-container {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            gap: 20px;
        }
        .sidebar {
            width: 250px;
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            position: sticky;
            top: 20px;
            height: fit-content;
        }
        .sidebar h2 {
            font-size: 18px;
            margin-bottom: 15px;
            color: #1a202c;
        }
        .category-nav {
            list-style: none;
        }
        .category-item {
            margin-bottom: 8px;
        }
        .category-link {
            display: block;
            padding: 8px 12px;
            color: #4a5568;
            text-decoration: none;
            border-radius: 6px;
            transition: all 0.2s ease;
            font-size: 14px;
        }
        .category-link:hover {
            background: #f7fafc;
            color: #667eea;
        }
        .category-count {
            float: right;
            background: #e2e8f0;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 12px;
        }
        .content {
            flex: 1;
        }
        .category-section {
            margin-bottom: 40px;
        }
        .category-header {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .category-header h2 {
            font-size: 24px;
            color: #1a202c;
            margin-bottom: 5px;
        }
        .category-header p {
            color: #718096;
            font-size: 14px;
        }
        .news-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 20px;
        }
        .news-card {
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
            position: relative;
            overflow: hidden;
        }
        .news-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }
        .news-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.15);
        }
        .news-title {
            font-size: 17px;
            font-weight: bold;
            color: #1a202c;
            margin-bottom: 12px;
            line-height: 1.4;
        }
        .news-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 12px;
            font-size: 13px;
        }
        .source, .time {
            color: #4a5568;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .authority {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }
        .authority.high { background: #10b981; color: white; }
        .authority.medium { background: #f59e0b; color: white; }
        .authority.low { background: #9ca3af; color: white; }
        .news-summary {
            flex: 1;
            color: #4a5568;
            line-height: 1.7;
            margin-bottom: 16px;
            font-size: 14px;
        }
        .news-actions {
            display: flex;
            gap: 10px;
            margin-top: auto;
        }
        .btn {
            flex: 1;
            padding: 10px 16px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            text-align: center;
            display: inline-block;
        }
        .btn-primary {
            background: #667eea;
            color: white;
        }
        .btn-primary:hover {
            background: #5568d3;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
        }
        .btn-secondary {
            background: #764ba2;
            color: white;
        }
        .btn-secondary:hover {
            background: #6a4293;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(118, 75, 162, 0.3);
        }
        .footer {
            max-width: 1400px;
            margin: 30px auto 0;
            text-align: center;
            color: white;
            font-size: 14px;
            opacity: 0.8;
        }
        .loading {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.85);
            color: white;
            padding: 24px 48px;
            border-radius: 12px;
            display: none;
            z-index: 1000;
            font-size: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        .loading.active { display: block; }
        @media (max-width: 1200px) {
            .main-container { flex-direction: column; }
            .sidebar { width: 100%; position: relative; }
            .news-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>${topicName}</h1>
        <p>新闻摘要 - 最近3-5天内的技术突破与行业动态</p>
        <div class="stats">
            <span class="badge">共 ${newsData.length} 条技术新闻</span>
            <span class="badge">${Object.keys(categories).length} 个分类</span>
            <span class="badge">查询目录: ${dirName}</span>
        </div>
    </div>
    <div class="main-container">
        <aside class="sidebar">
            <h2>目录导航</h2>
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
                    ${categories[category].map((item, index) => generateNewsCard(item, dirName)).join('')}
                </div>
            </section>
            `).join('')}
        </main>
    </div>
    <div class="footer">
        <p>由 Claude Code 生成 | 查询目录: output/${dirName}/ | AI解读: analysis/</p>
    </div>
    <div class="loading" id="loading">正在生成AI解读...</div>
    <script>
        ${getClientScript(dirName)}
    </script>
</body>
</html>`;
}

function generateSimpleHtml(newsData, topicName, dirName) {
    return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${topicName} - 新闻摘要</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .header {
            max-width: 1200px;
            margin: 0 auto 30px;
            text-align: center;
            color: white;
        }
        .header h1 { font-size: 36px; margin-bottom: 10px; }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }
        .news-card {
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .news-title {
            font-size: 18px;
            font-weight: bold;
            color: #1a202c;
            margin-bottom: 12px;
        }
        .news-actions {
            display: flex;
            gap: 10px;
            margin-top: 16px;
        }
        .btn {
            flex: 1;
            padding: 10px 16px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            text-align: center;
            text-decoration: none;
            cursor: pointer;
        }
        .btn-primary { background: #667eea; color: white; }
        .btn-secondary { background: #764ba2; color: white; }
    </style>
</head>
<body>
    <div class="header">
        <h1>${topicName}</h1>
        <p>共 ${newsData.length} 条新闻 | ${dirName}</p>
    </div>
    <div class="container">
        ${newsData.map(item => generateNewsCard(item, dirName)).join('')}
    </div>
    <script>${getClientScript(dirName)}</script>
</body>
</html>`;
}

function generateNewsCard(item, dirName) {
    const authority = item.authority || 'medium';
    const authorityText = {
        'high': '权威来源',
        'medium': '一般来源',
        'low': '待验证'
    }[authority.toLowerCase()] || '未知';

    return `
    <div class="news-card">
        <div class="news-title">${item.title}</div>
        <div class="news-meta">
            <span class="source">📰 ${item.source}</span>
            <span class="time">⏰ ${item.time}</span>
            <span class="authority ${authority.toLowerCase()}">${authorityText}</span>
        </div>
        <div class="news-summary">${item.summary}</div>
        <div class="news-actions">
            <a href="${item.url}" target="_blank" class="btn btn-primary">查看原文</a>
            <button class="btn btn-secondary" onclick="analyzeNews('${dirName}', '${item.title.replace(/'/g, "\\'")}', '${item.url}', \`${item.summary.replace(/`/g, '\\`')}\`, '${item.source}', '${item.time}')">AI解读</button>
        </div>
    </div>`;
}

function getClientScript(dirName) {
    return `
        async function analyzeNews(dirName, title, url, content, source, time) {
            const loading = document.getElementById('loading');
            if (loading) loading.classList.add('active');

            try {
                const response = await fetch('http://localhost:3456/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ dirName, title, url, content, source, time })
                });

                const result = await response.json();
                if (result.success) {
                    console.log('AI解读已生成:', result.filePath);
                } else {
                    alert('生成AI解读失败: ' + result.error);
                }
            } catch (error) {
                alert('无法连接到AI解读服务器。请确保服务器正在运行。\\n错误: ' + error.message);
            } finally {
                if (loading) setTimeout(() => loading.classList.remove('active'), 500);
            }
        }

        // 平滑滚动
        document.querySelectorAll('.category-link').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    `;
}

// 打开浏览器
function openInBrowser(htmlPath) {
    // 优先使用PowerShell（Windows上更可靠）
    if (process.platform === 'win32') {
        exec(`powershell -Command "Start-Process '${htmlPath}'"`, (error) => {
            if (error) {
                console.error('PowerShell打开失败，尝试使用start命令');
                exec(`start "" "${htmlPath}"`, (error2) => {
                    if (error2) {
                        console.error('打开浏览器失败:', error2);
                        console.log('请手动打开:', htmlPath);
                    } else {
                        console.log('浏览器已打开');
                    }
                });
            } else {
                console.log('浏览器已打开（PowerShell）');
            }
        });
    } else {
        const command = process.platform === 'darwin' ? 'open' : 'xdg-open';
        exec(`${command} "${htmlPath}"`, (error) => {
            if (error) {
                console.error('打开浏览器失败:', error);
                console.log('请手动打开:', htmlPath);
            } else {
                console.log('浏览器已打开');
            }
        });
    }
}

module.exports = { generateNewsHtml, openInBrowser };
