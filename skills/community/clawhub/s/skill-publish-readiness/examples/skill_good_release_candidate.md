# 示例：同一候选的 quick 与 deep 审查

## 输入

`skills/release-note-writer/` 包含 `SKILL.md`、`CHANGELOG.md`、`examples/`、`templates/`；frontmatter 有稳定 slug、展示名、版本和实际使用的依赖声明。

## auto 选择

用户说“最后帮我快速看一眼能不能发”，因此 auto 选择 quick。

## quick 输出

- 实际模式：quick
- 结论：可以发
- 证据：frontmatter 可解析；名称、slug、版本一致；摘要点明发布说明场景；示例与 CHANGELOG 存在；未发现明显凭据
- 关键问题：无阻塞项
- 下一步：建议执行带显式 `--slug`、`--name`、`--dry-run` 的命令

## deep 输出

当用户改为要求“完整安全与一致性报告”时，执行 deep：

- 逐项核对正文、示例、模板和 `_meta.json`
- 检查依赖、环境变量、敏感值、缓存文件和输入路径
- 差异化评分：20/25
- 结论：可以发；仍须把 dry-run、registry 和安装结果作为不同证据层记录

## 要点

quick 用于决策闸门，deep 用于可追溯审查；两者不能把未执行的 dry-run 写成已通过。
