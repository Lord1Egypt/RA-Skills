# persona：人设查询与保存（GetPersonas / AddPersona）

对应 Web / MarkAI `getPersonas()`、`addPersona()`：

- 列表：`POST {csoBaseUrl}/cso/v1/platformdata/GetPersonas`，请求体 `{}`
- 新建：`POST {csoBaseUrl}/cso/v1/platformdata/AddPersona`，请求体 `{ personaName, styleGuide, materials: [] }`

返回人设含 **`styleGuide`**（Markdown 风格指南）、`materials`、`taskStatus` 等，供文案与三库工作流使用。

## 命令一：查询人设列表

```text
siluzan-cso persona list [选项]
```

| 选项                  | 说明                                                                                      |
| --------------------- | ----------------------------------------------------------------------------------------- |
| `-t, --token <token>` | 凭据（可选，默认读 `~/.siluzan/config.json`）                                             |
| `--id <id>`           | 只显示指定人设 id                                                                         |
| `--name <text>`       | 按人设名称子串过滤（客户端过滤）                                                          |
| `--json-out <path>`   | 将完整人设（含 `styleGuide`）落盘到目录或 \*.json 文件，stdout 仅一行摘要（防工具死循环） |
| `--no-style-guide`    | 搭配 `--json-out`：省略 `styleGuide`，改输出 `styleGuideChars`（字符数）                  |
| `--unicode`           | 表格使用 Unicode 线框                                                                     |
| `--verbose`           | 打印详细错误                                                                              |

终端表格仅展示 `styleGuide` 摘要；需要全文时用 `--json-out` 落盘后脚本读盘（见 `references/core/tips.md`）。

> **⚠️ 列全量列表用 `--json-out` 落盘即可（不再有截断风险）。** `styleGuide` 通常每条数千字，旧 `--json` 直吐到 stdout 动辄数万字符、
> 极易被宿主 bash 工具从中间截断丢记录——这正是 `--json` 被移除、改 `--json-out` 落盘的原因。
> 正确姿势：先 `persona list --json-out ./snap-cso --no-style-guide` 落盘精简列表（仅含 `styleGuideChars` 长度提示），脚本读盘选中目标后再用
> `persona list --id <id> --json-out ./snap-cso` 单独落盘那一条的完整 `styleGuide`。

`--no-style-guide` 模式下每条记录形如（去掉 `styleGuide`，新增 `styleGuideChars`）：

```json
{ "id": "...", "personaName": "...", "taskStatus": 3, "materials": [], "styleGuideChars": 5837 }
```

## 命令二：保存人设到平台

```text
siluzan-cso persona create --name <名称> ( --style-guide <markdown> | --style-guide-file <path> ) [选项]
```

| 选项                        | 说明                                                                             |
| --------------------------- | -------------------------------------------------------------------------------- |
| `--name <name>`             | **必填**。人设名称，长度上限 60 字符                                             |
| `--style-guide <markdown>`  | 直接传入 styleGuide markdown 内容（与 `--style-guide-file` 二选一）              |
| `--style-guide-file <path>` | 从本地 markdown 文件读取 styleGuide（长文推荐用文件，与 `--style-guide` 二选一） |
| `-t, --token <token>`       | 凭据（可选）                                                                     |
| `--verbose`                 | 打印详细错误                                                                     |

> `persona create` 为写入命令，仅输出简洁人类可读确认（含新建人设 `id`），不再支持 JSON 输出。

> **CLI 不会替你生成 styleGuide**。AI 助手在调用本命令前，应先按
> `three-lib-content-workflow/persona-reverse-sop.md` 的 SOP 把 styleGuide 写好（Markdown 格式），再用
> `--style-guide-file` 把文件喂给 CLI。这样保持 CLI 只做平台持久化、不依赖外部 LLM 的设计。

### 典型用法

1. AI 助手先把 styleGuide 写到临时文件，如 `./tmp-persona.md`
2. 调命令保存：
   ```text
   siluzan-cso persona create --name "外贸老炮" --style-guide-file ./tmp-persona.md
   ```
3. 拿到回包里的 `id`，后续写稿时用 `siluzan-cso persona list --id <id> --json-out ./snap-cso` 落盘后脚本读全文复核。
   （若是「先浏览全部人设再挑一个」，先 `persona list --json-out ./snap-cso --no-style-guide` 落盘精简列表，再按 `--id` 取全文。）

## 字段说明

| 字段                  | 含义                                                       |
| --------------------- | ---------------------------------------------------------- |
| `personaName`         | 人设名称                                                   |
| `styleGuide`          | 风格指南正文（Markdown）                                   |
| `materials`           | 参考素材（文件名、URL 等），新建时固定传空数组             |
| `taskStatus`          | `1` 待生成 · `2` 生成中 · `0`或`3` 生成完成 · `4` 生成失败 |
| `createdDateTime`     | **UTC** 时间字符串                                         |
| `lastChangedDateTime` | **UTC** 时间字符串                                         |

> 时间字段展示前必须做时区转换，详见 SKILL.md 「时间字段输出约定（全局）」。

## 与 Skill 的关系

编写口播/成稿前应先拿到目标人设的 `styleGuide`，再结合 `three-lib-content-workflow/` 中的 SOP。
若用户要求「新建一个人设」，先按 `persona-reverse-sop.md` 反推风格指南、确认无误后再用 `persona create` 写回平台。
详见上级 `SKILL.md`「三库内容工作流」。
