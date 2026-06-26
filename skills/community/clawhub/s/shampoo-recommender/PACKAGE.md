# 娜可露露洗发水推荐助手 - 打包说明

## Skill 信息

- **名称**: shampoo-recommender
- **版本**: 1.0.0
- **描述**: 娜可露露洗发水专业推荐助手，根据发质、头皮问题、使用场景和价格区间进行精准推荐

## 文件清单

```
shampoo-recommender/
├── SKILL.md                      # 主文件（必须）
├── PACKAGE.md                    # 打包说明
├── SETUP_GUIDE.md               # 设置指南
├── references/
│   ├── products.md               # 产品线参考
│   ├── faq.md                    # 常见问题解答
│   └── examples.md               # 使用示例
├── scripts/
│   ├── card_generator.py         # 推荐卡片生成器
│   ├── setup_assets.py           # 资源生成脚本
│   ├── test_skill.py             # 测试脚本
│   └── package_skill.py          # 打包脚本
└── assets/
    ├── README.md                 # 图片资源说明
    ├── images/                   # 产品广告图（已创建，待填充）
    ├── templates/                # 推荐卡片模板（已创建，待填充）
    └── mockups/                  # 产品Mockup（已创建，待填充）
```

## 安装方法

### 方法 1：直接复制到 Skills 目录

将 `shampoo-recommender/` 文件夹复制到 OpenClaw 的 skills 目录：

```
# Windows
%USERPROFILE%\.qclaw\workspace\skills\shampoo-recommender\

# 或 QClaw 安装目录
C:\Program Files\QClaw\resources\openclaw\config\skills\shampoo-recommender\
```

### 方法 2：打包为 .zip 文件

```bash
# 在 shampoo-recommender 目录外执行
zip -r shampoo-recommender.zip shampoo-recommender/

# 或使用 PowerShell
Compress-Archive -Path "shampoo-recommender" -DestinationPath "shampoo-recommender.zip"
```

## 使用方法

### 触发词

当用户说以下任意内容时触发：
- "洗发水"
- "推荐洗发水"
- "给我推荐洗发水"
- "什么洗发水好用"
- "娜可露露"
- "游泳洗头"
- "海边游泳"
- "去氯"
- 等等...

### 推荐流程

1. 收集信息：使用场景 → 发质 → 头皮问题 → 价格区间
2. 分析匹配：根据多维度条件筛选产品
3. 输出推荐：专业顾问式格式（分析+推荐+建议+价格）

### 测试 Skill

```bash
python scripts/test_skill.py
```

### 生成资源文件

```bash
python scripts/setup_assets.py
```

## 功能特性

- ✅ 7 款娜可露露洗发水产品推荐
- ✅ 多维度推荐（发质 × 头皮问题 × 场景 × 价格）
- ✅ 游泳场景专项推荐（去氯修护）
- ✅ 专业顾问式对话风格
- ✅ FAQ 常见问题解答
- ✅ 使用示例参考
- ✅ 推荐卡片生成器
- ✅ 完整测试覆盖

## 后续完善建议

1. **补充真实产品信息**
   - 更新 `references/products.md` 中的真实 SKU、价格、成分
   - 添加娜可露露官方产品图片到 `assets/images/`

2. **扩展功能**
   - 添加用户评价/反馈收集
   - 集成电商链接（如有）
   - 添加产品对比功能

3. **优化体验**
   - 根据用户使用数据优化推荐算法
   - 添加更多使用场景（如孕妇、儿童等特殊人群）

## 技术依赖

- Python 3.7+
- Pillow（用于图片生成）

## 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | 2026-03-21 | 初始版本，包含7款产品、游泳场景、FAQ、使用示例、测试脚本、卡片生成器 |

## 作者

- 创建者: OpenClaw Assistant
- 维护: 待补充
