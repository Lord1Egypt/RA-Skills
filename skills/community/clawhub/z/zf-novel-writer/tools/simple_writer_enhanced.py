#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版小说写作工具 - Enhanced Simple Writer v4
使用 WorldContextLoader 统一数据源
"""

import argparse
from pathlib import Path
from datetime import datetime

# 添加路径
tools_dir = Path(__file__).parent
workspace_dir = tools_dir.parent.parent.parent
story_dir = workspace_dir / "story"

# 导入 WorldContextLoader
from world_context_loader import WorldContextLoader
from setup_health_check import check_setup_health


def generate_writing_prompt(chapter_num: int, loader: WorldContextLoader):
    """生成写作提示词"""
    
    # 获取上下文
    ctx = loader.get_context(chapter_num)
    
    # 提取数据
    protagonist = ctx['protagonist']
    era_info = ctx['era_info']
    chapter_info = ctx['chapter_info']
    heroine_phases = ctx['heroine_phases']
    style_rules = ctx['style_rules']
    villain = ctx['villain']
    shen_jin_status = ctx['shen_jin_status']
    pending_setups = ctx['pending_setups']
    world_setting = ctx['world_setting']
    prev_summaries = ctx['prev_summaries']
    
    # 前章概要
    prev_summary_text = "无（第一章）"
    if prev_summaries:
        last = prev_summaries[-1]
        # 优先使用 summary 字段,如果不存在则用标题
        prev_summary_text = last['data'].get('summary', f"第{last['chapter']}章：{last['data'].get('title', '')}")
    
    # 前章结尾衔接信息
    prev_ending = loader.load_previous_chapter_ending(chapter_num)
    ending_text = "无（第一章）"
    if prev_ending:
        ending_lines = []
        if prev_ending.get('time'):
            ending_lines.append(f"**时间点：** {prev_ending['time']}")
        if prev_ending.get('scene'):
            ending_lines.append(f"**结尾场景：** {prev_ending['scene']}")
        if prev_ending.get('emotion'):
            ending_lines.append(f"**情绪状态：** {prev_ending['emotion']}")
        if prev_ending.get('last_300_chars'):
            ending_lines.append(f"\n**上一章最后300字：**\n{prev_ending['last_300_chars']}")
        
        if ending_lines:
            ending_text = "\n".join(ending_lines)
    
    # 前章变量（财务、人物、文明）
    prev_variables_text = "无"
    if prev_summaries:
        last = prev_summaries[-1]
        variables = last['data'].get('variables', {})
        if variables:
            lines = []
            for category, items in variables.items():
                if isinstance(items, dict):
                    lines.append(f"**{category}变量：**")
                    for key, value in items.items():
                        lines.append(f"- {key}: {value}")
            if lines:
                prev_variables_text = "\n".join(lines)
    
    # 铺垫健康度检查
    health_result = check_setup_health(ctx['canon'], chapter_num)
    health = health_result['health']
    warnings = health_result['warnings']
    expired = health_result['expired']
    
    # 生成健康度建议
    health_advice = []
    if health['short'] > 10:
        health_advice.append(f"⚠️ 短期铺垫过载（{health['short']}个）,建议本章兑现2-3个")
    if health['medium'] > 15:
        health_advice.append(f"⚠️ 中期铺垫过载（{health['medium']}个）,建议本章兑现1-2个")
    if health['long'] > 5:
        health_advice.append(f"⚠️ 长期铺垫过载（{health['long']}个）,请谨慎创建新铺垫")
    if health['ongoing'] > 3:
        health_advice.append(f"⚠️ 周期铺垫过载（{health['ongoing']}个）")
    
    health_text = f"""**统计：** 短期{health['short']}个 | 中期{health['medium']}个 | 长期{health['long']}个 | 周期{health['ongoing']}个 | 总计{health['total']}个"""
    
    if health_advice:
        health_text += "\n\n**建议：**\n" + "\n".join(health_advice)
    
    # 过期铺垫警告
    expired_text = ""
    if expired:
        expired_lines = ["⚠️ **过期铺垫警告（已超过预期章节+5章）：**"]
        for e in expired:
            expired_lines.append(f"- [{e['id']}] {e['setup'][:40]}...（预期{e['expected']},已过期{e['overdue']}章）")
        expired_text = "\n".join(expired_lines)
    
    # 未兑现铺垫（按类型分组）
    pending_text = "无"
    if pending_setups:
        # 按类型分组
        by_type = {"short": [], "medium": [], "long": [], "ongoing": []}
        for s in pending_setups:
            setup_type = s.get('type', 'medium')
            by_type[setup_type].append(s)
        
        pending_lines = []
        type_names = {"short": "短期", "medium": "中期", "long": "长期", "ongoing": "周期"}
        
        for setup_type in ["short", "medium", "long", "ongoing"]:
            if by_type[setup_type]:
                pending_lines.append(f"\n**{type_names[setup_type]}铺垫：**")
                for s in by_type[setup_type]:
                    payoff_range = s.get('expected_payoff_range', [0, 0])
                    setup_chapter = s.get('created_chapter', s.get('chapter', 0))
                    pending_lines.append(f"- [{s['id']}] 第{setup_chapter}章：{s['setup']}（预期第{payoff_range[0]}-{payoff_range[1]}章兑现）")
        
        pending_text = "\n".join(pending_lines)
    
    # 女主阶段（已移除,改用 Excel 中的 heroine 字段）
    # heroine_text 现在直接从 chapter_info['heroine'] 获取
    
    # 读取级别定义（中文级别 → 英文文件名）
    level_mapping = {
        '青铜': 'BRONZE', '白银': 'SILVER', '黄金': 'GOLD',
        '铂金': 'PLATINUM', '钻石': 'DIAMOND', '王者': 'KING',
        '至尊': 'SUPREME', '主宰': 'LORD'
    }
    # 优先使用 Excel 中的"系统级别",如果存在
    # 否则使用纪元配置
    system_level = chapter_info.get('system_level', '') if chapter_info else ''
    if not system_level:
        system_level = era_info.get('level', '青铜')
    
    # 只有当系统级别是标准级别时,才加载级别定义文件
    level_definition = ""
    level_en = level_mapping.get(system_level)
    if level_en:
        level_file = story_dir / f"LEVEL_{level_en}.md"
        if level_file.exists():
            try:
                with open(level_file, 'r', encoding='utf-8') as f:
                    level_definition = f.read()
            except:
                pass
    
    # 主角状态
    protagonist_state = ctx.get('protagonist_state', {})
    protagonist_state_text = f"""**年龄：** {protagonist_state.get('age', '未知')}岁
**位置：** {protagonist_state.get('location', '未知')}
**状态：** {protagonist_state.get('status', '未知')}
**时间线：** {protagonist_state.get('timeline', '未知')}"""
    
    # 世界设定（精简版,提取关键信息）
    world_setting_summary = ""
    if world_setting:
        # 提取沈烬档案、情绪周期、终局等关键信息
        lines = []
        
        # ⭐ 基础世界观（始终显示）
        lines.append("### 时代背景")
        lines.append("- **时间**：2032-2048年（架空近未来）")
        lines.append("- **世界**：无超自然，无科幻，现实逻辑")
        lines.append("")
        
        lines.append("### 地理")
        lines.append("- **东陆联邦**：全球第二大经济体，强监管金融")
        lines.append("- **临海市**：金融中心（金融岛、西岸新区、北城工业区、临海港）")
        lines.append("- **新港城**：离岸金融中心")
        lines.append("")
        
        lines.append("### 政治架构")
        lines.append("```")
        lines.append("联邦委员会 → 国家资本监管总署 → 金融稳定委员会/战略安全局")
        lines.append("```")
        lines.append("**核心三原则**：银行不可倒、地产不可崩、汇率不可失控")
        lines.append("")
        
        # ⭐ 根据章节号智能显示沈烬信息（核心修复）
        rival_name_in_setting = rival.get('name', '') if villain else ''
        if rival_name_in_setting and rival_name_in_setting in str(world_setting):
            if chapter_num <= 1000:
                # 隐藏期：只显示表象身份，禁止揭露序列宿主 / Hidden phase: only surface identity
                lines.append(f"### {rival_name_in_setting}档案（⚠️ 隐藏期 - 第1-1000章）")
                lines.append(f"- **表象身份**：{rival.get('cover_identity', '海外资本新星')}")
                lines.append("")
                lines.append("🚨 **绝对禁止**：")
                lines.append("- ❌ 禁止提及「序列」「宿主」「文明跃迁」等词汇")
                lines.append(f"- ❌ 禁止暗示{rival_name_in_setting}背后有神秘力量")
                lines.append(f"- ❌ 禁止出现{rival_name_in_setting}的内心独白或视角")
                lines.append(f"- ❌ 禁止让{protagonist_name}「仿佛看到」{rival_name_in_setting}（任何视觉化描写）")
                lines.append("")
                lines.append("✅ **允许**：")
                lines.append("- 作为竞争对手被提及（不超过3次/章）")
                lines.append("- 保持神秘感，但不要过度渲染")
            elif chapter_num <= 2000:
                # 萌芽期：开始暗示，但不揭露 / Sprouting phase: hints but no reveal
                lines.append(f"### {rival_name_in_setting}档案（⚠️ 萌芽期 - 第1001-2000章）")
                lines.append(f"- **表象身份**：{rival.get('cover_identity', '海外资本新星')}")
                lines.append("- **暗示**：他背后似乎有某种更大的力量，但不揭露具体是什么")
                lines.append("- **允许**：模糊暗示，但不出现「序列」「宿主」等词")
            elif chapter_num <= 3000:
                # 揭露期：逐步揭露 / Reveal phase: gradual exposure
                lines.append(f"### {rival_name_in_setting}档案（⚠️ 揭露期 - 第2001-3000章）")
                lines.append(f"- **身份**：{rival.get('true_identity', '阿尔法序列宿主')}")
                lines.append(f"- **哲学对立**：{protagonist_name}=国家优先，{rival_name_in_setting}=资本优先")
            else:
                # 对决期：完整信息 / Final phase: full info
                lines.append(f"### {rival_name_in_setting}档案（对决期 - 第3001章后）")
                lines.append(f"- **身份**：{rival.get('true_identity', '阿尔法序列宿主')}")
                lines.append(f"- **哲学对立**：{protagonist_name}=国家优先/重情，{rival_name_in_setting}=资本优先/无情")
            lines.append("")
        
        # 揭露时间线（始终显示，让 Writer Agent 知道节奏）
        lines.append(f"### 揭露时间线（⚠️ 重要：控制{rival_name_in_setting}身份揭露节奏）")
        lines.append("| 章节 | 阶段 | 对手身份处理 |")
        lines.append("|------|------|--------------|")
        lines.append("| 1-1000 | 隐藏期 | 不揭露对手的真实身份，只作为商业对手出现 |")
        lines.append("| 1001-2000 | 萌芽期 | 开始暗示对手背后的力量，但仍不完全揭露 |")
        lines.append("| 2001-3000 | 揭露期 | 逐步揭露对手真实身份 |")
        lines.append("| 3001-4000 | 对决期 | 完整展现最终对决 |")
        lines.append("")
        
        # 系统真相（根据纪元选择性显示）
        current_era = era_info.get('era', 1) if era_info else 1
        if current_era >= 3:  # 黄金纪元开始暗示
            lines.append("### 系统真相（逐步揭露）")
            lines.append(f"- {protagonist_name}：文明稳态序列（资本服务国家）")
            lines.append(f"- {rival_name_in_setting}：文明跃迁序列（资本凌驾国家）")
            lines.append("")
        
        # 情绪周期（从 world_setting 动态获取 / Get from world_setting dynamically）
        if "情绪周期" in world_setting:
            lines.append("### 情绪周期")
            emotion_cycles = world_setting.get("情绪周期", [])
            for cycle in emotion_cycles:
                lines.append(f"- {cycle}")
            lines.append("")
        
        # 终局（只在后期显示）
        if current_era >= 7:  # 至尊/主宰纪元
            lines.append("### 终局方向")
            lines.append(f"- {rival_name_in_setting}胜出后主动让渡权限，男主成为规则制定者")
            lines.append("- 代价：地球失去宇宙资源优先权，但获得独立发展权")
            lines.append("")
        
        # 三派格局（从 world_setting 动态获取或使用占位符）
        factions = world_setting.get('factions', []) if isinstance(world_setting, dict) else []
        if factions:
            lines.append("### 三派格局")
            for faction in factions:
                lines.append(f"- **{faction.get('name', '')}**：{faction.get('desc', '')}")
        else:
            lines.append("### 势力格局")
            lines.append("- *请参考 canon_bible.json 中的势力设定*")
        
        world_setting_summary = "\n".join(lines)
    
    # 构建人物列表（从上下文获取，避免硬编码）
    protagonist_name = protagonist.get('name', '主角') if protagonist else '主角'
    heroine_name = chapter_info.get('heroine', '') if chapter_info else ''
    rival_name = villain.get('name', '') if villain else ''
    
    character_list = f"- {protagonist_name}：主角,冷静理性"
    if heroine_name:
        character_list += f"\n- {heroine_name}：女主角"
    if chapter_num > 1000 and rival_name:
        character_list += f"\n- {rival_name}：对手"
    
    # 构建提示词
    book_title = ctx.get('book_title', '{BOOK_NAME}')
    core_theme = world_setting.get('core_theme', '{CORE_THEME}') if isinstance(world_setting, dict) else '{CORE_THEME}'
    genre = world_setting.get('genre', '{GENRE}') if isinstance(world_setting, dict) else '{GENRE}'
    
    prompt = f"""# 《{book_title}》第{chapter_num}章写作任务

---

## 固定设定

【核心主题】{core_theme},谁制定规则
【小说类型】{genre},非爽文
【世界观】无超自然力量,系统只提供认知提升
【人物】
{character_list}
【原则】
- 禁止无脑打脸,降智反派、连续碾压
- 必须存在代价
- 每章必须推进变量

---

## 章节模板

【纪元】：{era_info.get('level', '青铜')}{era_info.get('chapters', '')}
【章节位置】：第{chapter_num}章
【上一章核心事件】：{prev_summary_text}
【前章变量状态】：
{prev_variables_text}

---

## 👤 主角当前状态

{protagonist_state_text}

**⚠️ 重要：** 请确保主角年龄与当前时间线一致！

---

## 📖 上一章衔接信息

{ending_text}

**⚠️ 衔接判断：**
- 如果上章是悬念结尾 → 本章开头必须无缝衔接
- 如果需要时间跳跃 → 开头明确说明"X小时后"/"第二天"
- 不要无故跳跃（上章晚上 → 本章突然早上）

---

## 📊 铺垫健康度

{health_text}
{expired_text}

---

【未解决风险】：{pending_text}
【{ctx.get('rival_name', '对手')}当前动作】：{shen_jin_status}
【{heroine_name or '女主'}认知阶段】：初识
【本章目标】：{chapter_info.get('core_event', '') if chapter_info else ''}
【铺垫要求】：创建2-3个新铺垫,兑现1-2个已有短期铺垫

---

## 章节信息

- **章节号**: 第{chapter_num}章
- **标题**: {chapter_info.get('title', '') if chapter_info else ''}
- **核心事件**: {chapter_info.get('core_event', '') if chapter_info else ''}
- **对手**: {chapter_info.get('opponent', '') if chapter_info else ''}
- **女主**: {chapter_info.get('heroine', '') if chapter_info else ''}
- **剧情核心**: {chapter_info.get('plot_core', '') if chapter_info else ''}
- **冲突类型**: {chapter_info.get('conflict_type', '') if chapter_info else ''}
- **系统提示**: {chapter_info.get('system_hint', '') if chapter_info else ''}
- **系统级别**: {chapter_info.get('system_level') if chapter_info and chapter_info.get('system_level') else era_info.get('level', '青铜')}
- **系统定位**: {era_info.get('position', '概率观察者')}
- **核心能力**: {era_info.get('core_ability', '看见风险,但无法改变结果')}
- **已激活属性**: {chapter_info.get('active_attribute', '') if chapter_info else ''}
- **爽点**: {chapter_info.get('cool_point', '') if chapter_info else ''}
- **信息增量**: {chapter_info.get('info_increment', '') if chapter_info else ''}
- **高维片段**: {chapter_info.get('high_dimension', '') if chapter_info else ''}

{f"## 📊 {era_info.get('level', '青铜')}级系统定义\n\n{level_definition}\n" if level_definition else ""}

---

## 🌍 世界设定

{world_setting_summary}

---

## 🎯 铺垫使用规则

**本章必须遵守：**
1. ✅ **每章最多创建 2-3 个新铺垫**
2. ✅ **必须兑现 1-2 个已有的短期铺垫**（优先选择预期章节临近的）
3. ✅ **不要创建无意义的铺垫**（必须有明确的兑现计划）

**铺垫分类：**
- **短期铺垫（short）**：1-5章内解决（如资金问题、具体事件）
- **中期铺垫（medium）**：5-20章内解决（如人物动机、次要谜题）
- **长期铺垫（long）**：20+章解决（如核心谜题、主线秘密）
- **周期铺垫（ongoing）**：持续作用,反复出现（如主要势力线）

**未兑现铺垫列表：**
{pending_text}

---

## 生成要求

- 字数：3000-3500字
- 每段≤6行,对话独立成段
- 每段直接空行,其余不要随便空行
- 不能直接分胜负
- 必须影响至少一个长期变量
- 结尾必须留下结构性悬念

---

## ⚠️ 重要提醒

【章节内容必须包含】
✅ 故事正文（3000-3500字）
✅ 自然融入的系统提示（【系统提示：...】）
✅ 结尾在悬念/转折点（不要总结,不要预告）
✅ 【变量更新】- 必须在正文结束后输出

【变量更新格式】
```
【变量更新】
**金融变量：**
- 流动性变化：[具体金额]
**人物变量：**
- {protagonist_name}情感状态：[变化]
**文明变量：**
- 文明觉醒度：[百分比]
```

---

## 🔄 Continuity 提取

**生成后自动提取（不出现正文中）：**

### 1. 本章创建的铺垫
```
【本章创建的铺垫 (setups)】
{{"id": "setup_xxx", "setup": "铺垫描述"}}
```

### 2. 本章兑现的铺垫
```
【本章兑现的铺垫 (payoffs)】
{{"id": "setup_xxx", "payoff": "兑现内容"}}
```

### 3. 人物弧线变化
```
【人物弧线变化】
{{"角色": "变化描述"}}
```

### 4. 情绪曲线
```
【情绪曲线】
["阶段1→阶段2→阶段3"]
```

---

## 防跑偏自检

- [ ] 是否围绕核心主题？
- [ ] 是否符合现实金融逻辑？
- [ ] 是否存在成本与风险？
- [ ] 是否推进纪元主线？
- [ ] ⚠️ **{rival_name_in_setting or '对手'}使用是否符合当前章节范围？**
  - 第1-1000章：{rival_name_in_setting or '对手'}只能作为商业对手出现，**禁止**揭露真实身份
  - 禁止{rival_name_in_setting or '对手'}的视角/内心独白
  - 禁止「仿佛看到{rival_name_in_setting or '对手'}的脸」等视觉化描写
  - 提及次数不超过3次/章

---

---

## 现在开始生成第{chapter_num}章：{chapter_info.get('title', '') if chapter_info else ''}

【⚠️ 输出格式要求】

**第一行必须是标题行**（用于归档时提取,之后会被删除）：
```
# {chapter_info.get('title', '') if chapter_info else ''}
```

**完整输出格式：**
1. **第一行**：标题行,格式为 `# 章节标题`（例如：`# 主权规则`）
2. **第二行**：空行
3. **第三行开始**：正文内容（3000-3500字）
4. **正文结束**：直接结束在悬念/转折点（不要写"本章完"、"下章预告"）
5. **最后**：写【变量更新】

**正确示例：**
```
# 章节标题

{protagonist_name}站在商场玻璃幕墙前,看着自己的倒影.
十八岁的夏天,他刚刚收到大学录取通知书...

[正文3000-3500字,直接结束在悬念/转折点]

---

【变量更新】
...
```

**❌ 错误示例：**
- 没有标题行 ❌
- 标题行格式错误（如"# 第1章：标题"）❌
- "本章总结：{protagonist_name}意识到..." ❌
- "本章完"、"未完待续" ❌
- **任何章节分割标记 ❌❌❌**
  - `## 一`、`## 二`、`## 三` 等 Markdown 章节
  - `第一部分`、`第二部分`、`第一节`、`第二节` 等
  - `一、`、`二、`、`三、` 等数字分割

**⚠️ 正文必须是一个完整的整体,不要有任何分割感！**
- 正文应该像一篇完整的小说,流畅连贯
- 从开头到结尾一气呵成,不要分成几个"部分"
- 用段落和场景转换来组织内容,而不是用章节标记

---

## 🔄 Continuity 信息输出（必须在【变量更新】之后）

**⚠️ 重要：在【变量更新】之后,必须输出以下信息：**

### 【本章创建的铺垫 (setups)】
列出本章引入的、未来会兑现的线索：
```
【本章创建的铺垫 (setups)】
- 对手公开威胁{protagonist_name},将在三个月内切断其供应链
- 女主借款15万,建立合作关系
- {rival_name_in_setting or '对手'}主动联系{protagonist_name},邀请合作
```

### 【本章兑现的铺垫 (payoffs)】（如果有）
列出本章兑现的、之前章节埋下的伏笔：
```
【本章兑现的铺垫 (payoffs)】
- {protagonist_name}在股东会议上揭露对手负债率75%（对应第1章危机）
- 女主与对手关系紧张,会议上针锋相对（对应第1章铺垫）
```

### 【人物弧线变化】（如果有）
```
【人物弧线变化】
- {protagonist_name}：从被动观察到主动对抗,开始理解规则的本质
- 女主：从观望到支持,开始信任{protagonist_name}
```

---

现在开始生成,第一行必须是标题行.
"""
    
    return prompt


def save_prompt(prompt: str, chapter_num: int):
    """保存提示词到文件"""
    prompts_dir = Path(__file__).parent / "prompts"
    prompts_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = prompts_dir / f"chapter_{chapter_num}_{timestamp}.txt"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    return filepath


def clean_chapter_content(content: str) -> str:
    """
    清理章节内容中的元数据和章节分割标记
    
    清理内容：
    - ## 一、## 二 等 Markdown 章节标记
    - 第一部分、第二部分 等分割描述
    - 一、二、三、 等数字分割（独立成行时）
    - 多余空行（超过2个连续空行）
    """
    import re
    
    # 1. 删除 Markdown 章节标记 (## 一、## 二、## 1、## 2 等)
    content = re.sub(r'^##\s*[\d一二三四五六七八九十]+\s*$', '', content, flags=re.MULTILINE)
    
    # 2. 删除"第X部分"、"第X节"等分割描述
    content = re.sub(r'^第[一二三四五六七八九十\d]+[部分节][\s]*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^[一二三四五六七八九十\d]+[、.．]\s*$', '', content, flags=re.MULTILINE)
    
    # 3. 删除多余空行（超过2个连续空行变为2个）
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # 4. 去除开头和结尾的多余空行
    content = content.strip()
    
    return content


def main():
    parser = argparse.ArgumentParser(description='小说写作工具 v4')
    parser.add_argument('--chapter', type=int, required=True, help='章节号')
    parser.add_argument('--prompt-only', action='store_true', help='只生成提示词')
    args = parser.parse_args()
    
    print("="*70)
    print("           Novel Writer v4")
    print("     (WorldContextLoader 统一数据源)")
    print("="*70)
    
    # 初始化加载器
    loader = WorldContextLoader()
    
    # 获取上下文
    print(f"[1/3] 加载第{args.chapter}章上下文...")
    ctx = loader.get_context(args.chapter)
    
    chapter_info = ctx.get('chapter_info')
    if not chapter_info:
        print(f"[ERROR] 未找到第{args.chapter}章的规划")
        return
    
    print(f"[INFO] 标题: {chapter_info.get('title')}")
    print(f"[INFO] 纪元: {ctx['era_info'].get('level')}")
    print(f"[INFO] 反派: {ctx['villain'].get('name')}")
    
    # 生成提示词
    print(f"[2/3] 生成提示词...")
    prompt = generate_writing_prompt(args.chapter, loader)
    print(f"[INFO] 提示词长度: {len(prompt)} 字符")
    
    # 保存
    print(f"[3/3] 保存提示词...")
    filepath = save_prompt(prompt, args.chapter)
    print(f"[INFO] 已保存: {filepath}")
    
    print("="*70)


if __name__ == "__main__":
    main()