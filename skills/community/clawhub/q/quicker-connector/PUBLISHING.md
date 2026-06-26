# Quicker Connector 发布指南

## 🚀 发布到 ClawHub

### 前提条件

1. **注册 ClawHub 开发者账号**
   - 访问: https://clawhub.ai
   - 点击 "开发者中心" → "注册"

2. **安装 ClawHub CLI (可选)**
   ```bash
   # 安装 CLI 工具
   npm install -g @clawhub/cli
   
   # 登录
   clawhub login
   ```

3. **准备发布包**
   - 确保 `package.json` 版本号正确
   - 运行验证测试: `python verify_optimization.py`
   - 确保所有文档都是最新的

### 发布步骤

#### 方法一: 使用发布脚本 (推荐)

1. **生成发布包**
   ```bash
   cd quicker-connector
   python scripts/publish_to_clawhub.py
   ```

2. **上传到 ClawHub**
   - 登录 ClawHub 开发者中心
   - 点击 "发布新技能"
   - 上传生成的 `.tar.gz` 文件
   - 填写技能信息:
     - 名称: `quicker-connector`
     - 版本: `1.2.0`
     - 描述: "与 Quicker 自动化工具集成，支持 CSV/数据库双数据源"
     - 分类: `automation`, `productivity`, `windows`
     - 标签: `quicker`, `automation`, `workflow`

3. **提交审核**
   - 等待 ClawHub 团队审核 (通常 1-3 个工作日)
   - 审核通过后，技能将出现在 ClawHub 市场

#### 方法二: 使用 CLI 工具

```bash
# 打包技能
tar -czf quicker-connector-1.2.0.tar.gz quicker-connector/

# 使用 CLI 发布
clawhub publish quicker-connector-1.2.0.tar.gz \
  --name "quicker-connector" \
  --version "1.2.0" \
  --description "Quicker automation integration skill" \
  --category "automation" \
  --tags "quicker,automation,windows"
```

### 发布检查清单

#### ✅ 必要文件检查
- [x] `skill.json` - 技能主配置
- [x] `SKILL.md` - OpenClaw 格式技能文档
- [x] `README.md` - 项目说明文档
- [x] `LICENSE` - MIT 许可证
- [x] `package.json` - NPM 包配置
- [x] `scripts/` - 核心脚本目录
- [x] `tests/` - 测试文件
- [x] `examples/` - 使用示例

#### ✅ 功能验证
- [x] 基本功能测试通过
- [x] 智能匹配功能正常
- [x] 执行功能验证
- [x] 导出功能正常
- [x] 初始化向导工作

#### ✅ 文档完整性
- [x] 中文文档: `README_ZH.md`
- [x] 英文文档: `README_EN.md`
- [x] 更新日志: `CHANGELOG.md`
- [x] 贡献指南: `CONTRIBUTING.md`
- [x] 发布说明: `RELEASE.md`

#### ✅ 安全合规
- [x] 已通过 skill-vetting 安全审计
- [x] 权限声明完整
- [x] 无敏感信息泄露
- [x] 文件操作限制在用户路径
- [x] 子进程调用受限

### 版本管理

#### 语义化版本
- `MAJOR`: 不兼容的 API 变更
- `MINOR`: 向后兼容的功能新增
- `PATCH`: 向后兼容的问题修复

#### 当前版本: 1.2.0
- **1** - 主要版本
- **2** - 功能增强版本
- **0** - 补丁版本

#### 更新版本号
```bash
# 更新 package.json
sed -i 's/"version": "1.2.0"/"version": "1.2.1"/' package.json

# 更新 skill.json
sed -i 's/"version": "1.2.0"/"version": "1.2.1"/' skill.json

# 更新 SKILL.md
sed -i 's/version: 1.2.0/version: 1.2.1/' SKILL.md
```

### 发布后验证

1. **安装测试**
   ```bash
   # 从 ClawHub 安装
   clawhub install quicker-connector
   
   # 验证安装
   cd ~/.openclaw/workspace/skills/quicker-connector
   python verify_optimization.py
   ```

2. **功能测试**
   ```bash
   # 启动 OpenClaw Gateway
   openclaw gateway start
   
   # 测试技能触发
   # 尝试: "用 quicker 截图"
   # 尝试: "帮我翻译这段文字"
   ```

### 维护指南

#### 接收用户反馈
- 监控 ClawHub 用户评分和评论
- 关注 GitHub Issues
- 定期检查错误报告

#### 定期更新
1. **每月检查**
   - 检查兼容性更新
   - 更新依赖版本
   - 修复已知问题

2. **季度更新**
   - 功能增强
   - 性能优化
   - 文档更新

#### 安全更新
- 及时响应安全漏洞
- 更新依赖补丁
- 重新进行安全审计

### 故障排除

#### 发布失败
1. **包太大**
   ```bash
   # 检查包大小
   du -sh quicker-connector-1.2.0.tar.gz
   
   # 移除不必要的文件
   rm -rf __pycache__ *.pyc .DS_Store
   ```

2. **格式错误**
   ```bash
   # 验证 JSON 格式
   python -m json.tool skill.json > /dev/null
   
   # 验证 YAML 格式
   python -c "import yaml; yaml.safe_load(open('SKILL.md').read().split('---')[0])"
   ```

3. **权限问题**
   - 确保 `.tar.gz` 包可读
   - 确保脚本有执行权限
   - 检查文件所有权

#### 安装问题
1. **目录权限**
   ```bash
   # 修复目录权限
   chmod -R 755 ~/.openclaw/workspace/skills
   ```

2. **Python 依赖**
   ```bash
   # 确保 Python 3.8+
   python --version
   
   # 确保必要的包
   pip install chardet sqlite3
   ```

### 联系支持

- **ClawHub 支持**: support@clawhub.ai
- **技能问题**: https://github.com/awamwang/quicker-connector/issues
- **开发者文档**: https://docs.clawhub.ai/publishing-skills
- **社区讨论**: https://clawhub.ai/community

---

## 📄 许可证说明

本项目使用 MIT 许可证发布。发布到 ClawHub 时，许可证会自动包含在包中。

## 🤝 贡献与协作

欢迎提交 Pull Request 和改进建议。详情见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

*最后更新: 2026-03-28*  
*版本: 1.2.0*  
*状态: 准备发布*