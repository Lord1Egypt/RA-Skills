# Real API Example

这个目录用于沉淀「真实系统 API」类 skill 的可复制成功案例。

## 适用场景（规划）

- 目标系统提供真实 API
- 需要 token / secret / credential
- 需要请求重试、权限校验、限流处理、schema 校验和幂等写库

## 当前状态：规划占位

- **本目录当前为规划占位**，仅保留最小结构（`README.md`、`scripts/`、`tests/` 占位）。
- **尚未沉淀可复制实现**；目录内无参考代码。
- **AI 编程工具不得**基于空目录自行脑补 API 对接实现。
- 后续补齐可复制案例后，再按 README copy map 选择性复制到新技能 `scripts/`。

## 轻量结构

```text
real_api/
  README.md
  scripts/
    service/
    util/
  tests/
```

不要在本目录添加 `SKILL.md`、市场 README、`references/`、`development/`、`.github/` 等完整 skill 仓库层文件。

## 复制边界（待案例补齐后生效）

- 参考代码将从 `examples/real_api/scripts/` 选择性复制到新技能 `scripts/`
- 根 `README.md`、`SKILL.md`、`references/` 仍按模板主目录规则编写
- 当前阶段：**不可作为实现参考**
