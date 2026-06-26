# Step 0 & Step 0.8 指令

> **🔴 V3.0 架构声明：本文件中的手动执行指令（如"Agent自行read/write/exec"）已被orchestrator.py替代。Agent不应直接按本文件的exec命令执行，而应通过orchestrator的action调用。本文件保留为prompt模板和知识注入的参考源，orchestrator的prep_prompt action会自动读取本文件中的prompt和知识路径。**

🔴 **PX关键约束（V3.0.0 A-2方案）**：Agent直接用read工具读取图片，价值优先选择最多5张。不依赖model_detect.py/OCR引擎。model_detect.py/image_understand.py/image_ocr.py已退出PX主流程（model_detect.py仍在P5分批模式中使用）。

---

---

## 路径约定

| 变量 | 含义 | 示例 |
|------|------|------|
| `{SKILL_DIR}` | 本 SKILL.md 所在目录 | `.../skill_v2/` |
| `{DATA_DIR}` | 中间结果持久化目录 | `~/.openclaw/workspace/data/{task_id}/` |
| `{task_id}` | 任务唯一标识 | `task_20260421_153000` |

每步输出写入 `{DATA_DIR}/p{n}_output.json`,支持断点续跑。

---

## 执行流程:Step 0 → Step 7

> **关键约束**:
> 1. 所有步骤串行执行,禁止使用 sessions_spawn 并行
> 2. **你(Agent)就是 LLM**:所有「调用 LLM」的步骤,直接用你自己的推理能力执行,不需要调用任何外部接口或 API。你读取 Prompt 模板后,直接输出对应的 JSON 结果即可。
> 3. 每步调用 LLM 后必须执行 JSON 解析兜底逻辑(见「JSON 解析兜底」一节)
> 4. 中间结果必须写入 `{DATA_DIR}/`,确保可断点续跑
> 5. **严禁跳步**:必须严格按 Step 0→Step 1(P0)→Step 2(P1)→Step 3(P2/P3/P4)→Step 4(P5)→Step 5(P6)→Step 6(P7)→Step 7(输出) 顺序执行,任何步骤不得跳过或合并。每步必须有对应的 JSON 输出文件写入 `{DATA_DIR}/`,否则视为未完成,不得进入下一步。禁止直接从需求文档一步生成测试用例。
> 6. **严禁合并 Step 5/6/7**:禁止将 Step 5(P6)、Step 6(P7)、Step 7(输出)合并为一个回复执行。每个 Step 必须单独完成并输出一行状态行后,再自动推进到下一个 Step。
> 6. **自动推进（禁止暂停等待用户）**:Step 0 到 Step 7 按顺序自动推进,不得以「是否继续」「先看看成果」等理由暂停等待用户指示。每个Step独立执行,禁止在单个exec中合并多Step逻辑。如回复被截断,用户发送「继续」时按gate pass恢复。
> 7. **对话输出规范(严格遵守)**:
>    - **每步只允许输出一行状态确认**,格式:`✅ Step X(PX)完成!- 关键指标(如:质量评分0.85/功能点37个/测试点26条)- 文件已保存`
>    - **🚫 严禁输出(违反即视为执行错误)**:需求文档原文、JSON 结构体、P0/P1/P2/P3/P4/P5 等任何中间分析内容、任何超过2行的详细说明。**每步只能输出一行状态确认,然后立即执行下一步。**
>    - **P6 执行时**:开始时输出「⏳ 正在生成测试用例,预计需要 1-2 分钟,请稍候...」;每完成10条输出一次进度「已生成 X/N 条用例...」
>
> ### 🔴 执行诚实规则(全流程强制)
>
> 1. **禁止声称未执行的操作**:如果 exec 命令未实际执行,不能说「已执行」「已生成」「已发送」
> 2. **文件操作必须验证**:所有文件写入/生成操作,必须用 `exec: ls -la {path}` 验证文件存在后才可确认
> 3. **MEDIA 发送必须在实际生成文件后**:先 exec 生成 → 验证文件存在 → 再输出 MEDIA 行
> 4. **禁止幻觉输出**:不能在未真正调用 exec 工具生成 Excel 的情况下说「Excel文件已发送」
> 5. **步骤级伪完成禁止**:禁止说「已完成分析」如果分析结果未落盘到 {DATA_DIR} 对应 JSON 文件
> 6. **结果完整性校验**:任何步骤声明「完成」,必须满足:目标文件存在 + 文件结构合法(可 JSON.parse)+ 关键字段非空 + 最小产出数量达标
> 7. **exec 退出码校验**:所有 exec 命令必须检查退出码为 0 才算执行成功,非 0 则标记为失败
> 8. **文件非空校验**:文件类操作除了存在性校验,还需检查文件大小 > 0(至少 100 bytes),避免生成空文件
> 9. **降级诚实**:降级逻辑必须实际执行,禁止说「已转 PCI」但文件中未写入
> 10. **部分成功诚实披露**:禁止将部分成功描述为全部成功
>
> ### 🔴 跨步骤可测性分流规则
>
> 对所有从 P0/P0.5 继承来的 blocker/PCI,P1-P6 必须进行可测性分流:
> - **可测**:信息充分,正常生成用例
> - **条件可测**:可生成用例,但需在用例 `remarks` 中附前置假设/待确认条件,`case_type` 标注为 `"条件验证"`
> - **不可测**:只登记为风险条目写入 P6 输出的 `statistics.risk_items` 数组(因 P6 在 P5 之后执行,无法修改 P5 输出),**禁止生成伪完整用例**
> - Step 7 最终产物中必须新增统计:不可测需求点数、条件可测用例数、因需求缺失而降级的断言数
>
> ### 🔴 异常处理兆底规则
>
> 非交互模式下,除 Onboarding BLOCKED 外,任何步骤因执行错误(非业务逻辑判断,如文件读写失败、JSON 解析失败、Python 脚本异常)无法继续时,按跳步分级规则处理:关键产物(P0-P4/P5写入)错误→终止流程;非关键步骤(P6/P7)错误→允许受控降级继续。终止模板:`❌ Step {N} 执行失败: {错误原因}。中间产物保存在 {DATA_DIR},可发送「从 P{N} 重新开始」重试。`
>
> ### 🔴 关键产物门禁（强制）
>
> 所有 P0-P7 产物写入后必须通过 `truncation_guard.py --auto-mv` 四级校验（L1文件存在→L2 JSON有效→L3结构完整→L4内容完整）。
> 校验通过后脚本自动 mv tmp→正式文件 + 生成 gate pass；校验失败则自动 rm tmp，不会残留不完整产物。
> 后续步骤通过 gate pass 链式依赖确保前置完整，未通过校验的步骤无法启动。
>
> **退出码处理**：
> - 退出码1/2/3（L1/L2/L3失败）→ 必须终止流程，可重试1次
> - 退出码4（L4数量不足）→ P5允许受控降级继续，其他Step必须终止
>
> **L4组合校验（P5/P6增强）**：
>
> P5 L4组合校验（数量阈值之外）：
> | 校验项 | 说明 | 失败行为 |
> |--------|------|----------|
> | 模块覆盖 | P2的一级模块在P5中必须有对应测试点 | WARNING（不FAIL） |
> | 优先级保留 | P2存在P0/P1测试点时，P5中P0/P1不能为0 | FAIL（退出码4） |
> | merge_log一致性 | merge_log.final_count == len(test_points) | FAIL（退出码4） |
>
> P6 L4组合校验：
> | 校验项 | 说明 | 失败行为 |
> |--------|------|----------|
> | P0全展开 | P5的P0测试点在P6中必须都有对应用例 | WARNING（不FAIL） |
>
> WARNING不阻塞流程，但写入gate pass的summary.warnings数组，输出格式变为 `GUARD_PASS:{step}:{count}:WARNINGS:{warning_count}`
>
> **降级产物隔离**：P6降级产物写入 `p6_output.degraded.json`（不生成gate pass），statistics中标记degraded:true
>
> ### 🔴 跳步分级规则
>
> - **一级关键产物缺失(P0-P4 JSON文件不存在、为空或JSON格式无效)→ 必须终止**,输出 `❌ 关键产物缺失:{文件名},流程终止。中间产物保存在 {DATA_DIR},用户可发送「重试」重新执行。`
> - **二级关键产物P5写入失败(文件不存在/为空/JSON无效)→ 必须终止**;P5质量不达标 → 允许受控降级
- **非关键步骤失败（P6/P7）→ 允许受控降级**，输出警告但继续执行。P6失败时降级操作：跳过P6完整用例展开，直接基于P0需求结构+P1功能点树+P2测试点，生成最小可行用例集（每个功能点至少1条正向验证用例），输出到 `{DATA_DIR}/p6_output.degraded.json`（降级产物使用.degraded.json后缀，不生成P6 gate pass），statistics中标记degraded:true），并输出警告 ⚠️ P6用例展开失败，已降级为最小可行用例集，建议人工补充。
> - **禁止行为**:不得"调整策略"、"简化流程"、跳过已失败的步骤继续执行。失败后唯一选项是终止或重试。
>
> ### 🔴 工具调用指导(弱模型适配)
>
> - write工具的content参数必须是纯字符串,不要嵌套JSON对象
> - JSON内容中如含引号、换行符等特殊字符，必须使用heredoc写入方式
- **所有 P0-P7 产物写入必须先写 `.tmp.json`，再调用 `truncation_guard.py --auto-mv`，禁止直接写正式文件**
> - 禁止连续3次工具调用失败后继续尝试同一方式,必须切换策略(如从write切换到exec heredoc)
> - **严禁自建脚本替代官方工具**:不得创建自定义 export_excel.py 或其他 tools/ 目录下的脚本替代官方版本
>
> **优先级**:关键产物门禁 > 工具调用指导。P0-P4写入失败时,允许切换策略重试1次(如write→heredoc),重试仍失败则必须终止(不适用"切换策略继续"规则)。P5-P7写入失败时,允许切换策略重试最多3次。
>
> ### 🔴 禁止自建脚本
>
> tools/ 目录下的脚本(export_excel.py、export_markdown.py、model_detect.py等)为官方工具,执行方不得创建替代版本。如果路径发现检查1.5失败,输出错误并在Step 7中直接内联输出Markdown格式用例到对话(不依赖export_markdown.py脚本),不得自建简化版export_excel.py。内联Markdown格式规范:表头含19列完整字段名(项目/类型/用例编号/需求/优先级/标题/用例菜单/预置条件/步骤/期望结果/是否冒烟用例/创建者/经办人/用例类型/测试类别/执行结果/截图/测试用例集/备注),每个用例一行,末尾附统计(总数/P0数/冒烟数/降级标记)。

---

### Step 0:接收用户需求 & 初始化

**⚠️ 本步只输出1行状态,不输出中间过程。**

**前置门禁检查（校验当前task_id的onboarding.pass.json）**:
```bash
exec: python3 -c "
import os, sys, json
gp = os.path.join('{DATA_DIR}', 'gates', 'onboarding.pass.json')
if not os.path.exists(gp):
    print('GATE_BLOCKED:onboarding:当前task的onboarding.pass.json不存在'); sys.exit(1)
d = json.load(open(gp))
if d.get('task_id') != '{task_id}':
    print('GATE_BLOCKED:onboarding:task_id不匹配'); sys.exit(1)
print(f'GATE_OK:onboarding已完成,task_id={d.get("task_id")}')
"
```
如果 GATE_BLOCKED → **必须停止,返回执行Onboarding**。
注意：{task_id}和{DATA_DIR}在Onboarding阶段已创建，Agent必须使用Onboarding输出的实际值。

**目标**:从用户消息中提取需求文本,初始化任务上下文。

**执行指令**:

1. 从用户消息中提取 `requirement_text`(原始需求全文)
2. 识别业务域 `domain`:
   - 从需求文本中识别关键词(按优先级匹配,取第一个命中的域):
     - 交易/委托/撤单/成交/清算/结算/资金冻结/T+1 → `trade`
     - 资管/净值/申赎/申购/赎回/衍生品/期货/期权/保证金 → `asset_mgmt`
     - 风控/预警/限额/合规检查/风险控制 → `risk_ctrl`
     - 客户/跟进/开户/KYC/客户经理/客户关系 → `crm`
     - 网上营业厅/APP/适当性/产品推荐/在线交易/移动端/H5 → `etrading`
     - 运营/活动/营销/后台管理/数据报表/统计/导出 → `ops_mgmt`
     - 合规/证书/从业/监管/报送/资质/执照 → `compliance`
     - 部署/监控/服务器/权限配置/变更/IT/基础设施/投行/承销/IPO → `it_infra`
   - 无法识别 → 使用 `preferences.json` 中的 `default_domain`(默认 `trade`)
3. 生成 `task_id`:格式 `task_YYYYMMDD_HHMMSS`
4. 创建数据目录:`exec: mkdir -p ~/.openclaw/workspace/data/{task_id}`
5. 读取 `{SKILL_DIR}/user_knowledge/preferences.json`,记录用户偏好
6. 向用户确认:`「✅ 任务 {task_id} 已创建,业务域:{domain},开始分析需求...」`

**写入**:`{DATA_DIR}/task_meta.json`
```json
{
  "task_id": "...",
  "domain": "...",
  "requirement_text": "...",
  "created_at": "ISO8601",
  "preferences": { ... },
  "skill_version": "3.0.0",
  "requirement_hash": "sha256(requirement_text)",
  "preferences_hash": "sha256(preferences.json normalized)",
  "cache_signature": "{skill_version}:{domain}:{requirement_hash}:{preferences_hash}"
}
```

---

### Step 0.8(自动):PX 图片理解与测试增强（A-2方案）

**目标**:从需求文档中抽取图片,Agent直接用视觉能力理解图片内容,生成测试增强数据供后续步骤消费。

**触发条件**:用户提供的需求文档为 docx 格式时自动执行。非 docx 格式或纯文本输入时跳过此步。

**⚠️ 本步只输出1行状态,不输出中间过程。**

**架构说明（V3.0.0 A-2方案）**:
- 不再依赖 model_detect.py 判断视觉能力
- 不再依赖 OCR 引擎（云端环境装不上）
- 不再通过 Python 脚本生成 vision_queue 让 Agent 理解隐含指令
- Agent 直接用 read 工具读取图片,能看懂就用,看不懂就降级为 caption+上下文
- model_detect.py / image_understand.py / image_ocr.py 退出主流程（保留文件不删除,供回退参考）

**内部动作**(不输出到对话):

1. **图片抽取**:
   ```bash
   exec: python3 {SKILL_DIR}/tools/image_extract.py "{docx_path}" --output-dir {DATA_DIR}/px_images --json-output {DATA_DIR}/px_extract.json
   ```
   - 失败或无图片 → 跳过 PX,继续 Step 0.5/Step 1

2. **图片价值优先选择（最多5张）**:
   读取 `{DATA_DIR}/px_extract.json`,按以下优先级选择最多5张图片:
   - **优先级1**:caption 或相邻文本命中关键词（流程/状态/原型/页面/规则/接口/表格）的图片
   - **优先级2**:相邻文本包含"如下图""见图""页面""流程""状态""规则"的图片
   - **优先级3**:按文档位置顺序补足至5张
   - 跳过明显装饰性图片（如 logo、分隔线、背景图,可通过图片尺寸<50x50或caption含"logo/icon/分隔"判断）

3. **Agent直接读取图片并理解**:
   对每张选中的图片,执行:
   ```
   read {图片文件路径}
   ```
   读取后,用视觉能力描述图片内容,重点关注:
   - 图片类型（页面原型/流程图/状态图/数据表/接口截图/其他）
   - 具体UI元素（按钮名、字段名、菜单项、状态节点等）
   - 与需求文本的关联（哪个功能模块、哪个业务流程）
   - 可衍生的测试点（交互逻辑、数据校验、状态转换等）

   **理解判定标准（三条件）**:
   Agent对一张图片同时满足以下3个条件时,判定为"已理解":
   1. 能识别图片类型（prototype/flowchart/table/api_screenshot/other）
   2. 能提取至少2个具体元素（按钮名、字段名、状态节点、表头、文案等）
   3. 能说出与需求文本相关的至少1个测试价值点

   满足三条件 → `understanding_mode = "vision"`,记录完整理解结果
   不满足 → `understanding_mode = "caption_context_only"`,仅保留 caption + 上下文文本,不输出具体UI/规则断言

4. **写入理解结果**:
   将所有图片的理解结果写入 `{DATA_DIR}/px_understand.json`:
   ```json
   {
     "task_id": "...",
     "total_images": 18,
     "selected_images": 5,
     "results": [
       {
         "image_id": "img_001",
         "file_path": "...",
         "selected": true,
         "selection_reason": "caption命中'流程'关键词",
         "understanding_mode": "vision",
         "confidence": "high",
         "image_type": "flowchart",
         "evidence": ["状态:待审核", "状态:已通过", "箭头:审核→发布"],
         "description": "...",
         "derived_features": ["审核流程状态转换"],
         "derived_test_points": ["状态从待审核到已通过的转换条件"],
         "derived_risks": ["审核超时未处理"],
         "degradation_reason": null
       }
     ],
     "skipped_images": [
       {
         "image_id": "img_006",
         "file_path": "...",
         "selected": false,
         "selection_reason": "超出5张上限,未命中高价值关键词",
         "understanding_mode": "skipped"
       }
     ],
     "summary": {
       "vision_count": 3,
       "caption_only_count": 2,
       "skipped_count": 13
     }
   }
   ```

5. **测试增强聚合**:
   ```bash
   exec: python3 {SKILL_DIR}/tools/image_enhance.py {DATA_DIR}/px_understand.json --output {DATA_DIR}/px_enhance.json
   ```
   - `image_enhance.py` 需适配新的输入格式:
     - 识别 `understanding_mode` 字段
     - 对 `caption_context_only` 产物做保守增强（不生成强断言测试点）
     - 对低置信度图片（confidence=low）禁止生成强断言测试点
   - 输出含 step_subsets,供 P0-P7 各步消费

6. **写入结果**:`{DATA_DIR}/px_enhance.json`

**降级策略**:
- PX 任何步骤失败不阻断主链路,直接跳过进入 Step 0.5/Step 1
- Agent 无法理解任何图片（全部降级为 caption_context_only）→ 正常继续,仅注入 caption + 上下文
- image_enhance.py 失败 → 跳过增强,仅保留 px_understand.json 供 P0 参考

**对话输出**(仅此一行):
`✅ PX完成 | 图片{N}张/视觉理解{V}张/跳过{S}张 | 文件已保存`

**⚡ 自动推进**:完成后立即执行 Step 0.5(如开启)或 Step 1。

---

