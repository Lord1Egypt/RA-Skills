# 使用示例

## 基本截图示例

### 示例1: 快速全屏截图
```bash
# 使用快速截图工具
python scripts/quick_capture.py

# 使用完整截图工具
python scripts/screenshot.py --output my_screen.png
```

### 示例2: 区域截图
```bash
# 截取屏幕左上角500x500区域
python scripts/screenshot.py --region "0,0,500,500" --output top_left.png

# 截取屏幕中心区域
python scripts/screenshot.py --region "710,290,1210,790" --output center.png
```

### 示例3: 带时间戳的截图
```bash
# 自动添加时间戳
python scripts/quick_capture.py -o screenshot_$(date +%Y%m%d_%H%M%S).png
```

## OCR文字识别示例

### 示例4: 提取屏幕文字
```bash
# 提取全屏文字
python scripts/ocr_screenshot.py --text-output screen_text.txt

# 提取特定区域文字
python scripts/ocr_screenshot.py --region "100,100,800,600" --text-output region_text.txt

# 使用中文识别
python scripts/ocr_screenshot.py --lang chi_sim --text-output chinese_text.txt
```

### 示例5: 批量处理截图
```bash
# 创建批处理脚本 process_screenshots.bat (Windows)
@echo off
python scripts/ocr_screenshot.py --text-output screenshot1.txt
python scripts/ocr_screenshot.py --region "0,0,500,500" --text-output region1.txt
python scripts/ocr_screenshot.py --lang eng+chi_sim --text-output bilingual.txt
```

## 屏幕分析示例

### 示例6: 查找特定文字
```bash
# 查找屏幕上的"错误"文字
python scripts/analyze_screen.py --task find_text --text "错误" --output error_positions.json

# 查找多个关键词
python scripts/analyze_screen.py --task find_text --text "成功|完成|OK" --output results.json
```

### 示例7: 颜色检测
```bash
# 查找红色元素 (#FF0000)
python scripts/analyze_screen.py --task find_color --color "#FF0000" --output red_elements.json

# 查找蓝色元素，增加容差
python scripts/analyze_screen.py --task find_color --color "#0000FF" --tolerance 20 --output blue_elements.json
```

### 示例8: 屏幕边缘检测
```bash
# 检测屏幕边缘
python scripts/analyze_screen.py --task detect_edges --output edges.png

# 分析边缘密度
python scripts/analyze_screen.py --task detect_edges --output analysis.json
```

## 高级使用示例

### 示例9: 定时截图监控
```python
# 创建定时截图脚本 monitor.py
import time
from datetime import datetime
from PIL import ImageGrab

interval = 5  # 秒
duration = 60  # 秒

for i in range(duration // interval):
    # 截图
    screenshot = ImageGrab.grab()
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"monitor_{timestamp}.png"
    
    # 保存
    screenshot.save(filename)
    print(f"已保存: {filename}")
    
    # 等待
    time.sleep(interval)
```

### 示例10: 变化检测
```python
# 创建变化检测脚本 change_detector.py
import cv2
import numpy as np
from PIL import ImageGrab
import time

prev_screen = None
threshold = 0.01  # 1%的变化阈值

while True:
    current_screen = ImageGrab.grab()
    
    if prev_screen is not None:
        # 转换为灰度图
        prev_gray = cv2.cvtColor(np.array(prev_screen), cv2.COLOR_RGB2GRAY)
        curr_gray = cv2.cvtColor(np.array(current_screen), cv2.COLOR_RGB2GRAY)
        
        # 计算差异
        diff = cv2.absdiff(prev_gray, curr_gray)
        change_percentage = np.sum(diff > 25) / diff.size
        
        if change_percentage > threshold:
            print(f"检测到变化: {change_percentage*100:.2f}%")
            # 保存变化截图
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            current_screen.save(f"change_{timestamp}.png")
    
    prev_screen = current_screen
    time.sleep(1)
```

### 示例11: 自动化报告生成
```python
# 创建报告生成脚本 report_generator.py
import json
from datetime import datetime
from PIL import ImageGrab
import pyautogui

def generate_screen_report():
    """生成屏幕报告"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "screen_info": {},
        "screenshot": None
    }
    
    # 获取屏幕信息
    screen_width, screen_height = pyautogui.size()
    mouse_x, mouse_y = pyautogui.position()
    
    report["screen_info"] = {
        "resolution": f"{screen_width}x{screen_height}",
        "mouse_position": [mouse_x, mouse_y]
    }
    
    # 截图
    screenshot = ImageGrab.grab()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_file = f"report_screenshot_{timestamp}.png"
    screenshot.save(screenshot_file)
    
    report["screenshot"] = screenshot_file
    report["screenshot_size"] = f"{screenshot.size[0]}x{screenshot.size[1]}"
    
    # 保存报告
    report_file = f"screen_report_{timestamp}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"报告已生成: {report_file}")
    return report_file

if __name__ == "__main__":
    generate_screen_report()
```

## 集成示例

### 示例12: 与CodeBuddy集成
```python
# 在CodeBuddy技能中集成屏幕截图功能
def capture_and_analyze():
    """捕获并分析屏幕"""
    from scripts.screenshot import capture_full_screen
    from scripts.ocr_screenshot import capture_and_ocr
    from scripts.analyze_screen import find_text_on_screen
    
    # 1. 截图
    screenshot_file = "analysis_screenshot.png"
    capture_full_screen(screenshot_file)
    
    # 2. OCR识别
    text_file = "analysis_text.txt"
    capture_and_ocr(output_image=screenshot_file, output_text=text_file)
    
    # 3. 分析特定内容
    search_results = find_text_on_screen("错误", lang='chi_sim')
    
    return {
        "screenshot": screenshot_file,
        "text": text_file,
        "errors_found": len(search_results) if search_results else 0
    }
```

### 示例13: 错误监控系统
```python
# 错误监控脚本 error_monitor.py
import time
import json
from datetime import datetime
from scripts.analyze_screen import find_text_on_screen

def monitor_errors(interval=30, duration=3600):
    """监控屏幕错误"""
    error_log = []
    start_time = time.time()
    
    while time.time() - start_time < duration:
        # 搜索错误关键词
        errors = find_text_on_screen("错误|失败|异常|Error|Failed|Exception")
        
        if errors:
            error_entry = {
                "timestamp": datetime.now().isoformat(),
                "errors": errors,
                "count": len(errors)
            }
            error_log.append(error_entry)
            
            # 保存错误日志
            with open("error_log.json", "w", encoding="utf-8") as f:
                json.dump(error_log, f, indent=2, ensure_ascii=False)
            
            print(f"发现 {len(errors)} 个错误")
        
        time.sleep(interval)
    
    return error_log
```

## 故障排除示例

### 示例14: 诊断脚本
```bash
# 运行诊断测试
python scripts/test_screenshot.py

# 检查依赖
python -c "from PIL import ImageGrab; import pyautogui; print('依赖检查通过')"

# 测试OCR
python -c "import pytesseract; print('Tesseract版本:', pytesseract.get_tesseract_version())"
```

这些示例展示了Screen Capture Hub技能的各种用法，您可以根据需要修改和扩展。