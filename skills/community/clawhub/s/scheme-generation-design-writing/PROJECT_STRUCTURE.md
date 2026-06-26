# 项目结构

`
scheme-generation-design-writing/
├── SKILL.md                          # 技能主文档（必需）
├── README.md                         # 项目说明
├── config.json                       # 配置文件模板
├── LICENSE                           # MIT 许可证
├── CHANGELOG.md                      # 更新日志
├── .gitignore                        # Git 忽略文件
│
├── scripts/                          # 脚本目录
│   ├── index_projects.py            # 项目索引构建器
│   └── match_projects.py            # 项目匹配器
│
├── data/                             # 数据目录
│   └── project_index_example.json   # 索引文件示例
│
└── references/                       # 参考文档目录
    ├── concept_plan_schema.md       # 概念方案模板结构
    ├── design_desc_schema.md        # 设计说明模板结构
    ├── examples.md                  # 使用示例
    └── quick-start.md               # 快速开始指南
`

## 文件说明

### 根目录文件

#### SKILL.md（必需）
技能的主文档，包含：
- 技能元数据（name、description）
- 完整的使用说明
- 工作流程
- 配置说明
- 故障排查

#### README.md
项目简介，包含：
- 快速介绍
- 主要功能
- 快速开始
- 技术特点

#### config.json
配置文件模板，用户需要根据实际情况修改：
- projects_path: 历史项目路径
- output_path: 输出目录
- 其他配置项

#### LICENSE
MIT 许可证文件

#### CHANGELOG.md
版本更新日志

#### .gitignore
Git 忽略规则，排除：
- Python 缓存文件
- 生成的索引文件
- 用户配置文件
- 生成的文档

### scripts/ 目录

#### index_projects.py
项目索引构建器，功能：
- 扫描历史项目目录
- 提取项目信息（名称、日期、行业、类型等）
- 分类项目文件
- 生成 JSON 索引文件

#### match_projects.py
项目匹配器，功能：
- 加载项目索引
- 根据关键词匹配相关项目
- 计算相关度评分
- 返回 Top N 项目

### data/ 目录

#### project_index_example.json
索引文件示例，展示：
- 索引数据结构
- 字段说明
- 示例数据

**注意：** 实际的 project_index.json 会在运行 index_projects.py 后自动生成，不包含在版本控制中。

### references/ 目录

#### concept_plan_schema.md
概念方案文档模板结构，定义：
- 必选章节
- 可选章节
- 撰写原则
- 示例结构

#### design_desc_schema.md
设计说明文档模板结构，定义：
- 必选章节
- 可选章节
- 撰写原则
- 示例结构

#### examples.md
详细的使用示例，包含：
- 生成概念方案示例
- 生成设计说明示例
- 高级用法示例
- 常见问题

#### quick-start.md
快速开始指南，包含：
- 安装步骤
- 配置说明
- 基本使用
- 故障排查

## 文件依赖关系

`
SKILL.md (主入口)
    ├── 引用 config.json (配置)
    ├── 调用 scripts/index_projects.py (索引构建)
    ├── 调用 scripts/match_projects.py (项目匹配)
    ├── 参考 references/concept_plan_schema.md (方案模板)
    └── 参考 references/design_desc_schema.md (说明模板)

scripts/index_projects.py
    ├── 读取 config.json
    └── 生成 data/project_index.json

scripts/match_projects.py
    └── 读取 data/project_index.json

README.md
    └── 引用 references/quick-start.md
`

## 数据流

`
用户配置 config.json
    ↓
运行 index_projects.py
    ↓
生成 data/project_index.json
    ↓
用户在 OpenClaw 中输入需求
    ↓
OpenClaw 调用 match_projects.py
    ↓
返回相关项目列表
    ↓
OpenClaw 读取项目文档
    ↓
OpenClaw 根据模板生成文档
    ↓
输出 Word 文档到 output_path
`

## 版本控制

### 包含在版本控制中
- 所有源代码文件
- 文档文件
- 配置文件模板
- 示例文件

### 不包含在版本控制中
- data/project_index.json (自动生成)
- 用户的实际 config.json (包含敏感路径)
- 生成的 Word 文档
- Python 缓存文件
- IDE 配置文件

## 部署清单

上传到 ClawHub 时应包含：
- ✅ SKILL.md
- ✅ README.md
- ✅ config.json (模板)
- ✅ LICENSE
- ✅ CHANGELOG.md
- ✅ .gitignore
- ✅ scripts/index_projects.py
- ✅ scripts/match_projects.py
- ✅ data/project_index_example.json
- ✅ references/concept_plan_schema.md
- ✅ references/design_desc_schema.md
- ✅ references/examples.md
- ✅ references/quick-start.md

## 文件大小

预估文件大小：
- SKILL.md: ~15 KB
- README.md: ~3 KB
- scripts/index_projects.py: ~8 KB
- scripts/match_projects.py: ~6 KB
- references/*.md: ~20 KB
- 其他文件: ~5 KB

总计: ~60 KB

## 兼容性

- Python: 3.7+
- OpenClaw: 所有版本
- 操作系统: Windows, macOS, Linux
- 依赖: 仅 Python 标准库
