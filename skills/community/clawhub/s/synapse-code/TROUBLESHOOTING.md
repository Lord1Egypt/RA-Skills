# Synapse Skills 故障排查指南

> **版本**: v1.1.0  
> **最后更新**: 2026-04-08  
> **适用范围**: synapse-wiki, synapse-code

---

## 🔍 快速诊断流程

```
遇到问题 → 查看错误信息 → 对照本文档 → 尝试解决方案 → 验证修复
```

---

## 📦 安装问题

### 问题 1: 安装脚本失败

**错误信息**:
```
[ERROR] Python 3 未安装
```

**解决方案**:
```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt-get install python3

# 验证安装
python3 --version
```

---

### 问题 2: Claude skills 目录不存在

**错误信息**:
```
Creating Claude skills directory...
```

**解决方案**:
```bash
# 手动创建目录
mkdir -p ~/.claude/skills

# 重新运行安装脚本
cd ~/.claude/skills/synapse-code
./install.sh
```

---

### 问题 3: npm 安装 GitNexus 失败

**错误信息**:
```
npm ERR! Could not install gitnexus
```

**解决方案**:
```bash
# 检查 Node.js 版本
node --version  # 需要 v16+

# 清理 npm 缓存
npm cache clean --force

# 手动安装 gitnexus
cd ~/.claude/skills/synapse-code
npm install

# 验证安装
~/.claude/skills/synapse-code/node_modules/.bin/gitnexus --version
```

---

## 🔧 synapse-code 问题

### 问题 1: Pipeline 脚本未找到

**错误信息**:
```
Error: pipeline.py not found at ~/pipeline-workspace/pipeline.py
```

**原因**: Pipeline workspace 未配置或路径不正确

**解决方案**:

1. **检查配置文件**:
```bash
cat ~/.claude/skills/synapse-code/config.json
```

2. **修正路径**:
```json
{
  "pipeline": {
    "workspace": "~/pipeline-workspace",
    "enabled": true
  },
  "paths": {
    "pipeline_script": "~/pipeline-workspace/pipeline.py"
  }
}
```

3. **确认 Pipeline 存在**:
```bash
ls -la ~/pipeline-workspace/pipeline.py
```

---

### 问题 2: Task Type 推断错误

**现象**: 场景识别不准确

**示例**:
```bash
# 输入
/synapse-code run my-project "设计一个电商系统"

# 预期: design, 实际: feature
```

**解决方案**:

1. **使用更明确的关键词**:
```bash
# ❌ 不推荐
/synapse-code run my-project "设计一个电商系统"

# ✅ 推荐
/synapse-code run my-project "设计方案：电商系统架构规划"
```

2. **手动指定场景**:
```bash
/synapse-code run my-project "电商系统" --scenario design
```

---

### 问题 3: Auto-Log 未记录

**现象**: Pipeline 运行后记忆未更新

**检查步骤**:

1. **确认 .synapse/ 目录存在**:
```bash
ls -la /path/to/project/.synapse/
```

2. **检查 config.json**:
```json
{
  "pipeline": {
    "auto_log": true  // 确保为 true
  }
}
```

3. **手动触发 auto-log**:
```bash
/synapse-code log /path/to/project
```

4. **验证记忆文件**:
```bash
ls -la /path/to/project/.synapse/memory/*/
```

---

### 问题 4: Status 检查无输出

**错误信息**:
```
Error: Not a git repository
```

**原因**: 项目未初始化 git

**解决方案**:
```bash
cd /path/to/project
git init
/synapse-code init /path/to/project
```

---

### 问题 5: Memory Query 无结果

**现象**: 查询历史记录返回空

**检查步骤**:

1. **确认记忆文件存在**:
```bash
find /path/to/project/.synapse/memory -name "*.md"
```

2. **尝试不同查询方式**:
```bash
# 按 task type 查询
/synapse-code query project --task-type feature

# 按关键词查询
/synapse-code query project --contains "登录"

# 查看最近记录
/synapse-code query project --recent-logs --limit 10
```

---

## 📚 synapse-wiki 问题

### 问题 1: Ingest 失败

**错误信息**:
```
Error: Source file not found
```

**原因**: 资料文件路径不正确

**解决方案**:

1. **确认文件存在**:
```bash
ls -la /path/to/wiki/raw/articles/
```

2. **使用绝对路径**:
```bash
# ❌ 可能失败
/synapse-wiki ingest /path/to/wiki raw/articles/article.md

# ✅ 推荐
/synapse-wiki ingest /path/to/wiki /path/to/wiki/raw/articles/article.md
```

3. **验证 Wiki 结构**:
```bash
ls -la /path/to/wiki/
# 应该包含：raw/, wiki/, CLAUDE.md, log.md
```

---

### 问题 2: Wiki 页面未创建

**现象**: ingest 完成但 wiki/ 目录为空

**检查步骤**:

1. **查看 ingest 输出**:
```bash
/synapse-wiki ingest /path/to/wiki /path/to/article.md
```

2. **检查文章格式**:
```markdown
# 必须包含标题
# 测试文章

内容...
```

3. **手动创建测试**:
```bash
# 创建简单测试文章
echo "# Test Article\n\nContent here" > /path/to/wiki/raw/articles/test.md

# 重新 ingest
/synapse-wiki ingest /path/to/wiki /path/to/wiki/raw/articles/test.md
```

---

### 问题 3: Query 返回"没有找到"

**现象**: 查询时提示没有相关内容

**原因**: Wiki 内容为空或查询关键词不匹配

**解决方案**:

1. **先 ingest 资料**:
```bash
# 确保有资料被摄取
/synapse-wiki ingest /path/to/wiki /path/to/article.md
```

2. **检查 index.md**:
```bash
cat /path/to/wiki/wiki/index.md
# 应该列出所有页面
```

3. **使用更宽泛的关键词**:
```bash
# ❌ 太具体
/synapse-wiki query /path/to/wiki "LLM Wiki 的三层架构具体是什么"

# ✅ 更宽泛
/synapse-wiki query /path/to/wiki "LLM Wiki 架构"
```

---

### 问题 4: Lint 报告大量问题

**现象**: 运行 lint 发现很多 isolated pages

**原因**: 新 ingest 的资料没有建立概念关联

**解决方案**:

1. **这是正常现象** - isolated pages 表示页面没有入链

2. **手动建立关联** (可选):
```markdown
# 在相关页面添加 wikilink
相关概念：[[Prompt Engineering]]
```

3. **继续 ingest 更多资料** - 随着知识网络扩大，关联会自动建立

---

## 🐛 常见 Python 错误

### 错误 1: ModuleNotFoundError

**错误信息**:
```
ModuleNotFoundError: No module named 'xxx'
```

**解决方案**:
```bash
# 安装缺失模块
pip3 install <module-name>

# 或检查 script 头部导入
head -20 scripts/*.py
```

---

### 错误 2: Permission Denied

**错误信息**:
```
PermissionError: [Errno 13] Permission denied
```

**解决方案**:
```bash
# 修复脚本权限
chmod +x ~/.claude/skills/synapse-code/scripts/*.py
chmod +x ~/.claude/skills/synapse-code/commands/*.sh

# 修复目录权限
chmod 755 ~/.claude/skills/synapse-code
```

---

### 错误 3: JSON Decode Error

**错误信息**:
```
json.JSONDecodeError: Expecting value: line 1 column 1
```

**原因**: config.json 格式错误或为空

**解决方案**:
```bash
# 检查配置文件
cat ~/.claude/skills/synapse-code/config.json

# 使用模板重建
cp ~/.claude/skills/synapse-code/config.template.json \
   ~/.claude/skills/synapse-code/config.json
```

---

## 🔊 日志调试

### 查看详细日志

```bash
# 运行脚本时增加详细输出
python3 scripts/run_pipeline.py project "需求" 2>&1 | tee debug.log

# 查看日志
cat debug.log
```

### 清理缓存

```bash
# 清理 Python 缓存
find ~/.claude/skills/synapse-code -name "__pycache__" -exec rm -rf {} \;
find ~/.claude/skills/synapse-code -name "*.pyc" -delete

# 清理临时文件
rm -rf /tmp/pipeline_summary.json
rm -rf /tmp/synapse-*
```

---

## 📞 获取帮助

### 内置帮助

```bash
# 查看 Skill 帮助
/synapse-code --help

# 查看命令帮助
/synapse-code run --help
```

### 文档资源

- [AGENT_GUIDE.md](AGENT_GUIDE.md) - Agent 使用指南
- [TESTING.md](TESTING.md) - 测试指南
- [README.md](README.md) - 项目说明

### GitHub Issues

遇到问题可以提交 Issue:
- synapse-code: https://github.com/ankechenlab-node/synapse-code/issues
- synapse-wiki: https://github.com/ankechenlab-node/synapse-wiki/issues

---

## 📋 诊断清单

遇到问题时，按以下清单检查：

### synapse-code
- [ ] Python 3 已安装 (`python3 --version`)
- [ ] git 已安装 (`git --version`)
- [ ] 项目是 git 仓库 (`.git/` 存在)
- [ ] config.json 存在且格式正确
- [ ] pipeline-workspace 路径正确
- [ ] .synapse/ 目录存在

### synapse-wiki
- [ ] Wiki 目录结构完整
- [ ] CLAUDE.md 存在
- [ ] raw/ 目录有资料
- [ ] wiki/index.md 存在
- [ ] log.md 存在

---

*故障排查指南会持续更新，欢迎贡献解决方案*
