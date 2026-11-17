# version-decide

> 说明：本 README 是**中文（zh）本地化副本**。技能的默认文档为英文 `SKILL.md`，运行时输出跟随用户语言（en/zh）。English primary docs: `SKILL.md`.

根据代码变更范围判定下一个版本号。面向开发者，尤其是新手开发者。

输出**唯一且明确**的版本号建议，并给出可追溯的依据。

## 为什么需要它

版本号不是标签，是**对下游依赖方作出的兼容性承诺**。猜错一次的成本是别人的线上故障。
新手最常犯的三个错：

1. 改了 README 也发一次版本（版本号通胀，真正的破坏被淹没在噪音里）
2. 0.x 阶段按 SemVer 字面理解，以为 minor 可以随便加（实际上 npm/Cargo 里 minor 就是破坏边界）
3. 废弃了 API 却没升版本（SemVer §7 明确要求必须 minor）

## 快速上手

```bash
# 校验当前版本号
python scripts/semver_check.py check 1.2.3

# 从变更推导下一个版本号
python scripts/semver_check.py analyze 1.2.3 --changes "feat: 新增 JSON 输出" "fix: 修空指针"
# → 1.2.3 -> 1.3.0  [minor]

# 破坏性变更，先发 beta 留迁移窗口
python scripts/semver_check.py analyze 1.4.2 --changes "break: 配置改为 YAML" --pre beta
# → 1.4.2 -> 2.0.0-beta.1  [major]
```

零依赖，Python 3.8+。

## 判定核心

| 变更 | 级别 |
|---|---|
| 移除/重命名公共导出、签名变化、行为改变、删除模块 | **major** |
| 标记废弃、新增公共 API、依赖约束放宽 | **minor** |
| 内部重构、性能优化、修 bug、安全修复（不改 API） | **patch** |
| 文档、测试、CI、格式 | **none**（不需发版） |

同批变更按 major > minor > patch 的优先序判定。`0.x` 阶段采用 npm/Cargo 语义：minor 递增即破坏边界。

## 开发

```bash
python -m unittest test_semver_check -v   # 33 项回归测试
```

## 文档

- `SKILL.md` —— 判定流程（确认 → 定级 → 计算 → 输出）
- `references/standards-comparison.md` —— SemVer 2.0.0 / Conventional Commits / PEP 440 / Cargo / Go / CalVer 官方规则与冲突点
- `references/decision-tables.md` —— 完整判定表、确认清单、边界情况

## 依据

判定依据主要来自下列标准官方条文；其中 0.x npm/Cargo 语义、`security`→patch 等
为本技能自定义的局部默认（非标准，详见 `references/standards-comparison.md`），2026-10 核实：
[SemVer 2.0.0](https://semver.org/spec/v2.0.0.html) ·
[Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) ·
[PEP 440](https://peps.python.org/pep-0440/) ·
[Cargo](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html) ·
[Go Modules](https://go.dev/doc/modules/version-numbers) ·
[PyPA Versioning](https://packaging.python.org/en/latest/discussions/versioning/)

MIT 许可证。
