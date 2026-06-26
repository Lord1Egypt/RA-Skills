# 视频译制 ProcessMedia 请求示例

> 本文件收录 MPS `ProcessMedia` 接口在**视频配音译制**场景下的**请求 JSON 示例**。
> 字段释义、关键规则、ExtendedParameter 完整结构 → 见 [`mps_video_dubbing.md`](./mps_video_dubbing.md)（特别是「参数说明」「强制规则」两节）。

---

## 公共模板

5 个示例共用以下 `InputInfo` / `OutputStorage` / 接口元字段，下方各示例**仅展示 `ExtendedParameter` 差异部分**。

```json
{
  "regionId": 1,
  "serviceType": "mps",
  "cmd": "ProcessMedia",
  "data": {
    "Version": "2019-06-12",
    "InputInfo": {
      "Type": "COS",
      "CosInputInfo": {
        "Bucket": "mps-ollie-test-1308104797",
        "Region": "ap-guangzhou",
        "Object": "input/17_1773808857717.MP4"
      }
    },
    "OutputStorage": {
      "Type": "COS",
      "CosOutputStorage": {
        "Bucket": "mps-ollie-test-1308104797",
        "Region": "ap-guangzhou"
      }
    },
    "AiAnalysisTask": {
      "Definition": 25,
      "ExtendedParameter": "<见下方各示例>"
    }
  }
}
```

---

## 1. ASR + 不压制字幕

无硬字幕视频，ASR 识别 + 翻译，**不**压字幕，仅替换配音。

```text
ExtendedParameter:
  "{\"delogo\":{\"cluster_id\":\"gpu_zhiyan\",\"CustomerAppId\":\"audio_clone_asr\",\"subtitle_param\":{\"translate_src_language\":\"zh\",\"translate_dst_language\":\"en\",\"use_draw\":false,\"font_type\":\"auto\"}}}"
```

差异点：`CustomerAppId=audio_clone_asr`，`use_draw=false`。

---

## 2. ASR + 压制字幕

无硬字幕视频，ASR 识别 + 翻译，并把翻译字幕**压制**到画面，同时替换配音。

```text
ExtendedParameter:
  "{\"delogo\":{\"cluster_id\":\"gpu_zhiyan\",\"CustomerAppId\":\"audio_clone_asr\",\"subtitle_param\":{\"translate_src_language\":\"zh\",\"translate_dst_language\":\"en\",\"use_draw\":true,\"font_type\":\"auto\"}}}"
```

差异点：`use_draw=true`。

---

## 3. OCR + 预设字幕区域（推荐，90% 场景）

画面有硬字幕，OCR 识别 + 擦除 + 翻译 + 压新字幕 + AI 配音。**不传** `als_filter`，由后端使用默认区域（画面中部靠下）。

```text
ExtendedParameter:
  "{\"delogo\":{\"cluster_id\":\"gpu_zhiyan\",\"CustomerAppId\":\"audio_clone_ocr\",\"subtitle_param\":{\"translate_src_language\":\"zh\",\"translate_dst_language\":\"en\",\"use_draw\":true,\"font_type\":\"auto\"}}}"
```

差异点：`CustomerAppId=audio_clone_ocr`，**无 `als_filter`**。

---

## 4. OCR + 自定义字幕区域（底部）

画面有硬字幕但位置非中下部，需自定义识别/擦除像素矩形区域。

```text
ExtendedParameter（转义形式）:
  "{\"delogo\":{\"cluster_id\":\"gpu_zhiyan\",\"CustomerAppId\":\"audio_clone_ocr\",\"subtitle_param\":{\"translate_src_language\":\"zh\",\"translate_dst_language\":\"en\",\"use_draw\":true,\"font_type\":\"auto\"},\"als_filter\":{\"active_areas\":[{\"type\":2,\"lt_x\":53,\"lt_y\":741,\"rb_x\":953,\"rb_y\":922}]}}}"
```

解包形式：

```json
{
  "delogo": {
    "cluster_id": "gpu_zhiyan",
    "CustomerAppId": "audio_clone_ocr",
    "subtitle_param": {
      "translate_src_language": "zh",
      "translate_dst_language": "en",
      "use_draw": true,
      "font_type": "auto"
    },
    "als_filter": {
      "active_areas": [
        { "type": 2, "lt_x": 53, "lt_y": 741, "rb_x": 953, "rb_y": 922 }
      ]
    }
  }
}
```

差异点：新增 `als_filter.active_areas`，矩形像素坐标 `(53,741)→(953,922)`。

---

## 5. OCR + 自定义字幕区域（中上部）

同 #4，换一组坐标（如顶部横幅字幕）。

```text
ExtendedParameter:
  "{\"delogo\":{\"cluster_id\":\"gpu_zhiyan\",\"CustomerAppId\":\"audio_clone_ocr\",\"subtitle_param\":{\"translate_src_language\":\"zh\",\"translate_dst_language\":\"en\",\"use_draw\":true,\"font_type\":\"auto\"},\"als_filter\":{\"active_areas\":[{\"type\":2,\"lt_x\":200,\"lt_y\":400,\"rb_x\":900,\"rb_y\":700}]}}}"
```

差异点：坐标改为 `(200,400)→(900,700)`。

---

> 字段释义、关键规则（cluster_id / use_draw / font_type / als_filter / preview_size 等）→ 见 [`mps_video_dubbing.md`](./mps_video_dubbing.md)（特别是「强制规则」一节）。
