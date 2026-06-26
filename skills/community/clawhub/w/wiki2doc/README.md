# Wiki2Doc 工具集完整文档

> 将 Confluence Wiki 页面自动化转换为测试用例 Excel 的完整解决方案

## 目录

- [项目概述](#项目概述)
- [功能特性](#功能特性)
- [快速开始](#快速开始)
- [详细使用说明](#详细使用说明)
- [测试设计方法](#测试设计方法)
- [常见问题](#常见问题)
- [更新日志](#更新日志)

## 项目概述

Wiki2Doc 是一个完整的自动化测试工具集，可以从 Confluence Wiki 页面自动提取需求内容，分析需求质量，生成结构化测试用例，并输出为专业的 Excel 格式。

### 核心价值

- **自动化**：一键完成从Wiki到Excel的完整转换
- **智能化**：自动检测需求遗漏点、矛盾点和不明确点
- **专业化**：支持多种测试设计方法（边界值、场景法、错误推测等）
- **模块化**：各工具可独立使用，也可组合使用
- **标准化**：输出标准化的测试用例格式

### 工作流程

```
Wiki URL
    ↓
[步骤1] 提取内容 → Word文档 (.docx)
    ↓
[步骤2] 需求分析 → 分析报告 (.txt/.json)
    ↓
[步骤3] 生成用例 → Markdown文件 (.md)
    ↓
[步骤4] 格式转换 → Excel文件 (.xlsx)
```

## 功能特性

### ✅ Wiki内容提取
- 自动登录 Confluence（支持账号密码）
- 提取页面标题和完整内容
- 支持文本、图片、表格、代码块等多种格式
- 过滤 CSS 隐藏元素
- 图片自动转换为 JPG
- 保持原始文档顺序

### ✅ 需求分析
- **遗漏点检测**：识别缺失的测试要点、数据校验、UI规格等
- **矛盾点检测**：发现数值矛盾、逻辑矛盾、描述矛盾
- **不明确点检测**：识别模糊描述、缩写不明确等
- **不完整点检测**：发现句子不完整、列表缺失等
- 生成详细的分析报告

### ✅ 测试用例生成
支持多种测试设计方法：

1. **正向测试**：基于功能特性的正常流程测试
2. **边界值测试**：基于数值边界的测试
3. **错误推测**：基于经验的异常场景测试
4. **场景法**：完整的业务流程测试
5. **UI测试**：界面显示和适配测试
6. **兼容性测试**：多环境兼容测试
7. **性能测试**：性能相关测试

### ✅ 格式转换
- Markdown → Excel 自动转换
- 专业的表格格式化
- 自适应列宽和行高
- 表头样式优化
- 自动换行和边框

## 快速开始

### 环境准备

```bash
# 1. 进入项目目录
cd ~/.claude/skills/wiki2doc

# 2. 创建虚拟环境（推荐）
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 安装 Playwright 浏览器（首次使用）
playwright install chromium
```

### 一键生成测试用例

```bash
# 完整自动化流程
/skill wiki2doc --auto http://10.225.1.76:8090/pages/viewpage.action?pageId=12345678
```

该命令将自动完成所有步骤，最终在 `demand/` 目录生成：
- Word文档
- 需求分析报告
- 测试用例Markdown
- 测试用例Excel

## 详细使用说明

### 模式一：完整自动化流程

**推荐使用**，适合快速生成测试用例。

```bash
/skill wiki2doc --auto <Wiki_URL>
```

**示例：**
```bash
/skill wiki2doc --auto http://10.225.1.76:8090/pages/viewpage.action?pageId=34556052
```

**执行过程：**
1. 提取Wiki内容并生成Word文档
2. 分析需求并生成分析报告
3. 自动生成测试用例（Markdown格式）
4. 转换为Excel格式

**输出文件：**
- `需求标题.docx` - Word文档
- `需求标题_analysis_report.txt` - 分析报告
- `需求标题_testcases.md` - 测试用例Markdown
- `需求标题_testcases.xlsx` - 测试用例Excel

### 模式二：独立工具使用

#### 1. Wiki内容提取

```bash
# 单个页面
python bin/wiki2doc.py http://10.225.1.76:8090/pages/viewpage.action?pageId=12345678

# 批量处理
python bin/wiki2doc.py --batch "url1,url2,url3"
```

#### 2. 需求分析

```bash
python bin/analyze/analyze_requirements.py demand/需求文档.docx
```

**输出：**
- JSON格式报告（机器可读）
- TXT格式报告（人类可读）

**分析内容：**
- 遗漏点：缺少测试要点、数据校验等
- 矛盾点：数值矛盾、逻辑矛盾
- 不明确点：模糊描述、缩写不明确
- 不完整点：句子不完整、列表缺失

#### 3. 测试用例生成

```bash
python bin/generate/generate_testcases.py demand/需求文档.docx
```

**输出：**
- Markdown格式测试用例
- JSON格式测试用例

**生成策略：**
- 自动提取功能特性
- 应用多种测试设计方法
- 生成结构化测试用例
- 包含完整的测试信息

#### 4. Markdown转Excel

```bash
python bin/convert/md2excel.py demand/测试用例.md
```

**输出：**
- 格式化的Excel文件
- 专业的表格样式
- 自适应布局

**Excel格式：**
- 用例编号
- 用例模块
- 用例标题
- 前置条件
- 测试步骤
- 优先级
- 预期结果

## 测试设计方法

### 1. 正向测试（功能测试）
- 验证功能正常工作
- 测试核心业务流程
- 验证界面显示正确

### 2. 边界值测试
- 最小值、最小值-1
- 最大值、最大值+1
- 空值、特殊值

### 3. 错误推测法
- 网络异常
- 权限不足
- 数据异常
- 并发冲突
- 资源耗尽

### 4. 场景法
- 基本流程
- 备选流程
- 异常流程
- 端到端流程

### 5. UI测试
- 界面显示
- 样式正确性
- 布局适配
- 响应式设计

### 6. 兼容性测试
- 浏览器兼容
- 分辨率适配
- 系统版本兼容
- 设备兼容

### 7. 性能测试
- 页面加载性能
- 并发性能
- 大数据量性能
- 资源消耗

## 配置说明

### Confluence配置

默认配置在 `bin/wiki2doc.py` 中：

```python
BASE_URL = "http://10.225.1.76:8090"
USERNAME = "yanghua"
PASSWORD = "Aa123123"
```

**修改方式：**

编辑 `bin/wiki2doc.py` 文件，修改相关配置。

**环境变量方式（推荐）：**

```bash
export CONFLUENCE_URL="http://your-wiki-url"
export CONFLUENCE_USERNAME="your-username"
export CONFLUENCE_PASSWORD="your-password"
```

### 输出目录配置

默认输出目录：`~/.claude/skills/wiki2doc/demand/`

可通过环境变量修改：
```bash
export OUTPUT_DIR="/path/to/output"
```

## 文件结构

```
wiki2doc/
├── bin/                          # 工具脚本目录
│   ├── wiki2doc.py              # Wiki提取工具
│   ├── wiki2testcases.py        # 完整工作流脚本
│   ├── analyze/                 # 需求分析模块
│   │   └── analyze_requirements.py
│   ├── generate/                # 测试用例生成模块
│   │   └── generate_testcases.py
│   └── convert/                 # 格式转换模块
│       └── md2excel.py
├── demand/                       # 输出目录
├── .venv/                       # 虚拟环境
├── requirements.txt             # 依赖列表
├── skill.md                     # 技能说明
└── README.md                    # 本文档
```

## 常见问题

### 1. 登录失败

**问题：** 无法登录Confluence

**解决方案：**
- 检查网络连接
- 确认账号密码正确
- 检查Confluence地址是否正确
- 尝试手动登录验证账号状态

### 2. 页面加载超时

**问题：** 提示"Timeout waiting for selector"

**解决方案：**
- 检查网络速度
- 增加超时时间（修改脚本中的timeout参数）
- 检查页面是否存在指定元素

### 3. 图片下载失败

**问题：** 部分图片未下载成功

**解决方案：**
- 检查图片链接是否有效
- 确认有权限访问图片
- 部分图片失败不影响其他内容

### 4. 生成的测试用例不完整

**问题：** 测试用例数量较少或不够详细

**解决方案：**
- 确保需求文档内容充分
- 手动补充特殊场景的测试用例
- 调整生成策略参数

### 5. Excel格式问题

**问题：** Excel显示异常

**解决方案：**
- 使用Microsoft Excel 2016及以上版本
- 检查文件是否完整下载
- 尝试使用WPS或其他办公软件打开

### 6. 编码问题

**问题：** 中文显示乱码

**解决方案：**
- 确保文件编码为UTF-8
- 在Excel中导入时选择UTF-8编码
- 使用记事本打开MD文件验证编码

## 最佳实践

### 1. 需求文档质量
- 确保Wiki页面结构清晰
- 使用标题和列表组织内容
- 包含详细的功能描述
- 明确测试要点

### 2. 测试用例优化
- 自动生成后进行人工审核
- 补充业务特定的测试场景
- 调整优先级排序
- 删除冗余测试用例

### 3. 团队协作
- 将生成的Excel导入测试管理系统
- 定期更新需求文档
- 建立测试用例评审机制
- 保存历史版本

### 4. 持续改进
- 收集测试反馈
- 优化生成策略
- 补充新的测试方法
- 完善测试模板

## 更新日志

### v2.0.0 (2026-03-06)
- ✨ 新增需求分析功能
- ✨ 新增测试用例自动生成
- ✨ 新增Markdown转Excel工具
- ✨ 新增完整自动化工作流
- 🎨 重构为模块化架构
- 📝 完善文档和使用说明

### v1.0.0 (2026-02-28)
- ✅ Wiki内容提取功能
- ✅ Word文档生成
- ✅ 图片处理和转换
- ✅ 批量处理支持

## 贡献指南

欢迎贡献代码、报告问题或提出建议！

### 开发环境设置
```bash
git clone <repo-url>
cd wiki2doc
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 提交代码
1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

本项目仅供内部使用。

## 联系方式

- 项目维护者：Claude Code
- 技术支持：通过Issue反馈问题
- 功能建议：通过Issue提交建议

---

**Made with ❤️ by Claude Code**
