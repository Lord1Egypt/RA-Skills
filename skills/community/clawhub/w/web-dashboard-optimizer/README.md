# Web Dashboard Optimizer 📊

为 AI Agent 创建流畅、稳定的 Web 监控面板界面的最佳实践集合。

## ✨ 特性

- 🔄 **智能刷新** - 数据哈希对比，仅变化时重新渲染
- 📜 **滚动位置保持** - 自动刷新不跳动
- 🎨 **弹窗交互优化** - 打开/关闭平滑，位置保持
- 🚀 **服务自动重启** - 无限循环守护，5 秒自动重启
- 📱 **响应式设计** - 移动端适配
- 🎯 **连接状态指示** - 实时显示连接状态

## 🎯 适用场景

- 任务执行监控
- 数据可视化展示
- 实时状态面板
- 后台管理界面
- 系统监控仪表板

## 🚀 快速开始

### 1. 安装技能

```bash
clawhub install web-dashboard-optimizer
```

### 2. 复制模板

```bash
cp -r skills/web-dashboard-optimizer my-dashboard
cd my-dashboard
```

### 3. 自定义数据源

编辑 `server.js`：

```javascript
function getData() {
    // 从你的数据源读取
    return {
        timestamp: Date.now(),
        items: [...]
    };
}
```

### 4. 启动服务

```bash
./run-monitor.sh
```

访问：http://localhost:18790

## 📁 文件结构

```
web-dashboard-optimizer/
├── SKILL.md           # 技能文档
├── Meta.json          # 元数据
├── README.md          # 使用说明
├── dashboard.html     # 前端模板
├── server.js          # Node.js 服务器
└── run-monitor.sh     # 自动重启脚本
```

## 🎨 核心代码片段

### 智能刷新

```javascript
const scrollY = window.scrollY;
const hasChanges = newDataHash !== lastDataHash;
if (hasChanges) {
    render(data);
    window.scrollTo(0, scrollY); // 恢复滚动位置
}
```

### 弹窗位置管理

```javascript
// 打开
const scrollY = window.scrollY;
document.body.style.top = -scrollY + 'px';
document.body.classList.add('modal-open');

// 关闭
const scrollY = parseInt(document.body.style.top || '0');
document.body.classList.remove('modal-open');
window.scrollTo(0, Math.abs(scrollY));
```

### 自动重启

```bash
while true; do
    node server.js
    sleep 5  # 5 秒后自动重启
done
```

## 📊 对比 ClawHub 其他监控技能

| 功能 | web-dashboard-optimizer | openclaw-dashboard |
|------|------------------------|-------------------|
| 滚动位置保持 | ✅ 完善 | ⚠️ 基础 |
| 弹窗交互 | ✅ 完善 | ✅ 完善 |
| 智能刷新 | ✅ 数据哈希 | ✅ 完整 |
| 服务自动重启 | ✅ 简单 | ⚠️ 需配置 |
| 自定义 UI | ✅ 完全自由 | ⚠️ 有限 |
| 学习价值 | ✅ 透明可学 | ⚠️ 黑盒 |
| 启动复杂度 | ✅ 一键启动 | ⚠️ 需配置 |

## 🛠️ 自定义

### 修改样式

编辑 `dashboard.html` 中的 `<style>` 部分。

### 修改刷新间隔

```javascript
// 改为 30 秒
refreshInterval = setInterval(loadData, 30000);
```

### 添加数据源

编辑 `server.js` 中的 `getData()` 函数。

## 🐛 故障排查

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

## 📚 最佳实践

1. **数据哈希对比** - 避免不必要的重新渲染
2. **滚动位置保存** - 提升用户体验
3. **弹窗位置管理** - 防止页面跳动
4. **自动重启** - 确保服务持续在线
5. **日志记录** - 便于问题排查

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT-0 - 免费使用、修改、分发，无需署名。

## 🙏 致谢

灵感来源于 openclaw-dashboard 和实际项目需求。

---

**创建时间**: 2026-03-20  
**版本**: 1.0.0  
**作者**: OpenClaw Community
