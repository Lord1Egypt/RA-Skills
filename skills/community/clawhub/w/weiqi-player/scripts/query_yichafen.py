#!/usr/bin/env python3
"""
易查分平台围棋业余段位查询 - 浏览器会话复用优化版
使用 Playwright 持久化上下文实现会话复用

优化效果：
- 单次查询：~8-10秒（启动+关闭浏览器）
- 批量查询：~3-5秒/人（复用会话，一次启动）

依赖安装：
    pip install playwright
    playwright install chromium

【单个查询】
    python3 query_yichafen.py 张三
    python3 query_yichafen.py 李四

【批量查询 - 推荐】
    python3 query_yichafen.py --batch 张三 李四 王五
    python3 query_yichafen.py --batch 赵六 孙七
"""

import sys
import json
import time
import os
from pathlib import Path
from contextlib import contextmanager
from collections import OrderedDict

# 尝试导入 playwright
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ 请先安装 Playwright:")
    print("   pip install playwright")
    print("   playwright install chromium")
    sys.exit(1)

# 配置
BASE_URL = "https://yeyuweiqi.yichafen.com/qz/s9W2g0zKmt"
USER_DATA_DIR = Path("/tmp/yichafen_browser_data")
SESSION_TIMEOUT = 300  # 会话有效期5分钟
STATE_FILE = Path("/tmp/yichafen_state.json")


# ===== 性能计时工具 =====
class PerformanceTimer:
    """性能计时器 - 追踪每个步骤的执行耗时"""
    def __init__(self):
        self.timings = OrderedDict()
        self.start_time = None
    
    def start(self):
        """开始总计时"""
        self.start_time = time.time()
        return self
    
    @contextmanager
    def step(self, name):
        """上下文管理器 - 计时单个步骤"""
        step_start = time.time()
        try:
            yield self
        finally:
            elapsed = time.time() - step_start
            self.timings[name] = elapsed
    
    def get_total(self):
        """获取总耗时"""
        if self.start_time:
            return time.time() - self.start_time
        return 0
    
    def format_report(self):
        """格式化计时报告"""
        lines = []
        lines.append("\n" + "="*50)
        lines.append("⏱️  性能计时报告（易查分查询）")
        lines.append("="*50)
        
        total_step_time = 0
        for name, elapsed in self.timings.items():
            total_step_time += elapsed
            lines.append(f"  {name:20s} : {elapsed:>8.3f}s")
        
        lines.append("-"*50)
        lines.append(f"  {'步骤累计':20s} : {total_step_time:>8.3f}s")
        lines.append(f"  {'总耗时':20s} : {self.get_total():>8.3f}s")
        lines.append("="*50)
        return "\n".join(lines)


# 全局计时器实例
timer = PerformanceTimer()


def is_browser_ready():
    """检查浏览器是否已准备好（页面已加载）"""
    if not STATE_FILE.exists():
        return False
    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
        # 检查是否在有效期内
        if time.time() - state.get('timestamp', 0) > SESSION_TIMEOUT:
            return False
        return state.get('ready', False)
    except:
        return False


def save_browser_state(ready=True):
    """保存浏览器状态"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump({
            'ready': ready,
            'timestamp': time.time()
        }, f)


def query_player_fast(name, headless=True):
    """
    快速查询 - 单次查询优化版（精简流程）
    
    Args:
        name: 选手姓名
        headless: 是否无头模式
    """
    global timer
    timer.start()
    
    with sync_playwright() as p:
        with timer.step("启动浏览器"):
            browser = p.chromium.launch(
                headless=headless,
                args=['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
            )
        
        page = browser.new_page()
        
        try:
            # 合并步骤：直接加载页面并等待输入框
            with timer.step("加载并查询"):
                page.goto(BASE_URL, wait_until='networkidle')
                # 使用更精确的选择器
                input_box = page.locator('input[name="s_xingming"]').first
                if input_box.count() == 0:
                    input_box = page.locator('input[type="text"]').first
                input_box.fill(name)
                time.sleep(0.3)
                # 点击查询按钮（而不是按Enter）
                button = page.locator('#yiDunSubmitBtn').first
                if button.count() > 0:
                    button.click()
                else:
                    input_box.press('Enter')
                # 等待结果出现（最多4秒）
                for _ in range(20):  # 20 * 0.2s = 4s max
                    time.sleep(0.2)
                    text = page.locator('body').inner_text()
                    # 检查是否有结果数据（姓名出现在页面中且包含段位信息）
                    if name in text and ('段' in text or '暂无数据' in text or '未找到' in text):
                        break
            
            with timer.step("提取数据"):
                text_content = page.locator('body').inner_text()
            
            return text_content
            
        finally:
            with timer.step("关闭浏览器"):
                browser.close()


def query_player(name, headless=True):
    """
    查询选手信息（含性能计时）- 保持兼容性的原始版本
    
    Args:
        name: 选手姓名
        headless: 是否无头模式（False可看到浏览器界面，用于调试）
    """
    # 默认使用快速版本
    return query_player_fast(name, headless)


def parse_player_info(text):
    """解析选手信息 - 改进版"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    info = {
        '姓名': None,
        '段位': None,
        '等级分': None,
        '总排名': None,
        '省区排名': None,
        '本市排名': None,
        '省区': None,
        '城市': None,
        '性别': None,
        '出生': None,
        '备注': None,
    }
    
    # 简单解析逻辑
    for i, line in enumerate(lines):
        # 段位（简单格式如 "6段"，不含其他文字）
        if line.endswith('段') and len(line) <= 3 and '晋升' not in line and '备注' not in line:
            info['段位'] = line
        
        # 等级分（通常是一个四位数左右的数字）
        if line.replace('.', '').isdigit():
            val = float(line)
            if 1000 < val < 3000:
                info['等级分'] = line
        
        # 总排名（格式: "总排名\t2559" 或两行格式）
        if line.startswith('总排名'):
            parts = line.split('\t')
            if len(parts) > 1:
                info['总排名'] = parts[1].strip()
            elif i + 1 < len(lines):
                next_line = lines[i + 1].replace('\t', '').strip()
                if next_line.isdigit():
                    info['总排名'] = next_line
        
        # 省区排名
        if line.startswith('省区排名'):
            parts = line.split('\t')
            if len(parts) > 1:
                info['省区排名'] = parts[1].strip()
            elif i + 1 < len(lines):
                info['省区排名'] = lines[i + 1].replace('\t', '').strip()
        
        # 本市排名
        if line.startswith('本市排名'):
            parts = line.split('\t')
            if len(parts) > 1:
                info['本市排名'] = parts[1].strip()
            elif i + 1 < len(lines):
                info['本市排名'] = lines[i + 1].replace('\t', '').strip()
        
        # 省区
        if line.startswith('省区') and not line.startswith('省区排名'):
            parts = line.split('\t')
            if len(parts) > 1:
                info['省区'] = parts[1].strip()
            elif i + 1 < len(lines):
                info['省区'] = lines[i + 1]
        
        # 城市
        if line.startswith('城市'):
            parts = line.split('\t')
            if len(parts) > 1:
                info['城市'] = parts[1].strip()
            elif i + 1 < len(lines):
                info['城市'] = lines[i + 1]
        
        # 性别
        if line.startswith('性别'):
            parts = line.split('\t')
            if len(parts) > 1:
                info['性别'] = parts[1].strip()
            elif i + 1 < len(lines):
                info['性别'] = lines[i + 1]
        
        # 出生
        if line.startswith('出生'):
            parts = line.split('\t')
            if len(parts) > 1:
                info['出生'] = parts[1].strip()
            elif i + 1 < len(lines):
                info['出生'] = lines[i + 1]
        
        # 备注（以"备注"开头或包含晋升信息）
        if line.startswith('备注\t') or (len(line) > 10 and '晋升' in line and '杯' in line):
            info['备注'] = line.replace('备注\t', '')
    
    return info


def format_output(name, info, elapsed):
    """格式化输出结果 - 单行 Markdown 格式"""
    print(f"\n📋 **{name}** - 易查分业余段位查询\n")
    
    parts = []
    if info.get('段位'):
        parts.append(f"段位: {info['段位']}")
    if info.get('等级分'):
        parts.append(f"等级分: {info['等级分']}")
    if info.get('总排名'):
        parts.append(f"总排名: {info['总排名']}")
    if info.get('省区'):
        parts.append(f"地区: {info['省区']} {info.get('城市', '')}".strip())
    if info.get('性别'):
        parts.append(f"性别: {info['性别']}")
    if info.get('出生'):
        parts.append(f"出生: {info['出生']}")
    
    if parts:
        print(" | ".join(parts))
    else:
        print("⚠️ 未查询到业余段位信息")
    
    if info.get('备注'):
        print(f"\n备注: {info['备注']}")
    
    print(f"\n⏱️ 查询耗时: {elapsed:.1f}秒\n")
    
    # 输出详细性能报告
    print(timer.format_report())


def query_single_player(page, name, timer):
    """
    在已打开的页面中查询单个选手（用于批量查询）
    
    Args:
        page: Playwright page 对象
        name: 选手姓名
        timer: 性能计时器
    
    Returns:
        dict: 选手信息字典
    """
    try:
        # 重新导航到页面
        with timer.step(f"[{name}] 页面导航"):
            page.goto(BASE_URL, wait_until='domcontentloaded')
            time.sleep(0.8)
        
        # 填写表单
        with timer.step(f"[{name}] 填写表单"):
            input_selector = 'input[placeholder*="姓名"], input[type="text"]'
            input_box = page.locator(input_selector).first
            input_box.fill("")
            input_box.fill(name)
            time.sleep(0.2)
        
        # 点击查询
        with timer.step(f"[{name}] 点击查询"):
            button_selector = 'button:has-text("查询"), .query-btn, [class*="query"]'
            button = page.locator(button_selector).first
            if button.count() > 0:
                button.click()
            else:
                input_box.press('Enter')
        
        # 等待结果
        with timer.step(f"[{name}] 等待结果"):
            time.sleep(1.0)
            try:
                page.wait_for_selector('.result-container, .info-item, table', timeout=4000)
            except:
                pass
        
        # 提取数据
        with timer.step(f"[{name}] 提取数据"):
            text_content = page.locator('body').inner_text()
            info = parse_player_info(text_content)
            info['_name'] = name
            info['_raw'] = text_content
            return info
            
    except Exception as e:
        print(f"❌ 查询 {name} 出错: {e}")
        return {'_name': name, '_error': str(e)}


def query_multiple_players(names, headless=True):
    """
    批量查询多个选手（共享浏览器会话）
    
    Args:
        names: 姓名列表
        headless: 是否无头模式
    
    Returns:
        list: 选手信息列表
    """
    global timer
    timer.start()
    results = []
    
    print(f"🚀 批量查询 {len(names)} 位棋手...")
    print(f"   名单: {', '.join(names)}\n")
    
    with sync_playwright() as p:
        # 启动浏览器（只启动一次）
        with timer.step("启动浏览器"):
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(USER_DATA_DIR),
                headless=headless,
                args=['--no-sandbox'] if headless else []
            )
        
        # 获取页面
        with timer.step("初始化页面"):
            page = browser.pages[0] if browser.pages else browser.new_page()
            page.goto(BASE_URL, wait_until='networkidle')
            page.wait_for_selector('input[placeholder*="姓名"], input[type="text"]', timeout=10000)
            print("✅ 浏览器初始化完成\n")
        
        # 逐个查询
        for i, name in enumerate(names, 1):
            print(f"[{i}/{len(names)}] 查询: {name}")
            info = query_single_player(page, name, timer)
            results.append(info)
            
            # 输出当前结果
            if info.get('段位') or info.get('等级分'):
                print(f"    ✅ 段位: {info.get('段位', 'N/A')}, 等级分: {info.get('等级分', 'N/A')}")
            else:
                print(f"    ⚠️ 未找到段位信息")
            print()
        
        # 关闭浏览器（只关闭一次）
        with timer.step("关闭浏览器"):
            browser.close()
    
    return results


def format_batch_output(results, total_elapsed):
    """格式化批量查询输出 - 单行 Markdown 格式"""
    print("\n📋 批量查询结果汇总\n")
    
    for info in results:
        name = info.get('_name', '未知')
        
        if info.get('_error'):
            print(f"• **{name}**: ❌ 查询失败 - {info['_error']}")
            continue
        
        parts = []
        if info.get('段位'):
            parts.append(f"段位: {info['段位']}")
        if info.get('等级分'):
            parts.append(f"等级分: {info['等级分']}")
        if info.get('总排名'):
            parts.append(f"总排名: {info['总排名']}")
        if info.get('省区'):
            parts.append(f"地区: {info['省区']}")
        
        if parts:
            print(f"• **{name}**: {' | '.join(parts)}")
        else:
            print(f"• **{name}**: ⚠️ 未找到段位信息")
    
    print(f"\n⏱️ 总耗时: {total_elapsed:.1f}秒 | 平均: {total_elapsed/len(results):.1f}秒/人\n")
    print(timer.format_report())


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n【单个查询】")
        print("  python3 query_yichafen.py <姓名>")
        print("  示例: python3 query_yichafen.py 张三")
        print("\n【批量查询】")
        print("  python3 query_yichafen.py --batch 姓名1 姓名2 姓名3 ...")
        print("  示例: python3 query_yichafen.py --batch 张三 李四 王五")
        sys.exit(1)
    
    # 检查是否有 --visible 参数（调试用）
    headless = '--visible' not in sys.argv
    
    # 批量查询模式
    if '--batch' in sys.argv:
        names = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
        if len(names) < 1:
            print("❌ 批量查询需要至少一个姓名")
            sys.exit(1)
        
        start_time = time.time()
        results = query_multiple_players(names, headless=headless)
        total_elapsed = time.time() - start_time
        format_batch_output(results, total_elapsed)
        return
    
    # 单个查询模式
    name = sys.argv[1]
    
    start_time = time.time()
    
    # 执行查询
    result_text = query_player(name, headless=headless)
    
    elapsed = time.time() - start_time
    
    if result_text:
        info = parse_player_info(result_text)
        format_output(name, info, elapsed)
        
        # 同时打印原始文本（调试用）
        if '--debug' in sys.argv:
            print("\n原始文本:")
            print("-" * 50)
            print(result_text[:1500])
    else:
        print("❌ 查询失败，请检查网络连接或稍后重试")


if __name__ == "__main__":
    main()
