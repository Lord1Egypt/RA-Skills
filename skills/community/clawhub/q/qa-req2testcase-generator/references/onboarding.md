# Onboarding 检查指令

> **🔴 V3.0 架构声明：本文件中的手动执行指令（如"Agent自行read/write/exec"）已被orchestrator.py替代。Agent不应直接按本文件的exec命令执行，而应通过orchestrator的action调用。本文件保留为Onboarding交互流程的参考源。**

---

## 🔴 前置条件：需求载荷必须就绪

**在启动任何Onboarding检查之前，必须确认需求载荷（requirement payload）已就绪。**

需求载荷就绪的判定规则：
- 当前消息包含需求正文（文本形式的需求描述）→ ✅ 就绪
- 当前消息包含需求附件（.docx/.pdf/.txt等文件）→ ✅ 就绪
- 当前消息明确引用最近消息中的需求材料（如"分析上面的需求""分析我刚发的文档"）→ ✅ 就绪
- 当前消息仅表达意图（如"等会发需求""准备好了""开始吧"）→ ❌ 未就绪

**未就绪时的唯一合法输出**：
```
请发送需求正文或需求文档，收到后立即开始分析。
```
不得输出步骤清单、能力介绍、流程说明等任何额外内容。不得启动Onboarding。

**禁止复用旧需求**：若最近一次需求材料对应的task_id已完成（存在该task的Excel产物），且本轮未明确要求"继续/复用该需求"，不得自动拿旧需求重启新流程。

---

## 🔴 两阶段交互规则

**阶段1——Onboarding（检查1→检查4）**：交互模式，检查3（PRD审查选择）和检查4（L5上传选择）**必须暂停等待用户选择**，不得自动跳过。跳过交互=协议违规。

**阶段2——主流程（Step 0→Step 7）**：零暂停模式，连续执行不得等待用户输入。

唯一允许在主流程暂停的情况：Step 0.5 PRD审查发现blocker且用户选择查看问题清单中断流程。

---

## Onboarding 检查（每次执行前必做）

在开始 Step 0 之前，按以下顺序检查环境就绪状态。任何一项 BLOCKED 则停止并提示用户。

### 检查 1:文件完整性

```
读取本 SKILL.md 所在目录,确认以下文件/目录存在:
- prompts/P0_requirement_structuring.md
- prompts/P1_feature_tree_generation.md
- prompts/P2_test_point_draft.md
- prompts/P3_risk_identification.md
- prompts/P4_pci_identification.md
- prompts/P5_test_point_merge.md
- prompts/P6_testcase_generation.md
- prompts/PX_image_understand.md
- tools/image_extract.py
- tools/model_detect.py
- tools/image_understand.py
- tools/image_enhance.py
- knowledge/model_vision_capability.json
- knowledge/industry/
- knowledge/methodology/
- knowledge/company_standards/
- knowledge/defect_patterns/
```

如有缺失:输出 `❌ Onboarding 失败:缺少文件 {path},Skill 安装不完整。` → BLOCKED(用户可检查安装后重试)

### 检查 0.5:缓存检测(新任务 vs 续跑)

```bash
exec: ls ~/.openclaw/workspace/data/ 2>/dev/null | grep "^task_" | sort -r | head -3
```

> ⚠️ **此步骤禁止输出任何选项菜单。不得输出「继续 / 重新开始 / 重新生成」三选项。不得等待用户回复。违反即为协议违规。**

- **无缓存**:直接继续
- **有缓存**:默认按**新任务优先**处理,**自动清理本次不复用的历史缓存并重新开始**,不得等待用户选择,不得输出三选项
- **仅当用户消息中明确包含以下指令时**,才进入特例分支:
  - `继续 task_XXXXXX` → 从指定 task 继续
  - `重新生成` → 保留 P0-P5,仅清除 P6/P7/最终 Excel 后重跑
  - `从 P{n} 重新开始` → 清除该步及后续缓存,从指定步骤重跑

> **默认策略(必须严格执行)**:
> - 用户直接发送新需求文档/需求文本 = 视为新任务,自动重新开始
> - 不得因发现历史缓存而暂停或要求用户确认
> - **严禁输出"继续 / 重新开始 / 重新生成"选择菜单**
> - 检测到缓存后应直接输出: `检测到历史缓存,已自动清理,开始新任务。` 然后立即进入下一步

### 检查 1.5:SKILL_DIR 路径自动发现(必须完成,后续步骤依赖此结果)

```bash
exec: bash -c '
# 1. 环境变量优先
if [ -n "$SKILL_DIR" ] && [ -f "$SKILL_DIR/tools/export_excel.py" ]; then
    echo "SKILL_DIR=$SKILL_DIR"; echo "export_excel.py=$SKILL_DIR/tools/export_excel.py"
# 2. 原glob搜索
elif candidates=$(timeout 10 find ~/.openclaw ~/.local ~/skills /app/skills -name export_excel.py -print -quit 2>/dev/null) && [ -n "$candidates" ]; then
    skill_dir=$(dirname $(dirname "$candidates"))
    echo "SKILL_DIR=$skill_dir"; echo "export_excel.py=$candidates"
# 3. 容器常见路径
elif [ -f "/app/skills/qa-req2testcase-generator/tools/export_excel.py" ]; then
    echo "SKILL_DIR=/app/skills/qa-req2testcase-generator"; echo "export_excel.py=/app/skills/qa-req2testcase-generator/tools/export_excel.py"
else
    echo "ERROR: 未找到 export_excel.py,请设置 SKILL_DIR 环境变量"
fi
'
```

- 成功找到:将输出的 `SKILL_DIR` 路径记录为本次任务的 `{SKILL_DIR}`,后续所有步骤使用此实际路径
- 未找到:输出 `⚠️ 无法定位 export_excel.py,Excel 导出将降级为 Markdown 输出。` → 继续(不阻塞)

> **重要**:后续步骤中所有 `{SKILL_DIR}` 占位符,必须替换为本步骤发现的实际路径,不得使用字面量 `{SKILL_DIR}`。

### 检查 2:Python + openpyxl 可用性

```bash
exec: python3 -c "import openpyxl; print('ok')"
```

- 成功:继续
- 失败:尝试 `exec: pip install openpyxl`,再次检查
- 仍失败:输出 `⚠️ openpyxl 不可用,Excel 导出将不可用,但 Markdown 输出正常。` → 继续(不阻塞)

### 检查 3:用户偏好

```
读取 user_knowledge/preferences.json
```

- 存在:解析并记录 `prd_quality_review`、`default_domain`、`max_defect_patterns`、`output_format`
- 不存在:自动创建默认配置(见下方默认值),提示用户 `i️ 已创建默认偏好配置,可在 user_knowledge/preferences.json 中自定义。`
- 文件存在但格式损坏:输出 `⚠️ preferences.json 格式错误,已使用默认配置。`,使用默认值继续,不阻塞流程
- **交互式询问(必须暂停等待用户选择)**:
  - 若用户消息明确包含 `开启PRD审查` / `PRD质量审查能力打开` → 按开关指令处理,不进入主流程
  - 若 `preferences.json` 中 `prd_quality_review == true` → 已开启,直接继续,不询问
  - 若 `prd_quality_review == false` 或未设置 → **暂停并输出以下选项,等待用户回复**:
  ```
  i️ 本技能内置 PRD 质量审查能力:在生成测试用例前,自动对需求文档进行完整性评分,识别缺失项和歧义点,帮助你在测试前发现需求问题。
  当前状态: ⏸️ 未开启(默认)
  请选择:
  • 回复「开启」→ 开启 PRD 质量审查,分析需求后先评分再生成用例,不到合格分数流程强制中断,并输出PRD问题清单
  • 回复「跳过」→ 跳过审查,直接生成测试用例
  ```
  用户回复「开启」→ 将 `preferences.json` 中 `prd_quality_review` 更新为 `true`,继续执行 Step 0.5
  用户回复「跳过」→ 保持 `prd_quality_review` 为 `false`,跳过 Step 0.5,直接进入 Step 1

默认值:
```json
{
  "prd_quality_review": false,
  "default_domain": "trade",
  "max_defect_patterns": 20,
  "output_format": "excel"
}
```

### 检查 4:知识库状态(L5 为空时强制中断)

```bash
exec: ls {SKILL_DIR}/user_knowledge/project/ 2>/dev/null | wc -l
```

- **L5 有文件**:提示「✅ L5 项目知识库已就绪」,继续检查 L6
- **L5 为空**:**暂停并输出以下选项,等待用户回复**:
  ```
  i️ L5 项目知识库为空。
  你可以上传历史需求文档(.docx/.pdf)或包含多个文档的 .zip 包,我会提取项目特有的业务规则和测试经验,显著提升用例质量。
  请选择:
  • 回复「上传」并附上文件 → 解析文档,提取关键信息存入 L5,然后继续
  • 回复「跳过」→ 不导入,直接开始(后续可随时发送文档补充 L5)
  ```
  用户回复「上传」并附文件 → 执行 L5 导入逻辑(解析文档→提取关键信息→存入 user_knowledge/project/),导入完成后继续
  用户回复「跳过」→ 不导入,继续检查 L6

```bash
exec: ls {SKILL_DIR}/user_knowledge/experience/ 2>/dev/null | wc -l
```
- **L6 有文件**:提示「✅ L6 经验库已就绪」
- **L6 为空**:**必须输出以下提示(不可省略)**:
  ```
  i️ L6 经验库为空,生成用例后可将评审结果交给我学习。
  现在开始 Step 0!
  ````}]}

---

---

## 🔴 Onboarding完成门禁

**Onboarding所有检查完成后，必须创建task_id并写入完成标记，否则不得进入Step 0。**

**task_id创建（提前到Onboarding阶段）**：
需求载荷就绪后，在Onboarding完成时立即创建task_id和DATA_DIR，确保onboarding.pass.json能写入正确的task目录。
```bash
exec: python3 -c "
import json, os, time
task_id = 'task_' + time.strftime('%Y%m%d_%H%M%S')
data_dir = os.path.expanduser('~/.openclaw/workspace/data/' + task_id)
os.makedirs(os.path.join(data_dir, 'gates'), exist_ok=True)
# 写入task_meta（基础版，Step 0会补充完整字段）
meta = {'task_id': task_id, 'created_at': time.strftime('%Y-%m-%dT%H:%M:%S+08:00'), 'skill_version': '3.0.0'}
with open(os.path.join(data_dir, 'task_meta.json'), 'w') as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)
print(f'TASK_CREATED:{task_id}')
print(f'DATA_DIR:{data_dir}')
"
```
Agent必须记录输出的task_id和DATA_DIR，后续所有步骤使用这些实际值。

**写入onboarding.pass.json**：
```bash
exec: python3 -c "
import json, os, time
data_dir = '{DATA_DIR}'
os.makedirs(os.path.join(data_dir, 'gates'), exist_ok=True)
onboarding_pass = {
    'step': 'onboarding',
    'task_id': '{task_id}',
    'completed_at': time.strftime('%Y-%m-%dT%H:%M:%S+08:00'),
    'checks_passed': ['file_integrity', 'cache', 'skill_dir', 'python_openpyxl', 'user_prefs', 'knowledge_status'],
    'prd_review_choice': '{user_choice_prd}',
    'l5_choice': '{user_choice_l5}'
}
with open(os.path.join(data_dir, 'gates', 'onboarding.pass.json'), 'w') as f:
    json.dump(onboarding_pass, f, ensure_ascii=False, indent=2)
print('ONBOARDING_PASS:completed')
"
```

- 输出 `ONBOARDING_PASS:completed` → 可以进入Step 0
- 未输出 → 禁止进入Step 0，重新执行Onboarding

---

## 🔴 主流程模式:自动推进(Onboarding完成门禁通过后,从此处开始)

> **Step 0 前置检查**：必须存在 `{DATA_DIR}/gates/onboarding.pass.json` 且 task_id 一致，否则禁止进入主流程。
>
> **自动推进规则（顶层协议优先，与本文件中任何旧表述冲突时以此为准）**：
> - Step 0 到 Step 7 按顺序自动推进，不得在步骤之间等待用户输入
> - 每步完成后的动作链：写入文件 → truncation_guard校验 → 输出1行状态 → 自动推进下一步
> - 每个Step独立执行，禁止在单个exec中合并多个Step的逻辑
> - Step 0.5 发现blocker时：暂停让用户选择[1]中断/[2]转PCI继续（合法交互）
> - 如果回复因output token耗尽被截断，用户发送"继续"时按gate pass恢复

