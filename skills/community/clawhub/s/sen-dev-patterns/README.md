# Sen 开发提效 Skill

> 让AI Agent理解你的开发习惯，跨项目复用规范、样式、模块和算法

## 核心亮点

| 亮点 | 说明 |
|------|------|
| **满意度加权公式** | 内置集团口径的目标L值计算公式 |
| **水晶质感UI** | 完整的水晶渐变按钮、日志区域、状态栏样式 |
| **跨平台适配** | 自动识别Windows/Mac字体、路径分隔符 |
| **踩坑即记录** | 每次踩坑后立即沉淀，避免重复犯错 |
| **质量评分9.0** | 经过3轮Skill Vetter评估优化 |

---

## 适用场景

- 开发新的桌面应用时复用UI样式和模块
- 需要调用已验证的计算口径（如满意度加权公式）
- 保持跨项目的一致性（样式、规范、命名）
- 快速初始化新的Worker/工具模块

---

## 目录结构

```
sen-dev-patterns/
├── SKILL.md                    # Skill主文件
├── README.md                   # 本文件（市场展示页）
├── references/                 # 参考文档库
│   ├── ui-style-guide.md       # UI样式规范（桌面+Web）
│   ├── coding-standards.md     # 编程规范（最小改动原则）
│   ├── algorithm-library.md    # 算法计算口径库
│   │                              # ⭐ 满意度加权公式（集团口径）
│   │                              # ⭐ 同比/环比/转化率/排名计算
│   ├── pitfalls-record.md      # 踩坑记录
│   ├── code-modules.md          # 代码模块库（日志/文件/GUI）
│   ├── icon-library.md          # 图标库（Emoji/SVG/按钮）
│   ├── performance-guide.md     # 性能优化指南
│   ├── git-workflow.md         # Git工作流与备份规范
│   └── evaluation-report.md     # 质量评估报告
└── scripts/
    └── init_module.py          # 初始化标准模块
```

---

## 快速开始

### 1. 复用UI样式

```python
# 复制水晶质感按钮样式
button_style = """
    QPushButton {
        color: #ffffff;
        border-radius: 16px;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #667eea, stop:1 #764ba2);
    }
"""
```

### 2. 调用计算口径

```python
# 计算目标L值（满意度加权公式）
z_val = 5      # 期末值
aa_val = 3    # 期初值
ab_val = 8    # 目标值

# 公式: L = z + (aa/z)^0.5 * (ab-z)
result = z + (aa/z)**0.5 * (ab - z)
```

### 3. 初始化新模块

```bash
# 初始化Worker
python scripts/init_module.py --type worker --name MyWorker

# 初始化工具模块
python scripts/init_module.py --type util --name DateHelper

# 初始化应用
python scripts/init_module.py --type app --name MyApp --app-title "我的应用"
```

---

## 核心算法库

### 1. 满意度加权公式（集团口径）

**用途**: 计算目标L值，综合考虑期初、期末和目标

```python
def calc_target_l(z_val, aa_val, ab_val):
    """
    满意度加权公式
    z: 期末值
    aa: 期初值
    ab: 目标值
    """
    return z_val + (aa_val / z_val) ** 0.5 * (ab_val - z_val)
```

### 2. 同比/环比/转化率

| 指标 | 公式 | 用途 |
|------|------|------|
| 同比增长率 | `(本期/去年同期-1)*100%` | 年对比 |
| 环比增长率 | `(本期/上期-1)*100%` | 月/周对比 |
| 转化率 | `(转化数/点击数)*100%` | 漏斗分析 |

### 3. 排名计算

```python
def calc_rank(data, value, order='desc'):
    """计算排名，order='desc'降序，'asc'升序"""
    sorted_data = sorted(data, reverse=(order == 'desc'))
    return sorted_data.index(value) + 1
```

---

## 编程原则

### 最小改动原则

1. **只改需要改的地方** - 需求变更时，只修改与当前问题相关的最少代码行
2. **禁止重构** - 不主动重构已验证正确的代码
3. **禁止优化无关代码** - 不要借机优化其他代码

### 已正确部分绝对不动

- 若明确说明某部分逻辑正确，必须严格保护
- 不得修改变量名、结构、顺序、注释和格式

---

## UI配色方案

| 用途 | 颜色 | 说明 |
|------|------|------|
| 主色调 | `#667eea → #764ba2` | 渐变色，标题、重要按钮 |
| 成功色 | `#48bb78` / `#68d391` | 绿色，成功、完成 |
| 警告色 | `#f6ad55` / `#ff9500` | 橙色，进度、警告 |
| 错误色 | `#fc8181` / `#e74c3c` | 红色，错误、失败 |
| 信息色 | `#63b3ed` / `#3498db` | 蓝色，信息、链接 |
| 背景色 | `#f0f5f9` | 浅色背景 |
| 日志背景 | `#1a202c` | 深色日志区域 |

---

## 维护指南

### 添加新的踩坑记录

1. 打开 `references/pitfalls-record.md`
2. 按模板添加新章节
3. 包含：问题描述、原因分析、解决方案、预防措施

### 添加新的算法

1. 打开 `references/algorithm-library.md`
2. 按模板添加新算法
3. 包含：公式、代码实现、使用示例

---

## 更新日志

| 日期 | 版本 | 更新内容 |
|------|------|----------|
| 2026-04-24 | v1.3 | 添加Web开发规范、Git工作流与备份规范 |
| 2026-04-24 | v1.2 | 添加同比/环比/转化率算法、性能优化指南 |
| 2026-04-24 | v1.1 | 添加代码模块库、图标库 |
| 2026-04-24 | v1.0 | 初始版本 |

---

## 作者

- **开发者**: 很拽的猪
- **项目位置**: `D:\自动化项目\`

## 许可证

MIT License - 自由使用和修改
