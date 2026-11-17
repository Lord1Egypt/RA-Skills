# 元造中文教程（新手全流程）

> 配套技能：元造 yotta-skill-creator（零依赖 Python 3.8+）
> 目标：从零造一个合规技能目录 → 结构自检通过 → 交给元守做发布前检查。

## 1. 教程目标与前置

- 学会 `create` 的完整用法与选项；
- 理解命名规则与中文名规范（`yotta-` 前缀 + `元X`）；
- 分清完整模式与自用模式；
- 前置：Python 3.8+（无需额外依赖）；一个新技能的名字与一句话定位。

## 2. 快速体验：造一个完整发布版脚手架

```bash
python3 scripts/yotta_skill_creator.py create yotta-demo-tool \
    --zh 元示 --desc "示例技能：演示脚手架。触发：用户说 元示。边界：仅演示。" \
    --summary "元阁示例技能" --with-cli
```

预期输出：`created: .../yotta-demo-tool`、`files: N`、`OK: 脚手架合格，可继续开发`。

## 3. 命名校验：试错示例

```bash
python3 scripts/yotta_skill_creator.py create my-tool --zh 元示 --desc "d" --out .   # [ERROR] 必须以 yotta- 开头
python3 scripts/yotta_skill_creator.py create yotta-Bad  --zh 元示 --desc "d" --out .   # [ERROR] 小写连字符
python3 scripts/yotta_skill_creator.py create yotta-ok   --zh 工具  --desc "d" --out .   # [ERROR] 应以「元」开头
```

命中任一条即退出码 2，不会生成任何文件。

## 4. 查看生成内容

完整模式目录包含：SKILL.md / README.md + README.zh-CN.md / package.json / CHANGELOG.md /
LICENSE / NOTICE / install.sh / bin/install.js / .gitignore / .npmignore /
.github/workflows/publish.yml / references/ / assets/（--with-cli 时还有 scripts/）。

## 5. 编辑 SKILL.md 正文

脚手架 SKILL.md 是骨架：把「一句话」「触发与边界」「核心流程」「渐进披露」替换为真实内容；
`--with-cli` 生成的 CLI 骨架可直接运行（`python3 scripts/yotta_demo_tool.py --version`），
在此基础上实现逻辑并补测试。

## 6. 自用模式

```bash
python3 scripts/yotta_skill_creator.py create yotta-private --zh 元私 \
    --desc "自用技能：内部流程。触发：内部场景。边界：不发布。" --self-use
```

只生成 SKILL.md / references/（--with-cli 时含 scripts/）；输出明确提示「自用模式：未生成发布件」。
自用技能不发布到 GitHub / npm / ClawHub，直接用技能本体即可。

## 7. 结构自检失败怎么办

自检失败会逐行列出 ERROR（缺文件 / 占位符残留 / frontmatter 不一致 / 版本不一致 /
围栏不配对），按行修正后重跑 `create` 或自行补齐。骨架本身自检通过，失败通常来自二次编辑
引入的问题（例如手改后留下双花括号占位符、改坏 frontmatter）。

## 8. 交给元守

```bash
# 完整模式：发布前全量检查（以下命令在元守 yotta-publish-guard 的安装目录内运行）
python3 scripts/yotta_publish_guard.py check <技能目录>

# 自用模式：只查技能本体
python3 scripts/yotta_publish_guard.py check <技能目录> --self-use
```

通过（READY）后再跑 pack / versions / names / publish。

## 9. 常见问题

- **目标目录已存在**：会被拒绝（不覆盖）；换 `--out` 或先改名。
- **中文名规则**：必须以「元」开头，2-8 字符。
- **--desc 不能为空**，且建议写全「做什么 + 何时触发 + 边界」三要素，生成后就是合格的
  SKILL.md 描述。
- **占位符残留**：生成后不应再有双花括号占位符；自检会拦截。
- **自用技能后来想发布**：重跑 create（不带 --self-use）或按发布规范补齐发布件后跑
  publish-guard check。
