#!/usr/bin/env python3
"""
黑鸟骑行记录上传工具
批量上传 FIT 文件到黑鸟网页版 (https://www.blackbirdsport.com)

依赖：
- playwright (pip install playwright)
- playwright install chromium (首次运行需要)

使用方法：
    python upload_to_blackbird.py <fit_file_or_directory> [more_files...]
    
示例：
    python upload_to_blackbird.py /path/to/ride.fit
    python upload_to_blackbird.py /path/to/rides/
    python upload_to_blackbird.py *.fit
"""

import sys
import os
import glob
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


def upload_to_blackbird(file_paths, headless=False):
    """
    上传 FIT 文件到黑鸟骑行网页
    
    Args:
        file_paths: FIT 文件路径列表
        headless: 是否无头模式运行（默认 False，显示浏览器便于登录）
    """
    # 确保所有文件都存在
    valid_files = []
    for fp in file_paths:
        if os.path.isfile(fp) and fp.endswith('.fit'):
            valid_files.append(os.path.abspath(fp))
        else:
            print(f"跳过无效文件：{fp}")
    
    if not valid_files:
        print("错误：没有有效的 FIT 文件")
        return False
    
    print(f"准备上传 {len(valid_files)} 个文件到黑鸟骑行...")
    
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800}
        )
        page = context.new_page()
        
        # 导航到上传页面
        upload_url = "https://www.blackbirdsport.com/user/records/upload"
        print(f"正在打开：{upload_url}")
        page.goto(upload_url, timeout=60000)
        
        # 等待页面加载（检查是否已登录）
        try:
            # 等待上传按钮出现（表示已登录）
            page.wait_for_selector('button:has-text("Choose File")', timeout=10000)
            print("✓ 已登录，可以上传文件")
        except PlaywrightTimeout:
            print("⚠ 未检测到登录状态，请先在浏览器中登录")
            print("登录完成后，脚本会自动继续...")
            # 等待用户登录（最长 5 分钟）
            try:
                page.wait_for_selector('button:has-text("Choose File")', timeout=300000)
                print("✓ 检测到登录，继续上传")
            except PlaywrightTimeout:
                print("超时：用户未登录，退出")
                browser.close()
                return False
        
        # 使用文件上传功能
        # 找到文件输入元素（通常在 Choose File 按钮后面）
        file_input = page.query_selector('input[type="file"]')
        
        if file_input:
            # 直接设置文件输入
            print(f"正在上传文件...")
            file_input.set_input_files(valid_files)
            
            # 等待上传完成
            print("等待上传完成...")
            page.wait_for_timeout(10000)  # 等待 10 秒让上传开始
            
            # 检查上传状态
            try:
                # 等待看到"成功"状态
                page.wait_for_selector('text=成功', timeout=60000)
                print("✓ 文件上传成功！")
            except PlaywrightTimeout:
                print("⚠ 上传可能需要更长时间，请检查网页状态")
        else:
            # 如果没有找到 file input，尝试点击 Choose File 按钮
            print("未找到文件输入元素，尝试点击 Choose File 按钮...")
            page.click('button:has-text("Choose File")')
            page.wait_for_timeout(2000)
            # 使用系统文件对话框（需要额外的处理）
            print("⚠ 需要手动选择文件，或使用 playwright 的 set_input_files 方法")
        
        print("\n上传完成！请检查网页上的上传状态。")
        print("如需关闭浏览器，请手动关闭或按 Ctrl+C")
        
        # 保持浏览器打开一段时间让用户查看结果
        try:
            page.wait_for_timeout(30000)  # 等待 30 秒
        except KeyboardInterrupt:
            pass
        
        browser.close()
    
    return True


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("错误：请提供至少一个 FIT 文件路径")
        sys.exit(1)
    
    # 收集所有文件
    all_files = []
    for arg in sys.argv[1:]:
        if os.path.isdir(arg):
            # 如果是目录，获取所有 .fit 文件
            files = glob.glob(os.path.join(arg, "*.fit"))
            all_files.extend(files)
        elif '*' in arg or '?' in arg:
            # 通配符匹配
            files = glob.glob(arg)
            all_files.extend(files)
        else:
            all_files.append(arg)
    
    # 过滤出 _GM.fit 文件（如果存在）
    gm_files = [f for f in all_files if '_GM.fit' in f]
    if gm_files:
        print(f"找到 {len(gm_files)} 个 _GM.fit 文件")
        files_to_upload = gm_files
    else:
        print(f"找到 {len(all_files)} 个 FIT 文件")
        files_to_upload = all_files
    
    # 执行上传
    success = upload_to_blackbird(files_to_upload, headless=False)
    
    if success:
        print("\n✓ 上传流程完成！")
        sys.exit(0)
    else:
        print("\n✗ 上传失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
