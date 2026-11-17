# 翻译质量自检清单

完成歌词翻译后，按本清单逐项检查。每项都通过即为合格译文。

## 目录

1. [完整性检查](#1-完整性检查)
2. [准确性检查](#2-准确性检查)
3. [流畅性检查](#3-流畅性检查)
4. [可唱性检查](#4-可唱性检查)
5. [押韵检查](#5-押韵检查)
6. [文化处理检查](#6-文化处理检查)
7. [人设语气检查](#7-人设语气检查)
8. [格式规范检查](#8-格式规范检查)
9. [自动验证脚本](#9-自动验证脚本)

---

## 1. 完整性检查

### 必查项

- [ ] 每行原文都有对应译文（除非是纯音乐段）
- [ ] 段落标记 [Verse]/[Chorus]/[Bridge] 等原样保留
- [ ] 译注编号连续无遗漏（注1、注2、注3...）
- [ ] 副歌重复段每次都完整翻译（不要"同上"）
- [ ] 演唱者标记 [Verse 1: Justin Bieber] 等保留

### 检查方法

```python
# 行数对比
orig_lines = original.strip().split('\n')
trans_lines = translation.strip().split('\n')

# 过滤空行和段落标记
orig_real = [l for l in orig_lines if l.strip() and not l.strip().startswith('[')]
trans_real = [l for l in trans_lines if l.strip() and not l.strip().startswith('[')]

assert len(orig_real) == len(trans_real), f"行数不匹配: 原文 {len(orig_real)} 行, 译文 {len(trans_real)} 行"
```

### 常见问题

- **遗漏行**：原文有的行译文没有 → 补译
- **多余行**：译文有的行原文没有 → 删除
- **段落标记丢失**：[Chorus] 没保留 → 补回

---

## 2. 准确性检查

### 必查项

- [ ] 关键名词翻译正确（人名、地名、专有名词）
- [ ] 关键动词未误译（如 "kill" 不要译为"治愈"）
- [ ] 否定句保持否定（"don't" 不要译为"请"）
- [ ] 时态基本一致（过去时不要变现在时）
- [ ] 数字与单位正确
- [ ] 比喻/隐喻未丢失

### 检查方法

逐行对照，重点检查：

1. 主语是否清晰（英文歌词常省略主语）
2. 否定词是否准确传达
3. 修饰关系是否正确（定语前置/后置）
4. 暗喻是否保留

### 案例

原文：`I heard that your dreams came true`
错译：`我听说你的梦想破灭了`
正译：`听说你的梦想成真了`

错误原因：将 "came true"（实现）误译为"破灭"。

---

## 3. 流畅性检查

### 必查项

- [ ] 无翻译腔（如"被...所"被动句、"是的,..."开头）
- [ ] 句式符合中文习惯（主谓宾顺序、修饰语位置）
- [ ] 用词自然（避免书面语与口语混用）
- [ ] 无生造词
- [ ] 标点正确（中文用中文标点）

### 翻译腔典型反例

| 翻译腔 | 自然中文 |
|--------|---------|
| 被风吹拂着 | 风吹过 |
| 是的，我同意 | 我同意 |
| 在...的时候 | ...时 |
| 关于...的问题 | 关于... |
| ...的事实 | ... |
| 一个...的男孩 | 一个男孩 |

### 检查方法

读一遍译文，凡读到拗口处，标记后重译。

---

## 4. 可唱性检查

### 必查项

- [ ] 每行音节数与原文差距 ≤ ±2
- [ ] 逗号/断句位置与原文对应
- [ ] 重音音节对应（高级要求）
- [ ] 闭口音/开口音选择合理

### 音节数检查脚本

```python
def count_syllables_chinese(text):
    """估算中文字数（每字约一音节）"""
    return len([c for c in text if c.strip() and not c in '，。！？、；：'])

def count_syllables_english(text):
    """估算英文音节数"""
    import re
    words = re.findall(r'\b\w+\b', text.lower())
    # 简化估算：每个元音组算一个音节
    syllables = 0
    for word in words:
        vowel_groups = re.findall(r'[aeiouy]+', word)
        syllables += max(1, len(vowel_groups))
    return syllables

# 检查
for orig_line, trans_line in zip(orig_lines, trans_lines):
    orig_count = count_syllables_english(orig_line) if is_english else count_syllables_chinese(orig_line)
    trans_count = count_syllables_chinese(trans_line)
    diff = abs(orig_count - trans_count)
    if diff > 2:
        print(f"音节差距过大: {orig_line} ({orig_count}) vs {trans_line} ({trans_count}), 差距 {diff}")
```

### 边界

- **抒情慢歌**：可适当放宽（差 3-4 字可接受）
- **快节奏歌**：严格（差 1-2 字以内）
- **说唱**：可不严格匹配，但保留节奏感

---

## 5. 押韵检查

### 必查项

- [ ] 副歌（Chorus）部分押韵（AABB 或 ABAB）
- [ ] 主歌（Verse）可不押韵但读起来顺口
- [ ] 桥段（Bridge）可换韵制造转折
- [ ] 整首歌用韵统一（不要中途换韵除非有意）

### 押韵检测脚本

```python
def check_rhyme(lines, expected_pattern='AABB'):
    """检查中文押韵"""
    # 取每行末字
    end_chars = [line.strip()[-1] if line.strip() else '' for line in lines]
    
    # 中文韵母分类（简化）
    rhyme_groups = {
        'a': ['a', 'ia', 'ua'],
        'o': ['o', 'uo'],
        'e': ['e', 'ie', 'üe'],
        'i': ['i', 'ü'],
        'u': ['u'],
        'an': ['an', 'ian', 'uan', 'üan'],
        'en': ['en', 'in', 'un', 'ün'],
        'ang': ['ang', 'iang', 'uang'],
        'eng': ['eng', 'ing', 'ong', 'iong'],
    }
    
    # 简化：检查每行末字是否同韵
    # 实际应用需更复杂拼音分析
    pass
```

### 案例

原文（Imagine 副歌，押 /u:/ 韵）：
```
You may say I'm a dreamer
But I'm not the only one
I hope someday you'll join us
And the world will be as one
```

译文（押 un 韵）：
```
你可能觉得我在作梦  (meng)
但是我不是唯一这么想的人  (ren)
希望有一天，你也能加入我们  (men)
这个世界再也没有分裂的国家、对立的阵营  (ying - 失韵)
```

最后一行失韵，需要调整：
```
这个世界再也没有分裂、对立的人群  (qun - 押韵)
```

---

## 6. 文化处理检查

### 必查项

- [ ] 文化典故已加注释
- [ ] 文化符号词（oppa, senpai）保留原文
- [ ] 历史事件/人物有背景说明
- [ ] 宗教词汇处理得当（"Hallelujah" 意译为"赞美主"）
- [ ] 方言/俚语有意译或注释

### 检查清单

| 原文元素 | 处理方式 | 注释 |
|---------|---------|------|
| 圣经典故 | 意译 + 脚注 | 必要 |
| 希腊神话 | 直译或意译 | 视知名度 |
| 日本神话/佛教 | 直译 + 脚注 | 必要 |
| 现代俚语 | 意译 | 可选 |
| 历史事件 | 保留 + 脚注 | 必要 |
| 文化符号 | 保留原文 | 不需 |

---

## 7. 人设语气检查

### 必查项

- [ ] 偶像曲的甜腻语气已传达（语气词"呀"、"哦"）
- [ ] 说唱的硬核感已传达（短句、爆破音）
- [ ] 民谣的疏淡感已传达（用词朴素）
- [ ] 抒情歌的浪漫感已传达（用词诗意）
- [ ] 叛逆歌曲的冲击力已传达（用词直接）

### 人设识别信号

| 人设类型 | 识别信号 | 译文处理 |
|---------|---------|---------|
| 甜腻偶像 | 「だわ」「のよ」「かしら」 | 加"呀"、"哦" |
| 硬核说唱 | 短句、爆破音、俚语 | 短句、爆破字、意译俚语 |
| 抒情歌手 | 长句、形容词多 | 诗化中文、修饰丰富 |
| 民谣歌手 | 简单词、叙事性强 | 朴素中文、保留叙事 |
| 叛逆少年 | 短句、感叹号、俚语 | 短促有力、加感叹号 |
| 心碎者 | 反复、感叹、停顿 | 保留反复、用省略号 |

### 案例

错例：Billie Eilish《Bad Guy》译为"我才是坏人"——丧失挑衅感
正译："我才是那个反派 哼"——加"哼"传达挑衅

---

## 8. 格式规范检查

### 必查项

- [ ] 段落标记格式统一（[Verse 1] 不要 [verse 1] 或 [Verse1]）
- [ ] 空行使用一致（每行原词+译文间是否空行）
- [ ] 标点统一（中文用中文标点，英文用英文标点）
- [ ] 注释编号格式统一（注1 vs 注一 vs [1]）
- [ ] 字符编码正确（无乱码、无 escape 序列）

### 格式标准

```
[Section Marker]

原文行
译文行

原文行
译文行

[Next Section]
...

---

### 译注

注1：内容
注2：内容
```

---

## 9. 自动验证脚本

skill 内置验证脚本，位于 `scripts/validate_translation.py`：

```bash
python /home/z/my-project/skills/song-translation-expert/scripts/validate_translation.py \
    original.txt translated.txt
```

### 脚本检查项

1. 行数对齐
2. 段落标记保留
3. 拟声词一致处理
4. 音节数差距
5. 注释完整性
6. 翻译腔检测（简单关键词匹配）
7. 重复段检查

### 输出示例

```
✓ 行数对齐: 36/36
✓ 段落标记保留: 5/5
✓ 拟声词一致: 通过
⚠ 音节数差距: 3 行超过 ±2 (Line 5: 8 vs 11, Line 12: 6 vs 9, Line 23: 10 vs 13)
✓ 注释完整: 3/3
✓ 翻译腔检测: 通过
✓ 重复段检查: 通过

总体评分: 85/100
建议: 优化第 5, 12, 23 行的音节数
```

### 评分标准

- 90-100: 优秀
- 80-89: 良好（建议小修）
- 70-79: 合格（建议中等修改）
- < 70: 不合格（建议重译）

---

## 总结

质量自检是 skill 输出前的最后一道关卡。每条规则都对应一个真实的翻译失败案例，不可跳过。

对于追求极致质量的用户，建议：

1. 翻译完成后跑一遍 `validate_translation.py` 脚本
2. 根据脚本提示逐项修复
3. 重新跑脚本直到 90 分以上
4. 最后人工读一遍译文，确认无翻译腔

对于普通用户，至少完成清单的前 5 项必查项即可输出。
