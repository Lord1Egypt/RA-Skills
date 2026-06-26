---
name: scheme-generation-design-writing
description: 概念方案生成与设计说明撰写。根据历史项目资料和 Figma 设计稿自动生成概念方案模板（.docx）和设计说明文档（.docx）。适用场景：(1) 用户提供历史项目资料目录 + 需求，要求生成概念方案模板，(2) 用户提供 Figma 链接 + 历史项目资料，要求撰写设计说明，(3) 用户只需要生成方案模板或设计说明之一，(4) 用户提到'方案模板'、'设计说明'、'概念方案'、'design doc'、'design proposal'等关键词。依赖 figma skill（读取设计稿）。
---

# 概念方案生成与设计说明撰写 Skill

## 概述

这是一个专业的 UI/UX 设计文档自动生成工具，充分利用 OpenClaw 的原生能力，将设计文档产出时间从 3-5 天缩短至 2 分钟。

**核心价值：**
- 基于历史项目资料智能生成概念方案
- 根据 Figma 设计稿自动撰写设计说明
- 支持多风格方案对比
- 输出专业的 Word 文档

**核心理念：**
- Skill 只做编排和索引管理
- OpenClaw 负责理解、生成和渲染
- 无需复杂的 Python 库依赖

## 工作流程

### 流程 1: 生成概念方案

\\\
用户输入需求
    ↓
Skill: 扫描并索引历史项目
    ↓
Skill: 匹配相关项目（Top 5）
    ↓
OpenClaw: 读取相关项目文档
    ↓
OpenClaw: 理解设计风格和规范
    ↓
OpenClaw: 生成 3 个风格的方案
    ↓
OpenClaw: 渲染 Word 文档
    ↓
输出结果
\\\

### 流程 2: 生成设计说明

\\\
用户提供设计稿 + 需求
    ↓
Skill: 匹配相关历史项目
    ↓
OpenClaw: 分析设计稿
  ├─ 图片 → OpenClaw 视觉理解
  └─ Figma → figma skill 提取
    ↓
OpenClaw: 读取相关设计说明
    ↓
OpenClaw: 生成结构化设计说明
    ↓
OpenClaw: 渲染 Word 文档
    ↓
输出结果
\\\

## 使用方法

### 场景 1: 生成概念方案

**用户输入示例：**
\\\
请基于历史项目生成一个智能家居 APP 的概念方案，要求：
- 行业：IoT / 智能硬件
- 目标用户：25-45岁，中高收入
- 核心功能：设备控制、场景联动、数据可视化
- 设计风格：科技感、简洁、现代
\\\

**Skill 执行步骤：**
1. 检查项目索引是否存在，如不存在则运行 \python scripts/index_projects.py\
2. 运行 \python scripts/match_projects.py "智能家居 IoT 科技感"\ 匹配相关项目
3. 将匹配到的项目路径返回给 OpenClaw
4. OpenClaw 读取这些项目的文档并理解设计模式
5. OpenClaw 根据 \
eferences/concept_plan_schema.md\ 生成 3 个不同风格的方案
6. OpenClaw 创建 Word 文档并保存到配置的输出目录

### 场景 2: 生成设计说明

**用户输入示例：**
\\\
请基于这个设计稿生成设计说明：
- 设计稿：C:\designs\smart-home.png
- 项目：智能家居控制 APP
- 目标用户：25-45岁家庭用户
\\\

或者：

\\\
请基于这个 Figma 设计稿生成设计说明：
https://www.figma.com/file/xxxxx
\\\

**Skill 执行步骤：**
1. OpenClaw 分析设计稿（布局、色彩、字体、组件）
   - 如果是图片：使用 OpenClaw 的视觉理解能力
   - 如果是 Figma 链接：调用 figma skill 提取设计信息
2. 运行 \python scripts/match_projects.py "智能家居"\ 匹配相关项目
3. OpenClaw 读取相关项目的设计说明文档
4. OpenClaw 根据 \
eferences/design_desc_schema.md\ 生成结构化设计说明
5. OpenClaw 创建 Word 文档并保存

## 配置

### config.json

在使用前需要配置项目路径和输出路径：

\\\json
{
  "projects_path": "C:\\path\\to\\your\\historical\\projects",
  "output_path": "C:\\path\\to\\output\\directory",
  "max_related_projects": 5,
  "num_proposal_styles": 3,
  "enable_figma": true,
  "enable_image_analysis": true
}
\\\

**配置说明：**
- \projects_path\: 历史项目资料的根目录
- \output_path\: 生成文档的输出目录
- \max_related_projects\: 匹配相关项目的最大数量（默认 5）
- \
um_proposal_styles\: 生成概念方案的风格数量（默认 3）
- \enable_figma\: 是否启用 Figma 集成（默认 true）
- \enable_image_analysis\: 是否启用图片分析（默认 true）

## 脚本说明

### scripts/index_projects.py
**功能：** 扫描历史项目目录，生成项目索引  
**输出：** \data/project_index.json\  
**运行：** \python scripts/index_projects.py\

索引包含：
- 项目名称、路径、日期
- 自动识别的行业和类型
- 提取的关键词
- 文件分类（需求文档、设计文档、设计稿等）

### scripts/match_projects.py
**功能：** 基于需求关键词匹配相关项目  
**输入：** 需求关键词  
**输出：** 相关项目路径列表（按相关度排序）  
**运行：** \python scripts/match_projects.py "关键词"\

匹配算法考虑：
- 关键词在项目名称、行业、类型中的匹配度
- 项目新鲜度（越新越好）
- 项目完整度（文件越多越好）

## 项目索引结构

\\\json
{
  "version": "1.0.0",
  "created_at": "2026-05-27T11:30:00",
  "total_projects": 50,
  "projects": [
    {
      "id": "proj_001",
      "name": "2020.12.9 福建省农村信用社手机银行体验升级",
      "path": "C:\\projects\\2020.12.9 福建省农村信用社...",
      "date": "2020-12-09",
      "industry": "金融",
      "type": "APP",
      "keywords": ["手机银行", "金融", "体验升级"],
      "files": {
        "requirements": ["需求文档.docx"],
        "design_docs": ["设计说明.docx"],
        "designs": ["首页.png", "列表页.png"],
        "others": []
      },
      "file_count": 4,
      "indexed_at": "2026-05-27T11:30:00"
    }
  ]
}
\\\

## 文档模板结构

详细的文档结构定义请参考：
- \
eferences/concept_plan_schema.md\ - 概念方案模板结构
- \
eferences/design_desc_schema.md\ - 设计说明模板结构

### 概念方案包含章节

1. 封面
2. 项目概述
3. 设计目标与范围
4. 用户画像与场景（可选）
5. 竞品分析（可选）
6. 信息架构（可选）
7. 交互方案（可选）
8. 视觉风格方向（可选）
9. 技术可行性评估（可选）

### 设计说明包含章节

1. 封面
2. 页面概述
3. 页面布局结构
4. 组件清单与说明（可选）
5. 交互逻辑（可选）
6. 视觉规范（可选）
7. 响应式适配（可选）
8. 设计变量引用（可选）

## 依赖

### 必需
- Python 3.7+
- openClaw（用于文档理解和生成）

### 可选
- figma skill（用于 Figma 设计稿分析）

### Python 包
- 标准库即可，无需额外安装

## 首次使用

1. **配置项目路径**
   编辑 \config.json\，设置你的历史项目路径和输出路径

2. **建立项目索引**
   \\\ash
   python scripts/index_projects.py
   \\\

3. **测试匹配**
   \\\ash
   python scripts/match_projects.py "智能家居"
   \\\

4. **开始使用**
   在 OpenClaw 中输入需求即可

## 性能指标

- **索引构建**: 1-2 分钟（50 个项目）
- **项目匹配**: < 1 秒
- **方案生成**: 30-60 秒
- **设计说明生成**: 60-90 秒
- **生成质量**: 人工审阅通过率 > 70%

## 优势

✅ **极简**: 代码 < 500 行，无复杂依赖  
✅ **智能**: 充分利用 OpenClaw 的理解能力  
✅ **灵活**: OpenClaw 可处理各种文档格式  
✅ **快速**: 2 分钟生成专业文档  
✅ **可扩展**: 易于添加新的文档类型和模板  

## 注意事项

1. **历史项目要求**
   - 至少 20-30 个项目
   - 推荐 50-100 个项目
   - 项目质量越高，生成质量越好

2. **文件格式支持**
   - Word (.docx, .doc)
   - PDF (.pdf)
   - Markdown (.md)
   - 图片 (.jpg, .png, .gif)
   - Figma 链接

3. **生成质量**
   - 首次生成可能需要人工审阅和调整
   - 建议定期更新项目索引
   - 可以基于反馈优化匹配算法

## 故障排查

### 问题 1: 找不到相关项目
**原因：** 索引不存在或关键词匹配度低  
**解决：** 
- 运行 \python scripts/index_projects.py\ 重建索引
- 调整查询关键词，使用更具体的描述

### 问题 2: 生成质量不佳
**原因：** 历史项目数量少或质量低  
**解决：** 
- 增加高质量历史项目
- 优化需求描述，提供更多上下文
- 手动指定参考项目

### 问题 3: 索引构建失败
**原因：** 项目路径错误或无访问权限  
**解决：** 
- 检查 \config.json\ 中的路径是否正确
- 确保有读取权限
- 检查路径中是否有特殊字符

### 问题 4: Figma 集成失败
**原因：** figma skill 未安装或配置错误  
**解决：** 
- 确保 figma skill 已安装
- 检查 Figma API token 配置
- 验证 Figma 链接是否有效

## 更新日志

### v1.0.0 (2026-05-27)
- 初始版本发布
- 支持概念方案生成
- 支持设计说明生成
- 支持图片和 Figma 设计稿分析
- 智能项目匹配算法

## 许可证

MIT License

## 作者

Created for ClawHub Skills Repository
