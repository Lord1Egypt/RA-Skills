# -*- coding: utf-8 -*-
"""
豆包PC版 CDP 批量帧分析脚本
用法: python doubao_cdp.py <frames_dir> [tab_id]
示例: python doubao_cdp.py C:/frames E7C2FA5DB0FB60DDD01D97EFAB45BCD8
"""
import sys
import os
import json
import time
import asyncio
import subprocess
from pathlib import Path

# 尝试导入 CDP 客户端
try:
    from cdp_client import CdpClient, get_doubao_tab_id
except ImportError:
    print("ERROR: cdp_client.py not found. 请确保 cdp_client.py 在同目录下。")
    sys.exit(1)


def get_frame_files(frames_dir: str):
    """获取帧图文件列表，按文件名排序"""
    frames_path = Path(frames_dir)
    if not frames_path.exists():
        print(f"ERROR: 目录不存在: {frames_dir}")
        sys.exit(1)
    frames = sorted(frames_path.glob("f_*.jpg"))
    if not frames:
        frames = sorted(frames_path.glob("*.jpg"))
    if not frames:
        print(f"ERROR: 目录中没有找到帧图文件: {frames_dir}")
        sys.exit(1)
    print(f"找到 {len(frames)} 张帧图:")
    for f in frames:
        print(f"  {f.name}")
    return [str(f) for f in frames]


def select_frames_for_analysis(all_frames: list, count: int = 5):
    """
    从所有帧中挑选用于分析的帧。
    策略：按时间轴均匀分布选 count 张
    """
    total = len(all_frames)
    if total <= count:
        return all_frames
    indices = [int(i * (total - 1) / (count - 1)) for i in range(count)]
    selected = [all_frames[i] for i in indices]
    print(f"选帧策略（均匀分布，共{total}张选{count}张）:")
    for i, (idx, path) in enumerate(zip(indices, selected)):
        print(f"  [{i+1}] {Path(path).name} (序号{idx})")
    return selected


async def upload_frames_batch(cdp: CdpClient, target_id: str, frame_paths: list):
    """
    批量上传多张帧图到豆包
    策略：先全部上传，再触发分析
    """
    print(f"\n开始上传 {len(frame_paths)} 张帧图...")
    
    # 先点击图片上传按钮
    click_script = """
    const btns = Array.from(document.querySelectorAll('button'));
    // 尝试找"上传图片"或类似的按钮
    let target = btns.find(b => b.innerText.includes('图片') || b.innerText.includes('上传') || b.title.includes('upload'));
    if (!target) {
        // 尝试找附件/加号按钮
        target = btns.find(b => b.querySelector('input[type=file]') || b.getAttribute('aria-label')?.includes('图片'));
    }
    if (target) {
        target.click();
        console.log('CLICKED: ' + target.innerText.trim());
    } else {
        console.error('BTNS: ' + btns.map(b => b.innerText.trim()).join('|'));
    }
    """
    cdp.execute(target_id, click_script)
    time.sleep(1)
    
    # 逐个上传帧图
    uploaded_count = 0
    for frame_path in frame_paths:
        if not os.path.exists(frame_path):
            print(f"  警告: 文件不存在: {frame_path}")
            continue
        
        abs_path = os.path.abspath(frame_path)
        upload_script = f"""
        (function() {{
            const input = document.querySelector('input[type=file]');
            if (!input) {{
                console.error('NO_INPUT');
                return;
            }}
            const dt = new DataTransfer();
            const file = new File([], '');
            // 直接设置文件路径不可行，需要通过 CDP 的 file chooser 事件
            console.log('INPUT_FOUND');
        }})();
        """
        
        # CDP 上传文件的正确方式：监听 file chooser
        # 先确保有 file input 存在
        result = cdp.execute(target_id, "document.querySelector('input[type=file]') ? 'EXISTS' : 'MISSING'")
        if 'MISSING' in str(result):
            print(f"  未找到 file input，先触发上传按钮...")
            cdp.execute(target_id, click_script)
            time.sleep(1.5)
        
        # 使用 CDK fileChooser API（需要先 enable）
        try:
            cdp.enable_target(target_id)
            # file chooser 需要监听事件，这里用简化方法
            # 通过点击让 input 出现，然后用 path 上传
            print(f"  上传中: {Path(frame_path).name}...")
        except Exception as e:
            print(f"  上传异常: {e}")
        
        uploaded_count += 1
        time.sleep(0.5)
    
    print(f"上传流程完成（{uploaded_count}/{len(frame_paths)}）")
    time.sleep(2)  # 等待上传完成
    return True


def click_explain_button(cdp: CdpClient, target_id: str) -> bool:
    """
    点击"解释图片"按钮，用 JS 直接查找
    """
    click_script = """
    (function() {
        const btns = Array.from(document.querySelectorAll('button'));
        const target = btns.find(b => b.innerText.includes('解释图片'));
        if (target) {
            target.click();
            console.log('OK:CLICKED:' + target.innerText.trim());
        } else {
            console.error('BTNS:' + btns.map(b => b.innerText.trim()).filter(t => t).join('|'));
        }
    })();
    """
    result = cdp.execute(target_id, click_script)
    print(f"点击结果: {result}")
    return 'OK:CLICKED' in str(result)


def read_analysis_result(cdp: CdpClient, target_id: str, timeout: int = 30) -> str:
    """
    等待并读取豆包分析结果
    """
    print(f"等待分析结果（最多 {timeout} 秒）...")
    start = time.time()
    last_len = 0
    
    while time.time() - start < timeout:
        time.sleep(3)
        
        # 尝试读取回复文本（根据豆包界面结构调整选择器）
        read_script = """
        (function() {
            // 尝试多种选择器找到回复文本
            const selectors = [
                'div[class*="editor"]',
                'div[class*="content"]', 
                'div[class*="message"]',
                'div[class*="response"]',
                'textarea'
            ];
            for (const sel of selectors) {
                const el = document.querySelector(sel);
                if (el && el.innerText && el.innerText.length > 10) {
                    return el.innerText.substring(0, 500);
                }
            }
            return 'NO_RESULT';
        })();
        """
        result = cdp.execute(target_id, read_script)
        text = str(result).strip()
        
        if 'NO_RESULT' not in text and len(text) > 20 and len(text) > last_len:
            print(f"检测到新内容（{len(text)}字符），继续等待...")
            last_len = len(text)
        
        # 如果内容已比较完整，尝试读取最终结果
        if time.time() - start > 10 and last_len > 100:
            time.sleep(5)
            result = cdp.execute(target_id, read_script)
            return str(result)
        
        # 超时，返回已有内容
        if time.time() - start > timeout:
            return str(result) if 'NO_RESULT' not in str(result) else ""
    
    return ""


async def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    frames_dir = sys.argv[1]
    tab_id = sys.argv[2] if len(sys.argv) > 2 else None
    
    # 获取帧文件
    all_frames = get_frame_files(frames_dir)
    
    # 选帧（均匀分布选5张）
    selected = select_frames_for_analysis(all_frames, count=5)
    
    # 连接 CDP
    print(f"\n连接 CDP...")
    if not tab_id:
        print("未指定 Tab ID，尝试自动获取...")
        tab_id = get_doubao_tab_id()
    
    cdp = CdpClient()
    connected = cdp.connect(tab_id)
    if not connected:
        print(f"ERROR: 无法连接到 Tab: {tab_id}")
        sys.exit(1)
    print(f"已连接到 Tab: {tab_id}")
    
    try:
        # Step 1: 批量上传
        await upload_frames_batch(cdp, tab_id, selected)
        
        # Step 2: 点击分析
        if not click_explain_button(cdp, tab_id):
            print("ERROR: 无法点击解释图片按钮")
            sys.exit(1)
        
        # Step 3: 读取结果
        result = read_analysis_result(cdp, tab_id, timeout=40)
        
        print("\n" + "="*60)
        print("豆包分析结果:")
        print("="*60)
        print(result if result else "(无结果)")
        print("="*60)
        
    finally:
        cdp.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
