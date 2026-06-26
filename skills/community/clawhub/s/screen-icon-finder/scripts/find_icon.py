import cv2
import numpy as np
import pyautogui
import sys
import os


def screenshot(path='_temp_screen.png'):
    """截取全屏并保存"""
    img = pyautogui.screenshot()
    img.save(path)
    return path


def find_icon(small_path, big_path=None, threshold=0.75, scale_min=0.3, scale_max=2.0, scale_steps=35):
    """
    在大图中查找小图，支持多尺度匹配和 NMS 去重。
    
    small_path: 小图路径（要找的目标图标）
    big_path: 大图路径（屏幕截图），默认截取全屏
    threshold: 匹配阈值，默认 0.75
    返回: [(x, y, score, center_x, center_y, scale, w, h), ...]
    """
    if big_path is None:
        big_path = screenshot()

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

    return [(x, y, s, x + best_size[0] // 2, y + best_size[1] // 2, best_scale, best_size[0], best_size[1])
            for x, y, s in filtered]


def mark_icon(result, big_path, output_path, color=(0, 255, 0)):
    """在大图上标记单个匹配位置"""
    img = cv2.imread(big_path)
    font = cv2.FONT_HERSHEY_SIMPLEX
    x, y, score, cx, cy, scale, w, h = result
    
    cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
    cv2.putText(img, f'Score:{score:.2f}', (x + w // 2 - 30, y - 10), font, 0.8, color, 2)
    
    cv2.imwrite(output_path, img)


def mark_icons(results, big_path, output_path, color=(0, 255, 0)):
    """在大图上标记所有匹配位置，带序号"""
    img = cv2.imread(big_path)
    font = cv2.FONT_HERSHEY_SIMPLEX

    for i, r in enumerate(results):
        x, y, score, cx, cy, scale, w, h = r
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
        cv2.putText(img, f'{i+1}', (x + w // 2 - 10, y - 10), font, 1.5, (0, 0, 255), 3)
        cv2.putText(img, f'{score:.2f}', (x + w // 2 - 20, y + h + 25), font, 0.6, color, 1)

    cv2.imwrite(output_path, img)


def click(result):
    """点击匹配位置的中心"""
    _, _, _, cx, cy, _, _, _ = result
    pyautogui.click(cx, cy)
    return cx, cy


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python find_icon.py <小图路径> [大图路径] [阈值]')
        print('  小图路径: 要查找的图标图片路径')
        print('  大图路径: 可选，屏幕截图路径，默认截取全屏')
        print('  阈值: 可选，匹配阈值默认 0.75')
        sys.exit(1)

    small = sys.argv[1]
    big = sys.argv[2] if len(sys.argv) > 2 else None
    threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 0.75

    results = find_icon(small, big, threshold=threshold)

    print(f'找到 {len(results)} 个匹配:')
    for i, r in enumerate(results):
        print(f'  #{i+1}: 位置({r[0]}, {r[1]}), 中心({r[3]}, {r[4]}), 缩放={r[5]:.2f}, 匹配度={r[2]:.4f}')

    if results:
        big_path = '_temp_screen.png' if big is None else big
        mark_icons(results, big_path, '_result.png')
        print(f'已保存标记图: _result.png')
