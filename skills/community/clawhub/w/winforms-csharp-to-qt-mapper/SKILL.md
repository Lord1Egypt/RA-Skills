---
name: winforms-to-qt-mapper
description: |
  提供完整的C# WinForms到Qt C++迁移指导,包括架构分析、控件映射、事件转换、布局迁移、性能优化和测试验证。适用于从单体WinForms应用重构为分层Qt架构的企业级项目。

  使用时机:
  - 需要将WinForms应用迁移到Qt框架时
  - 需要设计Qt分层架构和接口层时
  - 需要分析WinForms项目并识别迁移策略时
  - 需要转换C#事件处理到Qt信号槽时
  - 需要优化Qt项目性能时
  - 需要建立Qt测试体系时

  基于企业级项目迁移实战经验:
  - 完整的MainControlWrapper接口设计
  - 全面的测试用例覆盖
  - 显著性能提升
  - 零编译错误,零链接错误
  - 完整的架构分析和优化策略
  - UI 100%一致性验证方法
---

# WinForms到Qt迁移工具

## 快速开始

### 场景A: 全新项目迁移

```bash
# 1. 分析WinForms项目架构
node scripts/architecture_analyzer.js --project <路径> --output <文件>

# 2. 生成迁移计划
node scripts/migration_planner.js --analysis <分析结果> --output <计划文件>

# 3. 生成Qt代码
node scripts/code_generator.js --mapping <映射文件> --output <目录>
```

### 场景B: 架构重构

```bash
# 1. 设计分层架构
node scripts/layered_architect.js --project <路径> --output <设计文件>

# 2. 创建接口层
node scripts/interface_generator.js --analysis <分析结果> --output <目录>

# 3. 性能优化
node scripts/performance_optimizer.js --project <路径> --output <优化建议>
```

### 场景C: 现有项目优化

```bash
# 1. 性能分析
node scripts/performance_analyzer.js --project <路径> --output <分析报告>

# 2. 测试生成
node scripts/test_generator.js --project <路径> --output <测试目录>
```

## 核心功能

### 1. 架构分析

**功能**: 分析WinForms单体架构,识别依赖关系和复杂度

**输出**:
- 依赖图和复杂度分析
- 重构建议和优先级
- 接口层设计方案

**详细指南**: [architecture_analysis.md](references/architecture_analysis.md)

### 2. 接口层生成

**功能**: 生成MainControlWrapper接口层代码

**特性**:
- 标准接口分类(初始化/控制、数据获取、配置管理等)
- 接口命名规范
- 测试框架自动生成

**详细指南**: [interface_layer.md](references/interface_layer.md)

### 3. 代码转换

**功能**: WinForms代码到Qt代码的转换

**包含**:
- 控件映射 → [control_mapping.md](references/control_mapping.md)
- 事件转换 → [event_conversion.md](references/event_conversion.md)
- 布局迁移 → [layout_migration.md](references/layout_migration.md)

### 4. 性能优化

**功能**: Qt项目性能分析和优化

**优化策略**:
- 延迟加载策略
- UI刷新优化
- OpenGL加速
- 缓存机制设计

**详细指南**: [performance_optimization.md](references/performance_optimization.md)

### 5. 测试验证

**功能**: 完整的测试体系建立

**覆盖范围**:
- 完整的测试用例分类(单元测试、接口测试、集成测试、UI测试、性能测试)
- Google Test框架使用
- 测试覆盖率目标(>90%)

**详细指南**: [testing_strategy.md](references/testing_strategy.md)

## 迁移工作流程

### 阶段1: 需求分析和UI清单

```bash
# 1. 分析WinForms项目架构
node scripts/architecture_analyzer.js --project <路径> --output analysis.json

# 2. 建立UI功能清单(重要!)
node scripts/ui_inventory.js --project <路径> --output ui_inventory.json

# 3. 生成迁移计划
node scripts/migration_planner.js --analysis analysis.json --ui ui_inventory.json --output plan.json

# 4. 输出内容:
#    - 项目结构分析
#    - UI功能清单(字体、布局、颜色、交互等)
#    - 控件和事件清单
#    - 依赖关系图
#    - 复杂度评估
```

**重要提示**: UI功能清单是实现100% UI一致性的基础,详见 [UI功能清单文档](references/ui_inventory_checklist.md)

### 阶段2: 设计规划

```bash
# 1. 设计分层架构
node scripts/layered_architect.js --analysis analysis.json --output architecture.json

# 2. 生成接口层
node scripts/interface_generator.js --analysis analysis.json --output interface/

# 3. 输出内容:
#    - 分层架构设计
#    - 接口层定义
#    - 数据模型设计
#    - 性能优化策略
```

### 阶段3: 代码转换

```bash
# 1. 生成Qt项目基础
node scripts/code_generator.js --mapping plan.json --output QtProject/

# 2. 转换控件和属性
node scripts/control_mapper.js --mapping plan.json --output QtProject/

# 3. 转换事件处理
node scripts/event_converter.js --mapping plan.json --output QtProject/

# 4. 迁移布局系统
node scripts/layout_migrator.js --mapping plan.json --output QtProject/
```

### 阶段4: UI一致性验证(重要!)

```bash
# 1. 像素级UI对比
node scripts/ui_compare.js --winforms WinFormsApp/ --qt QtProject/ --output ui_diff.json

# 2. 字体和颜色验证
node scripts/validate_styles.js --project QtProject/ --inventory ui_inventory.json --output style_validation.json

# 3. 交互行为验证
node scripts/validate_interactions.js --project QtProject/ --output interaction_report.json

# 4. 可折叠/隐藏功能验证
node scripts/validate_collapsible_ui.js --project QtProject/ --output collapsible_report.json
```

**验证标准**: 详见 [UI一致性验证清单](references/ui_inventory_checklist.md)

### 阶段5: 测试验证

```bash
# 1. 生成测试代码
node scripts/test_generator.js --project QtProject/ --output tests/

# 2. 验证迁移结果
node scripts/validate_migration.js --qt-project QtProject/ --winforms-project WinFormsProject/

# 3. 性能测试
node scripts/performance_tester.js --project QtProject/ --output perf_report.json

# 4. 输出内容:
#    - 测试用例报告
#    - 覆盖率分析
#    - 性能对比
#    - 回归测试结果
```

## 常用命令速查

### 架构分析

```bash
# 完整分析
node scripts/architecture_analyzer.js --project ./WinFormsApp --output analysis.json

# 仅分析依赖
node scripts/architecture_analyzer.js --project ./WinFormsApp --type dependencies --output deps.json

# 仅分析复杂度
node scripts/architecture_analyzer.js --project ./WinFormsApp --type complexity --output complexity.json
```

### 代码生成

```bash
# 生成完整项目
node scripts/code_generator.js --mapping mapping.json --output QtApp/

# 仅生成接口层
node scripts/interface_generator.js --analysis analysis.json --output interface/

# 仅生成测试
node scripts/test_generator.js --project QtApp/ --output tests/
```

### 验证和优化

```bash
# 验证迁移
node scripts/validate_migration.js --qt-project QtApp/ --winforms-project WinFormsApp/

# 性能分析
node scripts/performance_analyzer.js --project QtApp/ --output perf_analysis.json

# 优化建议
node scripts/performance_optimizer.js --analysis perf_analysis.json --output optimization.json
```

## 参考文档索引

详细的迁移指南请查看 [references/](references/) 目录:

### 架构设计
- [架构分析完整指南](references/architecture_analysis.md) - WinForms架构分析和评估
- [分层架构设计](references/layered_architecture.md) - Qt分层架构设计方法
- [接口层设计](references/interface_layer.md) - MainControlWrapper接口层设计

### 代码转换
- [控件映射参考](references/control_mapping.md) - WinForms到Qt控件映射
- [事件转换指南](references/event_conversion.md) - C#事件到Qt信号槽转换
- [布局迁移指南](references/layout_migration.md) - 布局系统迁移
- [数据绑定转换](references/data_binding.md) - 数据绑定到Model/View转换

### 高级主题
- [内存管理](references/memory_management.md) - C#到C++内存管理转换
- [多线程转换](references/threading.md) - C#多线程到Qt多线程转换
- [DLL集成](references/dll_integration.md) - DLL集成方案(显式加载)

### 性能和测试
- [性能分析](references/performance_analysis.md) - 性能分析方法
- [性能优化](references/performance_optimization.md) - 性能优化策略(+47%提升经验)
- [测试策略](references/testing_strategy.md) - 测试策略(172个测试用例经验)
- [测试生成](references/test_generation.md) - 测试代码生成

### 问题解决
- [编译问题解决](references/compilation_issues.md) - 编译问题解决
- [常见问题](references/troubleshooting.md) - 常见问题解决
- [最佳实践](references/best_practices.md) - 最佳实践总结

### UI一致性(重要!)
- [UI功能清单](references/ui_inventory_checklist.md) - 迁移前UI清单和验证方法
- [UI差异对比](references/ui_differences.md) - WinForms vs Qt UI差异详细对比
- [可折叠UI实现](references/collapsible_ui.md) - 可折叠/隐藏UI组件实现指南

## 模板和示例

### 项目模板

```bash
# Qt项目模板
assets/templates/qt-project-template/

# 接口层模板
assets/templates/interface-layer-template/

# 测试模板
assets/templates/test-template/
```

### 示例代码

- [控件映射示例](examples/control_mapping/)
- [事件转换示例](examples/event_conversion/)
- [布局迁移示例](examples/layout_migration/)
- [性能优化示例](examples/performance_optimization/)

## 技术支持

### 文档
- [故障排除指南](references/troubleshooting.md)
- [FAQ](references/faq.md)
- [术语表](references/glossary.md)

### 示例
- [完整项目示例](examples/)
- [UI一致性示例](examples/ui_consistency/)
- [可折叠UI示例](examples/collapsible_ui/)

### 外部资源
- [Qt官方文档](https://doc.qt.io/)
- [Qt控件参考](https://doc.qt.io/qt-5/widget-classes.html)
- [信号和槽机制](https://doc.qt.io/qt-5/signalsandslots.html)
- [布局管理系统](https://doc.qt.io/qt-5/layout.html)

---

## UI 100%一致性验证指南

### 验证流程

```
迁移前
  ↓
建立UI功能清单 ← [ui_inventory_checklist.md]
  ↓
迁移实现
  ↓
像素级UI对比 ← [ui_differences.md]
  ↓
字体和颜色验证
  ↓
交互行为验证
  ↓
可折叠/隐藏功能验证 ← [collapsible_ui.md]
  ↓
100%一致 ✅
```

### 必须验证的内容

#### 1. 外观一致性
- ✅ 控件尺寸(像素级)
- ✅ 控件间距(像素级)
- ✅ 字体、颜色、样式
- ✅ 图标、图片显示
- ✅ 控件边框、圆角

#### 2. 布局一致性
- ✅ 窗体初始大小
- ✅ 控件初始位置
- ✅ 响应式缩放行为
- ✅ 最小/最大尺寸
- ✅ 停靠行为

#### 3. 交互一致性
- ✅ 鼠标事件响应
- ✅ 键盘快捷键
- ✅ Tab顺序
- ✅ 焦点行为
- ✅ 拖拽行为

#### 4. 可折叠/隐藏功能
- ✅ 面板折叠/展开
- ✅ 标签页动态管理
- ✅ 菜单项动态控制
- ✅ 工具栏状态切换

### 验证工具

- **Screen Ruler**: 像素级测量
- **PixPick**: 取色器
- **Snipaste**: 截图对比
- **PyAutoGUI**: 自动化截图对比

### 常见差异修复

| 差异 | WinForms | Qt | 修复方法 |
|------|----------|----|---------|
| 按钮圆角 | 0px | 2-4px | `border-radius: 0px` |
| 表格行高 | 23px | 21px | `setDefaultSectionSize(23)` |
| 滚动条宽度 | 17px | 16px | `setStyleSheet("width: 17px")` |

---

**重要提示**: 本Skill提供的是**迁移指导和辅助工具**,无法实现100%自动化转换。重要的业务逻辑、复杂交互和性能优化需要人工审查和调整。

**UI一致性**: 实现100% UI一致性需要严格遵循[UI功能清单](references/ui_inventory_checklist.md),进行像素级验证,特别是字体、布局、颜色和可折叠/隐藏功能的细节对比。