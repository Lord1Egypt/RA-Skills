#!/usr/bin/env python3
"""
analyze.py - 从 observations (visual + audio) 合成 metadata.json

用法:
  python3 analyze.py --observations-visual obs_v.json --observations-audio obs_a.json --output metadata.json --method api|agent|manual

method:
  api   - 使用外部 API(vision/audio LLM)合成(需要 --api-key/--api-base/--model)
  agent - 在当前会话/agent 内用模型合成(本地或远程模型)
  manual- 只把 observations 转成可编辑的 Markdown 供人工审阅

注意:API 调用会把 observations 一并传给模型。
"""

import argparse
import json
import os
import re
import sys
import urllib.request

# 公共工具
from common import http_request_with_retry, parse_json_from_llm, extract_llm_content


def observations_to_markdown(obs_v, obs_a):
    parts = ["# Observations (Visual)", ""]
    for f in obs_v:
        parts.append(f"## {f.get('frame')}")
        parts.append(f"- desc: {f.get('desc')}")
        parts.append(f"- texts: {f.get('texts')}")
        parts.append(f"- objects: {', '.join(f.get('objects', []))}")
        parts.append(f"- actions: {', '.join(f.get('actions', []))}")
        parts.append(f"- style: {f.get('style')}")
        parts.append(f"- cover_candidate: {f.get('cover_candidate')}")
        parts.append("")
    parts.append("# Observations (Audio)")
    parts.append("")
    parts.append(f"transcript:\n{obs_a.get('transcript','')}")
    parts.append("")
    parts.append(f"speakers: {', '.join(obs_a.get('speakers',[]))}")
    parts.append("")
    parts.append(f"key_points:\n- " + "\n- ".join(obs_a.get('key_points',[])))
    parts.append("")
    parts.append(f"tone: {obs_a.get('tone','')}")
    return "\n".join(parts)


def synthesize_agent(obs_v, obs_a):
    """Agent 模式:不调 API,用启发式规则生成基础 metadata。
    适合快速预览或作为 API 模式的 fallback。"""
    # --- 标题 ---
    # 优先从 key_points 取最有信息量的那句,截取到 80 字
    key_points = obs_a.get('key_points', [])
    transcript = obs_a.get('transcript', '')

    title = ''
    if key_points:
        # 取第一个 key_point 作为基础,但尽量让它像人写的
        title = key_points[0]
        if len(title) > 80:
            title = title[:77] + '...'
    elif transcript:
        # 从 transcript 第一句取前 60 字
        first_sentence = transcript.split('。')[0].split(',')[0]
        title = first_sentence[:60]
    else:
        title = obs_v[0].get('desc', '未命名视频')[:60]

    # --- 简介 ---
    # 把 key_points 和 transcript 前几句组合
    intro_parts = []
    if key_points:
        intro_parts.append('\n'.join(f'- {p}' for p in key_points[:5]))
    if transcript:
        # 取 transcript 前几句(最多 500 字)
        sentences = re.split(r'[。!?\n]', transcript)
        intro_text = '。'.join(s for s in sentences if s.strip())[:500]
        intro_parts.append(intro_text)
    intro = '\n\n'.join(intro_parts) if intro_parts else obs_v[0].get('desc', '')

    # --- 标签 ---
    # 从 style + objects + key_points 中提取
    tags = set()
    for f in obs_v:
        for t in (f.get('style') or '').split('/'):
            t = t.strip()
            if t and len(t) <= 20:
                tags.add(t)
        for obj in (f.get('objects') or []):
            if isinstance(obj, str) and len(obj) <= 10:
                tags.add(obj)
    for kp in key_points[:3]:
        # 从 key_points 提取关键词
        for word in re.findall(r'[A-Za-z]+|[\u4e00-\u9fff]{2,6}', kp):
            if len(word) >= 2:
                tags.add(word)
    tags = list(tags)[:10]
    if not tags:
        tags = ['视频']

    # --- 封面建议 ---
    cover_primary = None
    cover_reason = ''
    cover_secondary = None
    for f in obs_v:
        if f.get('cover_candidate'):
            frame_name = f.get('frame', '')
            if not cover_primary:
                cover_primary = frame_name
                desc = f.get('desc', '')
                texts = f.get('texts', '')
                reasons = []
                if texts:
                    reasons.append(f'含文字"{texts[:30]}"')
                if desc:
                    reasons.append(f'画面内容:{desc[:50]}')
                cover_reason = ';'.join(reasons) if reasons else '视觉信息密度高'
            elif not cover_secondary:
                cover_secondary = frame_name

    # --- 分区 (2026-05 B站 type2 平铺分区, 共30个, 无子分区) ---
    # 完整列表: 影视 娱乐 音乐 舞蹈 动画 绘画 鬼畜 游戏 资讯 知识
    #           人工智能 科技数码 汽车 时尚美妆 家装房产 户外潮流 健身
    #           体育运动 手工 美食 小剧场 旅游出行 三农 动物 亲子
    #           健康 情感 vlog 生活兴趣 生活经验
    all_text = ' '.join(f.get('texts', '') + ' ' + f.get('desc', '') for f in obs_v)
    all_text += ' ' + transcript
    category = '科技数码'
    if any(kw in all_text for kw in ['电影', '电视剧', '解说', '影视']):
        category = '影视'
    elif any(kw in all_text for kw in ['综艺', '明星', '八卦']):
        category = '娱乐'
    elif any(kw in all_text for kw in ['AI音乐', 'AI 作曲', 'AI 翻唱']):
        category = '音乐'
    elif any(kw in all_text for kw in ['音乐', '翻唱', '编曲', '弹唱', '乐器', '演唱']):
        category = '音乐'
    elif any(kw in all_text for kw in ['舞蹈', '编舞', '宅舞']):
        category = '舞蹈'
    elif any(kw in all_text for kw in ['动画', '动漫', 'MAD']):
        category = '动画'
    elif any(kw in all_text for kw in ['绘画', '画画', '插画', '素描']):
        category = '绘画'
    elif any(kw in all_text for kw in ['鬼畜', '调教', '音 MAD']):
        category = '鬼畜'
    elif any(kw in all_text for kw in ['手游', '手机游戏', '原神', '星铁']):
        category = '游戏'
    elif any(kw in all_text for kw in ['游戏', '通关', '攻略', '速通', '电竞']):
        category = '游戏'
    elif any(kw in all_text for kw in ['新闻', '时事', '热点']):
        category = '资讯'
    elif any(kw in all_text for kw in ['教程', '教学', '原理', '解析', '讲解', '学习', '课堂']):
        category = '知识'
    elif any(kw in all_text for kw in ['AI', '人工智能', 'LLM', 'GPT', 'Agent', '机器学习', '深度学习']):
        category = '人工智能'
    elif any(kw in all_text for kw in ['编程', '代码', 'Python', 'JavaScript', 'Rust', '开发', '算法']):
        category = '科技数码'
    elif any(kw in all_text for kw in ['电路', '电气', '电压', '电流', '电机', '机械', '工程', '单片机', 'STM32', 'ESP32', 'Arduino', 'PCB', '焊接']):
        category = '科技数码'
    elif any(kw in all_text for kw in ['数码', '手机', '电脑', '笔记本', '显卡', 'CPU', '硬件', '评测']):
        category = '科技数码'
    elif any(kw in all_text for kw in ['汽车', '改装', '赛车', '驾驶']):
        category = '汽车'
    elif any(kw in all_text for kw in ['时尚', '穿搭', '美妆', '护肤']):
        category = '时尚美妆'
    elif any(kw in all_text for kw in ['家装', '装修', '房产', '买房']):
        category = '家装房产'
    elif any(kw in all_text for kw in ['户外', '潮流', '露营', '徒步']):
        category = '户外潮流'
    elif any(kw in all_text for kw in ['健身', '训练', '增肌', '减脂']):
        category = '健身'
    elif any(kw in all_text for kw in ['运动', '篮球', '足球', '体育']):
        category = '体育运动'
    elif any(kw in all_text for kw in ['手工', 'DIY', '制作']):
        category = '手工'
    elif any(kw in all_text for kw in ['美食', '烹饪', '食谱', '做饭', '料理', '烘焙']):
        category = '美食'
    elif any(kw in all_text for kw in ['短剧', '小剧场', '微剧']):
        category = '小剧场'
    elif any(kw in all_text for kw in ['旅游', '旅行', '出行', '攻略']):
        category = '旅游出行'
    elif any(kw in all_text for kw in ['农业', '农村', '三农']):
        category = '三农'
    elif any(kw in all_text for kw in ['宠物', '猫', '狗', '动物']):
        category = '动物'
    elif any(kw in all_text for kw in ['亲子', '育儿', '宝宝']):
        category = '亲子'
    elif any(kw in all_text for kw in ['健康', '医疗', '养生']):
        category = '健康'
    elif any(kw in all_text for kw in ['情感', '恋爱', '心理']):
        category = '情感'
    elif any(kw in all_text for kw in ['Vlog', 'vlog', '记录', '体验']):
        category = 'vlog'
    elif any(kw in all_text for kw in ['搞笑', '整活', '沙雕']):
        category = '生活兴趣'
    elif any(kw in all_text for kw in ['生活', '日常']):
        category = '生活兴趣'

    # --- 创作声明(必选单选,6 选 1,对齐 B 站投稿页) ---
    # 内容无需标注 | 含AI生成内容 | 含虚构演绎内容 | 内容含营销信息 | 个人观点,仅供参考 | 内容为转载
    declaration = '内容无需标注'
    if any(kw in all_text for kw in ['AI生成', 'AI生成内容', 'Sora', 'Runway', 'Midjourney', 'Stable Diffusion', 'Seedream', 'AI视频', 'AI合成', '人工智能合成']):
        declaration = '含AI生成内容'
    elif any(kw in all_text for kw in ['虚构', '演绎', '剧情', '角色扮演']):
        declaration = '含虚构演绎内容'
    elif any(kw in all_text for kw in ['推广', '赞助', '广告', '商单', '带货']):
        declaration = '内容含营销信息'
    elif any(kw in all_text for kw in ['评论', '观点', '看法', '个人观点', '我认为', '我觉得', '评价', '时事', '社会热点', '深度解析']):
        declaration = '个人观点，仅供参考'
    elif any(kw in all_text for kw in ['转载', '搬运', '转自']):
        declaration = '内容为转载'

    # --- 内容授权声明（非必选勾选） ---
    # "内容为自制：未经作者允许，禁止转载"
    # 默认不勾选，仅当视频明确为自制原创时建议勾选
    copyright_claim = False

    # --- 水印（默认开启） ---
    # B站原创水印：显示在视频右上角，防止盗用
    # 默认开启，除非用户明确说明不加水印
    watermark = True

    metadata = {
        'title': title,
        'intro': intro,
        'tags': tags,
        'category': category,
        'cover_suggestion': {
            'primary': cover_primary or obs_v[0].get('frame', ''),
            'reason': cover_reason or '首帧',
            'secondary': cover_secondary or ''
        },
        'declaration': declaration,
        'copyright_claim': copyright_claim,
        'watermark': watermark,
        # 作者声明(非必选,可多选,对齐 B 站 neutral_mark.marks)
        # 可选值:
        #   作者声明:该视频使用人工智能合成技术
        #   作者声明:视频内含有危险行为,请勿轻易模仿
        #   作者声明:该内容仅供娱乐,请勿过分解读
        #   作者声明:该内容可能引人不适,请谨慎选择观看
        #   作者声明:请理性适度消费
        #   作者声明:个人观点,仅供参考
        'author_marks': []  # 由 Agent/API 根据内容判断是否需要添加
    }
    return metadata


SYNTHESIZE_SYSTEM_PROMPT = """你是一位资深的 B 站内容运营,擅长根据视频内容撰写投稿元数据。你的目标受众是 B 站的普通观众,不是机器人。

核心原则:
- **标题是给人看的**:像真实 UP 主写的,不是 AI 概括。要有信息量、有辨识度,让人一眼知道视频讲什么并且想点进来。可以是陈述式、设问式、或带一点个性。严禁空泛套话(如"深入浅出""全面解析""带你了解")。**严禁使用对人物的侮辱性、贬低性或歧视性描述**(如"光头""胖子""矮子"等),应使用中性或尊重的表述(如"主持人""表演者""师傅"等)。
- **简介是给人读的**:让人看完能判断"这个视频跟我有关吗"。用自然语言,可以分段,包含关键信息点。不是摘要,是预告。**严禁使用对人物的侮辱性、贬低性或歧视性描述**,描述人物时使用中性、尊重的称呼。
- **标签从内容中自然长出来**:不要堆砌泛标签,要具体到内容领域。**至少包含 3-4 个二字的短标签**(如:街舞、非遗、魔术、街头),避免全部使用四字或更长的标签。
- **分区要准**:必须综合视觉观测和音频观测两个维度的内容来判断分区,不要只看画面或只听音频。优先选最匹配的一级分区,再在对应子分区中选最贴切的。
- **封面建议要具体**:基于实际画面内容,说清楚为什么这帧好、适合做什么风格。

输出语言:根据视频内容的主要语言输出。中文视频用中文，英文视频用英文，以此类推。技术术语可保留原文。"""

SYNTHESIZE_USER_PROMPT = """## 视觉观测(从视频中抽取的关键帧分析)
{obs_visual}

## 音频观测(语音转写 + 结构化信息)
{obs_audio}

## 任务
根据以上视觉和音频观测,生成 B 站投稿元数据。

严格输出一个 JSON 对象,包含以下字段:

| 字段 | 类型 | 要求 |
|------|------|------|
| title | string | 80字以内。像 UP 主写的标题,有信息量有辨识度,不做标题党。参考示例。**严禁对人物使用侮辱性、贬低性或歧视性描述**(如"光头""胖子""矮子"等),必须使用中性尊重的称呼(如"主持人""表演者""师傅""嘉宾"等)。 |
| intro | string | 2000字以内。给观众看的视频介绍,用自然语言写,让人看完知道视频讲什么。可以分段。**严禁在简介末尾堆砌关键词或搜索词,简介就是简介,不是 SEO 字段。** **严禁对人物使用侮辱性、贬低性或歧视性描述**(如"光头""胖子""矮子"等),必须使用中性尊重的称呼(如"主持人""表演者""师傅""嘉宾"等)。 |
| tags | string[] | 10个以内,每个20字以内。**B站投稿规范要求**:填写与内容相关的标签,包括但不限于涉及的人物、团体、概念、视频本身的属性等。**不要填写与内容不相关或者无意义的标签内容。** 至少包含 3-4 个二字的短标签(如:街舞、非遗、魔术、街头、篮球、手工),避免全部使用四字或更长的标签。 |
| category | string | B站分区 (2026-05 type2 平铺列表, 无子分区), 必须为以下之一: 影视 | 娱乐 | 音乐 | 舞蹈 | 动画 | 绘画 | 鬼畜 | 游戏 | 资讯 | 知识 | 人工智能 | 科技数码 | 汽车 | 时尚美妆 | 家装房产 | 户外潮流 | 健身 | 体育运动 | 手工 | 美食 | 小剧场 | 旅游出行 | 三农 | 动物 | 亲子 | 健康 | 情感 | vlog | 生活兴趣 | 生活经验 |
| cover_suggestion | object | 封面建议:{{ "primary": "最推荐的帧编号+理由", "reason": "为什么这帧适合", "secondary": "备选帧编号+理由" }} |
| declaration | string | 创作声明(必选单选,6选1),必须为以下之一(不能自创):"内容无需标注" | "含AI生成内容" | "含虚构演绎内容" | "内容含营销信息" | "个人观点,仅供参考" | "内容为转载"。**B站社区公约创作声明规范**(严格遵守):\n1. 含有AI生成且可能误导他人的内容 → "含AI生成内容"\n2. 含有剧本、策划、表演等手法制作的虚构情节短剧 → "含虚构演绎内容"\n3. 含有针对时事政治、社会热点或专业问题发表的评论或观点 → "个人观点,仅供参考"\n4. 含有商品或服务购买推荐,或链接分享 → "内容含营销信息"\n5. 含有国内外时事、公共政策、社会事件等信息 → 需注明时间、地点或参考信源(但声明仍从上述6项中选)\n**注意**:街头表演、打赏、卖艺不算营销;未主动添加或声明有误可能导致限制传播、删除下线、账号封禁等处理;默认选"内容无需标注"。 |
| copyright_claim | boolean | 是否勾选“内容为自制：未经作者允许，禁止转载”。**默认 false,不要主动设为 true,只有用户明确说明内容是自制的才设为 true**。 |
| watermark | boolean | 是否添加原创水印（默认 true，显示在视频右上角防盗用。除非用户明确说不加水印才设为 false） |
| author_marks | string[] | 作者声明(非必选,可多选,可空数组)。每项必须为以下之一(不能自创):"作者声明:该视频使用人工智能合成技术" | "作者声明:视频内含有危险行为,请勿轻易模仿" | "作者声明:该内容仅供娱乐,请勿过分解读" | "作者声明:该内容可能引人不适,请谨慎选择观看" | "作者声明:请理性适度消费" | "作者声明:个人观点,仅供参考" |

## 标题参考示例(好的 vs 差的)
✅ 好的:"用 AI Agent 自动审查代码缺陷,我把自家项目翻了个底朝天" / "ESP32 心率监测器:20 块钱的方案也能跑" / "别再手动投稿了,写个脚本自动发 B 站"
❌ 差的:"AI Agent 技术分享" / "ESP32 项目介绍" / "自动投稿工具详解"

## 简介参考示例
"之前参加了一个代码审查活动,想到与其让人看,不如让 AI 也来审一遍。我用自己的 Obsidian 同步工具当靶子,让 AI Agent 逐行读了 2 万行 Rust + 8200 行 TypeScript,找到了几个挺有意思的问题。视频里走了一遍完整流程,包括怎么配置、怎么跑、以及 AI 看到的那些盲点。"

严格输出 JSON,不要包含 markdown 代码块标记或其他文字。"""


def synthesize_api(obs_v, obs_a, api_key, api_base, model):
    user_content = SYNTHESIZE_USER_PROMPT.format(
        obs_visual=json.dumps(obs_v, ensure_ascii=False, indent=2),
        obs_audio=json.dumps(obs_a, ensure_ascii=False, indent=2)
    )
    payload = {
        'model': model,
        'messages': [
            {'role':'system','content': SYNTHESIZE_SYSTEM_PROMPT},
            {'role':'user','content': user_content}
        ],
        'max_tokens': 4000
    }
    req = urllib.request.Request(
        f"{api_base.rstrip('/')}/chat/completions",
        data=json.dumps(payload).encode('utf-8'),
        headers={"Content-Type":"application/json","Authorization":f"Bearer {api_key}"}
    )
    resp_data = http_request_with_retry(req, timeout=120, label=f"Synthesize LLM ({model})")
    content = extract_llm_content(resp_data, label=f"Synthesize LLM ({model})")

    # 多轮 JSON 解析重试
    for attempt in range(3):
        metadata = parse_json_from_llm(content, expect_array=False)
        if isinstance(metadata, dict) and 'title' in metadata and 'intro' in metadata and 'tags' in metadata:
            print(f"Synthesize JSON parsed OK on attempt {attempt+1}")
            return metadata
        if metadata is None:
            try:
                metadata = json.loads(content)
            except (json.JSONDecodeError, ValueError):
                pass
        if not isinstance(metadata, dict) or 'title' not in metadata:
            print(f"WARNING: Synthesize parse attempt {attempt+1}/3 failed")
            if attempt < 2:
                retry_msg = f"你的上一次输出不是合法 JSON,解析失败。\n上一次输出(前500字): {content[:500]}\n\n请重新输出,严格只输出一个 JSON 对象,不要包含 markdown 标记、解释或额外文字。"
                retry_payload = {
                    'model': model,
                    'messages': [
                        {'role':'system','content': SYNTHESIZE_SYSTEM_PROMPT},
                        {'role':'user','content': user_content},
                        {'role':'assistant','content': content},
                        {'role':'user','content': retry_msg}
                    ],
                    'max_tokens': 4000
                }
                retry_req = urllib.request.Request(
                    f"{api_base.rstrip('/')}/chat/completions",
                    data=json.dumps(retry_payload).encode('utf-8'),
                    headers={"Content-Type":"application/json","Authorization":f"Bearer {api_key}"}
                )
                try:
                    retry_resp = http_request_with_retry(retry_req, timeout=120, label=f"Synthesize retry {attempt+2}")
                    content = extract_llm_content(retry_resp, label=f"Synthesize retry {attempt+2}")
                except Exception as retry_err:
                    print(f"  Retry request failed: {retry_err}")
                    continue
            else:
                print(f"WARNING: All 3 synthesize parse attempts failed.")
                return synthesize_agent(obs_v, obs_a)
    # Safety net: should not reach here, but guarantee a return
    return synthesize_agent(obs_v, obs_a)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--observations-visual', required=True)
    parser.add_argument('--observations-audio', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--method', choices=['api','agent','manual'], default='manual')
    parser.add_argument('--api-key')
    parser.add_argument('--api-base')
    parser.add_argument('--model', default=None)
    args = parser.parse_args()

    with open(args.observations_visual, encoding='utf-8') as f:
        obs_v = json.load(f)
    with open(args.observations_audio, encoding='utf-8') as f:
        obs_a = json.load(f)

    if args.method == 'manual':
        md = observations_to_markdown(obs_v, obs_a)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(md)
        print('Wrote manual markdown to', args.output)
        return

    if args.method == 'agent':
        # 输出带引导 prompt 的 markdown,让 Agent 自行合成 metadata
        agent_md = SYNTHESIZE_SYSTEM_PROMPT + '\n\n'
        agent_md += SYNTHESIZE_USER_PROMPT.format(
            obs_visual=json.dumps(obs_v, ensure_ascii=False, indent=2),
            obs_audio=json.dumps(obs_a, ensure_ascii=False, indent=2)
        )
        agent_md += '\n\n--- END OF PROMPT ---\n\n请根据以上内容生成 metadata.json 并写入文件。\n'
        agent_md += f'输出文件路径: {args.output}\n'
        agent_md += '请严格输出 JSON 格式。\n'
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(agent_md)
        print(f'Wrote agent prompt to {args.output}. Agent should read it and generate metadata.')
        return

    if args.method == 'api':
        if not args.api_key or not args.api_base:
            print('api method requires --api-key and --api-base', file=sys.stderr); sys.exit(1)
        print(f"⚠️  PRIVACY: Observations + metadata will be sent to external LLM endpoint: {args.api_base}")
        md = synthesize_api(obs_v, obs_a, args.api_key, args.api_base, args.model)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(md, f, ensure_ascii=False, indent=2)
        print('Wrote metadata (api) to', args.output)
        return

if __name__ == '__main__':
    main()
