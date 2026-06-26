#!/usr/bin/env python3
"""
Playwright 自动化脚本：访问Vue.js网站、登录、操作自定义下拉框、点击发送按钮并截图
新策略：使用JavaScript直接操作Vue组件
支持命令行参数指定品类名、店铺名、价格区间
"""

from playwright.sync_api import sync_playwright
import time
import os
import argparse

def main(category, shop, price_range):
    """
    主函数，执行自动化操作
    
    Args:
        category: 品类名称
        shop: 店铺名称
        price_range: 价格区间
    
    Returns:
        截图保存路径
    """
    # 初始化结果变量
    result = {
        'category': {'success': False, 'value': category},
        'shop': {'success': False, 'value': shop},
        'price': {'success': False, 'value': price_range}
    }
    send_clicked = False
    
    with sync_playwright() as p:
        # 启动浏览器（无头模式）
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        print("="*60)
        print("开始执行任务")
        print("="*60)
        print(f"\n📋 执行参数:")
        print(f"  - 品类: {category}")
        print(f"  - 店铺: {shop}")
        print(f"  - 价格区间: {price_range}")
        
        # ==================== 步骤1: 访问网站并登录 ====================
        print("\n【步骤1】访问网站并登录...")
        
        page.goto('http://139.9.192.16:9089/', wait_until='networkidle')
        page.wait_for_timeout(3000)
        
        # 填写用户名
        try:
            page.fill('input[type="text"]', 'test')
            print("  ✓ 已填写用户名")
        except Exception as e:
            print(f"  ✗ 填写用户名失败: {e}")
        
        # 填写密码
        try:
            page.fill('input[type="password"]', '123456')
            print("  ✓ 已填写密码")
        except Exception as e:
            print(f"  ✗ 填写密码失败: {e}")
        
        # 点击登录
        try:
            page.click('button:has-text("登录")')
            print("  ✓ 已点击登录按钮")
        except Exception as e:
            print(f"  ✗ 点击登录失败: {e}")
        
        # 等待登录后的页面完全加载
        print("\n等待页面渲染...")
        page.wait_for_timeout(5000)
        
        # ==================== 步骤2: 定位品类、店铺、价格区间选择器 ====================
        print("\n" + "="*60)
        print("【步骤2】定位并操作下拉框")
        print("="*60)
        
        # 1. 品类选择下拉框
        print("\n1. 操作品类下拉框...")
        try:
            # 点击品类下拉框
            category_selector = 'div[data-select-type="category"] .custom-select'
            page.click(category_selector)
            page.wait_for_timeout(1000)
            
            # 选择指定品类
            page.click(f'.dropdown-menu .dropdown-item:has-text("{category}")')
            print(f"  ✓ 已选择品类: {category}")
            result['category']['success'] = True
        except Exception as e:
            print(f"  ✗ 操作品类下拉框失败: {e}")
        
        # 2. 店铺选择下拉框
        print("\n2. 操作店铺下拉框...")
        try:
            # 点击店铺下拉框
            store_selector = 'div[data-select-type="store"] .custom-select'
            page.click(store_selector)
            page.wait_for_timeout(1000)
            
            # 选择指定店铺
            page.click(f'.dropdown-menu .dropdown-item:has-text("{shop}")')
            print(f"  ✓ 已选择店铺: {shop}")
            result['shop']['success'] = True
        except Exception as e:
            print(f"  ✗ 操作店铺下拉框失败: {e}")
        
        # 3. 价格区间选择下拉框
        print("\n3. 操作价格区间下拉框...")
        try:
            # 点击价格区间下拉框
            price_selector = 'div[data-select-type="priceRange"] .custom-select'
            page.click(price_selector)
            page.wait_for_timeout(1000)
            
            # 选择指定价格区间
            page.click(f'.dropdown-menu .dropdown-item:has-text("{price_range}")')
            print(f"  ✓ 已选择价格区间: {price_range}")
            result['price']['success'] = True
        except Exception as e:
            print(f"  ✗ 操作价格区间下拉框失败: {e}")
        
        # ==================== 步骤3: 点击发送按钮 ====================
        print("\n" + "="*60)
        print("【步骤3】点击发送按钮")
        print("="*60)
        try:
            # 点击发送按钮
            page.click('.send-btn')
            send_clicked = True
            print("  ✓ 已点击发送按钮")
        except Exception as e:
            print(f"  ✗ 点击发送按钮失败: {e}")
        
        # 等待操作完成
        page.wait_for_timeout(3000)

        # ==================== 步骤4: 截图 ====================
        print("\n" + "="*60)
        print("【步骤4】截图")
        print("="*60)

        # 适配Windows路径
        screenshot_path = os.path.join(os.getcwd(), 'screenshot.png')
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"✅ 截图已保存到: {screenshot_path}")
        
        # 关闭浏览器
        context.close()
        browser.close()
        
        # ==================== 任务完成汇总 ====================
        print("\n" + "="*60)
        print("🎉 任务完成!")
        print("="*60)
        print(f"\n📋 执行结果汇总:")
        print(f"  - 品类选择: {'✅ 成功' if result.get('category', {}).get('success', False) else '⚠️ 失败'} (值: {result.get('category', {}).get('value', '无')})")
        print(f"  - 店铺选择: {'✅ 成功' if result.get('shop', {}).get('success', False) else '⚠️ 失败'} (值: {result.get('shop', {}).get('value', '无')})")
        print(f"  - 价格选择: {'✅ 成功' if result.get('price', {}).get('success', False) else '⚠️ 失败'} (值: {result.get('price', {}).get('value', '无')})")
        print(f"  - 发送按钮: {'✅ 已点击' if send_clicked else '⚠️ 失败'}")
        print(f"  - 截图: ✅ 已保存到 screenshot_form.png")
        
        return screenshot_path

if __name__ == '__main__':
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='自动化操作下拉框并截图')
    parser.add_argument('--category', type=str, required=True, help='品类名称')
    parser.add_argument('--shop', type=str, required=True, help='店铺名称')
    parser.add_argument('--price-range', type=str, dest='price_range', required=True, help='价格区间')
    
    args = parser.parse_args()
    
    # 执行主函数
    main(
        category=args.category,
        shop=args.shop,
        price_range=args.price_range
    )
