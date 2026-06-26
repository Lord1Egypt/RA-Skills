# Web 界面交互优化技能

为 AI Agent 创建流畅、稳定的 Web 监控面板界面。

## 功能特性

- 📊 数据监控面板模板
- 🔄 智能刷新（数据变化才更新）
- 📜 滚动位置保持
- 🎨 弹窗交互优化
- 🚀 服务自动重启
- 📱 响应式设计

## 适用场景

- 任务执行监控
- 数据可视化展示
- 实时状态面板
- 后台管理界面

## 快速开始

### 1. 创建基础 HTML 文件

```bash
cd /workspace/tools
cat > dashboard.html << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>监控面板</title>
    <style>
        /* 基础样式 */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        
        /* 卡片样式 */
        .card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        /* 统计卡片 */
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: box-shadow 0.3s;
        }
        .stat-card:hover { box-shadow: 0 8px 20px rgba(0,0,0,0.15); }
        .stat-value { font-size: 36px; font-weight: bold; color: #667eea; }
        .stat-label { color: #666; margin-top: 5px; }
        
        /* 任务列表 */
        .task-card {
            border: 2px solid #e5e7eb;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            background: #fafafa;
            transition: border-color 0.3s, box-shadow 0.3s;
        }
        .task-card:hover {
            border-color: #667eea;
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
        }
        .task-card.updated {
            animation: highlightUpdate 1s;
        }
        @keyframes highlightUpdate {
            0% { background: #fef3c7; }
            100% { background: #fafafa; }
        }
        
        /* 弹窗样式 */
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.8);
            z-index: 1000;
            overflow-y: auto;
        }
        .modal.show {
            display: flex;
            align-items: flex-start;
            justify-content: center;
            padding: 40px 20px;
        }
        .modal-content {
            background: white;
            border-radius: 20px;
            max-width: 1000px;
            width: 100%;
            position: relative;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        }
        .modal-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px 30px;
            border-radius: 20px 20px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .modal-close {
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            width: 40px; height: 40px;
            border-radius: 50%;
            font-size: 24px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .modal-close:hover {
            background: rgba(255,255,255,0.3);
            transform: rotate(90deg);
        }
        .modal-body {
            padding: 30px;
            overflow-y: auto;
            max-height: 70vh;
        }
        
        /* 防止弹窗打开时页面滚动 */
        body.modal-open {
            position: fixed;
            width: 100%;
            overflow: hidden;
        }
        
        /* 按钮样式 */
        .btn {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            transition: box-shadow 0.3s;
        }
        .btn:hover { box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4); }
        .btn:disabled { opacity: 0.6; cursor: not-allowed; }
    </style>
</head>
<body>
    <div class="container">
        <header class="card">
            <h1>📊 监控面板</h1>
            <div class="auto-refresh">
                <span>自动刷新 (60 秒)</span>
                <button class="btn" id="refreshBtn" onclick="loadData()">🔄 刷新</button>
            </div>
        </header>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value" id="stat1">-</div>
                <div class="stat-label">统计 1</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="stat2">-</div>
                <div class="stat-label">统计 2</div>
            </div>
        </div>
        
        <div class="card">
            <h2>📋 列表</h2>
            <div id="list"></div>
        </div>
    </div>
    
    <!-- 弹窗 -->
    <div id="modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modalTitle">标题</h2>
                <button class="modal-close" onclick="closeModal()">×</button>
            </div>
            <div class="modal-body" id="modalBody">内容</div>
        </div>
    </div>
    
    <script>
        let autoRefresh = true;
        let refreshInterval;
        let lastDataHash = '';
        let isModalOpen = false;
        
        // 智能刷新（仅数据变化时更新）
        function generateDataHash(data) {
            return JSON.stringify(data);
        }
        
        async function loadData() {
            const btn = document.getElementById('refreshBtn');
            btn.disabled = true;
            btn.textContent = '刷新中...';
            
            // 保存滚动位置
            const scrollY = window.scrollY;
            
            try {
                const response = await fetch('/api/data');
                const data = await response.json();
                
                const newDataHash = generateDataHash(data);
                const hasChanges = newDataHash !== lastDataHash;
                
                if (hasChanges || !lastDataHash) {
                    // 渲染数据
                    render(data);
                    lastDataHash = newDataHash;
                    
                    // 标记更新
                    document.querySelectorAll('.card').forEach(card => {
                        card.classList.add('updated');
                        setTimeout(() => card.classList.remove('updated'), 1000);
                    });
                    
                    // 恢复滚动位置
                    window.scrollTo(0, scrollY);
                }
            } catch (error) {
                console.error('加载失败:', error);
            } finally {
                btn.disabled = false;
                btn.textContent = '🔄 刷新';
            }
        }
        
        function render(data) {
            // 自定义渲染逻辑
            document.getElementById('list').innerHTML = '<p>数据已加载</p>';
        }
        
        // 弹窗管理
        function openModal(title, content) {
            if (isModalOpen) return;
            isModalOpen = true;
            
            // 保存滚动位置
            const scrollY = window.scrollY;
            document.body.style.top = -scrollY + 'px';
            document.body.classList.add('modal-open');
            
            document.getElementById('modalTitle').textContent = title;
            document.getElementById('modalBody').innerHTML = content;
            document.getElementById('modal').classList.add('show');
        }
        
        function closeModal() {
            document.getElementById('modal').classList.remove('show');
            
            // 恢复滚动位置
            const scrollY = parseInt(document.body.style.top || '0');
            document.body.classList.remove('modal-open');
            document.body.style.top = '';
            window.scrollTo(0, Math.abs(scrollY));
            
            isModalOpen = false;
        }
        
        // ESC 键关闭弹窗
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && isModalOpen) {
                closeModal();
            }
        });
        
        // 点击弹窗外部关闭
        document.getElementById('modal').addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal();
            }
        });
        
        // 自动刷新
        function startAutoRefresh() {
            refreshInterval = setInterval(loadData, 60000);
        }
        
        function stopAutoRefresh() {
            clearInterval(refreshInterval);
        }
        
        // 初始化
        loadData();
        startAutoRefresh();
    </script>
</body>
</html>
EOF
```

### 2. 创建 Node.js 服务器

```bash
cat > server.js << 'EOF'
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 18790;

// 读取 HTML 文件
const htmlPath = path.join(__dirname, 'dashboard.html');
const html = fs.readFileSync(htmlPath, 'utf-8');

// 模拟数据
function getData() {
    return {
        timestamp: Date.now(),
        items: [
            { id: 1, name: '任务 1', status: 'success' },
            { id: 2, name: '任务 2', status: 'pending' },
        ]
    };
}

const server = http.createServer((req, res) => {
    // CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    
    if (req.url === '/' || req.url === '/index.html') {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(html);
        return;
    }
    
    if (req.url === '/api/data') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(getData()));
        return;
    }
    
    res.writeHead(404);
    res.end('Not Found');
});

server.listen(PORT, () => {
    console.log(`📊 监控面板已启动`);
    console.log(`   访问地址：http://localhost:${PORT}`);
    console.log(`   API: http://localhost:${PORT}/api/data`);
});
EOF
```

### 3. 创建带自动重启的启动脚本

```bash
cat > run-monitor.sh << 'EOF'
#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="/tmp/openclaw-monitor"
PID_FILE="$LOG_DIR/monitor.pid"
LOG_FILE="$LOG_DIR/monitor.log"

mkdir -p "$LOG_DIR"

# 检查是否已在运行
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ 监控面板已在运行 (PID: $PID)"
        exit 0
    fi
fi

# 启动服务（带自动重启）
echo "🚀 启动监控面板..."
cd "$SCRIPT_DIR"

(
    while true; do
        node server.js >> "$LOG_FILE" 2>&1
        echo "⚠️  服务意外停止，5 秒后重启..." >> "$LOG_FILE"
        sleep 5
    done
) > /dev/null 2>&1 &

echo $! > "$PID_FILE"

sleep 3

if ps -p $(cat "$PID_FILE") > /dev/null 2>&1; then
    echo "✅ 监控面板已启动"
    echo "   访问地址：http://localhost:18790"
    echo "   日志文件：$LOG_FILE"
    echo "   进程 PID: $(cat $PID_FILE)"
else
    echo "❌ 启动失败"
    rm -f "$PID_FILE"
fi
EOF

chmod +x run-monitor.sh
```

### 4. 运行

```bash
./run-monitor.sh
```

访问：http://localhost:18790

## 关键优化点

### 1. 智能刷新

```javascript
// 只在数据变化时重新渲染
const hasChanges = newDataHash !== lastDataHash;
if (hasChanges) {
    render(data);
    // 恢复滚动位置
    window.scrollTo(0, scrollY);
}
```

### 2. 滚动位置保持

```javascript
// 刷新前保存
const scrollY = window.scrollY;

// 渲染后恢复
window.scrollTo(0, scrollY);
```

### 3. 弹窗交互

```javascript
// 打开时保存位置
const scrollY = window.scrollY;
document.body.style.top = -scrollY + 'px';
document.body.classList.add('modal-open');

// 关闭时恢复
const scrollY = parseInt(document.body.style.top || '0');
document.body.classList.remove('modal-open');
window.scrollTo(0, Math.abs(scrollY));
```

### 4. 服务自动重启

```bash
while true; do
    node server.js
    sleep 5  # 5 秒后自动重启
done
```

## 自定义

### 修改数据源

编辑 `server.js` 中的 `getData()` 函数：

```javascript
function getData() {
    // 从数据库、API 或文件读取数据
    const data = fs.readFileSync('/path/to/data.json');
    return JSON.parse(data);
}
```

### 修改样式

编辑 `dashboard.html` 中的 `<style>` 部分。

### 修改刷新间隔

```javascript
// 改为 30 秒
refreshInterval = setInterval(loadData, 30000);
```

## 最佳实践

1. **数据哈希对比**：避免不必要的重新渲染
2. **滚动位置保存**：提升用户体验
3. **弹窗位置管理**：防止页面跳动
4. **自动重启**：确保服务持续在线
5. **日志记录**：便于问题排查

## 故障排查

### 服务无法启动

```bash
# 查看日志
tail -f /tmp/openclaw-monitor/monitor.log

# 检查端口占用
lsof -ti:18790 | xargs kill -9

# 重新启动
./run-monitor.sh
```

### 页面空白

1. 检查浏览器控制台错误
2. 确认服务器正在运行
3. 检查 HTML 文件路径

### 自动刷新导致跳动

确保 `loadData()` 函数中保存和恢复了滚动位置。

## 扩展功能

### 添加搜索过滤

```javascript
function filterTasks() {
    const searchText = document.getElementById('searchInput').value.toLowerCase();
    filteredTasks = allTasks.filter(task => 
        task.name.toLowerCase().includes(searchText)
    );
    renderTasks(filteredTasks);
}
```

### 添加状态筛选

```html
<select onchange="filterByStatus(this.value)">
    <option value="all">全部状态</option>
    <option value="success">✅ 成功</option>
    <option value="error">❌ 失败</option>
</select>
```

### 添加数据分组

```javascript
const taskGroups = {
    'stock': { name: '📈 股票监控', keywords: ['股票', '持仓'] },
    'news': { name: '📰 新闻资讯', keywords: ['新闻', '简报'] }
};

function getTaskGroup(taskName) {
    for (const [group, config] of Object.entries(taskGroups)) {
        if (config.keywords.some(k => taskName.includes(k))) {
            return group;
        }
    }
    return 'other';
}
```

## 总结

这个技能提供了：

- ✅ 完整的监控面板模板
- ✅ 滚动位置保持
- ✅ 智能刷新机制
- ✅ 弹窗交互优化
- ✅ 服务自动重启
- ✅ 响应式设计

可以直接用于创建各种监控面板，无需重复处理交互细节。
