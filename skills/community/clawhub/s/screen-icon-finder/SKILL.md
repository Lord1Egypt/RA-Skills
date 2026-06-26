---
name: screen-icon-finder
description: |
  在屏幕截图或图片中，通过 OpenCV 模板匹配查找指定图标/图片的位置，支持多尺度匹配去重。
  用于：(1) 用户发来一个小图，让你在屏幕上找；(2) 查找所有匹配图标并标号；(3) 点击找到的图标。
  关键词：找图标、定位图标、模板匹配、找按钮、点击图标、图片搜索。
---

# Screen Icon Finder

通过 OpenCV 模板匹配，在屏幕截图或任意图片中精确查找目标图标位置。

## 核心脚本

### find_icon.py — 查找 + 标记

```python
import cv2
import numpy as np
import sys

def find_icon(small_path, big_path=None, threshold=0.75, scale_min=0.3, scale_max=2.0, scale_steps=35):
    """
    在大图中查找小图，支持多尺度匹配和 NMS 去重。
    
    small_path: 小图路径（要找的目标图标，用户发来的图片）
    big_path: 大图路径（屏幕截图），默认截取全屏
    threshold: 匹配阈值，默认 0.75
    返回: [(x, y, score, center_x, center_y, scale, w, h), ...]
    """
    import pyautogui
    
    if big_path is None:
        img = pyautogui.screenshot()
        img.save('_temp_screen.png')
        big_path = '_temp_screen.png'
    
    small = cv2.imread(small_path)
    big = cv2.imread(big_path)
    
    gray_big = cv2.cvtColor(big, cv2.COLOR_BGR2GRAY)
    gray_small = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    
    # 找最佳缩放
    best_score = 0
    best_scale = 1
    best_size = None
    
    for scale in np.linspace(scale_min, scale_max, scale_steps):
        w = int(small.shape[1] * scale)
        h = int(small.shape[0] * scale)
        if w > big.shape[1] or h > big.shape[0] or w < 5 or h < 5:
            continue
        resized = cv2.resize(gray_small, (w, h))
        result = cv2.matchTemplate(gray_big, resized, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        if max_val > best_score:
            best_score = max_val
            best_scale = scale
            best_size = (w, h)
    
    # 找所有匹配
    resized = cv2.resize(gray_small, best_size)
    result = cv2.matchTemplate(gray_big, resized, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    matches = list(zip(*locations[::-1]))
    
    # NMS 去重
    scored = [(x, y, result[y, x]) for x, y in matches]
    scored.sort(key=lambda t: t[2], reverse=True)
    
    filtered = []
    min_dist = max(best_size) * 0.5
    
    for x, y, s in scored:
        too_close = False
        for fx, fy, _ in filtered:
            if abs(x - fx) < min_dist and abs(y - fy) < min_dist:
                too_close = True
                break
        if not too_close:
            filtered.append((x, y, s))
    
    return [(x, y, s, x+best_size[0]//2, y+best_size[1]//2, best_scale, best_size[0], best_size[1]) 
            for x, y, s in filtered]


def mark_icons(matches, big_path, output_path, color=(0, 255, 0)):
    """在大图上标记所有匹配位置，带序号"""
    img = cv2.imread(big_path)
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    for i, (x, y, score, cx, cy, scale, w, h) in enumerate(matches):
        cv2.rectangle(img, (x, y), (x+w, y+h), color, 3)
        cv2.putText(img, f'{i+1}', (x + w//2 - 10, y - 10), font, 1.5, (0, 0, 255), 3)
        cv2.putText(img, f'{score:.2f}', (x + w//2 - 20, y + h + 25), font, 0.6, color, 1)
    
    cv2.imwrite(output_path, img)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python find_icon.py <小图路径> [大图路径]')
        sys.exit(1)
    
    small = sys.argv[1]
    big = sys.argv[2] if len(sys.argv) > 2 else None
    
    results = find_icon(small, big)
    
    print(f'找到 {len(results)} 个匹配:')
    for i, r in enumerate(results):
        print(f'  #{i+1}: 位置({r[0]}, {r[1]}), 中心({r[3]}, {r[4]}), 缩放={r[5]:.2f}, 匹配度={r[2]:.4f}')
    
    if results:
        # 默认标记第一个
        big_path = '_temp_screen.png' if big is None else big
        mark_icons(results, big_path, '_result.png')
        print(f'已保存标记图: _result.png')
```

## 使用方式

### 1. 用户发图查找

用户发来一个小图（图标截图），在全屏截图中查找：
```
用户：找到这个图标，在屏幕上标记出来
AI：调用 find_icon.py，传入小图路径，标记结果发回
```

### 2. 标记多个匹配

传入阈值，默认 0.75。匹配度高（>0.9）说明是目标图标，低的话可能是相似图。

### 3. 点击图标

找到后用 `pyautogui.click(cx, cy)` 点击中心坐标。

## 注意

- 微信截图和屏幕截图分辨率可能不同，多尺度匹配是关键
- 缩放范围 0.3~2.0，步长 35，可覆盖大多数场景
- NMS 去重避免重复标记同一图标
