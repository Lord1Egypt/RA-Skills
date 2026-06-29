## [1.6.0] - 2026-06-10

### 修复
- refactor: round-robin-allocator

---

## [1.5.1] - 2026-06-10

### 修复
- 演示输出

---

## [1.5.0] - 2026-06-10

### 修复
- refactor: round-robin-allocator

---

## [1.4.0] - 2026-06-10

### 修复
- refactor: round-robin-allocator

---

## [1.3.0] - 2026-06-10

### 修复
- refactor: round-robin-allocator

---

## [1.2.0] - 2026-06-10

### 修复
- refactor: round-robin-allocator

---

## 1.1.3 (2026-06-10)

### 标准化修复
- 修复 R-23 文档引用说明（Chart.js/Plotly.js 明确为 CDN 依赖）
- 恢复版本一致性（三端同步至 1.1.3）

## 1.1.2 (2026-06-10)

### 标准化完善
- 修复 R-06 H1 不匹配技能名
- 修复 R-16 权限权重缺失
- 创建 references/antipatterns.md（3 条反模式示例）
- 创建 references/faq.md（8 对 Q&A，含三类错误场景分类排错指导）
- 补充 SKILL.md 使用示例为双场景完整交互流程
- 新增「限制与边界」章节，说明输入规模/比例/参数/环境约束

## 1.1.1 (2026-06-10)

### 标准化修正
- skill-standardization 审计修复：frontmatter 补 trigger/trigger_negative、_meta.json 同步、changelog v前缀修正
- 移动 _allocator_config.json 到 .standardization/round-robin-allocator/data/ 标准化目录
- 删除 test_output/ 违规产出物目录
- SKILL.md 渐进式拆分：创建 references/usage.md（使用指南）和 references/algorithm.md（算法说明）
- SKILL.md 从 398 行精简到 87 行，符合 ≤230 行渐进式加载规范
- 修正代码中 R-12 数据目录路径违规，更新 _CONFIG_PATH

## 1.1.0 (2026-06-10)

### 配置系统（代码强制钩子）
- 新增 `_allocator_config.json` 持久化配置：`skip_confirm`（跳过确认）、`default_mode`（默认后处理模式）
- 支持 CLI 选项：`--no-confirm`（本次跳过）、`--always`（永久跳过并写配置）、`--set-default-mode`（设默认模式）
- 配置由脚本在标准化数据目录读取，LLM 无法绕过

### 确认表与交互菜单（全量重构）
- 新增确认表，执行前展示 N/T/K/比例/后处理等参数
- 完整交互菜单：1=确认执行、2=取消、3=永久跳过确认、4-7=切换后处理并立即执行、8=设默认后处理（二级菜单）、9=补充更新参数
- 选项 9 支持自然语言输入补充/更新参数（如 `5套方案，比例7:8:10:3:5`），关键字匹配，不覆盖已有值
- 缺参数时确认表标注「? (缺) 按9补充」，不自动推断或编造 N/K
- 比例不指定则默认等分，确认表明确标注「? (缺)（未指定，默认等分）按9补充」
- 确认表底栏动态显示缺失项（如 `9=补充K`）

### 三路分流 → 统一 3D 路径
- **删除 2D 路径**：N+T 或 T+K 无方案/无对象不再执行 2D 展示，统一路由到 3D 确认表
- 确认表循环：缺 N/K 按 9 补充后自动路由到完整 3D 分配
- 交互模式也校验 N/K 必须齐全

### 后处理模式增强
- 四种后处理：algorithm / random / fair / custom
- random 模式支持 `--seed` 参数
- custom 模式无 `--repeat-ratio` 时自动回退到 fair
- 模式名菜单中文标注：4=ID排序、5=随机打乱、6=均匀分布、7=自定义

### HTML 可视化增强
- 新增 Plotly.js 3D 散点图：XYZ 三轴分配空间映射（X=对象ID, Y=方案编号, Z=轮次, 颜色=覆盖率）
- CDN 从 cdn.plotly.com 切换到 cdn.jsdelivr.net（白名单兼容）
- 覆盖率表新增热力着色

### 输出流程优化
- CSV 不再自动生成，执行完后询问「导出 CSV？(y/n) [n]」
- Markdown 输出格式固定

### 文档与代码重构
- SKILL.md 完整重写，去除旧版 2D 路径说明、推断规则、错误示例
- 新增确认表/菜单/交互示例完整文档
- new file: references/usage.md（使用指南）
- new file: references/algorithm.md（算法说明）
- visualizer.py 重构：3D 散点图替换二维散点图、Plotly CDN 修正、布局优化

## 1.0.2 (2026-05-30)

### 修复
- audit --fix 自动修正
