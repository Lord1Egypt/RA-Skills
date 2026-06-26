# 阿里云 TTS 配置指南

**创建时间**: 2026-03-05  
**目标**: 为每小时优先级提醒配置中文语音（阿福管家风格）

---

## 📋 配置前准备

### 已有资源
- ✅ 阿里云账号（已注册）
- ✅ API Key：`sk-sp-1f4a006856914b31b5b2a54cc9df76d7`
- ✅ 免费额度：10 万字符/月（约 5-10 小时语音）

### 需要获取
- ❌ **AppKey**（智能语音交互服务）
- ❌ **AppSecret**（可选，用于签名）

---

## 🚀 开通步骤

### 第 1 步：登录阿里云控制台

1. 打开浏览器访问：https://home.console.aliyun.com
2. 使用您的阿里云账号登录

---

### 第 2 步：开通智能语音交互服务

1. 访问 **智能语音交互** 产品页：
   ```
   https://nls-portal.console.aliyun.com
   ```

2. 点击 **"立即开通"** 或 **"免费试用"**

3. 确认开通协议，点击 **"确认开通"**

---

### 第 3 步：创建应用获取 AppKey

1. 进入 **项目管理** 页面：
   ```
   https://nls-portal.console.aliyun.com/project
   ```

2. 点击 **"创建项目"**

3. 填写项目信息：
   - **项目名称**：`OpenClaw-TTS`（或任意名称）
   - **项目描述**：OpenClaw 语音提醒服务
   - **选择服务**：勾选 **"语音合成"**（TTS）

4. 点击 **"确定"** 创建

5. 创建成功后，在项目列表中查看：
   - **AppKey**：复制保存（格式如：`35432156`）
   - **AppSecret**：复制保存（用于签名，可选）

---

### 第 4 步：配置 OpenClaw

#### 方式 A：修改配置文件

编辑 `C:\Users\Xiabi\.openclaw\openclaw.json`：

```json
{
  "tts": {
    "provider": "aliyun",
    "appKey": "你的 AppKey",
    "appSecret": "你的 AppSecret（可选）",
    "voice": "zh-CN-XiaoxiaoNeural",
    "enabled": true
  }
}
```

#### 方式 B：使用命令行配置

```bash
openclaw config set tts.provider aliyun
openclaw config set tts.appKey 你的 AppKey
openclaw config set tts.voice zh-CN-XiaoxiaoNeural
openclaw config set tts.enabled true
```

---

## 🎤 推荐语音配置

### 中文语音（推荐）

| 语音名称 | 风格 | 适用场景 |
|---------|------|---------|
| `zh-CN-XiaoxiaoNeural` | 温柔女声 | 默认推荐 |
| `zh-CN-YunxiNeural` | 成熟男声 | 商务场景 |
| `zh-CN-YunyangNeural` | 新闻男声 | 正式播报 |
| `zh-CN-XiaoyiNeural` | 活泼女声 | 轻松场景 |

### 阿福管家风格推荐

**推荐**: `zh-CN-YunxiNeural`（成熟稳重的男声）

配置示例：
```json
{
  "tts": {
    "provider": "aliyun",
    "appKey": "你的 AppKey",
    "voice": "zh-CN-YunxiNeural",
    "speed": 1.0,
    "volume": 50,
    "pitch": 0
  }
}
```

---

## 🧪 测试 TTS

### 方式 1：使用 OpenClaw TTS 工具

```bash
# 测试中文语音
openclaw tts "Thomas 先生，下午好！现在是 15 点 30 分，提醒您优先处理工作事项。"
```

### 方式 2：在对话中测试

直接对我说：
```
"用中文 TTS 说：Thomas 先生，该喝水了！"
```

### 方式 3：使用阿里云在线测试

1. 访问在线演示：
   ```
   https://nls-portal.console.aliyun.com/demo
   ```

2. 选择 **"语音合成"** 标签

3. 输入测试文本，选择语音，点击 **"试听"**

---

## 💰 费用说明

### 免费额度（老用户）

- **每月免费**：10 万字符
- **约等于**：5-10 小时语音
- **使用场景估算**：
  - 每小时提醒：24 次/天 × 50-100 字 = 1200-2400 字/天
  - 每月约 3.6 万 -7.2 万字符
  - ✅ **免费额度完全够用**

### 超出后价格

| 语音类型 | 价格 |
|---------|------|
| 普通发音人 | 0.06 元/万字符 |
| 优质发音人 | 0.12 元/万字符 |

**月度成本估算**：
- 即使超出免费额度，每月也就 **2-5 块钱**
- 非常便宜！

---

## 🔧 故障排查

### 问题 1：提示"AppKey 无效"

**原因**：AppKey 填写错误或未开通服务

**解决**：
1. 检查 AppKey 是否正确复制（无空格）
2. 确认已开通"智能语音交互"服务
3. 确认项目已创建并启用

### 问题 2：TTS 工具不工作

**原因**：配置文件未生效

**解决**：
```bash
# 重启 OpenClaw
openclaw gateway restart

# 或手动重启
openclaw gateway stop
openclaw gateway start
```

### 问题 3：语音是英文不是中文

**原因**：语音配置错误

**解决**：
```json
{
  "tts": {
    "voice": "zh-CN-XiaoxiaoNeural"  // 确保是中文语音
  }
}
```

---

## 📝 配置检查清单

- [ ] 登录阿里云控制台
- [ ] 开通"智能语音交互"服务
- [ ] 创建项目，获取 AppKey
- [ ] 复制 AppKey 到安全位置
- [ ] 修改 OpenClaw 配置（openclaw.json）
- [ ] 重启 OpenClaw
- [ ] 测试 TTS："用中文说：测试成功"
- [ ] 配置每小时提醒使用 TTS

---

## 🎯 下一步

### 立即行动（5 分钟）

1. **现在开通服务**：
   ```
   https://nls-portal.console.aliyun.com
   ```

2. **创建项目获取 AppKey**

3. **告诉我 AppKey**，我帮您配置到 OpenClaw

### 配置完成后

- ✅ 每小时优先级提醒自动使用中文语音
- ✅ 阿福管家风格播报
- ✅ 每月 10 万字符免费额度

---

## 📞 需要帮助？

**阿里云官方文档**：
- 智能语音交互：https://help.aliyun.com/product/30413.html
- TTS API 文档：https://help.aliyun.com/document_detail/84437.html

**遇到问题随时问我**！🐾

---

**Thomas 先生，现在去开通服务吧！拿到 AppKey 后告诉我，我立即帮您配置！** 🚀
