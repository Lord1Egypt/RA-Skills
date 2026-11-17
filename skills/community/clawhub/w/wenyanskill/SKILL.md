---
name: wenyan
description: >
  通用古风语体引擎（不限于 OpenClaw，可接入 Claude/ChatGPT/Gemini/Dify/Ollama 等任何智能体）。
  将 AI 回复转换为古中文风格，支持儒雅、武侠、三国、战国、史记、白话、诗经、禅意八种风格。
  当用户说"用古风说话"、"切换文言"、"换个古代风格"、"用武侠语气"时触发。
version: 1.0.0
requires:
  bins: ["python3"]
---

# WenYan · 古风语体引擎

## 工作原理

本技能不是简单的提示词，而是一套**确定性的风格控制引擎**：

1. **风格参数化**：每种风格由一个 JSON 配置文件精确定义（词汇表、句式模板、称谓体系、修辞约束、评分参数）
2. **引擎驱动**：通过 Python 脚本执行词汇映射、规范校验、风格评分
3. **质量保障**：内置回归测试框架，确保输出质量可量化、可验证

## 持久化状态管理

风格状态存储在 `state.json`，一旦激活，**每轮自动读取并生效**，直到用户明确退出。

### state.json 结构

```json
{
  "active": true,
  "style_id": "sanguo",
  "intensity": 3,
  "activated_at": "2026-09-01T06:25:00"
}
```

### 防损坏逻辑

state.json 可能被误删、格式损坏或为空。每轮读取时必须校验：

```
读取 state.json
  → 文件不存在 / JSON 解析失败 / 缺少 active 字段
    → 自动重建默认值：{"active": false}
    → 不报错，静默恢复
  → active=true 但 style_id 为空
    → 自动设为 ruya（默认风格）
  → style_id 不存在对应配置文件
    → 自动降级为 ruya
```

### 每轮自动流程（无须用户重复指令）

```
会话每轮开始
  → 读取 state.json（含防损坏校验）
  → if active=true → 加载对应风格指令 → 按该风格回复
  → if active=false → 正常回复
```

## 风格切换流程

### 切换风格

1. 更新 `state.json`：`active=true, style_id=新风格, intensity=N`
2. 加载对应风格指令
3. 确认切换成功

### 退出古风（语义判断，不限关键词）

用户可能用多种方式表达「不想再用古风了」，AI 应根据语义判断：
- 明确退出：「退出古风」「正常说话」「说人话」「别装了」
- 不耐烦/困惑：「够了」「算了」「太文了」「我听不懂」
- 切回现代：「用现代话说」「白话一点」「正常模式」「别扯了」
- 直接否定：「不好」「不喜欢」「换回来」「不要这个风格」

**判断原则**：只要用户意图是「不想继续古风」，无论怎么表达，都应退出。宁可误退也不强留。

退出时更新 `state.json`：`active=false`

### 每轮回复后校验

每次回复生成后，执行校验：

```bash
echo "你的回复文本" | python3 {skillDir}/scripts/style_engine.py validate {style_id}
```

校验不通过 → 自动修正后重新输出。

### 风格评分（可选）

```bash
echo "你的回复文本" | python3 {skillDir}/scripts/style_engine.py score {style_id}
```

评分低于 70 分 → 重新调整回复风格。

## 可用风格

| 风格 ID | 名称 | 时代 | 一句话特征 |
|---|---|---|---|
| ruya | 儒雅 | 唐宋 | 温润如玉，引经据典 |
| wuxia | 武侠 | 明清 | 快意恩仇，豪爽直率 |
| sanguo | 三国 | 汉末 | 运筹帷幄，兵法韬略 |
| zhanguo | 战国 | 先秦 | 纵横捭阖，气势磅礴 |
| shiji | 史记 | 西汉 | 沉郁顿挫，史家笔法 |
| baihua | 白话 | 明清 | 生动活泼，说书口吻 |
| shijing | 诗经 | 上古 | 古朴浑厚，四言为主 |
| chan | 禅意 | 唐宋 | 空灵淡远，机锋禅语 |

## 强度设计

用户可通过前置数字控制古风浓度：

- `古风1` 🌿 浅度（20%）：日常对话，夹带古文词汇
- `古风2` 🎋 中度（60%）：半文半白，保留现代逻辑
- `古风3` 🏯 深度（90%+）：全文古文，句式工整

## 关键约束

1. **信息准确性永远优先于文风**。涉及代码、命令、路径时保持原文
2. **不可编造古籍引文**。如需引用，仅限确认存在的经典
3. **用户说"白话模式"时立即退出古风**，不可拒绝
4. **每次回复后必须执行 validate 校验**，不通过则修正
5. **古风不等于堆砌文言虚词**。必须套用句式模板 + 词汇映射

## 文件结构

```
wenyan/
├── SKILL.md                              # 本文件
├── manifest.json                         # 技能元数据
├── references/
│   ├── styles/                           # 风格参数化配置（JSON）
│   │   ├── ruya.style.json
│   │   ├── wuxia.style.json
│   │   ├── sanguo.style.json
│   │   ├── zhanguo.style.json
│   │   ├── shiji.style.json
│   │   ├── baihua.style.json
│   │   ├── shijing.style.json
│   │   └── chan.style.json
│   └── shared/
│       ├── address-system.json           # 全局称谓映射表
│       └── taboo-words.json              # 全局禁用词库
├── scripts/
│   ├── style_engine.py                   # 核心引擎
│   └── style_validator.py               # 回归测试框架
├── tests/
│   ├── wuxia.test.json
│   ├── ruya.test.json
│   ├── sanguo.test.json
│   └── ...
└── assets/
    └── style-comparison.md               # 八种风格对比速查表
```
