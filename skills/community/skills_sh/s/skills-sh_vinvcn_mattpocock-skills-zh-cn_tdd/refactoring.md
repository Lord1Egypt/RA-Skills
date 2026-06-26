# Refactor Candidates

TDD cycle 后寻找：

- **Duplication** → Extract function/class
- **Long methods** → 拆成 private helpers（tests 仍保持在 public interface 上）
- **Shallow modules** → 合并或 deepen
- **Feature envy** → 把逻辑移到数据所在处
- **Primitive obsession** → 引入 value objects
- 新代码暴露出有问题的 **Existing code**
