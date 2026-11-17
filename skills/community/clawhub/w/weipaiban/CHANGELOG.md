# Changelog

本项目遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 规范，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [2.0.2] - 2026-11-11

本次只调整 SkillHub 上架信息，便于按「公众号 SVG」「微信互动排版」被找到。技能流程与 2.0.0 相同。

### 变更

- `SKILL.md` 展示名改为「微排版公众号SVG交互作品」，短简介、长描述和标签改为公众号、SVG、互动排版、视差滑动、二选一
- 新增 `overview.md`，作为 SkillHub 详情页概述
- `README.md` 首段补充微信公众号与 SVG 互动图文

## [2.0.0] - 2026-11-11

本次为破坏性升级。技能从「按模板克隆并改写元素」改为「按 format 设计、制作并发布整篇交互作品」。不保留 1.x 流程兼容层。

### 新增

- 六种 format：`layered-scroll`、`parallax-scroll`、`coloring-scroll`、`quiz`、`choice-expand`、`scene-transition`
- 交互 HTML 方言、组件说明、素材契约与质量标准（`references/dialect.md`、`references/formats/`、`references/components/`、`references/task-contract.md` 等）
- 脚本：`scripts/fetch_ai_assets.py`、`scripts/build_oss_src.py`、`scripts/upload_images.py`、`scripts/publish.py`、`scripts/pick_direction.py`
- 默认图片来源改为微排版 AI 素材库：按一个 tag 拉取全部已发布图，再分配到槽位
- 发布改为 `POST/PUT /api/v1/vectors/svg`，用整份 HTML 创建或替换未发布作品
- 任务目录改为 `/tmp/weipaiban-{taskId}/`，阶段见 `task-contract.md`

### 移除

- 删除 `steps/` 下的模板搜索、克隆、配色、文本替换、图片分类与即梦生图流程
- 删除 `references/error-handling.md`、`references/runtime-dependencies.md`、`examples/usage-example.md`
- 不再依赖 `VOLCENGINE_*` 与 `jimeng-ai`；不再把 Step 8 作为可选生图阶段
- 不再锁定 `rembg[cpu,cli]==2.0.67`。1.2 的「检测依赖后须用户同意才安装」门禁随图片生成阶段一起删除。技能不会自动安装 `rembg`；只在用户提供且需要透明的图片时才可选使用，模型为 `birefnet-general`
- 库内素材不再重新上传、不再用 `rembg -m u2netp` 去背

### 变更

- `SKILL.md` 版本号改为 `2.0.0`，工作流、依赖声明和写入路径按 2.0 重写
- 技能标识从 `weipaiban-skill` 改为 `weipaiban`。调用名变为 `/weipaiban`。仓库地址仍是 `21epub/weipaiban-skill`
- `references/api-formats.md` 改为作品发布 API，不再描述模板搜索、克隆和 parser
- `README.md` 改为 2.0 的人类说明；agent 元数据只保留在 `SKILL.md`
- `README.md` 补充开源仓库 `https://github.com/21epub/weipaiban-skill` 与微信交流群二维码（`assets/contact-me-qr.png`）。`SKILL.md` 只指向这两处，不把二维码写入作品
- 说明 `WEIPAIBAN_API_KEY` 在 <https://weipaiban.cn/settings/api-keys> 创建或复制。缺密钥或 401 时，文档和脚本都把这个地址告诉用户

## [1.2.0] - 2026-04-29

本次发布聚焦安全与执行治理：在不牺牲流程可用性的前提下，补齐受控执行门禁、数据外传边界说明、写入最小化声明，并强化 rembg 供应链版本管理。

### 新增

- `SKILL.md` 新增「执行门禁（安全基线）」章节，明确强制确认动作、受控自动动作与中止优先规则
- `SKILL.md` 新增「写入最小化说明」，明确 `/tmp` 与 `~/.u2net` 的触发条件、用途与清理策略
- `steps/02-search-templates.md`、`steps/03-create-and-parse.md`、`steps/08d-image-upload.md` 新增「数据发送范围（透明披露）」说明
- `steps/09-update-and-complete.md` 新增提交 payload 字段白名单，限制仅更新 `elements` 允许字段
- `references/runtime-dependencies.md` 新增 rembg 锁定版本的升级流程（评估 → 回归 → 更新锁定版本号）

### 变更

- Step 2/3/8c/8d/9 的关键命令块改为「受控执行模板」语义，要求执行前确认条件与占位参数替换
- Step 3 补充任务目录重命名的范围、失败处理与清理说明，降低路径操作误解风险
- Step 8c 明确去背景仅在 `needsTransparent=true` 且依赖通过时执行，依赖失效时走降级上传分支
- Step 8a 安装示例从未锁定版本改为精确锁定：`pip3 install "rembg[cpu,cli]==2.0.67"`

### 安全

- 强化「先确认后执行」约束，降低自动执行类告警风险
- 明确外传边界（仅当前请求所需字段/单图文件或 URL），降低“隐式数据外传”判定概率
- rembg 依赖改为精确版本锁定，缓解“未固定版本”的供应链风险告警

## [1.1.0] - 2026-04-24

本次发布将 Step 8（图片生成）从「必需阶段」调整为「可选阶段」，明确区分必需 / 可选依赖，并引入「用户同意后才安装」的交互原则。缺失即梦凭据或 rembg 时，作品可保留模板原图降级完成。

### 新增

- 新增参考文档 [references/runtime-dependencies.md](references/runtime-dependencies.md)，集中说明凭据、外部服务、本地二进制、磁盘写入和数据流向
- SKILL.md frontmatter 增加 `optionalEnv` / `optionalSkills` / `optionalBinaries` / `externalServices` / `writes` 元数据字段，便于 openclaw 识别可选依赖和运行时副作用
- README.md frontmatter 增加 `optional` 字段
- SKILL.md 新增「运行时依赖」章节，区分必需依赖、可选依赖、降级行为
- Step 8a 新增「⏸️ 依赖缺失交互点」：向用户展示依赖检测结果表，提供「安装 / 跳过图片生成 / 取消」三选一

### 变更

- Step 8a/b/c/d 在步骤表中标注为「可选」，并在表格上方补充说明
- Step 8a 的依赖处理从「自动检测并安装」改为「只检测、展示结果、请求用户选择」，不再主动执行 `pip install` 或安装其他技能
- Step 8c 改为固定使用 `u2netp` 轻量模型（`rembg -m u2netp`），明确首次下载 `~/.u2net/u2netp.onnx`（约 4.7MB）
- Step 8c 当 rembg 不可用时，改为跳过背景去除并使用即梦原图 URL 上传（标记 `bgRemoved=false`），而非尝试安装
- 断点恢复规则：08a 改为识别 `meta.json` 中的 `skipImageGeneration` 标志
- README.md「安全与权限」章节重写为「必需 / 可选 / 降级行为」三段式

### 移除

- 移除 Step 8a 和 Step 8c 中自动执行 `pip3 install "rembg[cpu,cli]"` 的行为（改为仅在用户明确选择「安装」后提示并确认）

## [1.0.0] - 2026-04-24

- 微排版技能初始版本
