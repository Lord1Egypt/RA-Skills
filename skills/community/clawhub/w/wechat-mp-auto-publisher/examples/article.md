---
title: OpenClaw 自动化工作流：2 分钟搞定公众号文章自动发布
cover: /home/ray/.openclaw/workspace/skills/wechat-mp-auto-publisher/examples/images/cover.png
tags: [OpenClaw, AI 自动化，微信公众号]
---

# OpenClaw 自动化工作流：2 分钟搞定公众号文章自动发布

## 引言

### 背景痛点

你是不是也遇到过这些情况：

- 写了一篇技术文章，手动排版到公众号要花 1 小时
- 每次都要找配图、调格式、上传封面，繁琐得要命
- 想保持定期更新，但时间精力跟不上

我懂你。作为技术人，我们更想把时间花在刀刃上，而不是重复劳动。

### 要解决的问题

今天给你介绍一个**全自动解决方案**：用 OpenClaw 的 `wechat-mp-auto-publisher` 技能，从写文章到发布公众号，**全程自动化，2 分钟搞定**。

### 预期收获

看完这篇教程，你将：
- ✅ 理解 OpenClaw 自动化工作流的核心逻辑
- ✅ 学会一键生成文章框架 + 搜索素材 + 撰写内容
- ✅ 掌握自动配图（通义万相）+ 自动发布的完整流程
- ✅ 直接复用技能，解放双手

![AI 自动化工作流](/home/ray/.openclaw/workspace/skills/wechat-mp-auto-publisher/examples/images/img1.png)

---

## 核心内容

### 要点 1：什么是 OpenClaw 自动化工作流？

OpenClaw 是一个**AI 智能体运行平台**，可以理解为"AI 的操作系统"。它允许你定义各种技能（Skill），让 AI 自动执行复杂任务。

**自动化工作流的核心逻辑：**

```
用户指令 → AI 理解意图 → 调用技能 → 分步执行 → 输出结果
```

以公众号文章为例：

1. **用户说**："写一篇关于 OpenClaw 的文章，发布到公众号"
2. **AI 理解**：触发 `wechat-mp-auto-publisher` 技能
3. **分步执行**：
   - 生成文章框架
   - 搜索背景资料
   - 撰写文章内容
   - 生成配图（封面 + 正文图）
   - 发布到公众号草稿箱
4. **输出结果**：文章链接 + 预览二维码

**关键优势：**
- 🚀 **全流程自动化** - 无需人工干预
- ⚡ **速度快** - 2 分钟完成全部工作
- 🎯 **质量稳定** - 框架化输出，避免遗漏
- 🔄 **可复用** - 一次配置，无限次使用

### 要点 2：技能架构拆解

![AI 概念架构图](/home/ray/.openclaw/workspace/skills/wechat-mp-auto-publisher/examples/images/img2.png)

`wechat-mp-auto-publisher` 技能由 4 个核心脚本组成：

| 脚本 | 功能 | 耗时 |
|------|------|------|
| `generate-framework.js` | 生成文章框架 | <1 秒 |
| `search.js` | 百度搜索素材 | 30 秒 |
| (AI 撰写) | 撰写 3000 字文章 | 30-60 秒 |
| `publish.js` | 发布到公众号 | 5-10 秒 |

**配图环节（通义万相）：**
- 封面图：1 张（1280×1280）
- 正文配图：5 张（场景图、概念图、流程图等）
- 每张耗时：约 6.5 秒
- 总计：约 33 秒

**整体性能：**
- 总耗时：约 2 分钟
- 成功率：100%（经多次测试验证）

### 要点 3：实战案例演示

**案例：写一篇"AI 自动化办公"主题文章**

**步骤 1：生成框架**
```bash
node scripts/generate-framework.js "AI 自动化办公"
```

输出框架：
```markdown
# AI 自动化办公

## 引言
- 背景痛点
- 要解决的问题
- 预期收获

## 核心内容
### 要点 1：自动化场景
### 要点 2：工具选型
### 要点 3：实施步骤

## 实战应用
## 常见问题
## 总结
```

**步骤 2：搜索素材**
```bash
node scripts/search.js "AI 办公自动化"
node scripts/search.js "智能工作流"
node scripts/search.js "RPA 工具对比"
```

![趋势分析图](/home/ray/.openclaw/workspace/skills/wechat-mp-auto-publisher/examples/images/img3.png)

**步骤 3：AI 撰写文章**
- 根据框架展开
- 结合搜索结果补充实时信息
- 口语化表达，像跟朋友聊天
- 每个功能点配代码示例

**步骤 4：生成配图**
```bash
# 封面图
uv run scripts/generate.py \
  --prompt "技术文章封面图，AI 自动化办公主题，简约科技感，蓝紫色调" \
  --output cover.png \
  --model wan2.6-t2i \
  --size "1280*1280"

# 正文配图（5 张）
# 场景图、概念图、趋势图、流程图、实战图
```

**步骤 5：发布到公众号**
```bash
node scripts/publish.js examples/article.md
```

输出：
```
✅ 发布成功！
草稿箱链接：https://mp.weixin.qq.com/s/xxx
预览二维码：[图片]
```

---

![三步流程图](/home/ray/.openclaw/workspace/skills/wechat-mp-auto-publisher/examples/images/img4.png)

## 实战应用

### 使用场景

这个技能适合：

1. **技术博主** - 定期输出技术文章
2. **产品运营** - 快速生成产品推文
3. **企业宣传** - 自动化内容生产
4. **个人 IP** - 保持内容更新频率

### 操作步骤

**环境准备：**

1. 安装 OpenClaw
```bash
npm install -g openclaw
```

2. 配置 API Key
```bash
# ~/.openclaw/.env
DASHSCOPE_API_KEY="sk-xxx"  # 阿里云百炼
WECHAT_APP_ID="wx_xxx"      # 微信公众号
WECHAT_APP_SECRET="xxx"
```

3. 安装技能
```bash
# 技能已在 ~/.openclaw/workspace/skills/wechat-mp-auto-publisher/
```

**使用流程：**

1. 对 OpenClaw 说："写一篇关于 XX 的文章，发布到公众号"
2. AI 自动执行 5 个步骤
3. 每步完成后询问是否继续（可随时停止）
4. 收到草稿箱链接，手机预览确认
5. 手动点击发布（或配置自动发布）

### 注意事项

⚠️ **重要提醒：**

1. **图片路径必须用绝对路径** - wechat-toolkit 要求
2. **发布前检查 IP 白名单** - 确保服务器 IP 在公众号后台配置
3. **API Key 安全** - 不要泄露到公开代码库
4. **内容审核** - 自动生成的内容需人工审核后再发布
5. **频次控制** - 公众号有群发次数限制（订阅号每天 1 次）

![多显示器工作站](/home/ray/.openclaw/workspace/skills/wechat-mp-auto-publisher/examples/images/img5.png)

---

## 常见问题

### Q1：API Key 从哪里获取？

**阿里云百炼（通义万相）：**
https://bailian.console.aliyun.com/?tab=globalset#/efm/api_key

**微信公众号：**
- 登录公众号后台
- 开发 → 基本配置
- 获取 AppID 和 AppSecret

### Q2：配图质量如何？

通义万相（wan2.6-t2i）表现优秀：
- ✅ 稳定性：100% 成功率
- ✅ 速度：6.5 秒/张
- ✅ 质量：科技感强，符合技术文章调性
- ✅ 尺寸：支持自定义（推荐 1280×1280）

### Q3：可以自定义文章风格吗？

可以！修改技能脚本中的 prompt 即可：
- 正式风格 → 调整语气词
- 幽默风格 → 增加段子
- 教程风格 → 强化步骤说明

---

## 总结

### 核心要点

1. **OpenClaw 自动化工作流** = AI 智能体 + 技能编排
2. **wechat-mp-auto-publisher** = 5 步全流程自动化
3. **通义万相配图** = 稳定快速，6.5 秒/张
4. **2 分钟完成** = 从 0 到发布公众号

### 下一步行动

1. **立即体验** - 对 OpenClaw 说"写一篇测试文章"
2. **配置环境** - 设置 API Key 和公众号凭证
3. **定制技能** - 根据你的需求调整框架和风格

### 相关资源

- OpenClaw 官方文档：https://docs.openclaw.ai
- 通义万相 API：https://help.aliyun.com/zh/dashscope/
- 公众号开发文档：https://developers.weixin.qq.com/doc/

---

**觉得有用？欢迎分享给更多朋友！** 🚀

有问题可以在评论区留言，我会逐一回复～
