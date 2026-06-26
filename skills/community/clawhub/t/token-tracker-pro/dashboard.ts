import express from 'express';
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;
const DATA_FILE = join(__dirname, 'data/token-history.json');

// 中间件
app.use(express.json());

// API 路由
app.get('/api/stats/today', (req, res) => {
  try {
    if (!existsSync(DATA_FILE)) {
      return res.json({ total: 0, count: 0, average: 0, max: 0, min: 0 });
    }
    const data = JSON.parse(readFileSync(DATA_FILE, 'utf8'));
    const today = new Date().toISOString().split('T')[0];
    const todayTokens = data.tokens.filter((t: any) => t.date === today);

    const stats = {
      total: todayTokens.reduce((sum: number, t: any) => sum + t.tokens, 0),
      count: todayTokens.length,
      average: todayTokens.length > 0
        ? todayTokens.reduce((sum: number, t: any) => sum + t.tokens, 0) / todayTokens.length
        : 0,
      max: todayTokens.length > 0 ? Math.max(...todayTokens.map((t: any) => t.tokens)) : 0,
      min: todayTokens.length > 0 ? Math.min(...todayTokens.map((t: any) => t.tokens)) : 0
    };

    res.json(stats);
  } catch (error: any) {
    console.error('Error:', error);
    res.json({ total: 0, count: 0, average: 0, max: 0, min: 0 });
  }
});

app.get('/api/stats/week', (req, res) => {
  try {
    if (!existsSync(DATA_FILE)) {
      return res.json({ total: 0, count: 0, average: 0 });
    }
    const data = JSON.parse(readFileSync(DATA_FILE, 'utf8'));
    const oneWeekAgo = new Date();
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

    const weekTokens = data.tokens.filter((t: any) => {
      const tokenDate = new Date(t.date);
      return tokenDate >= oneWeekAgo;
    });

    const stats = {
      total: weekTokens.reduce((sum: number, t: any) => sum + t.tokens, 0),
      count: weekTokens.length,
      average: weekTokens.length > 0
        ? weekTokens.reduce((sum: number, t: any) => sum + t.tokens, 0) / weekTokens.length
        : 0
    };

    res.json(stats);
  } catch (error: any) {
    console.error('Error:', error);
    res.json({ total: 0, count: 0, average: 0 });
  }
});

app.get('/api/history', (req, res) => {
  try {
    if (!existsSync(DATA_FILE)) {
      return res.json({ tokens: [], total: 0, daily: {}, weekly: {} });
    }
    const data = JSON.parse(readFileSync(DATA_FILE, 'utf8'));
    const limit = parseInt(req.query.limit as string) || 50;

    res.json({
      tokens: data.tokens.slice(-limit),
      total: data.total,
      daily: data.daily,
      weekly: data.weekly
    });
  } catch (error: any) {
    console.error('Error:', error);
    res.json({ tokens: [], total: 0, daily: {}, weekly: {} });
  }
});

app.get('/api/suggestions', (req, res) => {
  const suggestions = [
    '使用 memory_search 而不是重复搜索',
    '使用 memory_get 获取特定部分',
    '避免重复读取 MEMORY.md',
    '合并多个工具调用',
    '减少日志输出',
    '使用更精确的搜索词',
    '定期清理不必要的历史',
    '使用更高效的模型'
  ];

  res.json(suggestions);
});

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// 根路径
app.get('/', (req, res) => {
  res.send(`
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Token Tracker Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      padding: 20px;
    }
    .container { max-width: 1200px; margin: 0 auto; }
    .header { text-align: center; color: white; margin-bottom: 40px; }
    .header h1 { font-size: 2.5em; margin-bottom: 10px; }
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 20px;
      margin-bottom: 40px;
    }
    .stat-card {
      background: white;
      border-radius: 12px;
      padding: 24px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stat-card .label { color: #6b7280; font-size: 0.875em; margin-bottom: 8px; }
    .stat-card .value { font-size: 2em; font-weight: bold; color: #111827; }
    .charts-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
      gap: 20px;
      margin-bottom: 40px;
    }
    .chart-container {
      background: white;
      border-radius: 12px;
      padding: 24px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .chart-container h2 { font-size: 1.25em; margin-bottom: 20px; }
    .chart-container canvas { max-height: 300px; }
    @media (max-width: 768px) {
      .charts-grid { grid-template-columns: 1fr; }
      .header h1 { font-size: 1.8em; }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>📊 Token Tracker Dashboard</h1>
      <p>实时监控 Token 消耗，优化使用效率</p>
    </div>

    <div class="stats-grid" id="stats"></div>

    <div class="charts-grid">
      <div class="chart-container">
        <h2>📈 7天趋势</h2>
        <canvas id="trendChart"></canvas>
      </div>
      <div class="chart-container">
        <h2>📊 模型分布</h2>
        <canvas id="modelChart"></canvas>
      </div>
    </div>

    <div class="chart-container">
      <h2>💡 节省建议</h2>
      <ul id="suggestions"></ul>
    </div>
  </div>

  <script>
    async function fetchStats() {
      try {
        const [todayRes, historyRes, suggestionsRes] = await Promise.all([
          fetch('/api/stats/today'),
          fetch('/api/history?limit=10'),
          fetch('/api/suggestions')
        ]);

        const today = await todayRes.json();
        const history = await historyRes.json();
        const suggestions = await suggestionsRes.json();

        document.getElementById('stats').innerHTML = \`
          <div class="stat-card">
            <div class="label">今日消耗</div>
            <div class="value">\${today.total.toLocaleString()}</div>
            <div class="trend">平均: \${today.average.toFixed(2)} tokens/次</div>
          </div>
          <div class="stat-card">
            <div class="label">记录次数</div>
            <div class="value">\${today.count}</div>
          </div>
          <div class="stat-card">
            <div class="label">本周总计</div>
            <div class="value">\${history.week?.total || 0}.toLocaleString()}</div>
          </div>
        \`;

        document.getElementById('suggestions').innerHTML = suggestions.map(s => \`<li>\${s}</li>\`).join('');

        drawTrendChart(history);
        drawModelChart(history);

      } catch (error) {
        console.error('Error:', error);
      }
    }

    function drawTrendChart(history) {
      const ctx = document.getElementById('trendChart').getContext('2d');
      const days = 7;
      const labels = [];
      const data = [];

      for (let i = days - 1; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        const dateStr = date.toISOString().split('T')[0];
        labels.push(date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' }));
        const dayTokens = history.tokens.filter((t: any) => t.date === dateStr);
        data.push(dayTokens.reduce((sum: number, t: any) => sum + t.tokens, 0));
      }

      new Chart(ctx, {
        type: 'line',
        data: {
          labels,
          datasets: [{
            label: 'Token 消耗',
            data,
            borderColor: '#667eea',
            backgroundColor: 'rgba(102, 126, 234, 0.1)',
            fill: true,
            tension: 0.4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            y: {
              beginAtZero: true,
              ticks: { callback: v => v.toLocaleString() }
            }
          }
        }
      });
    }

    function drawModelChart(history) {
      const ctx = document.getElementById('modelChart').getContext('2d');
      const modelStats: { [key: string]: number } = {};

      history.tokens.forEach((token: any) => {
        modelStats[token.model] = (modelStats[token.model] || 0) + token.tokens;
      });

      const labels = Object.keys(modelStats);
      const data = Object.values(modelStats);

      new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels,
          datasets: [{
            data,
            backgroundColor: ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { position: 'bottom' } }
        }
      });
    }

    fetchStats();
    setInterval(fetchStats, 30000);
  </script>
</body>
</html>
  `);
});

// 启动服务器
app.listen(PORT, () => {
  console.log('\n🚀 Token Tracker Web Dashboard');
  console.log(`   服务地址: http://localhost:${PORT}`);
  console.log(`   数据文件: ${DATA_FILE}`);
  console.log(`   按 Ctrl+C 停止服务\n`);
});
