"""
完整的发布+配置一体脚本（1号店/2号店通用）
发布成功后立即跳转到商品管理页配置自动发货+售罄上架

=== 使用说明 ===
每次上架新商品，只需修改下方的「商品配置区」即可：
  1. 先设置 SHOP（1或2），后续变量自动匹配
  2. 改 TITLE / DESC / IMAGE_FILE / IMAGE_KEYWORD / PAN_TEXT / PAN_CODE
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import time

from playwright.sync_api import sync_playwright

# ============================================================
# ⭐ 商品配置 — 爱听书纯净版
SHOP = 2

TITLE = "爱听书纯净版"

DESC = """是一款免费的安卓端听书软件，主要面向小说爱好者、通勤人群和视力敏感用户。软件通过语音合成技术，将文字内容转化为音频，帮助用户在驾车、运动或休息时“阅读”书籍
网盘发货，一经售出除链接失效外不退不换"""

IMAGE_FILE = "爱听书.jpg"          # 图片文件名
IMAGE_KEYWORD = "爱听书"             # 图库搜索关键字

PAN_TEXT = """通过网盘分享的文件：爱听书_2.6.5(265)-纯净版.apk
链接: https://pan.baidu.com/s/1YPUYfNbxtCxB_ibHmI2pVQ 提取码: dede
dede"""
PAN_CODE = "dede"

# ============================================================
# 以下脚本逻辑 — 不需要改
# ============================================================

# === 根据店铺自动匹配参数 ===
if SHOP == 1:
    SHOP_NAME = "一号店铺名"
    STOCK = "9999"
    ENABLE_TWO_PERSON_DISCOUNT = True  # 1号店需要2人小刀
elif SHOP == 2:
    SHOP_NAME = "二号店铺名"
    STOCK = "1"
    ENABLE_TWO_PERSON_DISCOUNT = False  # 2号店不需要
else:
    raise ValueError(f"SHOP 只能为 1 或 2，当前: {SHOP}")

print(f"🏪 当前店铺: {SHOP_NAME} ({'1号店' if SHOP == 1 else '2号店'})")

IMAGE_DIR = r"图片资料目录"

IMAGE_PATH = f"{IMAGE_DIR}\\{IMAGE_FILE}"

p = sync_playwright().start()
browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
page = browser.contexts[0].pages[0]
page.bring_to_front()
time.sleep(2)

print(f"当前URL: {page.url}")

# ======================================================
# 第一步：发布商品
# ======================================================
print("=" * 40)
print("第一步：发布商品")
print("=" * 40)

page.goto("https://ed.weeeg.com/ekadmin/product/add_product", wait_until="domcontentloaded")
time.sleep(5)

# 1. 标题
page.locator('input[placeholder*="宝贝标题"]').first.fill(TITLE)
time.sleep(0.5)
print("✅ 标题已填")

# 2. 图库选图
page.locator('.upLoad').first.click(force=True)
time.sleep(3)

found = page.evaluate(f"""() => {{
    var keyword = '{IMAGE_KEYWORD}'.toLowerCase();
    var pics = document.querySelectorAll('.pictrueList_pic');
    for (var pic of pics) {{
        var p = pic.querySelector('p');
        if (p && p.innerText.trim().toLowerCase().includes(keyword)) {{
            var img = pic.querySelector('img');
            if (img) {{ img.click(); return true; }}
        }}
    }}
    return false;
}}""")

if found:
    time.sleep(1)
    page.evaluate("""() => {
        var btns = document.querySelectorAll('button');
        for (var b of btns) {
            if (b.innerText.includes('使用选中图片')) { b.click(); return; }
        }
    }""")
    time.sleep(2)
    print("✅ 图片已选")
else:
    print(f"⚠️ 图库未找到{IMAGE_KEYWORD}，需要上传")
    page.locator('button:has-text("上传图片")').first.click()
    time.sleep(3)

    with page.expect_file_chooser() as fc_info:
        page.locator('.el-upload--picture-card, .el-upload').first.click(force=True)
        time.sleep(2)
    fc_info.value.set_files(IMAGE_PATH)
    print("✅ 文件已选择")
    time.sleep(8)

    # 点击上传弹窗中的"确 定"按钮
    clicked = page.evaluate("""() => {
        var dialogs = document.querySelectorAll('.el-dialog__wrapper');
        var visibleDialogs = [];
        for (var d of dialogs) {
            if (d.style.display !== 'none' && d.offsetParent !== null) {
                visibleDialogs.push(d);
            }
        }
        var target = visibleDialogs[visibleDialogs.length - 1];
        if (target) {
            var btns = target.querySelectorAll('button');
            for (var b of btns) {
                if (b.innerText.trim() === '确定' || b.innerText.trim() === '确 定') {
                    b.click(); return 'clicked';
                }
            }
        }
        var allBtns = document.querySelectorAll('button');
        for (var b of allBtns) {
            var t = b.innerText.trim();
            if (t === '确定' || t === '确 定') {
                b.click(); return 'clicked_global';
            }
        }
        return 'not_found';
    }""")
    print(f"上传弹窗确定按钮: {clicked}")
    time.sleep(3)

    # 强制关闭所有弹窗（图库弹窗可能还开着遮挡）
    page.evaluate("""() => {
        document.querySelectorAll('.el-dialog__wrapper, .el-dialog, .v-modal').forEach(d => {
            if (d.style.display !== 'none' || d.offsetParent !== null) {
                if (d.style) d.style.display = 'none';
            }
        });
        document.querySelectorAll('.el-dialog__headerbtn, .el-dialog__close, .el-icon-close').forEach(b => {
            b.click();
        });
    }""")
    time.sleep(2)

    # 重新打开图库
    page.locator('.upLoad').first.click(force=True)
    time.sleep(3)

    # 模糊匹配被截断的文件名
    found2 = page.evaluate(f"""() => {{
        var keyword = '{IMAGE_KEYWORD}'.toLowerCase();
        var pics = document.querySelectorAll('.pictrueList_pic');
        for (var pic of pics) {{
            var p = pic.querySelector('p');
            if (p) {{
                var name = p.innerText.trim().toLowerCase();
                if (name.includes(keyword)) {{
                    var img = pic.querySelector('img');
                    if (img) {{ img.click(); return true; }}
                }}
            }}
        }}
        return false;
    }}""")

    if found2:
        time.sleep(1)
        page.evaluate("""() => {
            var btns = document.querySelectorAll('button');
            for (var b of btns) {
                if (b.innerText.includes('使用选中图片')) { b.click(); return; }
            }
        }""")
        time.sleep(2)
        print("✅ 上传并选中图片")
    else:
        print(f"⚠️ 上传后仍未找到{IMAGE_KEYWORD}图片，尝试直接点第一张图...")
        page.evaluate("""() => {
            var pics = document.querySelectorAll('.pictrueList_pic');
            if (pics.length > 0) {
                var img = pics[0].querySelector('img');
                if (img) { img.click(); return true; }
            }
            return false;
        }""")
        time.sleep(1)
        page.evaluate("""() => {
            var btns = document.querySelectorAll('button');
            for (var b of btns) {
                if (b.innerText.includes('使用选中图片')) { b.click(); return; }
            }
        }""")
        time.sleep(2)
        print("✅ 已选第一张图（兜底策略）")

# 3. 描述
page.locator('textarea[placeholder*="宝贝描述"]').first.fill(DESC)
time.sleep(0.5)
print("✅ 描述已填")

# 4. 城市
page.locator('.el-form-item').filter(has_text="定位城市").locator('.el-cascader input').first.click()
time.sleep(2)
for city in ["省份名", "城市名", "区名"]:
    page.evaluate(f"""() => {{
        var menus = document.querySelectorAll('.el-cascader-menu');
        for (var m of menus) {{
            var nodes = m.querySelectorAll('.el-cascader-node');
            for (var n of nodes) {{
                var label = n.querySelector('.el-cascader-node__label');
                if (label && label.innerText.trim() === '{city}') {{ n.click(); return true; }}
            }}
        }}
        return false;
    }}""")
    time.sleep(1)
print("✅ 城市已选")

# 5. 店铺（根据SHOP自动选择）
page.locator('.el-form-item').filter(has_text="所属店铺").locator('input').first.click()
time.sleep(2)
page.locator('.el-select-dropdown__item').filter(has_text=SHOP_NAME).first.click()
time.sleep(1)
print(f"✅ 店铺已选 ({SHOP_NAME})")

# 6. 规格
page.locator('.el-radio').filter(has_text="单规格").first.click()
time.sleep(0.5)
print("✅ 规格已选")

# 7. 售价
page.locator('.el-form-item').filter(has_text="售价").locator('input').first.fill("1")
time.sleep(0.5)
print("✅ 售价已填")

# 8. 库存
page.locator('.el-form-item').filter(has_text="库存").locator('input').first.fill(STOCK)
time.sleep(0.5)
print(f"✅ 库存已填 ({STOCK})")

# 9. 运费
page.locator('.el-radio').filter(has_text="包邮").first.click()
time.sleep(0.5)
print("✅ 运费已选")

print("⏳ 等待3秒后发布...")
time.sleep(3)

# 10. 点击发布
page.locator('button.submission').first.click(force=True)
time.sleep(5)

# 11. 确认弹窗
page.evaluate("""() => {
    var btns = document.querySelectorAll('.el-message-box__btns button, button');
    for (var b of btns) {
        if (b.innerText.includes('确定') || b.innerText.includes('确 定')) {
            b.click(); return;
        }
    }
}""")
time.sleep(3)

if "product_list" in page.url:
    print("🎉 发布成功！")
else:
    page.locator('button.submission').first.click(force=True)
    time.sleep(5)
    page.evaluate("""() => {
        var btns = document.querySelectorAll('button');
        for (var b of btns) {
            if (b.innerText.includes('确定')) { b.click(); return; }
        }
    }""")
    time.sleep(3)

print(f"当前URL: {page.url}")

# ======================================================
# 第二步：立即配置自动发货+售罄上架
# ======================================================
print("=" * 40)
print("第二步：配置自动发货+售罄上架")
print("=" * 40)

if "product_list" not in page.url:
    page.goto("https://ed.weeeg.com/ekadmin/product/product_list", wait_until="domcontentloaded")
    time.sleep(3)

# 滚动表格
page.evaluate("""() => {
    var w = document.querySelector('.el-table__body-wrapper');
    if (w) w.scrollLeft = 9999;
}""")
time.sleep(1)

# 检查是否已有商品
rows = page.evaluate("""() => {
    return document.querySelectorAll('.el-table__body-wrapper tbody tr').length;
}""")
print(f"表格行数: {rows}")

if rows > 0:
    # 点击自动发货开关
    print("开启自动发货...")
    page.evaluate("""() => {
        var tr = document.querySelector('.el-table__body-wrapper tbody tr');
        var tds = tr.querySelectorAll('td');
        var sw = tds[10].querySelector('.el-switch');
        if (sw) {
            if (sw.classList.contains('is-checked')) return;
            var core = sw.querySelector('.el-switch__core') || sw;
            core.click();
        }
    }""")
    time.sleep(3)

    # 填网盘分享文本
    page.evaluate(f"""() => {{
        var ta = document.querySelector('.addproduct-dialog textarea, .el-dialog__body textarea');
        if (ta) {{
            ta.value = `{PAN_TEXT}`;
            ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
        }}
    }}""")
    print("✅ 已填入完整的网盘分享文本")
    time.sleep(1)

    # 展开高级配置
    page.evaluate("""() => {
        var labels = document.querySelectorAll('.addproduct-dialog label, .el-dialog__body label, span, .el-collapse-item__header');
        for (var l of labels) {
            if (l.innerText.includes('高级配置')) { l.click(); return; }
        }
    }""")
    print("✅ 已展开高级配置")
    time.sleep(2)

    # 提取码
    page.evaluate(f"""() => {{
        var inputs = document.querySelectorAll('.addproduct-dialog input, .el-dialog__body input');
        for (var inp of inputs) {{
            if (inp.placeholder && (inp.placeholder.includes('提取码') || inp.placeholder.includes('密码'))) {{
                inp.value = '{PAN_CODE}';
                inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
                return;
            }}
        }}
    }}""")
    print("✅ 已填入提取码")
    time.sleep(1)

    # 勾选发货声明
    page.evaluate("""() => {
        var cbs = document.querySelectorAll('.el-checkbox');
        for (var cb of cbs) {
            var label = cb.querySelector('.el-checkbox__label');
            if (label && label.innerText.includes('发货声明')) {
                var inp = cb.querySelector('input');
                if (inp && !inp.checked) { cb.click(); }
                return;
            }
        }
    }""")
    print("✅ 已勾选发货声明")
    time.sleep(1)

    # 保存
    page.evaluate("""() => {
        var btns = document.querySelectorAll('.addproduct-dialog button, .el-dialog__footer button');
        for (var b of btns) {
            if (b.innerText.includes('保存')) { b.click(); return; }
        }
    }""")
    print("✅ 已点击保存")
    time.sleep(5)

    # 先关闭弹窗（等弹窗消失后再操作主开关）
    page.evaluate("""() => {
        document.querySelectorAll('.addproduct-dialog, .el-dialog__wrapper').forEach(d => {
            if (d.style.display !== 'none') {
                var closeBtn = d.querySelector('.el-dialog__headerbtn, .el-dialog__close');
                if (closeBtn) closeBtn.click();
            }
        });
    }""")
    time.sleep(2)

    # 自动发货开关没变蓝则再点一次（两个店铺都需要这个二次点击）
    page.evaluate("""() => {
        var tr = document.querySelector('.el-table__body-wrapper tbody tr');
        if (!tr) return;
        var tds = tr.querySelectorAll('td');
        var sw = tds[10].querySelector('.el-switch');
        if (sw && !sw.classList.contains('is-checked')) {
            var core = sw.querySelector('.el-switch__core') || sw;
            core.click();
        }
    }""")
    time.sleep(3)

    # 再次检查，如果还没变蓝再点一次
    page.evaluate("""() => {
        var tr = document.querySelector('.el-table__body-wrapper tbody tr');
        if (!tr) return;
        var tds = tr.querySelectorAll('td');
        var sw = tds[10].querySelector('.el-switch');
        if (sw && !sw.classList.contains('is-checked')) {
            var core = sw.querySelector('.el-switch__core') || sw;
            core.click();
        }
    }""")
    time.sleep(3)

    # 开启售罄上架
    print("开启售罄上架...")
    page.evaluate("""() => {
        var tr = document.querySelector('.el-table__body-wrapper tbody tr');
        var tds = tr.querySelectorAll('td');
        var sw = tds[11].querySelector('.el-switch');
        if (sw) {
            if (sw.classList.contains('is-checked')) return;
            var core = sw.querySelector('.el-switch__core') || sw;
            core.click();
        }
    }""")
    time.sleep(3)

    # 售罄上架弹窗
    page.evaluate("""() => {
        var dialogs = document.querySelectorAll('.el-dialog__wrapper');
        for (var d of dialogs) {
            if (d.style.display !== 'none' && d.offsetParent !== null) {
                var cb = d.querySelector('.el-checkbox input');
                if (cb && !cb.checked) { cb.click(); }
                var btns = d.querySelectorAll('button');
                for (var b of btns) {
                    if (b.innerText.includes('确定')) { b.click(); return; }
                }
            }
        }
    }""")
    time.sleep(3)

    # 1号店额外：开启2人小刀
    if ENABLE_TWO_PERSON_DISCOUNT:
        print("开启2人小刀...")
        page.evaluate("""() => {
            var tr = document.querySelector('.el-table__body-wrapper tbody tr');
            var tds = tr.querySelectorAll('td');
            var sw = tds[12].querySelector('.el-switch');
            if (sw) {
                if (sw.classList.contains('is-checked')) return;
                var core = sw.querySelector('.el-switch__core') || sw;
                core.click();
            }
        }""")
        time.sleep(3)

        # 2人小刀弹窗
        page.evaluate("""() => {
            var dialogs = document.querySelectorAll('.el-dialog__wrapper');
            for (var d of dialogs) {
                if (d.style.display !== 'none' && d.offsetParent !== null) {
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
        }""")
        time.sleep(3)
        print("✅ 2人小刀已开启 (0.7)")

    # 验证最终状态
    page.reload(wait_until="domcontentloaded")
    time.sleep(5)
    page.evaluate("""() => {
        var w = document.querySelector('.el-table__body-wrapper');
        if (w) w.scrollLeft = 9999;
    }""")
    time.sleep(2)

    status = page.evaluate("""() => {
        var tr = document.querySelector('.el-table__body-wrapper tbody tr');
        if (!tr) return ['未知', '未知', '未知'];
        var tds = tr.querySelectorAll('td');
        if (tds.length < 13) return ['未知', '未知', '未知'];
        return [tds[10].innerText, tds[11].innerText, tds[12].innerText];
    }""")
    print(f"最终: 自动发货={status[0]}, 售罄上架={status[1]}, 2人小刀={status[2]}")
else:
    print("⚠️ 表格为空，无法配置")

p.stop()
print("🎉 全部完成！")
