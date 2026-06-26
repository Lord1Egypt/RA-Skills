---
name: grounding
description: Use GLM-4.7V's multimodal grounding capability to detect and locate objects/text in images. Activate when user asks to find, locate, detect, or ground specific objects, text, UI elements, or regions in an image. Also triggers on phrases like "找到xxx的位置", "框出xxx", "定位xxx", "grounding", "bounding box", "坐标框".
---

# Grounding - 多模态目标定位

利用 GLM-4.7V 的 grounding 能力，在图片中定位目标对象或文字，输出带标注框的结果图。

## 工作流程

```
用户输入（图片 + prompt）
        │
        ▼
  HttpInterface() → 调用模型 API → 得到 response 文本
        │
        ▼
  parse_bboxes_from_response() → 从回复中解析出坐标框列表
        │
        ▼
  visualize_boxes(renormalize=True) → 反归一化 + 画框 → 保存结果图
```

## Step 1: 调用模型获取坐标

使用 `HttpInterface` 调用模型 API：

```python
import os
os.environ['NO_PROXY'] = '<model-host>'  # 跳过代理
os.environ['no_proxy'] = '<model-host>'

from interface_http import HttpInterface

url = 'http://<host>:<port>/v1/chat/completions'
prompt = '''请在这张图中找到所有"{target}"，并以 [xmin, ymin, xmax, ymax] 格式输出每个目标的边界框坐标，坐标值为 0-1000 的归一化整数。每个目标一行，格式如下：
目标名称: [xmin, ymin, xmax, ymax]'''

response = HttpInterface(url, prompt, images=[image_path], no_think=True)
# 返回: "目标名称: [xmin, ymin, xmax, ymax]"
```

**注意：** 调用前需设置 `NO_PROXY` 环境变量跳过代理，否则内网请求会被代理拦截。

## Step 2: 解析坐标框

```python
from utils_boxes import parse_bboxes_from_response

boxes = parse_bboxes_from_response(response)
# 返回: [[x1, y1, x2, y2], ...]  (0-1000 归一化)
```

`parse_bboxes_from_response` 会自动：
- 从回复尾部向前检查截断，拓展 context window
- 遍历所有括号风格（`[]`, `{}`, `()`, `<>`, `<bbox>`）提取坐标
- 扁平化嵌套列表，返回一维 box 列表

## Step 3: 画框可视化

```python
from utils_boxes import visualize_boxes

visualize_boxes(
    img_path=image_path,
    boxes=boxes,                    # parse_bboxes_from_response 的输出
    labels=['label1', 'label2'],    # 每个框的标签
    renormalize=True,               # 自动将 0-1000 归一化转为像素坐标
    save_path='output.jpg',
    colors=['red', 'blue'],         # 可选
    thickness=[2, 3],               # 可选
)
```

`renormalize=True` 时，内部自动调用 `reverse_normalize_box`：`pixel = coord * img_dimension / 1000`

## 完整示例

```python
import os
os.environ['NO_PROXY'] = '172.20.112.202'
os.environ['no_proxy'] = '172.20.112.202'

from interface_http import HttpInterface
from utils_boxes import parse_bboxes_from_response, visualize_boxes

url = 'http://172.20.112.202:5002/v1/chat/completions'
img = '/path/to/image.jpg'

# 1. 调用模型
response = HttpInterface(
    url,
    '请在这张图中找到"红色圣诞帽"，以 [xmin, ymin, xmax, ymax] 格式输出坐标（0-1000归一化）',
    images=[img],
    no_think=True,
)

# 2. 解析坐标
boxes = parse_bboxes_from_response(response)

# 3. 画框
visualize_boxes(img_path=img, boxes=boxes, labels=['圣诞帽'], renormalize=True, save_path='out.jpg')
```

## 工具函数速查

| 函数 | 作用 |
|------|------|
| `HttpInterface(url, prompt, images, no_think)` | 调用模型 API，返回文本回复 |
| `parse_bboxes_from_response(text)` | 从模型回复中提取所有坐标框列表 |
| `find_boxes_all(text, flat=True)` | 提取文本中所有括号风格的坐标框 |
| `reverse_normalize_box(box, w, h)` | 0-1000 归一化 → 像素坐标 |
| `visualize_boxes(..., renormalize=True)` | 画框 + 自动反归一化 |

## 注意事项

- 模型 API 地址配置在 `/root/.openclaw/agents/main/agent/models.json`
- 调用内网模型时必须设置 `NO_PROXY` 环境变量
- `no_think=True` 可关闭模型思考模式，加快响应
