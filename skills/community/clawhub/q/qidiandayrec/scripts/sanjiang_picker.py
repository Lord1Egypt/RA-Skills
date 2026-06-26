#!/usr/bin/env python3
"""
起点三江榜单好书推荐爬虫（v2 缓存+性格版）
=============================================
从起点图(qidiantu.com)获取最新三江榜单书籍列表，
首次抓取时获取全量书籍详情并预打 SBTI 人格标签，缓存到本地。
后续请求直接读缓存，零网络请求，保护源站。

核心特性：
  - 本地缓存：每天首次抓取全量数据（含详情+SBTI标签）缓存到本地
  - 性格筛选：支持按 SBTI 人格推荐（--sbti MALO / --sbti 吗喽）
  - 历史去重：每次推荐与上一次不重复
  - 随机轮换：从候选池中随机挑选，保证新鲜感
  - 分类多样性：尽量覆盖不同分类
  - 零配置启动：自动检测并安装所需依赖

数据源：
  - 三江榜单列表：https://www.qidiantu.com/bang/1/6/{date}
  - 书籍详情页：https://www.qidiantu.com/info/{book_id}

用法：
  python3 sanjiang_picker.py [--count 3] [--date YYYY-MM-DD] [--output json|markdown|text]
  python3 sanjiang_picker.py --sbti MALO          # 按 SBTI 人格推荐
  python3 sanjiang_picker.py --sbti 吗喽          # 支持中文人格名
  python3 sanjiang_picker.py --refresh             # 强制刷新缓存
  python3 sanjiang_picker.py --list-sbti           # 列出所有 SBTI 人格
  python3 sanjiang_picker.py --dump-cache          # 输出当天完整缓存数据
  python3 sanjiang_picker.py --setup               # 仅检测环境并安装依赖

依赖（自动安装）：beautifulsoup4 lxml
"""

import argparse
import hashlib
import json
import os
import random
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta
from html import unescape
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


# ─── 环境检测与自动安装 ────────────────────────────────
REQUIRED_PACKAGES = {
    # import_name: pip_package_name
    "bs4": "beautifulsoup4",
    "lxml": "lxml",
}


def check_python_version():
    """检测 Python 版本，要求 3.6+（仅打印警告，不退出）
    
    注意：能运行到这里说明 Python 已安装。
    Python 安装检测由 SKILL.md 中的 agent 预检流程负责（在调用脚本之前）。
    这里只做版本号检查。
    """
    v = sys.version_info
    if v.major < 3 or (v.major == 3 and v.minor < 6):
        print(f"[WARN] 建议使用 Python 3.6+，当前版本: {v.major}.{v.minor}.{v.micro}", file=sys.stderr)
        print("[WARN] 部分功能可能不兼容，建议升级 Python", file=sys.stderr)
    return True


def check_and_install_deps(verbose=False):
    """检测并自动安装缺失的 Python 依赖。"""
    missing = []
    for import_name, pip_name in REQUIRED_PACKAGES.items():
        try:
            __import__(import_name)
            if verbose:
                print(f"  ✅ {pip_name} 已安装", file=sys.stderr)
        except ImportError:
            missing.append((import_name, pip_name))
            if verbose:
                print(f"  ❌ {pip_name} 未安装", file=sys.stderr)
    
    if not missing:
        if verbose:
            print("[OK] 所有依赖已就绪！", file=sys.stderr)
        return True
    
    pip_packages = [pip_name for _, pip_name in missing]
    print(f"[INFO] 检测到缺失依赖: {', '.join(pip_packages)}，正在自动安装...", file=sys.stderr)
    
    pip_commands = [
        [sys.executable, "-m", "pip", "install"] + pip_packages,
        ["pip3", "install"] + pip_packages,
        ["pip", "install"] + pip_packages,
    ]
    
    installed = False
    for cmd in pip_commands:
        try:
            if verbose:
                print(f"[INFO] 尝试: {' '.join(cmd)}", file=sys.stderr)
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                print(f"[OK] 依赖安装成功: {', '.join(pip_packages)}", file=sys.stderr)
                installed = True
                break
            else:
                if verbose:
                    print(f"[WARN] 安装命令返回非零: {result.stderr[:200]}", file=sys.stderr)
        except FileNotFoundError:
            if verbose:
                print(f"[WARN] 命令不存在: {cmd[0]}", file=sys.stderr)
            continue
        except subprocess.TimeoutExpired:
            print("[WARN] 安装超时，请检查网络连接", file=sys.stderr)
            continue
        except Exception as e:
            if verbose:
                print(f"[WARN] 安装异常: {e}", file=sys.stderr)
            continue
    
    if not installed:
        print("[ERROR] 自动安装依赖失败，请手动安装：", file=sys.stderr)
        print(f"  pip3 install {' '.join(pip_packages)}", file=sys.stderr)
        print("", file=sys.stderr)
        print("如果 pip3 命令不存在，请先安装 pip：", file=sys.stderr)
        if sys.platform == "darwin":
            print("  python3 -m ensurepip --upgrade", file=sys.stderr)
        elif sys.platform == "win32":
            print("  python -m ensurepip --upgrade", file=sys.stderr)
        else:
            print("  sudo apt install python3-pip  # Ubuntu/Debian", file=sys.stderr)
            print("  sudo yum install python3-pip  # CentOS/RHEL", file=sys.stderr)
        return False
    
    # 验证安装结果
    all_ok = True
    for import_name, pip_name in missing:
        try:
            __import__(import_name)
            if verbose:
                print(f"  ✅ {pip_name} 验证通过", file=sys.stderr)
        except ImportError:
            print(f"[ERROR] {pip_name} 安装后仍无法导入，请手动安装", file=sys.stderr)
            all_ok = False
    
    return all_ok


def setup_environment():
    """完整的环境检测与初始化（供 --setup 参数调用）"""
    print("=" * 50, file=sys.stderr)
    print("🔍 起点三江推荐 - 环境检测", file=sys.stderr)
    print("=" * 50, file=sys.stderr)
    
    v = sys.version_info
    print(f"\n📌 Python: {v.major}.{v.minor}.{v.micro} ({sys.executable})", file=sys.stderr)
    if v.major >= 3 and v.minor >= 6:
        print("   ✅ 版本符合要求 (3.6+)", file=sys.stderr)
    else:
        print("   ⚠️  建议升级到 3.6+", file=sys.stderr)
    
    print(f"\n📌 pip 检测:", file=sys.stderr)
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            pip_ver = result.stdout.strip().split("\n")[0]
            print(f"   ✅ {pip_ver}", file=sys.stderr)
        else:
            print("   ⚠️  pip 未安装", file=sys.stderr)
    except Exception:
        print("   ⚠️  无法检测 pip 版本", file=sys.stderr)
    
    print(f"\n📌 依赖检测:", file=sys.stderr)
    ok = check_and_install_deps(verbose=True)
    
    print(f"\n📌 网络连通性:", file=sys.stderr)
    try:
        req = Request("https://www.qidiantu.com", headers=HEADERS)
        with urlopen(req, timeout=10):
            print("   ✅ qidiantu.com 可访问", file=sys.stderr)
    except Exception as e:
        print(f"   ⚠️  qidiantu.com 访问异常: {e}", file=sys.stderr)
    
    # 显示缓存状态
    print(f"\n📌 缓存状态:", file=sys.stderr)
    if os.path.isdir(CACHE_DIR):
        cache_files = [f for f in os.listdir(CACHE_DIR) if f.startswith("sanjiang_") and f.endswith(".json")]
        if cache_files:
            print(f"   📁 缓存目录: {CACHE_DIR}", file=sys.stderr)
            print(f"   📄 缓存文件: {len(cache_files)} 个", file=sys.stderr)
            for cf in sorted(cache_files, reverse=True)[:3]:
                fpath = os.path.join(CACHE_DIR, cf)
                fsize = os.path.getsize(fpath)
                print(f"      - {cf} ({fsize/1024:.1f} KB)", file=sys.stderr)
        else:
            print("   📁 缓存目录已创建，暂无缓存文件", file=sys.stderr)
    else:
        print("   📁 缓存目录尚未创建（首次运行时自动创建）", file=sys.stderr)
    
    print(f"\n{'=' * 50}", file=sys.stderr)
    if ok:
        print("✅ 环境检测通过，可以正常使用！", file=sys.stderr)
        print("用法: python3 sanjiang_picker.py --count 3", file=sys.stderr)
        print("按性格: python3 sanjiang_picker.py --sbti MALO", file=sys.stderr)
    else:
        print("❌ 有依赖未安装成功，请参考上方提示手动安装", file=sys.stderr)
    print("=" * 50, file=sys.stderr)
    
    return ok


# ─── 启动时自动检测依赖 ────────────────────────────────
check_python_version()

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    print("[INFO] 首次运行，正在自动配置环境...", file=sys.stderr)
    if check_and_install_deps():
        try:
            from bs4 import BeautifulSoup
            HAS_BS4 = True
        except ImportError:
            HAS_BS4 = False
    else:
        HAS_BS4 = False


# ─── 配置 ─────────────────────────────────────────────
BASE_URL = "https://www.qidiantu.com"
SANJIANG_LIST_PATH = "/bang/1/6/{date}"  # date 格式: YYYY-MM-DD
BOOK_INFO_PATH = "/info/{book_id}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}
REQUEST_TIMEOUT = 15  # 秒
RETRY_COUNT = 2
RETRY_DELAY = 3  # 秒

# 历史记录与缓存路径（与脚本同目录）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(SCRIPT_DIR, ".sanjiang_history.json")
CACHE_DIR = os.path.join(SCRIPT_DIR, ".cache")
CACHE_MAX_AGE_DAYS = 7  # 缓存文件最多保留天数


# ─── SBTI 人格库（2026年4月爆火的玩梗版MBTI）──────────
# 每种人格包含：缩写、中文名、特征关键词、适配的小说分类关键词
SBTI_PERSONALITIES = [
    {"code": "SOLO", "name": "孤儿", "trait": "独行侠，莫挨老子",
     "keywords": ["武侠", "仙侠", "灵异", "悬疑", "末世"],
     "reason_templates": [
         "这本书的主角就是SBTI里的{code}（{name}），一个人扛下所有——{trait}。看完你会觉得自己那点孤独根本不算事儿。",
         "测出{code}（{name}）的朋友注意了！这本书就是你的精神传记，主角比你还能独来独往。",
         "SBTI测出{code}的人必看，主角{trait}的程度让你自愧不如。",
     ]},
    {"code": "MALO", "name": "吗喽", "trait": "躺平哲学，拒绝内卷",
     "keywords": ["都市", "轻小说", "日常", "生活"],
     "reason_templates": [
         "SBTI吗喽人狂喜！主角前期摆得比你还平，后期躺赢得比你还香。这不就是做梦都不敢想的完美人生？",
         "测出{code}（{name}）的书荒患者特供：主角的核心竞争力就是——{trait}。看完治愈你的上班内耗。",
         "这本书简直是{name}人格的圣经，主角把{trait}发挥到了艺术层面。",
     ]},
    {"code": "FUCK", "name": "草者", "trait": "叛逆暴躁，人形野草不服管",
     "keywords": ["玄幻", "奇幻", "战争", "军事"],
     "reason_templates": [
         "SBTI草者（{code}）专属推荐：主角脾气比你还暴，打脸比你还狠，看得你爽到想给作者充VIP。",
         "测出{code}的朋友，这本书能满足你所有想砸键盘的冲动。主角替你把想说的脏话都用行动说了。",
         "这书的主角就是{name}本名，{trait}，一路莽到底，看完整个人精神状态都好了。",
     ]},
    {"code": "OJBK", "name": "无所谓人", "trait": "随波逐流，口头禅：随便",
     "keywords": ["历史", "二次元", "轻小说"],
     "reason_templates": [
         "你SBTI测出{code}（{name}）？巧了，这本书的主角比你还随便，结果随便着随便着就成了大佬。",
         "无所谓人看了都得说一句'有所谓'的好书。主角的佛系程度让你这个{name}都自叹不如。",
         "测出{code}的朋友别滑走！这本书证明了{trait}也能成大事，你的精神状态没毛病。",
     ]},
    {"code": "FAKE", "name": "伪人", "trait": "面具大师，隐藏真实自我",
     "keywords": ["悬疑", "灵异", "历史", "权谋"],
     "reason_templates": [
         "SBTI伪人（{code}）必入！主角表面一套背后一套的段位，比你的职场假笑高了整整十个level。",
         "测出{code}的社交高手看过来，主角的{trait}技术让你直呼内行。看完可能解锁新的演技。",
         "这书就是{name}的操作手册，主角{trait}玩到飞起，每章都有反转看得你头皮发麻。",
     ]},
    {"code": "IMSB", "name": "自我攻击者", "trait": "内耗严重，又菜又爱想",
     "keywords": ["都市", "科幻", "现实"],
     "reason_templates": [
         "SBTI自我攻击者（{code}）看这本能治病！主角前期比你还能内耗，后期逆袭的时候你哭得比他还凶。",
         "测出{code}的朋友，主角跟你一样{trait}，但人家靠着这份纠结居然成了绝世高手。鸡汤都没这么励志。",
         "{name}人格特供良药：看完这本书你会发现，原来内耗也是一种超能力。",
     ]},
    {"code": "JOKE-R", "name": "小丑", "trait": "用搞笑掩盖心碎，气氛组担当",
     "keywords": ["轻小说", "都市", "游戏", "日常"],
     "reason_templates": [
         "SBTI小丑（{code}）本丑推荐：这本书笑着笑着就哭了，哭着哭着又笑了。跟你的人生是不是很像？",
         "测出{code}的朋友！这书主角{trait}的程度跟你有得一拼，但他比你多了个主角光环。",
         "小丑人格专属治愈番：主角是比你还能活跃气氛的{name}，但这次他终于不用强颜欢笑了。",
     ]},
    {"code": "ZZZZ", "name": "装死者", "trait": "遇事就躲，逃避现实大师",
     "keywords": ["奇幻", "仙侠", "游戏", "异界"],
     "reason_templates": [
         "SBTI装死者（{code}）找到组织了！主角的核心技能就是装死——然后一不小心装成了绝世强者。",
         "测出{code}的朋友，这本书告诉你{trait}不是问题，关键是装死的姿势要够帅。",
         "这本就是为{name}量身定做的：主角躺着躺着就赢了。你说气不气？",
     ]},
    {"code": "ATM", "name": "ATM-er", "trait": "人形提款机，总在为别人兜底",
     "keywords": ["都市", "历史", "现实"],
     "reason_templates": [
         "SBTI ATM-er看了想打人的好书：主角前期跟你一样当冤大头，后期让所有白嫖过他的人跪着唱征服。",
         "测出{code}的老好人必看！这本书能教你怎么从{name}进化成CTRL（拿捏者）。",
         "ATM人格代入感拉满：主角{trait}了三十章，剩下的章节全在收利息。爽翻。",
     ]},
    {"code": "DRUNK", "name": "酒鬼", "trait": "快乐全靠喝，一杯敬过往",
     "keywords": ["武侠", "历史", "仙侠"],
     "reason_templates": [
         "SBTI酒鬼（{code}）看了能醉的好书！主角喝着喝着就悟出了绝世武功，你喝着喝着就看完了全文。",
         "测出{code}的朋友，这本书的主角跟你一样{trait}，但人家是越喝越强你是越喝越困。",
         "给{name}人格的朋友一个不喝酒也能快乐的替代方案——看这本书。",
     ]},
    {"code": "WOC!", "name": "握草人", "trait": "易震惊体质，遇事只会卧槽",
     "keywords": ["玄幻", "科幻", "奇幻", "悬疑"],
     "reason_templates": [
         "SBTI握草人（{code}）预警：这本书每三章一个'卧槽'时刻，你的表情管理会全程失控。",
         "测出{code}的朋友，你的{trait}在这本书面前将得到充分释放。建议不要在公共场合阅读。",
         "这本书就是为{name}准备的精神过山车，看完你的'卧槽'键都得换新的。",
     ]},
    {"code": "MUM", "name": "妈妈", "trait": "天生母爱泛滥，到处照顾人",
     "keywords": ["轻小说", "都市", "日常", "游戏"],
     "reason_templates": [
         "SBTI妈妈（{code}）人格看了想领养主角：这本书的主角太惨了，你的{trait}属性会被疯狂触发。",
         "测出{code}的朋友注意了，这本书可能让你产生'我要冲进书里保护他'的冲动。",
         "{name}人格专属：主角身边全是需要照顾的人，比你带的团队还让人操心。",
     ]},
    {"code": "SEXY", "name": "尤物", "trait": "自信撩人，自带魅力光环",
     "keywords": ["都市", "历史", "武侠", "现实"],
     "reason_templates": [
         "SBTI尤物（{code}）本物推荐：这本书的主角魅力值跟你一样拉满，区别是人家有主角光环你只有美颜滤镜。",
         "测出{code}的朋友，主角{trait}的程度甚至超过了你的自我认知，这书简直是照镜子。",
         "给{name}人格推荐的'如何让全世界为你疯狂'教科书，主角示范得很到位。",
     ]},
    {"code": "CTRL", "name": "拿捏者", "trait": "控场大师，一切尽在掌握",
     "keywords": ["历史", "悬疑", "权谋", "科幻"],
     "reason_templates": [
         "SBTI拿捏者（{code}）看了拍大腿：主角的控场能力跟你一样强，但人家拿捏的是整个天下。",
         "测出{code}的朋友，这本书的主角{trait}，你们是精神上的同类。看完可能学到新套路。",
         "{name}人格必看：这书主角的操盘手法让你这个CTRL都得说声'学到了'。",
     ]},
    {"code": "SHIT", "name": "狗屎人", "trait": "愤世嫉俗，看啥都不顺眼",
     "keywords": ["现实", "末世", "科幻", "战争"],
     "reason_templates": [
         "SBTI狗屎人（{code}）终于找到了能看顺眼的书：主角跟你一样{trait}，但他比你多一个技能——能打。",
         "测出{code}的朋友，这本书的世界观跟你看到的一样烂，但主角选择了掀桌子。过瘾。",
         "{name}人格特供爽文：整个世界都是垃圾？没关系，主角一个人把垃圾场翻了个底朝天。",
     ]},
]

# 构建人格查找索引（code 和 name 都能查到）
_SBTI_INDEX = {}
for _p in SBTI_PERSONALITIES:
    _SBTI_INDEX[_p["code"].upper()] = _p
    _SBTI_INDEX[_p["name"]] = _p
    # 也支持不带感叹号的版本，如 WOC
    _clean_code = _p["code"].replace("!", "").replace("-", "").upper()
    _SBTI_INDEX[_clean_code] = _p


def resolve_sbti_filter(query):
    """
    将用户输入的性格描述解析为 SBTI 人格对象列表。
    
    支持：
    1. 精确匹配：code（如 MALO, FUCK）或中文名（如 吗喽, 草者）
    2. 模糊匹配：用户自由描述性格特征，匹配最相关的人格
    
    返回匹配到的人格列表（可能多个，模糊匹配时返回top3）。
    """
    if not query:
        return []
    
    query_upper = query.strip().upper().replace("!", "").replace("-", "")
    query_stripped = query.strip()
    
    # 精确匹配 code 或 name
    if query_upper in _SBTI_INDEX:
        return [_SBTI_INDEX[query_upper]]
    if query_stripped in _SBTI_INDEX:
        return [_SBTI_INDEX[query_stripped]]
    
    # 模糊匹配：按 trait/name/keywords 计算相关度
    scores = []
    for p in SBTI_PERSONALITIES:
        score = 0
        q_lower = query_stripped.lower()
        
        # trait 匹配（权重最高）
        for word in q_lower:
            if word in p["trait"]:
                score += 3
        # 整词匹配 trait
        for trait_word in p["trait"].replace("，", " ").replace("、", " ").split():
            if trait_word in q_lower or q_lower in trait_word:
                score += 5
        
        # name 部分匹配
        if p["name"] in query_stripped or query_stripped in p["name"]:
            score += 10
        
        # keywords 匹配
        for kw in p["keywords"]:
            if kw in query_stripped:
                score += 2
        
        # 特征关键词匹配表（用户常见自我描述 → 人格映射）
        trait_map = {
            "躺平": "MALO", "摆烂": "MALO", "不想上班": "MALO", "咸鱼": "MALO",
            "暴躁": "FUCK", "叛逆": "FUCK", "不服": "FUCK", "莽": "FUCK",
            "社恐": "SOLO", "独来独往": "SOLO", "一个人": "SOLO", "孤独": "SOLO",
            "随便": "OJBK", "无所谓": "OJBK", "佛系": "OJBK", "都行": "OJBK",
            "内耗": "IMSB", "焦虑": "IMSB", "纠结": "IMSB", "自我怀疑": "IMSB",
            "搞笑": "JOKE-R", "逗比": "JOKE-R", "气氛组": "JOKE-R", "开心果": "JOKE-R",
            "装死": "ZZZZ", "逃避": "ZZZZ", "鸵鸟": "ZZZZ", "不想面对": "ZZZZ",
            "老好人": "ATM", "讨好": "ATM", "心软": "ATM", "烂好人": "ATM",
            "喝酒": "DRUNK", "干杯": "DRUNK", "微醺": "DRUNK",
            "卧槽": "WOC!", "震惊": "WOC!", "大吃一惊": "WOC!",
            "照顾": "MUM", "操心": "MUM", "母爱": "MUM", "带娃": "MUM",
            "自信": "SEXY", "魅力": "SEXY", "撩": "SEXY", "帅": "SEXY",
            "控制": "CTRL", "拿捏": "CTRL", "掌控": "CTRL", "大局观": "CTRL",
            "愤世嫉俗": "SHIT", "看不惯": "SHIT", "垃圾": "SHIT", "烂": "SHIT",
            "假面": "FAKE", "伪装": "FAKE", "两面派": "FAKE", "戴面具": "FAKE",
        }
        for keyword, target_code in trait_map.items():
            if keyword in q_lower and p["code"] == target_code:
                score += 15
        
        if score > 0:
            scores.append((score, p))
    
    if not scores:
        return []
    
    # 按分数降序，返回 top3
    scores.sort(key=lambda x: -x[0])
    return [s[1] for s in scores[:3]]


def assign_sbti_personality(book):
    """
    根据书籍信息分配一个 SBTI 人格标签。
    
    匹配策略：
    1. 优先根据书籍分类关键词匹配最合适的人格
    2. 如果没有分类匹配，用 book_id hash 确定性分配
    """
    category = book.get("category", "")
    book_id = book.get("book_id", "")
    
    matched = []
    for p in SBTI_PERSONALITIES:
        for kw in p["keywords"]:
            if kw in category:
                matched.append(p)
                break
    
    if matched:
        idx = int(hashlib.md5(book_id.encode()).hexdigest(), 16) % len(matched)
        personality = matched[idx]
    else:
        idx = int(hashlib.md5(book_id.encode()).hexdigest(), 16) % len(SBTI_PERSONALITIES)
        personality = SBTI_PERSONALITIES[idx]
    
    return personality


def generate_sbti_reason(book, personality):
    """根据分配的 SBTI 人格生成诙谐必看理由"""
    templates = personality["reason_templates"]
    book_name = book.get("book_name", "")
    idx = int(hashlib.md5(book_name.encode()).hexdigest(), 16) % len(templates)
    template = templates[idx]
    
    return template.format(
        code=personality["code"],
        name=personality["name"],
        trait=personality["trait"],
    )


def label_single_book_sbti(book):
    """为单本书打上 SBTI 标签（预标注阶段，不做去重）"""
    personality = assign_sbti_personality(book)
    book["sbti_code"] = personality["code"]
    book["sbti_name"] = personality["name"]
    book["sbti_trait"] = personality["trait"]
    book["sbti_reason"] = generate_sbti_reason(book, personality)
    return book


def dedupe_sbti_in_batch(books):
    """
    对最终推荐批次做 SBTI 去重：同一批推荐里人格尽量不重复。
    
    如果某本书的人格与前面重复了，尝试重新分配一个不同的人格。
    """
    used_codes = set()
    for book in books:
        code = book.get("sbti_code", "")
        if code not in used_codes:
            used_codes.add(code)
            continue
        
        # 重复了，尝试找替代人格
        category = book.get("category", "")
        book_id = book.get("book_id", "")
        available = [p for p in SBTI_PERSONALITIES if p["code"] not in used_codes]
        if not available:
            used_codes.add(code)
            continue
        
        cat_matched = [p for p in available for kw in p["keywords"] if kw in category]
        if cat_matched:
            idx = int(hashlib.md5(book_id.encode()).hexdigest(), 16) % len(cat_matched)
            personality = cat_matched[idx]
        else:
            idx = int(hashlib.md5(book_id.encode()).hexdigest(), 16) % len(available)
            personality = available[idx]
        
        used_codes.add(personality["code"])
        book["sbti_code"] = personality["code"]
        book["sbti_name"] = personality["name"]
        book["sbti_trait"] = personality["trait"]
        book["sbti_reason"] = generate_sbti_reason(book, personality)
    
    return books


# ─── 缓存管理 ─────────────────────────────────────────

def _cache_file_path(date_str):
    """获取指定日期的缓存文件路径"""
    return os.path.join(CACHE_DIR, f"sanjiang_{date_str}.json")


def load_cache(date_str):
    """加载指定日期的缓存数据。
    
    返回格式：
    {
        "date": "2026-04-10",
        "fetched_at": "2026-04-10 19:30:05",
        "book_count": 25,
        "books": [
            {
                "book_id": "1048197630",
                "book_name": "xxx",
                "author": "xxx",
                "category": "玄幻 · 东方玄幻",
                "sbti_code": "FUCK",
                "sbti_name": "草者",
                "sbti_trait": "...",
                "sbti_reason": "...",
                ...
            },
            ...
        ]
    }
    
    返回 None 表示无缓存或缓存无效。
    """
    fpath = _cache_file_path(date_str)
    if not os.path.exists(fpath):
        return None
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        # 基本校验
        if not isinstance(data, dict) or "books" not in data:
            return None
        if not data["books"]:
            return None
        return data
    except (json.JSONDecodeError, IOError, KeyError):
        return None


def save_cache(date_str, books):
    """保存全量数据到缓存文件"""
    os.makedirs(CACHE_DIR, exist_ok=True)
    fpath = _cache_file_path(date_str)
    data = {
        "date": date_str,
        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "book_count": len(books),
        "books": books,
    }
    try:
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        fsize = os.path.getsize(fpath)
        print(f"[CACHE] 已缓存 {len(books)} 本书到 {fpath} ({fsize/1024:.1f} KB)", file=sys.stderr)
    except IOError as e:
        print(f"[WARN] 缓存写入失败: {e}", file=sys.stderr)


def cleanup_old_caches():
    """清理过期缓存文件（保留最近 CACHE_MAX_AGE_DAYS 天）"""
    if not os.path.isdir(CACHE_DIR):
        return
    cutoff = (datetime.now() - timedelta(days=CACHE_MAX_AGE_DAYS)).strftime("%Y-%m-%d")
    removed = 0
    for fname in os.listdir(CACHE_DIR):
        if not fname.startswith("sanjiang_") or not fname.endswith(".json"):
            continue
        # 从文件名提取日期：sanjiang_2026-04-10.json
        m = re.search(r"sanjiang_(\d{4}-\d{2}-\d{2})\.json", fname)
        if m and m.group(1) < cutoff:
            try:
                os.remove(os.path.join(CACHE_DIR, fname))
                removed += 1
            except OSError:
                pass
    if removed:
        print(f"[CACHE] 已清理 {removed} 个过期缓存文件", file=sys.stderr)


# ─── 历史记录管理 ─────────────────────────────────────
def load_history():
    """加载推荐历史记录"""
    if not os.path.exists(HISTORY_FILE):
        return {"last_book_ids": [], "last_date": "", "all_recommended": {}}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"last_book_ids": [], "last_date": "", "all_recommended": {}}


def save_history(book_ids, date_str):
    """保存本次推荐到历史记录"""
    history = load_history()
    history["last_book_ids"] = book_ids
    history["last_date"] = date_str
    if "all_recommended" not in history:
        history["all_recommended"] = {}
    history["all_recommended"][date_str] = book_ids
    cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    history["all_recommended"] = {
        k: v for k, v in history["all_recommended"].items() if k >= cutoff
    }
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"[WARN] 无法保存历史记录: {e}", file=sys.stderr)


def get_last_book_ids():
    """获取上一次推荐的书籍ID列表"""
    history = load_history()
    return history.get("last_book_ids", [])


# ─── 网络请求 ─────────────────────────────────────────
def http_get(url, retries=RETRY_COUNT):
    """带重试的 HTTP GET 请求"""
    for attempt in range(retries + 1):
        try:
            req = Request(url, headers=HEADERS)
            with urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                charset = resp.headers.get_content_charset() or "utf-8"
                return resp.read().decode(charset, errors="replace")
        except HTTPError as e:
            if e.code == 404:
                print(f"[WARN] 404 Not Found: {url}", file=sys.stderr)
                return None
            if attempt < retries:
                print(f"[WARN] HTTP {e.code}, retry {attempt+1}/{retries}: {url}", file=sys.stderr)
                time.sleep(RETRY_DELAY)
            else:
                print(f"[ERROR] HTTP {e.code} after {retries} retries: {url}", file=sys.stderr)
                return None
        except URLError as e:
            if attempt < retries:
                print(f"[WARN] URL Error, retry {attempt+1}/{retries}: {e}", file=sys.stderr)
                time.sleep(RETRY_DELAY)
            else:
                print(f"[ERROR] URL Error after {retries} retries: {e}", file=sys.stderr)
                return None
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}", file=sys.stderr)
            return None
    return None


# ─── 三江榜单列表解析 ─────────────────────────────────
def get_latest_sanjiang_date():
    """尝试获取最近的三江榜单日期（通常是周五更新）"""
    today = datetime.now()
    for i in range(8):
        check_date = today - timedelta(days=i)
        date_str = check_date.strftime("%Y-%m-%d")
        # 先检查本地有没有这天的缓存
        cached = load_cache(date_str)
        if cached:
            return date_str
        # 没缓存就去网络探测
        url = BASE_URL + SANJIANG_LIST_PATH.format(date=date_str)
        html = http_get(url)
        if html and "三江" in html:
            return date_str
    return today.strftime("%Y-%m-%d")


def parse_sanjiang_list(html):
    """解析三江榜单列表页，提取书籍基本信息"""
    books = []
    if not html:
        return books
    if not HAS_BS4:
        print("[ERROR] beautifulsoup4 is required.", file=sys.stderr)
        return books

    soup = BeautifulSoup(html, "lxml")

    rows = soup.select("table tbody tr")
    if rows:
        for row in rows:
            book = _parse_table_row(row)
            if book:
                books.append(book)

    if not books:
        items = soup.select("div.book-item, li.book-item, div.rank-item")
        for item in items:
            book = _parse_list_item(item)
            if book:
                books.append(book)

    if not books:
        books = _parse_links_fallback(soup)

    return books


def _parse_table_row(row):
    """解析表格行"""
    try:
        link_tag = row.select_one("a[href*='/info/']")
        if not link_tag:
            return None
        book_name = link_tag.get_text(strip=True)
        href = link_tag.get("href", "")
        book_id = _extract_book_id(href)
        if not book_id:
            return None
        author_tag = row.select_one("a[href*='/author/'], td:nth-child(3)")
        author = author_tag.get_text(strip=True) if author_tag else ""
        cat_tag = row.select_one("td:nth-child(2), span.cat, a[href*='/cat/']")
        category = cat_tag.get_text(strip=True) if cat_tag else ""
        return {
            "book_id": book_id,
            "book_name": book_name,
            "author": author,
            "category": category,
            "detail_url": BASE_URL + f"/info/{book_id}",
            "qidian_url": f"https://www.qidian.com/book/{book_id}/?_trace=qidiandayrec_skill",
        }
    except Exception:
        return None


def _parse_list_item(item):
    """解析列表项"""
    try:
        link_tag = item.select_one("a[href*='/info/']")
        if not link_tag:
            return None
        book_name = link_tag.get_text(strip=True)
        href = link_tag.get("href", "")
        book_id = _extract_book_id(href)
        if not book_id:
            return None
        author_tag = item.select_one("a[href*='/author/'], span.author")
        author = author_tag.get_text(strip=True) if author_tag else ""
        cat_tag = item.select_one("span.cat, a[href*='/cat/']")
        category = cat_tag.get_text(strip=True) if cat_tag else ""
        return {
            "book_id": book_id,
            "book_name": book_name,
            "author": author,
            "category": category,
            "detail_url": BASE_URL + f"/info/{book_id}",
            "qidian_url": f"https://www.qidian.com/book/{book_id}/?_trace=qidiandayrec_skill",
        }
    except Exception:
        return None


def _parse_links_fallback(soup):
    """最通用的兜底解析"""
    books = []
    seen_ids = set()
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        book_id = _extract_book_id(href)
        if book_id and book_id not in seen_ids:
            book_name = a_tag.get_text(strip=True)
            if book_name and len(book_name) > 1:
                seen_ids.add(book_id)
                books.append({
                    "book_id": book_id,
                    "book_name": book_name,
                    "author": "",
                    "category": "",
                    "detail_url": BASE_URL + f"/info/{book_id}",
                    "qidian_url": f"https://www.qidian.com/book/{book_id}/?_trace=qidiandayrec_skill",
                })
    return books


def _extract_book_id(href):
    """从链接中提取书籍ID"""
    m = re.search(r"/info/(\d+)", href)
    if m:
        return m.group(1)
    return None


# ─── 书籍详情解析 ─────────────────────────────────────
def fetch_book_detail(book_id):
    """获取单本书的详细信息"""
    url = BASE_URL + BOOK_INFO_PATH.format(book_id=book_id)
    html = http_get(url)
    if not html:
        return {}
    if not HAS_BS4:
        return {}

    soup = BeautifulSoup(html, "lxml")
    detail = {}
    text = soup.get_text()

    try:
        title_tag = soup.select_one("h1")
        if title_tag:
            name = title_tag.get_text(strip=True)
            name = re.sub(r"\(VIP\).*", "", name).strip()
            detail["book_name"] = name

        m = re.search(r"作者[：:]\s*([^\(（]+)", text)
        if m:
            detail["author"] = m.group(1).strip()

        m = re.search(r"标签[：:]\s*([^\s　]+)\s*([^\s　]*)", text)
        if m:
            cat = m.group(1).strip()
            sub_cat = m.group(2).strip()
            detail["category"] = f"{cat} · {sub_cat}" if sub_cat else cat

        m = re.search(r"状态[：:]\s*(\S+)", text)
        if m:
            detail["status"] = m.group(1).strip()

        m = re.search(r"总字数[：:]\s*(\d+[\.\d]*万?)", text)
        if m:
            detail["word_count"] = m.group(1)

        m = re.search(r"总收藏[：:]\s*(\d+[\.\d]*万?)", text)
        if m:
            detail["collect"] = m.group(1)

        m = re.search(r"总推荐[：:]\s*(\d+[\.\d]*万?k?)", text)
        if m:
            detail["recommend"] = m.group(1)

        m = re.search(r"首订[：:]\s*(\d+)", text)
        if m:
            detail["first_order"] = m.group(1)

        m = re.search(r"真实粉丝数[：:]\s*(\d+[\.\d]*万?k?)", text)
        if m:
            detail["fans"] = m.group(1)

        intro = ""
        m = re.search(r"简介及书单.*?\n+(.*?)(?:展开更多简介|收起)", text, re.DOTALL)
        if m:
            intro = m.group(1).strip()
            intro = re.sub(r"\s+", " ", intro)
            intro = intro.replace("\u3000", " ").strip()
        
        if not intro:
            m = re.search(r"数据\s*\n+(.*?)(?:展开更多简介|收起|书单)", text, re.DOTALL)
            if m:
                intro = m.group(1).strip()
                intro = re.sub(r"\s+", " ", intro)
                intro = intro.replace("\u3000", " ").strip()

        if not intro:
            for p in soup.find_all(string=True):
                p_text = p.strip()
                if len(p_text) > 100 and "起点图" not in p_text and "鲁ICP" not in p_text:
                    intro = re.sub(r"\s+", " ", p_text.replace("\u3000", " ")).strip()
                    break

        if intro:
            detail["intro"] = intro

    except Exception as e:
        print(f"[WARN] Error parsing detail for book {book_id}: {e}", file=sys.stderr)

    return detail


# ─── 全量抓取 + 预标注（首次请求时执行）──────────────────

def fetch_and_cache_all(date_str):
    """
    全量抓取三江榜单：获取列表 → 逐本获取详情 → 预打 SBTI 标签 → 写入缓存。
    
    这是唯一会产生网络请求的路径。后续所有请求直接读缓存。
    
    返回: 带完整详情和 SBTI 标签的书籍列表
    """
    # 1. 获取榜单列表
    list_url = BASE_URL + SANJIANG_LIST_PATH.format(date=date_str)
    print(f"[FETCH] 正在从起点图获取三江榜单: {list_url}", file=sys.stderr)
    html = http_get(list_url)
    if not html:
        print("[ERROR] 无法获取三江榜单页面", file=sys.stderr)
        return []

    books = parse_sanjiang_list(html)
    if not books:
        print("[ERROR] 未解析到任何书籍信息", file=sys.stderr)
        return []
    print(f"[FETCH] 解析到 {len(books)} 本书，开始获取全量详情...", file=sys.stderr)

    # 2. 逐本获取详情
    enriched = []
    for i, book in enumerate(books, 1):
        print(f"[FETCH] ({i}/{len(books)}) 获取详情: {book['book_name']}...", file=sys.stderr)
        detail = fetch_book_detail(book["book_id"])
        merged = {**book, **detail}
        merged.setdefault("book_name", f"未知书名({book['book_id']})")
        merged.setdefault("author", "未知作者")
        merged.setdefault("category", "未知分类")
        merged.setdefault("intro", "暂无简介")
        merged.setdefault("word_count", "")
        merged.setdefault("collect", "")
        merged.setdefault("recommend", "")
        
        # 3. 预打 SBTI 标签（每本书各自的最佳匹配，不做批次去重）
        merged = label_single_book_sbti(merged)
        
        enriched.append(merged)
        # 请求间隔，善待源站
        if i < len(books):
            time.sleep(1.5)

    # 4. 写入缓存
    save_cache(date_str, enriched)
    
    # 5. 清理过期缓存
    cleanup_old_caches()

    return enriched


def get_books_with_cache(date_str, force_refresh=False):
    """
    获取书籍数据（优先读缓存，缓存不存在则全量抓取）。
    
    这是数据获取的唯一入口，所有推荐逻辑都应该通过这里拿数据。
    
    参数:
      date_str: 榜单日期
      force_refresh: True=忽略缓存强制重新抓取
    
    返回: 带完整详情和 SBTI 标签的书籍列表
    """
    if not force_refresh:
        cached = load_cache(date_str)
        if cached:
            books = cached["books"]
            print(f"[CACHE] ✅ 命中缓存！{cached['book_count']} 本书 "
                  f"(缓存时间: {cached['fetched_at']})", file=sys.stderr)
            return books
        else:
            print(f"[CACHE] 未命中缓存，将从起点图全量抓取...", file=sys.stderr)
    else:
        print(f"[CACHE] 强制刷新，忽略已有缓存...", file=sys.stderr)
    
    return fetch_and_cache_all(date_str)


# ─── 书籍筛选与推荐 ───────────────────────────────────

def pick_best_books(books, count=3, exclude_ids=None, sbti_filter=None):
    """
    从书籍池中挑选推荐书籍。
    
    筛选策略（按优先级）：
    1. SBTI 筛选（如果指定了 --sbti）：只从匹配的人格中选
    2. 去重：排除上次推荐的书籍
    3. 随机轮换：打乱顺序
    4. 分类多样性：尽量覆盖不同分类
    5. 兜底：候选不足时放宽条件
    """
    if exclude_ids is None:
        exclude_ids = set()
    else:
        exclude_ids = set(exclude_ids)

    candidates = list(books)
    
    # SBTI 人格筛选
    if sbti_filter:
        target_codes = set(p["code"] for p in sbti_filter)
        sbti_matched = [b for b in candidates if b.get("sbti_code") in target_codes]
        if sbti_matched:
            print(f"[FILTER] SBTI筛选: {[p['code']+'('+p['name']+')' for p in sbti_filter]} "
                  f"→ 匹配 {len(sbti_matched)} 本", file=sys.stderr)
            candidates = sbti_matched
        else:
            # 没有精确匹配，放宽到分类关键词匹配
            all_keywords = set()
            for p in sbti_filter:
                all_keywords.update(p["keywords"])
            kw_matched = [b for b in candidates 
                         if any(kw in b.get("category", "") for kw in all_keywords)]
            if kw_matched:
                print(f"[FILTER] SBTI精确匹配为空，按关键词放宽 → 匹配 {len(kw_matched)} 本", file=sys.stderr)
                candidates = kw_matched
            else:
                print(f"[FILTER] SBTI筛选无匹配，使用全量候选池", file=sys.stderr)

    # 去重
    deduped = [b for b in candidates if b["book_id"] not in exclude_ids]
    if len(deduped) < count:
        print(f"[WARN] 去重后仅剩 {len(deduped)} 本候选，回退到全量选择", file=sys.stderr)
        deduped = list(candidates)

    # 随机打乱
    random.shuffle(deduped)

    # 按分类多样性挑选
    selected = []
    used_categories = set()
    remaining = list(deduped)

    for book in remaining[:]:
        if len(selected) >= count:
            break
        cat = book.get("category", "")
        if cat and cat not in used_categories:
            selected.append(book)
            used_categories.add(cat)
            remaining.remove(book)

    for book in remaining:
        if len(selected) >= count:
            break
        if book not in selected:
            selected.append(book)

    return selected[:count]


# ─── 输出格式化 ───────────────────────────────────────
def format_markdown(books, date_str, sbti_query=None):
    """格式化为 Markdown"""
    sbti_note = ""
    if sbti_query:
        sbti_note = f"\n> 🎯 已按你的性格「{sbti_query}」筛选推荐\n"
    
    lines = [
        f"# 📚 三江好书推荐 | {date_str}",
        "",
        f"> 本期从起点三江榜单中精选 {len(books)} 本优质好书，每本都配了 SBTI 人格鉴定，对号入座！",
        sbti_note,
    ]

    for i, book in enumerate(books, 1):
        sbti_tag = ""
        if book.get("sbti_code"):
            sbti_tag = f" 🏷️ SBTI：{book['sbti_code']}（{book['sbti_name']}）"
        
        lines.append(f"## {i}. 《{book['book_name']}》{sbti_tag}")
        lines.append("")
        lines.append("| 项目 | 信息 |")
        lines.append("|------|------|")
        lines.append(f"| 作者 | {book['author']} |")
        lines.append(f"| 分类 | {book['category']} |")
        if book.get("word_count"):
            lines.append(f"| 字数 | {book['word_count']} |")
        if book.get("collect"):
            lines.append(f"| 收藏 | {book['collect']} |")
        if book.get("recommend"):
            lines.append(f"| 推荐票 | {book['recommend']} |")
        lines.append(f"| 起点链接 | [点击阅读]({book.get('qidian_url', '')}) |")
        lines.append("")
        
        if book.get("sbti_reason"):
            lines.append("**🎭 必看理由：**")
            lines.append("")
            lines.append(f"> {book['sbti_reason']}")
            lines.append("")
        
        lines.append("**📖 简介：**")
        lines.append("")
        intro = book.get("intro", "暂无简介")
        if len(intro) > 500:
            intro = intro[:500] + "…"
        lines.append(f"> {intro}")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append(f"*数据来源：起点图 (qidiantu.com) | SBTI人格鉴定纯属娱乐 | 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    return "\n".join(lines)


def format_text(books, date_str, sbti_query=None):
    """格式化为纯文本"""
    sbti_note = ""
    if sbti_query:
        sbti_note = f"\n🎯 已按性格「{sbti_query}」筛选推荐\n"
    
    lines = [
        f"📚 三江好书推荐 | {date_str}",
        f"本期从起点三江榜单中精选 {len(books)} 本优质好书，附 SBTI 人格鉴定",
        sbti_note,
        "=" * 50,
    ]

    for i, book in enumerate(books, 1):
        sbti_tag = ""
        if book.get("sbti_code"):
            sbti_tag = f" 🏷️SBTI: {book['sbti_code']}（{book['sbti_name']}）"
        
        lines.append("")
        lines.append(f"【{i}】《{book['book_name']}》{sbti_tag}")
        lines.append(f"  作者：{book['author']}")
        lines.append(f"  分类：{book['category']}")
        if book.get("word_count"):
            lines.append(f"  字数：{book['word_count']}")
        if book.get("collect"):
            lines.append(f"  收藏：{book['collect']}")
        lines.append(f"  链接：{book.get('qidian_url', '')}")
        if book.get("sbti_reason"):
            lines.append(f"  🎭必看理由：{book['sbti_reason']}")
        intro = book.get("intro", "暂无简介")
        if len(intro) > 300:
            intro = intro[:300] + "…"
        lines.append(f"  简介：{intro}")

    lines.append("")
    lines.append(f"数据来源：起点图 | SBTI鉴定纯属娱乐 | 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    return "\n".join(lines)


def format_sbti_list():
    """格式化 SBTI 人格列表"""
    lines = [
        "# 🎭 SBTI 人格大全（2026年4月版）",
        "",
        "| 代号 | 人格名 | 特征 | 适配小说类型 |",
        "|------|--------|------|-------------|",
    ]
    for p in SBTI_PERSONALITIES:
        kws = "、".join(p["keywords"][:4])
        lines.append(f"| {p['code']} | {p['name']} | {p['trait']} | {kws} |")
    lines.append("")
    lines.append("用法示例：")
    lines.append("```")
    lines.append("python3 sanjiang_picker.py --sbti MALO        # 按代号筛选")
    lines.append("python3 sanjiang_picker.py --sbti 吗喽        # 按中文名筛选")
    lines.append("python3 sanjiang_picker.py --sbti 躺平         # 按性格描述筛选")
    lines.append("python3 sanjiang_picker.py --sbti 社恐独来独往  # 自由描述")
    lines.append("```")
    return "\n".join(lines)


# ─── 主流程 ───────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="起点三江榜单好书推荐（支持 SBTI 性格筛选）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  %(prog)s                          # 默认推荐3本
  %(prog)s --count 5                # 推荐5本
  %(prog)s --sbti MALO              # 推荐适合"吗喽"人格的书
  %(prog)s --sbti 躺平              # 按性格描述推荐
  %(prog)s --sbti 社恐独行侠        # 自由描述性格
  %(prog)s --list-sbti              # 查看所有SBTI人格
  %(prog)s --refresh                # 强制刷新缓存
  %(prog)s --dump-cache             # 输出完整缓存数据
        """
    )
    parser.add_argument("--count", type=int, default=3, help="推荐书籍数量（默认3本）")
    parser.add_argument("--date", type=str, default=None, help="榜单日期 YYYY-MM-DD（默认自动获取最新）")
    parser.add_argument("--output", type=str, default="markdown", choices=["json", "markdown", "text"],
                        help="输出格式（默认markdown）")
    parser.add_argument("--sbti", type=str, default=None,
                        help="按 SBTI 人格筛选推荐（支持代号/中文名/性格描述）")
    parser.add_argument("--list-sbti", action="store_true", help="列出所有 SBTI 人格类型")
    parser.add_argument("--refresh", action="store_true", help="强制刷新缓存（忽略已有缓存重新抓取）")
    parser.add_argument("--dump-cache", action="store_true", help="输出当天完整缓存数据（JSON格式）")
    parser.add_argument("--no-save", action="store_true", help="不保存本次推荐到历史（用于测试）")
    parser.add_argument("--setup", action="store_true", help="仅检测环境并安装依赖，不执行推荐")
    args = parser.parse_args()

    # --setup 模式
    if args.setup:
        ok = setup_environment()
        sys.exit(0 if ok else 1)

    # --list-sbti 模式
    if args.list_sbti:
        print(format_sbti_list())
        sys.exit(0)

    # 检查依赖
    if not HAS_BS4:
        print("[ERROR] 核心依赖未安装且自动安装失败。", file=sys.stderr)
        print("[HINT] 请手动执行: pip3 install beautifulsoup4 lxml", file=sys.stderr)
        sys.exit(1)

    # 1. 确定榜单日期
    if args.date:
        date_str = args.date
    else:
        print("[INFO] 正在获取最新三江榜单日期...", file=sys.stderr)
        date_str = get_latest_sanjiang_date()
    print(f"[INFO] 使用榜单日期: {date_str}", file=sys.stderr)

    # 2. 获取数据（优先缓存）
    books = get_books_with_cache(date_str, force_refresh=args.refresh)
    if not books:
        print("[ERROR] 无法获取任何书籍数据", file=sys.stderr)
        sys.exit(1)
    print(f"[INFO] 候选池: {len(books)} 本书", file=sys.stderr)

    # --dump-cache 模式：直接输出全量缓存
    if args.dump_cache:
        print(json.dumps(books, ensure_ascii=False, indent=2))
        sys.exit(0)

    # 3. 解析 SBTI 筛选条件
    sbti_filter = None
    if args.sbti:
        sbti_filter = resolve_sbti_filter(args.sbti)
        if sbti_filter:
            matched_names = [f"{p['code']}({p['name']})" for p in sbti_filter]
            print(f"[SBTI] 匹配人格: {', '.join(matched_names)}", file=sys.stderr)
        else:
            print(f"[SBTI] 未匹配到任何人格，将使用全量候选池", file=sys.stderr)

    # 4. 获取上次推荐记录（用于去重）
    last_ids = get_last_book_ids()
    if last_ids:
        print(f"[INFO] 上次推荐: {last_ids}，本次将排除", file=sys.stderr)

    # 5. 挑选推荐
    selected = pick_best_books(books, count=args.count, exclude_ids=last_ids, sbti_filter=sbti_filter)
    print(f"[INFO] 精选 {len(selected)} 本推荐", file=sys.stderr)

    # 6. 对最终推荐批次做 SBTI 去重（同批不重复人格）
    selected = dedupe_sbti_in_batch(selected)

    # 7. 保存本次推荐到历史
    if not args.no_save:
        selected_ids = [b["book_id"] for b in selected]
        save_history(selected_ids, date_str)
        print(f"[INFO] 已保存本次推荐到历史记录", file=sys.stderr)

    # 8. 输出
    if args.output == "json":
        output = json.dumps(selected, ensure_ascii=False, indent=2)
    elif args.output == "text":
        output = format_text(selected, date_str, sbti_query=args.sbti)
    else:
        output = format_markdown(selected, date_str, sbti_query=args.sbti)

    print(output)


if __name__ == "__main__":
    main()
