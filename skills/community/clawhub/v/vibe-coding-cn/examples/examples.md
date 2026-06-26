# Vibe Coding 使用示例

## 示例 1: 个税计算器

**命令**:
```bash
vibe-coding "做一个个税计算器"
```

**输出**:
```
output/个税计算器/
├── docs/
│   ├── requirements.md      # 需求文档（6 个功能，3 个用户故事）
│   ├── architecture.md      # 架构设计（技术选型 + 数据模型）
│   └── vibe-report.md       # 总结报告
├── index.html               # 主页面（响应式 UI）
├── taxCalculator.js         # 个税计算引擎
└── app.js                   # 应用主逻辑
```

**功能**:
- 输入月收入、五险一金、起征点
- 自动计算应纳税额
- 显示税率和速算扣除数
- 计算税后收入

---

## 示例 2: 打字游戏

**命令**:
```bash
vibe-coding "做一个打字游戏"
```

**输出**:
```
output/打字游戏/
├── docs/
│   ├── requirements.md
│   └── architecture.md
├── index.html               # 游戏页面（Canvas 渲染）
├── game.js                  # 游戏逻辑
└── app.js                   # 应用主逻辑
```

**功能**:
- 单词从屏幕上方掉落
- 用户输入对应单词
- 计分系统
- 难度递增

---

## 示例 3: 待办事项应用

**命令**:
```bash
vibe-coding "做一个待办事项应用"
```

**输出**:
```
output/待办事项应用/
├── docs/
│   ├── requirements.md
│   └── architecture.md
├── index.html               # 主页面
├── app.js                   # 应用逻辑
└── styles.css               # 样式文件
```

**功能**:
- 添加/删除任务
- 标记完成状态
- 本地存储（localStorage）
- 刷新不丢失数据

---

## 示例 4: Markdown 编辑器

**命令**:
```bash
vibe-coding "做一个 Markdown 编辑器"
```

**输出**:
```
output/markdown 编辑器/
├── docs/
│   ├── requirements.md
│   └── architecture.md
├── index.html               # 编辑器页面
├── editor.js                # 编辑器逻辑
└── preview.js               # 预览渲染
```

**功能**:
- 实时 Markdown 预览
- 本地保存
- 导出 HTML
- 语法高亮

---

## 示例 5: 库存管理系统

**命令**:
```bash
vibe-coding "做一个库存管理系统"
```

**输出**:
```
output/库存管理系统/
├── docs/
│   ├── requirements.md
│   └── architecture.md
├── index.html               # 管理页面
├── inventory.js             # 库存管理
└── app.js                   # 应用主逻辑
```

**功能**:
- 添加/删除商品
- 库存数量管理
- 入库/出库记录
- 库存预警

---

## 执行时间统计

| 项目 | 耗时 | 文件数 | 质量评分 |
|------|------|--------|---------|
| 个税计算器 | 4 分 30 秒 | 5 | 88/100 |
| 打字游戏 | 4 分 15 秒 | 5 | 86/100 |
| 待办事项应用 | 3 分 50 秒 | 5 | 87/100 |
| Markdown 编辑器 | 4 分 45 秒 | 6 | 85/100 |
| 库存管理系统 | 5 分 20 秒 | 7 | 84/100 |

**平均**: 4 分 32 秒，5.6 个文件，86/100 质量评分

---

## 常见问题

### Q: 可以指定输出目录吗？

**A**: 可以，使用环境变量：
```bash
VIBE_OUTPUT=./my-projects vibe-coding "做一个个税计算器"
```

### Q: 可以跳过测试阶段吗？

**A**: 可以，使用环境变量：
```bash
VIBE_SKIP_PHASES=4,5 vibe-coding "做一个个税计算器"
```

### Q: 生成的代码能直接运行吗？

**A**: 可以！打开生成的 `index.html` 即可运行。

### Q: 如何修改生成的代码？

**A**: 直接编辑 `output/{项目名}/` 目录下的文件即可。

---

**更多示例**: 欢迎提交你的创意！
