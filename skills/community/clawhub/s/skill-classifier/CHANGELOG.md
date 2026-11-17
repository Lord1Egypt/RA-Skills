# 更新日志 (CHANGELOG)

## [1.2.6] - 2026-09-25

### 📊 真实运行验收与示例更新
- **修复**：Markdown 表格的描述单元格压平换行/制表符并在 120 字处截断——真实运行发现多行长描述会撑破表格（完整内容仍在 JSON/HTML）
- 输出示例更新为真实运行节选（本机 64 个技能：31 ✅ / 5 ⚠️ / 28 ❌，含真实技能名/来源/截断描述），替换虚构示例
- 真实验收通过项：状态三分类判定、anyBins→needsetup、分类分布、JSON 结构、HTML 解析与转义、快照保存

---

## [1.2.5] - 2026-09-25

### 📝 名称与示例勘误
- SKILL.md H1 统一为「OpenClaw 技能分类与统计」（此前残留旧名「技能统计与分类管理」）
- 英文 README 示例勘误：示例技能名改为真实技能（含主页链接形态）；分类过滤与覆盖层示例改用实际存在的中文类目——"Dev Tools"/"Coding" 不在 10 大类 48 子类体系内，照抄会得到空结果
- GitHub 仓库描述中文半边同步为现行名称

---

## [1.2.4] - 2026-09-25

### 🔧 显示名修复
- ClawHub 显示名由误设的 "Clh Stage" 恢复为「OpenClaw技能分类与统计」（publish 时补 `--name`）

---

## [1.2.3] - 2026-09-25

### 🔒 ClawHub clawscan 整改（HTML 报告 XSS + 网络范围说明）
- **修复 XSS**：HTML 报告的 JS 渲染层对所有技能元数据（名称/emoji/版本/来源/分类/描述/调用量/状态图标）统一 HTML 转义后再写入 innerHTML——此前恶意技能的元数据可在打开报告时执行脚本
- 主页链接仅放行 http(s) scheme（阻断 `javascript:` 等危险协议），外链补 `rel="noopener noreferrer"`
- 「隐私与安全」网络范围说明修正：除飞书/Notion API 白名单外，`--check-updates` 还会经 `git ls-remote` 访问安装记录登记的 git 远端
- 新增 `tests/test_html_escaping.py`（scheme 过滤/转义覆盖/script-break 中和/SVG 转义/正常渲染回归）

---

## [1.2.2] - 2026-09-25

### 🛡 ClawHub SkillSpector 审查意见整改
- **修复**：`filesystem.py` 嵌套技能去重键错误——叶子目录同名时会误吞顶层同名技能（`seen_names` 改记 `full_name`），附回归测试
- description 与实际能力对齐：补增量快照对比、重复检测、汉化词表/报告；「Web 界面」改为「交互式 HTML 报告（静态网页，无需服务器）」
- frontmatter 新增 `allowed-tools: Bash`（声明工具范围）与 `metadata.language: zh-CN`（声明输出语言）
- `--push` 执行前新增隐私提示；SKILL/README 补「隐私与安全」说明（外发范围、权限范围、无持久化）
- subprocess 调用均为参数列表形式（无 shell=True），本次复核确认无注入面

---

## [1.2.1] - 2026-09-24

### 📝 说明双语化
- frontmatter `description`、README 简介与 GitHub 仓库描述统一为「英文在前、中文在后」的双语格式
- README 拆分为英文 `README.md` 与中文 `README.zh-CN.md`，顶部互链切换

---

## [1.2.0] - 2026-09-23

### 🚀 待提升项目全部落地（roadmap 六项 + 六项增强）

#### 新功能
- **使用频率统计**（`--usage`）：主路读 state 库 `skill_usage` 表，回退 `skills curator status --json`；md/html/json 增加调用量列
- **缺失依赖关系图**（`--deps`）：md 输出 mermaid 图，HTML 输出 SVG 二部图；数据源为 skills list 的 `missing` 字段（43 条边实测）
- **批量启用/禁用**（`--enable` / `--disable`）：写官方机制 `skills.entries.<名>.enabled`，改前自动备份 openclaw.json、写回前 JSON 校验、写后跑 CLI 验证
- **更新检查**（`--check-updates`）：git 安装轨对比本地/安装记录 commit 与远端 HEAD；ClawHub 轨提示官方 `openclaw skills update --all`；只报告不自动升级
- **飞书云文档导出**（`--push feishu`）：上传 md → docx 导入任务 → 返回文档链接
- **Notion 页面导出**（`--push notion`）：md 转 blocks 分批追加；两者凭据一律走环境变量，零第三方依赖

#### 增强
- **修复状态误判**：`get_skill_status` 补检 `anyBins` 组（此前仅缺 anyBins 的技能如 spotify-player 被误标 Ready）
- **输出利用元数据**：emoji、来源（bundled/workspace/…）、主页链接进入所有输出格式
- **分类自定义覆盖层**：`~/.openclaw/skill_categories.json` 优先于内置映射表，第三方技能不再必须改源码
- **汉化词表辅助**（`--i18n-report`）：输出未命中词表的英文词清单
- **判重算法升级**：描述相似度从「前 20 字符相等」改为 `difflib.SequenceMatcher`（阈值 0.9）
- **HTML 表头排序**：名称/版本/来源/调用量/分类点击排序

#### 工程化
- 新增 `tests/`：47 个 pytest 用例（状态判定/分类/覆盖层/导出器/差异/用量/更新/启停/HTTP 客户端/Notion blocks）
- 新增 GitHub Actions CI：compileall + pytest（Python 3.9 / 3.12 矩阵）
- 新增 `utils/webclient.py`：标准库 HTTP 客户端，强制 HTTPS + 主机白名单 + 拒绝内网/环回/保留地址

---

## [1.1.0] - 2026-09-23

### 🛠 对抗审查整改

#### 修复
- **`-o` 自定义输出目录**：目标目录不存在时自动创建（此前三个导出器直接 `FileNotFoundError` 崩溃）；同时规范化路径并拒绝包含 `..` 的路径段
- **frontmatter 规范化**：`name` 改为 `openclaw-skill-manager`（与目录同名，符合 AgentSkills 规范的小写连字符要求），`version`/`author` 迁入 `metadata`
- **移除 `scripts/` 旧版脚本**：其中硬编码了作者本机私人路径，且为 Windows-only 死代码

#### 对齐
- 文档功能清单与代码对齐：移除「HTML 排序」「目录大小/安装时间」「快照 24 小时过期」「分类学习自动保存」等无实现声明
- 「自动翻译」改述为「描述汉化：内置词表替换」（实际行为）；「依赖检查」改述为「状态检测：识别缺失依赖（NeedSetup）」
- 分类数字修正为实测口径：10 大类 48 子类
- 注意事项声明分类规则适用范围（基于作者个人技能库定制）

#### 清理
- 移除死代码：分类学习、未注册技能扫描、依赖检查、目录大小等未接线函数及空循环桩
- `openclaw` CLI 调用改为参数列表形式，并预检命令是否存在
- 输出/缓存目录改为运行时惰性创建，消除 import 副作用
- 消除重复 import 与重复汉化调用
- 全部示例命令 `python` → `python3`；旧目录名 `kt_skill_list_skill` 统一为 `openclaw-skill-manager`
- 作者署名统一为 handle `kuntao2011`

---

## [1.0.1] - 2026-05-10

### 🔄 名称调整
- 技能名称由 "OpenClaw技能统计与分类管理" 改为 **"OpenClaw技能分类与统计"**
- 优化名称表述，减少歧义

---

## [1.0.0] - 2026-05-10

### ✨ 首次公开发布

**技能正式名称**：**OpenClaw技能统计与分类管理**

### 🎯 核心功能

- ✅ **多格式输出**：Markdown / JSON / HTML
- ✅ **自动分类**：9 大类 30+ 子类自动归类
- ✅ **状态图标**：✅ Ready / ⚠️ NeedSetup / ❌ Disabled
- ✅ **元数据提取**：版本号、作者、目录大小
- ✅ **交互式 HTML**：实时搜索、分类筛选、状态过滤、统计面板
- ✅ **增量更新**：对比历史快照，仅输出变化的技能
- ✅ **重复检测**：自动识别功能重复的技能
- ✅ **灵活过滤**：按状态、关键词、分类筛选
- ✅ **自动翻译**：英文描述自动翻译为中文

### 🏗️ 模块化架构

```
openclaw-skill-manager/
├── data/          # 数据层（OpenClaw CLI、文件系统、元数据）
├── classifier/    # 分类层（映射表、重复检测）
├── exporter/      # 导出层（Markdown、JSON、HTML）
└── utils/         # 工具层（配置、描述汉化、差异对比）
```

### 📄 GitHub 发布配套文件

- `README.md` - 完整的项目说明和使用文档
- `LICENSE` - MIT 开源许可证
- `.gitignore` - Python 项目标准忽略规则
- `requirements.txt` - 依赖说明文件
- `CHANGELOG.md` - 本更新日志

### 👤 作者信息

- **作者**：kuntao2011
- **发布日期**：2026-05-10
