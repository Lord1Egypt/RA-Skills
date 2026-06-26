# WSB Digest 安装指南

## 快速开始 (5分钟)

### 步骤 1: 复制 Skill 文件

```bash
# 进入你的 OpenClaw workspace
cd ~/.openclaw/workspace/skills

# 创建 wsb-digest 目录并复制文件
mkdir -p wsb-digest/scripts
cp /path/to/downloaded/apewisdom-wsb.js wsb-digest/scripts/
cp /path/to/downloaded/wsb-digest-trigger.sh wsb-digest/scripts/
cp /path/to/downloaded/SKILL.md wsb-digest/

# 添加执行权限
chmod +x wsb-digest/scripts/wsb-digest-trigger.sh
```

### 步骤 2: 配置 Discord 频道

编辑 `scripts/wsb-digest-trigger.sh`，找到这一行：

```bash
TARGET_CHANNEL_ID="你的频道ID"
```

替换为你的实际频道 ID。

**获取频道 ID 的方法：**
1. 打开 Discord
2. 用户设置 → 高级 → 开启「开发者模式」
3. 右键点击目标频道 → 复制频道 ID

### 步骤 3: 配置 OpenClaw 路径

在同一文件中，检查这一行：

```bash
OPENCLAW_BIN="/root/.local/share/pnpm/openclaw"
```

根据你的安装方式修改：

| 安装方式 | 路径 |
|---------|------|
| pnpm global | `/root/.local/share/pnpm/openclaw` |
| npm global | `/usr/bin/openclaw` 或 `/usr/local/bin/openclaw` |
| 其他 | 运行 `which openclaw` 查看 |

### 步骤 4: 设置定时任务

```bash
crontab -e
```

添加以下行：

```bash
# WSB Digest - 每天北京时间 9:00 和 21:00 推送
0 9,21 * * * /root/.openclaw/workspace/skills/wsb-digest/scripts/wsb-digest-trigger.sh
```

**时间格式说明：**
```
# 每天 9:00 和 21:00
0 9,21 * * *

# 每天 12:00 一次
0 12 * * *

# 每 6 小时
0 */6 * * *
```

### 步骤 5: 测试

```bash
# 手动运行测试
/root/.openclaw/workspace/skills/wsb-digest/scripts/wsb-digest-trigger.sh

# 查看输出
# 如果成功，你会在 Discord 频道看到消息

# 查看日志
tail -f /tmp/wsb-digest.log
```

## 详细配置

### 修改显示数量

编辑 `scripts/apewisdom-wsb.js`：

```javascript
// TOP 股票数量 (默认 15)
const stocks = data.results.slice(0, 15);

// 快速上升股票数量 (默认 5)
const trending = data.results
  .filter(s => s.rank_24h_ago && s.rank_24h_ago - s.rank > 10)
  .slice(0, 5);

// 新上榜股票数量 (默认 5)
const newEntries = data.results
  .filter(s => !s.rank_24h_ago || s.rank_24h_ago === 0)
  .slice(0, 5);
```

### 自定义报告模板

在 `generateDigest()` 函数中，修改 `output` 变量：

```javascript
let output = `📊 **WSB 每日热股报告**\n\n`;
output += `⏰ ${now} (北京时间)\n`;
// ... 添加你想要的格式
```

### 更改时区

默认是北京时间 (Asia/Shanghai)，如需更改：

```javascript
const now = new Date().toLocaleString('zh-CN', { 
  timeZone: '你的时区',  // 例如: 'America/New_York'
  // ...
});
```

时区列表: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

## 故障排除

### 问题 1: "node: command not found"

**症状**: 脚本报错找不到 node

**解决**:
```bash
# 检查 node 安装
which node

# 在脚本中添加正确的 PATH
export PATH="/usr/local/bin:/usr/bin:$PATH"
```

### 问题 2: "Failed to send digest"

**症状**: Discord 消息发送失败

**检查清单**:
1. ✅ `TARGET_CHANNEL_ID` 是否正确？
2. ✅ OpenClaw 是否已连接到 Discord？
3. ✅ 运行 `openclaw message send --channel discord --target "你的频道ID" --message "测试"`

### 问题 3: 抓取返回空数据

**症状**: API 返回 0 条数据

**正常情况**: ApeWisdom API 偶尔会波动，脚本会自动重试 3 次。如果还是失败，可能是网络问题。

**检查**:
```bash
# 手动测试 API
curl -s "https://apewisdom.io/api/v1.0/filter/wallstreetbets/page/1" | head
```

### 问题 4: 消息被截断

**解决**: 脚本已内置分片功能，无需处理。如果仍有问题，调低 `MAX` 值：

```javascript
const MAX = 1500; // 从 1800 调低
```

## 日志位置

```bash
# 实时查看
tail -f /tmp/wsb-digest.log

# 查看最近 100 行
tail -n 100 /tmp/wsb-digest.log

# 搜索错误
grep "❌" /tmp/wsb-digest.log
```

## 更新 Skill

```bash
cd ~/.openclaw/workspace/skills/wsb-digest
git pull  # 如果是 git 仓库
# 或者重新复制新文件
```

## 卸载

```bash
# 1. 删除定时任务
crontab -e
# 删除 WSB Digest 相关的行

# 2. 删除 skill 文件
rm -rf ~/.openclaw/workspace/skills/wsb-digest

# 3. 清理日志 (可选)
rm /tmp/wsb-digest.log
```

## 需要帮助？

- 查看 SKILL.md 获取完整文档
- 检查日志: `tail -f /tmp/wsb-digest.log`
- 测试脚本: 手动运行 `wsb-digest-trigger.sh` 查看详细输出
