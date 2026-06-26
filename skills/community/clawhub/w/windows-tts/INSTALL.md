# Windows TTS - 快速安装指南

## 方法一：通过 ClawHub 安装（推荐）

```bash
# 1. 登录 ClawHub
clawhub login

# 2. 搜索技能
clawhub search windows-tts

# 3. 安装到 OpenClaw
clawhub install windows-tts

# 4. 验证安装
clawhub list
```

## 方法二：手动安装

### 步骤 1：克隆或下载

```bash
# 进入 skills 目录
cd /home/cmos/skills

# 从 GitHub 克隆（如果有）
git clone https://github.com/your-repo/windows-tts.git

# 或直接复制文件
cp -r /path/to/windows-tts ./
```

### 步骤 2：安装依赖

```bash
cd windows-tts
npm install
npm run build
```

### 步骤 3：配置 OpenClaw

编辑 `/home/cmos/.openclaw/openclaw.json`，在 `plugins` 部分添加：

```json
{
  "plugins": {
    "allow": [
      "windows-tts"
    ],
    "entries": {
      "windows-tts": {
        "enabled": true,
        "config": {
          "url": "http://192.168.1.60:5000",
          "defaultVoice": "zh-CN-XiaoxiaoNeural",
          "defaultVolume": 0.8,
          "timeout": 10000
        }
      }
    }
  }
}
```

### 步骤 4：复制插件到 OpenClaw

```bash
cp -r /home/cmos/skills/windows-tts /home/cmos/.openclaw/extensions/windows-tts
```

### 步骤 5：重启 OpenClaw

```bash
# 重启 OpenClaw 服务
# 具体命令取决于你的启动方式
systemctl restart openclaw
# 或
openclaw restart
```

## 验证安装

### 测试连接

```bash
cd /home/cmos/skills/windows-tts
node -e "
const {WindowsTtsClient} = require('./dist/client');
const client = new WindowsTtsClient({url: 'http://192.168.1.60:5000'});
client.notify({text: '安装成功！'}).then(console.log).catch(console.error);
"
```

### 预期输出

```json
{
  "status": "success",
  "message": "播报完成"
}
```

如果听到"安装成功！"的播报，说明安装成功！🎉

## 配置说明

### 必需配置

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `url` | Windows TTS 服务器地址 | `http://192.168.1.60:5000` |

### 可选配置

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `defaultVoice` | `zh-CN-XiaoxiaoNeural` | 默认音色 |
| `defaultVolume` | `0.8` | 默认音量 (0.0-1.0) |
| `timeout` | `10000` | 超时时间 (毫秒) |

### 常用音色推荐

| 音色 | 特点 | 适用场景 |
|------|------|----------|
| `zh-CN-XiaoxiaoNeural` | 温暖亲切 | 家庭提醒、日常通知 |
| `zh-CN-YunxiNeural` | 清晰专业 | 正式通知、会议提醒 |
| `zh-CN-YunjianNeural` | 激情活力 | 运动场景、活动播报 |
| `en-US-JennyNeural` | 友好女声 | 英文通知 |

## 使用方法

### 在 OpenClaw 中调用

```typescript
// 基本用法
tts_notify({
  text: "程老板，该提醒孩子写作业了！"
});

// 自定义音色和音量
tts_notify({
  text: "Attention: Meeting in 5 minutes",
  voice: "en-US-JennyNeural",
  volume: 0.7
});
```

### 设置定时提醒

编辑 `/home/cmos/.openclaw/cron/jobs.json`：

```json
{
  "jobs": [
    {
      "id": "homework-reminder",
      "agent": "life",
      "schedule": "0 19 * * *",
      "task": "发送作业提醒",
      "delivery": {
        "method": "tts_notify",
        "config": {
          "text": "亲爱的程老板，该提醒孩子写作业了！"
        }
      },
      "enabled": true
    }
  ]
}
```

## 故障排查

### 问题 1：找不到技能

```bash
# 确认技能已安装
clawhub list

# 如果未安装，重新安装
clawhub install windows-tts
```

### 问题 2：连接失败

```bash
# 测试服务器连接
curl -X POST http://192.168.1.60:5000/play_tts \
  -H "Content-Type: application/json" \
  -d '{"text": "测试"}'

# 检查防火墙
# 确保 Windows 允许 5000 端口
```

### 问题 3：音量太小

1. 检查 Windows 系统音量
2. 检查蓝牙音响音量
3. 在配置中提高 `defaultVolume`

## 卸载

```bash
# 通过 ClawHub 卸载
clawhub uninstall windows-tts

# 手动删除
rm -rf /home/cmos/.openclaw/extensions/windows-tts
```

## 更新

```bash
# 通过 ClawHub 更新
clawhub update windows-tts

# 或重新安装
clawhub install windows-tts --force
```

## 帮助

遇到问题？

- 查看文档：`cat SKILL.md`
- 查看示例：`cat README.md`
- 提交 issue：GitHub 仓库
- 社区支持：OpenClaw Discord

## 许可证

MIT License
