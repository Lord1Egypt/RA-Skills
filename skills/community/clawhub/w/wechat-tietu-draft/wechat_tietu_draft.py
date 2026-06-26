#!/usr/bin/env python3
"""
wechat-tietu-draft: 微信公众号贴图类型草稿创建脚本
专门用于从.txt文件创建贴图类型草稿，修复段落丢失问题。

重要规则：
1. 只接受.txt文本文件
2. 将纯文本转换为HTML格式以保留段落结构
3. 标题和正文只允许纯文本及emoji
4. 文件第一行作为标题（可选），其余作为正文

段落处理规则（修复版）：
- 双换行符(\n\n) → 段落分隔 <br><br>
- 单换行符(\n) → 段落内换行 <br>

版本: v1.0.0
"""

import os
import sys

# 清除所有代理环境变量，避免websockets的SOCKS代理错误
proxy_vars = [
    'http_proxy', 'https_proxy', 'all_proxy',
    'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY',
    'no_proxy', 'NO_PROXY'
]

for var in proxy_vars:
    os.environ.pop(var, None)

import json
import time
import asyncio
import re
import websockets
import subprocess
import urllib.parse

# 与 skill_main 共用（skill_main 不 import 本模块，无循环依赖）
from skill_main import (
    DEFAULT_CDP_PORT,
    check_wechat_session_expired_via_cdp,
    ensure_chrome_ready_for_draft,
    print_chrome_help,
    prompt_session_expired_scan_login,
    refetch_best_wechat_page,
    validate_and_read_txt_file,
    wait_until_ready_for_draft,
)

CDP_PORT = int(os.environ.get("CDP_TIETU_PORT", str(DEFAULT_CDP_PORT)))


def _js_json_literal(s):
    """将 Python 字符串转为可在 JS 中 JSON.parse('...') 的安全字面量，避免 ` \\ ${ 等破坏脚本。"""
    return json.dumps(s, ensure_ascii=False).replace('\\', '\\\\').replace("'", "\\'")


def convert_text_to_prosemirror_html(text):
    """
    将纯文本转换为ProseMirror兼容的HTML
    修复段落丢失问题：使用<br>标签而不是<p>标签
    
    规则:
    1. 双换行符(\n\n) -> <br><br> (段落分隔)
    2. 单换行符(\n) -> <br> (段落内换行)
    3. 转义文本中的HTML标签，但保留文本中的<br>字样
    """
    if not text or not text.strip():
        return ""
    
    # 第一步：先处理换行符转换，避免干扰
    # 标准化换行符
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # 第二步：转换换行符为临时标记
    # 使用临时标记，避免与文本中的<br>混淆
    # 1. 将双换行符替换为 [DOUBLE_BR]
    temp_text = text.replace('\n\n', '[DOUBLE_BR]')
    # 2. 将剩余的单换行符替换为 [SINGLE_BR]
    temp_text = temp_text.replace('\n', '[SINGLE_BR]')
    
    # 第三步：转义HTML标签
    import html
    escaped_text = html.escape(temp_text)
    
    # 第四步：将临时标记恢复为真正的<br>标签
    # 注意：文本中的<br>字样已经被转义为&lt;br&gt;
    result = escaped_text.replace('[DOUBLE_BR]', '<br><br>')
    result = result.replace('[SINGLE_BR]', '<br>')
    
    return result

async def create_tietu_draft_from_file(file_path):
    """从.txt文件创建贴图类型草稿"""
    print("微信公众号贴图草稿运行日志（文件输入版）")
    print(time.strftime("%Y-%m-%d %H:%M:%S"))
    print("-" * 3)
    
    print("\n📋 重要规则:")
    print("1. ✅ 只接受.txt文本文件")
    print("2. ✅ 不做任何HTML或格式转换")
    print("3. ✅ 标题和正文只允许纯文本及emoji")
    print("4. ✅ 文件第一行作为标题（可选），其余作为正文")
    
    # 验证并读取文件
    title, content = validate_and_read_txt_file(file_path)
    if title is None or content is None:
        print("\n❌ 文件验证失败，任务终止")
        return
    
    if not ensure_chrome_ready_for_draft(CDP_PORT):
        print("\n❌ Chrome 未就绪，任务终止")
        return
    
    print("\n📋 前提条件:")
    print(f"1. Chrome已启动 (端口 {CDP_PORT})")
    print("2. 已扫码登录微信公众号")
    print("3. 在微信公众号页面")
    
    # 检查Chrome状态
    print("\n🔍 检查Chrome状态...")
    try:
        result = subprocess.run(
            ["curl", "-s", f"http://127.0.0.1:{CDP_PORT}/json/list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            print("❌ 无法连接到Chrome调试端口")
            print("请确保Chrome已启动并启用远程调试:")
            print("  Chrome启动命令:")
            print("  /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome \\")
            print(f"    --remote-debugging-port={CDP_PORT} \\")
            print("    --user-data-dir=/tmp/wechat-debug \\")
            print("    https://mp.weixin.qq.com/")
            return
        
        pages = json.loads(result.stdout)
        if not pages:
            print("❌ 没有找到Chrome页面")
            return
        
        print(f"✅ 找到 {len(pages)} 个页面")
        
        # 查找微信公众号页面
        wechat_page = None
        for page in pages:
            url = page.get('url', '')
            title_text = page.get('title', '')
            
            # 检查是否是微信公众号页面
            if 'mp.weixin.qq.com' in url:
                wechat_page = page
                print(f"✅ 找到微信公众号页面: {url[:80]}...")
                break
        
        if not wechat_page:
            print("❌ 未找到微信公众号页面")
            print("请确保已登录微信公众号")
            return

        # 会话过期单独检测（扫码登录页已由 check_chrome_running_strict 按标题处理）
        ws_dbg = wechat_page.get("webSocketDebuggerUrl")
        if check_wechat_session_expired_via_cdp(ws_dbg) is True:
            print("❌ 微信公众号会话已过期（a#jumpUrl「登录」）")
            prompt_session_expired_scan_login(ws_dbg, will_auto_continue=True)
            if not wait_until_ready_for_draft(port=CDP_PORT, max_seconds=300, interval=5):
                return
            wechat_page = refetch_best_wechat_page(CDP_PORT)
            if not wechat_page:
                print("❌ 登录后仍无法获取有效的微信公众号页面")
                return
            print(f"✅ 已切换到登录后的页面: {(wechat_page.get('url') or '')[:80]}...")
            ws_dbg = wechat_page.get("webSocketDebuggerUrl")

        # 提取token
        url = wechat_page['url']
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        token = query_params.get('token', [''])[0]
        
        if not token:
            print("❌ 无法从URL提取token")
            print(f"URL: {url[:100]}...")
            return
        
        print(f"✅ 提取到token: {token[:10]}...")
        
        # 总是创建新的贴图类型草稿，避免覆盖现有草稿
        # 即使当前页面已经是贴图类型草稿编辑器，也创建新的
        tietu_url = f"https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=77&createType=8&token={token}&lang=zh_CN"
        print(f"\n🌐 创建新的贴图类型草稿...")
        print(f"目标URL: {tietu_url[:80]}...")
        
        # 记录原始URL用于后续比较
        original_url = wechat_page['url']
        original_appmsgid = None
        if 'appmsgid=' in original_url:
            import re
            match = re.search(r'appmsgid=(\d+)', original_url)
            if match:
                original_appmsgid = match.group(1)
                print(f"原始草稿ID: {original_appmsgid}")
        
        should_navigate = True  # 总是导航到新草稿页面
        
        # 保存原始信息供后续使用
        url_info = {
            'original_url': original_url,
            'original_appmsgid': original_appmsgid
        }
        
        # 获取WebSocket URL
        ws_url = wechat_page['webSocketDebuggerUrl']
        
        # 连接到Chrome DevTools
        print("\n🔗 连接到Chrome DevTools...")
        async with websockets.connect(ws_url, proxy=None) as websocket:
            print("✅ 连接成功")
            print(f"   连接URL: {ws_url}")
            
            # 调试：获取页面信息
            debug_cmd = {
                "id": 0,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": "JSON.stringify({title: document.title, url: window.location.href, readyState: document.readyState})",
                    "returnByValue": True
                }
            }
            await websocket.send(json.dumps(debug_cmd))
            debug_response = await websocket.recv()
            debug_result = json.loads(debug_response)
            print(f"🔍 初始调试: {debug_result}")
            
            if should_navigate:
                # 导航到贴图类型草稿页面
                navigate_cmd = {
                    "id": 1,
                    "method": "Page.navigate",
                    "params": {"url": tietu_url}
                }
                
                await websocket.send(json.dumps(navigate_cmd))
                response = await websocket.recv()
                print("✅ 页面导航完成")
                
                # 等待页面加载：先等 load 事件，再给 SPA 渲染时间
                print("⏳ 等待页面加载...")
                await asyncio.sleep(3)
            else:
                print("✅ 使用现有页面，跳过导航")
                await asyncio.sleep(3)
            
            # 检查页面元素（带重试：SPA 可能延迟渲染）
            elements = {}
            max_check_attempts = 3
            check_interval = 2
            print("\n🔍 检查页面元素...")
            check_elements_js = """
            (function() {
                try {
                    const elements = {};
                    
                    // 基本页面信息
                    elements.pageTitle = document.title;
                    elements.url = window.location.href;
                    elements.readyState = document.readyState;
                    
                    // 简化：检查标题输入框
                    const titleInput = document.querySelector('textarea#title');
                    elements.hasTitleInput = !!titleInput;
                    if (titleInput) {
                        elements.titleValue = titleInput.value;
                        elements.titleId = titleInput.id;
                    }
                    
                    // 正文编辑器：页面上常有多个 ProseMirror（标题区/摘要/正文），
                    // querySelector 只取到第一个会把正文写进标题区 → 标题像正文、正文空。
                    const pmAll = Array.from(document.querySelectorAll('div.ProseMirror[contenteditable="true"]'));
                    function pmArea(el) {
                        if (!el) return 0;
                        const r = el.getBoundingClientRect();
                        return Math.max(0, r.width) * Math.max(0, r.height);
                    }
                    let contentEditor = null;
                    if (pmAll.length === 1) {
                        contentEditor = pmAll[0];
                    } else if (pmAll.length > 1) {
                        contentEditor = pmAll.reduce(function(a, b) { return pmArea(a) >= pmArea(b) ? a : b; });
                    }
                    elements.proseMirrorCount = pmAll.length;
                    elements.hasContentEditor = !!contentEditor;
                    if (contentEditor) {
                        elements.contentText = contentEditor.textContent.substring(0, 100);
                    }
                    
                    // 简化：检查保存按钮
                    const buttons = Array.from(document.querySelectorAll('button'));
                    const saveButtons = buttons.filter(btn => 
                        btn.textContent.includes('保存为草稿') || btn.textContent.includes('保存')
                    );
                    elements.hasSaveButton = saveButtons.length > 0;
                    elements.saveButtonCount = saveButtons.length;
                    
                    // 简单调试信息
                    elements.debug = {
                        totalButtons: buttons.length,
                        bodyChildren: document.body.children.length,
                        hasForm: document.querySelector('form') !== null,
                        hasTextarea: document.querySelector('textarea') !== null
                    };
                    
                    return elements;
                } catch (error) {
                    return {error: error.message, stack: error.stack};
                }
            })()
            """
            
            # 必须使用 returnByValue: True，否则 CDP 只返回对象引用，拿不到 pageTitle/url 等序列化值，会显示「未知」且元素全未找到
            check_cmd = {
                "id": 2,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": check_elements_js,
                    "returnByValue": True
                }
            }
            
            for attempt in range(max_check_attempts):
                if attempt > 0:
                    print(f"   重试 ({attempt + 1}/{max_check_attempts})，等待 {check_interval} 秒...")
                    await asyncio.sleep(check_interval)
                await websocket.send(json.dumps(check_cmd))
                response = await websocket.recv()
                result = json.loads(response)
                if 'result' not in result or 'result' not in result.get('result', {}):
                    continue
                elements = result['result']['result'].get('value', {})
                if not isinstance(elements, dict):
                    elements = {}
                if elements.get('error'):
                    print(f"❌ JavaScript执行错误: {elements.get('error')}")
                    print(f"   堆栈: {elements.get('stack', '无')}")
                    return
                # 三个关键元素都找到则不再重试
                if (elements.get('hasTitleInput') and elements.get('hasContentEditor') and elements.get('hasSaveButton')):
                    break

            # 使用最后一次检查得到的 elements 输出（returnByValue 已保证拿到序列化值）
            print(f"🔍 页面检查结果:")
            print(f"   页面标题: {elements.get('pageTitle', '未知')}")
            url_str = elements.get('url') or '未知'
            print(f"   页面URL: {(url_str[:80] + '...') if len(str(url_str)) > 80 else url_str}")
            print(f"   文档状态: {elements.get('readyState', '未知')}")
            
            print(f"\n📝 元素检查:")
            print(f"   标题输入框: {'✅ 找到' if elements.get('hasTitleInput') else '❌ 未找到'}")
            if elements.get('hasTitleInput'):
                title_val = elements.get('titleValue') or '空'
                print(f"   当前标题值: {str(title_val)[:50]}...")
            
            print(f"   正文编辑器: {'✅ 找到' if elements.get('hasContentEditor') else '❌ 未找到'}")
            if elements.get('proseMirrorCount'):
                print(f"   ProseMirror 数量: {elements.get('proseMirrorCount')}（正文取面积最大者，避免写进标题区）")
            if elements.get('hasContentEditor'):
                content_preview = elements.get('contentText') or '空'
                print(f"   内容预览: {str(content_preview)[:50]}...")
            
            print(f"   保存按钮: {'✅ 找到' if elements.get('hasSaveButton') else '❌ 未找到'}")
            print(f"   保存按钮数量: {elements.get('saveButtonCount', 0)}")
            
            debug_info = elements.get('debug', {}) or {}
            print(f"\n📊 调试信息:")
            print(f"   总按钮数: {debug_info.get('totalButtons', 0)}")
            print(f"   Body子元素: {debug_info.get('bodyChildren', 0)}个")
            print(f"   有表单: {'✅ 是' if debug_info.get('hasForm') else '❌ 否'}")
            print(f"   有文本域: {'✅ 是' if debug_info.get('hasTextarea') else '❌ 否'}")
            
            if not elements.get('hasTitleInput'):
                print("\n⚠️  警告: 未找到标题输入框")
                print("   可能原因:")
                print("   1. 页面未完全加载")
                print("   2. 微信公众号界面已更新")
                print("   3. 不是贴图类型草稿页面")
            
            if not elements.get('hasContentEditor'):
                print("\n⚠️  警告: 未找到正文编辑器")
                print("   可能原因:")
                print("   1. 页面未完全加载")
                print("   2. 微信公众号界面已更新")
                print("   3. 不是贴图类型草稿页面")
            
            if not elements.get('hasSaveButton'):
                print("\n⚠️  警告: 未找到保存按钮")
                print("   可能原因:")
                print("   1. 页面未完全加载")
                print("   2. 微信公众号界面已更新")
                print("   3. 不是贴图类型草稿页面")
            
            if not (elements.get('hasTitleInput') and elements.get('hasContentEditor') and elements.get('hasSaveButton')):
                print("\n❌ 页面关键元素未找全，无法继续填写。请确认已打开贴图类型草稿页面并重试。")
                return
            
            # 填写标题（如果有）
            if title:
                print(f"\n📝 填写标题: {title}")
                title_payload = _js_json_literal(title)
                fill_title_js = f"""
                (function() {{
                    var titleStr = JSON.parse('{title_payload}');
                    var titleInput = document.querySelector('textarea#title');
                    if (titleInput) {{
                        titleInput.value = titleStr;
                        titleInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        return {{ success: true, value: titleInput.value }};
                    }}
                    return {{ success: false }};
                }})()
                """
                eval_cmd = {
                    "id": 3,
                    "method": "Runtime.evaluate",
                    "params": {
                        "expression": fill_title_js,
                        "awaitPromise": True,
                        "returnByValue": True
                    }
                }
                await websocket.send(json.dumps(eval_cmd))
                response = await websocket.recv()
                result = json.loads(response)
                if 'result' in result and 'result' in result['result']:
                    fill_result = result['result']['result'].get('value') or {}
                    if fill_result.get('success'):
                        print("✅ 标题填写成功")
                    else:
                        print("❌ 标题填写失败")
            
            # 填写正文（HTML 通过 JSON 传入，避免 ` \ ${ 等破坏脚本）
            print(f"\n📄 填写正文 ({len(content)} 字符)...")
            html_content = convert_text_to_prosemirror_html(content)
            print(f"   🔄 转换为HTML: {len(html_content)} 字符")
            print(f"   📋 HTML预览: {html_content[:100]}...")
            html_payload = _js_json_literal(html_content)
            fill_content_js = f"""
            (function() {{
                var htmlStr = JSON.parse('{html_payload}');
                var pmAll = Array.from(document.querySelectorAll('div.ProseMirror[contenteditable="true"]'));
                function pmArea(el) {{
                    if (!el) return 0;
                    var r = el.getBoundingClientRect();
                    return Math.max(0, r.width) * Math.max(0, r.height);
                }}
                var contentEditor = null;
                if (pmAll.length === 1) contentEditor = pmAll[0];
                else if (pmAll.length > 1)
                    contentEditor = pmAll.reduce(function(a, b) {{ return pmArea(a) >= pmArea(b) ? a : b; }});
                if (contentEditor) {{
                    contentEditor.innerHTML = '';
                    contentEditor.innerHTML = htmlStr;
                    contentEditor.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    contentEditor.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    return {{
                        success: true,
                        charCount: contentEditor.textContent.length,
                        htmlLength: contentEditor.innerHTML.length,
                        htmlPreview: contentEditor.innerHTML.substring(0, 100),
                        pickedIndex: pmAll.indexOf(contentEditor),
                        proseMirrorCount: pmAll.length
                    }};
                }}
                return {{ success: false, proseMirrorCount: pmAll.length }};
            }})()
            """
            eval_cmd = {
                "id": 4,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": fill_content_js,
                    "awaitPromise": True,
                    "returnByValue": True
                }
            }
            await websocket.send(json.dumps(eval_cmd))
            response = await websocket.recv()
            result = json.loads(response)
            if 'result' in result and 'result' in result['result']:
                fill_result = result['result']['result'].get('value') or {}
                if fill_result.get('success'):
                    print(f"✅ 正文填写成功")
                    print(f"   字符数: {fill_result.get('charCount', '未知')}")
                    if fill_result.get('proseMirrorCount', 0) > 1:
                        print(f"   使用第 {fill_result.get('pickedIndex', '?') + 1}/{fill_result.get('proseMirrorCount')} 个 ProseMirror（按面积大小区分正文）")
                else:
                    print("❌ 正文填写失败")
                    if fill_result.get('proseMirrorCount') is not None:
                        print(f"   ProseMirror 数量: {fill_result.get('proseMirrorCount')}")
            
            # 保存草稿
            print("\n💾 保存草稿...")
            save_js = """
            (function() {
                var saveButtons = Array.from(document.querySelectorAll('button')).filter(function(btn) {
                    return btn.textContent.indexOf('保存为草稿') !== -1 || btn.textContent.indexOf('保存') !== -1;
                });
                if (saveButtons.length > 0) {
                    saveButtons[0].click();
                    return { success: true, buttonText: saveButtons[0].textContent };
                }
                return { success: false };
            })()
            """
            eval_cmd = {
                "id": 5,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": save_js,
                    "awaitPromise": True,
                    "returnByValue": True
                }
            }
            await websocket.send(json.dumps(eval_cmd))
            response = await websocket.recv()
            result = json.loads(response)
            if 'result' in result and 'result' in result['result']:
                save_result = result['result']['result'].get('value') or {}
                if save_result.get('success'):
                    print(f"✅ 已点击保存按钮: {save_result.get('buttonText', '未知')}")
                else:
                    print("❌ 保存按钮点击失败")
            
            # 方案C优化：等待800毫秒后开始检查保存状态
            print("\n⏳ 等待保存完成（方案C优化: 800ms）...")
            await asyncio.sleep(0.8)
            
            # 重要：给页面更多时间完成跳转和保存
            print("⏳ 等待页面完成跳转和保存（额外2秒）...")
            await asyncio.sleep(2)
            
            # 检查保存状态
            print("🔍 检查保存状态...")
            check_save_js = """
            (function() {
                const status = {};
                
                // 检查Toast提示
                const toasts = Array.from(document.querySelectorAll('.weui-toast, .weui-toptips, .el-message'));
                status.hasToast = toasts.length > 0;
                status.toastText = toasts.length > 0 ? toasts[0].textContent : '';
                
                // 检查页面标题变化
                status.pageTitle = document.title;
                status.isSavedPage = document.title.includes('草稿') || document.title.includes('Draft');
                
                // 检查URL变化
                status.currentUrl = window.location.href;
                status.hasToken = status.currentUrl.includes('token=');
                status.isTietuType = status.currentUrl.includes('type=77') && status.currentUrl.includes('createType=8');
                
                // 新增：检查草稿是否已存在
                status.hasAppMsgId = status.currentUrl.includes('appmsgid=');
                status.hasReprintConfirm = status.currentUrl.includes('reprint_confirm=0');
                status.isExistingDraft = status.hasAppMsgId && status.hasReprintConfirm && status.currentUrl.includes('type=77');
                
                // 检查按钮状态变化
                const buttons = Array.from(document.querySelectorAll('button'));
                const saveButtons = buttons.filter(btn => 
                    btn.textContent.includes('保存为草稿') || btn.textContent.includes('保存')
                );
                const editButtons = buttons.filter(btn => 
                    btn.textContent.includes('继续编辑') || btn.textContent.includes('编辑')
                );
                
                status.saveButtonDisabled = saveButtons.length > 0 ? saveButtons[0].disabled : false;
                status.hasEditButton = editButtons.length > 0;
                
                return status;
            })()
            """
            
            eval_cmd = {
                "id": 6,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": check_save_js,
                    "awaitPromise": True
                }
            }
            
            await websocket.send(json.dumps(eval_cmd))
            response = await websocket.recv()
            result = json.loads(response)
            
            if 'result' in result and 'result' in result['result']:
                status = result['result']['result'].get('value', {})
                
                print("\n📊 保存状态报告:")
                
                # 多维度检查保存状态
                checks = []
                
                # 1. Toast提示检查
                if status.get('hasToast'):
                    toast_text = status.get('toastText', '')
                    if '成功' in toast_text or '保存' in toast_text:
                        checks.append(("✅ Toast提示", "保存成功提示"))
                    else:
                        checks.append(("⚠️  Toast提示", f"有提示但内容: {toast_text[:30]}..."))
                else:
                    checks.append(("❓ Toast提示", "无提示"))
                
                # 2. 页面标题检查
                page_title = status.get('pageTitle', '')
                if '草稿' in page_title or 'Draft' in page_title:
                    checks.append(("✅ 页面标题", "包含草稿相关字样"))
                else:
                    checks.append(("❓ 页面标题", f"当前: {page_title[:30]}..."))
                
                # 3. URL检查
                current_url = status.get('currentUrl', '')
                has_token = status.get('hasToken', False)
                is_tietu_type = status.get('isTietuType', False)
                has_appmsgid = status.get('hasAppMsgId', False)
                has_reprint_confirm = status.get('hasReprintConfirm', False)
                is_existing_draft = status.get('isExistingDraft', False)
                
                if is_existing_draft:
                    # 这是已存在的草稿编辑器页面
                    checks.append(("✅ URL参数", "已有草稿页面(appmsgid+reprint_confirm+type=77)"))
                elif has_token and is_tietu_type:
                    checks.append(("✅ URL参数", "包含token和贴图类型参数"))
                elif has_token:
                    checks.append(("⚠️  URL参数", "有token但不是贴图类型"))
                else:
                    checks.append(("❓ URL参数", "无token参数"))
                
                # 4. 按钮状态检查
                save_disabled = status.get('saveButtonDisabled', False)
                has_edit_button = status.get('hasEditButton', False)
                
                if save_disabled:
                    checks.append(("✅ 按钮状态", "保存按钮已禁用"))
                else:
                    checks.append(("❓ 按钮状态", "保存按钮未禁用"))
                
                if has_edit_button:
                    checks.append(("✅ 编辑按钮", "出现继续编辑按钮"))
                else:
                    checks.append(("❓ 编辑按钮", "无继续编辑按钮"))
                
                # 显示检查结果
                for check, desc in checks:
                    print(f"   {check}: {desc}")
                
                # 综合判断
                success_checks = sum(1 for check, _ in checks if check.startswith('✅'))
                warning_checks = sum(1 for check, _ in checks if check.startswith('⚠️'))
                
                print(f"\n📈 检查统计: ✅ {success_checks} | ⚠️  {warning_checks} | ❓ {len(checks) - success_checks - warning_checks}")
                
                # 添加URL变化验证
                print(f"\n🔗 URL变化验证:")
                final_url_check = """
                (function() {
                    return {
                        url: window.location.href,
                        hasAppMsgId: window.location.href.includes('appmsgid='),
                        appmsgid: (function() {
                            const match = window.location.href.match(/appmsgid=(\\d+)/);
                            return match ? match[1] : null;
                        })()
                    };
                })()
                """
                
                final_check_cmd = {
                    "id": 10,
                    "method": "Runtime.evaluate",
                    "params": {"expression": final_url_check, "returnByValue": True}
                }
                await websocket.send(json.dumps(final_check_cmd))
                final_response = await websocket.recv()
                final_result = json.loads(final_response)
                
                final_url = None
                final_appmsgid = None
                if 'result' in final_result and 'result' in final_result['result']:
                    url_info = final_result['result']['result'].get('value', {})
                    final_url = url_info.get('url', '')
                    final_appmsgid = url_info.get('appmsgid')
                
                print(f"   最终URL: {final_url[:80] if final_url else '未知'}...")
                print(f"   最终草稿ID: {final_appmsgid if final_appmsgid else '无'}")
                print(f"   原始草稿ID: {url_info.get('original_appmsgid', '无')}")
                
                # 基于URL变化的成功判断
                url_based_success = False
                original_appmsgid = url_info.get('original_appmsgid')
                
                if final_appmsgid and original_appmsgid:
                    if final_appmsgid != original_appmsgid:
                        print(f"   ✅ 草稿ID变化: {original_appmsgid} → {final_appmsgid} (创建了新草稿)")
                        url_based_success = True
                    else:
                        print(f"   ⚠️  草稿ID未变: 可能是覆盖或导航失败")
                elif final_appmsgid and not original_appmsgid:
                    print(f"   ✅ 创建了草稿 (新ID: {final_appmsgid})")
                    url_based_success = True
                elif final_url and 'isNew=1' in final_url and 'appmsgid=' in final_url:
                    print(f"   ✅ 从isNew=1页面变成了有appmsgid的编辑页面")
                    url_based_success = True
                
                # 最终成功判断：JavaScript检查 OR URL变化验证
                final_success = (success_checks >= 3) or is_existing_draft or url_based_success
                
                if final_success:
                    print("\n🎉 保存成功！贴图草稿已创建。")
                    print(f"   标题: {title if title else '(无标题)'}")
                    print(f"   正文长度: {len(content)} 字符")
                    print(f"   保存时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    if is_existing_draft:
                        print(f"   📝 这是已有草稿的编辑器页面")
                    elif url_based_success:
                        print(f"   🔗 通过URL变化验证成功")
                        if final_appmsgid:
                            print(f"   草稿ID: {final_appmsgid}")
                else:
                    print("\n⚠️  保存状态不确定，请手动检查:")
                    print("   1. 查看微信公众号草稿箱")
                    print("   2. 检查页面是否有错误提示")
                    print("   3. 如果需要，手动保存草稿")
                    print("   ℹ️  注意: 即使脚本报告失败，操作也可能已成功")
            
            print("\n") 
            print("任务完成")
            print("=" * 3)
            
    except websockets.exceptions.InvalidURI:
        print("❌ 无效的WebSocket URL")
    except websockets.exceptions.ConnectionClosedError:
        print("❌ WebSocket连接已关闭")
    except ConnectionRefusedError:
        print("❌ 无法连接到Chrome调试端口")
        print("请确保Chrome已启动并启用远程调试")
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    """仅允许由 skill_main 通过子进程调用（环境变量 CDP_TIETU_CHILD=1）。"""
    if os.environ.get("CDP_TIETU_CHILD") != "1":
        d = os.path.dirname(os.path.abspath(__file__))
        print("请勿直接运行本脚本。")
        print("请使用技能入口创建贴图草稿：")
        print()
        print(f"  cd {d}")
        print("  python3 skill_main.py --file <你的文章.txt>")
        print()
        print("—" * 56)
        print("【给 OpenClaw / 自动化】")
        print("  不要为「直接运行本脚本」去改代码（例如去掉 CDP_TIETU_CHILD 或改入口）。")
        print("  正确用法：始终通过 skill_main.py --file <文章.txt> 创建草稿；")
        print("  本文件仅作 skill_main 的子进程，故意不可单独执行。")
        print("—" * 56)
        print()
        sys.exit(2)
    if len(sys.argv) != 2:
        print("内部调用参数错误：需要唯一参数 .txt 路径", file=sys.stderr)
        sys.exit(1)
    asyncio.run(create_tietu_draft_from_file(sys.argv[1]))


if __name__ == "__main__":
    main()