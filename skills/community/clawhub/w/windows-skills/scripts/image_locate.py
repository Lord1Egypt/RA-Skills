"""图像定位模块 - 在屏幕上查找图片位置"""
import cv2
import numpy as np
import pyautogui
import os


def locate_on_screen(
    target_image: str,
    confidence: float = 0.8,
    grayscale: bool = True
) -> tuple | None:
    """在屏幕上查找图片位置
    
    Args:
        target_image: 要查找的图片路径
        confidence: 匹配置信度 (0-1)
        grayscale: 是否使用灰度匹配
        
    Returns:
        (x, y) 中心坐标，未找到返回 None
    """
    if not os.path.exists(target_image):
        raise FileNotFoundError(f"图片不存在: {target_image}")
    
    # 截图
    screenshot = pyautogui.screenshot()
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # 加载目标图片
    target = cv2.imread(target_image)
    if target is None:
        raise ValueError(f"无法读取目标图片: {target_image}")
    
    # 转换为灰度
    if grayscale:
        screenshot_gray = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)
        target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    else:
        screenshot_gray = screenshot_cv
        target_gray = target
    
    # 模板匹配
    result = cv2.matchTemplate(screenshot_gray, target_gray, cv2.TM_CCOEFF_NORMED)
    
    # 找最佳匹配
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    if max_val >= confidence:
        # 计算中心点
        h, w = target_gray.shape[:2]
        x = max_loc[0] + w // 2
        y = max_loc[1] + h // 2
        return (x, y, max_val)
    
    return None


def locate_all(
    target_image: str,
    confidence: float = 0.8,
    grayscale: bool = True
) -> list:
    """查找所有匹配位置
    
    Args:
        target_image: 要查找的图片路径
        confidence: 匹配置信度
        grayscale: 是否使用灰度匹配
        
    Returns:
        [(x, y, confidence), ...] 位置列表
    """
    if not os.path.exists(target_image):
        raise FileNotFoundError(f"图片不存在: {target_image}")
    
    # 截图
    screenshot = pyautogui.screenshot()
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # 加载目标图片
    target = cv2.imread(target_image)
    if target is None:
        raise ValueError(f"无法读取目标图片: {target_image}")
    
    # 转换为灰度
    if grayscale:
        screenshot_gray = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)
        target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    else:
        screenshot_gray = screenshot_cv
        target_gray = target
    
    # 模板匹配
    result = cv2.matchTemplate(screenshot_gray, target_gray, cv2.TM_CCOEFF_NORMED)
    
    # 找所有匹配位置
    locations = np.where(result >= confidence)
    
    h, w = target_gray.shape[:2]
    positions = []
    
    for pt in zip(*locations[::-1]):
        x = pt[0] + w // 2
        y = pt[1] + h // 2
        conf = result[pt[1], pt[0]]
        positions.append((x, y, conf))
    
    return positions


def wait_and_locate(
    target_image: str,
    timeout: float = 10,
    confidence: float = 0.8,
    poll_interval: float = 0.5
) -> tuple | None:
    """等待并查找图片（轮询）
    
    Args:
        target_image: 要查找的图片路径
        timeout: 超时时间（秒）
        confidence: 匹配置信度
        poll_interval: 轮询间隔
        
    Returns:
        (x, y) 中心坐标，超时返回 None
    """
    import time
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        pos = locate_on_screen(target_image, confidence)
        if pos:
            return pos
        time.sleep(poll_interval)
    
    return None


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python image_locate.py <目标图片> [置信度]")
        sys.exit(1)
    
    target = sys.argv[1]
    conf = float(sys.argv[2]) if len(sys.argv) > 2 else 0.8
    
    print(f"正在查找: {target}")
    
    pos = locate_on_screen(target, conf)
    
    if pos:
        x, y, c = pos
        print(f"找到! 位置: ({x}, {y}), 置信度: {c:.2f}")
    else:
        print("未找到")
