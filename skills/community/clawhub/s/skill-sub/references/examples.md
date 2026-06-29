# skill-sub 使用示例

> 本文档是 SKILL.md 的渐进式补充，提供完整使用示例。

---

## 示例 1：创建发布流水线调用链

```
用户：帮我创建一条发布流水线的调用链，包含安全审计、打包、推送

AI：
  1. 分析意图 → 需要 skills-security-check + 内置打包 + git-sync
  2. 读取技能信息 → 提取关键步骤
  3. 规划步骤：
       步骤1: 安全审计 → 依赖:无 → 里程碑(关键词:审计)
       步骤2: 打包 → 依赖:[1] → 非里程碑
       步骤3: 推送代码 → 依赖:[2] → 里程碑(最后一步)
  4. 展示确认
  5. [配置: naming_mode=auto] → AI 命名为 "发布流水线"
  6. 保存
```

**生成的调用链 JSON：**

```json
{
  "name": "发布流水线",
  "description": "技能发布完整流程",
  "purpose": "一键发布技能到 SkillHub/ClawHub",
  "user_intent": "帮我打包发布这个技能",
  "tags": ["发布", "技能管理"],
  "steps": [
    {
      "index": 1,
      "skill_name": "skills-security-check",
      "step_name": "安全审计",
      "action": "对技能目录执行安全审计，检查敏感信息泄露",
      "skill_instruction": "security-audit",
      "depends_on": [],
      "retry_policy": {"max_retries": 3},
      "failure_mode": {"on_exhaust": "abort", "is_milestone": true}
    },
    {
      "index": 2,
      "skill_name": "(内置)",
      "step_name": "打包",
      "action": "按规范打包为 ZIP（仅含 SKILL.md、_meta.json、scripts/*.py）",
      "depends_on": [1],
      "retry_policy": {"max_retries": 3},
      "failure_mode": {"on_exhaust": "ask", "is_milestone": false}
    },
    {
      "index": 3,
      "skill_name": "git-sync",
      "step_name": "推送代码",
      "action": "推送到 Gitee 和 GitHub 仓库",
      "depends_on": [2],
      "retry_policy": {"max_retries": 3, "error_types": ["network_error", "timeout"]},
      "failure_mode": {"on_exhaust": "ask", "is_milestone": true}
    }
  ]
}
```

---

## 示例 2：执行调用链

```
用户：执行发布流水线

AI：
  1. 生成执行计划 → 3步，2个里程碑
  2. 步骤1（安全审计）→ 第一层 action → ✅成功
  3. 步骤2（打包）→ 第一层 action → ❌文件占用
     → 分级重试: file_locked → 立即重试 → ✅成功
  4. 步骤3（推送代码）→ 第一层 action → ❌网络错误
     → 分级重试: network_error → 5秒后重试 → ✅成功
  5. 汇报: 全部 3/3 步成功
```

---

## 示例 3：查看里程碑判断依据

```
用户：查看发布流水线详情

AI：
  📌 调用链: 发布流水线
  ...
  📐 里程碑判断依据:
       ★ 步骤1(安全审计): 关键词匹配: '审计'
       ○ 步骤2(打包): 默认规则（非关键节点）
       ★ 步骤3(推送代码): 最终交付步骤
```

---

## 示例 4：用 skill-sub 摘取步骤形成调用链

> 注意：skill-sub 本身**不参与**调用链，它只负责摘取其他 skill 的步骤并形成调用链。

**场景**：用户希望将"语义理解 → 规划 → 三步循环执行 → 标准化审查"这套流程固化为调用链。

```
用户：帮我创建一条"标准化执行流水线"调用链

AI：
  1. 分析意图 → 需要 semantic-split + triphasic-execution + skill-standardization
  2. 读取技能信息：
     - semantic-split：提取关键步骤（语义拆分、规划生成）
     - triphasic-execution：提取三步循环步骤
     - skill-standardization：提取审查/改写步骤
  3. 规划步骤：
       步骤1: 语义理解 → 依赖:无 → 非里程碑
       步骤2: 规划步骤 → 依赖:[1] → 非里程碑
       步骤3: 三步循环执行 → 依赖:[2] → 里程碑
       步骤4: 标准化审查 → 依赖:[3] → 里程碑(关键词:审查)
  4. 展示确认
  5. 保存为调用链 "标准化执行流水线"
```

**关键点**：调用链通过 `chain_manager.py` 保存为 JSON 文件，可复用，不绑定某一次具体任务。

---

## 使用技巧

### 命名建议

- **格式**：「动词+对象」（如「发布技能」「审查代码」「生成报告」）
- **避免泛化名**：「通用流程」「测试链」→ 改名为「技能安全审计+发布」「用户注册流程测试」
- **命名即意图**：好的名称让 `list` 一眼能看懂这条链干嘛

### 里程碑配置经验

| 场景 | 建议 |
|------|------|
| 安全/审计/部署步骤 | 必须标里程碑（失败不可接受） |
| 数据生成/中间计算 | 非里程碑 + `on_exhaust: skip` |
| 不确定是否关键 | 暂时非里程碑 + `on_exhaust: ask` |

### 调用链生命周期

1. **创建** → 命名 + 配置依赖 + 验证（`validate`）
2. **试运行** → 用简单场景跑一次，看流程是否顺畅
3. **调整** → 修 action 描述、调重试次数、改里程碑标记
4. **复用** → 同类任务直接执行
5. **清理** → 不再需要的链用 `delete --force` 删除，不用留
