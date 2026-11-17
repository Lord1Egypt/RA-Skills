# refining-the-tone-of-ai

一个面向中文写作的 Agent Skill，用于减少模板化、机械化和过度润色造成的“AI 味”，同时保留原文的事实、立场、文体、约束和作者声音。

它遵循“保留优先”的编辑原则：先确定不能改变的内容，再判断具体表达是否确有问题，最后以尽可能小的改动完成精修。它不会为了显得“像人写的”而随机替换同义词、强行口语化、故意制造粗糙感或编造个人经历。

## 主要能力

- 识别并调整模板化的二分句、总结腔、助手路标词和机械排比。
- 区分应当修改的套话与必须保留的逻辑结构。
- 保留数字、名称、术语、引文、证据强度、因果方向、操作顺序、限定语和固定提法。
- 针对社交文案、公共写作、邮件、学术或技术文本、小说、SOP、政论评论与公文等文体采取不同策略。
- 默认只返回修改稿；用户要求时可提供诊断、对照或修改说明。判断需要调整结构而用户没有要求时，先提问，不先交局部修改稿。
- 提供可选的本地模式审计脚本，便于批量发现值得人工复核的表达。

## 适用场景

当中文文本出现以下问题时，可以使用本 Skill：

- 频繁出现“不是 A，而是 B”“真正重要的是”“总的来说”等固定句壳。
- 段落结构过于整齐，句式和节奏重复，主次关系被机械排比抹平。
- 文本带有明显的助手导航语，例如“下面我们来”“接下来我会”“希望这能帮到你”。
- 社交文案过度包装，学术文本拔高结论，小说叙述依赖程式化修饰语。
- 需要“去 AI 味”“降低 AI 感”“改得更像人写”，同时又不能改变事实和文体。

以下任务不属于本 Skill 的目标：

- 承诺绕过 AI 检测器或降低某个 AIGC 分数。
- 掩盖抄袭、伪造作者身份、编造引用或个人经历。
- 把模式审计结果当作原创性、写作质量或作者身份的证明。

## 安装

推荐安装到跨运行时可发现的 `.agents/skills` 目录，Codex、Kimi Code 等客户端均可自动识别。

### PowerShell

```powershell
git clone https://github.com/fyihang/refining-the-tone-of-ai.git "$env:USERPROFILE\.agents\skills\refining-the-tone-of-ai"
```

### Bash

```bash
git clone https://github.com/fyihang/refining-the-tone-of-ai.git ~/.agents/skills/refining-the-tone-of-ai
```

安装后新建会话或重启客户端，让 Skill 被重新发现。

更新现有安装：

```powershell
git -C "$env:USERPROFILE\.agents\skills\refining-the-tone-of-ai" pull --ff-only
```

## 使用方法

### 自然语言触发

直接描述修改目标即可，例如：

```text
请把这段中文改得自然一些，去掉模板化 AI 语气，但不要改变事实、数字和结论强度。
```

```text
请降低这封邮件的 AI 感，保留时间、附件名称和事项顺序，只返回修改后的正文。
```

### 显式调用

需要明确指定 Skill 时，在提示词中使用：

```text
使用 $refining-the-tone-of-ai 精修下面的中文技术说明，保留术语、引用、限制条件和因果关系。
```

### 按文体使用

| 文体 | 示例提示词 | 重点保留内容 |
|---|---|---|
| 社交文案 | `使用 $refining-the-tone-of-ai 精修这段社交平台文案，不要虚构经历，也不要增加结尾提问。` | 日期、数字、行动信息、必要的 CTA |
| 公共写作 | `去掉这篇文章的模板化表达，保留作者立场和原有语气。` | 立场、论证关系、作者声音 |
| 学术或技术文本 | `精修这段技术说明，保留术语、变量、引文和证据强度。` | 术语、数据、引用、限制条件、相关与因果的区别 |
| 邮件 | `降低邮件的 AI 感，保留截止时间、附件名称和任务顺序，只返回正文。` | 时间、对象、事项顺序、行动要求 |
| 小说 | `清理这段小说叙述中的程式化修饰语，保留情节、对白意图和人物声音。` | 场景连续性、时间线、对白、人物语气 |
| SOP | `优化这份操作说明的表达，但不得删除影响安全或结果的步骤依赖。` | 操作顺序、安全条件、前置依赖 |
| 政论、评论与公文 | `使用 $refining-the-tone-of-ai 精修这篇评论，保留固定提法、引语和作者立场，不要套用口号式结尾。` | 固定提法、文件名、引语及出处、限定句、公文格式 |

## 编辑原则

修改文本时遵循以下顺序：

1. 提取不能改变的内容：事实、数字、名称、术语、引文、因果方向、证据强度、限定语和已写明的限度、必须保留的行动顺序，以及固定提法。固定提法包括出自文件或会议的规范表述和编号式政策简称、`《》`中的文件名、法律名和书名，以及栏目或系列名称。除非用户要求，否则逐字保留，不扩写、不缩写、不调序、不改写。
2. 判断文本属于哪种文体及其正式程度。
3. 根据上下文识别具体问题，不把固定词语机械地视为删除目标。
4. 优先进行局部修改；只有段落结构本身造成问题时才重写整段。未经要求不跨段移动；若需要改结构而用户没有提出，先问，不先交局部修改稿。
5. 将修改稿与原文逐项核对，恢复任何未经授权发生的内容变化。
6. 按用户要求输出；默认不附加诊断或修改说明。

“不是 A，而是 B”只在 A 于原文、题目、用户要求、明确的读者疑问或文中交代了出处的说法中都找不到来源时才删去，删去后 B 不变。引语、对白，以及原文本来就要陈述的事实（例如已交代的排除原因或情节）保留；“何谓 X？不是……”里只为释义而举出的另一义项不算来源。写得“像某家报纸”不是目标；评论写作中的设问立答、划定边界等手法，只能调动原文已有的材料；需要跨段调整结构时会先征求你的意见，且不先交一版局部修改稿。

例如，“核心在于”如果只是拔高普通判断，可以改写；如果它表达精确的技术定义，则应当保留。类似地，“先 A，再 B”如果只是形式化排列，可以简化；如果它代表操作依赖、时间顺序或证词内容，则不能删除。

## 模式审计脚本

`scripts/audit_ai_flavor.py` 可以扫描文本文件、目录、glob 或标准输入。脚本仅标记已配置的表达模式，不能代替人工编辑判断。

### 基本扫描

```powershell
python .\scripts\audit_ai_flavor.py .\draft.md --profile general
```

### 扫描目录或 glob

```powershell
python .\scripts\audit_ai_flavor.py .\drafts --profile academic
python .\scripts\audit_ai_flavor.py ".\drafts\*.md" --profile social
```

目录扫描默认只读取该目录中的文本文件，不会进入子目录。需要连同子目录一起扫描时，加上 `--recursive`。

固定提法可以写进文本文件，一行一条，扫描时加上 `--keep-terms FILE`。空行和以 `#` 开头的行会跳过。列出的字串按原文逐字豁免：整段落在该字串里的命中不再报出；四字顿号链会先遮住这些字串，所以链中间的固定提法会把链打断。这不给 JSON 增加字段，`schema_version` 仍为 `1`。

### 从标准输入读取并输出 JSON

```powershell
Get-Content .\draft.md -Raw | python .\scripts\audit_ai_flavor.py --stdin --profile general --json
```

JSON 输出包含 `schema_version`、`profile`、判定语义和逐文档结果。当前 schema 版本为 `1`。

### 在自动化流程中使用

```powershell
python .\scripts\audit_ai_flavor.py .\drafts --profile general --fail-on-review
```

退出码：

| 退出码 | 含义 |
|---:|---|
| `0` | 命令成功；未启用 `--fail-on-review`，或没有文档需要复核 |
| `1` | 启用了 `--fail-on-review`，且至少一个文档判定为 `review` |
| `2` | 输入路径、glob 或标准输入等参数存在错误 |

判定规则：满足任一条件即为 `review`：总分 ≥ 4；3 级命中 ≥ 2 处；同一规则中严重度 ≥ 2 的命中 ≥ 2 处。否则为 `clear`。此前单个 3 级命中、总分大于 2、或任一规则命中 2 次即判 `review`，现已放宽。`--fail-on-review` 是否返回退出码 `1` 跟随这一判定，因此同样放宽。JSON 的字段和 `schema_version`（仍为 `1`）不变。

“二分对照壳”（`binary_contrast`）在所有 profile 下都是 0 级：命中仍出现在文本输出和 JSON 的 `findings` 里，并计入 `finding_count`，但不计入总分，也不参与上面的复核条件。严重度为 0 的重复命中不会因为同一规则出现两次而触发 `review`。是否属于“虚空打靶”需要结合全文和你的要求判断，脚本无法可靠识别。操作规程 profile 里严重度为 0 的“机械先后顺序”使用同一套计分方式。

可用 Profile：

| Profile | 用途 |
|---|---|
| `general` | 通用中文文本 |
| `social` | 社交平台和传播文案 |
| `academic` | 学术及技术文本 |
| `fiction` | 小说和叙事文本 |
| `sop` | 操作规程、教程和步骤说明 |
| `email` | 邮件与事务性沟通 |
| `editorial` | 社论、评论、理论文章与公文 |

`general` 下每一处用 `……` 收束的列举各记 1 分，评论里若有多处，总分可以达到 `review`。评论和公文请用 `--profile editorial`。

`clear` 表示没有达到上述复核条件，不代表文本质量合格、内容原创或由人类创作。`review` 只表示值得对照编辑规则再看一遍，同样不是质量或作者身份判断。

查看完整命令参数：

```powershell
python .\scripts\audit_ai_flavor.py --help
```

## 项目结构

```text
refining-the-tone-of-ai/
├── SKILL.md                       # Skill 的核心行为说明
├── agents/openai.yaml             # 显示名称、简介和默认调用提示
├── scripts/audit_ai_flavor.py     # 可选的文本模式审计脚本
└── tests/
    ├── test_audit_ai_flavor.py    # 自动化测试
    └── fixtures/                  # 多种文体的修改前后样例
```

## 开发与验证

运行全部测试：

```powershell
python -B -m unittest discover -s tests -v
```

验证 Skill 目录结构：

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .
```

测试重点包括：

- Profile 的上下文差异。
- 引文和代码块保护。
- Windows 风格 glob、标准输入和 JSON 输出。
- `clear` 与 `review` 的判定边界。
- 输入错误是否以清晰信息和正确退出码结束。

## 许可证

本项目采用 [GNU General Public License v3.0 only](LICENSE)（`GPL-3.0-only`）发布。你可以在该许可证规定的条件下使用、研究、修改和分发本项目；分发修改版本或衍生作品时，应当遵守 GPL v3 的相应义务。完整条款以仓库中的 [`LICENSE`](LICENSE) 文件为准。

## 支持项目

如果这个 Skill 对你的中文写作工作有帮助，可以考虑为 [fyihang/refining-the-tone-of-ai](https://github.com/fyihang/refining-the-tone-of-ai) 点一个 Star，帮助更多使用者发现并改进它。
