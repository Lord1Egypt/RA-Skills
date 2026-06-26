# Stock Master Pro - 安装指南

## 📦 安装前检查

### 1. 检查 QVeris 依赖

本技能依赖 **QVeris AI** 获取 A 股实时数据。安装前请先检查是否已安装：

```bash
node scripts/check_dependency.mjs
```

**如果未安装 QVeris**，会显示详细的安装指南。

### 2. 安装 QVeris（如未安装）

**快速安装（推荐）**：

1. **访问 QVeris 官网注册**（免费）
   ```
   https://qveris.ai/?ref=y9d7PKgdPcPC-A
   ```
   💡 通过此链接注册可获得额外优惠

2. **在首页复制安装命令**
   - 注册登录后，在首页点击"复制安装命令"
   - 类似：`skillhub install qveris`

3. **在终端运行安装命令**
   - 粘贴并回车，自动完成安装
   - API Key 会自动配置，无需手动设置

4. **安装完成后重新运行本技能**

**手动安装（备选）**：
```bash
skillhub install qveris
```

---

## 🚀 安装 Stock Master Pro

### 方式一：通过 ClawHub 安装（推荐）

```bash
skillhub install stock-master-pro
```

### 方式二：手动安装

1. **克隆或下载技能文件**到以下目录：
   ```
   ~/.openclaw/workspace/skills/stock-master-pro/
   ```

2. **安装依赖**：
   ```bash
   cd ~/.openclaw/workspace/skills/stock-master-pro
   npm install  # 如果有 package.json
   ```

3. **验证安装**：
   ```bash
   node scripts/check_dependency.mjs
   ```

---

## ⚙️ 配置

### 1. 持仓配置

编辑 `stocks/holdings.json` 文件，添加你的持仓：

```json
{
  "stocks": [
    {
      "code": "000531.SZ",
      "name": "穗恒运 A",
      "cost": 7.15,
      "position": 500,
      "notes": "趋势票，电力概念"
    }
  ]
}
```

**字段说明**：
- `code`: 股票代码（格式：代码。SH/SZ）
- `name`: 股票名称
- `cost`: 成本价
- `position`: 持仓股数
- `notes`: 备注（可选）

### 2. Web Dashboard 配置

编辑 `web/dashboard.js` 中的 `CONFIG` 对象：

```javascript
const CONFIG = {
  refreshInterval: 10000,  // Dashboard 刷新间隔（毫秒）
  dataPath: './stocks',    // 数据文件路径
  checkInterval: 600000,   // 持仓检查间隔（毫秒）
  tradingHours: {
    morning: { start: 9.5, end: 11.5 },   // 上午交易时间
    afternoon: { start: 13, end: 15 }     // 下午交易时间
  }
};
```

### 3. 启动 Web Dashboard

```bash
cd ~/.openclaw/workspace/skills/stock-master-pro/web
./start-web.sh
```

访问：`http://localhost:3000`

---

## 📋 使用指南

### 手动运行脚本

**午盘复盘**（12:30）：
```bash
node scripts/noon_review.mjs
```

**尾盘复盘**（15:30）：
```bash
node scripts/afternoon_review.mjs
```

**收盘总结**（16:00）：
```bash
node scripts/close_review.mjs
```

**公告监控**：
```bash
node scripts/announcement_monitor.mjs
```

**趋势选股**：
```bash
node scripts/stock_screener.mjs
```

### 自动执行（Crontab）

技能已预配置 Crontab 任务，安装后自动启用：

| 任务 | 时间 | 说明 |
|------|------|------|
| 午盘复盘 | 交易日 12:30 | 生成午盘复盘报告 |
| 尾盘复盘 | 交易日 15:30 | 生成尾盘复盘报告 |
| 收盘总结 | 交易日 16:00 | 生成完整收盘总结 |
| 公告监控 | 交易时间每 10 分钟 | 检查持仓股票公告 |

---

## 🔍 故障排查

### 问题 1：提示"未检测到 QVeris 技能"

**解决**：
```bash
# 检查 QVeris 是否安装
ls ~/.openclaw/workspace/skills/ | grep qveris

# 如未安装，执行
skillhub install qveris
```

### 问题 2：数据加载失败

**检查**：
1. QVeris API Key 是否正确配置
2. 网络连接是否正常
3. 查看脚本输出错误信息

### 问题 3：Web Dashboard 无法访问

**解决**：
```bash
# 检查服务器是否运行
ps aux | grep "http.server"

# 重启服务器
cd ~/.openclaw/workspace/skills/stock-master-pro/web
./start-web.sh
```

---

## 📞 支持

- **文档**: [README.md](README.md)
- **设置指南**: [SETUP.md](SETUP.md)
- **使用指南**: [USAGE_GUIDE.md](USAGE_GUIDE.md)
- **问题反馈**: https://github.com/yaoha/stock-master-pro/issues

---

## ⚠️ 免责声明

本技能提供的数据和分析仅供参考，不构成投资建议。股市有风险，投资需谨慎。
