import json
import re


def asr_9d550677d16a4c879a19bfeee1623a38(segments, draft_id):
    subtitles = []
    index = 1
    prev_sub = None
    normalized_segments = segments
    total = len(normalized_segments) if isinstance(normalized_segments, (list, tuple)) else 0
    for item in normalized_segments or []:
        try:
            if isinstance(item, dict):
                start = item.get("start")
                end = item.get("end")
                text = str(item.get("text") or "").strip()
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
            elif isinstance(item, (list, tuple)) and len(item) >= 3:
                start = float(item[0])
                end = float(item[1])
                text = str(item[2]).strip()
            else:
                continue
            track_name = f"sub_{index-1}"
            is_last = (index == total)
            next_start = None
            if not is_last and isinstance(normalized_segments, (list, tuple)):
                try:
                    nxt = normalized_segments[index]
                    if isinstance(nxt, dict):
                        next_start = nxt.get("start")
                        try:
                            next_start = float(next_start)
                        except Exception:
                            next_start = None
                        if isinstance(next_start, (int, float)) and next_start > 1000:
                            next_start = next_start / 1000.0
                    elif isinstance(nxt, (list, tuple)) and len(nxt) >= 1:
                        next_start = float(nxt[0])
                except Exception:
                    next_start = None
            next_same_start = None
            if isinstance(normalized_segments, (list, tuple)):
                try:
                    nxt2 = normalized_segments[index + 1]
                    if isinstance(nxt2, dict):
                        next_same_start = nxt2.get("start")
                        try:
                            next_same_start = float(next_same_start)
                        except Exception:
                            next_same_start = None
                        if isinstance(next_same_start, (int, float)) and next_same_start > 1000:
                            next_same_start = next_same_start / 1000.0
                    elif isinstance(nxt2, (list, tuple)) and len(nxt2) >= 1:
                        next_same_start = float(nxt2[0])
                except Exception:
                    next_same_start = None
            focus_time = start
            vis_start = prev_sub["focus_time"] if prev_sub is not None else max(0.0, start - 1.0)
            calc_end = next_same_start if isinstance(next_same_start, (int, float)) else end
            current_sub = {
                "track_name": track_name,
                "text": text,
                "start": vis_start,
                "focus_time": focus_time,
                "exit_time": (9999.0 if is_last else (next_start if isinstance(next_start, (int, float)) else (focus_time + 2.0))),
                "end": calc_end
            }
            if prev_sub is not None:
                prev_sub["exit_time"] = focus_time
            subtitles.append(current_sub)
            prev_sub = current_sub
            index += 1
        except Exception:
            continue
    inputs = {
        "subtitles": subtitles,
        "sticker_config": {
            "sticker_id": "7169527615806573831",
            "start": subtitles[0]["start"] if subtitles else 0.0,
            "end": subtitles[-1]["end"] if subtitles else 0.0,
            "x_px": -894,
            "y_px": -799,
            "scale": 0.17
        },
        "y_bottom": -1006,
        "y_middle": -806,
        "y_top": -606,
        "x_wait": -150,
        "x_focus": 50,
        "scale_small": 0.8,
        "scale_full": 1.0,
        "alpha_hidden": 0.4,
        "alpha_full": 1.0,
        "fixed_width": 0.55
    }
    return {
        "draft_id": str(draft_id) if draft_id is not None else "",
        "inputs": inputs,
        "script": [
            {
            "type": "action",
            "id": "add_global_sticker",
            "index": 0,
            "action_type": "add_sticker",
            "params": {
                "sticker_id": "${sticker_config.sticker_id}",
                "start": "${sticker_config.start}",
                "end": "${sticker_config.end}",
                "track_name": "sticker_layer",
                "transform_x_px": "${sticker_config.x_px}",
                "transform_y_px": "${sticker_config.y_px}",
                "scale_x": "${sticker_config.scale}",
                "scale_y": "${sticker_config.scale}"
            }
            },
            {
            "type": "for",
            "id": "loop_rolling_subs",
            "index": 1,
            "in": "${subtitles}",
            "loop": [
                {
                "type": "action",
                "id": "add_text_base",
                "index": 0,
                "action_type": "add_text",
                "params": {
                    "text": "${item.text}",
                    "start": "${item.start}",
                    "end": "${item.end}",
                    "track_name": "${item.track_name}",
                    "font": "研宋体",
                    "font_size": 12.0,
                    "font_color": "#ffffff",
                    "shadow_enabled": True,
                    "align": 0,
                    "fixed_width": "${fixed_width}",
                    "transform_x_px": "${x_wait}",
                    "transform_y_px": "${y_bottom}",
                    "scale_x": "${scale_small}",
                    "scale_y": "${scale_small}"
                }
                },
                {
                "type": "action",
                "id": "sub_full_sync_motion",
                "index": 1,
                "action_type": "add_video_keyframe",
                "params": {
                    "track_name": "${item.track_name}",
                    "times": [
                    "${item.focus_time} - 0.1", "${item.focus_time}",
                    "${item.focus_time} - 0.1", "${item.focus_time}",
                    "${item.focus_time} - 0.1", "${item.focus_time}",
                    "${item.focus_time} - 0.1", "${item.focus_time}",
                    "${item.exit_time} - 0.1", "${item.exit_time}",
                    "${item.exit_time} - 0.1", "${item.exit_time}",
                    "${item.exit_time} - 0.1", "${item.exit_time}",
                    "${item.exit_time} - 0.1", "${item.exit_time}"
                    ],
                    "property_types": [
                    "position_x_px", "position_x_px",
                    "position_y_px", "position_y_px",
                    "uniform_scale", "uniform_scale",
                    "alpha", "alpha",
                    "position_x_px", "position_x_px",
                    "position_y_px", "position_y_px",
                    "uniform_scale", "uniform_scale",
                    "alpha", "alpha"
                    ],
                    "values": [
                    "${x_wait}", "${x_focus}",
                    "${y_bottom}", "${y_middle}",
                    "${scale_small}", "${scale_full}",
                    "${alpha_hidden}", "${alpha_full}",
                    "${x_focus}", "${x_wait}",
                    "${y_middle}", "${y_top}",
                    "${scale_full}", "${scale_small}",
                    "${alpha_full}", "${alpha_hidden}"
                    ]
                }
                }
            ]
            }
        ]
    }

# segemnts = [{'start': 3260, 'end': 4460, 'text': '为什么我们选择把', 'words': [{'word': '为', 'start_time': 3260, 'end_time': 3420}, {'word': '什', 'start_time': 3420, 'end_time': 3540}, {'word': '么', 'start_time': 3540, 'end_time': 3620}, {'word': '我', 'start_time': 3620, 'end_time': 3740}, {'word': '们', 'start_time': 3740, 'end_time': 3900}, {'word': '选', 'start_time': 3900, 'end_time': 4060}, {'word': '择', 'start_time': 4060, 'end_time': 4180}, {'word': '把', 'start_time': 4180, 'end_time': 4460}]}, {'start': 4500, 'end': 5580, 'text': '代码开源了', 'words': [{'word': '代', 'start_time': 4500, 'end_time': 4700}, {'word': '码', 'start_time': 4700, 'end_time': 4900}, {'word': '开', 'start_time': 4940, 'end_time': 5100}, {'word': '源', 'start_time': 5180, 'end_time': 5220}, {'word': '了', 'start_time': 5340, 'end_time': 5580}]}, {'start': 5980, 'end': 7780, 'text': '明明辛辛苦苦做了半年', 'words': [{'word': '明', 'start_time': 5980, 'end_time': 6180}, {'word': '明', 'start_time': 6260, 'end_time': 6340}, {'word': '辛', 'start_time': 6420, 'end_time': 6500}, {'word': '辛', 'start_time': 6580, 'end_time': 6700}, {'word': '苦', 'start_time': 6700, 'end_time': 6860}, {'word': '苦', 'start_time': 6900, 'end_time': 7020}, {'word': '做', 'start_time': 7020, 'end_time': 7220}, {'word': '了', 'start_time': 7220, 'end_time': 7340}, {'word': '半', 'start_time': 7340, 'end_time': 7540}, {'word': '年', 'start_time': 7540, 'end_time': 7780}]}, {'start': 7980, 'end': 9580, 'text': '而且开源版本的剪辑', 'words': [{'word': '而', 'start_time': 7980, 'end_time': 8180}, {'word': '且', 'start_time': 8180, 'end_time': 8340}, {'word': '开', 'start_time': 8380, 'end_time': 8580}, {'word': '源', 'start_time': 8620, 'end_time': 8660}, {'word': '版', 'start_time': 8780, 'end_time': 8940}, {'word': '本', 'start_time': 8940, 'end_time': 9060}, {'word': '的', 'start_time': 9060, 'end_time': 9260}, {'word': '剪', 'start_time': 9260, 'end_time': 9500}, {'word': '辑', 'start_time': 9500, 'end_time': 9580}]}, {'start': 9780, 'end': 11860, 'text': ' API的能力实际上已经', 'words': [{'word': 'API', 'start_time': 9780, 'end_time': 10100}, {'word': '的', 'start_time': 10100, 'end_time': 10300}, {'word': '能', 'start_time': 10300, 'end_time': 10460}, {'word': '力', 'start_time': 10460, 'end_time': 10620}, {'word': '实', 'start_time': 10860, 'end_time': 11060}, {'word': '际', 'start_time': 11060, 'end_time': 11220}, {'word': '上', 'start_time': 11220, 'end_time': 11420}, {'word': '已', 'start_time': 11420, 'end_time': 11660}, {'word': '经', 'start_time': 11660, 'end_time': 11860}]}, {'start': 11860, 'end': 12860, 'text': '非常丰富了', 'words': [{'word': '非', 'start_time': 11860, 'end_time': 12060}, {'word': '常', 'start_time': 12060, 'end_time': 12220}, {'word': '丰', 'start_time': 12220, 'end_time': 12460}, {'word': '富', 'start_time': 12460, 'end_time': 12620}, {'word': '了', 'start_time': 12620, 'end_time': 12860}]}, {'start': 13740, 'end': 14860, 'text': '为什么选择这么做', 'words': [{'word': '为', 'start_time': 13740, 'end_time': 13900}, {'word': '什', 'start_time': 13900, 'end_time': 13980}, {'word': '么', 'start_time': 13980, 'end_time': 14060}, {'word': '选', 'start_time': 14060, 'end_time': 14220}, {'word': '择', 'start_time': 14220, 'end_time': 14340}, {'word': '这', 'start_time': 14340, 'end_time': 14460}, {'word': '么', 'start_time': 14460, 'end_time': 14580}, {'word': '做', 'start_time': 14580, 'end_time': 14860}]}, {'start': 15260, 'end': 17540, 'text': '主要原因是我觉得未来', 'words': [{'word': '主', 'start_time': 15260, 'end_time': 15460}, {'word': '要', 'start_time': 15460, 'end_time': 15580}, {'word': '原', 'start_time': 15580, 'end_time': 15740}, {'word': '因', 'start_time': 15740, 'end_time': 15900}, {'word': '是', 'start_time': 15900, 'end_time': 16220}, {'word': '我', 'start_time': 16220, 'end_time': 16460}, {'word': '觉', 'start_time': 16460, 'end_time': 16660}, {'word': '得', 'start_time': 16660, 'end_time': 16820}, {'word': '未', 'start_time': 17020, 'end_time': 17260}, {'word': '来', 'start_time': 17260, 'end_time': 17540}]}, {'start': 17660, 'end': 19220, 'text': '一定是AI编程的', 'words': [{'word': '一', 'start_time': 17660, 'end_time': 17860}, {'word': '定', 'start_time': 17860, 'end_time': 18020}, {'word': '是', 'start_time': 18020, 'end_time': 18300}, {'word': 'AI', 'start_time': 18380, 'end_time': 18620}, {'word': '编', 'start_time': 18740, 'end_time': 18940}, {'word': '程', 'start_time': 18940, 'end_time': 19060}, {'word': '的', 'start_time': 19060, 'end_time': 19220}]}, {'start': 19220, 'end': 19540, 'text': '时代', 'words': [{'word': '时', 'start_time': 19220, 'end_time': 19380}, {'word': '代', 'start_time': 19380, 'end_time': 19540}]}, {'start': 20240, 'end': 21800, 'text': '人人都能通过和 ', 'words': [{'word': '人', 'start_time': 20240, 'end_time': 20440}, {'word': '人', 'start_time': 20480, 'end_time': 20640}, {'word': '都', 'start_time': 20640, 'end_time': 20880}, {'word': '能', 'start_time': 20880, 'end_time': 21160}, {'word': '通', 'start_time': 21160, 'end_time': 21360}, {'word': '过', 'start_time': 21360, 'end_time': 21520}, {'word': '和', 'start_time': 21520, 'end_time': 21800}]}, {'start': 21840, 'end': 24080, 'text': 'AI 对话的方式实现', 'words': [{'word': 'AI', 'start_time': 21840, 'end_time': 22240}, {'word': '对', 'start_time': 22240, 'end_time': 22440}, {'word': '话', 'start_time': 22440, 'end_time': 22640}, {'word': '的', 'start_time': 22640, 'end_time': 22800}, {'word': '方', 'start_time': 22800, 'end_time': 22960}, {'word': '式', 'start_time': 22960, 'end_time': 23120}, {'word': '实', 'start_time': 23640, 'end_time': 23880}, {'word': '现', 'start_time': 23880, 'end_time': 24080}]}, {'start': 24080, 'end': 25160, 'text': '自己想要的功能', 'words': [{'word': '自', 'start_time': 24080, 'end_time': 24240}, {'word': '己', 'start_time': 24240, 'end_time': 24360}, {'word': '想', 'start_time': 24360, 'end_time': 24560}, {'word': '要', 'start_time': 24560, 'end_time': 24680}, {'word': '的', 'start_time': 24680, 'end_time': 24840}, {'word': '功', 'start_time': 24840, 'end_time': 25000}, {'word': '能', 'start_time': 25000, 'end_time': 25160}]}, {'start': 25830, 'end': 28470, 'text': '那把代码开源就是一个', 'words': [{'word': '那', 'start_time': 25830, 'end_time': 26070}, {'word': '把', 'start_time': 26110, 'end_time': 26390}, {'word': '代', 'start_time': 26510, 'end_time': 26750}, {'word': '码', 'start_time': 26750, 'end_time': 26950}, {'word': '开', 'start_time': 26990, 'end_time': 27190}, {'word': '源', 'start_time': 27190, 'end_time': 27310}, {'word': '就', 'start_time': 27830, 'end_time': 28070}, {'word': '是', 'start_time': 28070, 'end_time': 28190}, {'word': '一', 'start_time': 28190, 'end_time': 28310}, {'word': '个', 'start_time': 28310, 'end_time': 28470}]}, {'start': 28470, 'end': 30710, 'text': '最好的微调全世界 ', 'words': [{'word': '最', 'start_time': 28470, 'end_time': 28710}, {'word': '好', 'start_time': 28710, 'end_time': 28950}, {'word': '的', 'start_time': 28950, 'end_time': 29190}, {'word': '微', 'start_time': 29510, 'end_time': 29630}, {'word': '调', 'start_time': 29750, 'end_time': 30030}, {'word': '全', 'start_time': 30110, 'end_time': 30350}, {'word': '世', 'start_time': 30350, 'end_time': 30510}, {'word': '界', 'start_time': 30510, 'end_time': 30710}]}, {'start': 30830, 'end': 31990, 'text': 'AI 模型的方法', 'words': [{'word': 'AI', 'start_time': 30830, 'end_time': 31070}, {'word': '模', 'start_time': 31150, 'end_time': 31350}, {'word': '型', 'start_time': 31350, 'end_time': 31470}, {'word': '的', 'start_time': 31470, 'end_time': 31630}, {'word': '方', 'start_time': 31630, 'end_time': 31790}, {'word': '法', 'start_time': 31790, 'end_time': 31990}]}, {'start': 32700, 'end': 34100, 'text': '这样大家无论用哪', 'words': [{'word': '这', 'start_time': 32700, 'end_time': 32860}, {'word': '样', 'start_time': 32860, 'end_time': 33020}, {'word': '大', 'start_time': 33020, 'end_time': 33260}, {'word': '家', 'start_time': 33260, 'end_time': 33460}, {'word': '无', 'start_time': 33500, 'end_time': 33660}, {'word': '论', 'start_time': 33660, 'end_time': 33780}, {'word': '用', 'start_time': 33780, 'end_time': 33980}, {'word': '哪', 'start_time': 33980, 'end_time': 34100}]}, {'start': 34100, 'end': 36460, 'text': '一家的 AI 去做剪辑', 'words': [{'word': '一', 'start_time': 34100, 'end_time': 34220}, {'word': '家', 'start_time': 34220, 'end_time': 34380}, {'word': '的', 'start_time': 34380, 'end_time': 34540}, {'word': 'AI', 'start_time': 34580, 'end_time': 34820}, {'word': '去', 'start_time': 34980, 'end_time': 35340}, {'word': '做', 'start_time': 35500, 'end_time': 35820}, {'word': '剪', 'start_time': 36020, 'end_time': 36300}, {'word': '辑', 'start_time': 36300, 'end_time': 36460}]}, {'start': 36620, 'end': 37820, 'text': '工具的时候', 'words': [{'word': '工', 'start_time': 36620, 'end_time': 36900}, {'word': '具', 'start_time': 36900, 'end_time': 37100}, {'word': '的', 'start_time': 37220, 'end_time': 37460}, {'word': '时', 'start_time': 37460, 'end_time': 37620}, {'word': '候', 'start_time': 37620, 'end_time': 37820}]}, {'start': 38260, 'end': 39940, 'text': '都有很大概率会用到', 'words': [{'word': '都', 'start_time': 38260, 'end_time': 38500}, {'word': '有', 'start_time': 38500, 'end_time': 38660}, {'word': '很', 'start_time': 38660, 'end_time': 38820}, {'word': '大', 'start_time': 38820, 'end_time': 39020}, {'word': '概', 'start_time': 39020, 'end_time': 39220}, {'word': '率', 'start_time': 39220, 'end_time': 39340}, {'word': '会', 'start_time': 39420, 'end_time': 39660}, {'word': '用', 'start_time': 39660, 'end_time': 39820}, {'word': '到', 'start_time': 39820, 'end_time': 39940}]}, {'start': 39940, 'end': 40780, 'text': '我们的接口', 'words': [{'word': '我', 'start_time': 39940, 'end_time': 40060}, {'word': '们', 'start_time': 40060, 'end_time': 40140}, {'word': '的', 'start_time': 40140, 'end_time': 40300}, {'word': '接', 'start_time': 40300, 'end_time': 40500}, {'word': '口', 'start_time': 40500, 'end_time': 40780}]}]
# print(asr_9d550677d16a4c879a19bfeee1623a38(segemnts, "123"))

def apply_template(segments, draft_id):
    return asr_9d550677d16a4c879a19bfeee1623a38(segments, draft_id)

