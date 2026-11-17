# ym-skill-generator · 技能生成器

按一句需求生成合规可用的技能骨架，或把对话里刚实现的功能**体检、脱敏、打包**成可分发、可上架的技能包。

覆盖 WorkBuddy 技能（Skill）从**从零创建**到**交付上架**的完整链路：需求澄清 → 建骨架 → 填内容 → 脱敏 → 体检 → 打包安装。

## 解决什么问题

- **不知道骨架该长什么样** —— 按技能基础结构一次建全：`SKILL.md` / `references/` / `scripts/` / `templates/`
- **上架字段缺斤少两** —— 自动补齐市场分发字段（`description_zh` / `description_en` / `version` / `author` 等）
- **带病打包** —— 打包前自动体检 9 类风险，输出 P0 / P1 / P2 分级报告
- **把不该发的东西发出去了** —— 硬编码路径、明文凭据、内网地址、个人数据自动识别并提示脱敏
- **报错看不懂 / 规则太严** —— 报错带中文「怎么修」；规则可 `--explain` 查含义、`--ignore-rule` 按规则放行
- **改了版本忘了写更新说明** —— `bump.py` 一条命令同时改 version 与版本历史

## 安装

克隆到 WorkBuddy 技能目录即可被识别：

```bash
git clone https://github.com/liuyuming0823/ym-skill-generator.git ~/.workbuddy/skills/ym-skill-generator
```

Windows 路径：`%USERPROFILE%\.workbuddy\skills\ym-skill-generator`

> **技能名（slug）为 `ym-skill-generator`。** 原名 `skill-generator` 已被他人占用，
> 自 v2.1.0 起 `name` / 目录名 / 仓库名三处同步改名。

## 快速开始

```bash
cd ~/.workbuddy/skills/ym-skill-generator

# 从一句需求生成骨架（生成后自动体检，并直接安装到本机技能目录）
python scripts/new_skill.py my-skill \
  --desc "一句话说清做什么/何时触发" \
  --triggers "触发词1,触发词2" \
  --dirs scripts,references \
  --deps requests

# 只体检
python scripts/audit_skill.py <技能目录>

# 体检 + 打包 + 安装（默认就是这条链路）
python scripts/pack_skill.py <技能目录>
```

**退出码（四个脚本统一）**：`0` 成功 · `1` 有 P1 警告 · `2` 有 P0 阻断 · `3` 参数/目录错 · `4` 写入打包失败。
非 0 退出时会打印「怎么修」，不用猜。

## 五个脚本

### `new_skill.py` —— 生成骨架

| 参数 | 说明 |
|------|------|
| `<skill_name>` | 技能名，kebab-case（传中文会提示改用 `--display-name`） |
| `--desc` / `--desc-zh` / `--desc-en` | 描述：做什么 / 何时触发 / 触发词 |
| `--display-name` / `--display-name-en` | 展示名 |
| `--triggers` | 逗号分隔的触发词 |
| `--dirs` | 要创建的目录，默认 `scripts,references` |
| `--deps` | 第三方依赖，会自动生成 `scripts/setup.py`（自带重试与国内镜像兜底） |
| `--config-fields` | 配置字段，会生成 `config/settings.example.json` |
| `--author` / `--category` | 署名与分类，署名默认读 `~/.workbuddy/USER.md` |
| `--mode market\|local` | 按市场规范生成 / 本机自用 |
| `--out` / `--install` / `--force` | 输出目录 / 直接安装 / 覆盖同名（旧版先备份再替换） |
| `--no-audit` / `--json` | 跳过体检 / 输出 JSON |

#### 技能标识（slug）与前缀

标识**默认就是你传的那个名字**，不会自动加任何前缀 —— 生成器是要分发给别人用的，
个人命名习惯不该被写进公共默认值（v2.6.0 起移除了内置的默认前缀）。

想固定用某个标识前缀，自己配一档即可，优先级从高到低：

```bash
export SKILL_NAME_PREFIX="my-"                    # 环境变量
echo '{"name_prefix": "my-"}' > ~/.workbuddy/skill-gen.json   # 或平台根配置
python scripts/new_skill.py oa-todo --prefix "my-"  # 或每次显式传
python scripts/new_skill.py oa-todo --no-prefix     # 优先级最高：明确不加
```

### `audit_skill.py` —— 体检

```bash
python scripts/audit_skill.py <dir>                          # 人读报告
python scripts/audit_skill.py <dir> --market                 # 追加市场分发规范检查（上架前用）
python scripts/audit_skill.py <dir> --json                   # 机器读
python scripts/audit_skill.py <dir> --hide-p2                # 只看要命的
python scripts/audit_skill.py <dir> --ignore-rule 引用缺失   # 按规则放行（可重复）
python scripts/audit_skill.py <dir> --show-noise             # 展开示例/产物路径提示（默认折叠）
python scripts/audit_skill.py <dir> --fix [--write]          # 半自动补 frontmatter 字段
python scripts/audit_skill.py --explain 引用缺失              # 这条规则判什么、怎么改、怎么放行
python scripts/audit_skill.py --selftest                     # 自检体检器本身
```

### `pack_skill.py` —— 体检 + 打包 + 安装

```bash
python scripts/pack_skill.py <dir>               # 默认：技能目录包 + 安装到本机
python scripts/pack_skill.py <dir> --as-plugin   # 插件形态包（插件市场分发用）
python scripts/pack_skill.py <dir> --no-install  # 只出 zip，不安装
python scripts/pack_skill.py <dir> --no-market   # 跳过市场字段检查（本机自用）
python scripts/pack_skill.py <dir> --dry-run     # 只看会打进哪些文件
```

### `bump.py` —— 改版本号（v2.3.0 新增）

```bash
python scripts/bump.py <dir> -m "修了什么"          # 0.1.0 → 0.1.1，并在版本历史顶部插一条
python scripts/bump.py <dir> --minor -m "加了什么"  # 次版本 +1
python scripts/bump.py <dir> --set 3.0.0           # 直接指定
python scripts/bump.py <dir> -m "说明" --dry-run   # 只看会改什么
```

### `make_icon.py` —— 技能图标（512×512 / ≤500KB）

```bash
python scripts/make_icon.py --prompt          # 拿 ImageGen 提示词
python scripts/make_icon.py <生成图>           # 居中裁切 + 清生成标 + 压到 512×512 / ≤500KB
python scripts/make_icon.py --check <图片>    # 上传前合规自查
```

图标**不进技能包、也不放进技能目录**（平台单独收；放进目录会让绑定仓库发布被拒）。
完整流程见 `references/icon-guide.md`。

## 体检的 9 类风险

结构完整性、绝对路径、明文凭据、危险操作、外部依赖、数据模板、文件引用完整性、体积垃圾、市场分发字段。

分级：**P0 阻断**（真实凭据、破坏性操作）/ **P1 警告**（硬编码路径、外部依赖、引用缺失、缺市场必填字段）/ **P2 知情**（命名规范、外部副作用、运行时数据、垃圾文件）。

放行方式，四选一：

| 方式 | 适用 |
|---|---|
| 行尾 `# skill-audit: ignore` | 单行（必须加在被判定的那一行行尾）；**仅限脚本文件** `.py` / `.js` / `.sh` |
| `.skillignore` 写 glob | 整个文件或目录不参与体检与打包 |
| `.skillignore` 写 `rule:规则名` | 按规则永久放行（**文档里确需放行就用这种**） |
| `--ignore-rule 规则名` | 临时放行，不改文件 |

⚠️ **`.md` 文档里禁止用注释形式放行**。文档注释渲染后不可见，第三方安全审计会判为
「隐蔽地指示审计放行」，实测已使技能在 SkillHub 被标 `suspicious`；这条已由体检规则
「文档放行标记」自动拦下。

## 产出形态，别搞混

| 形态 | 结构 | 用途 |
|------|------|------|
| 技能目录包 | 顶层 `{skill-name}/SKILL.md` + `references/` / `scripts/` / `templates/` | 本机包，**也是开放平台技能类目上传包**（不需要任何清单文件） |
| 插件形态包 | `.codebuddy-plugin/plugin.json` + `skills/{技能名}/SKILL.md` | 插件市场分发用，**不能**用于技能上架 |

## 目录结构

```
ym-skill-generator/
├── SKILL.md                      # 技能主文档（完整工作流，约 14.5k 字符）
├── references/
│   ├── checklist.md              # 逐项判定标准与放行条件
│   ├── generation-guide.md       # 骨架生成指引
│   ├── naming-and-discovery.md   # 命名与可发现性
│   ├── sanitize-rules.md         # 脱敏规则
│   ├── icon-guide.md             # 图标流程（512×512 / ≤500KB）
│   ├── publishing.md             # 发布 ≠ 上线、插件形态包、上架阶段的两个坑
│   ├── pitfalls.md               # 低频坑（打包/上架报错时再查）
│   └── CHANGELOG.md              # 完整版本历史（正文只留最近两版）
├── scripts/
│   ├── _friendly.py              # 共用：中文报错、统一退出码、备份、pip 重试（v2.3.0 新增）
│   ├── new_skill.py              # 生成骨架
│   ├── audit_skill.py            # 体检（含 --explain / --ignore-rule / --fix / --selftest）
│   ├── pack_skill.py             # 打包 + 安装
│   ├── bump.py                   # 递增版本 + 写版本历史（v2.3.0 新增）
│   ├── make_icon.py              # 技能图标（512×512 / ≤500KB）
│   └── setup.py                  # 环境自检（Pillow 为可选依赖）
└── templates/
    └── skill-skeleton.md         # SKILL.md 骨架模板
```

## 依赖

核心功能**纯 Python 标准库**，无需安装任何第三方包。

仅「技能图标」能力需要 **Pillow**（可选）：跑 `python scripts/setup.py` 自检，
或 `python scripts/setup.py --install-pillow` 一键安装（失败会自动重试并改用国内镜像）。

## 相关项目

- [expert-packager](https://github.com/liuyuming0823/expert-packager) —— 配套的**专家**生成器：生成、校验、安装、打包 WorkBuddy 专家包

这对工具的分工是：**ym-skill-generator 管「技能」，expert-packager 管「专家」**，两条上传规范不复用，别混。
