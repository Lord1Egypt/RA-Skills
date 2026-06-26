import json


def asr_e8d06597e17c46a8a6d9b5c60a757c26(segments, draft_id):
    subtitle_list = []
    normalized_segments = segments if isinstance(segments, (list, tuple)) else []

    for item in normalized_segments:
        try:
            if isinstance(item, dict):
                start = item.get("start", 0)
                end = item.get("end", start)
                content = str(item.get("text") or "").strip()
                en_content = str(item.get("en") or "").strip()
                keywords = item.get("keywords") or []
            elif isinstance(item, (list, tuple)) and len(item) >= 3:
                start = item[0]
                end = item[1]
                content = str(item[2] or "").strip()
                en_content = ""
                keywords = []
            else:
                continue

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

            h_start = 0
            h_end = 0
            if isinstance(keywords, str):
                keywords = [keywords]
            if isinstance(keywords, (list, tuple)):
                for kw in keywords:
                    kw_text = str(kw or "").strip()
                    if kw_text and kw_text in content:
                        h_start = content.find(kw_text)
                        h_end = h_start + len(kw_text)
                        break
            if h_end <= h_start:
                h_start, h_end = 0, 0

            has_keyword = h_end > h_start
            subtitle_item = {
                "content": content,
                "en_content": en_content,
                "has_keyword": has_keyword,
                "start": start,
                "end": end,
                "intro_duration": end-start,
                "transform_y_cn": -0.475,
                "transform_y_en": -0.6
            }
            if has_keyword:
                subtitle_item["h_start"] = h_start
                subtitle_item["h_end"] = h_end
            subtitle_list.append(subtitle_item)
        except Exception:
            continue

    return {
        "inputs": {
            "subtitle_list": subtitle_list
        },
        "draft_id": draft_id,
        "script": [
    {
      "type": "for",
      "in": "${subtitle_list}",
      "id": "subtitle_loop",
      "index": 0,
      "loop": [
        {
          "type": "if",
          "condition": "${item.has_keyword} == True",
          "id": "check_highlight",
          "index": 0,
          "then": [
            {
              "type": "action",
              "action_type": "add_text",
              "id": "add_cn_highlight",
              "index": 0,
              "params": {
                "text": "${item.content}",
                "start": "${item.start}",
                "end": "${item.end}",
                "track_name": "subtitle_cn",
                "font": "港风繁体",
                "font_size": 12.0,
                "intro_animation": "打字机_II",
                "intro_duration": "${item.intro_duration}",
                "font_color": "#FFFFFF",
                "transform_y": "${item.transform_y_cn}",
                "fixed_width": 0.6,
                "shadow_enabled": True,
                "text_styles": [
                  {
                    "start": "${item.h_start}",
                    "end": "${item.h_end}",
                    "style": {
                      "size": 16.0,
                      "color": "#FE8A80",
                      "bold": True
                    }
                  }
                ]
              }
            }
          ],
          "else": [
            {
              "type": "action",
              "action_type": "add_text",
              "id": "add_cn_normal",
              "index": 0,
              "params": {
                "text": "${item.content}",
                "start": "${item.start}",
                "end": "${item.end}",
                "track_name": "subtitle_cn",
                "font": "港风繁体",
                "font_size": 12.0,
                "intro_animation": "打字机_II",
                "intro_duration": "${item.intro_duration}",
                "font_color": "#FFFFFF",
                "transform_y": "${item.transform_y_cn}",
                "fixed_width": 0.6,
                "shadow_enabled": True
              }
            }
          ]
        },
        {
          "type": "action",
          "action_type": "add_text",
          "id": "add_en_subtitle",
          "index": 1,
          "params": {
            "text": "${item.en_content}",
            "start": "${item.start}",
            "end": "${item.end}",
            "track_name": "subtitle_en",
            "font": "港风繁体",
            "font_size": 6.0,
            "intro_animation": "打字机_II",
            "intro_duration": "${item.intro_duration}",
            "font_color": "#FFFFFF",
            "transform_y": "${item.transform_y_en}",
            "fixed_width": 0.6,
            "shadow_enabled": True
          }
        }
      ]
    }
  ]
    }


# segemnts = [{'start': 450, 'end': 930, 'text': '家人们，', 'words': [{'confidence': 0, 'end_time': 610, 'start_time': 450, 'text': '家'}, {'confidence': 0, 'end_time': 730, 'start_time': 610, 'text': '人'}, {'confidence': 0, 'end_time': 930, 'start_time': 730, 'text': '们'}], 'keywords': [], 'en': 'Hey everyone,'}, {'start': 1210, 'end': 2690, 'text': '爱视频界的 Banana，', 'words': [{'confidence': 0, 'end_time': 1370, 'start_time': 1210, 'text': '爱'}, {'confidence': 0, 'end_time': 1610, 'start_time': 1530, 'text': '视'}, {'confidence': 0, 'end_time': 1690, 'start_time': 1610, 'text': '频'}, {'confidence': 0, 'end_time': 1970, 'start_time': 1810, 'text': '界'}, {'confidence': 0, 'end_time': 2210, 'start_time': 1970, 'text': '的'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 2690, 'start_time': 2370, 'text': 'Banana'}], 'keywords': [], 'en': "The 'Banana' of video circles,"}, {'start': 3290, 'end': 4970, 'text': '可灵欧一闪亮登场了，', 'words': [{'confidence': 0, 'end_time': 3330, 'start_time': 3290, 'text': '可'}, {'confidence': 0, 'end_time': 3490, 'start_time': 3450, 'text': '灵'}, {'confidence': 0, 'end_time': 3690, 'start_time': 3650, 'text': '欧'}, {'confidence': 0, 'end_time': 3850, 'start_time': 3810, 'text': '一'}, {'confidence': 0, 'end_time': 4170, 'start_time': 4010, 'text': '闪'}, {'confidence': 0, 'end_time': 4370, 'start_time': 4170, 'text': '亮'}, {'confidence': 0, 'end_time': 4570, 'start_time': 4370, 'text': '登'}, {'confidence': 0, 'end_time': 4730, 'start_time': 4570, 'text': '场'}, {'confidence': 0, 'end_time': 4970, 'start_time': 4730, 'text': '了'}], 'keywords': ['可灵欧一'], 'en': 'Kling O1 has made its debut,'}, {'start': 5290, 'end': 6050, 'text': '它就像一颗', 'words': [{'confidence': 0, 'end_time': 5370, 'start_time': 5290, 'text': '它'}, {'confidence': 0, 'end_time': 5570, 'start_time': 5410, 'text': '就'}, {'confidence': 0, 'end_time': 5730, 'start_time': 5570, 'text': '像'}, {'confidence': 0, 'end_time': 5890, 'start_time': 5730, 'text': '一'}, {'confidence': 0, 'end_time': 6050, 'start_time': 5890, 'text': '颗'}], 'keywords': [], 'en': 'It is like a'}, {'start': 6130, 'end': 7370, 'text': '在 AI 视频领域', 'words': [{'confidence': 0, 'end_time': 6410, 'start_time': 6130, 'text': '在'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 6650, 'start_time': 6450, 'text': 'AI'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 6890, 'start_time': 6730, 'text': '视'}, {'confidence': 0, 'end_time': 7050, 'start_time': 6890, 'text': '频'}, {'confidence': 0, 'end_time': 7210, 'start_time': 7050, 'text': '领'}, {'confidence': 0, 'end_time': 7370, 'start_time': 7210, 'text': '域'}], 'keywords': ['AI 视频'], 'en': 'rising star in the AI video field,'}, {'start': 7570, 'end': 8690, 'text': '冉冉升起的星星，', 'words': [{'confidence': 0, 'end_time': 7610, 'start_time': 7570, 'text': '冉'}, {'confidence': 0, 'end_time': 7810, 'start_time': 7730, 'text': '冉'}, {'confidence': 0, 'end_time': 8050, 'start_time': 7890, 'text': '升'}, {'confidence': 0, 'end_time': 8170, 'start_time': 8050, 'text': '起'}, {'confidence': 0, 'end_time': 8370, 'start_time': 8170, 'text': '的'}, {'confidence': 0, 'end_time': 8490, 'start_time': 8370, 'text': '星'}, {'confidence': 0, 'end_time': 8690, 'start_time': 8570, 'text': '星'}], 'keywords': [], 'en': 'shining brightly,'}, {'start': 9010, 'end': 10210, 'text': '带着无限惊喜。', 'words': [{'confidence': 0, 'end_time': 9210, 'start_time': 9010, 'text': '带'}, {'confidence': 0, 'end_time': 9330, 'start_time': 9210, 'text': '着'}, {'confidence': 0, 'end_time': 9570, 'start_time': 9330, 'text': '无'}, {'confidence': 0, 'end_time': 9730, 'start_time': 9570, 'text': '限'}, {'confidence': 0, 'end_time': 10010, 'start_time': 9810, 'text': '惊'}, {'confidence': 0, 'end_time': 10210, 'start_time': 10010, 'text': '喜'}], 'keywords': [], 'en': 'bringing endless surprises.'}, {'start': 11180, 'end': 12340, 'text': '可灵 o e 拥有', 'words': [{'confidence': 0, 'end_time': 11260, 'start_time': 11180, 'text': '可'}, {'confidence': 0, 'end_time': 11420, 'start_time': 11380, 'text': '灵'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 11580, 'start_time': 11540, 'text': 'o'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 11780, 'start_time': 11700, 'text': 'e'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 12140, 'start_time': 11980, 'text': '拥'}, {'confidence': 0, 'end_time': 12340, 'start_time': 12140, 'text': '有'}], 'keywords': ['可灵 o e'], 'en': 'Kling o e possesses'}, {'start': 12340, 'end': 13420, 'text': '强大的 AI 功能，', 'words': [{'confidence': 0, 'end_time': 12500, 'start_time': 12340, 'text': '强'}, {'confidence': 0, 'end_time': 12620, 'start_time': 12500, 'text': '大'}, {'confidence': 0, 'end_time': 12780, 'start_time': 12620, 'text': '的'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 13020, 'start_time': 12860, 'text': 'AI'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 13260, 'start_time': 13100, 'text': '功'}, {'confidence': 0, 'end_time': 13420, 'start_time': 13260, 'text': '能'}], 'keywords': ['AI 功能'], 'en': 'powerful AI functions,'}, {'start': 13620, 'end': 15060, 'text': '能快速且精准的', 'words': [{'confidence': 0, 'end_time': 13900, 'start_time': 13620, 'text': '能'}, {'confidence': 0, 'end_time': 14140, 'start_time': 13900, 'text': '快'}, {'confidence': 0, 'end_time': 14300, 'start_time': 14140, 'text': '速'}, {'confidence': 0, 'end_time': 14660, 'start_time': 14420, 'text': '且'}, {'confidence': 0, 'end_time': 14820, 'start_time': 14700, 'text': '精'}, {'confidence': 0, 'end_time': 14980, 'start_time': 14820, 'text': '准'}, {'confidence': 0, 'end_time': 15060, 'start_time': 14980, 'text': '的'}], 'keywords': [], 'en': 'which can quickly and accurately'}, {'start': 15100, 'end': 15740, 'text': '处理视频，', 'words': [{'confidence': 0, 'end_time': 15220, 'start_time': 15100, 'text': '处'}, {'confidence': 0, 'end_time': 15380, 'start_time': 15220, 'text': '理'}, {'confidence': 0, 'end_time': 15540, 'start_time': 15380, 'text': '视'}, {'confidence': 0, 'end_time': 15740, 'start_time': 15540, 'text': '频'}], 'keywords': [], 'en': 'process videos.'}, {'start': 16100, 'end': 17020, 'text': '无论是剪辑、', 'words': [{'confidence': 0, 'end_time': 16300, 'start_time': 16100, 'text': '无'}, {'confidence': 0, 'end_time': 16420, 'start_time': 16300, 'text': '论'}, {'confidence': 0, 'end_time': 16620, 'start_time': 16420, 'text': '是'}, {'confidence': 0, 'end_time': 16860, 'start_time': 16620, 'text': '剪'}, {'confidence': 0, 'end_time': 17020, 'start_time': 16860, 'text': '辑'}], 'keywords': [], 'en': 'Whether it is editing,'}, {'start': 17220, 'end': 18020, 'text': '特效添加，', 'words': [{'confidence': 0, 'end_time': 17420, 'start_time': 17220, 'text': '特'}, {'confidence': 0, 'end_time': 17580, 'start_time': 17420, 'text': '效'}, {'confidence': 0, 'end_time': 17780, 'start_time': 17620, 'text': '添'}, {'confidence': 0, 'end_time': 18020, 'start_time': 17780, 'text': '加'}], 'keywords': [], 'en': 'adding special effects,'}, {'start': 18140, 'end': 19140, 'text': '还是智能配音，', 'words': [{'confidence': 0, 'end_time': 18340, 'start_time': 18140, 'text': '还'}, {'confidence': 0, 'end_time': 18460, 'start_time': 18340, 'text': '是'}, {'confidence': 0, 'end_time': 18620, 'start_time': 18460, 'text': '智'}, {'confidence': 0, 'end_time': 18740, 'start_time': 18620, 'text': '能'}, {'confidence': 0, 'end_time': 18940, 'start_time': 18740, 'text': '配'}, {'confidence': 0, 'end_time': 19140, 'start_time': 18940, 'text': '音'}], 'keywords': ['智能配音'], 'en': 'or intelligent voiceover,'}, {'start': 19340, 'end': 20620, 'text': '它都能轻松搞定。', 'words': [{'confidence': 0, 'end_time': 19380, 'start_time': 19340, 'text': '它'}, {'confidence': 0, 'end_time': 19620, 'start_time': 19460, 'text': '都'}, {'confidence': 0, 'end_time': 19820, 'start_time': 19620, 'text': '能'}, {'confidence': 0, 'end_time': 20020, 'start_time': 19820, 'text': '轻'}, {'confidence': 0, 'end_time': 20180, 'start_time': 20020, 'text': '松'}, {'confidence': 0, 'end_time': 20420, 'start_time': 20180, 'text': '搞'}, {'confidence': 0, 'end_time': 20620, 'start_time': 20420, 'text': '定'}], 'keywords': [], 'en': 'it can handle them all easily.'}, {'start': 21710, 'end': 22750, 'text': '有了可灵 O1，', 'words': [{'confidence': 0, 'end_time': 21910, 'start_time': 21710, 'text': '有'}, {'confidence': 0, 'end_time': 22030, 'start_time': 21910, 'text': '了'}, {'confidence': 0, 'end_time': 22150, 'start_time': 22030, 'text': '可'}, {'confidence': 0, 'end_time': 22310, 'start_time': 22270, 'text': '灵'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 22750, 'start_time': 22470, 'text': 'O1'}], 'keywords': ['可灵 O1'], 'en': 'With Kling O1,'}, {'start': 23190, 'end': 24750, 'text': '就算你是视频小白，', 'words': [{'confidence': 0, 'end_time': 23430, 'start_time': 23190, 'text': '就'}, {'confidence': 0, 'end_time': 23590, 'start_time': 23430, 'text': '算'}, {'confidence': 0, 'end_time': 23750, 'start_time': 23590, 'text': '你'}, {'confidence': 0, 'end_time': 23950, 'start_time': 23750, 'text': '是'}, {'confidence': 0, 'end_time': 24110, 'start_time': 23950, 'text': '视'}, {'confidence': 0, 'end_time': 24270, 'start_time': 24110, 'text': '频'}, {'confidence': 0, 'end_time': 24510, 'start_time': 24270, 'text': '小'}, {'confidence': 0, 'end_time': 24750, 'start_time': 24510, 'text': '白'}], 'keywords': ['视频小白'], 'en': 'even if you are a video novice,'}, {'start': 24910, 'end': 26470, 'text': '也能秒变创作大神，', 'words': [{'confidence': 0, 'end_time': 25110, 'start_time': 24910, 'text': '也'}, {'confidence': 0, 'end_time': 25270, 'start_time': 25110, 'text': '能'}, {'confidence': 0, 'end_time': 25470, 'start_time': 25270, 'text': '秒'}, {'confidence': 0, 'end_time': 25670, 'start_time': 25470, 'text': '变'}, {'confidence': 0, 'end_time': 25870, 'start_time': 25670, 'text': '创'}, {'confidence': 0, 'end_time': 25990, 'start_time': 25870, 'text': '作'}, {'confidence': 0, 'end_time': 26230, 'start_time': 25990, 'text': '大'}, {'confidence': 0, 'end_time': 26470, 'start_time': 26230, 'text': '神'}], 'keywords': ['创作大神'], 'en': 'you can become a creative pro,'}, {'start': 26750, 'end': 27670, 'text': '轻松产出', 'words': [{'confidence': 0, 'end_time': 27030, 'start_time': 26750, 'text': '轻'}, {'confidence': 0, 'end_time': 27150, 'start_time': 27030, 'text': '松'}, {'confidence': 0, 'end_time': 27390, 'start_time': 27190, 'text': '产'}, {'confidence': 0, 'end_time': 27670, 'start_time': 27390, 'text': '出'}], 'keywords': [], 'en': 'and easily produce'}, {'start': 27750, 'end': 29270, 'text': '高质量的 AI 视频。', 'words': [{'confidence': 0, 'end_time': 28030, 'start_time': 27750, 'text': '高'}, {'confidence': 0, 'end_time': 28190, 'start_time': 28030, 'text': '质'}, {'confidence': 0, 'end_time': 28310, 'start_time': 28190, 'text': '量'}, {'confidence': 0, 'end_time': 28510, 'start_time': 28310, 'text': '的'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 28750, 'start_time': 28550, 'text': 'AI'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 29070, 'start_time': 28870, 'text': '视'}, {'confidence': 0, 'end_time': 29270, 'start_time': 29070, 'text': '频'}], 'keywords': [], 'en': 'high-quality AI videos.'}, {'start': 29670, 'end': 30390, 'text': '别再犹豫，', 'words': [{'confidence': 0, 'end_time': 29910, 'start_time': 29670, 'text': '别'}, {'confidence': 0, 'end_time': 30110, 'start_time': 29910, 'text': '再'}, {'confidence': 0, 'end_time': 30230, 'start_time': 30110, 'text': '犹'}, {'confidence': 0, 'end_time': 30390, 'start_time': 30230, 'text': '豫'}], 'keywords': [], 'en': "Don't hesitate,"}, {'start': 30590, 'end': 31590, 'text': '赶紧让可灵 O1', 'words': [{'confidence': 0, 'end_time': 30750, 'start_time': 30590, 'text': '赶'}, {'confidence': 0, 'end_time': 30830, 'start_time': 30750, 'text': '紧'}, {'confidence': 0, 'end_time': 31030, 'start_time': 30830, 'text': '让'}, {'confidence': 0, 'end_time': 31150, 'start_time': 31030, 'text': '可'}, {'confidence': 0, 'end_time': 31270, 'start_time': 31230, 'text': '灵'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 31590, 'start_time': 31390, 'text': 'O1'}], 'keywords': [], 'en': 'quickly let Kling O1'}, {'start': 31790, 'end': 33110, 'text': '成为你视频创作的', 'words': [{'confidence': 0, 'end_time': 31950, 'start_time': 31790, 'text': '成'}, {'confidence': 0, 'end_time': 32070, 'start_time': 31950, 'text': '为'}, {'confidence': 0, 'end_time': 32230, 'start_time': 32070, 'text': '你'}, {'confidence': 0, 'end_time': 32390, 'start_time': 32230, 'text': '视'}, {'confidence': 0, 'end_time': 32510, 'start_time': 32390, 'text': '频'}, {'confidence': 0, 'end_time': 32710, 'start_time': 32550, 'text': '创'}, {'confidence': 0, 'end_time': 32830, 'start_time': 32710, 'text': '作'}, {'confidence': 0, 'end_time': 33110, 'start_time': 32830, 'text': '的'}], 'keywords': [], 'en': 'become your video creation'}, {'start': 33150, 'end': 34190, 'text': '得力助手吧！', 'words': [{'confidence': 0, 'end_time': 33350, 'start_time': 33150, 'text': '得'}, {'confidence': 0, 'end_time': 33510, 'start_time': 33350, 'text': '力'}, {'confidence': 0, 'end_time': 33750, 'start_time': 33550, 'text': '助'}, {'confidence': 0, 'end_time': 33910, 'start_time': 33750, 'text': '手'}, {'confidence': 0, 'end_time': 34190, 'start_time': 33910, 'text': '吧'}], 'keywords': ['得力助手'], 'en': 'competent assistant!'}]
# segemnts = [{'start': 450, 'end': 930, 'text': '家人们', 'words': [{'confidence': 0, 'end_time': 610, 'start_time': 450, 'text': '家'}, {'confidence': 0, 'end_time': 730, 'start_time': 610, 'text': '人'}, {'confidence': 0, 'end_time': 930, 'start_time': 730, 'text': '们'}], 'keywords': [], 'en': 'Hey everyone'}, {'start': 0, 'end': 0, 'text': '视频界的 Banana', 'words': [], 'keywords': ['Banana'], 'en': 'The Banana of the video world'}, {'start': 0, 'end': 0, 'text': '可灵欧一闪亮登场了', 'words': [], 'keywords': ['可灵欧一'], 'en': 'Kling O1 makes its grand debut'}, {'start': 0, 'end': 0, 'text': '它像一颗冉冉升起的星星', 'words': [], 'keywords': [], 'en': 'It is like a rising star'}, {'start': 0, 'end': 0, 'text': '在 AI 视频领域', 'words': [], 'keywords': [], 'en': 'In the field of AI video'}, {'start': 0, 'end': 0, 'text': '带着无限惊喜', 'words': [], 'keywords': [], 'en': 'Bringing infinite surprises'}, {'start': 0, 'end': 0, 'text': '可灵 o e 拥有强大功能', 'words': [], 'keywords': [], 'en': 'Kling o e has powerful features'}, {'start': 0, 'end': 0, 'text': '能快速精准的处理视频', 'words': [], 'keywords': [], 'en': 'It processes videos fast and accurately'}, {'start': 0, 'end': 0, 'text': '无论是剪辑特效添加', 'words': [], 'keywords': [], 'en': 'Whether it is editing or adding effects'}, {'start': 0, 'end': 0, 'text': '还是智能配音', 'words': [], 'keywords': ['智能配音'], 'en': 'Or smart voiceovers'}, {'start': 0, 'end': 0, 'text': '它都能轻松搞定', 'words': [], 'keywords': [], 'en': 'It can handle it all easily'}, {'start': 0, 'end': 0, 'text': '有了可灵 O1', 'words': [], 'keywords': [], 'en': 'With Kling O1'}, {'start': 0, 'end': 0, 'text': '就算你是视频小白', 'words': [], 'keywords': ['视频小白'], 'en': 'Even if you are a video novice'}, {'start': 0, 'end': 0, 'text': '也能秒变创作大神', 'words': [], 'keywords': [], 'en': 'You can become a creative master in seconds'}, {'start': 0, 'end': 0, 'text': '轻松产出高质量 AI 视频', 'words': [], 'keywords': [], 'en': 'Easily produce high-quality AI videos'}, {'start': 0, 'end': 0, 'text': '别再犹豫', 'words': [], 'keywords': [], 'en': "Don't hesitate any longer"}, {'start': 0, 'end': 0, 'text': '让可灵 O1 成为助手', 'words': [], 'keywords': [], 'en': 'Let Kling O1 become your assistant'}]
# segemnts = [{'start': 450, 'end': 930, 'text': '家人们', 'words': [{'confidence': 0, 'end_time': 610, 'start_time': 450, 'text': '家'}, {'confidence': 0, 'end_time': 730, 'start_time': 610, 'text': '人'}, {'confidence': 0, 'end_time': 930, 'start_time': 730, 'text': '们'}], 'keywords': [], 'en': 'Hey everyone'}, {'start': 1210, 'end': 2690, 'text': '爱视频界的 Banana', 'words': [{'confidence': 0, 'end_time': 1370, 'start_time': 1210, 'text': '爱'}, {'confidence': 0, 'end_time': 1610, 'start_time': 1530, 'text': '视'}, {'confidence': 0, 'end_time': 1690, 'start_time': 1610, 'text': '频'}, {'confidence': 0, 'end_time': 1970, 'start_time': 1810, 'text': '界'}, {'confidence': 0, 'end_time': 2210, 'start_time': 1970, 'text': '的'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 2690, 'start_time': 2370, 'text': 'Banana'}], 'keywords': ['Banana'], 'en': 'The Banana of the video world'}, {'start': 3290, 'end': 4970, 'text': '可灵欧一闪亮登场了', 'words': [{'confidence': 0, 'end_time': 3330, 'start_time': 3290, 'text': '可'}, {'confidence': 0, 'end_time': 3490, 'start_time': 3450, 'text': '灵'}, {'confidence': 0, 'end_time': 3690, 'start_time': 3650, 'text': '欧'}, {'confidence': 0, 'end_time': 3850, 'start_time': 3810, 'text': '一'}, {'confidence': 0, 'end_time': 4170, 'start_time': 4010, 'text': '闪'}, {'confidence': 0, 'end_time': 4370, 'start_time': 4170, 'text': '亮'}, {'confidence': 0, 'end_time': 4570, 'start_time': 4370, 'text': '登'}, {'confidence': 0, 'end_time': 4730, 'start_time': 4570, 'text': '场'}, {'confidence': 0, 'end_time': 4970, 'start_time': 4730, 'text': '了'}], 'keywords': ['可灵欧一'], 'en': 'Kling O1 has made its grand debut'}, {'start': 5290, 'end': 6050, 'text': '它就像一颗', 'words': [{'confidence': 0, 'end_time': 5370, 'start_time': 5290, 'text': '它'}, {'confidence': 0, 'end_time': 5570, 'start_time': 5410, 'text': '就'}, {'confidence': 0, 'end_time': 5730, 'start_time': 5570, 'text': '像'}, {'confidence': 0, 'end_time': 5890, 'start_time': 5730, 'text': '一'}, {'confidence': 0, 'end_time': 6050, 'start_time': 5890, 'text': '颗'}], 'keywords': [], 'en': 'It is just like a'}, {'start': 6130, 'end': 7370, 'text': '在 AI 视频领域', 'words': [{'confidence': 0, 'end_time': 6410, 'start_time': 6130, 'text': '在'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 6650, 'start_time': 6450, 'text': 'AI'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 6890, 'start_time': 6730, 'text': '视'}, {'confidence': 0, 'end_time': 7050, 'start_time': 6890, 'text': '频'}, {'confidence': 0, 'end_time': 7210, 'start_time': 7050, 'text': '领'}, {'confidence': 0, 'end_time': 7370, 'start_time': 7210, 'text': '域'}], 'keywords': ['AI'], 'en': 'In the field of AI video'}, {'start': 7570, 'end': 8690, 'text': '冉冉升起的星星', 'words': [{'confidence': 0, 'end_time': 7610, 'start_time': 7570, 'text': '冉'}, {'confidence': 0, 'end_time': 7810, 'start_time': 7730, 'text': '冉'}, {'confidence': 0, 'end_time': 8050, 'start_time': 7890, 'text': '升'}, {'confidence': 0, 'end_time': 8170, 'start_time': 8050, 'text': '起'}, {'confidence': 0, 'end_time': 8370, 'start_time': 8170, 'text': '的'}, {'confidence': 0, 'end_time': 8490, 'start_time': 8370, 'text': '星'}, {'confidence': 0, 'end_time': 8690, 'start_time': 8570, 'text': '星'}], 'keywords': ['星星'], 'en': 'Rising star'}, {'start': 9010, 'end': 10210, 'text': '带着无限惊喜', 'words': [{'confidence': 0, 'end_time': 9210, 'start_time': 9010, 'text': '带'}, {'confidence': 0, 'end_time': 9330, 'start_time': 9210, 'text': '着'}, {'confidence': 0, 'end_time': 9570, 'start_time': 9330, 'text': '无'}, {'confidence': 0, 'end_time': 9730, 'start_time': 9570, 'text': '限'}, {'confidence': 0, 'end_time': 10010, 'start_time': 9810, 'text': '惊'}, {'confidence': 0, 'end_time': 10210, 'start_time': 10010, 'text': '喜'}], 'keywords': [], 'en': 'Bringing infinite surprises'}, {'start': 11180, 'end': 12340, 'text': '可灵 o e 拥有', 'words': [{'confidence': 0, 'end_time': 11260, 'start_time': 11180, 'text': '可'}, {'confidence': 0, 'end_time': 11420, 'start_time': 11380, 'text': '灵'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 11580, 'start_time': 11540, 'text': 'o'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 11780, 'start_time': 11700, 'text': 'e'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 12140, 'start_time': 11980, 'text': '拥'}, {'confidence': 0, 'end_time': 12340, 'start_time': 12140, 'text': '有'}], 'keywords': [], 'en': 'Kling o e possesses'}, {'start': 12340, 'end': 13420, 'text': '强大的 AI 功能', 'words': [{'confidence': 0, 'end_time': 12500, 'start_time': 12340, 'text': '强'}, {'confidence': 0, 'end_time': 12620, 'start_time': 12500, 'text': '大'}, {'confidence': 0, 'end_time': 12780, 'start_time': 12620, 'text': '的'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 13020, 'start_time': 12860, 'text': 'AI'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 13260, 'start_time': 13100, 'text': '功'}, {'confidence': 0, 'end_time': 13420, 'start_time': 13260, 'text': '能'}], 'keywords': [], 'en': 'Powerful AI functions'}, {'start': 13620, 'end': 15060, 'text': '能快速且精准的', 'words': [{'confidence': 0, 'end_time': 13900, 'start_time': 13620, 'text': '能'}, {'confidence': 0, 'end_time': 14140, 'start_time': 13900, 'text': '快'}, {'confidence': 0, 'end_time': 14300, 'start_time': 14140, 'text': '速'}, {'confidence': 0, 'end_time': 14660, 'start_time': 14420, 'text': '且'}, {'confidence': 0, 'end_time': 14820, 'start_time': 14700, 'text': '精'}, {'confidence': 0, 'end_time': 14980, 'start_time': 14820, 'text': '准'}, {'confidence': 0, 'end_time': 15060, 'start_time': 14980, 'text': '的'}], 'keywords': [], 'en': 'Can quickly and accurately'}, {'start': 15100, 'end': 15740, 'text': '处理视频', 'words': [{'confidence': 0, 'end_time': 15220, 'start_time': 15100, 'text': '处'}, {'confidence': 0, 'end_time': 15380, 'start_time': 15220, 'text': '理'}, {'confidence': 0, 'end_time': 15540, 'start_time': 15380, 'text': '视'}, {'confidence': 0, 'end_time': 15740, 'start_time': 15540, 'text': '频'}], 'keywords': ['处理'], 'en': 'Process videos'}, {'start': 16100, 'end': 17020, 'text': '无论是剪辑', 'words': [{'confidence': 0, 'end_time': 16300, 'start_time': 16100, 'text': '无'}, {'confidence': 0, 'end_time': 16420, 'start_time': 16300, 'text': '论'}, {'confidence': 0, 'end_time': 16620, 'start_time': 16420, 'text': '是'}, {'confidence': 0, 'end_time': 16860, 'start_time': 16620, 'text': '剪'}, {'confidence': 0, 'end_time': 17020, 'start_time': 16860, 'text': '辑'}], 'keywords': ['剪辑'], 'en': "Whether it's editing"}, {'start': 17220, 'end': 18020, 'text': '特效添加', 'words': [{'confidence': 0, 'end_time': 17420, 'start_time': 17220, 'text': '特'}, {'confidence': 0, 'end_time': 17580, 'start_time': 17420, 'text': '效'}, {'confidence': 0, 'end_time': 17780, 'start_time': 17620, 'text': '添'}, {'confidence': 0, 'end_time': 18020, 'start_time': 17780, 'text': '加'}], 'keywords': ['特效'], 'en': 'Adding special effects'}, {'start': 18140, 'end': 19140, 'text': '还是智能配音', 'words': [{'confidence': 0, 'end_time': 18340, 'start_time': 18140, 'text': '还'}, {'confidence': 0, 'end_time': 18460, 'start_time': 18340, 'text': '是'}, {'confidence': 0, 'end_time': 18620, 'start_time': 18460, 'text': '智'}, {'confidence': 0, 'end_time': 18740, 'start_time': 18620, 'text': '能'}, {'confidence': 0, 'end_time': 18940, 'start_time': 18740, 'text': '配'}, {'confidence': 0, 'end_time': 19140, 'start_time': 18940, 'text': '音'}], 'keywords': ['配音'], 'en': 'Or intelligent dubbing'}, {'start': 19340, 'end': 20620, 'text': '它都能轻松搞定', 'words': [{'confidence': 0, 'end_time': 19380, 'start_time': 19340, 'text': '它'}, {'confidence': 0, 'end_time': 19620, 'start_time': 19460, 'text': '都'}, {'confidence': 0, 'end_time': 19820, 'start_time': 19620, 'text': '能'}, {'confidence': 0, 'end_time': 20020, 'start_time': 19820, 'text': '轻'}, {'confidence': 0, 'end_time': 20180, 'start_time': 20020, 'text': '松'}, {'confidence': 0, 'end_time': 20420, 'start_time': 20180, 'text': '搞'}, {'confidence': 0, 'end_time': 20620, 'start_time': 20420, 'text': '定'}], 'keywords': [], 'en': 'It can handle it all easily'}, {'start': 21710, 'end': 22750, 'text': '有了可灵 O1', 'words': [{'confidence': 0, 'end_time': 21910, 'start_time': 21710, 'text': '有'}, {'confidence': 0, 'end_time': 22030, 'start_time': 21910, 'text': '了'}, {'confidence': 0, 'end_time': 22150, 'start_time': 22030, 'text': '可'}, {'confidence': 0, 'end_time': 22310, 'start_time': 22270, 'text': '灵'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 22750, 'start_time': 22470, 'text': 'O1'}], 'keywords': ['可灵 O1'], 'en': 'With Kling O1'}, {'start': 23190, 'end': 24750, 'text': '就算你是视频小白', 'words': [{'confidence': 0, 'end_time': 23430, 'start_time': 23190, 'text': '就'}, {'confidence': 0, 'end_time': 23590, 'start_time': 23430, 'text': '算'}, {'confidence': 0, 'end_time': 23750, 'start_time': 23590, 'text': '你'}, {'confidence': 0, 'end_time': 23950, 'start_time': 23750, 'text': '是'}, {'confidence': 0, 'end_time': 24110, 'start_time': 23950, 'text': '视'}, {'confidence': 0, 'end_time': 24270, 'start_time': 24110, 'text': '频'}, {'confidence': 0, 'end_time': 24510, 'start_time': 24270, 'text': '小'}, {'confidence': 0, 'end_time': 24750, 'start_time': 24510, 'text': '白'}], 'keywords': ['小白'], 'en': 'Even if you are a video novice'}, {'start': 24910, 'end': 26470, 'text': '也能秒变创作大神', 'words': [{'confidence': 0, 'end_time': 25110, 'start_time': 24910, 'text': '也'}, {'confidence': 0, 'end_time': 25270, 'start_time': 25110, 'text': '能'}, {'confidence': 0, 'end_time': 25470, 'start_time': 25270, 'text': '秒'}, {'confidence': 0, 'end_time': 25670, 'start_time': 25470, 'text': '变'}, {'confidence': 0, 'end_time': 25870, 'start_time': 25670, 'text': '创'}, {'confidence': 0, 'end_time': 25990, 'start_time': 25870, 'text': '作'}, {'confidence': 0, 'end_time': 26230, 'start_time': 25990, 'text': '大'}, {'confidence': 0, 'end_time': 26470, 'start_time': 26230, 'text': '神'}], 'keywords': ['大神'], 'en': 'Can become a creative pro instantly'}, {'start': 26750, 'end': 27670, 'text': '轻松产出', 'words': [{'confidence': 0, 'end_time': 27030, 'start_time': 26750, 'text': '轻'}, {'confidence': 0, 'end_time': 27150, 'start_time': 27030, 'text': '松'}, {'confidence': 0, 'end_time': 27390, 'start_time': 27190, 'text': '产'}, {'confidence': 0, 'end_time': 27670, 'start_time': 27390, 'text': '出'}], 'keywords': [], 'en': 'Easily produce'}, {'start': 27750, 'end': 29270, 'text': '高质量的 AI 视频', 'words': [{'confidence': 0, 'end_time': 28030, 'start_time': 27750, 'text': '高'}, {'confidence': 0, 'end_time': 28190, 'start_time': 28030, 'text': '质'}, {'confidence': 0, 'end_time': 28310, 'start_time': 28190, 'text': '量'}, {'confidence': 0, 'end_time': 28510, 'start_time': 28310, 'text': '的'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 28750, 'start_time': 28550, 'text': 'AI'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 29070, 'start_time': 28870, 'text': '视'}, {'confidence': 0, 'end_time': 29270, 'start_time': 29070, 'text': '频'}], 'keywords': [], 'en': 'High-quality AI videos'}, {'start': 29670, 'end': 30390, 'text': '别再犹豫', 'words': [{'confidence': 0, 'end_time': 29910, 'start_time': 29670, 'text': '别'}, {'confidence': 0, 'end_time': 30110, 'start_time': 29910, 'text': '再'}, {'confidence': 0, 'end_time': 30230, 'start_time': 30110, 'text': '犹'}, {'confidence': 0, 'end_time': 30390, 'start_time': 30230, 'text': '豫'}], 'keywords': [], 'en': "Don't hesitate any longer"}, {'start': 30590, 'end': 31590, 'text': '赶紧让可灵 O1', 'words': [{'confidence': 0, 'end_time': 30750, 'start_time': 30590, 'text': '赶'}, {'confidence': 0, 'end_time': 30830, 'start_time': 30750, 'text': '紧'}, {'confidence': 0, 'end_time': 31030, 'start_time': 30830, 'text': '让'}, {'confidence': 0, 'end_time': 31150, 'start_time': 31030, 'text': '可'}, {'confidence': 0, 'end_time': 31270, 'start_time': 31230, 'text': '灵'}, {'confidence': 0, 'end_time': -1, 'start_time': -1, 'text': ' '}, {'confidence': 0, 'end_time': 31590, 'start_time': 31390, 'text': 'O1'}], 'keywords': [], 'en': 'Hurry and let Kling O1'}, {'start': 31790, 'end': 33110, 'text': '成为你视频创作的', 'words': [{'confidence': 0, 'end_time': 31950, 'start_time': 31790, 'text': '成'}, {'confidence': 0, 'end_time': 32070, 'start_time': 31950, 'text': '为'}, {'confidence': 0, 'end_time': 32230, 'start_time': 32070, 'text': '你'}, {'confidence': 0, 'end_time': 32390, 'start_time': 32230, 'text': '视'}, {'confidence': 0, 'end_time': 32510, 'start_time': 32390, 'text': '频'}, {'confidence': 0, 'end_time': 32710, 'start_time': 32550, 'text': '创'}, {'confidence': 0, 'end_time': 32830, 'start_time': 32710, 'text': '作'}, {'confidence': 0, 'end_time': 33110, 'start_time': 32830, 'text': '的'}], 'keywords': [], 'en': 'Become your video creation'}, {'start': 33150, 'end': 34190, 'text': '得力助手吧', 'words': [{'confidence': 0, 'end_time': 33350, 'start_time': 33150, 'text': '得'}, {'confidence': 0, 'end_time': 33510, 'start_time': 33350, 'text': '力'}, {'confidence': 0, 'end_time': 33750, 'start_time': 33550, 'text': '助'}, {'confidence': 0, 'end_time': 33910, 'start_time': 33750, 'text': '手'}, {'confidence': 0, 'end_time': 34190, 'start_time': 33910, 'text': '吧'}], 'keywords': ['助手'], 'en': 'Competent assistant'}]
# print(asr_e8d06597e17c46a8a6d9b5c60a757c26(segemnts, "123"))

def apply_template(segments, draft_id):
    return asr_e8d06597e17c46a8a6d9b5c60a757c26(segments, draft_id)

