# 上传到 ClawHub 技能仓库指南

本文档说明如何将技能上传到 ClawHub 技能仓库。

## 准备工作

### 1. 检查文件完整性

确保所有必需文件都已创建：

`ash
cd scheme-generation-design-writing

# 检查根目录文件
ls -la SKILL.md README.md config.json LICENSE CHANGELOG.md .gitignore

# 检查脚本文件
ls -la scripts/index_projects.py scripts/match_projects.py

# 检查数据文件
ls -la data/project_index_example.json

# 检查参考文档
ls -la references/concept_plan_schema.md references/design_desc_schema.md references/examples.md references/quick-start.md
`

### 2. 验证 SKILL.md 格式

确保 SKILL.md 包含正确的元数据：

`markdown
---
name: scheme-generation-design-writing
description: 概念方案生成与设计说明撰写。根据历史项目资料和 Figma 设计稿自动生成概念方案模板（.docx）和设计说明文档（.docx）。
---
`

### 3. 测试脚本功能

在上传前测试脚本是否正常工作：

`ash
# 测试索引构建（需要先配置 config.json）
python scripts/index_projects.py

# 测试项目匹配
python scripts/match_projects.py "测试关键词"
`

## 上传方式

### 方式 1: 通过 Git 仓库上传

#### 步骤 1: 初始化 Git 仓库

`ash
cd scheme-generation-design-writing
git init
git add .
git commit -m "Initial commit: Scheme Generation and Design Writing skill v1.0.0"
`

#### 步骤 2: 创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名称: scheme-generation-design-writing
3. 描述: 概念方案生成与设计说明撰写 - OpenClaw Skill
4. 选择 Public
5. 不要初始化 README（我们已经有了）
6. 创建仓库

#### 步骤 3: 推送到 GitHub

`ash
git remote add origin https://github.com/YOUR_USERNAME/scheme-generation-design-writing.git
git branch -M main
git push -u origin main
`

#### 步骤 4: 提交到 ClawHub

1. 访问 ClawHub 技能仓库提交页面
2. 填写技能信息：
   - **技能名称**: Scheme Generation and Design Writing
   - **技能标识**: scheme-generation-design-writing
   - **描述**: 概念方案生成与设计说明撰写
   - **GitHub 仓库**: https://github.com/YOUR_USERNAME/scheme-generation-design-writing
   - **版本**: 1.0.0
   - **分类**: 设计工具 / Design Tools
   - **标签**: design, documentation, figma, ui/ux, automation
3. 提交审核

### 方式 2: 直接上传压缩包

#### 步骤 1: 创建压缩包

`ash
# Windows (PowerShell)
Compress-Archive -Path scheme-generation-design-writing -DestinationPath scheme-generation-design-writing-v1.0.0.zip

# macOS/Linux
cd ..
zip -r scheme-generation-design-writing-v1.0.0.zip scheme-generation-design-writing -x "*.pyc" "*__pycache__*" "*.git*"
`

#### 步骤 2: 上传到 ClawHub

1. 访问 ClawHub 技能仓库上传页面
2. 上传 ZIP 文件
3. 填写技能信息（同上）
4. 提交审核

## 技能信息填写指南

### 基本信息

**技能名称（英文）**: Scheme Generation and Design Writing

**技能名称（中文）**: 概念方案生成与设计说明撰写

**技能标识**: scheme-generation-design-writing

**版本**: 1.0.0

### 描述信息

**简短描述（英文）**:
`
Automatically generate concept proposals and design specifications based on historical project data and Figma designs. Reduce documentation time from 3-5 days to 2 minutes.
`

**简短描述（中文）**:
`
基于历史项目资料和 Figma 设计稿自动生成概念方案和设计说明文档。将文档产出时间从 3-5 天缩短至 2 分钟。
`

**详细描述**:
`
这是一个专业的 UI/UX 设计文档自动生成工具，充分利用 OpenClaw 的原生能力。

核心功能：
- 基于历史项目资料智能生成概念方案
- 根据 Figma 设计稿自动撰写设计说明
- 支持多风格方案对比
- 输出专业的 Word 文档

技术特点：
- 极简设计，代码 < 500 行
- 无复杂依赖，仅需 Python 标准库
- 智能项目匹配算法
- 支持图片和 Figma 设计稿分析

适用场景：
- UI/UX 设计师需要快速生成设计文档
- 设计团队需要标准化文档输出
- 项目经理需要快速产出方案文档
- 设计咨询公司需要提高文档产出效率
`

### 分类和标签

**主分类**: 设计工具 / Design Tools

**子分类**: 文档生成 / Documentation

**标签**:
- design
- documentation
- figma
- ui/ux
- automation
- word
- proposal
- specification

### 依赖信息

**Python 版本**: 3.7+

**OpenClaw 版本**: 所有版本

**可选依赖**:
- figma skill (用于 Figma 集成)

**系统要求**:
- 操作系统: Windows, macOS, Linux
- 磁盘空间: < 1 MB
- 内存: < 100 MB

### 使用统计

**预计使用时长**: 2-5 分钟

**难度等级**: 中级 / Intermediate

**推荐用户**:
- UI/UX 设计师
- 产品设计师
- 交互设计师
- 设计团队负责人
- 项目经理

## 审核要点

ClawHub 审核时会检查：

### 1. 文件完整性
- ✅ SKILL.md 存在且格式正确
- ✅ README.md 清晰易懂
- ✅ 脚本文件可执行
- ✅ 文档完整

### 2. 代码质量
- ✅ 代码符合 PEP 8 规范
- ✅ 有适当的注释
- ✅ 错误处理完善
- ✅ 无安全隐患

### 3. 文档质量
- ✅ 使用说明清晰
- ✅ 示例完整
- ✅ 故障排查详细
- ✅ 中英文描述准确

### 4. 功能测试
- ✅ 脚本可正常运行
- ✅ 配置文件格式正确
- ✅ 示例数据有效
- ✅ 无明显 bug

## 审核后

### 审核通过
1. 技能会出现在 ClawHub 技能市场
2. 用户可以通过 OpenClaw 安装使用
3. 你会收到通知邮件

### 审核未通过
1. 你会收到审核意见
2. 根据意见修改
3. 重新提交审核

## 维护和更新

### 发布新版本

1. 更新代码和文档
2. 更新 CHANGELOG.md
3. 更新版本号
4. 提交到 Git 仓库
5. 在 ClawHub 提交新版本

### 版本号规范

遵循语义化版本 (Semantic Versioning):
- **主版本号**: 不兼容的 API 修改
- **次版本号**: 向下兼容的功能性新增
- **修订号**: 向下兼容的问题修正

示例:
- 1.0.0 → 1.0.1 (bug 修复)
- 1.0.1 → 1.1.0 (新增功能)
- 1.1.0 → 2.0.0 (重大更新)

## 推广建议

### 1. 编写博客文章
介绍技能的使用场景和价值

### 2. 制作演示视频
展示技能的实际使用效果

### 3. 社交媒体分享
在设计师社区分享

### 4. 收集用户反馈
持续改进技能

## 联系方式

如有问题，可以通过以下方式联系：
- GitHub Issues
- ClawHub 社区论坛
- 邮件: your-email@example.com

## 许可证

本技能采用 MIT 许可证，允许：
- ✅ 商业使用
- ✅ 修改
- ✅ 分发
- ✅ 私人使用

要求：
- 保留版权声明
- 保留许可证声明

## 致谢

感谢 ClawHub 社区和所有贡献者！
