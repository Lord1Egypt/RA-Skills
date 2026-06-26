# 快速安装指南

## 安装步骤

1. **复制整个技能文件夹**

将 `teaching-materials` 文件夹复制到目标 WorkBuddy 的 skills 目录：

```bash
# 目标路径
{目标用户主目录}/.workbuddy/skills/teaching-materials/
```

2. **确认依赖的 Skills**

本技能需要以下 skills 的支持（可选，但推荐）：

- **docx** - 用于生成 Word 教案和任务单
- **pptx** - 用于处理 PPT 文件  
- **dragon-ppt-maker** - 用于生成精美的 PPT 课件
- **diagram-generator** - 用于生成思维导图

**检查方法**:

```bash
cd ~/.workbuddy/skills
ls -la | grep -E "docx|pptx|dragon-ppt-maker|diagram-generator"
```

如果缺少某些 skills，可以：
- 从 SkillHub 安装
- 或手动从其他 WorkBuddy 实例复制

3. **测试安装**

运行以下命令测试基础功能：

```bash
# 检查依赖
cd ~/.workbuddy/skills/teaching-materials
python generator.py --check

# 测试创建文件夹
cd ~/你的工作空间
python ~/.workbuddy/skills/teaching-materials/teaching_materials.py \
    --create-folder \
    --grade "五上" \
    --unit "第一单元" \
    --lesson_num "第1课" \
    --lesson_name "古诗三首"
```

4. **配置快捷激活命令（自动）**

安装本技能后，系统会自动在用户全局记忆中添加以下激活命令：

| 命令 | 说明 | 示例 |
|------|------|------|
| `tapl` | 快捷启动（Teacher AI Preparing Lesson 缩写） | 输入 "tapl" 即可启动 |
| `备课` | 中文快捷命令 | 输入 "备课" 即可启动 |
| `备课助手` | 中文完整名称 | 输入 "备课助手" 即可启动 |
| `做课件` | 强调制作课件 | 输入 "做课件" 即可启动 |
| `写教案` | 强调编写教案 | 输入 "写教案" 即可启动 |
| `教学助手` | 教学辅助通用命令 | 输入 "教学助手" 即可启动 |
| `teaching` | 英文通用命令 | 输入 "teaching" 即可启动 |

**激活命令配置位置**：
```
{用户主目录}/.workbuddy/memory/CLAW.md
```

**配置内容**（已自动添加）：
```markdown
## 技能快捷命令

- `tapl` → 启动中小学教师智能备课助手
- `备课` → 启动中小学教师智能备课助手
- `备课助手` → 启动中小学教师智能备课助手
- `做课件` → 启动中小学教师智能备课助手
- `写教案` → 启动中小学教师智能备课助手
- `教学助手` → 启动中小学教师智能备课助手
- `teaching` → 启动中小学教师智能备课助手
```

5. **在 WorkBuddy 中使用**

重启 WorkBuddy 后，可以通过以下方式使用本技能：

**快捷激活**：
```
tapl
备课
备课助手
做课件
写教案
教学助手
teaching
tapl 六年级下册英语第一课
备课《折扣》
做课件《圆的面积》
写教案《小数乘法》
```

**自然语言**：
```
帮我设计一节《二次函数》的教学设计
制作一个《全等三角形》复习课的PPT
创建一个《有理数运算》的导学案
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能的核心说明，WorkBuddy 加载时的主文件 |
| `teaching_materials.py` | 基础版 Python 程序，可独立运行 |
| `generator.py` | 完整版生成器工具，提供更多功能 |
| `requirements.txt` | 依赖说明 |
| `README.md` | 详细使用文档 |
| `references/` | 参考模板和指南 |

## 独立使用

如果不使用 WorkBuddy，也可以独立运行 Python 程序：

### 基础版

```bash
python teaching_materials.py \
    --grade "五上" \
    --unit "第一单元" \
    --lesson_num "第1课" \
    --lesson_name "古诗三首" \
    --subject "语文" \
    --generate-design
```

### 完整版（需要依赖）

```python
from generator import TeachingMaterialsTool

tool = TeachingMaterialsTool()
deps = tool.check_dependencies()
```

## 常见问题

**Q: 生成的 Word 文档是空的？**  
A: 基础版程序生成的是 Markdown 模板数据。需要结合 AI 助手或 docx skill 转换为完整 Word 文档。

**Q: PPT 生成失败？**  
A: 确保 dragon-ppt-maker skill 已安装，并且 Python 环境正常。

**Q: 如何在 Linux/Mac 上使用？**  
A: 本技能已跨平台适配，直接复制文件夹到对应路径即可。

## 更新记录

- v2.0 (2025-03-26): 新增 Python 独立程序
- v1.0: 初始版本，纯提示词型技能
