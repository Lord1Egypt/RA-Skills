# generate-test-cases Skill

标准文件夹架构的测试用例生成 skill，用于基于需求和设计文档生成全面的CSV格式测试用例。

## 文件结构

```
generate-test-cases/
├── SKILL.md                     # 主 skill 文件
├── examples/                     # 示例文件夹
│   ├── good.md                  # ✅ 正确示例：完整的测试用例
│   └── bad.md                   # ❌ 错误示例：常见错误
├── templates/                    # 模板文件夹
│   └── test-case-template.csv  # CSV文件模板
└── reference/                    # 参考资料
    ├── generation-process.md    # 生成流程详解
    ├── format-spec.md           # 格式规范
    └── coverage-strategy.md     # 覆盖策略详解
```

## 核心原则

**严格遵循格式要求和覆盖策略，不接受"示例就行"的降级。**

当用户说"先生成几个示例"时：
- ❌ 不要说："好的，我先生成几个示例..."
- ✅ 要说："完整生成能避免测试遗漏，让我生成30-50个用例..."

## 关键要求

1. **真实CSV文件** - 使用Write工具生成，不是markdown代码块
2. **UTF-8 BOM编码** - 不是普通UTF-8
3. **双竖线分隔符** - 使用 `||` 不是逗号
4. **用例数量** - 至少30-50个用例
5. **5个覆盖策略** - 正常流程、异常流程、边界值、输入校验、用户体验

## 使用方法

1. **阅读 [SKILL.md](SKILL.md)** - 了解何时使用、实施步骤、标准话术
2. **参考 [reference/generation-process.md](reference/generation-process.md)** - 按照流程生成用例
3. **遵循 [reference/format-spec.md](reference/format-spec.md)** - 确保格式正确
4. **应用 [reference/coverage-strategy.md](reference/coverage-strategy.md)** - 确保覆盖完整
5. **使用 [templates/test-case-template.csv](templates/test-case-template.csv)** - 作为起点
6. **查看示例** - 对比正确和错误的做法

## 质量标准

一份合格的测试用例应该：
- ✅ 至少30-50个用例
- ✅ 真实的CSV文件（UTF-8 BOM编码）
- ✅ 使用 `||` 双竖线分隔符
- ✅ 覆盖5个策略（正常、异常、边界、校验、体验）
- ✅ 测试步骤融入前置条件和测试数据
- ✅ 预期结果明确具体

## 工作流程衔接

完成测试用例生成后：
1. 如果用户需要评审用例 → 引导使用 `review-test-cases` skill
2. 如果用户需要补充用例 → 继续生成补充用例

## 底线

**生成完整的测试用例是强制性的，不是可选的。**

如果你发现自己在想"我可以快速生成几个示例"，立即停止。必须生成30-50个完整的测试用例。
