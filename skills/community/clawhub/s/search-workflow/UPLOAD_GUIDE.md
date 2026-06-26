# 🔍 Search Workflow Skill - ClawHub 上传指南

**创建时间**: 2026-03-14  
**技能版本**: v1.0.0  
**作者**: academic-assistant

---

## 📦 技能包内容

```
search-workflow/
├── openclaw.skill.json    # 技能配置 (2.5 KB)
├── SKILL.md               # 技能说明 (1.4 KB)
└── scripts/
    └── search_workflow.py # 主脚本 (3.1 KB)
```

**总大小**: ~7 KB

---

## 🚀 上传步骤

### 步骤 1: 登录 ClawHub

浏览器已打开，请访问：
```
https://clawhub.ai/cli/auth?redirect_uri=http%3A%2F%2F127.0.0.1%3A60875%2Fcallback&state=92e37531d0c233a8c5d59604852b5bb6
```

**登录流程**:
1. 点击浏览器中的链接
2. 使用 ClawHub 账号登录
3. 授权 CLI 访问
4. 登录成功后返回终端

---

### 步骤 2: 验证登录

```bash
clawhub whoami
```

**预期输出**:
```
✅ Logged in as: [你的用户名]
```

---

### 步骤 3: 上传技能

```bash
clawhub publish C:\Users\13600\.openclaw\workspace\skills\search-workflow
```

**预期输出**:
```
📦 Packing skill...
📤 Uploading to ClawHub...
✅ Published successfully!
🔗 Skill URL: https://clawhub.com/skills/search-workflow
```

---

### 步骤 4: 验证上传

访问 ClawHub 技能页面：
```
https://clawhub.com/skills/search-workflow
```

**检查内容**:
- ✅ 技能名称正确
- ✅ 描述完整
- ✅ 版本号正确 (v1.0.0)
- ✅ 作者信息
- ✅ 许可证 (MIT)

---

## 📋 技能信息

### 基本信息

| 项目 | 内容 |
|------|------|
| **技能 ID** | search-workflow |
| **技能名称** | Search Workflow |
| **版本** | v1.0.0 |
| **作者** | academic-assistant |
| **许可证** | MIT |
| **分类** | productivity |

---

### 功能特点

- ✅ 5 阶段搜索流程
- ✅ 整合多个搜索技能
- ✅ 4 种搜索场景
- ✅ 自动触发关键词
- ✅ 结构化输出

---

### 触发关键词

```
搜索、查找、查询、search、调研、文献、资料
```

---

### 依赖技能

**必需**:
- tavily-search
- web_fetch

**可选**:
- web_search
- perplexity-search
- research-lookup
- bgpt-paper-search

---

## 🎯 使用示例

### 安装后使用

```bash
# 安装技能
clawhub install search-workflow

# 使用技能
python skills/search-workflow/scripts/search_workflow.py "柯罗马 清华大学 论文"
```

### 在 Agent 中配置

编辑 `agents/academic-assistant/agent/config.json`:
```json
{
  "skills": [
    "search-workflow",
    "tavily-search",
    ...
  ]
}
```

---

## 📊 技能详情

### 5 阶段工作流

| 阶段 | 时间 | 说明 |
|------|------|------|
| 1. 查询分析 | 1-2 分钟 | 意图识别、关键词提取 |
| 2. 搜索执行 | 2-10 分钟 | 多引擎搜索 |
| 3. 结果处理 | 1-5 分钟 | 去重、排序、摘要 |
| 4. 内容提取 | 1-5 分钟 | 网页全文获取 |
| 5. 整理输出 | 1-3 分钟 | 结构化报告 |

---

### 4 种搜索场景

| 场景 | 引擎 | 输出 |
|------|------|------|
| academic | tavily-search, bgpt-paper-search | 学术简历、论文列表 |
| realtime | tavily-search | 最新新闻 |
| deep_research | tavily-search, market-research-reports | 深度调研报告 |
| fact_check | tavily-search, perplexity-search | 事实核查报告 |

---

## ⚠️ 常见问题

### 问题 1: 登录失败

**错误**: `Error: Not logged in`

**解决**:
```bash
# 重新登录
clawhub login

# 检查登录状态
clawhub whoami
```

---

### 问题 2: 上传失败

**错误**: `Failed to publish skill`

**检查**:
1. 技能配置文件是否正确
2. 文件路径是否正确
3. 网络连接是否正常

**解决**:
```bash
# 验证技能配置
clawhub inspect C:\Users\13600\.openclaw\workspace\skills\search-workflow

# 重新上传
clawhub publish C:\Users\13600\.openclaw\workspace\skills\search-workflow
```

---

### 问题 3: 技能文件缺失

**错误**: `Missing required files`

**必需文件**:
- openclaw.skill.json
- SKILL.md

**检查**:
```bash
Get-ChildItem -Path "C:\Users\13600\.openclaw\workspace\skills\search-workflow" -File
```

---

## 📞 支持资源

### ClawHub 文档

- **官网**: https://clawhub.com/
- **文档**: https://clawhub.com/docs
- **技能市场**: https://clawhub.com/skills

### 社区支持

- **Discord**: https://discord.gg/clawhub
- **GitHub**: https://github.com/clawhub

---

## 📝 上传检查清单

- [ ] 技能文件已创建
- [ ] 配置文件正确
- [ ] 技能说明完整
- [ ] 脚本可执行
- [ ] 已登录 ClawHub
- [ ] 上传成功
- [ ] 验证技能页面

---

## 🎉 上传成功后

### 分享技能

```
🔍 Search Workflow Skill 已发布！

📦 技能名称：Search Workflow
🔗 链接：https://clawhub.com/skills/search-workflow
📝 版本：v1.0.0
👤 作者：academic-assistant

功能：标准化搜索工作流，整合多个搜索技能
```

### 推广建议

1. **ClawHub 社区**: 发布技能介绍帖
2. **社交媒体**: Twitter/X、微信公众号
3. **学术圈**: 实验室群组、学术会议

---

**创建时间**: 2026-03-14  
**维护者**: academic-assistant  
**下次更新**: 功能改进时

---

*祝上传顺利！*📦🚀
