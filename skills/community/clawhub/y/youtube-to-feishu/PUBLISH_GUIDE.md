# 📦 技能发布指南 - 油管视频转音频到飞书

## ✅ 技能已准备就绪

**技能文件夹：**
```
C:\Users\23134\.openclaw\workspace\skills\youtube-to-feishu\
```

**包含文件：**
- SKILL.md - 技能定义
- index.js - 工具注册
- youtube_upload.py - 下载脚本
- youtube_to_feishu_complete.py - 完整流程
- README.md - 使用文档
- requirements.txt - 依赖

---

## 🚀 发布到 ClawHub 应用市场

### 方法 1：通过 ClawHub 网站（推荐）

1. **访问** https://clawhub.ai
2. **登录** - 使用 GitHub/Google 或邮箱
3. **点击** "Upload" 或 "创建技能"
4. **上传** 整个技能文件夹
5. **填写信息**：
   - **名称：** 油管视频转音频到飞书
   - **Slug：** youtube-to-feishu
   - **版本：** 1.0.0
   - **标签：** youtube, audio, feishu, download, mp3, 视频转换
   - **描述：** 自动下载 YouTube 视频音频，转换为 MP3，上传到飞书云盘并发送下载链接

6. **提交审核** - 通常 24 小时内通过

---

### 方法 2：使用 CLI（需要登录）

```bash
# 1. 登录 clawhub
clawhub login

# 浏览器会打开，完成授权后返回

# 2. 发布技能
clawhub publish "C:\Users\23134\.openclaw\workspace\skills\youtube-to-feishu" \
  --slug "youtube-to-feishu" \
  --name "油管视频转音频到飞书" \
  --version "1.0.0" \
  --changelog "Initial release - YouTube audio to Feishu" \
  --tags "youtube,audio,feishu,download,mp3"
```

---

### 方法 3：通过 GitHub（开源技能）

1. **创建 GitHub 仓库**
   ```bash
   cd C:\Users\23134\.openclaw\workspace\skills\youtube-to-feishu
   git init
   git add .
   git commit -m "Initial release: youtube-to-feishu skill"
   git remote add origin https://github.com/YOUR_USERNAME/youtube-to-feishu.git
   git push -u origin main
   ```

2. **在 ClawHub 导入**
   - 访问 https://clawhub.ai/import
   - 粘贴 GitHub 仓库 URL
   - 自动同步发布

---

## 📝 技能信息模板

### 名称
```
油管视频转音频到飞书
```

### 简短描述
```
自动下载 YouTube 视频音频，转换为 MP3，上传到飞书云盘并发送下载链接到你的飞书对话。
```

### 详细介绍
```markdown
## 功能

- 📹 YouTube 视频下载
- 🎵 MP3 音频转换（192K 高质量）
- ☁️ 飞书云盘自动上传
- 📬 飞书消息即时推送
- 🧹 临时文件自动清理

## 使用方法

在 OpenClaw 对话中发送：

"下载这个 YouTube 音频到飞书：https://www.youtube.com/watch?v=VIDEO_ID"

或

"把这个视频转 MP3 存到飞书：<任何 YouTube 链接>"

## 依赖

- yt-dlp（自动安装）
- Python 3.8+
- 飞书 OAuth 授权

## 限制

- 文件大小：最大 100MB（飞书限制）
- 仅支持音频（视频会转换为 MP3）
- 需要飞书云盘 + IM 权限
```

### 标签
```
youtube, audio, feishu, download, mp3, 视频转换，飞书，自动化
```

### 版本
```
1.0.0
```

### 更新日志
```
Initial release:
- YouTube 音频下载
- MP3 转换（192K）
- 飞书云盘上传
- 飞书消息推送
- 自动清理临时文件
```

---

## 🎯 发布后

发布成功后，技能会出现在：
- https://clawhub.ai/skills/youtube-to-feishu

其他人可以通过以下方式安装：
```bash
# 通过 clawhub
clawhub install youtube-to-feishu

# 或在 OpenClaw 对话中
安装技能：youtube-to-feishu
```

---

## 📸 截图建议

建议上传以下截图到技能页面：

1. **使用示例** - 对话中使用技能的截图
2. **飞书消息** - 收到的交互式卡片截图
3. **飞书云盘** - 上传后的文件截图
4. **流程图** - 技能工作流程图（可选）

---

## ⚠️ 注意事项

1. **版权提醒** - 在技能描述中提醒用户遵守 YouTube 使用条款
2. **权限说明** - 明确说明需要的飞书权限
3. **文件大小** - 说明 100MB 限制
4. **使用场景** - 列出典型使用场景

---

## 🎉 完成检查清单

- [ ] 技能文件夹准备完成 ✅
- [ ] SKILL.md 编写完成 ✅
- [ ] README.md 编写完成 ✅
- [ ] 代码测试通过 ✅
- [ ] 选择发布方式
- [ ] 填写技能信息
- [ ] 上传/提交
- [ ] 等待审核（24 小时内）
- [ ] 审核通过后分享链接

---

*祝发布顺利！🚀*
