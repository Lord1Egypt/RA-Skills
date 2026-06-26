import json


def asr_42da310c1e4347ddb2c96dd2a5d055c2(segments, draft_id):
    subtitles = []
    index = 1
    normalized_segments = []
    if isinstance(segments, str):
        try:
            parsed = json.loads(segments)
        except Exception:
            parsed = None
        if isinstance(parsed, dict):
            inner_segments = parsed.get("segments")
            if isinstance(inner_segments, (list, tuple)):
                normalized_segments = inner_segments
        elif isinstance(parsed, (list, tuple)):
            normalized_segments = parsed
    elif isinstance(segments, (list, tuple)):
        normalized_segments = segments
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
                sub_id = f"sub_{index:03d}"
                subtitles.append({
                    "id": sub_id,
                    "text": text,
                    "start_time": start,
                    "end_time": end,
                    "target_track": "track_sub",
                })
                index += 1
            elif isinstance(item, (list, tuple)) and len(item) >= 3:
                start = float(item[0])
                end = float(item[1])
                text = str(item[2]).strip()
                sub_id = f"sub_{index:03d}"
                subtitles.append({
                    "id": sub_id,
                    "text": text,
                    "start_time": start,
                    "end_time": end,
                    "target_track": "track_sub",
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
                        "intro_animation": "向上露出",
                        "outro_animation": "向上滑动",
                        "font_size": 12.0,
                        "transform_y_px": -900,
                        "font": "俪金黑",
                        "font_color": "#ffbf17",
                        "shadow_enabled": True
                    }
                }
            ]
        }
    ]
    }

# segemnts = [[0.23, 2.07, '双十一挖到社交型冰'], [2.07, 3.87, '箱海信小榴莲500'], [3.99, 5.75, '法式款朋友见了都'], [5.75, 6.07, '要链接'], [6.39, 7.99, '60厘米超薄机身'], [8.31, 9.31, '纯平全嵌'], [9.63, 11.27, '两侧仅需3毫米'], [11.65, 12.97, '厨房显高级还百搭'], [13.13, 14.29, '真空冰箱科技'], [14.41, 15.33, '15倍保鲜'], [15.69, 18.05, '食材呢放7天仍新鲜'], [18.33, 19.69, '双系统防串味'], [19.81, 21.45, '高除菌率超省心'], [21.73, 23.29, '双十一国补八折'], [23.33, 24.49, '加专属优惠券'], [24.69, 26.25, '送399元礼'], [26.45, 27.29, '三期免息'], [27.45, 28.57, '加12年质保'], [28.91, 30.1, '买台冰箱还能成'], [30.22, 30.94, '种草达人'], [31.06, 32.3, '这波呀不亏']]
# print(asr_42da310c1e4347ddb2c96dd2a5d055c2(segemnts, "123"))

def apply_template(segments, draft_id):
    return asr_42da310c1e4347ddb2c96dd2a5d055c2(segments, draft_id)

