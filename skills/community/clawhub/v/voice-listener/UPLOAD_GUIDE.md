# 📤 上传到 ClawHub 指南

## ⚠️ 重要提醒

**以下文件和目录不会被上传（已在 .gitignore 中）：**

- ✅ `baidu_config.json` - 包含你的百度API密钥
- ✅ `iflytek_config.json` - 包含讯飞API密钥
- ✅ `*.wav` - 音频文件
- ✅ `*.log` - 日志文件
- ✅ `__pycache__/` - Python缓存

---

## 📦 准备上传的文件

### 核心文件

```
voice-listener/
├── README.md                    # 完整的使用说明
├── SKILL.md                     # OpenClaw技能文档
├── package.json                 # 技能包配置
├── skill.json                   # 技能元数据
├── clawhub.yaml                 # ClawHub配置
├── .gitignore                   # Git忽略文件
├── baidu_config.example.json    # 配置示例（不包含密钥）
├── voice_input_baidu_smart.py   # 智能唤醒主程序
├── voice_input_baidu_smart.bat  # 启动脚本
├── skill.py                     # OpenClaw技能接口
└── start_voice_listener.py      # 启动器
```

### 文档文件（可选，但建议上传）

```
├── BAIDU_README.md              # 百度API详细说明
├── SMART_WAKEUP_README.md       # 智能唤醒详细说明
└── USAGE.md                     # 使用示例
```

### 测试文件（可选，不推荐上传）

- `test_*.py` - 测试脚本
- `test*.bat` - 测试启动脚本

---

## 🚀 上传步骤

### 方法1：通过 GitHub（推荐）

1. **创建 GitHub 仓库**

   访问：https://github.com/new

   - **仓库名称**：`voice-listener`
   - **描述**：OpenClaw 语音监听助手 - 百度语音识别 + 智能唤醒
   - **可见性**：Public（公开）
   - **不要初始化** README、.gitignore

2. **上传文件**

   在本地技能目录执行：

   ```bash
   cd C:\Users\11666\.agents\skills\voice-listener
   git init
   git add .
   git commit -m "Initial commit: OpenClaw Voice Listener Skill"
   git branch -M main
   git remote add origin https://github.com/你的用户名/voice-listener.git
   git push -u origin main
   ```

3. **在 ClawHub 发布**

   访问 ClawHub：https://clawhub.com/

   - 登录你的账号
   - 点击"发布技能"
   - 输入 GitHub 仓库地址：`https://github.com/你的用户名/voice-listener`
   - 点击"发布"

---

### 方法2：通过 ClawHub 直接上传（如果支持）

1. 访问 ClawHub：https://clawhub.com/
2. 登录你的账号
3. 点击"发布技能"
4. 上传打包好的文件（ZIP格式）
5. 填写技能信息
6. 点击"发布"

---

## 📋 填写 ClawHub 技能信息

### 基本信息

- **技能ID**：`voice-listener`
- **技能名称**：语音监听助手
- **技能图标**：🎤
- **技能描述**：百度语音识别 + 智能唤醒模式。说'小龙虾'激活，'停止'暂停。支持持续语音输入。
- **版本**：1.0.0
- **作者**：你的名字
- **分类**：Productivity（生产力）

### 技能标签

- 语音识别
- 百度
- 唤醒
- 自动化
- 输入助手

### 安装说明

用户安装后需要：
1. 编辑 `baidu_config.json`
2. 填入自己的百度API密钥
3. 运行 `voice_input_baidu_smart.bat`

---

## ⚙️ 用户配置说明

### 配置示例

技能上传后，用户需要复制 `baidu_config.example.json` 为 `baidu_config.json`：

```bash
copy baidu_config.example.json baidu_config.json
```

然后编辑 `baidu_config.json`，填入自己的API密钥：

```json
{
  "APP_ID": "用户的APP_ID",
  "API_KEY": "用户的API_KEY",
  "SECRET_KEY": "用户的SECRET_KEY"
}
```

### 获取 API 密钥

1. 访问：https://ai.baidu.com/
2. 注册/登录账号
3. 进入控制台：https://console.bce.baidu.com/ai/
4. 创建应用，选择"语音识别"
5. 获取 APP ID、API Key、Secret Key

---

## 🔐 安全提示

### ✅ 已采取的安全措施

1. **.gitignore 配置**
   - `baidu_config.json` 已忽略
   - `iflytek_config.json` 已忽略
   - 所有敏感配置文件都不会上传

2. **示例配置文件**
   - 提供了 `baidu_config.example.json` 作为模板
   - 不包含任何真实密钥

3. **文档说明**
   - README.md 中包含详细的配置说明
   - 提醒用户使用自己的API密钥

---

## 📝 上传前检查清单

在上传之前，请确认：

- [ ] 已创建 GitHub 仓库
- [ ] 已配置 .gitignore
- [ ] 已删除或备份 `baidu_config.json`（避免意外上传）
- [ ] 已测试技能功能正常
- [ ] 已完善 README.md 说明
- [ ] 已完善 SKILL.md 文档
- [ ] 已准备 ClawHub 技能信息

---

## 🎯 上传后

### 1. 验证技能

在 ClawHub 上搜索你的技能，确认：
- ✅ 技能信息显示正确
- ✅ README.md 显示正常
- ✅ 下载链接正常

### 2. 测试安装

在新环境测试安装：
```bash
openclaw skill install voice-listener
```

确认：
- ✅ 技能安装成功
- ✅ 文件完整
- ✅ 配置示例正确

### 3. 收集反馈

发布后，收集用户反馈：
- 安装是否顺利
- 配置是否清晰
- 功能是否正常
- 文档是否完善

---

## 💡 提示

1. **首次上传**：可以先上传到个人仓库测试
2. **版本控制**：使用语义化版本（如 1.0.0、1.0.1）
3. **持续更新**：根据用户反馈持续改进
4. **社区贡献**：欢迎其他开发者提交PR

---

## 📞 联系方式

如果在发布过程中遇到问题：

- **ClawHub文档**：https://docs.clawhub.com/
- **OpenClaw社区**：https://discord.gg/clawd
- **GitHub Issues**：在仓库中提交Issue

---

**祝发布顺利！** 🎉

---

**准备好后，告诉我，我可以帮你完成具体的上传步骤！** 🚀