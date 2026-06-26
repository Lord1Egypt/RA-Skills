# Stock Master Pro Web Dashboard

专业金融风格的股票盯盘 Web 界面。

## 🚀 快速启动

### 方式 1：直接打开（推荐）

双击打开 `index.html` 文件，或在浏览器中访问：

```
file:///home/yaoha/.openclaw/workspace/skills/stock-master-pro/web/index.html
```

### 方式 2：本地服务器

```bash
# 使用 Python
cd ~/.openclaw/workspace/skills/stock-master-pro/web
python3 -m http.server 3000

# 访问 http://localhost:3000
```

```bash
# 使用 Node.js
npx serve .

# 访问 http://localhost:3000
```

## 📊 功能模块

### 1. 大盘概览
- 实时显示四大指数（上证、深证、创业板、中证 500）
- 自动更新涨跌幅和成交额
- K 线走势图

### 2. 持仓监控
- 实时盈亏计算
- 涨跌幅预警
- 量比监控
- 状态标签（强势/正常/震荡/走弱/大跌）

### 3. 复盘报告
- 午盘复盘（12:30）
- 尾盘复盘（15:30）
- 收盘总结（16:00）
- Markdown 格式展示

### 4. 实时预警
- 目标价预警
- 止损预警
- 涨跌幅预警
- 放量预警

## 🔄 自动刷新

- **数据刷新**：每 10 秒自动刷新
- **持仓检查**：每 10 分钟自动检查
- **页面隐藏**：自动暂停刷新（节省资源）
- **页面显示**：自动恢复刷新

## 🎨 设计特点

### 专业金融风格
- 深蓝色调（专业、信任）
- 等宽数字字体（JetBrains Mono）
- 红涨绿跌（A 股配色）
- 卡片式布局

### 交互动效
- 卡片悬停效果
- 数字滚动动画
- 预警闪烁提示
- 平滑过渡

### 响应式设计
- 支持桌面/平板/手机
- 自适应布局
- 触控友好

## 📁 文件结构

```
web/
├── index.html              # 主界面
├── dashboard.js            # 数据加载和交互
├── README.md               # 使用说明
├── components/             # 组件目录（可选扩展）
│   ├── MarketOverview.js   # 大盘概览
│   ├── HoldingsMonitor.js  # 持仓监控
│   └── ReviewPanel.js      # 复盘面板
└── assets/                 # 静态资源
    ├── logo.svg
    └── styles.css
```

## 🔧 配置

编辑 `dashboard.js` 中的 `CONFIG` 对象：

```javascript
const CONFIG = {
  refreshInterval: 10000,    // 数据刷新间隔（毫秒）
  dataPath: '../stocks',     // 数据文件路径
  checkInterval: 600000      // 持仓检查间隔（毫秒）
};
```

## 📊 数据来源

Dashboard 从以下文件读取数据：

- `../stocks/last_check.json` - 最新持仓检查数据
- `../stocks/reviews/*.md` - 复盘报告
- `../stocks/announcements.json` - 公告数据
- `../stocks/dragon_tiger.json` - 龙虎榜数据
- `../stocks/earnings_calendar.json` - 财报日历

## ⚠️ 注意事项

1. **跨域问题**：如果直接打开 HTML 文件遇到跨域问题，请使用本地服务器方式启动
2. **数据更新**：确保后端脚本（check_holdings.mjs 等）定期运行以更新数据
3. **浏览器兼容**：推荐使用 Chrome/Firefox/Edge 等现代浏览器

## 🎯 使用场景

### 日常盯盘
- 打开 Dashboard
- 自动显示实时数据
- 预警信息即时推送

### 复盘查看
- 点击"午盘复盘"/"尾盘复盘"按钮
- 查看生成的复盘报告
- 支持历史记录查看

### 持仓管理
- 实时查看盈亏
- 监控预警状态
- 快速决策

## 📝 更新日志

### v1.0.0 (2026-03-24)
- ✅ 初始版本
- ✅ 大盘概览
- ✅ 持仓监控
- ✅ 复盘报告
- ✅ 实时预警
- ✅ 自动刷新

## 📄 许可证

MIT
