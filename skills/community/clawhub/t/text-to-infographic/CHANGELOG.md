# Changelog

## 1.5.0 (2026-11-17)

- 布局从 6 种扩到 10 种：新增 comparison（对比双栏）、quadrant（2×2 矩阵）、flow（流程步骤）、venn（韦恩图），补齐「对照/优先级/分步/交集」四类高频关系结构
- 新增「一列一色」马卡龙配色（`MACARON`/`MACARON_LIGHT`，蓝/黄/红/绿）：comparison/quadrant/flow/venn/pyramid 五个布局直接产出多主体并列的马卡龙风配图，无需手写 SVG
- 重写 pyramid：修复早期「基座画反」问题，改为严格等腰正金字塔（塔尖在上、基座最下最宽），层内标题居中 + 右侧虚线引线说明
- 增强 flywheel：从「四瓣圆环」升级为「中心圆盘 + 外侧节点（标题+描述）+ 闭环箭头」，语义信息完整
- 校验器新增 6 条规则码：CMP-001/002、QDR-001、FLOW-001、VENN-001（共 31 条），`--rules` 同步更新
- `build_plan_from_text.py` 的 analyze 启发式补 4 个新布局的信号词与叙事前提
- schema 新增 meta.x_label/y_label（quadrant 轴标签）与 block.group_title（comparison 列标题）

## 1.4.0 (2026-11-11)

- 校验器升级为「带规则码的机器回执」：每条 finding 附稳定规则码（PLAN/SAFE/TEXT/TIME/PYR/FLY/FISH/SANK/DASH/SEM/SRC/NUM 系列，`--rules` 列出全部 25 条）；`--json` 输出 `code / level / layer / subject / message / evidence / why / fix`，可被 CI、agent 或其他工具直接消费
- 新增 `--fail-on-warn`（别名 `--strict`）：WARN 也判失败（exit 1），适合批处理与上线前把关；`--json` 的 `ok/decision` 同步反映该判据
- 新增可选 PNG 导出：`render_infographic_html.py --png`，用本机已有 Chrome/Chromium/Edge 无头截图自包含 HTML（默认 852×2x，小红书/公众号直发）；新增 `scripts/export_png.py`（两遍截图：1x 测高 → 目标倍率出图，纯标准库手写 PNG 解码测高，不往页面注入任何脚本）
- 安全契约不变：**不安装、不下载任何浏览器**——找不到浏览器时明确报错退出（exit 3），HTML 主路径不受影响；产物 HTML 仍零 JS 零外链，截图过程无网络请求
- 新增 `scripts/test_export_png.py`：解码往返 / 测高逻辑 / 真机截图冒烟（无浏览器自动 SKIP），8 项全过
- 沙箱/容器兼容：截图失败自动降级 `--no-sandbox` 重试一次并在本次运行内记住
- 校验器人类可读输出升级：每条带 `[LEVEL] CODE (subject)`，subject 精确到块 id / 字段路径

## 1.3.0 (2026-11-02)

- 新增 `scripts/build_plan_from_text.py`：text→plan 自动构建入口——`--analyze` 启发式推荐 chart_family 布局（输出证据与叙事前提），`--from-blocks` 把 LLM 抽取的 blocks 草稿组装成完整 plan（自动填 version/layout/visual_system），组装后立即调用校验器，有 ERROR 不产出 plan
- 校验器升级为独立可用的诊断工具：新增 `--explain`，每条 finding 附「为什么 / 怎么改」中文诊断；适配校验非本工具产出的 plan 场景
- 视觉 token 扩展（克制路线）：palette 新增 editorial / technical / warm 三个 preset（共 8 种）；`visual_system` 支持 accent / ink / paper / muted 四 token 十六进制覆盖，与渲染器边界一致
- 安全边界同步：四 token 全部走渲染器入口强校验 + schema pattern + 校验器拦截三处一致；`test_render_security.py` 扩展为覆盖 4 token × 8 注入 payload + 全 preset 烟测
- 新增示例 examples/editorial-flywheel-demo.json（editorial preset + token 体系演示），全部 7 例重渲染，产物零脚本/零外链
- 本版本自线上 v1.2.2（安全修复）基线上开发
- 补充（2026-11-05）：新增 `scripts/check_sync.py` —— 只读自检，比对本地 repos / 本地 zip / 线上 ClawHub 三处版本与关键脚本 sha256 指纹（检测同版本静默分叉）

## 1.2.2 (2026-10-27)

- 安全修复：`visual_system.accent` 之前直接插值进 CSS/SVG，可被构造值注入脚本/事件处理器/外链，违背「零脚本、零外链」承诺
- 渲染器边界严格校验：accent 只接受十六进制颜色（#RGB / #RRGGBB），非法值拒绝渲染
- 校验器同步拦截非法 accent（与 schema、渲染器三处一致）
- 产物 `<head>` 增加 CSP（`default-src 'none'`）阻断脚本与外部请求，双保险
- 新增回归测试 `scripts/test_render_security.py`（闭合标签/属性 breakout/CSS URL 等注入用例）
- SKILL.md 声明 `allowed-tools: Read, Write, Bash` 澄清工具边界

## 1.2.1 (2026-10-24)

- 修复 pyramid 布局错位：CSS clip-path 方案改为内联 SVG，坐标精确计算
- 层级顺序回归「blocks 第一个 = 基座」，配色由基座向顶层渐浅，右侧注释固定横排不再竖挤
- 清理废弃 CSS

## 1.2.0 (2026-10-21)

- 新增内置渲染器 `scripts/render_infographic_html.py`：plan JSON → 自包含静态 HTML（6 种 chart_family 布局，零 JS / 零外链 / 零依赖）
- 新增校验器 `scripts/validate_infographic_plan.py`：布局语义校验（A 层）+ 数值溯源（B 层，需 --source）+ 文本预算（C 层）
- 新增 `schemas/infographic-plan.schema.json` 与 6 个示例 plan
- 差异化叙事正式升级：可编辑 plan + 信息正确校验 + 安全渲染（零安装/无网络导出）
- 说明：v1.1.3 及之前为纯提示词版本（仅输出规格/HTML 源码），本版本起携带可执行工具

## 1.1.3 (2026-09-15)

- 纯提示词版本：单页信息图规格 + 可复制的静态 HTML 源码输出
