#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说正文清洗工具：格式清洗与代词优化
用法：python novel-text-cleaner.py 输入文件.txt [输出文件.txt]
不指定输出文件则原地覆盖。

规则一：去除行首短标签+中文冒号，末尾补中文句号
规则二：英文直引号→中文弯引号
规则三：减少代词"她/他/它"过度出现，用名字替换
"""

import re
import os
import sys

# ========== 全局参数 ==========
MAX_PREFIX_LEN = 4
PRONOUN_WINDOW = 150
MAX_COUNT = 1

# ========== 动作动词列表 ==========
ACTION_VERBS = [
    "说道", "喊道", "笑道", "哭道", "叹道", "答道", "问道", "怒道",
    "点了点头", "摇了摇头", "皱了皱眉", "叹了口气", "翻了翻白眼",
    "说", "道", "喊", "笑", "哭", "叹", "答", "问", "怒",
    "想", "看", "走", "坐", "站", "跑", "跳", "抓", "拉", "推",
]
ACTION_VERBS.sort(key=len, reverse=True)

# ========== 非名字排除词 ==========
NON_NAME_WORDS = set("""
然后 于是 所以 因为 但是 不过 虽然 如果 这时 那时 突然 忽然 接着 终于
果然 竟然 居然 显然 自然 当然 忽然 原来 后来 随后 此刻 同时 之后 之前
仿佛 好像 似乎 简直 甚至 尤其 特别 已经 曾经 刚才 刚刚 马上 立刻 立即
慢慢 渐渐 缓缓 轻轻 悄悄 默默 静静 什么 怎么 这个 那个 这些 那些 自己
这里 那里 这边 那边 上面 下面 前面 后面 里面 外面 旁边 中间 对面 到处
一种 一个 一些 一点 一样 一番 一头 大家 我们 你们 他们 她们 它们 咱们
别人 他人 对方 双方 各自 彼此 互相
信封 内容 信件 桌子 房间 门口 窗边 肩膀 背影 故事 事情 东西 问题 办法
时候 地方 样子 声音 眼睛 眼泪 心情 感觉 想法 道理 原因 结果 过程
一点 一下 一声 一句 一步 一眼 一手 手中 脸上 头上 身上 心中 心里
门前 门后 窗前 窗外 桌上 房中
""".split())

# ========== 姓氏白名单 ==========
SURNAMES = set("""
赵 钱 孙 李 周 吴 郑 王 冯 陈 褚 卫 蒋 沈 韩 杨 朱 秦 尤 许 何 吕 施 张 孔 曹 严 华 金 魏
陶 姜 戚 谢 邹 喻 柏 水 窦 章 云 苏 潘 葛 奚 范 彭 郎 鲁 韦 昌 马 苗 凤 花 方 俞 任 袁 柳
酆 鲍 史 唐 费 廉 岑 薛 雷 贺 倪 汤 滕 殷 罗 毕 郝 邬 安 常 乐 于 时 傅 皮 卞 齐 康 伍 余
元 卜 顾 孟 平 黄 和 穆 萧 尹 姚 邵 堪 汪 祁 毛 禹 狄 米 贝 明 臧 计 伏 成 戴 谈 宋 茅 庞
熊 纪 舒 屈 项 祝 董 梁 杜 阮 蓝 闵 席 季 麻 强 贾 路 娄 危 江 童 颜 郭 梅 盛 林 刁 钟 徐
邱 骆 高 夏 蔡 田 樊 胡 凌 霍 虞 万 支 柯 昝 管 卢 莫 经 房 裘 缪 干 解 应 宗 丁 宣 贲 邓
郁 单 杭 洪 包 诸 左 石 崔 吉 钮 龚 程 嵇 邢 滑 裴 陆 荣 翁 荀 羊 於 惠 甄 曲 家 封 芮 羿
储 靳 汲 邴 糜 松 井 段 富 巫 乌 焦 巴 弓 牧 隗 山 谷 车 侯 宓 蓬 全 郗 班 仰 秋 仲 伊 宫
宁 仇 栾 暴 甘 钭 厉 戎 祖 武 符 刘 景 詹 束 龙 叶 幸 司 韶 郜 黎 蓟 薄 印 宿 白 怀 蒲 台
从 鄂 索 咸 籍 赖 卓 蔺 屠 蒙 池 乔 阴 郁 胥 能 苍 双 闻 莘 党 翟 谭 贡 劳 逄 姬 申 扶 堵
冉 宰 郦 雍 却 璩 桂 濮 牛 寿 通 边 扈 燕 冀 郏 浦 尚 农 温 别 庄 柴 瞿 阎 充 慕 连
茹 习 宦 艾 鱼 容 向 古 易 慎 戈 廖 庾 终 暨 居 衡 步 都 耿 满 弘 匡 国 文 寇 广 禄 阙 东
欧 殳 沃 利 蔚 越 夔 隆 师 巩 厍 聂 晁 勾 敖 融 冷 訾 辛 阚 那 简 饶 空 曾 毋 沙 乜 养 鞠
须 丰 巢 关 蒯 相 查 后 荆 红 游 竺 权 逯 盖 益 桓 公
万俟 司马 上官 欧阳 夏侯 诸葛 闻人 东方
赫连 皇甫 尉迟 公羊 澹台 公冶 宗政 濮阳 淳于 单于 太叔 申屠 公孙 仲孙 轩辕 令狐 钟离 宇文 长孙
慕容 鲜于 闾丘 司徒 司空 亓官 司寇 仉 督 子车 颛孙 端木 巫马 公西 漆雕 乐正 壤驷 公良 拓跋 夹谷
宰父 谷梁 晋 楚 闫 法 汝 鄢 涂 钦 段干 百里 东郭 南门 呼延 归 海 羊舌 微生 岳 帅 缑 亢 况 后
有 琴 梁丘 左丘 东门 西门 商 牟 佘 佴 伯 赏 南宫 墨 哈 谯 笪 年 爱 阳 佟 第五
""".split())

PRONOUNS = ["她", "他", "它"]


def rule1_remove_prefix(text, max_prefix_len=MAX_PREFIX_LEN):
    """规则一：去除行首短标签+中文冒号，末尾补中文句号"""
    lines = text.split('\n')
    result = []
    pattern = re.compile(r'^(\s*).{1,' + str(max_prefix_len) + r'}：(.+)$')
    
    for line in lines:
        m = pattern.match(line)
        if m:
            indent = m.group(1)
            content = m.group(2)
            if content and content[-1] in '。！？…':
                content = content[:-1] + '。'
            elif content:
                content = content + '。'
            result.append(indent + content)
        else:
            result.append(line)
    
    return '\n'.join(result)


def rule2_quotes(text):
    """规则二：英文直引号→中文弯引号，逐字符交替替换"""
    result = []
    open_quote = True
    for ch in text:
        if ch == '"':
            result.append('\u201c' if open_quote else '\u201d')
            open_quote = not open_quote
        else:
            result.append(ch)
    return ''.join(result)


def rule3_pronoun_replace(text, window=PRONOUN_WINDOW, max_count=MAX_COUNT):
    """规则三：减少代词过度出现，用名字替换"""
    names = set()
    for verb in ACTION_VERBS:
        pattern = re.compile(r'([\u4e00-\u9fff]{2,4})' + re.escape(verb))
        for m in pattern.finditer(text):
            candidate = m.group(1)
            if candidate in NON_NAME_WORDS:
                continue
            is_valid = any(candidate.startswith(s) for s in SURNAMES)
            if is_valid and len(candidate) >= 2:
                names.add(candidate)
    
    if not names:
        return text
    
    pronoun_associations = {"她": [], "他": [], "它": []}
    sorted_names = sorted(names, key=len, reverse=True)
    
    for name in sorted_names:
        associated = False
        for m in re.finditer(re.escape(name), text):
            pos = m.end()
            window_text = text[pos:pos+200]
            for pronoun in PRONOUNS:
                pm = re.search(re.escape(pronoun), window_text)
                if pm:
                    between = window_text[:pm.start()]
                    has_other = any(other != name and other in between for other in sorted_names)
                    if not has_other and name not in pronoun_associations[pronoun]:
                        pronoun_associations[pronoun].append(name)
                        associated = True
                        break
            if associated:
                break
        if not associated and name not in pronoun_associations["他"]:
            pronoun_associations["他"].append(name)
    
    for pronoun in PRONOUNS:
        positions = [(m.start(), m.end()) for m in re.finditer(re.escape(pronoun), text)]
        if not positions:
            continue
        
        replacements = []
        window_start = 0
        
        for idx, (pos, end) in enumerate(positions):
            while window_start < len(positions) and positions[window_start][0] < pos - window:
                window_start += 1
            count_in_window = idx - window_start + 1
            if count_in_window > max_count and count_in_window % 2 == 0:
                replacement = _find_name(text, pos, pronoun, pronoun_associations, sorted_names)
                if replacement:
                    replacements.append((pos, end, replacement))
        
        for pos, end, name in reversed(replacements):
            text = text[:pos] + name + text[end:]
    
    return text


def rule4_dialogue_format(text):
    """规则四：对话格式规范化，将归属词移到引号前
    匹配："对话内容"归属词，"后续对话"
    替换为：归属词"对话内容后续对话"
    """
    # 处理英文引号
    pattern_en = r'"([^"]*)"(?:.*?说?，?)，?(.*?)"([^"]*)"'
    text = re.sub(pattern_en, r'\2"\1\3"', text)
    
    # 处理中文引号
    pattern_cn = r'“([^”]*)”(?:.*?说?，?)，?(.*?)“([^”]*)”'
    text = re.sub(pattern_cn, r'\2“\1\3”', text)
    
    return text


def _find_name(text, pronoun_pos, pronoun, associations, all_names):
    before = text[:pronoun_pos]
    assoc = associations.get(pronoun, [])
    best, best_pos = None, -1
    for name in assoc:
        p = before.rfind(name)
        if p > best_pos:
            best_pos, best = p, name
    if best:
        return best
    for name in all_names:
        p = before.rfind(name)
        if p > best_pos:
            best_pos, best = p, name
    return best


def process_text(text, enable_rule1=True, enable_rule2=True, enable_rule3=True, enable_rule4=True):
    if enable_rule1:
        text = rule1_remove_prefix(text)
    if enable_rule2:
        text = rule2_quotes(text)
    if enable_rule3:
        text = rule3_pronoun_replace(text)
    if enable_rule4:
        text = rule4_dialogue_format(text)
    return text


def main():
    if len(sys.argv) < 2:
        print("Usage: python novel-text-cleaner.py input.txt [output.txt]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path
    
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    result = process_text(text)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"Done: {len(text)} -> {len(result)} bytes")


if __name__ == "__main__":
    main()
