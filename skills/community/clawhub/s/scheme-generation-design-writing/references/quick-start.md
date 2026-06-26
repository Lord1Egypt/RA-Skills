# 快速开始指南

本指南将帮助你快速上手使用"概念方案生成与设计说明撰写"技能。

## 前置要求

- Python 3.7 或更高版本
- OpenClaw CLI 或 OpenClaw Desktop
- 至少 20-30 个历史项目资料

## 安装步骤

### 1. 安装技能

如果你是从 ClawHub 安装：

`ash
# 使用 OpenClaw 技能安装器
在 OpenClaw 中输入：请安装 scheme-generation-design-writing 技能
`

如果你是手动安装：

`ash
# 克隆或下载技能到 OpenClaw 技能目录
cp -r scheme-generation-design-writing ~/.OpenClaw/skills/
`

### 2. 配置项目路径

编辑 config.json 文件：

`json
{
  "projects_path": "C:\\path\\to\\your\\historical\\projects",
  "output_path": "C:\\path\\to\\output\\directory",
  "max_related_projects": 5,
  "num_proposal_styles": 3,
  "enable_figma": true,
  "enable_image_analysis": true
}
`

**重要配置项说明：**

- projects_path: 你的历史项目资料根目录（必填）
- output_path: 生成文档的输出目录（必填）
- max_related_projects: 匹配相关项目的最大数量（默认 5）
- 
um_proposal_styles: 生成概念方案的风格数量（默认 3）

### 3. 建立项目索引

首次使用前，需要建立项目索引：

`ash
cd ~/.OpenClaw/skills/scheme-generation-design-writing
python scripts/index_projects.py
`

**预期输出：**

`
=== 项目索引构建器 ===

项目路径: C:\path\to\your\historical\projects

找到 50 个项目文件夹

[1/50] 索引项目: 2020.12.9 福建省农村信用社手机银行体验升级
[2/50] 索引项目: 2021.03.15 智能家居控制APP设计
...

索引已保存到: data/project_index.json
总项目数: 50

=== 索引统计 ===

按行业分布:
  金融: 15 个项目
  IoT: 10 个项目
  电商: 8 个项目
  ...

按类型分布:
  APP: 35 个项目
  网站: 10 个项目
  ...

总文件数: 523

✓ 索引构建完成!
`

### 4. 测试匹配功能

测试项目匹配是否正常工作：

`ash
python scripts/match_projects.py "智能家居"
`

**预期输出：**

`
查询: 智能家居
最大结果数: 5

找到 3 个相关项目:

1. 2021.03.15 智能家居控制APP设计
   相关度: 8.5
   行业: IoT | 类型: APP
   日期: 2021-03-15
   路径: C:\projects\2021.03.15 智能家居控制APP设计
   文件数: 8
   设计文档: 概念方案.docx, 设计说明_设备列表.docx

2. 2022.08.20 智能家居小程序
   相关度: 7.0
   行业: IoT | 类型: 小程序
   ...
`

## 基本使用

### 场景 1: 生成概念方案

在 OpenClaw 中输入：

`
请基于历史项目生成一个智能家居 APP 的概念方案，要求：
- 行业：IoT / 智能硬件
- 目标用户：25-45岁，中高收入
- 核心功能：设备控制、场景联动、数据可视化
- 设计风格：科技感、简洁、现代
`

OpenClaw 会：
1. 自动匹配相关历史项目
2. 读取相关项目的设计文档
3. 生成 3 个不同风格的概念方案
4. 输出 Word 文档到配置的输出目录

### 场景 2: 生成设计说明

在 OpenClaw 中输入：

`
请基于这个设计稿生成设计说明：
C:\designs\device-list.png

项目信息：
- 项目名称：智能家居控制 APP
- 页面名称：设备列表页
`

OpenClaw 会：
1. 分析设计稿（布局、色彩、组件等）
2. 匹配相关历史项目
3. 生成结构化的设计说明
4. 输出 Word 文档

### 场景 3: 基于 Figma 生成设计说明

在 OpenClaw 中输入：

`
请基于这个 Figma 设计稿生成设计说明：
https://www.figma.com/file/xxxxx

项目：智能家居控制 APP
页面：设备列表页
`

**注意：** 需要先安装并配置 figma skill。

## 高级使用

### 自定义文档模板

如果你想自定义生成的文档结构，可以编辑：

- 
eferences/concept_plan_schema.md - 概念方案模板
- 
eferences/design_desc_schema.md - 设计说明模板

### 手动指定参考项目

如果自动匹配的项目不理想，可以手动指定：

`
请基于以下项目生成概念方案：
- C:\projects\2021.03.15 智能家居控制APP设计
- C:\projects\2022.08.20 智能家居小程序

需求：...
`

### 只生成特定章节

如果你只需要某些章节：

`
请为电商 APP 生成信息架构方案，只需要信息架构部分。
`

### 批量生成

如果你需要为多个页面生成设计说明：

`
请为以下 3 个页面生成设计说明：
1. 首页：C:\designs\home.png
2. 设备列表页：C:\designs\device-list.png
3. 设备详情页：C:\designs\device-detail.png

项目：智能家居控制 APP
`

## 维护与更新

### 更新项目索引

当你添加了新的历史项目后，需要重新建立索引：

`ash
python scripts/index_projects.py
`

建议定期（如每月）更新一次索引。

### 查看索引统计

查看当前索引的统计信息：

`ash
python scripts/index_projects.py
`

### 清理索引

如果需要重新建立索引，删除索引文件即可：

`ash
rm data/project_index.json
python scripts/index_projects.py
`

## 故障排查

### 问题 1: 找不到 config.json

**错误信息：**
`
配置文件不存在: config.json
`

**解决方法：**
1. 确保 config.json 在技能根目录
2. 检查文件名是否正确（区分大小写）

### 问题 2: 项目路径不存在

**错误信息：**
`
项目路径不存在: C:\path\to\projects
`

**解决方法：**
1. 检查 config.json 中的 projects_path 是否正确
2. 确保路径存在且有读取权限
3. Windows 路径使用双反斜杠 \\ 或单正斜杠 /

### 问题 3: 索引不存在

**错误信息：**
`
项目索引不存在: data/project_index.json
请先运行: python scripts/index_projects.py
`

**解决方法：**
`ash
python scripts/index_projects.py
`

### 问题 4: 找不到相关项目

**现象：**
`
未找到相关项目
`

**解决方法：**
1. 调整查询关键词，使用更具体的描述
2. 检查历史项目的命名是否包含相关关键词
3. 手动指定参考项目

### 问题 5: Python 版本过低

**错误信息：**
`
SyntaxError: ...
`

**解决方法：**
确保 Python 版本 >= 3.7：
`ash
python --version
`

## 最佳实践

### 1. 历史项目组织

建议的项目文件夹命名格式：
`
YYYY.MM.DD 项目名称 行业关键词 类型关键词
`

示例：
`
2021.03.15 智能家居控制APP IoT移动端
2022.06.20 电商平台改版 购物APP
`

### 2. 文件命名规范

- 需求文档：包含"需求"、"requirement"、"PRD"等关键词
- 设计文档：包含"设计"、"design"、"说明"等关键词
- 设计稿：使用描述性名称，如"首页.png"、"设备列表.png"

### 3. 提供详细需求

生成质量与需求描述的详细程度成正比。建议包含：
- 行业和项目类型
- 目标用户
- 核心功能
- 设计风格
- 特殊要求

### 4. 定期更新索引

建议每月更新一次项目索引，确保新项目被纳入匹配范围。

### 5. 人工审阅

生成的文档建议人工审阅后使用，特别是：
- 首次使用时
- 历史项目较少时
- 需求较特殊时

## 下一步

- 查看 
eferences/examples.md 了解更多使用示例
- 查看 SKILL.md 了解完整功能说明
- 根据实际需求自定义文档模板

## 获取帮助

如果遇到问题：
1. 查看本指南的"故障排查"部分
2. 查看 SKILL.md 的"注意事项"部分
3. 在 OpenClaw 中询问具体问题

祝使用愉快！
