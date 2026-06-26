# PPT Generator Skill

用 `python-pptx` 生成暗色科技风演示文稿。

## 使用方式

用户描述 PPT 内容后，生成 Python 脚本并执行，产出 `.pptx` 文件。

## 工作流

1. 用户说明 PPT 主题、大纲、内容要点
2. Agent 读取 `scripts/ppt_lib.py`（核心工具库）
3. Agent 生成调用脚本，组合幻灯片内容
4. 执行脚本 → 输出 `.pptx`
5. 通过 `lightclaw_upload_file` 发送给用户

## 设计规范

- **页面尺寸**：16:9 (13.333 × 7.5 英寸)
- **配色方案**：深蓝黑背景 + 科技蓝/紫/绿/橙强调色
- **字体**：Microsoft YaHei（中文）、Arial（英文）
- **布局**：卡片式、顶部色条、装饰线

## 幻灯片类型

| 类型 | 函数 | 用途 |
|------|------|------|
| 封面页 | `make_cover_slide()` | 标题+副标题+日期 |
| 章节页 | `make_section_slide()` | 章节标题+要点列表 |
| 内容页 | `make_content_slide()` | 标题+2x2卡片网格 |
| 对比页 | `make_compare_slide()` | 左右两栏对比 |
| 架构页 | `make_arch_slide()` | 三列流程+底部补充 |
| 卡片页 | `make_cards_slide()` | 灵活卡片网格 |
| 总结页 | `make_summary_slide()` | 价值总结+收尾 |

## 调色板

```python
DARK_BG    = (0x1A, 0x1A, 0x2E)  # 背景
ACCENT     = (0x00, 0xD2, 0xFF)  # 科技蓝
ACCENT2    = (0x7C, 0x3A, 0xED)  # 紫色
ACCENT3    = (0x10, 0xB9, 0x81)  # 绿色
ACCENT4    = (0xF5, 0x9E, 0x0B)  # 橙色
WHITE      = (0xFF, 0xFF, 0xFF)
LIGHT_GRAY = (0xCC, 0xCC, 0xCC)
CARD_BG    = (0x25, 0x25, 0x40)  # 卡片背景
```

## 依赖

```bash
pip install python-pptx
```

## 文件结构

```
skills/ppt-generator/
├── SKILL.md           # 本文件
└── scripts/
    └── ppt_lib.py     # 核心工具库（模板函数+调色板）
```
