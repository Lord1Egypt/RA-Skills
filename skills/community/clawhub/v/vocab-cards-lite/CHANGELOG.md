# CHANGELOG — vocab-cards-lite

## v2.0.4 (2026-08-11) — 依赖精确锁定

- **requirements.txt 改为精确锁定**：`pillow==11.3.0`、`fonttools==4.63.0`、`qrcode[pil]==8.2`（Python 3.9+ 实测通过），消除版本范围解析到未审计版本的可能，安装完全可复现。
- **文档措辞中性化**：不再声称“已覆盖 CVE”，改为如实描述“固定已验证版本、部署前请自行审计”。

## v2.0.3 (2026-08-11) — 安全扫描修复

- **setup.sh 去除自动绕过 PEP 668**：不再自动 `--break-system-packages`。改为：venv 优先（`--venv [路径]`）、检测到已激活 venv 直接用、普通安装失败且因 PEP 668 保护时打印指引并退出；仅显式 `--allow-global` 才允许安装到系统 Python（自担风险）。修复 ClawHub 安全扫描 SDI-2 / SQP-2 告警。
- **requirements.txt 锁定安全版本范围**：`pillow>=10.4.0,<12`（修复 CVE-2023-50447 任意代码执行等）、`fonttools>=4.55.0`（修复 CVE-2023-45139 XXE、CVE-2025-66034 任意文件写）、`qrcode[pil]>=7.4.2`。修复 SC1 / SC4 供应链告警。
- **skill-card.md 同步**：更新风险描述与缓解措施（对应新 setup.sh 行为与依赖锁定）。

## v2.0.2 (2026-08-11) — CLAWhub 发布检测合规化

- **frontmatter 强化**：新增 `author`(51comic)、`license`(MIT-0)、`tags`、`compatibility` 字段，补齐跨平台发布元数据
- **新增章节**：`When to Activate`（触发条件）、`Anti-Triggers`（不适用场景）、`Domain Knowledge`（领域知识）、`References`（参考文件表）
- **新增 `references/` 目录**（`references/REFERENCES.md`），满足发布检测的 references 目录要求
- **移除 `_samples/` 示例 PNG**：减少二进制体积、规避纯文本上传告警，功能零影响（示例图仅作演示）
- 字体（`assets/fonts/*.ttf`）保留：IPA 音标渲染必需

## v2.0.1 (2026-08-11) — 搜索关键词优化

- SKILL.md / README / _meta.json 补充「单词卡」「英文单词」「英文闪卡」「单词闪卡」等搜索关键词
- 提升 ClawHub / SkillHub / GitHub 三平台中文搜索命中率

# CHANGELOG — vocab-cards-lite

## v2.0.0 (2026-08-08) — 达尔文全量优化

### 🔴 P0 结构性修复（均有实测证据）

- **重写 setup.sh 校验逻辑**（发布阻断）：v1.0.5 的 setup.sh 仍校验已被删除的 `NotoSansCJK-Lite-*.ttf`，导致**任何新用户跑安装必然在第一步中断**。v2.0.0 改为：校验实际存在的 2 个包内 IPA 字体 + 检测系统 CJK/DejaVu 字体，缺失时打印中文安装指引（`sudo apt install fonts-noto-cjk fonts-dejavu` 等）。
- **动态画布高度**：主卡/副卡不再固定 1700px 截断内容。两遍渲染（先测量、再绘制），按内容动态加高（最低 1700px，上限 3200px，超限打印 WARN 并截断）。修复"例句多/释义长时内容被静默截断"。
- **输入字段校验**：新增 `validate_item()`。只有 `word` 必填；其余字段缺失自动补默认值并打印 `HINT` 中文提示；缺 `word` 的条目打印 `SKIP` 原因后跳过，不再出现难懂的 `KeyError: 'ipa_uk'`。
- **slugify 空值兜底**：纯中文或特殊字符单词不再产出 `.png` 非法文件名，自动生成 `word_<md5前8位>.png`；同批数据 slug 撞车时自动追加 `_2`、`_3` 序号，避免互相覆盖。

### 🟡 P1 健壮性修复

- **setup.sh pip 兼容**：优先普通 `pip install`；仅在系统 Python（PEP 668 保护）下回退 `--break-system-packages`。修复老版本 pip 报 `no such option`。
- **字体延迟加载**：字体路径探测与 cmap 加载从模块导入期推迟到首次绘制时（`_ensure_fonts()`）。`--help`、`import` 复用函数不再因缺字体直接崩溃。
- **副卡字段 .get 兜底**：`side` 的所有子字段（`info`/`related`/`expressions`/`culture`/`tip`）缺失时按空值处理；`related`/`expressions` 兼容 str 或 list 输入。
- **JSON 顶层校验**：输入文件不存在 → 退出码 2 + 中文提示；非法 JSON → 退出码 2；顶层不是数组 → 退出码 2。

### 🟢 P2 体验/规范优化

- **SKILL.md 补触发词**：description 增加「单词卡」「闪卡」「词汇卡」「flashcard」「vocab cards」「背单词卡片」等触发场景词，提升技能匹配命中率。
- **自带最小示例**：新增 `examples/sample.json`（3 条：完整词条 / 无副卡词条 / 仅 word 的极简词条），一行命令即可验证安装：
  `python3 scripts/vocab_cards.py examples/sample.json /tmp/vocab_demo`
- **退出码规范**：正常 → 0；输入文件不存在/非法 JSON → 2；全部失败/跳过 → 3。结束时打印汇总 `完成: 成功 X / 失败 Y / 跳过 Z`。
- **修复文档漂移**：字体表与代码实际文件名对齐；明确"灰线"与"纯黑"的实际配色；注意事项补充溢出风险与动态画布说明。

### 保留的亮点（未改动）

- 分段渲染 + `'x'` 基线对齐（`_segment_text` + `draw_t`）：IPA/中文/英文混排不歪斜
- 字体对象缓存（`_font_cache`）：批量生成性能
- 三字体策略：包内裁剪 IPA（68KB）/ 系统 NotoSansCJK（中文）/ 系统 DejaVu（英文）

### 备份

v1.0.5 原始文件完整备份于：
`~/.openclaw/workspace/agent-3f4ae09d/skills/vocab-cards-lite.v1.0.5-backup/`
（含 `GIT-STATUS-v1.0.5.txt` 记录当时的 git 工作区快照）

---

## v1.0.5 (2026-08-05)

- 分段渲染 + `'x'` 基线对齐，修复英文基线高低不平
- 统一纯黑白配色
- 三字体策略定型：删除 CJK Lite 字体，中文改用系统字体，包体降至 68KB

## v1.0.0 (2026-08-05) — 首版发布到 ClawHub

- 段级字体选择，根治"豆腐块"
- 主卡 + 副卡 + 百度百科二维码三件套
- 发布：@51comic/vocab-cards-lite，标签 vocabulary/flashcards/english/education/print/python
