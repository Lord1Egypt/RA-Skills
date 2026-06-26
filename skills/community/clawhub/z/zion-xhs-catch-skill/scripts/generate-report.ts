/**
 * 静态 HTML 报告生成器
 * 读取 output/*.json 采集结果，生成一个内联数据的 index.html
 * 用户可直接双击打开，无需服务器或 Zion 配置
 */

import * as fs from 'fs';
import * as path from 'path';

const OUTPUT_DIR = path.resolve(process.cwd(), 'output');

interface XHSNote {
  title: string;
  content: string;
  author_name: string;
  images: string[];
  likes: number;
  collects: number;
  comments_count: number;
  comments?: Array<{ author: string; content: string; likes: number }>;
  comments_extracted?: number;
  keyword: string;
  note_url: string;
  crawl_time: string;
}

function loadData(): XHSNote[] {
  const files = fs.readdirSync(OUTPUT_DIR).filter((f) => f.endsWith('.json') && !f.startsWith('comments_') && !f.startsWith('test_') && !f.startsWith('Zion_') && !f.startsWith('sync_errors_'));
  const all: XHSNote[] = [];
  for (const file of files) {
    try {
      const data = JSON.parse(fs.readFileSync(path.join(OUTPUT_DIR, file), 'utf-8'));
      if (Array.isArray(data)) all.push(...data);
    } catch {
      // ignore invalid json
    }
  }
  // 去重按 note_url
  const seen = new Set<string>();
  return all.filter((item) => {
    if (!item.note_url || seen.has(item.note_url)) return false;
    seen.add(item.note_url);
    return true;
  });
}

function generateHTML(data: XHSNote[]): string {
  const total = data.length;
  const totalLikes = data.reduce((s, i) => s + (i.likes || 0), 0);
  const totalCollects = data.reduce((s, i) => s + (i.collects || 0), 0);
  const totalComments = data.reduce((s, i) => s + (i.comments_count || 0), 0);
  const avgLikes = total > 0 ? Math.round(totalLikes / total) : 0;
  const keywords = [...new Set(data.map((d) => d.keyword).filter(Boolean))];

  // 关键词提取：找高频痛点词
  const painWords = ['坑', '痛点', '缺点', '后悔', '避雷', '吐槽', '难用', '局限', '失败', '困难', '问题', '挑战'];
  const painItems = data.filter((item) =>
    painWords.some((w) => (item.title + item.content).includes(w))
  );

  const jsonData = JSON.stringify(data, null, 2);

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>小红书采集报告</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    :root {
      --primary: #ff2442;
      --bg: #f5f5f5;
      --card-bg: #fff;
      --text: #333;
      --text-light: #666;
      --tag-bg: #fff0f0;
      --comment-bg: #fafafa;
      --border: #eee;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
    }
    header {
      background: linear-gradient(135deg, #ff2442 0%, #ff6b81 100%);
      color: white;
      padding: 2rem;
      text-align: center;
    }
    header h1 { font-size: 1.8rem; margin-bottom: 0.5rem; }
    header p { opacity: 0.9; font-size: 0.95rem; }
    .stats {
      display: flex; justify-content: center; gap: 2rem;
      padding: 1.5rem; background: white;
      border-bottom: 1px solid var(--border);
      flex-wrap: wrap;
    }
    .stat-item { text-align: center; }
    .stat-value { font-size: 2rem; font-weight: bold; color: var(--primary); }
    .stat-label { color: var(--text-light); font-size: 0.9rem; }
    .filters {
      padding: 1rem 2rem; background: white;
      display: flex; gap: 1rem; flex-wrap: wrap; align-items: center;
      position: sticky; top: 0; z-index: 10;
      border-bottom: 1px solid var(--border);
    }
    .filter-btn {
      padding: 0.5rem 1rem; border: 1px solid #ddd; background: white;
      border-radius: 20px; cursor: pointer; transition: all 0.2s; font-size: 0.85rem;
    }
    .filter-btn:hover, .filter-btn.active {
      border-color: var(--primary); background: var(--tag-bg); color: var(--primary);
    }
    .search-box {
      flex: 1; min-width: 200px; padding: 0.5rem 1rem;
      border: 1px solid #ddd; border-radius: 20px; font-size: 0.95rem;
    }
    .export-btn {
      padding: 0.5rem 1rem; border: none; border-radius: 20px;
      cursor: pointer; font-size: 0.85rem; color: white;
    }
    .export-btn.csv { background: #ff2442; }
    .export-btn.md { background: #333; }
    .container {
      max-width: 1200px; margin: 0 auto; padding: 2rem;
      display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 1.5rem;
    }
    .card {
      background: var(--card-bg); border-radius: 12px;
      overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.12); }
    .card-images {
      display: flex; gap: 4px; padding: 4px; background: #fafafa;
    }
    .card-images img {
      flex: 1; height: 120px; object-fit: cover; border-radius: 8px;
    }
    .card-content { padding: 1rem; }
    .card-keyword {
      display: inline-block; padding: 0.25rem 0.75rem;
      background: var(--tag-bg); color: var(--primary);
      border-radius: 12px; font-size: 0.75rem; margin-bottom: 0.5rem;
    }
    .card-title { font-size: 1rem; font-weight: 600; margin-bottom: 0.5rem; }
    .card-text {
      font-size: 0.9rem; color: var(--text-light);
      display: -webkit-box; -webkit-line-clamp: 4;
      -webkit-box-orient: vertical; overflow: hidden;
      margin-bottom: 1rem;
    }
    .card-meta {
      display: flex; justify-content: space-between; align-items: center;
      padding-top: 0.75rem; border-top: 1px solid #f0f0f0;
    }
    .card-author { font-size: 0.85rem; color: var(--text-light); }
    .card-stats { display: flex; gap: 1rem; font-size: 0.85rem; color: var(--text-light); }
    .comments-section {
      margin-top: 0.75rem; padding-top: 0.75rem;
      border-top: 1px dashed #eee;
    }
    .comments-toggle {
      font-size: 0.85rem; color: var(--primary); cursor: pointer;
      background: none; border: none; padding: 0;
    }
    .comments-list {
      margin-top: 0.5rem; display: none;
    }
    .comments-list.show { display: block; }
    .comment-item {
      padding: 0.5rem; background: var(--comment-bg);
      border-radius: 8px; margin-bottom: 0.5rem; font-size: 0.85rem;
    }
    .comment-author { color: var(--text-light); font-size: 0.8rem; }
    .comment-content { color: var(--text); margin-top: 0.25rem; }
    .pain-points-section {
      background: white; margin: 2rem auto; max-width: 1200px;
      padding: 2rem; border-radius: 12px;
    }
    .pain-points-section h2 { margin-bottom: 1rem; color: var(--primary); }
    .pain-point-item {
      padding: 1rem; background: var(--bg); border-radius: 8px;
      margin-bottom: 0.75rem; border-left: 4px solid var(--primary);
    }
    .empty-state { grid-column: 1 / -1; text-align: center; padding: 4rem; color: var(--text-light); }
    footer { text-align: center; padding: 2rem; color: var(--text-light); font-size: 0.85rem; }
  </style>
</head>
<body>
  <header>
    <h1>📕 小红书采集报告</h1>
    <p>${keywords.join(' · ')} · 共 ${total} 条笔记</p>
  </header>

  <div class="stats">
    <div class="stat-item"><div class="stat-value">${total}</div><div class="stat-label">笔记数</div></div>
    <div class="stat-item"><div class="stat-value">${totalLikes}</div><div class="stat-label">总点赞</div></div>
    <div class="stat-item"><div class="stat-value">${totalCollects}</div><div class="stat-label">总收藏</div></div>
    <div class="stat-item"><div class="stat-value">${totalComments}</div><div class="stat-label">总评论</div></div>
    <div class="stat-item"><div class="stat-value">${avgLikes}</div><div class="stat-label">平均点赞</div></div>
  </div>

  <div class="filters">
    <button class="filter-btn active" data-filter="all">全部</button>
    ${keywords.map(k => `<button class="filter-btn" data-filter="${k}">${k}</button>`).join('')}
    <input type="text" class="search-box" placeholder="搜索标题、正文、评论..." id="search">
    <button class="export-btn csv" onclick="exportCSV()">📥 导出CSV</button>
    <button class="export-btn md" onclick="exportMarkdown()">📝 导出MD</button>
  </div>

  <div class="container" id="cards"></div>

  <div class="pain-points-section">
    <h2>📌 核心痛点总结</h2>
    <div id="pain-points"></div>
  </div>

  <footer>
    <p>生成时间: ${new Date().toLocaleString('zh-CN')}</p>
  </footer>

  <script>
    const allData = ${jsonData};

    function renderCards(data) {
      const container = document.getElementById('cards');
      if (data.length === 0) {
        container.innerHTML = '<div class="empty-state">没有找到匹配的内容</div>';
        return;
      }
      container.innerHTML = data.map((item, idx) => \`
        <div class="card" data-keyword="\${item.keyword || ''}">
          \${item.images && item.images.length ? \`
            <div class="card-images">
              \${item.images.slice(0, 3).map(img => \`<img src="\${img}" alt="" loading="lazy">\`).join('')}
            </div>
          \` : ''}
          <div class="card-content">
            <span class="card-keyword">#\${item.keyword || ''}</span>
            <div class="card-title">\${item.title || '无标题'}</div>
            <div class="card-text">\${item.content || ''}</div>
            <div class="card-meta">
              <span class="card-author">\${item.author_name || '匿名'}</span>
              <div class="card-stats">
                <span>👍 \${item.likes || 0}</span>
                <span>⭐ \${item.collects || 0}</span>
                <span>💬 \${item.comments_count || 0}</span>
              </div>
            </div>
            \${item.comments && item.comments.length ? \`
              <div class="comments-section">
                <button class="comments-toggle" onclick="toggleComments(\${idx})">
                  💬 查看 \${item.comments.length} 条评论
                </button>
                <div class="comments-list" id="comments-\${idx}">
                  \${item.comments.map(c => \`
                    <div class="comment-item">
                      <div class="comment-author">\${c.author}</div>
                      <div class="comment-content">\${c.content}</div>
                    </div>
                  \`).join('')}
                </div>
              </div>
            \` : ''}
          </div>
        </div>
      \`).join('');
    }

    function toggleComments(idx) {
      const el = document.getElementById('comments-' + idx);
      el.classList.toggle('show');
    }

    function renderPainPoints() {
      const painWords = ['坑', '痛点', '缺点', '后悔', '避雷', '吐槽', '难用', '局限', '失败', '困难', '问题'];
      const items = allData.filter(item =>
        painWords.some(w => (item.title + item.content).includes(w))
      ).slice(0, 8);
      document.getElementById('pain-points').innerHTML = items.map(item => \`
        <div class="pain-point-item">
          <h4>\${item.title}</h4>
          <p>\${(item.content || '').substring(0, 200)}...</p>
        </div>
      \`).join('') || '<p style="color:#999">暂无匹配痛点关键词的笔记</p>';
    }

    let currentFilter = 'all', searchTerm = '';
    document.querySelectorAll('.filter-btn[data-filter]').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentFilter = btn.dataset.filter;
        filterAndRender();
      });
    });
    document.getElementById('search').addEventListener('input', (e) => {
      searchTerm = e.target.value.toLowerCase();
      filterAndRender();
    });
    function filterAndRender() {
      let filtered = allData;
      if (currentFilter !== 'all') filtered = filtered.filter(i => i.keyword === currentFilter);
      if (searchTerm) {
        filtered = filtered.filter(i =>
          (i.title + i.content + (i.comments || []).map(c => c.content).join('')).toLowerCase().includes(searchTerm)
        );
      }
      renderCards(filtered);
    }

    function exportCSV() {
      const headers = ['标题', '关键词', '点赞', '收藏', '评论数', '作者', '内容', '评论内容'];
      const rows = allData.map(item => [
        (item.title || '').replace(/"/g, '""'),
        item.keyword || '',
        item.likes || 0, item.collects || 0, item.comments_count || 0,
        (item.author_name || '').replace(/"/g, '""'),
        (item.content || '').replace(/"/g, '""').substring(0, 500),
        (item.comments || []).map(c => c.content).join('; ').substring(0, 300)
      ]);
      const csv = [headers, ...rows].map(r => r.map(c => \`"\${c}"\`).join(',')).join('\\n');
      downloadFile(csv, 'xhs_report.csv', 'text/csv');
    }
    function exportMarkdown() {
      let md = '# 小红书采集报告\\n\\n';
      md += \`> 生成时间: \${new Date().toLocaleString('zh-CN')} | 共 \${allData.length} 篇笔记\\n\\n---\\n\\n\`;
      allData.forEach((item, i) => {
        md += \`## \${i + 1}. \${item.title || '无标题'}\\n\\n\`;
        md += \`**关键词**: #\${item.keyword || ''} | **点赞**: \${item.likes || 0} | **收藏**: \${item.collects || 0}\\n\\n\`;
        md += \`**内容**:\\n\\n\${(item.content || '').substring(0, 600)}...\\n\\n\`;
        if (item.comments && item.comments.length) {
          md += '**评论**:\\n';
          item.comments.forEach(c => { md += \`- \${c.author}: \${c.content}\\n\`; });
          md += '\\n';
        }
        md += '---\\n\\n';
      });
      downloadFile(md, 'xhs_report.md', 'text/markdown');
    }
    function downloadFile(content, filename, type) {
      const blob = new Blob([content], { type: type + ';charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = filename; a.click();
      URL.revokeObjectURL(url);
    }

    renderCards(allData);
    renderPainPoints();
  </script>
</body>
</html>`;
}

export function generateReport() {
  const data = loadData();
  if (data.length === 0) {
    console.log('⚠️ 没有找到采集数据，跳过报告生成');
    return;
  }
  const html = generateHTML(data);
  const filepath = path.join(OUTPUT_DIR, 'index.html');
  fs.writeFileSync(filepath, html);
  console.log(`📊 静态报告已生成: ${filepath} (${data.length} 条笔记)`);
  console.log('   直接双击打开即可查看，无需服务器');
}

// CLI 入口
if (require.main === module) {
  generateReport();
}
