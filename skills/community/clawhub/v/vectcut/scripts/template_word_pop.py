import json
import random

def asr_28ac1b65432746129b952e05bc719183(segments, draft_id):
    word_list = []
    choices = [0.0, -10.0, 10.0]
    normalized_segments = segments
    for item in normalized_segments or []:
        try:
            if isinstance(item, dict):
                start = item.get("start")
                end = item.get("end")
                text = str(item.get("text") or "")
                phrase = item.get("phrase")
                try:
                    start = float(start)
                except Exception:
                    start = 0.0
                try:
                    end = float(end)
                except Exception:
                    end = start
                start = start / 1000.0
                end = end / 1000.0
                if isinstance(phrase, (list, tuple)) and phrase:
                    for p in phrase:
                        try:
                            p_text = str((p.get("text") if isinstance(p, dict) else "") or "").strip()
                            p_start = (p.get("start_time") if isinstance(p, dict) else None)
                            p_end = (p.get("end_time") if isinstance(p, dict) else None)
                            try:
                                p_start = float(p_start)
                            except Exception:
                                p_start = start * 1000.0
                            try:
                                p_end = float(p_end)
                            except Exception:
                                p_end = p_start
                            p_start = p_start / 1000.0
                            p_end = p_end / 1000.0
                            if p_text:
                                word_list.append({
                                    "text": p_text,
                                    "start": p_start,
                                    "end": p_end,
                                    "rotation": random.choice(choices)
                                })
                        except Exception:
                            continue
                else:
                    tokens = [t for t in text.strip().split() if t] if text.strip() else []
                    if not tokens and text.strip():
                        tokens = list(text.strip())
                    n = len(tokens)
                    if n <= 0:
                        continue
                    duration = max(0.0, (end - start))
                    step = duration / n if n > 0 else 0.0
                    for i, t in enumerate(tokens):
                        s = start + i * step
                        e = s + step
                        word_list.append({
                            "text": t,
                            "start": s,
                            "end": e,
                            "rotation": random.choice(choices)
                        })
            elif isinstance(item, (list, tuple)) and len(item) >= 3:
                try:
                    start = float(item[0]) / 1000.0
                except Exception:
                    start = 0.0
                try:
                    end = float(item[1]) / 1000.0
                except Exception:
                    end = start
                text = str(item[2] or "")
                tokens = [t for t in text.strip().split() if t] if text.strip() else []
                if not tokens and text.strip():
                    tokens = list(text.strip())
                n = len(tokens)
                if n <= 0:
                    continue
                duration = max(0.0, (end - start))
                step = duration / n if n > 0 else 0.0
                for i, t in enumerate(tokens):
                    s = start + i * step
                    e = s + step
                    word_list.append({
                        "text": t,
                        "start": s,
                        "end": e,
                        "rotation": random.choice(choices)
                    })
            else:
                continue
        except Exception:
            continue
    return {
        "draft_id": str(draft_id) if draft_id is not None else "",
        "inputs": {
            "word_list": word_list
        },
        "script": [
    {
      "type": "for",
      "id": "subtitle_loop",
      "index": 1,
      "in": "${word_list}",
      "loop": [
        {
          "type": "action",
          "id": "add_styled_word",
          "index": 0,
          "action_type": "add_text",
          "params": {
            "text": "${item.text}",
            "start": "${item.start}",
            "end": "${item.end}",
            "track_name": "word_by_word_track",
            "font_color": "#FFFFFF",
            "border_width": 48.0,
            "border_color": "#000000",
            "background_color": "#C3CF47",
            "background_alpha": 1,
            "background_round_radius":0.5,
            "transform_y":-0.53,
            "intro_animation": "弹入",
            "intro_duration": 0.1,
            "rotation": "${item.rotation}",
            "font_size": 12.0
          }
        }
      ]
    }
  ]
    }

# segments = [{'start': 419, 'end': 900, 'text': '家人们', 'phrase': [{'text': '家人', 'start_time': 419, 'end_time': 740}, {'text': '们', 'start_time': 740, 'end_time': 900}], 'words': [{'word': '家', 'start_time': 419, 'end_time': 600}, {'word': '人', 'start_time': 600, 'end_time': 740}, {'word': '们', 'start_time': 740, 'end_time': 900}]}, {'start': 1179, 'end': 3160, 'text': 'AI视频界的 Banana', 'phrase': [{'text': 'AI', 'start_time': 1179, 'end_time': 1499}, {'text': '视频', 'start_time': 1499, 'end_time': 1700}, {'text': '界', 'start_time': 1779, 'end_time': 1960}, {'text': '的', 'start_time': 1960, 'end_time': 2140}, {'text': 'Banana', 'start_time': 2299, 'end_time': 3160}], 'words': [{'word': 'AI', 'start_time': 1179, 'end_time': 1499}, {'word': '视', 'start_time': 1499, 'end_time': 1580}, {'word': '频', 'start_time': 1580, 'end_time': 1700}, {'word': '界', 'start_time': 1779, 'end_time': 1960}, {'word': '的', 'start_time': 1960, 'end_time': 2140}, {'word': 'Banana', 'start_time': 2299, 'end_time': 3160}]}, {'start': 3259, 'end': 5160, 'text': '可灵O1闪亮登场了', 'phrase': [{'text': '可', 'start_time': 3259, 'end_time': 3440}, {'text': '灵', 'start_time': 3440, 'end_time': 3620}, {'text': 'O1', 'start_time': 3620, 'end_time': 3900}, {'text': '闪', 'start_time': 3979, 'end_time': 4160}, {'text': '亮', 'start_time': 4160, 'end_time': 4320}, {'text': '登', 'start_time': 4320, 'end_time': 4500}, {'text': '场', 'start_time': 4500, 'end_time': 4680}, {'text': '了', 'start_time': 4680, 'end_time': 5160}], 'words': [{'word': '可', 'start_time': 3259, 'end_time': 3440}, {'word': '灵', 'start_time': 3440, 'end_time': 3620}, {'word': 'O1', 'start_time': 3620, 'end_time': 3900}, {'word': '闪', 'start_time': 3979, 'end_time': 4160}, {'word': '亮', 'start_time': 4160, 'end_time': 4320}, {'word': '登', 'start_time': 4320, 'end_time': 4500}, {'word': '场', 'start_time': 4500, 'end_time': 4680}, {'word': '了', 'start_time': 4680, 'end_time': 5160}]}, {'start': 5259, 'end': 8960, 'text': '它就像一颗在 AI 视频领域冉冉升起的新星', 'phrase': [{'text': '它', 'start_time': 5259, 'end_time': 5420}, {'text': '就', 'start_time': 5420, 'end_time': 5560}, {'text': '像', 'start_time': 5560, 'end_time': 5700}, {'text': '一颗', 'start_time': 5700, 'end_time': 6020}, {'text': '在', 'start_time': 6219, 'end_time': 6420}, {'text': 'AI', 'start_time': 6420, 'end_time': 6720}, {'text': '视频', 'start_time': 6720, 'end_time': 6940}, {'text': '领域', 'start_time': 7019, 'end_time': 7340}, {'text': '冉冉', 'start_time': 7459, 'end_time': 7900}, {'text': '升起', 'start_time': 7900, 'end_time': 8220}, {'text': '的', 'start_time': 8220, 'end_time': 8340}, {'text': '新星', 'start_time': 8340, 'end_time': 8960}], 'words': [{'word': '它', 'start_time': 5259, 'end_time': 5420}, {'word': '就', 'start_time': 5420, 'end_time': 5560}, {'word': '像', 'start_time': 5560, 'end_time': 5700}, {'word': '一', 'start_time': 5700, 'end_time': 5840}, {'word': '颗', 'start_time': 5840, 'end_time': 6020}, {'word': '在', 'start_time': 6219, 'end_time': 6420}, {'word': 'AI', 'start_time': 6420, 'end_time': 6720}, {'word': '视', 'start_time': 6720, 'end_time': 6820}, {'word': '频', 'start_time': 6820, 'end_time': 6940}, {'word': '领', 'start_time': 7019, 'end_time': 7180}, {'word': '域', 'start_time': 7180, 'end_time': 7340}, {'word': '冉', 'start_time': 7459, 'end_time': 7660}, {'word': '冉', 'start_time': 7699, 'end_time': 7900}, {'word': '升', 'start_time': 7900, 'end_time': 8080}, {'word': '起', 'start_time': 8080, 'end_time': 8220}, {'word': '的', 'start_time': 8220, 'end_time': 8340}, {'word': '新', 'start_time': 8340, 'end_time': 8480}, {'word': '星', 'start_time': 8480, 'end_time': 8960}]}, {'start': 9019, 'end': 10480, 'text': '带着无限惊喜', 'phrase': [{'text': '带着', 'start_time': 9019, 'end_time': 9360}, {'text': '无限', 'start_time': 9360, 'end_time': 9740}, {'text': '惊喜', 'start_time': 9779, 'end_time': 10480}], 'words': [{'word': '带', 'start_time': 9019, 'end_time': 9200}, {'word': '着', 'start_time': 9200, 'end_time': 9360}, {'word': '无', 'start_time': 9360, 'end_time': 9540}, {'word': '限', 'start_time': 9540, 'end_time': 9740}, {'word': '惊', 'start_time': 9779, 'end_time': 9980}, {'word': '喜', 'start_time': 9980, 'end_time': 10480}]}, {'start': 11179, 'end': 13640, 'text': '可灵O1拥有强大的 AI 功能', 'phrase': [{'text': '可', 'start_time': 11179, 'end_time': 11340}, {'text': '灵', 'start_time': 11340, 'end_time': 11500}, {'text': 'O1', 'start_time': 11500, 'end_time': 11780}, {'text': '拥', 'start_time': 11979, 'end_time': 12140}, {'text': '有', 'start_time': 12140, 'end_time': 12300}, {'text': '强', 'start_time': 12300, 'end_time': 12500}, {'text': '大', 'start_time': 12500, 'end_time': 12660}, {'text': '的', 'start_time': 12660, 'end_time': 12820}, {'text': 'AI', 'start_time': 12820, 'end_time': 13040}, {'text': '功', 'start_time': 13040, 'end_time': 13180}, {'text': '能', 'start_time': 13180, 'end_time': 13640}], 'words': [{'word': '可', 'start_time': 11179, 'end_time': 11340}, {'word': '灵', 'start_time': 11340, 'end_time': 11500}, {'word': 'O1', 'start_time': 11500, 'end_time': 11780}, {'word': '拥', 'start_time': 11979, 'end_time': 12140}, {'word': '有', 'start_time': 12140, 'end_time': 12300}, {'word': '强', 'start_time': 12300, 'end_time': 12500}, {'word': '大', 'start_time': 12500, 'end_time': 12660}, {'word': '的', 'start_time': 12660, 'end_time': 12820}, {'word': 'AI', 'start_time': 12820, 'end_time': 13040}, {'word': '功', 'start_time': 13040, 'end_time': 13180}, {'word': '能', 'start_time': 13180, 'end_time': 13640}]}, {'start': 13659, 'end': 15840, 'text': '能快速且精准的处理视频', 'phrase': [{'text': '能', 'start_time': 13659, 'end_time': 13860}, {'text': '快速', 'start_time': 13860, 'end_time': 14300}, {'text': '且', 'start_time': 14459, 'end_time': 14660}, {'text': '精准', 'start_time': 14660, 'end_time': 14980}, {'text': '的', 'start_time': 14980, 'end_time': 15100}, {'text': '处理', 'start_time': 15100, 'end_time': 15340}, {'text': '视频', 'start_time': 15340, 'end_time': 15840}], 'words': [{'word': '能', 'start_time': 13659, 'end_time': 13860}, {'word': '快', 'start_time': 13860, 'end_time': 14060}, {'word': '速', 'start_time': 14099, 'end_time': 14300}, {'word': '且', 'start_time': 14459, 'end_time': 14660}, {'word': '精', 'start_time': 14660, 'end_time': 14840}, {'word': '准', 'start_time': 14840, 'end_time': 14980}, {'word': '的', 'start_time': 14980, 'end_time': 15100}, {'word': '处', 'start_time': 15100, 'end_time': 15220}, {'word': '理', 'start_time': 15220, 'end_time': 15340}, {'word': '视', 'start_time': 15340, 'end_time': 15420}, {'word': '频', 'start_time': 15420, 'end_time': 15840}]}, {'start': 16099, 'end': 17020, 'text': '无论是剪辑', 'phrase': [{'text': '无论是', 'start_time': 16099, 'end_time': 16640}, {'text': '剪辑', 'start_time': 16640, 'end_time': 17020}], 'words': [{'word': '无', 'start_time': 16099, 'end_time': 16300}, {'word': '论', 'start_time': 16300, 'end_time': 16480}, {'word': '是', 'start_time': 16480, 'end_time': 16640}, {'word': '剪', 'start_time': 16640, 'end_time': 16820}, {'word': '辑', 'start_time': 16820, 'end_time': 17020}]}, {'start': 17259, 'end': 18178, 'text': '特效添加', 'phrase': [{'text': '特效', 'start_time': 17259, 'end_time': 17580}, {'text': '添加', 'start_time': 17580, 'end_time': 18178}], 'words': [{'word': '特', 'start_time': 17259, 'end_time': 17440}, {'word': '效', 'start_time': 17440, 'end_time': 17580}, {'word': '添', 'start_time': 17580, 'end_time': 17740}, {'word': '加', 'start_time': 17740, 'end_time': 18178}]}, {'start': 18179, 'end': 19100, 'text': '还是智能配音', 'phrase': [{'text': '还是', 'start_time': 18179, 'end_time': 18480}, {'text': '智能', 'start_time': 18480, 'end_time': 18780}, {'text': '配音', 'start_time': 18780, 'end_time': 19100}], 'words': [{'word': '还', 'start_time': 18179, 'end_time': 18340}, {'word': '是', 'start_time': 18340, 'end_time': 18480}, {'word': '智', 'start_time': 18480, 'end_time': 18640}, {'word': '能', 'start_time': 18640, 'end_time': 18780}, {'word': '配', 'start_time': 18780, 'end_time': 18920}, {'word': '音', 'start_time': 18920, 'end_time': 19100}]}, {'start': 19259, 'end': 20880, 'text': '它都能轻松搞定', 'phrase': [{'text': '它', 'start_time': 19259, 'end_time': 19440}, {'text': '都', 'start_time': 19440, 'end_time': 19580}, {'text': '能', 'start_time': 19580, 'end_time': 19740}, {'text': '轻松', 'start_time': 19779, 'end_time': 20180}, {'text': '搞定', 'start_time': 20180, 'end_time': 20880}], 'words': [{'word': '它', 'start_time': 19259, 'end_time': 19440}, {'word': '都', 'start_time': 19440, 'end_time': 19580}, {'word': '能', 'start_time': 19580, 'end_time': 19740}, {'word': '轻', 'start_time': 19779, 'end_time': 19980}, {'word': '松', 'start_time': 19980, 'end_time': 20180}, {'word': '搞', 'start_time': 20180, 'end_time': 20380}, {'word': '定', 'start_time': 20380, 'end_time': 20880}]}, {'start': 21739, 'end': 22700, 'text': '有了可灵 O1', 'phrase': [{'text': '有', 'start_time': 21739, 'end_time': 21920}, {'text': '了', 'start_time': 21920, 'end_time': 22060}, {'text': '可', 'start_time': 22060, 'end_time': 22200}, {'text': '灵', 'start_time': 22200, 'end_time': 22380}, {'text': 'O1', 'start_time': 22380, 'end_time': 22700}], 'words': [{'word': '有', 'start_time': 21739, 'end_time': 21920}, {'word': '了', 'start_time': 21920, 'end_time': 22060}, {'word': '可', 'start_time': 22060, 'end_time': 22200}, {'word': '灵', 'start_time': 22200, 'end_time': 22380}, {'word': 'O1', 'start_time': 22380, 'end_time': 22700}]}, {'start': 23219, 'end': 24938, 'text': '就算你是视频小白', 'phrase': [{'text': '就算', 'start_time': 23219, 'end_time': 23620}, {'text': '你', 'start_time': 23620, 'end_time': 23800}, {'text': '是', 'start_time': 23800, 'end_time': 23960}, {'text': '视频', 'start_time': 23960, 'end_time': 24180}, {'text': '小白', 'start_time': 24259, 'end_time': 24938}], 'words': [{'word': '就', 'start_time': 23219, 'end_time': 23420}, {'word': '算', 'start_time': 23420, 'end_time': 23620}, {'word': '你', 'start_time': 23620, 'end_time': 23800}, {'word': '是', 'start_time': 23800, 'end_time': 23960}, {'word': '视', 'start_time': 23960, 'end_time': 24060}, {'word': '频', 'start_time': 24060, 'end_time': 24180}, {'word': '小', 'start_time': 24259, 'end_time': 24460}, {'word': '白', 'start_time': 24460, 'end_time': 24938}]}, {'start': 24939, 'end': 26680, 'text': '也能秒变创作大神', 'phrase': [{'text': '也', 'start_time': 24939, 'end_time': 25120}, {'text': '能', 'start_time': 25120, 'end_time': 25280}, {'text': '秒', 'start_time': 25280, 'end_time': 25460}, {'text': '变', 'start_time': 25460, 'end_time': 25660}, {'text': '创作', 'start_time': 25660, 'end_time': 26040}, {'text': '大神', 'start_time': 26040, 'end_time': 26680}], 'words': [{'word': '也', 'start_time': 24939, 'end_time': 25120}, {'word': '能', 'start_time': 25120, 'end_time': 25280}, {'word': '秒', 'start_time': 25280, 'end_time': 25460}, {'word': '变', 'start_time': 25460, 'end_time': 25660}, {'word': '创', 'start_time': 25660, 'end_time': 25860}, {'word': '作', 'start_time': 25860, 'end_time': 26040}, {'word': '大', 'start_time': 26040, 'end_time': 26200}, {'word': '神', 'start_time': 26200, 'end_time': 26680}]}, {'start': 26779, 'end': 29320, 'text': '轻松产出高质量的 AI 视频', 'phrase': [{'text': '轻松', 'start_time': 26779, 'end_time': 27200}, {'text': '产出', 'start_time': 27200, 'end_time': 27580}, {'text': '高质量', 'start_time': 27779, 'end_time': 28360}, {'text': '的', 'start_time': 28360, 'end_time': 28540}, {'text': 'AI', 'start_time': 28540, 'end_time': 28800}, {'text': '视频', 'start_time': 28800, 'end_time': 29320}], 'words': [{'word': '轻', 'start_time': 26779, 'end_time': 26980}, {'word': '松', 'start_time': 27019, 'end_time': 27200}, {'word': '产', 'start_time': 27200, 'end_time': 27380}, {'word': '出', 'start_time': 27380, 'end_time': 27580}, {'word': '高', 'start_time': 27779, 'end_time': 27980}, {'word': '质', 'start_time': 28059, 'end_time': 28220}, {'word': '量', 'start_time': 28220, 'end_time': 28360}, {'word': '的', 'start_time': 28360, 'end_time': 28540}, {'word': 'AI', 'start_time': 28540, 'end_time': 28800}, {'word': '视', 'start_time': 28800, 'end_time': 28900}, {'word': '频', 'start_time': 28900, 'end_time': 29320}]}, {'start': 29699, 'end': 30578, 'text': '别再犹豫', 'phrase': [{'text': '别', 'start_time': 29699, 'end_time': 29900}, {'text': '再', 'start_time': 29939, 'end_time': 30100}, {'text': '犹豫', 'start_time': 30100, 'end_time': 30578}], 'words': [{'word': '别', 'start_time': 29699, 'end_time': 29900}, {'word': '再', 'start_time': 29939, 'end_time': 30100}, {'word': '犹', 'start_time': 30100, 'end_time': 30240}, {'word': '豫', 'start_time': 30240, 'end_time': 30578}]}, {'start': 30579, 'end': 34100, 'text': '赶紧让可灵 O1成为你视频创作的得力助手吧', 'phrase': [{'text': '赶', 'start_time': 30579, 'end_time': 30760}, {'text': '紧', 'start_time': 30760, 'end_time': 30920}, {'text': '让', 'start_time': 30920, 'end_time': 31080}, {'text': '可', 'start_time': 31080, 'end_time': 31220}, {'text': '灵', 'start_time': 31220, 'end_time': 31380}, {'text': 'O1', 'start_time': 31380, 'end_time': 31660}, {'text': '成', 'start_time': 31779, 'end_time': 31940}, {'text': '为', 'start_time': 31940, 'end_time': 32060}, {'text': '你', 'start_time': 32060, 'end_time': 32200}, {'text': '视', 'start_time': 32200, 'end_time': 32300}, {'text': '频', 'start_time': 32300, 'end_time': 32420}, {'text': '创', 'start_time': 32499, 'end_time': 32700}, {'text': '作', 'start_time': 32700, 'end_time': 32860}, {'text': '的', 'start_time': 32860, 'end_time': 33020}, {'text': '得', 'start_time': 33139, 'end_time': 33340}, {'text': '力', 'start_time': 33340, 'end_time': 33520}, {'text': '助', 'start_time': 33520, 'end_time': 33700}, {'text': '手', 'start_time': 33739, 'end_time': 33920}, {'text': '吧', 'start_time': 33920, 'end_time': 34100}], 'words': [{'word': '赶', 'start_time': 30579, 'end_time': 30760}, {'word': '紧', 'start_time': 30760, 'end_time': 30920}, {'word': '让', 'start_time': 30920, 'end_time': 31080}, {'word': '可', 'start_time': 31080, 'end_time': 31220}, {'word': '灵', 'start_time': 31220, 'end_time': 31380}, {'word': 'O1', 'start_time': 31380, 'end_time': 31660}, {'word': '成', 'start_time': 31779, 'end_time': 31940}, {'word': '为', 'start_time': 31940, 'end_time': 32060}, {'word': '你', 'start_time': 32060, 'end_time': 32200}, {'word': '视', 'start_time': 32200, 'end_time': 32300}, {'word': '频', 'start_time': 32300, 'end_time': 32420}, {'word': '创', 'start_time': 32499, 'end_time': 32700}, {'word': '作', 'start_time': 32700, 'end_time': 32860}, {'word': '的', 'start_time': 32860, 'end_time': 33020}, {'word': '得', 'start_time': 33139, 'end_time': 33340}, {'word': '力', 'start_time': 33340, 'end_time': 33520}, {'word': '助', 'start_time': 33520, 'end_time': 33700}, {'word': '手', 'start_time': 33739, 'end_time': 33920}, {'word': '吧', 'start_time': 33920, 'end_time': 34100}]}]
# print(asr_28ac1b65432746129b952e05bc719183(segments, "123"))

def apply_template(segments, draft_id):
    return asr_28ac1b65432746129b952e05bc719183(segments, draft_id)

