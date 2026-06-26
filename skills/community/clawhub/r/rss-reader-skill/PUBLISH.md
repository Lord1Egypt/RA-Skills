# 发布到 ClawHub 指南

## 方法 1：GitHub 仓库（推荐）

1. **创建 GitHub 仓库**
   ```bash
   cd ~/.agents/skills/rss-reader
   git init
   git add .
   git commit -m "Initial commit: RSS Reader Skill"
   git branch -M main
   git remote add origin https://github.com/你的用户名/rss-reader-skill.git
   git push -u origin main
   ```

2. **提交到 ClawHub**
   - 访问：https://clawhub.com
   - 点击 "Submit Skill"
   - 填写 GitHub 仓库地址
   - 等待审核

## 方法 2：打包上传

1. **打包 Skill**
   ```bash
   cd ~/.agents/skills
   tar -czf rss-reader.tar.gz rss-reader/
   ```

2. **上传到 ClawHub**
   - 访问：https://clawhub.com
   - 点击 "Upload Skill"
   - 选择 `rss-reader.tar.gz`
   - 填写 Skill 信息
   - 提交审核

## 文件清单

✅ 必需文件：
- `SKILL.md` - Skill 说明文档
- `rss_reader.py` - 主脚本
- `requirements.txt` - Python 依赖
- `package.json` - Skill 配置
- `LICENSE` - MIT 协议
- `.gitignore` - Git 忽略规则

✅ 可选文件：
- `README.md` - 详细说明文档
- `PUBLISH.md` - 发布指南（本文件）
- `data/.gitkeep` - 数据目录占位符

## 用户安装后需要做的事

1. **配置 API Key**
   ```bash
   # 获取智谱 API Key：https://open.bigmodel.cn/
   export OPENAI_API_KEY="你的Key"
   export OPENAI_BASE_URL="https://open.bigmodel.cn/api/paas/v4"
   ```

2. **配置飞书 Webhook（可选）**
   ```bash
   export FEISHU_WEBHOOK_URL="你的Webhook地址"
   ```

3. **重启 Gateway**
   ```bash
   openclaw gateway restart
   ```

## Skill 特性

- ✅ 18 个精选订阅源（中英文）
- ✅ AI 摘要（智谱/OpenAI）
- ✅ 每日汇总分析报告
- ✅ 飞书推送
- ✅ 定时刷新（每 2 小时）
- ⚠️ 默认不可用，必须配置 API Key

## 审核要点

1. **无硬编码 API Key** ✅
2. **无硬编码 Webhook** ✅
3. **清晰的配置说明** ✅
4. **MIT 协议** ✅
5. **完整的依赖说明** ✅
6. **测试通过** ✅
