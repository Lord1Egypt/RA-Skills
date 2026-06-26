# Teaching Materials Skill

中小学教学文档智能生成工具

## 功能

本技能可以智能生成以下教学文档：

- **课件 (PPT)**: 新授课、复习课、练习课等类型
- **教学设计 (教案)**: 完整的教学方案，包含教学目标、重难点、教学过程等
- **学生任务单 (导学案)**: 预习、课堂学习、巩固练习等模块

## 使用方式

### 方式 1: 作为 WorkBuddy Skill 使用（推荐）

#### 快捷激活命令

安装后可以使用以下快捷命令：

| 命令 | 说明 | 示例 |
|------|------|------|
| `tapl` | 快捷启动（Teacher AI Preparing Lesson 缩写） | `tapl` 或 `tapl 六年级下册英语第一课` |
| `备课` | 中文快捷命令 | `备课` 或 `备课《折扣》` |
| `备课助手` | 中文完整名称 | `备课助手` 或 `备课助手《古诗三首》` |
| `做课件` | 强调制作课件 | `做课件` 或 `做课件《圆的面积》` |
| `写教案` | 强调编写教案 | `写教案` 或 `写教案《小数乘法》` |
| `教学助手` | 教学辅助通用命令 | `教学助手` 或 `教学助手 英语` |
| `teaching` | 英文通用命令 | `teaching` 或 `teaching math` |

#### 自然语言触发

```
帮我设计一节《二次函数》的教学设计
制作一个《全等三角形》复习课的PPT
创建一个《有理数运算》的导学案
```

本技能会自动：
1. 收集教学信息（年级、课型、学生学情等）
2. 搜索网络教学资源
3. 生成精美的课件（含配图和思维导图）
4. 创建规范的教案和任务单
5. 保存到 `{workspace}/MyTeacher/` 目录

### 方式 2: 使用 Python 程序独立运行

本技能提供了独立的 Python 程序，可以独立运行：

#### 基础版本

```bash
# 仅创建文件夹结构
python teaching_materials.py \
    --grade "五上" \
    --unit "第一单元" \
    --lesson_num "第1课" \
    --lesson_name "古诗三首" \
    --create-folder

# 生成教学设计模板
python teaching_materials.py \
    --grade "五上" \
    --unit "第一单元" \
    --lesson_num "第1课" \
    --lesson_name "古诗三首" \
    --subject "语文" \
    --generate-design
```

#### 完整版本（需要依赖 skills）

```bash
# 检查依赖
python generator.py --check

# 在代码中调用
from generator import TeachingMaterialsTool

tool = TeachingMaterialsTool()
info = {
    "grade": "五上",
    "unit": "第一单元",
    "lesson_num": "第1课",
    "lesson_name": "古诗三首",
    "subject": "语文",
    "textbook": "人教版",
    "class_type": "新授课",
    "duration": "1课时",
    "teacher": "张老师",
    "class_name": "五(1)班"
}

# 创建文件夹结构
course_dir = tool.create_course_structure(info)

# 生成文档需要结合 AI 助手使用
```

## 文件结构

```
teaching-materials/
├── SKILL.md                     # 技能说明文档
├── teaching_materials.py        # 基础版 Python 程序
├── generator.py                 # 完整版 Python 工具
├── requirements.txt             # 依赖说明
├── README.md                    # 本文件
└── references/                  # 参考资料和模板
    ├── teaching_design_template.md   # 教学设计模板
    ├── task_sheet_template.md      # 任务单模板
    ├── ppt_guide.md                 # 课件制作指南
    ├── mindmap_guide.md             # 思维导图指南
    └── edu_platforms.md             # 教育资源平台信息
```

## 依赖

本技能主要依赖以下 WorkBuddy Skills：

- **docx**: 用于生成 Word 教案和任务单
- **pptx**: 用于处理 PPT 文件
- **dragon-ppt-maker**: 用于生成精美的 PPT 课件（含渐变背景、图文混排）
- **diagram-generator**: 用于生成思维导图

**注意**: 在独立运行 Python 程序时，某些功能需要手动调用相应的 skills。

## 特色功能

### 1. 自动配图

- 语文古诗词：自动生成诗人画像、意境图、时代背景图
- 数学课件：自动生成情境图、示意图、几何图形、思维导图
- 所有课件都确保图文并茂，避免纯文字堆砌

### 2. 思维导图集成

- 自动识别适合使用思维导图的内容
- 支持 Mermaid、DrawIO、Excalidraw 三种格式
- 智能插入到课件的适当位置

### 3. 学科配色方案

- 语文（古诗词）：深红+米色+金色，古风雅致
- 语文（现代文）：蓝色+紫红+橙色，现代清新
- 数学：青绿+深绿+橙色，严谨专业
- 英语：靛蓝+紫色+粉色，活泼友好

### 4. 网络资源获取

- 自动搜索学科网、智慧教育平台等资源
- 自动下载课件、教案、图片到 `参考资源/` 文件夹

## 输出规范

所有生成的文档统一保存在：

```
{workspace}/MyTeacher/
└── {年级}_{单元}_{课序}_{课程名}/
    ├── {课程名}_课件.pptx
    ├── {课程名}_教学设计.docx
    ├── {课程名}_任务单.docx
    └── 参考资源/
        ├── images/
        └── ...
```

## 更新日志

### v2.0 (当前版本)
- ✅ 新增独立的 Python 程序（teaching_materials.py）
- ✅ 新增完整的生成器工具（generator.py）
- ✅ 支持文件夹结构创建
- ✅ 支持模板数据生成

### v1.0
- 初始版本，纯提示词型技能

## 贡献

欢迎反馈问题和建议！

## 许可

本技能为 WorkBuddy 生态系统的一部分。
