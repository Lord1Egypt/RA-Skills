# SCI学术翻译润色

**将中文学术论文转化为native级别的发表级英文**

---

## 概述

这不是翻译，是**跨语言学术写作**。

忘记原文的形式，只保留意思。用英语思考，用英语写作。

支持 **Nature、IEEE、ACM、APA** 等主流期刊风格。

---

## 核心功能

### 三层解耦方法论
```
第一层：语义提取 → 去除中文修辞，保留核心意思
第二层：逻辑重构 → 归纳式转演绎式，PEEL结构
第三层：原生写作 → 不看原文，用英语写英语
```

### 4级术语策略
| 级别 | 情况 | 做法 |
|------|------|------|
| Level 1 | 有标准翻译 | 直接用 |
| Level 2 | 有近似概念 | 借用+首次解释 |
| Level 3 | 无对应概念 | 自创+定义 |
| Level 4 | 文化特有 | 拼音+解释 |

### 期刊风格适配
- **Nature/Science**: 主动语态，短句，结果优先
- **IEEE/ACM**: 正式，被动语态可接受，方法导向
- **APA**: 客观严谨，模糊限制语使用频繁

### 6步执行工作流
1. **预处理分析** → 确定期刊类型，创建术语表
2. **语义提取** → 提取核心意思，丢掉中文形式
3. **逻辑重构** → PEEL结构，演绎逻辑
4. **原生写作** → 不看原文，只看大纲
5. **质量验证** → 三类检查清单
6. **最终润色** → 朗读、精简、强化动词

---

## 资源库

### 20个专业示例
覆盖5个领域：
- 医学（Nature Medicine, The Lancet, JCI, NEJM）
- 计算机科学（NeurIPS/ICML, IEEE, ACM）
- 教育学（APA, BJET, Higher Education）
- 工程学（ASCE, ASME, IEEE Power Electronics）
- 社会科学（AER, ASR, International Organization）

每个示例包含：
- 原文中文段落
- ❌ 翻译腔版本（展示常见错误）
- ✅ Native English版本（专业润色后）
- 关键改进点说明

### 12个参考文档
| 文档 | 内容 |
|------|------|
| 常见翻译错误汇总 | 词汇/句式/结构/逻辑层面错误 |
| 术语翻译数据库 | 5领域常用术语标准翻译 |
| 学术过渡词库 | 8类关系的过渡表达 |
| 模糊限制语策略 | 如何表达学术谨慎 |
| 摘要写作指南 | 结构化/非结构化摘要模板 |
| 讨论部分写作指南 | 5段式讨论结构 |
| 回复审稿人信指南 | 礼貌但坚定的回复模板 |
| 引用格式对比 | APA/MLA/Chicago/IEEE/Nature |
| 学术写作通用指南 | 句子/段落/整体层面规范 |
| Nature投稿风格 | Nature期刊格式要求 |
| IEEE投稿风格 | IEEE期刊格式要求 |
| APA投稿风格 | APA期刊格式要求 |

### 7个提示词模板
- 全文翻译
- 摘要翻译
- 讨论部分翻译
- 回复审稿人
- Cover Letter
- 方法部分翻译
- 结果部分翻译

---

## 使用方法

### 安装
```bash
npx skills add xioahu1232/sci-translation-polish
```

### 使用示例
```
"帮我把这篇中文论文翻译成适合Nature发表的英文"
"润色这段摘要，目标期刊是IEEE"
"把讨论部分改成native级别的英语"
```

---

## 适用场景

- ✅ 中文学术论文准备投稿国际期刊
- ✅ 学位论文英文版撰写
- ✅ 稿件润色准备投稿
- ✅ 摘要/结论部分按英文学术规范重写
- ✅ 回复审稿人意见

---

## 常见翻译腔问题

| 中文 | ❌ 翻译腔 | ✅ Native English |
|------|----------|-------------------|
| 本文 | this paper | this study / we |
| 大量 | a large number of | numerous / extensive |
| 重要 | important | crucial / significant |
| 通过 | through | via / by / using |
| 研究表明 | research shows | evidence suggests |
| 非常 | very | highly / markedly |

---

## 技术细节

- 格式：SKILL.md（开放标准）
- 兼容：Claude Code, Codex CLI, Cursor, Windsurf, Gemini CLI
- 无需API密钥
- 纯文本技能

---

## 更新日志

### v1.1.0 (2026-04-09)
- ✨ 新增6步执行工作流
- ✨ 新增20个专业示例（5领域）
- ✨ 新增12个参考文档
- ✨ 新增7个提示词模板
- 📝 技能完善度从65分提升至85-90分

---

## 链接

- **虾评**: https://xiaping.coze.site/skill/84ff6d51-aa83-4dd7-901e-282eda8d3980
- **ClawHub**: https://clawhub.ai/skill/sci-translation-polish
- **GitHub**: https://github.com/xioahu1232/sci-translation-polish

---

## 许可证

MIT

---

**记住**：不是翻译，是跨语言学术写作。用英语思考，用英语写作。
