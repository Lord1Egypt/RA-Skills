"""
飞书 CLI 封装模块 — 读取多维表格商品清单，写回状态

依赖：
  - lark-cli (https://github.com/larksuite/cli)
  - 飞书 CLI 已认证（lark-cli api GET /open-apis/drive/v1/files 能正常返回）

用法：
  from feishu_reader import FeishuReader

  reader = FeishuReader(spreadsheet_token="xxx", sheet_id="xxx")
  products = reader.get_pending_products()
  for p in products:
      print(p['title'], p['shop'], p['image_file'])
  reader.mark_done(p['title'], p['shop'])

配合 publisher.py 使用：
  config = {
      'shop': p['shop'],
      'title': p['title'],
      'desc': p['desc'],
      'image_file': p['image_file'],
      'image_keyword': os.path.splitext(p['image_file'])[0],
      'pan_text': p['pan_text'],
      'pan_code': p['pan_code'],
      'image_dir': r'D:\图片目录',
  }
  from publisher import publish_product
  success = publish_product(config)
  if success:
      reader.mark_done(p['title'], p['shop'])
"""

import subprocess
import json
import os
import sys
from datetime import datetime
from typing import Optional


# ============================================================
# 店铺映射（按你本地店铺名）
# ============================================================
SHOP_MAP = {
    "一号店铺名": 1,
    "二号店铺名": 2,
}
SHOP_LABELS = {1: "一号店铺名", 2: "二号店铺名"}


class FeishuReader:
    """
    飞书多维表格商品清单读取器

    多维表格列定义（当前版本）：
      A: 发布日期      (如 "6.25"，同一天多商品可合并单元格)
      B: 商品标题      (如 "UPDF 专业版永久激活码")
      C: 宝贝描述      (多行文本，不含网盘链接)
      D: 商品图名称    (如 "updf"，不写扩展名，脚本自动补.jpg)
      E: 网盘发货文案  (完整文本，含链接和提取码)
      F: 店铺          (如 "一号店铺名" / "二号店铺名")
      G: 状态          (如 "待上货" / "已上货")
      H: 备注          (可选)

    版本：v1.0 — 2026-06-25
      支持飞书 CLI 读取多维表格，自动解析图片文件名、店铺名、提取码
      配合 publisher.py v4.1 使用，支持每步自检重试
    """

    def __init__(self, spreadsheet_token: str, sheet_id: str = None, lark_cli_path: str = None):
        self.spreadsheet_token = spreadsheet_token
        self.sheet_id = sheet_id

        # 自动查找 lark-cli（node 脚本，需通过 node 调用）
        self.node_path = r"C:\Users\14437\.workbuddy\binaries\node\versions\22.22.2\node.exe"
        self.lark_script = r"C:\Users\14437\.workbuddy\binaries\node\versions\22.22.2\node_modules\@larksuite\cli\scripts\run.js"

        # 如果指定的路径是 lark-cli 脚本本身，解析它
        if lark_cli_path and lark_cli_path != "lark-cli":
            base = os.path.dirname(lark_cli_path)
            self.node_path = os.path.join(base, "node.exe")
            self.lark_script = os.path.join(base, "node_modules", "@larksuite", "cli", "scripts", "run.js")

        # 如果没有 sheet_id，自动获取
        if not self.sheet_id:
            self._auto_get_sheet_id()

    def _run_cli(self, args: list) -> dict:
        """运行飞书 CLI 命令并返回解析后的 JSON"""
        cmd = [self.node_path, self.lark_script] + args
        try:
            result = subprocess.run(
                cmd, capture_output=True, timeout=30,
                encoding='utf-8', errors='replace'
            )
            if result.returncode != 0:
                print(f"⚠️ 飞书 CLI 错误: {result.stderr}")
                return {"ok": False, "error": result.stderr}
            return json.loads(result.stdout)
        except subprocess.TimeoutExpired:
            print(f"⚠️ 飞书 CLI 超时: {' '.join(cmd)}")
            return {"ok": False, "error": "timeout"}
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON 解析错误: {e}")
            print(f"  原始输出: {result.stdout[:200]}")
            return {"ok": False, "error": str(e)}
        except FileNotFoundError:
            print(f"❌ 飞书 CLI 未找到")
            return {"ok": False, "error": "lark-cli not found"}

    def _auto_get_sheet_id(self):
        """自动获取第一个 sheet 的 ID"""
        resp = self._run_cli([
            "sheets", "+workbook-info",
            "--spreadsheet-token", self.spreadsheet_token
        ])
        if resp.get("ok") and resp.get("data", {}).get("sheets"):
            self.sheet_id = resp["data"]["sheets"][0]["sheet_id"]
            print(f"📋 自动获取 sheet_id: {self.sheet_id}")
        else:
            print("❌ 无法获取 sheet_id")

    def _resolve_shop(self, shop_label: str) -> int:
        """
        根据店铺名解析店铺号。
        精确匹配 SHOP_MAP，匹配不到则按关键字推断。
        """
        label = shop_label.strip()
        # 精确匹配
        if label in SHOP_MAP:
            return SHOP_MAP[label]
        # 模糊匹配
        if "1" in label or "天空" in label or "流星" in label:
            return 1
        if "2" in label or "林酱" in label:
            return 2
        # 默认 1 号店
        print(f"  ⚠️ 无法识别的店铺名: '{label}'，默认使用 1 号店")
        return 1

    def _resolve_image(self, image_name: str) -> str:
        """
        解析商品图名称。
        先尝试精确匹配，再尝试模糊匹配（文件名中包含关键字）。
        """
        name = image_name.strip()
        if not name:
            return ""
        # 如果已有常见扩展名，直接返回
        if name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            return name

        # 尝试在图片目录中模糊匹配
        import os
        img_dir = r"图片资料目录"
        if os.path.exists(img_dir):
            name_lower = name.lower()
            for f in os.listdir(img_dir):
                f_lower = f.lower()
                if f_lower.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    f_no_ext = os.path.splitext(f_lower)[0]
                    if name_lower in f_no_ext or f_no_ext in name_lower:
                        return f

        # 默认补 .jpg
        return name + ".jpg"

    def read_all_rows(self) -> list[dict]:
        """
        读取多维表格所有行，返回商品字典列表

        返回格式:
          [
            {
              "publish_date": "6.25",
              "title": "UPDF 专业版永久激活码",
              "desc": "支持全平台...",
              "image_file": "updf.jpg",       ← 自动补了扩展名
              "pan_text": "通过网盘分享的文件：...",  ← 完整的网盘发货文案
              "pan_code": "abcd",              ← 从网盘文本中提取的提取码
              "shop_label": "一号店铺名",
              "shop": 1,
              "status": "待上货",
              "row_index": 2
            },
            ...
          ]
        """
        if not self.sheet_id:
            print("❌ sheet_id 未设置")
            return []

        resp = self._run_cli([
            "sheets", "+cells-get",
            "--spreadsheet-token", self.spreadsheet_token,
            "--sheet-id", self.sheet_id,
            "--range", "A:I"
        ])

        if not resp.get("ok"):
            print(f"❌ 读取飞书表格失败: {resp.get('error', 'unknown error')}")
            return []

        ranges = resp.get("data", {}).get("ranges", [])
        values = ranges[0].get("cells", []) if ranges else []
        if not values:
            print("📭 飞书表格为空")
            return []

        products = []
        # 记录上一个非空值（支持合并单元格）
        last_date = ""
        last_shop = ""
        for idx, row in enumerate(values):
            # 跳过表头行 (idx=0)
            if idx == 0:
                continue

            if len(row) < 7:
                continue

            # 日期列：合并单元格时只有第一个单元格有值
            publish_date = row[0].get("value", "") if isinstance(row[0], dict) else str(row[0])
            if publish_date.strip():
                last_date = publish_date.strip()
            else:
                publish_date = last_date

            title = row[1].get("value", "") if isinstance(row[1], dict) else str(row[1])
            desc = row[2].get("value", "") if isinstance(row[2], dict) else str(row[2])
            image_name = row[3].get("value", "") if isinstance(row[3], dict) else str(row[3])
            pan_text = row[4].get("value", "") if isinstance(row[4], dict) else str(row[4])

            # 店铺列：也支持合并单元格
            shop_label = row[5].get("value", "") if isinstance(row[5], dict) else str(row[5])
            if shop_label.strip():
                last_shop = shop_label.strip()
            else:
                shop_label = last_shop

            status = row[6].get("value", "") if isinstance(row[6], dict) else str(row[6])

            # 跳过空行
            if not title.strip():
                continue

            # 解析
            image_file = self._resolve_image(image_name)
            shop = self._resolve_shop(shop_label)

            # 从网盘文案中提取提取码（用于 publisher 的 pan_code 参数）
            pan_code = self._extract_pan_code(pan_text)

            products.append({
                "publish_date": publish_date.strip(),
                "title": title.strip(),
                "desc": desc.strip(),
                "image_file": image_file,
                "image_name_raw": image_name.strip(),
                "pan_text": pan_text.strip(),
                "pan_code": pan_code,
                "shop_label": shop_label.strip(),
                "shop": shop,
                "status": status.strip(),
                "row_index": idx + 1,  # 1-based
            })

        print(f"📋 飞书表格: {len(products)} 条商品")
        return products

    def _extract_pan_code(self, pan_text: str) -> str:
        """从网盘文案中提取提取码"""
        import re
        m = re.search(r'提取码[：:]\s*(\w+)', pan_text)
        if m:
            return m.group(1)
        return ""

    def get_today_products(self, date_str: str = None) -> list[dict]:
        """
        获取当天待上货的商品

        Args:
            date_str: 日期字符串，格式 M.D（如 "6.25"），默认今天

        Returns:
            当天且状态为"待上货"的商品列表
        """
        if not date_str:
            now = datetime.now()
            date_str = f"{now.month}.{now.day}"

        all_products = self.read_all_rows()
        today_products = []

        for p in all_products:
            # 日期匹配
            if p["publish_date"] != date_str:
                continue

            # 状态过滤：只取"待上货"
            if p["status"] in ("已上货", "已发布"):
                continue

            today_products.append(p)

        print(f"📅 {date_str} 待上货: {len(today_products)} 个商品")
        return today_products

    def get_pending_products(self) -> list[dict]:
        """
        获取所有待上货商品（不限日期）

        Returns:
            状态为"待上货"的商品列表
        """
        all_products = self.read_all_rows()
        pending = [p for p in all_products if p["status"] in ("待上货", "")]

        print(f"📋 待上货商品: {len(pending)} 个")
        return pending

    def update_status(self, row_index: int, new_status: str):
        """
        更新商品状态

        Args:
            row_index: 行号（1-based），如 A2 对应 row_index=2
            new_status: 新状态，如 "已上货"
        """
        if not self.sheet_id:
            print("❌ sheet_id 未设置")
            return False

        # 更新状态列 (G 列 — 多维表格的「状态」列)
        status_cell = f"G{row_index}"
        resp = self._run_cli([
            "sheets", "+cells-set",
            "--spreadsheet-token", self.spreadsheet_token,
            "--sheet-id", self.sheet_id,
            "--range", status_cell,
            "--cells", json.dumps([[{"value": new_status}]])
        ])

        if resp.get("ok"):
            print(f"  📌 飞书状态已更新: {status_cell} → {new_status}")
            return True
        else:
            print(f"  ⚠️ 更新状态失败: {resp.get('error', 'unknown')}")
            return False

    def mark_done(self, title: str, shop: int) -> bool:
        """
        标记某个商品为已上货（按标题+店铺匹配）

        Args:
            title: 商品标题
            shop: 店铺号 1 或 2
        """
        all_products = self.read_all_rows()
        for p in all_products:
            if p["title"] == title and p["shop"] == shop:
                return self.update_status(p["row_index"], "已上货")
        print(f"  ⚠️ 未找到匹配商品: {title} (店铺{shop})")
        return False

    def health_check(self) -> bool:
        """检查飞书 CLI 是否可用"""
        resp = self._run_cli(["api", "GET", "/open-apis/drive/v1/files", "--params", '{"page_size":1}'])
        ok = resp.get("ok", False)
        print(f"{'✅' if ok else '❌'} 飞书 CLI 状态: {'正常' if ok else '异常'}")
        return ok


if __name__ == "__main__":
    # 测试：读取飞书表格
    TOKEN = "CBwesfEuwh8i3JtUPBTc0K63nbd"

    reader = FeishuReader(spreadsheet_token=TOKEN)

    # 健康检查
    if not reader.health_check():
        print("❌ 飞书 CLI 不可用，请先配置")
        sys.exit(1)

    # 读取所有商品
    products = reader.read_all_rows()
    print(f"\n共 {len(products)} 条商品:\n")

    for p in products:
        print(f"  [{p['row_index']}] {p['publish_date']} | {p['title'][:30]:30s} | {p['shop_label']:10s} | {p['status']}")
        print(f"      图片: {p['image_file']}")
