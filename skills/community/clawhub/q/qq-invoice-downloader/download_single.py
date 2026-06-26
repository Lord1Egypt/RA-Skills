"""
单独下载和运国际发票 - 2026年1月8日
发票号码: 26312000000140009506
"""
import os
import re
from imap_tools import MailBox, A
from datetime import date
from playwright.sync_api import sync_playwright

OUTPUT_DIR = "Z:/OpenClaw/InvoiceOC/260108_v3"
os.makedirs(OUTPUT_DIR, exist_ok=True)

IMAP_SERVER = 'imap.qq.com'
EMAIL = '181957682@qq.com'
PASSWORD = 'dcdrfqjmoczrbhdj'

def download_tax_invoice():
    """从税务平台下载发票"""
    
    # 发票信息
    invoice_no = "26312000000140009506"
    url = f"https://dppt.shanghai.chinatax.gov.cn:8443/v/2_{invoice_no}_20260108161936008XK8EB0"
    
    print(f"访问: {url}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # 需要可见以便下载
            args=['--disable-web-security']
        )
        context = browser.new_context(
            accept_downloads=True
        )
        page = context.new_page()
        
        page.goto(url, timeout=60000)
        page.wait_for_load_state('networkidle')
        
        print("页面加载完成，等待下载按钮...")
        page.wait_for_timeout(3000)
        
        # 点击PDF下载
        try:
            with page.expect_download(timeout=30000) as download_info:
                page.click("button:has-text('PDF下载')")
            
            download = download_info.value
            save_path = os.path.join(OUTPUT_DIR, download.suggested_filename)
            download.save_as(save_path)
            print(f"下载成功: {save_path}")
        except Exception as e:
            print(f"下载失败: {e}")
            # 尝试使用JS点击
            page.evaluate('document.querySelector("button").click()')
            page.wait_for_timeout(5000)
        
        browser.close()

if __name__ == "__main__":
    download_tax_invoice()
