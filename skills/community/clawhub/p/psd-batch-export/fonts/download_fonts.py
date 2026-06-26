"""
字体下载工具 — 自动下载推荐的开源中文字体到技能包 fonts/ 目录。
支持字体：阿里妈妈系列、思源系列、霞鹜文楷（均免费商用）。

字体合集百度网盘: https://pan.baidu.com/s/16mr469ucSXcNpm-6GD_QeA 提取码: kxrv

用法:
  python download_fonts.py              # 交互式选择
  python download_fonts.py --all         # 下载全部
  python download_fonts.py --list        # 列出可用字体
"""
import sys, os, argparse
from pathlib import Path
import urllib.request
import zipfile, io

FONTS_DIR = Path(__file__).parent

FONT_LIST = {
    "alimama-shuhei": {
        "name": "阿里妈妈数黑体 Bold",
        "url": None,  # 需手动下载，提供引导
        "manual": "https://www.iconfont.cn/ 搜索「阿里妈妈数黑体」下载 Bold 版本",
        "file": "AlimamaShuHeiTi-Bold.ttf",
    },
    "alimama-fangyuan": {
        "name": "阿里妈妈方圆体",
        "url": None,
        "manual": "https://fonts.alibabagroup.com 搜索「阿里妈妈方圆体」",
        "file": "AlimamaFangYuanTiVF-Thin.ttf",
    },
    "lxgw-wenkai": {
        "name": "霞鹜文楷",
        "url": "https://github.com/lxgw/LxgwWenKai/releases/latest/download/LXGWWenKai-Regular.ttf",
        "file": "LXGWWenKai-Regular.ttf",
    },
}

def download_font(font_key, info):
    """下载单个字体"""
    dest = FONTS_DIR / info["file"]
    if dest.exists():
        print(f"  Already exists: {info['file']}")
        return True
    
    if info["url"] is None:
        print(f"\n  {info['name']} 需手动下载：")
        print(f"  {info['manual']}")
        print(f"  下载后放入: {FONTS_DIR}")
        return False
    
    print(f"  Downloading {info['name']}...")
    try:
        req = urllib.request.Request(info["url"], headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=30).read()
        
        # 检查是否是 zip
        if info["url"].endswith(".zip"):
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                for name in z.namelist():
                    if name.lower().endswith((".ttf", ".otf")):
                        z.extract(name, FONTS_DIR)
                        print(f"    Extracted: {name}")
        else:
            dest.write_bytes(data)
            print(f"    Saved: {info['file']}")
        return True
    except Exception as e:
        print(f"    Failed: {e}")
        print(f"    请手动从 {info['manual'] or info['url']} 下载")
        return False


def main():
    p = argparse.ArgumentParser(description="字体下载工具")
    p.add_argument("--all", action="store_true", help="下载全部")
    p.add_argument("--list", action="store_true", help="列出可用字体")
    a = p.parse_args()
    
    if a.list:
        print("可用字体：")
        for key, info in FONT_LIST.items():
            installed = " [已安装]" if (FONTS_DIR / info["file"]).exists() else ""
            print(f"  {key:<25} {info['name']}{installed}")
        return
    
    if a.all:
        keys = list(FONT_LIST.keys())
    else:
        print("选择要下载的字体（输入编号，多个用逗号分隔，all=全部）：")
        for i, (key, info) in enumerate(FONT_LIST.items(), 1):
            installed = " [已安装]" if (FONTS_DIR / info["file"]).exists() else ""
            print(f"  [{i}] {info['name']}{installed}")
        choice = input("> ").strip()
        if choice.lower() == "all":
            keys = list(FONT_LIST.keys())
        else:
            indices = [int(c.strip()) - 1 for c in choice.split(",") if c.strip().isdigit()]
            keys = [list(FONT_LIST.keys())[i] for i in indices if 0 <= i < len(FONT_LIST)]
    
    if not keys:
        print("未选择任何字体")
        return
    
    ok = 0
    for key in keys:
        if key in FONT_LIST:
            if download_font(key, FONT_LIST[key]):
                ok += 1
    
    print(f"\n完成: {ok}/{len(keys)} 个字体就绪")
    print(f"字体目录: {FONTS_DIR}")


if __name__ == "__main__":
    main()
