"""
发布+配置一体函数 v3.4（CDP 直连方案 + 每步自检重试 + 自动发货二次触发）

v3.4 变更：
- 新增 `_step_with_retry()` 每步自检重试机制（最多3次）
- 新增 `_set_input_vue_compat()` 兼容 Element UI 输入框（nativeInputValueSetter + 多种事件）
- 新增 `_check_field_value()` 支持按 placeholder 和 el-form-item label 两种查找方式
- 新增 `_check_form_errors()` 表单校验检查
- 新增 `_check_publish_success()` 发布后等待跳转+错误检测
- 修复售价/库存 placeholder 为空时的查找问题（改用 label 文本匹配）
- 修复城市 input placeholder 为"请选择"时的查找问题
- 自动发货保存后未变蓝 → 自动再点开关 + 重新保存（最多3次）
- 售罄上架保存后未变蓝 → 自动再点开关 + 重新确定（最多3次）
"""
import sys
import os
import time
import json
import asyncio
import urllib.request
sys.stdout.reconfigure(encoding='utf-8')
import websockets

# ============================================================
# 功能开关
# ============================================================
ENABLE_GALLERY_FALLBACK = True
ENABLE_GALLERY_FIRST_IMAGE_FALLBACK = True
ENABLE_IMAGE_BY_SHOP = False

EASY_SHOP_URL = "https://ed.weeeg.com"

# 自检重试配置
MAX_STEP_RETRY = 3
STEP_RETRY_DELAY = 1
MAX_PUBLISH_RETRY = 3


# ============================================================
# CDP 直连类
# ============================================================

def get_page_ws_endpoint(http_url="http://127.0.0.1:9222", url_filter="ed.weeeg.com"):
    resp = urllib.request.urlopen(f"{http_url}/json", timeout=5)
    pages = json.loads(resp.read())
    for p in pages:
        if p.get("webSocketDebuggerUrl"):
            if url_filter is None or url_filter in p.get("url", ""):
                return p["webSocketDebuggerUrl"]
    for p in pages:
        if p.get("webSocketDebuggerUrl"):
            return p["webSocketDebuggerUrl"]
    return None


class CDPPage:
    def __init__(self, ws_url: str):
        self.ws_url = ws_url
        self._ws = None
        self._msg_id = 0
        self._recv_buffer = asyncio.Queue()
        self._recv_task = None

    async def connect(self):
        self._ws = await websockets.connect(self.ws_url, max_size=2**24)
        self._recv_task = asyncio.create_task(self._background_recv())
        return self

    async def close(self):
        if self._recv_task:
            self._recv_task.cancel()
        if self._ws:
            await self._ws.close()

    async def _background_recv(self):
        try:
            while True:
                raw = await self._ws.recv()
                data = json.loads(raw)
                await self._recv_buffer.put(data)
        except (websockets.exceptions.ConnectionClosed, asyncio.CancelledError):
            pass

    async def _send(self, method: str, params: dict = None, timeout: float = 15) -> dict:
        self._msg_id += 1
        msg_id = self._msg_id
        cmd = {"id": msg_id, "method": method}
        if params:
            cmd["params"] = params
        await self._ws.send(json.dumps(cmd))
        deadline = time.time() + timeout
        while time.time() < deadline:
            remaining = deadline - time.time()
            if remaining <= 0:
                raise TimeoutError(f"CDP 超时: {method}")
            try:
                data = await asyncio.wait_for(self._recv_buffer.get(), timeout=max(0.1, remaining))
            except asyncio.TimeoutError:
                raise TimeoutError(f"CDP 超时: {method}")
            if data.get("id") == msg_id:
                return data

    async def evaluate(self, js_code: str, timeout: float = 15) -> any:
        code = js_code.strip()
        if code.startswith("() =>") or code.startswith("()=>"):
            if code.startswith("() =>"):
                code = code[5:].strip()
            else:
                code = code[4:].strip()
            if code.startswith("{"):
                code = f"(function(){code})()"
        result = await self._send("Runtime.evaluate", {
            "expression": code,
            "returnByValue": True,
            "replMode": True,
        }, timeout=timeout)
        exc = result.get("result", {}).get("exceptionDetails")
        if exc:
            print(f"  \u26a0\ufe0f JS 异常: {exc.get('text', '')} | {exc.get('exception', {}).get('description', '')[:100]}")
            return None
        return result.get("result", {}).get("result", {}).get("value")

    async def navigate(self, url: str, timeout: float = 15):
        return await self._send("Page.navigate", {"url": url}, timeout=timeout)

    async def screenshot(self, timeout: float = 15) -> str:
        for _ in range(50):
            try:
                self._recv_buffer.get_nowait()
            except asyncio.QueueEmpty:
                break
        result = await self._send("Page.captureScreenshot", {"format": "png"}, timeout=timeout)
        return result.get("result", {}).get("data", "")

    async def get_url(self) -> str:
        return await self.evaluate("window.location.href")

    async def click(self, selector: str) -> bool:
        return await self.evaluate(
            f"(function(){{var el=document.querySelector('{selector}');if(el){{el.click();return true}}return false}})()"
        )

    async def click_by_text(self, text: str) -> bool:
        return await self.evaluate(
            f"(function(){{var els=document.querySelectorAll('button,span,a,.el-button');for(var el of els){{if(el.innerText.includes('{text}')){{el.click();return true}}}}return false}})()"
        )

    async def fill_by_placeholder(self, placeholder: str, value: str) -> bool:
        return await self.evaluate(
            f"(function(){{var el=document.querySelector('input[placeholder*=\"{placeholder}\"]')||document.querySelector('textarea[placeholder*=\"{placeholder}\"]');if(el){{el.value=`{value}`;el.dispatchEvent(new Event('input',{{bubbles:true}}));return true}}return false}})()"
        )

    def sync(self, coro):
        return asyncio.run(coro)


# ============================================================
# 自检工具函数
# ============================================================

async def _check_field_value(page: CDPPage, label_text: str) -> bool:
    """检查输入框的值（先按 placeholder 找，再按 el-form-item label 找）"""
    val = await page.evaluate(f"""
(function() {{
    var el = document.querySelector('input[placeholder*="{label_text}"]') ||
             document.querySelector('textarea[placeholder*="{label_text}"]');
    if (!el) {{
        var items = document.querySelectorAll('.el-form-item');
        for (var item of items) {{
            var label = item.querySelector('.el-form-item__label');
            if (label && label.innerText.includes('{label_text}')) {{
                el = item.querySelector('input');
                if (el) break;
            }}
        }}
    }}
    if (!el) return '';
    var v = el.value || '';
    if (el.tagName === 'TEXTAREA') {{
        return v.replace(/\\s/g, '').substring(0, 10);
    }}
    return v;
}})()
""")
    return bool(val and val.strip())


async def _check_form_errors(page: CDPPage) -> list:
    """检查表单校验错误"""
    errors = await page.evaluate("""
(function() {
    var errs = document.querySelectorAll('.el-form-item__error, .el-form-item__error--inline');
    var msgs = [];
    for (var e of errs) {
        var t = e.innerText.trim();
        if (t) msgs.push(t);
    }
    var toasts = document.querySelectorAll('.el-message--error .el-message__content');
    for (var m of toasts) {
        var t = m.innerText.trim();
        if (t) msgs.push(t);
    }
    return JSON.stringify(msgs);
})()
""")
    if errors:
        return json.loads(errors)
    return []


async def _set_input_vue_compat(page: CDPPage, label_text: str, value: str) -> bool:
    """
    兼容 Element UI 的输入框设值方法
    先按 placeholder 找，再按 label 文本找
    使用 nativeInputValueSetter + 多种事件触发 Vue 响应式
    """
    result = await page.evaluate(f"""
(function() {{
    var inp = document.querySelector('input[placeholder*="{label_text}"]');
    if (!inp) {{
        var items = document.querySelectorAll('.el-form-item');
        for (var item of items) {{
            var label = item.querySelector('.el-form-item__label');
            if (label && label.innerText.includes('{label_text}')) {{
                inp = item.querySelector('input');
                if (inp) break;
            }}
        }}
    }}
    if (!inp) return 'no_input';
    try {{
        var nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        nativeSetter.call(inp, '{value}');
    }} catch(e) {{}}
    inp.value = '{value}';
    ['input', 'change', 'blur', 'keyup', 'keydown', 'keypress'].forEach(function(evt) {{
        inp.dispatchEvent(new Event(evt, {{ bubbles: true }}));
    }});
    try {{
        var inputEvent = new InputEvent('input', {{ bubbles: true, data: '{value}' }});
        inp.dispatchEvent(inputEvent);
    }} catch(e) {{}}
    try {{
        inp.dispatchEvent(new Event('change', {{ bubbles: true }}));
    }} catch(e) {{}}
    return inp.value;
}})()
""")
    return result == value


async def _step_with_retry(page: CDPPage, step_name: str,
                            do_fn, check_fn=None, max_retry=MAX_STEP_RETRY) -> bool:
    """带自检重试的步骤执行器"""
    for attempt in range(1, max_retry + 1):
        if attempt > 1:
            print(f"  \U0001f504 {step_name} 重试第{attempt}次...")
            await asyncio.sleep(STEP_RETRY_DELAY)

        ok = await do_fn()
        if not ok and attempt == 1:
            continue
        if not ok:
            continue

        if check_fn:
            passed = await check_fn()
            if passed:
                print(f"\u2705 {step_name}")
                return True
            print(f"  \u26a0\ufe0f {step_name} 自检未通过")
        else:
            print(f"\u2705 {step_name}")
            return True

    print(f"\u274c {step_name} 失败（重试{max_retry}次）")
    return False


async def _check_publish_success(page: CDPPage, timeout_sec: int = 30) -> bool:
    """检查发布是否成功（URL 是否跳转到 product_list）"""
    for i in range(timeout_sec):
        url = await page.get_url()
        if "product_list" in url:
            return True
        errors = await _check_form_errors(page)
        for err in errors:
            if "\u4e0d\u80fd\u4e3a\u7a7a" in err:
                print(f"  \u26a0\ufe0f 表单校验错误: {err}")
                return False
        await asyncio.sleep(1)
    return False


# ============================================================
# 主发布函数
# ============================================================

async def _publish_async(config: dict) -> bool:
    shop = config['shop']
    title = config['title']
    desc = config['desc']
    image_file = config['image_file']
    image_keyword = config['image_keyword']
    pan_text = config['pan_text']
    pan_code = config['pan_code']
    image_dir = config.get('image_dir', r"图片资料目录")

    if shop == 1:
        shop_name = "\u5929\u7a7a\u7684\u6d41\u661flyh"
        stock = "9999"
        enable_two_person_discount = True
    elif shop == 2:
        shop_name = "\u6797\u9171\u8d44\u6e90\u5e93"
        stock = "1"
        enable_two_person_discount = False
    else:
        print(f"\u274c \u65e0\u6548\u5e97\u94fa\u53f7: {shop}")
        return False

    print(f"\U0001f3ea \u5f53\u524d\u5e97\u94fa: {shop_name} ({'1\u53f7\u5e97' if shop == 1 else '2\u53f7\u5e97'})")

    image_path = f"{image_dir}\\{image_file}" if image_file else ""

    # ========== CDP 连接 ==========
    ws_url = get_page_ws_endpoint(url_filter="ed.weeeg.com")
    if not ws_url:
        print("\u274c \u672a\u627e\u5230\u6613\u5e97\u9875\u9762\uff0c\u8bf7\u786e\u4fdd Edge \u5df2\u6253\u5f00\u6613\u5e97\u540e\u53f0")
        return False

    print("\U0001f517 CDP \u76f4\u8fde\u4e2d...")
    page = CDPPage(ws_url)
    await page.connect()

    url = await page.get_url()
    print(f"\u5f53\u524dURL: {url}")

    # ======================================================
    # 第一步：发布商品
    # ======================================================
    print("=" * 40)
    print("\u7b2c\u4e00\u6b65\uff1a\u53d1\u5e03\u5546\u54c1")
    print("=" * 40)

    if "add_product" not in url:
        print("\u5bfc\u822a\u5230\u53d1\u5e03\u9875\u9762...")
        await page.navigate(f"{EASY_SHOP_URL}/ekadmin/product/add_product")
        await asyncio.sleep(3)

    # --- 1. 标题 ---
    async def _do_title():
        r = await page.fill_by_placeholder("\u5b9d\u8d1d\u6807\u9898", title)
        return bool(r)
    async def _check_title():
        return await _check_field_value(page, "\u5b9d\u8d1d\u6807\u9898")
    if not await _step_with_retry(page, "\u6807\u9898", _do_title, _check_title):
        await page.close()
        return False

    # --- 2. 图片 ---
    if image_file:
        async def _do_image():
            await page.evaluate("""(function() {
                var el = document.querySelector('.upLoad');
                if (el) el.click();
            })()""")
            await asyncio.sleep(3)

            found = await page.evaluate(f"""(function() {{
                var keyword = '{image_keyword}'.toLowerCase();
                var pics = document.querySelectorAll('.pictrueList_pic');
                for (var pic of pics) {{
                    var p = pic.querySelector('p');
                    if (p && p.innerText.trim().toLowerCase().includes(keyword)) {{
                        var img = pic.querySelector('img');
                        if (img) {{ img.click(); return true; }}
                    }}
                }}
                return false;
            }})()""")
            if found:
                await asyncio.sleep(1)
                await page.evaluate("""(function() {
                    var btns = document.querySelectorAll('button');
                    for (var b of btns) {
                        if (b.innerText.includes('\u4f7f\u7528\u9009\u4e2d\u56fe\u7247')) { b.click(); return; }
                    }
                })()""")
                await asyncio.sleep(2)
                return True

            print(f"  \u26a0\ufe0f \u56fe\u5e93\u672a\u627e\u5230{image_keyword}\uff0c\u9700\u8981\u4e0a\u4f20")
            if ENABLE_GALLERY_FALLBACK:
                await page.click_by_text("\u4e0a\u4f20\u56fe\u7247")
                await asyncio.sleep(3)

            if image_path and os.path.exists(image_path):
                print(f"  \U0001f4c1 \u51c6\u5907\u4e0a\u4f20: {image_path}")
                await asyncio.sleep(2)

                doc_result = await page._send("DOM.getDocument", {"depth": 0})
                doc_node_id = doc_result.get("result", {}).get("root", {}).get("nodeId")
                if doc_node_id:
                    q_result = await page._send("DOM.querySelector", {
                        "nodeId": doc_node_id,
                        "selector": "input[type=\"file\"]"
                    })
                    file_node_id = q_result.get("result", {}).get("nodeId")
                    if file_node_id and file_node_id > 0:
                        await page._send("DOM.setFileInputFiles", {
                            "files": [image_path],
                            "nodeId": file_node_id
                        })
                        print("  \u2705 \u6587\u4ef6\u5df2\u901a\u8fc7 CDP \u8bbe\u7f6e")
                    else:
                        return False
                else:
                    return False

                await asyncio.sleep(8)

                await page.evaluate("""(function() {
                    var allBtns = document.querySelectorAll('button');
                    for (var b of allBtns) {
                        var t = b.innerText.trim();
                        if (t === '\u786e\u5b9a' || t === '\u786e \u5b9a') { b.click(); return; }
                    }
                })()""")
                await asyncio.sleep(3)
                await page.evaluate("""(function() {
                    document.querySelectorAll('.el-dialog__wrapper, .v-modal').forEach(function(d) {
                        if (d.style) d.style.display = 'none';
                    });
                })()""")
                await asyncio.sleep(2)

                await page.evaluate("""(function() {
                    var el = document.querySelector('.upLoad');
                    if (el) el.click();
                })()""")
                await asyncio.sleep(3)

                await page.evaluate("""(function() {
                    var pics = document.querySelectorAll('.pictrueList_pic');
                    if (pics.length > 0) {
                        var img = pics[0].querySelector('img');
                        if (img) img.click();
                    }
                })()""")
                await asyncio.sleep(1)
                await page.evaluate("""(function() {
                    var btns = document.querySelectorAll('button');
                    for (var b of btns) {
                        if (b.innerText.includes('\u4f7f\u7528\u9009\u4e2d\u56fe\u7247')) { b.click(); return; }
                    }
                })()""")
                await asyncio.sleep(2)
                return True
            return False

        async def _check_image():
            has_img = await page.evaluate("""(function() {
                var upLoad = document.querySelector('.upLoad');
                if (!upLoad) return false;
                var parent = upLoad.parentElement;
                if (parent) {
                    var imgs = parent.querySelectorAll('img');
                    return imgs.length > 0;
                }
                return false;
            })()""")
            return bool(has_img)

        if not await _step_with_retry(page, "\u56fe\u7247", _do_image, _check_image, max_retry=2):
            await page.close()
            return False
    else:
        print("\u26a0\ufe0f \u65e0\u56fe\u7247\u6587\u4ef6\uff0c\u8df3\u8fc7\u56fe\u7247\u9009\u62e9")

    # --- 3. 描述 ---
    async def _do_desc():
        return bool(await page.fill_by_placeholder("\u5b9d\u8d1d\u63cf\u8ff0", desc))
    async def _check_desc():
        return await _check_field_value(page, "\u5b9d\u8d1d\u63cf\u8ff0")
    if not await _step_with_retry(page, "\u63cf\u8ff0", _do_desc, _check_desc):
        await page.close()
        return False

    # --- 4. 城市 ---
    async def _do_city():
        await page.evaluate("""(function() {
            var inputs = document.querySelectorAll('input');
            for (var inp of inputs) {
                if (inp.placeholder && inp.placeholder.includes('\u5b9a\u4f4d\u57ce\u5e02')) {
                    inp.click(); return;
                }
            }
        })()""")
        await asyncio.sleep(2)
        for city in ["\u5e7f\u4e1c\u7701", "\u5e7f\u5dde\u5e02", "\u6d77\u73e0\u533a"]:
            await page.evaluate(f"""(function() {{
                var menus = document.querySelectorAll('.el-cascader-menu');
                for (var m of menus) {{
                    var nodes = m.querySelectorAll('.el-cascader-node');
                    for (var n of nodes) {{
                        var label = n.querySelector('.el-cascader-node__label');
                        if (label && label.innerText.trim() === '{city}') {{ n.click(); return true; }}
                    }}
                }}
                return false;
            }})()""")
            await asyncio.sleep(1)
        return True
    async def _check_city():
        val = await page.evaluate("""(function() {
            var items = document.querySelectorAll('.el-form-item');
            for (var item of items) {
                if (item.innerText.includes('\u5b9a\u4f4d\u57ce\u5e02')) {
                    var inp = item.querySelector('input');
                    if (inp && inp.value && inp.value.length > 0) return inp.value;
                    return '';
                }
            }
            return '';
        })()""")
        return bool(val)
    if not await _step_with_retry(page, "\u57ce\u5e02", _do_city, _check_city):
        await page.close()
        return False

    # --- 5. 店铺 ---
    async def _do_shop():
        await page.evaluate("""(function() {
            var items = document.querySelectorAll('.el-form-item');
            for (var item of items) {
                if (item.innerText.includes('\u6240\u5c5e\u5e97\u94fa')) {
                    var inp = item.querySelector('input');
                    if (inp) { inp.click(); return; }
                }
            }
        })()""")
        await asyncio.sleep(2)
        await page.evaluate(f"""(function() {{
            var items = document.querySelectorAll('.el-select-dropdown__item');
            for (var item of items) {{
                if (item.innerText.includes('{shop_name}')) {{
                    item.click(); return;
                }}
            }}
        }})()""")
        await asyncio.sleep(1)
        return True
    async def _check_shop():
        val = await page.evaluate(f"""(function() {{
            var items = document.querySelectorAll('.el-form-item');
            for (var item of items) {{
                if (item.innerText.includes('\u6240\u5c5e\u5e97\u94fa')) {{
                    var spans = item.querySelectorAll('span');
                    for (var s of spans) {{
                        if (s.innerText.includes('{shop_name}')) return true;
                    }}
                }}
            }}
            return false;
        }})()""")
        return bool(val)
    if not await _step_with_retry(page, f"\u5e97\u94fa({shop_name})", _do_shop, _check_shop):
        await page.close()
        return False

    # --- 6. 单规格 ---
    async def _do_spec():
        await page.evaluate("""(function() {
            var radios = document.querySelectorAll('.el-radio');
            for (var r of radios) {
                if (r.innerText.includes('\u5355\u89c4\u683c')) { r.click(); return; }
            }
        })()""")
        await asyncio.sleep(0.5)
        return True
    async def _check_spec():
        checked = await page.evaluate("""(function() {
            var radios = document.querySelectorAll('.el-radio');
            for (var r of radios) {
                if (r.innerText.includes('\u5355\u89c4\u683c')) {
                    return r.classList.contains('is-checked') || !!r.querySelector('.is-checked');
                }
            }
            return false;
        })()""")
        return bool(checked)
    if not await _step_with_retry(page, "\u5355\u89c4\u683c", _do_spec, _check_spec):
        await page.close()
        return False

    # --- 7. 售价 ---
    async def _do_price():
        return await _set_input_vue_compat(page, "\u552e\u4ef7", "1")
    async def _check_price():
        return await _check_field_value(page, "\u552e\u4ef7")
    if not await _step_with_retry(page, "\u552e\u4ef7(1\u5143)", _do_price, _check_price):
        await page.close()
        return False

    # --- 8. 库存 ---
    async def _do_stock():
        return await _set_input_vue_compat(page, "\u5e93\u5b58", stock)
    async def _check_stock():
        return await _check_field_value(page, "\u5e93\u5b58")
    if not await _step_with_retry(page, f"\u5e93\u5b58({stock})", _do_stock, _check_stock):
        await page.close()
        return False

    # --- 9. 包邮 ---
    async def _do_shipping():
        await page.evaluate("""(function() {
            var radios = document.querySelectorAll('.el-radio');
            for (var r of radios) {
                if (r.innerText.includes('\u5305\u90ae')) { r.click(); return; }
            }
        })()""")
        await asyncio.sleep(0.5)
        return True
    async def _check_shipping():
        checked = await page.evaluate("""(function() {
            var radios = document.querySelectorAll('.el-radio');
            for (var r of radios) {
                if (r.innerText.includes('\u5305\u90ae')) {
                    return r.classList.contains('is-checked') || !!r.querySelector('.is-checked');
                }
            }
            return false;
        })()""")
        return bool(checked)
    if not await _step_with_retry(page, "\u5305\u90ae", _do_shipping, _check_shipping):
        await page.close()
        return False

    # --- 10. 发布前最终校验 ---
    print("\u23f3 \u6700\u7ec8\u8868\u5355\u6821\u9a8c...")
    final_errors = await _check_form_errors(page)
    if final_errors:
        print(f"  \u26a0\ufe0f \u8868\u5355\u6821\u9a8c\u672a\u901a\u8fc7: {final_errors}")
        for err in final_errors:
            if "\u552e\u4ef7" in err:
                print("  \U0001f504 \u91cd\u8bd5\u552e\u4ef7...")
                await _set_input_vue_compat(page, "\u552e\u4ef7", "1")
                await asyncio.sleep(1)
            if "\u5e93\u5b58" in err:
                print("  \U0001f504 \u91cd\u8bd5\u5e93\u5b58...")
                await _set_input_vue_compat(page, "\u5e93\u5b58", stock)
                await asyncio.sleep(1)
        final_errors2 = await _check_form_errors(page)
        if final_errors2:
            print(f"  \u274c \u4ecd\u6709\u6821\u9a8c\u9519\u8bef: {final_errors2}")
            await page.close()
            return False

    print("\u2705 \u6240\u6709\u5b57\u6bb5\u5df2\u586b\uff0c\u51c6\u5907\u53d1\u5e03...")
    await asyncio.sleep(2)

    # --- 11. 点击发布 ---
    for pub_attempt in range(MAX_PUBLISH_RETRY):
        if pub_attempt > 0:
            print(f"  \U0001f504 \u53d1\u5e03\u91cd\u8bd5\u7b2c{pub_attempt}\u6b21...")
            await asyncio.sleep(2)

        await page.evaluate("""(function() {
            var sub = document.querySelector('.submission');
            if (sub) { sub.click(); return; }
            var btns = document.querySelectorAll('button');
            for (var b of btns) {
                if (b.innerText.trim() === '\u53d1\u5e03') { b.click(); return; }
            }
        })()""")
        print(f"  \U0001f4e4 \u70b9\u51fb\u53d1\u5e03\u6309\u94ae (\u7b2c{pub_attempt+1}\u6b21)")

        success = await _check_publish_success(page, timeout_sec=20)
        if success:
            print("\U0001f389 \u53d1\u5e03\u6210\u529f\uff01")
            break

        errors = await _check_form_errors(page)
        if errors:
            print(f"  \u26a0\ufe0f \u53d1\u5e03\u5931\u8d25\uff0c\u9519\u8bef: {errors}")
            if any("\u552e\u4ef7" in e for e in errors):
                print("  \U0001f504 \u91cd\u65b0\u586b\u5199\u552e\u4ef7...")
                await _set_input_vue_compat(page, "\u552e\u4ef7", "1")
                await asyncio.sleep(1)
    else:
        print(f"\u274c \u53d1\u5e03\u5931\u8d25\uff08\u5df2\u91cd\u8bd5{MAX_PUBLISH_RETRY}\u6b21\uff09")
        await page.close()
        return False

    # ======================================================
    # 第二步：配置自动发货+售罄上架（v3.5 — 标题匹配行索引 + 弹窗Vue等待）
    # ======================================================
    print("=" * 40)
    print("第二步：配置自动发货+售罄上架")
    print("=" * 40)

    url_now = await page.get_url()
    if "product_list" not in url_now:
        await page.navigate(f"{EASY_SHOP_URL}/ekadmin/product/product_list")
        await asyncio.sleep(5)

    # 等待表格加载：重试最多 5 次
    rows = 0
    for retry in range(5):
        await page.evaluate("""(function() {
            var w = document.querySelector('.el-table__body-wrapper');
            if (w) w.scrollLeft = 9999;
        })()""")
        await asyncio.sleep(2)
        rows = await page.evaluate("""(function() {
            return document.querySelectorAll('.el-table__body-wrapper tbody tr').length;
        })()""")
        print(f"表格行数: {rows} (第{retry+1}次)")
        if rows and rows > 0:
            break

    if rows and rows > 0:
        # ---- v3.5: 通过标题匹配找到当前商品所在的行索引 ----
        target_row_index = await page.evaluate(f"""(function() {{
            var trs = document.querySelectorAll('.el-table__body-wrapper tbody tr');
            for (var i = 0; i < trs.length; i++) {{
                var tds = trs[i].querySelectorAll('td');
                if (tds.length >= 6) {{
                    var cellText = tds[5].innerText.trim();
                    if (cellText.includes('{title[:20]}')) {{
                        return i;
                    }}
                }}
            }}
            return 0;
        }})()""")
        print(f"  目标行索引: {target_row_index} (0-based)")

        # --- 自动发货 ---
        print("开启自动发货...")
        await page.evaluate(f"""(function() {{
            var trs = document.querySelectorAll('.el-table__body-wrapper tbody tr');
            if (trs.length <= {target_row_index}) return;
            var tr = trs[{target_row_index}];
            var tds = tr.querySelectorAll('td');
            if (tds.length < 11) return;
            var sw = tds[10].querySelector('.el-switch');
            if (sw) {{
                if (sw.classList.contains('is-checked')) return;
                var core = sw.querySelector('.el-switch__core') || sw;
                core.click();
            }}
        }})()""")
        await asyncio.sleep(3)

        # ---- v3.5: 等待弹窗Vue渲染完成（最多等15秒） ----
        print("等待弹窗 Vue 渲染...")
        dialog_ready = False
        for wait_i in range(10):
            await asyncio.sleep(1.5)
            dialog_body_len = await page.evaluate("""(function() {
                var dialog = document.querySelector('.addproduct-dialog') || document.querySelector('.el-dialog');
                if (!dialog) return -1;
                var body = dialog.querySelector('.el-dialog__body');
                if (!body) return -2;
                return body.innerHTML.length;
            })()""")
            if dialog_body_len and dialog_body_len > 50:
                dialog_ready = True
                print(f"  ✅ 弹窗 body 已渲染 ({dialog_body_len} chars, 第{wait_i+1}次)")
                break
            print(f"  ⏳ 弹窗渲染中... body长度={dialog_body_len} (第{wait_i+1}次)")

        if dialog_ready:
            print("✅ 自动发货弹窗已打开")

            await page.evaluate(f"""(function() {{
                var ta = document.querySelector('.addproduct-dialog textarea, .el-dialog__body textarea');
                if (ta) {{
                    ta.value = `{pan_text}`;
                    ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            }})()""")
            print("✅ 已填入网盘分享文本")
            await asyncio.sleep(1)

            await page.evaluate("""(function() {
                var labels = document.querySelectorAll('.addproduct-dialog label, .el-dialog__body label, span, .el-collapse-item__header');
                for (var l of labels) {
                    if (l.innerText.includes('高级配置')) { l.click(); return; }
                }
            })()""")
            print("✅ 已展开高级配置")
            await asyncio.sleep(2)

            await page.evaluate(f"""(function() {{
                var inputs = document.querySelectorAll('.addproduct-dialog input, .el-dialog__body input');
                for (var inp of inputs) {{
                    if (inp.placeholder && (inp.placeholder.includes('提取码') || inp.placeholder.includes('密码'))) {{
                        inp.value = '{pan_code}';
                        inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        return;
                    }}
                }}
            }})()""")
            print("✅ 已填入提取码")
            await asyncio.sleep(1)

            await page.evaluate("""(function() {
                var cbs = document.querySelectorAll('.el-checkbox');
                for (var cb of cbs) {
                    var label = cb.querySelector('.el-checkbox__label');
                    if (label && label.innerText.includes('发货声明')) {
                        var inp = cb.querySelector('input');
                        if (inp && !inp.checked) { cb.click(); }
                        return;
                    }
                }
            })()""")
            print("✅ 已勾选发货声明")
            await asyncio.sleep(1)

            await page.evaluate("""(function() {
                var btns = document.querySelectorAll('.addproduct-dialog button, .el-dialog__footer button');
                for (var b of btns) {
                    if (b.innerText.includes('保存')) { b.click(); return; }
                }
            })()""")
            print("✅ 已点击保存")
            await asyncio.sleep(5)

            await page.evaluate("""(function() {
                document.querySelectorAll('.addproduct-dialog, .el-dialog__wrapper').forEach(function(d) {
                    if (d.style.display !== 'none') {
                        var closeBtn = d.querySelector('.el-dialog__headerbtn, .el-dialog__close');
                        if (closeBtn) closeBtn.click();
                    }
                });
            })()""")
            await asyncio.sleep(2)

            for retry_i in range(3):
                sw_checked = await page.evaluate(f"""(function() {{
                    var trs = document.querySelectorAll('.el-table__body-wrapper tbody tr');
                    if (trs.length <= {target_row_index}) return 'no_tr';
                    var tr = trs[{target_row_index}];
                    var tds = tr.querySelectorAll('td');
                    if (tds.length < 11) return 'no_td';
                    var sw = tds[10].querySelector('.el-switch');
                    if (!sw) return 'no_sw';
                    if (sw.classList.contains('is-checked')) return 'checked';
                    return 'unchecked';
                }})()""")
                if sw_checked == 'checked':
                    print(f"  ✅ 自动发货开关已开启（第{retry_i+1}次检查）")
                    break
                print(f"  🔄 保存后自动发货未变蓝，第{retry_i+1}次重试（再点开关+重新保存）")
                await page.evaluate(f"""(function() {{
                    var trs = document.querySelectorAll('.el-table__body-wrapper tbody tr');
                    if (trs.length <= {target_row_index}) return;
                    var tr = trs[{target_row_index}];
                    var tds = tr.querySelectorAll('td');
                    if (tds.length < 11) return;
                    var sw = tds[10].querySelector('.el-switch');
                    if (sw) {{
                        var core = sw.querySelector('.el-switch__core') || sw;
                        core.click();
                    }}
                }})()""")
                await asyncio.sleep(3)
                await page.evaluate("""(function() {
                    var btns = document.querySelectorAll('.addproduct-dialog button, .el-dialog__footer button, .el-dialog__body button');
                    for (var b of btns) {
                        if (b.innerText.includes('保存')) { b.click(); return; }
                    }
                })()""")
                print(f"  💮 重新保存")
                await asyncio.sleep(5)
        else:
            print("⚠️ 自动发货弹窗未打开")

        # --- 售罄上架 ---
        print("开启售罄上架...")
        await page.evaluate(f"""(function() {{
            var trs = document.querySelectorAll('.el-table__body-wrapper tbody tr');
            if (trs.length <= {target_row_index}) return;
            var tr = trs[{target_row_index}];
            var tds = tr.querySelectorAll('td');
            if (tds.length < 12) return;
            var sw = tds[11].querySelector('.el-switch');
            if (sw) {{
                if (sw.classList.contains('is-checked')) return;
                var core = sw.querySelector('.el-switch__core') || sw;
                core.click();
            }}
        }})()""")
        await asyncio.sleep(3)

        await page.evaluate("""(function() {
            var dialogs = document.querySelectorAll('.el-dialog__wrapper');
            for (var d of dialogs) {
                var style = window.getComputedStyle(d);
                if (style.display !== 'none' && style.visibility !== 'hidden') {
                    var cb = d.querySelector('.el-checkbox input');
                    if (cb && !cb.checked) { cb.click(); }
                    var btns = d.querySelectorAll('button');
                    for (var b of btns) {
                        if (b.innerText.includes('确定')) { b.click(); return; }
                    }
                }
            }
        })()""")
        await asyncio.sleep(3)

        for retry_i in range(3):
            soldout_checked = await page.evaluate(f"""(function() {{
                var trs = document.querySelectorAll('.el-table__body-wrapper tbody tr');
                if (trs.length <= {target_row_index}) return 'no_tr';
                var tr = trs[{target_row_index}];
                var tds = tr.querySelectorAll('td');
                if (tds.length < 12) return 'no_td';
                var sw = tds[11].querySelector('.el-switch');
                if (!sw) return 'no_sw';
                if (sw.classList.contains('is-checked')) return 'checked';
                return 'unchecked';
            }})()""")
            if soldout_checked == 'checked':
                print(f"  ✅ 售罄上架已开启（第{retry_i+1}次检查）")
                break
            print(f"  🔄 售罄上架未变蓝，第{retry_i+1}次重试（再点开关+确定）...")
            await page.evaluate(f"""(function() {{
                var trs = document.querySelectorAll('.el-table__body-wrapper tbody tr');
                if (trs.length <= {target_row_index}) return;
                var tr = trs[{target_row_index}];
                var tds = tr.querySelectorAll('td');
                var sw = tds[11].querySelector('.el-switch');
                if (sw) {{
                    var core = sw.querySelector('.el-switch__core') || sw;
                    core.click();
                }}
            }})()""")
            await asyncio.sleep(3)
            await page.evaluate("""(function() {
                var dialogs = document.querySelectorAll('.el-dialog__wrapper');
                for (var d of dialogs) {
                    var style = window.getComputedStyle(d);
                    if (style.display !== 'none' && style.visibility !== 'hidden') {
                        var btns = d.querySelectorAll('button');
                        for (var b of btns) {
                            if (b.innerText.includes('确定')) { b.click(); return; }
                        }
                    }
                }
            })()""")
            await asyncio.sleep(3)

        # --- 2人小刀 ---
        if enable_two_person_discount:
            print("开启2人小刀...")
            await page.evaluate(f"""(function() {{
                var trs = document.querySelectorAll('.el-table__body-wrapper tbody tr');
                if (trs.length <= {target_row_index}) return;
                var tr = trs[{target_row_index}];
                var tds = tr.querySelectorAll('td');
                if (tds.length < 13) return;
                var sw = tds[12].querySelector('.el-switch');
                if (sw) {{
                    if (sw.classList.contains('is-checked')) return;
                    var core = sw.querySelector('.el-switch__core') || sw;
                    core.click();
                }}
            }})()""")
            await asyncio.sleep(3)

            knife_dialog = await page.evaluate("""(function() {
                var dialogs = document.querySelectorAll('.el-dialog__wrapper');
                for (var d of dialogs) {
                    var style = window.getComputedStyle(d);
                    if (style.display !== 'none' && style.visibility !== 'hidden') {
                        var inp = d.querySelector('input');
                        if (inp) return true;
                    }
                }
                return false;
            })()""")

            if knife_dialog:
                await page.evaluate("""(function() {
                    var dialogs = document.querySelectorAll('.el-dialog__wrapper');
                    for (var d of dialogs) {
                        var style = window.getComputedStyle(d);
                        if (style.display !== 'none' && style.visibility !== 'hidden') {
                            var inp = d.querySelector('input');
                            if (inp) {
                                inp.value = '0.7';
                                inp.dispatchEvent(new Event('input', { bubbles: true }));
                            }
                            var btns = d.querySelectorAll('button');
                            for (var b of btns) {
                                if (b.innerText.includes('确认设置')) { b.click(); return; }
                            }
                        }
                    }
                })()""")
                await asyncio.sleep(3)
                print("✅ 2人小刀已开启 (0.7)")
            else:
                print("⚠️ 2人小刀弹窗未打开")

        # 最终验证（v3.5：使用 target_row_index）
        await page.evaluate("location.reload()")
        await asyncio.sleep(5)
        await page.evaluate("""(function() {
            var w = document.querySelector('.el-table__body-wrapper');
            if (w) w.scrollLeft = 9999;
        })()""")
        await asyncio.sleep(2)

        status = await page.evaluate(f"""(function() {{
            var trs = document.querySelectorAll('.el-table__body-wrapper tbody tr');
            if (trs.length <= {target_row_index}) return ['未知','未知','未知'];
            var tr = trs[{target_row_index}];
            var tds = tr.querySelectorAll('td');
            if (tds.length < 13) return ['未知','未知','未知'];
            var d_sw = tds[10].querySelector('.el-switch');
            var s_sw = tds[11].querySelector('.el-switch');
            var k_sw = tds[12].querySelector('.el-switch');
            return [
                d_sw && d_sw.classList.contains('is-checked') ? '✅开启' : '❌关闭',
                s_sw && s_sw.classList.contains('is-checked') ? '✅开启' : '❌关闭',
                k_sw && k_sw.classList.contains('is-checked') ? '✅开启' : '❌关闭',
            ];
        }})()""")
        print(f"✔ 配置完成: 自动发货={status[0]}, 售罄上架={status[1]}, 2人小刀={status[2]}")
    else:
        print("⚠️ 表格为空，无法配置")
    await page.close()
    print("\U0001f389 \u5168\u90e8\u5b8c\u6210\uff01")
    return True


# ============================================================
# 同步包装器
# ============================================================

def publish_product(config: dict) -> bool:
    return asyncio.run(_publish_async(config))


# ============================================================
# 自测入口
# ============================================================
if __name__ == "__main__":
    ws_url = get_page_ws_endpoint(url_filter="ed.weeeg.com")
    if ws_url:
        print("\u2705 CDP \u8fde\u63a5\u6d4b\u8bd5\u901a\u8fc7")
    else:
        print("\u274c \u672a\u627e\u5230\u6613\u5e97\u9875\u9762")
