import json


def asr_60348d11a5f54d2a98afb52f6acdb916(segments, draft_id):
    subtitles = []
    index = 1
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
            sub_id = f"sub_{index:03d}"
            track = "track_sub_0" if index % 2 == 1 else "track_sub_1"
            is_last = (index == total)
            y_initial = -0.75
            y_end = -0.65
            alpha_initial = 1.0
            alpha_end = 1.0 if is_last else 0.3
            scale_initial = 1.0
            scale_end = 1.0 if is_last else 0.8
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
            move_time = 99999.0 if is_last else (next_start if isinstance(next_start, (int, float)) else end)
            calc_end = next_same_start if isinstance(next_same_start, (int, float)) else end
            subtitles.append({
                "id": sub_id,
                "text": text,
                "start_time": start,
                "end_time": calc_end,
                "target_track": track,
                "y_initial": y_initial,
                "y_end": y_end,
                "alpha_initial": alpha_initial,
                "alpha_end": alpha_end,
                "scale_initial": scale_initial,
                "scale_end": scale_end,
                "move_time": move_time
            })
            index += 1
        except Exception:
            continue
    return {
        "draft_id": str(draft_id) if draft_id is not None else "",
        "inputs": {
            "subtitles": subtitles,
        },
        "script": [
    {
      "type": "for",
      "id": "loop_subtitles",
      "index": 0,
      "in": "${subtitles}",
      "loop": [
        {
          "type": "action",
          "id": "create_text",
          "index": 0,
          "action_type": "add_text",
          "params": {
            "text": "${item.text}",
            "start": "${item.start_time}",
            "end": "${item.end_time}",
            "track_name": "${item.target_track}",
            "transform_y": "${item.y_initial}",
            "intro_animation": "向上滑动",
            "font_size": 12.0,
            "font": "后现代体",
            "font_color": "#ffde00",
            "shadow_enabled": True
          }
        },
        {
          "type": "action",
          "id": "add_full_motion_keyframe",
          "index": 1,
          "action_type": "add_video_keyframe",
          "params": {
            "track_name": "${item.target_track}",
            "times": [
              "${item.move_time} - 0.1", "${item.move_time}",
              "${item.move_time} - 0.1", "${item.move_time}",
              "${item.move_time} - 0.1", "${item.move_time}"
            ],
            "property_types": [
              "position_y", "position_y",
              "alpha", "alpha",
              "uniform_scale", "uniform_scale"
            ],
            "values": [
              "${item.y_initial}", "${item.y_end}",
              "${item.alpha_initial}", "${item.alpha_end}",
              "${item.scale_initial}", "${item.scale_end}"
            ]
          }
        }
      ]
    }
  ]
    }

# segemnts = [{'start': 3260, 'end': 4460, 'text': '为什么我们选择把', 'words': [{'word': '为', 'start_time': 3260, 'end_time': 3420}, {'word': '什', 'start_time': 3420, 'end_time': 3540}, {'word': '么', 'start_time': 3540, 'end_time': 3620}, {'word': '我', 'start_time': 3620, 'end_time': 3740}, {'word': '们', 'start_time': 3740, 'end_time': 3900}, {'word': '选', 'start_time': 3900, 'end_time': 4060}, {'word': '择', 'start_time': 4060, 'end_time': 4180}, {'word': '把', 'start_time': 4180, 'end_time': 4460}]}, {'start': 4500, 'end': 5580, 'text': '代码开源了', 'words': [{'word': '代', 'start_time': 4500, 'end_time': 4700}, {'word': '码', 'start_time': 4700, 'end_time': 4900}, {'word': '开', 'start_time': 4940, 'end_time': 5100}, {'word': '源', 'start_time': 5180, 'end_time': 5220}, {'word': '了', 'start_time': 5340, 'end_time': 5580}]}, {'start': 5980, 'end': 7780, 'text': '明明辛辛苦苦做了半年', 'words': [{'word': '明', 'start_time': 5980, 'end_time': 6180}, {'word': '明', 'start_time': 6260, 'end_time': 6340}, {'word': '辛', 'start_time': 6420, 'end_time': 6500}, {'word': '辛', 'start_time': 6580, 'end_time': 6700}, {'word': '苦', 'start_time': 6700, 'end_time': 6860}, {'word': '苦', 'start_time': 6900, 'end_time': 7020}, {'word': '做', 'start_time': 7020, 'end_time': 7220}, {'word': '了', 'start_time': 7220, 'end_time': 7340}, {'word': '半', 'start_time': 7340, 'end_time': 7540}, {'word': '年', 'start_time': 7540, 'end_time': 7780}]}, {'start': 7980, 'end': 9580, 'text': '而且开源版本的剪辑', 'words': [{'word': '而', 'start_time': 7980, 'end_time': 8180}, {'word': '且', 'start_time': 8180, 'end_time': 8340}, {'word': '开', 'start_time': 8380, 'end_time': 8580}, {'word': '源', 'start_time': 8620, 'end_time': 8660}, {'word': '版', 'start_time': 8780, 'end_time': 8940}, {'word': '本', 'start_time': 8940, 'end_time': 9060}, {'word': '的', 'start_time': 9060, 'end_time': 9260}, {'word': '剪', 'start_time': 9260, 'end_time': 9500}, {'word': '辑', 'start_time': 9500, 'end_time': 9580}]}, {'start': 9780, 'end': 11860, 'text': ' API 的能力实际上已经', 'words': [{'word': 'API', 'start_time': 9780, 'end_time': 10100}, {'word': '的', 'start_time': 10100, 'end_time': 10300}, {'word': '能', 'start_time': 10300, 'end_time': 10460}, {'word': '力', 'start_time': 10460, 'end_time': 10620}, {'word': '实', 'start_time': 10860, 'end_time': 11060}, {'word': '际', 'start_time': 11060, 'end_time': 11220}, {'word': '上', 'start_time': 11220, 'end_time': 11420}, {'word': '已', 'start_time': 11420, 'end_time': 11660}, {'word': '经', 'start_time': 11660, 'end_time': 11860}]}, {'start': 11860, 'end': 12860, 'text': '非常丰富了', 'words': [{'word': '非', 'start_time': 11860, 'end_time': 12060}, {'word': '常', 'start_time': 12060, 'end_time': 12220}, {'word': '丰', 'start_time': 12220, 'end_time': 12460}, {'word': '富', 'start_time': 12460, 'end_time': 12620}, {'word': '了', 'start_time': 12620, 'end_time': 12860}]}, {'start': 13740, 'end': 14860, 'text': '为什么选择这么做', 'words': [{'word': '为', 'start_time': 13740, 'end_time': 13900}, {'word': '什', 'start_time': 13900, 'end_time': 13980}, {'word': '么', 'start_time': 13980, 'end_time': 14060}, {'word': '选', 'start_time': 14060, 'end_time': 14220}, {'word': '择', 'start_time': 14220, 'end_time': 14340}, {'word': '这', 'start_time': 14340, 'end_time': 14460}, {'word': '么', 'start_time': 14460, 'end_time': 14580}, {'word': '做', 'start_time': 14580, 'end_time': 14860}]}, {'start': 15260, 'end': 17540, 'text': '主要原因是我觉得未来', 'words': [{'word': '主', 'start_time': 15260, 'end_time': 15460}, {'word': '要', 'start_time': 15460, 'end_time': 15580}, {'word': '原', 'start_time': 15580, 'end_time': 15740}, {'word': '因', 'start_time': 15740, 'end_time': 15900}, {'word': '是', 'start_time': 15900, 'end_time': 16220}, {'word': '我', 'start_time': 16220, 'end_time': 16460}, {'word': '觉', 'start_time': 16460, 'end_time': 16660}, {'word': '得', 'start_time': 16660, 'end_time': 16820}, {'word': '未', 'start_time': 17020, 'end_time': 17260}, {'word': '来', 'start_time': 17260, 'end_time': 17540}]}, {'start': 17660, 'end': 19220, 'text': '一定是 AI 编程的', 'words': [{'word': '一', 'start_time': 17660, 'end_time': 17860}, {'word': '定', 'start_time': 17860, 'end_time': 18020}, {'word': '是', 'start_time': 18020, 'end_time': 18300}, {'word': 'AI', 'start_time': 18380, 'end_time': 18620}, {'word': '编', 'start_time': 18740, 'end_time': 18940}, {'word': '程', 'start_time': 18940, 'end_time': 19060}, {'word': '的', 'start_time': 19060, 'end_time': 19220}]}, {'start': 19220, 'end': 19540, 'text': '时代', 'words': [{'word': '时', 'start_time': 19220, 'end_time': 19380}, {'word': '代', 'start_time': 19380, 'end_time': 19540}]}, {'start': 20240, 'end': 21800, 'text': '人人都能通过和 ', 'words': [{'word': '人', 'start_time': 20240, 'end_time': 20440}, {'word': '人', 'start_time': 20480, 'end_time': 20640}, {'word': '都', 'start_time': 20640, 'end_time': 20880}, {'word': '能', 'start_time': 20880, 'end_time': 21160}, {'word': '通', 'start_time': 21160, 'end_time': 21360}, {'word': '过', 'start_time': 21360, 'end_time': 21520}, {'word': '和', 'start_time': 21520, 'end_time': 21800}]}, {'start': 21840, 'end': 24080, 'text': 'AI 对话的方式实现', 'words': [{'word': 'AI', 'start_time': 21840, 'end_time': 22240}, {'word': '对', 'start_time': 22240, 'end_time': 22440}, {'word': '话', 'start_time': 22440, 'end_time': 22640}, {'word': '的', 'start_time': 22640, 'end_time': 22800}, {'word': '方', 'start_time': 22800, 'end_time': 22960}, {'word': '式', 'start_time': 22960, 'end_time': 23120}, {'word': '实', 'start_time': 23640, 'end_time': 23880}, {'word': '现', 'start_time': 23880, 'end_time': 24080}]}, {'start': 24080, 'end': 25160, 'text': '自己想要的功能', 'words': [{'word': '自', 'start_time': 24080, 'end_time': 24240}, {'word': '己', 'start_time': 24240, 'end_time': 24360}, {'word': '想', 'start_time': 24360, 'end_time': 24560}, {'word': '要', 'start_time': 24560, 'end_time': 24680}, {'word': '的', 'start_time': 24680, 'end_time': 24840}, {'word': '功', 'start_time': 24840, 'end_time': 25000}, {'word': '能', 'start_time': 25000, 'end_time': 25160}]}, {'start': 25830, 'end': 28470, 'text': '那把代码开源就是一个', 'words': [{'word': '那', 'start_time': 25830, 'end_time': 26070}, {'word': '把', 'start_time': 26110, 'end_time': 26390}, {'word': '代', 'start_time': 26510, 'end_time': 26750}, {'word': '码', 'start_time': 26750, 'end_time': 26950}, {'word': '开', 'start_time': 26990, 'end_time': 27190}, {'word': '源', 'start_time': 27190, 'end_time': 27310}, {'word': '就', 'start_time': 27830, 'end_time': 28070}, {'word': '是', 'start_time': 28070, 'end_time': 28190}, {'word': '一', 'start_time': 28190, 'end_time': 28310}, {'word': '个', 'start_time': 28310, 'end_time': 28470}]}, {'start': 28470, 'end': 30710, 'text': '最好的微调全世界 ', 'words': [{'word': '最', 'start_time': 28470, 'end_time': 28710}, {'word': '好', 'start_time': 28710, 'end_time': 28950}, {'word': '的', 'start_time': 28950, 'end_time': 29190}, {'word': '微', 'start_time': 29510, 'end_time': 29630}, {'word': '调', 'start_time': 29750, 'end_time': 30030}, {'word': '全', 'start_time': 30110, 'end_time': 30350}, {'word': '世', 'start_time': 30350, 'end_time': 30510}, {'word': '界', 'start_time': 30510, 'end_time': 30710}]}, {'start': 30830, 'end': 31990, 'text': 'AI 模型的方法', 'words': [{'word': 'AI', 'start_time': 30830, 'end_time': 31070}, {'word': '模', 'start_time': 31150, 'end_time': 31350}, {'word': '型', 'start_time': 31350, 'end_time': 31470}, {'word': '的', 'start_time': 31470, 'end_time': 31630}, {'word': '方', 'start_time': 31630, 'end_time': 31790}, {'word': '法', 'start_time': 31790, 'end_time': 31990}]}, {'start': 32700, 'end': 34100, 'text': '这样大家无论用哪', 'words': [{'word': '这', 'start_time': 32700, 'end_time': 32860}, {'word': '样', 'start_time': 32860, 'end_time': 33020}, {'word': '大', 'start_time': 33020, 'end_time': 33260}, {'word': '家', 'start_time': 33260, 'end_time': 33460}, {'word': '无', 'start_time': 33500, 'end_time': 33660}, {'word': '论', 'start_time': 33660, 'end_time': 33780}, {'word': '用', 'start_time': 33780, 'end_time': 33980}, {'word': '哪', 'start_time': 33980, 'end_time': 34100}]}, {'start': 34100, 'end': 36460, 'text': '一家的 AI 去做剪辑', 'words': [{'word': '一', 'start_time': 34100, 'end_time': 34220}, {'word': '家', 'start_time': 34220, 'end_time': 34380}, {'word': '的', 'start_time': 34380, 'end_time': 34540}, {'word': 'AI', 'start_time': 34580, 'end_time': 34820}, {'word': '去', 'start_time': 34980, 'end_time': 35340}, {'word': '做', 'start_time': 35500, 'end_time': 35820}, {'word': '剪', 'start_time': 36020, 'end_time': 36300}, {'word': '辑', 'start_time': 36300, 'end_time': 36460}]}, {'start': 36620, 'end': 37820, 'text': '工具的时候', 'words': [{'word': '工', 'start_time': 36620, 'end_time': 36900}, {'word': '具', 'start_time': 36900, 'end_time': 37100}, {'word': '的', 'start_time': 37220, 'end_time': 37460}, {'word': '时', 'start_time': 37460, 'end_time': 37620}, {'word': '候', 'start_time': 37620, 'end_time': 37820}]}, {'start': 38260, 'end': 39940, 'text': '都有很大概率会用到', 'words': [{'word': '都', 'start_time': 38260, 'end_time': 38500}, {'word': '有', 'start_time': 38500, 'end_time': 38660}, {'word': '很', 'start_time': 38660, 'end_time': 38820}, {'word': '大', 'start_time': 38820, 'end_time': 39020}, {'word': '概', 'start_time': 39020, 'end_time': 39220}, {'word': '率', 'start_time': 39220, 'end_time': 39340}, {'word': '会', 'start_time': 39420, 'end_time': 39660}, {'word': '用', 'start_time': 39660, 'end_time': 39820}, {'word': '到', 'start_time': 39820, 'end_time': 39940}]}, {'start': 39940, 'end': 40780, 'text': '我们的接口', 'words': [{'word': '我', 'start_time': 39940, 'end_time': 40060}, {'word': '们', 'start_time': 40060, 'end_time': 40140}, {'word': '的', 'start_time': 40140, 'end_time': 40300}, {'word': '接', 'start_time': 40300, 'end_time': 40500}, {'word': '口', 'start_time': 40500, 'end_time': 40780}]}]
# print(asr_60348d11a5f54d2a98afb52f6acdb916(segemnts, "123"))

def apply_template(segments, draft_id):
    return asr_60348d11a5f54d2a98afb52f6acdb916(segments, draft_id)

