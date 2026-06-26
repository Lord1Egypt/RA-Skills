const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');
const { spawn } = require('child_process');

const PORT = 3456;
const BASE_DIR = path.join(__dirname, "..");
// 支持从环境变量或当前工作目录读取工作目录
const WORK_DIR = process.env.NEWS_WORK_DIR || process.cwd();

console.log(`Server BASE_DIR: ${BASE_DIR}`);
console.log(`Server WORK_DIR: ${WORK_DIR}`);
const ANALYSIS_TIMEOUT = 120000; // 120秒超时

const MIME_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.md': 'text/markdown; charset=utf-8'
};

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;

    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    console.log(`${req.method} ${pathname}`);

    if (pathname === '/news-ai.js') {
        const scriptPath = path.join(__dirname, 'news-ai.js');
        fs.readFile(scriptPath, (err, data) => {
            if (err) {
                res.writeHead(404);
                res.end('news-ai.js not found');
                return;
            }
            res.writeHead(200, { 'Content-Type': 'application/javascript; charset=utf-8' });
            res.end(data);
        });
        return;
    }

    if (pathname === '/check-analysis' && req.method === 'GET') {
        const newsId = parsedUrl.query.newsId;
        const timestamp = parsedUrl.query.timestamp;

        if (!newsId || !timestamp) {
            res.writeHead(400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Missing newsId or timestamp' }));
            return;
        }

        const analysisFile = path.join(WORK_DIR, 'news-summary', timestamp, 'analysis', `news_analysis_${newsId}.html`);

        fs.access(analysisFile, fs.constants.F_OK, (err) => {
            console.log('发送成功响应'); res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ exists: !err }));
        });
        return;
    }

    if (pathname === '/analyze' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });

        req.on('end', async () => {
            console.log('收到analyze请求');
            try {
                const data = JSON.parse(body);
                const { newsId, newsUrl, newsSource, newsTime, timestamp, title, summary, customPrompt } = data;

                const analysisDir = path.join(WORK_DIR, 'news-summary', timestamp, 'analysis');
                const analysisFile = path.join(analysisDir, `news_analysis_${newsId}.html`);

                // 构建AI提示词
                const newsTitle = title || '未知标题';
                const newsSummary = summary || '暂无摘要';

                let aiPrompt = `你是一个HTML生成器。你的任务是生成一个完整的HTML页面。

重要：你的输出必须是纯HTML代码，从<!DOCTYPE html>开始，到</html>结束。不要包含任何解释性文字、说明或其他内容。

## 新闻信息
- **标题**: ${newsTitle}
- **来源**: ${newsSource || '未知来源'}
- **时间**: ${newsTime || '未知时间'}
- **链接**: ${newsUrl || '#'}

## 新闻摘要
${newsSummary}

## 分析要求
请对这条新闻进行深度分析，包括：
1. **背景分析**：事件的历史背景和相关上下文
2. **关键要点**：提炼出最重要的3-5个要点
3. **影响评估**：分析对行业、技术、用户等方面的影响
4. **相关延伸**：相关话题和深入思考的方向`;

                if (customPrompt) {
                    aiPrompt += `\n\n## 用户自定义分析角度\n${customPrompt}`;
                }

                aiPrompt += `

## HTML页面要求
1. 使用现代化的CSS样式，美观易读
2. 响应式设计，适配移动端和桌面端
3. 使用渐变背景和卡片布局
4. 包含新闻信息、分析内容、底部版权等完整结构
5. 颜色主题使用 #667eea 和 #764ba2 渐变
6. 字体使用系统默认字体栈

## 输出格式
你必须只输出HTML代码，从<!DOCTYPE html>开始。
不要输出任何其他文字，包括：
- 不要说"我为您生成了..."
- 不要说"页面包含..."
- 不要说"如果您需要..."
- 只输出纯HTML代码，没有任何解释

立即开始输出HTML代码：`;

                // 创建分析目录
                if (!fs.existsSync(analysisDir)) {
                    fs.mkdirSync(analysisDir, { recursive: true });
                }

                // 调用Claude CLI生成AI解读
                console.log('调用Claude CLI生成分析...');

                const claudeProcess = spawn('claude', [
                    '--print',                      // 非交互式模式
                    '--model', 'kimi-k2-thinking-turbo'  // 使用kimi模型
                ], {
                    stdio: ['pipe', 'pipe', 'pipe'],
                    shell: true
                });

                let output = '';
                let errorOutput = '';
                let timeoutId;
                let isTimeout = false;

                // 设置超时
                timeoutId = setTimeout(() => {
                    isTimeout = true;
                    claudeProcess.kill();
                    console.log('Claude CLI调用超时');
                }, ANALYSIS_TIMEOUT);

                claudeProcess.stdout.on('data', (data) => {
                    output += data.toString();
                });

                claudeProcess.stderr.on('data', (data) => {
                    errorOutput += data.toString();
                    console.error('Claude CLI错误输出:', data.toString());
                });

                claudeProcess.on('close', (code) => {
                    clearTimeout(timeoutId);

                    if (isTimeout) {
                        res.writeHead(408, { 'Content-Type': 'application/json' });
                        res.end(JSON.stringify({ error: 'AI分析请求超时，请稍后重试' }));
                        return;
                    }

                    if (code !== 0) {
                        console.error('Claude CLI执行失败，退出码:', code);
                        res.writeHead(500, { 'Content-Type': 'application/json' });
                        res.end(JSON.stringify({ error: `AI分析生成失败: ${errorOutput}` }));
                        return;
                    }

                    // 提取 HTML 内容
                    let htmlContent = output.trim();

                    // 尝试提取 HTML 代码（如果 Claude 输出了额外的文字）
                    const htmlMatch = htmlContent.match(/<!DOCTYPE html>[\s\S]*<\/html>/i);
                    if (htmlMatch) {
                        htmlContent = htmlMatch[0];
                        console.log('成功提取HTML代码');
                    } else if (!htmlContent.startsWith('<!DOCTYPE')) {
                        // 如果没有找到完整的 HTML，但内容不是以 <!DOCTYPE 开头，记录警告
                        console.warn('警告：输出可能不是有效的HTML');
                    }

                    fs.writeFile(analysisFile, htmlContent, 'utf8', (err) => {
                        if (err) {
                            console.error('写入分析文件失败:', err);
                            res.writeHead(500, { 'Content-Type': 'application/json' });
                            res.end(JSON.stringify({ error: '保存分析文件失败' }));
                            return;
                        }

                        console.log('分析生成成功');
                        res.writeHead(200, { 'Content-Type': 'application/json' });
                        res.end(JSON.stringify({ success: true, message: '分析生成成功' }));
                    });
                });

                // 发送提示词到Claude CLI
                claudeProcess.stdin.write(aiPrompt);
                claudeProcess.stdin.end();

            } catch (err) {
                console.error('处理请求失败:', err);
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: 'Invalid JSON' }));
            }
        });
        return;
    }

    if (pathname === '/delete-analysis' && req.method === 'DELETE') {
        const newsId = parsedUrl.query.newsId;
        const timestamp = parsedUrl.query.timestamp;

        if (!newsId || !timestamp) {
            res.writeHead(400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Missing newsId or timestamp' }));
            return;
        }

        const analysisFile = path.join(WORK_DIR, 'news-summary', timestamp, 'analysis', `news_analysis_${newsId}.html`);

        fs.unlink(analysisFile, (err) => {
            if (err) {
                console.error('删除分析文件失败:', err);
                res.writeHead(404, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: '分析文件不存在或删除失败' }));
                return;
            }

            console.log('分析文件已删除:', analysisFile);
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ success: true, message: '分析文件已删除' }));
        });
        return;
    }

    if (pathname === '/view-analysis' && req.method === 'GET') {
        const newsId = parsedUrl.query.newsId;
        const timestamp = parsedUrl.query.timestamp;

        if (!newsId || !timestamp) {
            res.writeHead(400);
            res.end('Missing newsId or timestamp');
            return;
        }

        const analysisFile = path.join(WORK_DIR, 'news-summary', timestamp, 'analysis', `news_analysis_${newsId}.html`);

        fs.readFile(analysisFile, 'utf8', (err, data) => {
            if (err) {
                res.writeHead(404);
                res.end('Analysis not found');
                return;
            }

            // 直接返回 HTML 内容
            res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
            res.end(data);
        });
        return;
    }

    // 支持两种路径：
    // 1. /output/ - 从 skill 目录的 output 子目录（向后兼容）
    // 2. /news-summary/ - 从当前工作目录的 news-summary 子目录
    if (pathname.startsWith('/output/')) {
        const filePath = path.join(BASE_DIR, pathname);

        fs.readFile(filePath, (err, data) => {
            if (err) {
                res.writeHead(404);
                res.end('File not found');
                return;
            }

            const ext = path.extname(filePath);
            const contentType = MIME_TYPES[ext] || 'application/octet-stream';

            res.writeHead(200, { 'Content-Type': contentType });
            res.end(data);
        });
        return;
    }

    if (pathname.startsWith('/news-summary/')) {
        const filePath = path.join(WORK_DIR, pathname);

        fs.readFile(filePath, (err, data) => {
            if (err) {
                res.writeHead(404);
                res.end('File not found');
                return;
            }

            const ext = path.extname(filePath);
            const contentType = MIME_TYPES[ext] || 'application/octet-stream';

            res.writeHead(200, { 'Content-Type': contentType });
            res.end(data);
        });
        return;
    }
    res.writeHead(404);
    res.end('Not found');
});

server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
});
