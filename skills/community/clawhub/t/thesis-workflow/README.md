# MBA/学术论文多Agent协作工作流

📝 多Agent协作完成MBA/学术论文写作的完整工作流，支持双版本起草、审核、整合、定稿。

适用于开题报告到毕业论文的全流程。

## 核心功能

- **双版本起草**：版本H（Hermes深度逻辑链）+ 版本O（OpenClaw格式规范）
- **Phase 3 审核**：7个维度严格审核（格式/大纲/内容准确性/查重/学术规范/文献完整/写作语法）
- **Phase 3.5 学术深度评审**：3轮深度审查（宏观结构→分章节→跨章节一致性）
- **Phase 4 整合**：Review Agent 出整合方案，OpenClaw 执行
- **Phase 5 Word输出**：md2docx_strict.py 合规脚本，中英文分离字体

### v1.7 新增：Loop Agent 架构

- **自动推进**：Orchestrator Loop 自动判断下一步动作（Phase 完成 → 下一 Phase / 打回 / 提示用户）
- **自检校验**：Guardrails 脚本 10 项自动化规范检查，Phase 退出前必须 100% 通过
- **智能审核**：审核 Loop 自动重审修订内容，连续 2 轮无新 P0 视为通过
- **人工把关**：4 个强制 Human-in-the-loop 检查点，确保关键决策不跳过

## 适用场景

- MBA毕业论文（战略管理/企业分析类）
- 学术研究报告（竞争战略/行业分析类）
- 需要多轮审核、多版本整合的正式长文

## 快速开始

### 方式一：直接安装

```bash
openclaw skills install git:hehe973781230/thesis-workflow
```

### 方式二：ClawHub

```bash
openclaw skills search "mba thesis workflow"
openclaw skills install thesis-workflow
```

ClawHub 页面：https://clawhub.ai/hehe973781230/thesis-workflow

## 工作流程

```
用户 → Phase 1（确认清单）→ Phase 2（双版本起草）→ Phase 2.5（用户确认）
     → Phase 3（审核）→ Phase 3.5（学术深度评审）→ Phase 4（整合）→ Phase 5（终审定稿）
     → [Phase 5.1 去AI味] → Phase 5.2（Word输出）
```

## v1.7.3 新增

- **Orchestrator 自动推进**：`scripts/orchestrator.py` 决策引擎 + 审核 Loop 自动重审
- **Verification Loop 真实校验**：字体/字号/行距/三线表/加粗残留/参考文献分编 6 项 Word 格式检查
- **Guardrails 10项校验**：章节完整性/字数/引用/标题层级/正文加粗/三线表/表标题位置/合并残留/关键词
- **单元测试**：25 个测试覆盖全部脚本

## 版本说明

| 版本 | 说明 |
|------|------|
| v1.0_*_H_*.md | Hermes版本（深度逻辑链） |
| v1.0_*_O_*.md | OpenClaw版本（格式规范） |
| v2.0_审核*.md | 审核报告 |
| v3.0_整合版.docx | 整合版Word |
| v4.0_终稿.docx | 终稿Word |

## 写作规范

- **引用格式**：GB/T 7714 作者年制（作者, 年）
- **正文字数**：≥3.5万字
- **写作语法**：正文段落禁止 `**加粗**` 强调术语
- **中文字体**：宋体12磅，行距20磅
- **英文字体**：Times New Roman
- **标题字体**：黑体16磅/14磅/13磅

## 技术栈

- OpenClaw subagent (sessions_spawn)
- Hermes CLI (深度推理)
- academic-thesis-review-skill (学术深度评审)
- md2docx_strict.py (Word转换)

## 开源协议

MIT-0 - 免费使用、修改和分发，无需署名

## 作者

GitHub: [hehe973781230](https://github.com/hehe973781230)

---

*如果这个skill对你有帮助，请给个 ⭐*
