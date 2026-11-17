# 元造 CLI 参考（yotta-skill-creator）

> 配套技能：元造 yotta-skill-creator（零依赖 Python 3.8+）
> 本文档给出 `create` 的完整参数、命名校验规则、结构自检项、退出码与自用模式差异。

## 1. 调用方式

```bash
python3 scripts/yotta_skill_creator.py create <skill-name> --zh 元X --desc "..." [选项]
python3 scripts/yotta_skill_creator.py --version
python3 scripts/yotta_skill_creator.py --help
```

## 2. 参数表

| 参数 | 必需 | 说明 |
|---|---|---|
| `create` | 是（子命令） | 生成技能目录 |
| `skill-name` | 是 | 技能名：`yotta-` 前缀小写连字符，≤ 64 字符 |
| `--zh` | 是 | 中文名：`元X` 规范（以「元」开头，2-8 字符） |
| `--desc` | 是 | SKILL.md 描述：做什么 + 何时触发 + 边界 |
| `--summary` | 否 | README 一句话简介；缺省 = desc |
| `--out` | 否 | 输出父目录；缺省 `.`（生成 `<out>/<name>/`） |
| `--with-cli` | 否 | 同时生成 `scripts/<cli_module>.py` + `test_<cli_module>.py` |
| `--no-banner` | 否 | 跳过 `assets/` 素材目录 |
| `--skip-installer` | 否 | 不生成 install.sh / bin/install.js，并从 package.json 去掉 bin |
| `--self-use` | 否 | 自用模式：只生成技能本体，不生成发布件 |

## 3. 命名校验规则

- slug 正则：`^yotta-[a-z0-9]+(?:-[a-z0-9]+)*$`——`yotta-` 开头；小写字母 / 数字；
  连字符分隔单词；不以连字符结尾；不允许大写。
- 长度 ≤ 64 字符。
- 中文名以「元」开头，2-8 字符（「元」+ 1-7 字）。
- 输出目录 `<out>/<slug>` 已存在 → 拒绝（不覆盖）。

任何一项不满足即返回退出码 2，并在 stderr 打印原因。

## 4. 结构自检项

`create` 结束前自动执行，全部通过才输出「OK: 脚手架合格」：

1. 必需文件齐全（按模式）：完整模式含 SKILL.md / LICENSE / README 中英 /
   CHANGELOG / NOTICE / package.json / .gitignore / .npmignore / publish.yml /
   （未 --skip-installer 时）install.sh + bin/install.js；自用模式含 SKILL.md /
   references；--with-cli 追加 scripts 与测试。
2. frontmatter：`name` 与目录名一致；`description` / `version` / `license` 齐全。
3. 版本对齐：package.json / SKILL.md / CHANGELOG 顶部版本一致。
4. README 中英各含「四方式安装」（npx / git clone / Download ZIP / install.sh）。
5. 无残留占位符（双花括号模板变量）。
6. Markdown 代码围栏配对（三个反引号成对）。

## 5. 退出码

| 退出码 | 含义 |
|---|---|
| 0 | 成功，脚手架合格 |
| 2 | 参数 / 命名 / 自检不通过 |
| 4 | 致命异常 |
| 130 | Ctrl+C 中断 |

## 6. 自用模式差异（--self-use）

| 内容 | 完整模式 | 自用模式 |
|---|---|---|
| SKILL.md | ✅ | ✅ |
| references/ | ✅ | ✅ |
| scripts/（--with-cli） | ✅ | ✅ |
| README.md / README.zh-CN.md | ✅ | ❌ |
| package.json / CHANGELOG.md | ✅ | ❌ |
| LICENSE / NOTICE | ✅ | ❌ |
| install.sh / bin/ | ✅ | ❌ |
| .gitignore / .npmignore | ✅ | ❌ |
| .github/workflows/publish.yml | ✅ | ❌ |
| assets/（--no-banner 跳过） | ✅ | ❌ |

自用模式自检只查技能本体完整性，不要求发布件；输出会提示「自用模式：未生成发布件」，
并说明若要发布需重跑 create（不带 --self-use）或按发布规范补齐发布件后跑 publish-guard check。

## 7. 生成后的下一步

1. 编辑 SKILL.md 正文（触发与边界 / 核心流程 / 渐进披露）；
2. `--with-cli` 时实现 `scripts/<cli_module>.py` 并补测试；
3. 完整模式发布前：用元守（yotta-publish-guard）的 `check` 做发布前检查（按其安装目录运行 `scripts/yotta_publish_guard.py check <技能目录>`）。
