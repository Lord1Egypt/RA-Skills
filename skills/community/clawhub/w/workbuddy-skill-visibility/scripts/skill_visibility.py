# -*- coding: utf-8 -*-
"""让 WorkBuddy 的内置技能出现在技能列表里，并支持完整复原。

为什么需要它
    技能列表只渲染来源为用户技能（source=userSettings）的条目，内置技能
    （source=builtin）被前端显式过滤掉，所以界面上一个都看不到。
    把内置技能复制一份到用户技能目录下，扫描器就会按用户技能收录；
    同名的内置那份在扫描阶段被按名去重跳过，所以列表里不会出现重复条目。

两条路，各管一段
    一是副本方案（默认，推荐）：把内置技能复制成用户技能目录里的副本。
    二是改前端 bundle（可用，但**不建议**，理由见下文专节）：直接改前端的过滤函数。
    两条路目标相同、实现互不依赖；都保留着，但不要并用。

路径全部运行时推导，不写死任何目录
    安装目录与配置目录都在运行时探测，探测结果可用环境变量或命令行开关覆盖：
        --app-root DIR      WorkBuddy 安装目录（环境变量 WORKBUDDY_APP_ROOT）
        --config-dir DIR    用户配置目录，默认 ~/.workbuddy（环境变量 WORKBUDDY_CONFIG_DIR）
    探测到但结构对不上时会明确报错并给出提示，不会去猜、更不会去改别的地方。

清单文件是可选的
    与本脚本同目录的 skill_visibility_manifest.json 记着"哪些副本是本脚本建的"。
    它**不是必须的**：删掉它脚本照常工作——技能目录里凡是内容与内置原件对得上的副本，
    都能被当场指纹识别并重新纳管，下一次 sync 会把清单重建出来。
    它多兜住一件事，是指纹替代不了的：应用升级后内置原件会变，副本与原件就不再一致，
    那时光靠指纹会把它看成"你自己装的技能"而不敢碰；有清单才认得出"这是我建的、只是旧了"，
    于是能更新它、也能删掉它。所以建议留着，但丢了也不必慌。

命令
    sync            复制并更新副本（不带参数时的默认命令）
    list            只列出会同步哪些，不动文件
    status          查看每个副本与内置原件是否一致
    restore [名字…] 删除副本，复原到操作前的状态；不给名字就全量
    bundle          给前端 bundle 打补丁，默认**只演练、不写盘**
    bundle-status   看 bundle 现在是原样还是已打补丁
    bundle-restore  从备份还原 bundle（救援动作，直接生效）

开关
    --dry-run       restore / bundle-restore 只演练不落盘，打印会动哪些、动多少
    --force         sync：撤回数量异常时也照做；restore：连"被改动过"的副本也删；
                    bundle：真正写盘（不加就只演练）
    --app-root / --config-dir   覆盖自动探测到的路径
    -h, --help      打印本文档
    --version       打印版本号

安全约定
    副本只从清单与"内容与内置原件对得上"这两个线索里认，两条都对不上的目录一律不碰，
    所以你自己装的技能不会被误删。
    全量复原时会把"清单外的可识别副本"一并纳入，清单丢了也不留残渣。
    restore 删除前会逐目录比对内容指纹：只要副本与内置原件不一致，
    就判定为"被改动过"并跳过、打印告警，需要显式加 --force 才删。
    删除时对链接只用删链接本身的方式，不会顺着链接删掉真目录。

名单是动态的，不是写死的
    每次运行都当场重新判定该复制哪些，依据两条：
    一是扫描内置技能目录并逐个读前置声明（有 SKILL.md）；
    二是读应用自己的技能索引缓存，它认可的内置技能才算数——磁盘上有而索引里没有的，
    说明应用当前不认它（多半按策略禁用了），不复制。
    所以内置技能新增、删除、改名、改声明，或者应用的认可名单变化，重跑一次就会自动跟上：
    新出现的会自动复制，不再该有的会从清单撤下并删掉副本。
    原件本身始终留在应用安装目录，脚本只读它；应用升级后重跑一次即可追平。

声明翻转（副本与原件不完全一致的那部分）
    内置技能里有一批声明了 user-invocable: false。前端对这类技能照旧过滤，原样复制过去
    界面里照样看不到，等于白发。所以脚本会在**副本**里把这一条翻成 true，让它能被列出来。
    只翻 user-invocable，disable-model-invocation 一律不动：后者表达的是"别让模型自动挑中我"，
    对必须与领域 skill 配对使用的决策层，这条约束要保留，
    否则模型可能单独选中一个自己站不住的中间层。
    改动只落在副本的 SKILL.md 前置声明块内，内置原件一个字节都不碰。
    因此这类副本不再与原件逐字节相同，一致性判定改走"副本 == 原件 patch 之后"的指纹：
    它们在 status 里照样报"一致"，restore 也不会把副本误判成"你改过的文件"。

改前端 bundle 这条路（脚本里做了，但**不建议用**）
    另一条路是直接改前端 chunk 里的过滤函数，让内置技能从"被过滤"变成"直接放行"。
    技术上成立，脚本也实现了，但请优先用副本方案。不建议的理由，按轻重排：
    一是它改的是**应用安装目录里的分发产物**。任何一次版本更新都会整包覆盖，改动静默丢失；
        而且文件名 contexts-XXXX.js 里的 XXXX 是内容哈希，升级后名字会变，
        所以脚本只能靠"glob contexts-*.js + 在内容里找锚点"来定位，不能写死文件名。
    二是它的失败模式比副本方案重得多。那个 chunk 在首屏关键路径上
        （入口的动态加载链里 bootstrap 静态依赖它，app-shell 的静态闭包也含它），
        一旦被改坏，外壳层和对话面板一起加载失败，**整个界面白屏，连对话窗口都打不开**。
    三是脚本虽然把白屏概率压得很低（先备份、先在临时副本上做语法体检、体检不过就不落盘、
        落盘后再复核锚点，任何一步不对就回滚），但语法体检只查语法，
        **查不出语义错误**——语法合法、行为错误，界面照样可能坏。
    四是它放不出应用后端根本不返回的技能。改前端过滤对这种技能没用。
    五是它与副本方案冗余。副本已经把内置技能顶替成用户技能，所以改 bundle 在这件事上
        不会再多出什么，只在"插件类、nested 类技能"上多放一点。
    两条路都能用，但不要并用，也不要在没备份的情况下试。

原件不会被改动
    内置技能原件始终留在应用安装目录里，本脚本只读它。
    应用升级后会更新原件，副本会滞后，重跑一次 sync 即可追平。
    bundle 那条路是唯一的例外：它确实会写应用安装目录里的文件（写前先留 .wb-orig.bak 备份）。
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

VERSION = "1.0.0"
HERE = os.path.dirname(os.path.abspath(__file__))
PROG = os.path.basename(sys.argv[0]) or "skill_visibility.py"

# 环境变量名，供覆盖自动探测到的路径。
ENV_APP_ROOT = "WORKBUDDY_APP_ROOT"
ENV_CONFIG_DIR = "WORKBUDDY_CONFIG_DIR"

# 清单文件名（可选文件）与改名前用过的旧名。
MANIFEST_NAME = "skill_visibility_manifest.json"
LEGACY_MANIFEST_NAMES = ["内置技能副本-清单.json"]

# 手动兜底的排除名单，正常留空。要放东西请连同理由写清楚，它优先于索引判定。
MANUAL_SKIP = {}

# 内置技能的 SKILL.md 前置声明块。
FRONT = re.compile(r"^---\s*\r?\n(.*?)\r?\n---", re.S)

# 副本里要翻转的前置声明字段，目前只有一条：user-invocable: false → true。
# 只翻这一条，因为它决定技能会不会出现在列表里；disable-model-invocation 不动，
# 那一条表达的是"别让模型自动挑中我"，对必须与领域 skill 配对使用的决策层，
# 这个约束得保留，否则模型可能单独挑中一个自己站不住的中间层。
USER_INVOCABLE_FALSE = re.compile(
    r"^([ \t]*user-invocable[ \t]*:[ \t]*)[\"']?false[\"']?([ \t]*)$", re.M
)

# ---- 改前端 bundle 那条路用到的常量（可用，但不建议，见文件开头）----

BUNDLE_BACKUP_SUFFIX = ".wb-orig.bak"

# 补丁清单：(说明, 原式, 新式)。每条都要求**全文恰好命中 1 次**才动手，否则原样跳过。
# 第二条的锚点必须带上函数名 filterPersonalSkillsByCwd：里面那个 filter 表达式
# 在全文出现两次，另一处属于 isUserInvocableSkill，光靠表达式会改错地方。
BUNDLE_PATCHES = (
    (
        "已安装技能列表：不再排除内置技能",
        "isInstalledListVisibleSkill(e){return e.userInvocable!==!1&&e.source!==`builtin`"
        "&&e.source!==`connector`&&!e.nested&&!isPluginOwnedSkill(e)}",
        "isInstalledListVisibleSkill(e){return e.userInvocable!==!1"
        "&&e.source!==`connector`&&!e.nested&&!isPluginOwnedSkill(e)}",
    ),
    (
        "唤起列表：不再排除内置技能",
        "filterPersonalSkillsByCwd(e,t){let n=e.filter(e=>e.userInvocable!==!1&&!isBuiltinPluginSkill(e))",
        "filterPersonalSkillsByCwd(e,t){let n=e.filter(e=>e.userInvocable!==!1)",
    ),
)


# ============================================================
# 一、路径：全部运行时推导，不写死任何用户目录
# ============================================================


class Paths(object):
    """一次运行用到的全部路径，集中一处，便于被 --app-root / --config-dir 覆盖。"""

    def __init__(self, app_root, config_dir):
        # 规范化一下：用户传进来的路径可能用正斜杠，混着显示不好看。
        self.app_root = os.path.normpath(app_root) if app_root else None
        self.config_dir = os.path.normpath(config_dir) if config_dir else None
        app_root, config_dir = self.app_root, self.config_dir
        # 应用装机目录里，Electron 把 app.asar 解包出来的那一层。
        self.unpacked = (
            os.path.join(app_root, "resources", "app.asar.unpacked") if app_root else None
        )
        self.builtin = (
            os.path.join(self.unpacked, "resources", "plugins", "workbuddy-builtin", "skills")
            if self.unpacked
            else None
        )
        self.renderer_assets = (
            os.path.join(self.unpacked, "renderer", "assets") if self.unpacked else None
        )
        self.skills_dir = os.path.join(config_dir, "skills") if config_dir else None
        self.index_cache = (
            os.path.join(config_dir, ".skill-list-cache.json") if config_dir else None
        )
        self.manifest = os.path.join(HERE, MANIFEST_NAME)
        self.legacy_manifests = [os.path.join(HERE, n) for n in LEGACY_MANIFEST_NAMES]

    def has_builtin(self):
        return bool(self.builtin) and os.path.isdir(self.builtin)

    def has_renderer(self):
        return bool(self.renderer_assets) and os.path.isdir(self.renderer_assets)

    def summary(self):
        return [
            ("安装目录", self.app_root),
            ("内置技能目录", self.builtin),
            ("用户技能目录", self.skills_dir),
            ("技能索引缓存", self.index_cache),
        ]


def candidate_app_roots():
    """应用安装目录的候选位置。

    只列出能验证的形态：本机实测 Windows 版装在 %LOCALAPPDATA%\\Programs\\WorkBuddy。
    其它平台/自定义安装一律用 --app-root 显式指定——不猜未经验证的目录约定。
    """
    out = []
    for env in (ENV_APP_ROOT,):
        val = os.environ.get(env)
        if val:
            out.append(val)
    local = os.environ.get("LOCALAPPDATA")
    if local:
        out.append(os.path.join(local, "Programs", "WorkBuddy"))
    for var in ("ProgramFiles", "ProgramFiles(x86)"):
        base = os.environ.get(var)
        if base:
            out.append(os.path.join(base, "WorkBuddy"))
    return out


def candidate_config_dirs():
    """用户配置目录的候选位置：环境变量优先，其次 ~/.workbuddy。"""
    out = []
    val = os.environ.get(ENV_CONFIG_DIR)
    if val:
        out.append(val)
    home = os.path.expanduser("~")
    if home and home != "~":
        out.append(os.path.join(home, ".workbuddy"))
    return out


def pick_existing(candidates, check):
    """按顺序取第一个通过 check 的候选；都不通过返回 None。"""
    for item in candidates:
        if item and check(item):
            return item
    return None


def is_app_root(path):
    return os.path.isdir(os.path.join(path, "resources", "app.asar.unpacked"))


def resolve_paths(app_root=None, config_dir=None):
    """确定本次运行的全部路径。显式参数 > 环境变量 > 自动探测。"""
    root = app_root or pick_existing(candidate_app_roots(), is_app_root)
    cfg = config_dir or pick_existing(candidate_config_dirs(), os.path.isdir)
    if cfg is None:
        # 配置目录可能还没被应用创建过——退回首选候选，由 sync 按需建。
        cfg = (candidate_config_dirs() or [None])[0]
    return Paths(root, cfg)


P = resolve_paths()


def require_builtin():
    """确认内置技能目录可用。不可用就打印排查提示。"""
    if P.has_builtin():
        return True
    print("找不到内置技能目录：%s" % (P.builtin or "(未探测到安装目录)"))
    if not P.app_root:
        print("没能自动探测到 WorkBuddy 安装目录。请用 --app-root 指定，")
        print("或设置环境变量 %s。" % ENV_APP_ROOT)
    else:
        print("已按 %s 当作安装目录，但结构对不上（缺 resources/app.asar.unpacked）。" % P.app_root)
        print("请用 --app-root 指定正确的安装目录。")
    return False


def require_renderer():
    """确认前端 assets 目录可用（只有 bundle 那条路需要）。"""
    if P.has_renderer():
        return True
    print("找不到前端资源目录：%s" % (P.renderer_assets or "(未探测到安装目录)"))
    print("请用 --app-root 指定正确的安装目录，或改用副本方案（sync）。")
    return False


# ============================================================
# 二、内容指纹与前置声明
# ============================================================


def read_text(path):
    """按字节读、按 utf-8 解，避免文本模式把 CRLF 折成 LF 破坏往返一致。"""
    with open(path, "rb") as handle:
        return handle.read().decode("utf-8", errors="replace")


def frontmatter(skill_dir):
    """取出 SKILL.md 的前置声明块正文；没有 SKILL.md 返回 None，没有声明块返回空串。"""
    path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(path):
        return None
    match = FRONT.match(read_text(path))
    return match.group(1) if match else ""


def field(front, key):
    match = re.search(r"^%s\s*:\s*(.+)$" % re.escape(key), front, re.M)
    return match.group(1).strip().strip("\"'") if match else ""


def needs_patch(skill_dir):
    """该技能是否需要在副本里翻转前置声明。

    判据只看原件的声明：user-invocable 为 false 的才要翻。
    """
    front = frontmatter(skill_dir)
    return front is not None and field(front, "user-invocable").lower() == "false"


def patch_frontmatter(text):
    """把 SKILL.md 前置声明里该翻的字段翻过来，块外内容原样保留。

    只在开头那个 --- 块里替换；没匹配到或块外出现同样的行都不动。
    声明本来就是 true（或没写）时原样返回，因此对不需要翻转的技能是无操作。
    """
    match = FRONT.match(text)
    if not match:
        return text
    block = match.group(1)
    new_block = USER_INVOCABLE_FALSE.sub(r"\g<1>true\g<2>", block)
    if new_block == block:
        return text
    return text[: match.start(1)] + new_block + text[match.end(1) :]


def apply_patch(skill_dir):
    """把补丁写进副本的 SKILL.md。返回是否真的改了内容。

    写之前先确认"解码再编码"能还原成原来那串字节；还原不了说明文件里有非法字节，
    这时宁可不打补丁，也不冒险把文件写坏——副本仍与原件逐字节一致，一切照旧。
    """
    path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(path):
        return False
    with open(path, "rb") as handle:
        raw = handle.read()
    text = read_text(path)
    new_text = patch_frontmatter(text)
    if new_text == text or text.encode("utf-8") != raw:
        return False
    with open(path, "wb") as handle:
        handle.write(new_text.encode("utf-8"))
    return True


def tree_hash(skill_dir, patch=False):
    """目录内容指纹：把相对路径与文件内容按稳定顺序喂进 sha256。

    patch=True 时，顶层 SKILL.md 按"打过补丁之后"的内容参与计算，
    用来跟已翻转声明的副本对齐；内容没变时仍旧吃原始字节，保证往返一致。

    注意：这个算法是既有副本的判定基准，改动会让所有已存在的副本被判为"滞后"。
    """
    digest = hashlib.sha256()
    if not os.path.isdir(skill_dir):
        return None
    for root, dirs, files in os.walk(skill_dir):
        dirs.sort()
        rel = os.path.relpath(root, skill_dir)
        digest.update(rel.replace("\\", "/").encode("utf-8"))
        for name in sorted(files):
            digest.update(name.encode("utf-8"))
            full = os.path.join(root, name)
            try:
                with open(full, "rb") as handle:
                    raw = handle.read()
                # 只有顶层 SKILL.md 可能被补丁碰到；内容没变就仍旧吃原始字节。
                if patch and rel == "." and name == "SKILL.md":
                    text = raw.decode("utf-8", errors="replace")
                    new_text = patch_frontmatter(text)
                    if new_text != text:
                        raw = new_text.encode("utf-8")
                digest.update(raw)
            except OSError:
                pass
    return digest.hexdigest()[:16]


def target_hash(skill_dir):
    """副本"应该长成什么样"的指纹，即原件打过补丁之后。

    对不需要翻转的技能，它与 tree_hash(原件) 完全相同。
    """
    return tree_hash(skill_dir, patch=True)


def count_files(skill_dir):
    total = 0
    for _, _, files in os.walk(skill_dir):
        total += len(files)
    return total


# ============================================================
# 三、该复制哪些：当场扫描 + 应用实时索引
# ============================================================


def app_active_builtin_dirs():
    """从应用自己的技能索引里读出"应用当前认得的内置技能"目录名集合。

    **不能只看 source=builtin 的条目**：副本一旦就位，同名的内置项会在扫描阶段被
    按名去重跳过，索引里就不再以 builtin 出现，只看 builtin 会把它们误判成"已被禁用"，
    进而把副本成批撤掉——这是一个自我毁灭的反馈回路。
    所以这里取**所有**索引条目 filePath 的父目录名做并集：
    内置原件的路径是 …\\workbuddy-builtin\\skills\\<名>\\SKILL.md，
    副本的路径是 …\\.workbuddy\\skills\\<名>\\SKILL.md，两者父目录名相同，并集不受顶替影响。
    真正被策略禁用的内置技能在任何来源下都不出现，于是被正确排除。

    按父目录名取而不是按 name：内置技能的显示名可能是中文，用名字对不上。

    返回 None 表示索引读不到或条目太少不可信，此时跳过这层判定。
    """
    if not P.index_cache:
        return None
    try:
        with open(P.index_cache, encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception:
        return None
    results = data.get("results")
    if not isinstance(results, list):
        return None
    active = set()
    for item in results:
        path = item.get("filePath") or ""
        if path:
            active.add(os.path.basename(os.path.dirname(path)))
        elif item.get("name"):
            active.add(item["name"])
    # 索引可能刚好写到一半或残缺，条目太少就判定为不可信，退回"只按前置声明过滤"，
    # 免得因为一份半截索引把已有副本成批撤掉。
    return active if len(active) >= 5 else None


def candidates():
    """动态算出该复制哪些内置技能。

    判定全部来自当场扫描与应用的实时索引，没有任何写死的名单：
    磁盘上有目录 + 有 SKILL.md + 应用索引里认得它。
    对声明了 user-invocable: false 的，不跳过，而是标上"需翻转声明"，
    复制后在副本里把这一条改成 true——否则复制过去界面照样看不到。

    返回 (picked, skipped)，picked 每项是 (目录名, 显示名, 原件路径, 是否需翻转)。
    """
    active = app_active_builtin_dirs()
    picked, skipped = [], []
    for name in sorted(os.listdir(P.builtin)):
        src = os.path.join(P.builtin, name)
        if not os.path.isdir(src):
            continue
        front = frontmatter(src)
        if front is None:
            skipped.append((name, "没有 SKILL.md"))
            continue
        if name in MANUAL_SKIP:
            skipped.append((name, MANUAL_SKIP[name]))
            continue
        if active is not None and name not in active:
            skipped.append((name, "应用索引里没有它，多半已被策略禁用"))
            continue
        picked.append((name, field(front, "name") or name, src, needs_patch(src)))
    return picked, skipped


def discover_copies():
    """在用户技能目录里认出"内容与某个内置原件对得上"的目录。

    对得上分两种：与原件逐字节一致（原样副本），或与"原件 patch 之后"一致
    （翻转了 user-invocable 的副本）。两种都是本脚本创建过的，即使清单丢了也能认出来。
    返回 {目录名: 对应的内置原件名}。
    """
    if not P.skills_dir or not os.path.isdir(P.skills_dir) or not P.has_builtin():
        return {}
    by_hash = {}
    for name in sorted(os.listdir(P.builtin)):
        src = os.path.join(P.builtin, name)
        if os.path.isdir(src):
            # 原件指纹与"patch 之后"的指纹都登记进来，两种副本都能对上。
            for h in {tree_hash(src), target_hash(src)}:
                by_hash.setdefault(h, []).append(name)
    found = {}
    for entry in sorted(os.listdir(P.skills_dir)):
        full = os.path.join(P.skills_dir, entry)
        if not os.path.isdir(full):
            continue
        if not os.path.isfile(os.path.join(full, "SKILL.md")):
            continue
        twin = by_hash.get(tree_hash(full))
        if twin and entry in twin:
            found[entry] = entry
    return found


# ============================================================
# 四、副本清单（可选文件，丢了也能重建）
# ============================================================


def load_manifest():
    """读清单。新名读不到就退回旧名（改名前留下的），两个都没有就当空清单。

    清单缺失不是错误：调用方会靠内容指纹把副本重新认出来并重建清单。
    """
    for path in [P.manifest] + [x for x in P.legacy_manifests if x != P.manifest]:
        if not os.path.isfile(path):
            continue
        try:
            with open(path, encoding="utf-8") as handle:
                data = json.load(handle)
            if isinstance(data.get("mirrored"), list):
                if path != P.manifest:
                    print("（读到改名前留下的清单 %s，本次会改写为新名）" % os.path.basename(path))
                return data
        except Exception:
            pass
    return {"mirrored": []}


def save_manifest(names):
    """写出清单。patched 栏每次都按原件当场重算，不靠历史值，免得原件改声明后变陈旧。"""
    patched = sorted(
        n for n in names
        if P.has_builtin() and needs_patch(os.path.join(P.builtin, n))
    )
    with open(P.manifest, "w", encoding="utf-8") as handle:
        json.dump(
            {
                "mirrored": sorted(names),
                "patched": patched,
                "source": P.builtin,
                "dest": P.skills_dir,
                "updatedAt": time.strftime("%Y-%m-%d %H:%M:%S"),
            },
            handle,
            ensure_ascii=False,
            indent=2,
        )
    # 新清单已经写出来了，旧名文件留着只会让人误以为还有一份，顺手清掉。
    for path in P.legacy_manifests:
        if path != P.manifest and os.path.isfile(path):
            try:
                os.remove(path)
            except OSError:
                pass


def remove_one(dst):
    """删副本。链接只删链接本身，绝不用会递归进目标的方式。"""
    if os.path.islink(dst):
        os.rmdir(dst)
    elif os.path.isdir(dst):
        shutil.rmtree(dst)
    else:
        os.remove(dst)


def skill_dirs():
    """用户技能目录下所有带 SKILL.md 的子目录名。"""
    if not P.skills_dir or not os.path.isdir(P.skills_dir):
        return []
    return sorted(
        n for n in os.listdir(P.skills_dir)
        if os.path.isdir(os.path.join(P.skills_dir, n))
        and os.path.isfile(os.path.join(P.skills_dir, n, "SKILL.md"))
    )


# ============================================================
# 五、副本方案的四个命令
# ============================================================


def do_list():
    """只列出会同步哪些、跳过哪些，不动任何文件。"""
    if not require_builtin():
        return 2
    picked, skipped = candidates()
    active = app_active_builtin_dirs()
    flipped = [n for n, _, _, needs in picked if needs]
    print("本次用到的路径（都是运行时探测出来的）：")
    for title, path in P.summary():
        print("  %-12s %s" % (title, path or "(未探测到)"))
    print("索引里能认到的技能目录：%s" % (
        "%d 个（含内置、插件、你自己的）" % len(active) if active else "索引读不到，跳过这层判定"
    ))
    print("\n结论：会同步 %d 个到 %s\n" % (len(picked), P.skills_dir))
    for name, title, _, needs in picked:
        note = []
        if title != name:
            note.append(title)
        if needs:
            note.append("副本里把 user-invocable 翻成 true")
        print("  %-32s %s" % (name, "；".join(note)))
    if flipped:
        print("\n其中 %d 个原件声明了 user-invocable: false，只在副本里翻成 true，原件不动：" % len(flipped))
        print("  " + "，".join(flipped))
    if skipped:
        print("\n跳过 %d 个：" % len(skipped))
        for name, why in skipped:
            print("  %-32s %s" % (name, why))
    return 0


def do_status():
    """逐副本比对指纹，报告谁一致、谁滞后、谁缺失。只读，不动文件。"""
    if not P.has_builtin():
        # status 不强制要求能定位内置原件（定位不到也该照样把副本现状报出来），
        # 但必须说清楚："无原件"是路径没找对，不是副本真出了问题。
        print("注意：定位不到内置技能目录（%s）。" % (P.builtin or "未探测到安装目录"))
        print("下面所有副本都会报成「无原件」，那是路径没对上，不是副本有问题。")
        print("请用 --app-root 指定安装目录，或设置环境变量 %s。\n" % ENV_APP_ROOT)
    names = load_manifest().get("mirrored", [])
    if not names:
        # 清单是可选的，所以这里不能直接下结论说"没有副本"——先靠内容指纹找一遍。
        recognized = sorted(discover_copies())
        if not recognized:
            print("清单为空，技能目录里也没有能认定为本脚本副本的目录。")
            print("要么本来就没建过副本，要么清单丢了、副本又已被改动过。")
            print("跑一次 sync 会按当前判定重新建副本，并写出新清单。")
            return 1
        print("清单为空（可能被删掉了），但技能目录里有 %d 个副本能靠内容指纹认出来：" % len(recognized))
        for name in recognized:
            print("  " + name)
        print()
        print("跑一次 sync 会把它们重新纳管，并重建 %s。" % MANIFEST_NAME)
        print("注意：指纹认不出「原件升级过、副本还旧着」的那种副本，只有清单认得出。")
        print("所以清单删了不影响用，但建议留着。")
        return 0

    same = stale = missing = odd = flipped = 0
    print("%-32s %-6s %s" % ("副本", "状态", "说明"))
    print("-" * 76)
    for name in names:
        dst = os.path.join(P.skills_dir, name) if P.skills_dir else name
        src = os.path.join(P.builtin, name) if P.builtin else name
        if not os.path.isdir(dst):
            print("%-32s %-6s %s" % (name, "缺失", "副本已不在，sync 可重新复制"))
            missing += 1
            continue
        if not P.has_builtin() or not os.path.isdir(src):
            print("%-32s %-6s %s" % (name, "无原件", "内置原件已不存在，建议 restore"))
            odd += 1
            continue
        # 比对基准是"原件 patch 之后"，这样翻转过声明的副本照样算一致，
        # 不会被当成"你改过的文件"。
        if tree_hash(dst) == target_hash(src):
            note = "与内置原件内容相同"
            if needs_patch(src):
                note = "与内置原件相同，副本里 user-invocable 已翻成 true"
                flipped += 1
            print("%-32s %-6s %s" % (name, "一致", note))
            same += 1
        else:
            print("%-32s %-6s %s" % (name, "滞后", "与原件不同：原件升级过或被改过，sync 可追平"))
            stale += 1

    unknown = [n for n in skill_dirs() if n not in names]
    recognizable = discover_copies()
    orphans = sorted(set(recognizable) - set(unknown) - set(names))
    print("-" * 76)
    print("一致 %d（其中 %d 个翻转了 user-invocable），滞后 %d，缺失 %d，异常 %d" % (
        same, flipped, stale, missing, odd
    ))
    if orphans:
        print("有 %d 个副本不在清单里，但内容与内置原件一致，可被识别并复原：" % len(orphans))
        print("  " + "，".join(orphans))
        print("  跑一次 sync 会把它们重新纳管。")
    others = [x for x in unknown if x not in recognizable]
    if others:
        print("另有 %d 个技能目录既不在清单里、内容也与内置原件不同，不会被动到：" % len(others))
        print("  " + "，".join(others))
    return 0


def do_sync(force=False):
    """把该复制的都复制（并在副本里翻转声明），不该留的撤掉。"""
    if not require_builtin():
        return 2
    picked, _ = candidates()
    wanted = set(name for name, _, _, _ in picked)
    done = set(load_manifest().get("mirrored", []))

    stale = sorted(done - wanted)
    # 防线：真被策略禁用的内置技能通常只有个别几个。一次要撤掉一半以上，
    # 更可能是判定信号出了问题（索引残缺、路径变化），先停下来别动。
    if stale and not force and len(stale) * 2 > max(len(done), 1):
        print("检测到本次要撤回 %d 个副本（清单共 %d 个），数量异常。" % (len(stale), len(done)))
        print("先不动任何文件。请用 list 核对判定依据；确认无误再加 --force 重跑。")
        print("拟撤回：" + "，".join(stale))
        return 1
    for name in stale:
        dst = os.path.join(P.skills_dir, name)
        if os.path.exists(dst) or os.path.islink(dst):
            remove_one(dst)
        done.discard(name)

    if not os.path.isdir(P.skills_dir):
        os.makedirs(P.skills_dir, exist_ok=True)

    copied, refused, replaced, adopted, flipped = [], [], [], [], []
    for name, _, src, needs in picked:
        dst = os.path.join(P.skills_dir, name)
        if os.path.islink(dst):
            os.rmdir(dst)
        elif os.path.isdir(dst) and name not in done:
            # 目录已存在但不归本脚本管：内容与内置原件对得上（原样或已翻转）的，
            # 视为本脚本的副本重新纳管；内容不同的当作你自己的技能，绝不覆盖。
            if tree_hash(dst) in (tree_hash(src), target_hash(src)):
                adopted.append(name)
                done.add(name)
                if needs and apply_patch(dst):
                    flipped.append(name)
                continue
            refused.append(name)
            continue
        elif os.path.isdir(dst):
            replaced.append(name)
        shutil.copytree(src, dst, dirs_exist_ok=True)
        if needs and apply_patch(dst):
            flipped.append(name)
        done.add(name)
        copied.append(name)
    save_manifest(done)

    if stale:
        print("已撤回 %d 个不再适合同步的旧副本：" % len(stale))
        for name in stale:
            print("  " + name)
        print()
    if adopted:
        print("重新纳管 %d 个已有的同名副本（内容与内置原件对得上，未覆盖）：" % len(adopted))
        for name in adopted:
            print("  " + name)
        print()
    print("已复制 %d 个副本到用户技能目录：" % len(copied))
    for name in copied:
        print("  %s%s" % (name, "（覆盖更新）" if name in replaced else ""))
    if flipped:
        print("\n其中 %d 个在副本里把 user-invocable 翻成了 true（原件不动）：" % len(flipped))
        for name in flipped:
            print("  " + name)
    if refused:
        print("\n以下同名目录已存在且内容与内置原件对不上，判定为你自己的技能，未覆盖：")
        for name in refused:
            print("  " + name)
    print("\n重开一次技能面板即可看到。复原用 restore。")
    return 0


def do_restore(force=False, dry=False, only=None):
    """删除副本、复原到操作前的状态。按名只删那几个，给空则全量。"""
    if not P.skills_dir:
        print("没能确定用户技能目录，无法复原。请用 --config-dir 指定。")
        return 2
    listed = load_manifest().get("mirrored", [])
    if only:
        missing = [n for n in only if n not in listed]
        if missing:
            print("这些名字不在清单里，无法按名复原：%s" % "，".join(missing))
        all_names = listed
        names = [n for n in listed if n in only]
        if not names:
            return 2
    else:
        # 全量复原：清单 ∪ 当场识别出的副本。清单万一丢了，
        # 只要副本内容与内置原件一致就仍能被认出并删掉，不会留下残渣。
        recognized = sorted(discover_copies())
        all_names = sorted(set(listed) | set(recognized))
        names = all_names
        extra = sorted(set(recognized) - set(listed))
        if extra:
            print("清单外还识别出 %d 个副本，一并纳入复原：" % len(extra))
            for name in extra:
                print("  " + name)
            print()
    if not all_names:
        print("清单为空，也没有可识别的副本，无需复原。")
        return 0

    def unverifiable(name):
        """原件不在时无法核对内容，删之前要提醒一句。"""
        return not (P.has_builtin() and os.path.isdir(os.path.join(P.builtin, name)))

    if dry:
        print("演练模式，不会删除任何文件。\n")
        print("%-32s %-8s %s" % ("副本", "状态", "将删除的文件数"))
        print("-" * 66)
        total = 0
        unverified = 0
        for name in names:
            dst = os.path.join(P.skills_dir, name)
            src = os.path.join(P.builtin, name) if P.builtin else name
            if not os.path.exists(dst) and not os.path.islink(dst):
                print("%-32s %-8s %s" % (name, "不存在", "跳过"))
                continue
            n = count_files(dst) if os.path.isdir(dst) else 1
            flag = ""
            if not force and os.path.isdir(src) and tree_hash(dst) != target_hash(src):
                flag = "（被改动过，需 --force）"
            elif unverifiable(name):
                flag = "（原件不在，无法核对内容）"
                unverified += 1
            print("%-32s %-8s %d %s" % (name, "待删", n, flag))
            total += n
        print("-" * 66)
        print("合计将删除 %d 个文件、%d 个目录。内置原件不在删除范围内。" % (total, len(names)))
        print("清单里另有 %d 个副本不受本次操作影响。" % (len(all_names) - len(names)))
        if unverified:
            print("其中 %d 个的原件已不在，删了就无从核对；确认这些确实是你建的副本再删。" % unverified)
        return 0

    removed, skipped, absent, unverified = [], [], [], []
    for name in names:
        dst = os.path.join(P.skills_dir, name)
        src = os.path.join(P.builtin, name) if P.builtin else name
        if not os.path.exists(dst) and not os.path.islink(dst):
            absent.append(name)
            continue
        if not force and os.path.isdir(src) and tree_hash(dst) != target_hash(src):
            skipped.append(name)
            continue
        if unverifiable(name):
            unverified.append(name)
        remove_one(dst)
        removed.append(name)

    left = [n for n in all_names if os.path.exists(os.path.join(P.skills_dir, n))]
    save_manifest(left)

    print("已删除 %d 个副本：" % len(removed))
    for name in removed:
        print("  " + name)
    if unverified:
        print("\n其中 %d 个的原件已不在，未能核对内容就删了：" % len(unverified))
        for name in unverified:
            print("  " + name)
    if absent:
        print("\n清单里有 %d 个副本本来就不在，已从清单剔除：" % len(absent))
        for name in absent:
            print("  " + name)
    if skipped:
        print("\n以下 %d 个副本与内置原件不一致，判定为被改动过，未删除：" % len(skipped))
        for name in skipped:
            print("  " + name)
        print("确认可以删，再加 --force 重跑一次。")

    print("\n复原校验：")
    residue = [n for n in names if os.path.exists(os.path.join(P.skills_dir, n))]
    print("  本次范围内的副本残留：%d 个%s" % (len(residue), "（" + "，".join(residue) + "）" if residue else ""))
    print("  清单现在还有 %d 条记录（未被本次操作涉及的副本继续在管）" % len(left))
    damaged = [n for n in all_names if not (P.has_builtin() and os.path.isdir(os.path.join(P.builtin, n)))]
    print("  内置原件缺失：%d 个%s" % (len(damaged), "（" + "，".join(damaged) + "）" if damaged else ""))
    print("  技能目录里现在有 %d 个技能" % len(skill_dirs()))
    return 1 if (residue or damaged) else 0


# ============================================================
# 六、改前端 bundle 那条路（可用，但不建议，见文件开头）
# ============================================================


def find_bundles():
    """在 renderer 目录里找出"符合命名且含目标锚点"的前端 chunk。

    不能写死文件名：contexts-XXXX.js 里的 XXXX 是内容哈希，应用一升级就变。
    所以按"文件名前缀 + 内容里能找到锚点"来认。
    """
    hits = []
    if not P.has_renderer():
        return hits
    for name in sorted(os.listdir(P.renderer_assets)):
        if not (name.startswith("contexts-") and name.endswith(".js")):
            continue
        path = os.path.join(P.renderer_assets, name)
        text = read_text(path)
        if any(old in text for _, old, _ in BUNDLE_PATCHES) or any(
            new in text for _, _, new in BUNDLE_PATCHES
        ):
            hits.append(path)
    return hits


def patch_bundle_text(text):
    """对 bundle 全文做补丁，返回 (新文本, 每条规则的处置说明)。

    每条规则都要求"原式恰好 1 次、新式 0 次"才替换；命中数不对就原样保留并如实报告，
    绝不靠猜去改。这样万一应用升级后代码变了，脚本只会说"没找到锚点"，不会乱改。
    """
    report = []
    new_text = text
    for title, old, new in BUNDLE_PATCHES:
        n_old = new_text.count(old)
        n_new = new_text.count(new)
        if n_old == 1 and n_new == 0:
            new_text = new_text.replace(old, new)
            report.append((title, "已替换（命中 1 处）", True))
        elif n_old == 0 and n_new == 1:
            report.append((title, "已是打过的状态，跳过", True))
        else:
            report.append(
                (title, "未动手：原式命中 %d 处、新式命中 %d 处，需恰好 1 与 0" % (n_old, n_new), False)
            )
    return new_text, report


def node_executable():
    """找一个可用的 node，用来做语法体检。找不到返回 None（体检跳过）。

    顺序：PATH 上的 node → 应用托管目录下的 node。不写死任何用户目录。
    """
    found = shutil.which("node")
    if found:
        return found
    base = os.path.join(P.config_dir, "binaries", "node", "versions") if P.config_dir else None
    if base and os.path.isdir(base):
        for version in sorted(os.listdir(base), reverse=True):
            for exe in ("node.exe", "node"):
                cand = os.path.join(base, version, exe)
                if os.path.isfile(cand):
                    return cand
    return None


def syntax_check(text):
    """借 node --check 给改后的代码做一次真正的语法体检。

    返回 True（语法通过）/ False（语法错）/ None（找不到 node，无法体检）。
    只是解析、不执行；写到临时 .mjs 上做，不碰目标文件。
    注意它只查语法，查不出语义错误——所以它是"必要不充分"的一道闸。
    """
    node = node_executable()
    if not node:
        return None
    tmp_dir = tempfile.mkdtemp(prefix="wbskill-bundle-")
    tmp = os.path.join(tmp_dir, "check.mjs")
    try:
        with open(tmp, "wb") as handle:
            handle.write(text.encode("utf-8"))
        proc = subprocess.run([node, "--check", tmp], capture_output=True, text=True, timeout=300)
        if proc.returncode != 0:
            detail = (proc.stderr or proc.stdout or "").strip()
            if detail:
                print("    体检报错：%s" % detail.splitlines()[0][:300])
        return proc.returncode == 0
    except Exception:
        return None
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def bundle_warning():
    """在动手前后都要打的那段警告。"""
    print("【这条路不建议用，请优先用副本方案（sync）】")
    print("  改的是应用安装目录里的分发产物：升级整包覆盖即失效，")
    print("  且文件名里的哈希会变，脚本只能靠内容锚点重新找。")
    print("  那个 chunk 在首屏关键路径上，改坏会整个界面白屏，连这个对话窗口都打不开。")
    print("  体检只查语法、查不出语义错误；也放不出应用后端根本不返回的技能。")
    print()


def do_bundle(force=False):
    """给前端 bundle 打补丁。默认只演练，不写盘；加 --force 才真写。"""
    bundle_warning()
    if not require_renderer():
        return 2
    hits = find_bundles()
    if not hits:
        print("在 %s 里没找到含目标锚点的 contexts-*.js。" % P.renderer_assets)
        print("多半是应用升级后改了代码或换了文件名。不做任何事。")
        return 2
    if len(hits) > 1:
        print("找到 %d 个候选，无法确定该改哪个，为安全起见不做任何事：" % len(hits))
        for path in hits:
            print("  " + path)
        return 2

    path = hits[0]
    with open(path, "rb") as handle:
        raw = handle.read()
    text = read_text(path)
    if text.encode("utf-8") != raw:
        print("目标文件含非法 UTF-8 字节，解码再编码无法还原原样，为安全起见不动它。")
        return 2

    print("目标文件：%s" % path)
    print("大小：%d 字节（%.1f MB）\n" % (len(raw), len(raw) / 1048576.0))
    new_text, report = patch_bundle_text(text)
    print("补丁处置：")
    for title, note, ok in report:
        print("  [%s] %s——%s" % ("OK" if ok else "跳过", title, note))
    print()

    if new_text == text:
        print("无需改动：目标已是打过补丁的状态，或锚点都没命中。")
        return 0

    if not force:
        print("以上是演练结果，**没有写入任何文件**。")
        print("确认要改，加 --force 重跑：会先备份、再在临时副本上做语法体检，")
        print("体检不过就不落盘；落盘后再复核锚点，任何一步不对就回滚。")
        print("改完需要重启应用才生效。还原用 bundle-restore。")
        return 0

    verdict = syntax_check(new_text)
    if verdict is False:
        print("语法体检未通过，**已放弃写入**，目标文件保持原样、未产生任何备份。")
        return 1
    if verdict is None:
        print("找不到 node，无法做语法体检。")
        print("改坏这个文件会让整个界面白屏，没有体检兜底风险太高，**因此不写入**。")
        print("请先确保 node 可用，或干脆改用副本方案（sync）。")
        return 1
    print("语法体检：通过（注意它只查语法，查不出语义错误）")

    backup = path + BUNDLE_BACKUP_SUFFIX
    if not os.path.exists(backup):
        shutil.copyfile(path, backup)
        print("已备份原文件到：%s" % backup)
    else:
        print("备份已存在，沿用：%s" % backup)

    with open(path, "wb") as handle:
        handle.write(new_text.encode("utf-8"))

    # 落盘后复核：新式在、原式不在，两条都成立才算写成功。
    after = read_text(path)
    bad = [
        title for title, old, new in BUNDLE_PATCHES
        if not (after.count(new) == 1 and after.count(old) == 0)
    ]
    if bad:
        print("落盘后复核不通过：%s" % "，".join(bad))
        print("正在从备份回滚……")
        shutil.copyfile(backup, path)
        print("已回滚到原文件。目标文件未被改动。")
        return 1

    print("已写入，复核通过。")
    print("请重启应用生效。若界面异常，跑 bundle-restore 即可还原。")
    return 0


def do_bundle_status():
    """看 bundle 现在是原样、已打补丁，还是找不到。只读，不动文件。"""
    if not require_renderer():
        return 1
    hits = find_bundles()
    if not hits:
        print("没找到含目标锚点的 contexts-*.js（路径：%s）。" % P.renderer_assets)
        print("要么应用升级后代码变了，要么本来就无需处理。")
        return 1
    print("%-46s %-12s %s" % ("文件", "状态", "备份"))
    print("-" * 78)
    for path in hits:
        text = read_text(path)
        done = sum(1 for _, _, new in BUNDLE_PATCHES if text.count(new) == 1)
        raw = sum(1 for _, old, _ in BUNDLE_PATCHES if text.count(old) == 1)
        if done == len(BUNDLE_PATCHES):
            state = "已打补丁"
        elif raw == len(BUNDLE_PATCHES):
            state = "原样"
        else:
            state = "部分/未知(%d/%d)" % (done, len(BUNDLE_PATCHES))
        has = "有" if os.path.exists(path + BUNDLE_BACKUP_SUFFIX) else "无"
        print("%-46s %-12s %s" % (os.path.basename(path), state, has))
    print()
    print("提示：这条路不建议用。副本方案（sync）不动应用安装目录，风险小得多。")
    return 0


def do_bundle_restore(dry=False):
    """从 .wb-orig.bak 还原 bundle。这是救援动作，所以默认**直接生效**，不要求 --force。

    理由是：走到这一步多半界面已经白屏，让人再加一个开关只会误事。
    想先看会动什么，用 --dry-run。
    """
    if not require_renderer():
        return 1
    backups = [
        os.path.join(P.renderer_assets, n)
        for n in sorted(os.listdir(P.renderer_assets))
        if n.endswith(BUNDLE_BACKUP_SUFFIX)
    ]
    if not backups:
        print("没有找到任何备份（%s）。无需还原。" % BUNDLE_BACKUP_SUFFIX)
        return 0
    print("找到 %d 个备份：\n" % len(backups))
    if dry:
        print("演练模式，不会写任何文件。\n")
    for backup in backups:
        target = backup[: -len(BUNDLE_BACKUP_SUFFIX)]
        name = os.path.basename(target)
        if not os.path.exists(target):
            print("  %-46s 目标文件不在，跳过（备份保留）" % name)
            continue
        if dry:
            print("  %-46s 将用备份覆盖它" % name)
            continue
        shutil.copyfile(backup, target)
        os.remove(backup)
        print("  %-46s 已还原，备份已移除" % name)
    print()
    if dry:
        print("以上是演练结果，未写盘。去掉 --dry-run 即执行。")
    else:
        print("已还原。请重启应用生效。")
    return 0


# ============================================================
# 七、命令行入口
# ============================================================

# 命令名 → (处理函数, 是否需要 force, 是否需要 dry)
COMMANDS = {
    "sync": lambda o: do_sync(o["force"]),
    "list": lambda o: do_list(),
    "status": lambda o: do_status(),
    "restore": lambda o: do_restore(o["force"], o["dry"], o["names"]),
    "bundle": lambda o: do_bundle(o["force"]),
    "bundle-status": lambda o: do_bundle_status(),
    "bundle-restore": lambda o: do_bundle_restore(o["dry"]),
}

# 早期版本的写法，保留兼容。
ALIASES = {"--remove": "restore", "--list": "list", "--status": "status"}

# 带值的开关。
VALUE_FLAGS = {"--app-root": "app_root", "--config-dir": "config_dir"}


def parse_argv(argv):
    """手写解析：命令与开关可出现在任意位置，开关可前置。

    返回 (命令名, 位置参数, 选项字典)。用法与旧版完全一致，另加两个路径开关。
    """
    opts = {"force": False, "dry": False, "app_root": None, "config_dir": None, "names": []}
    rest = []
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg in VALUE_FLAGS:
            if index + 1 >= len(argv):
                raise SystemExit("开关 %s 后面要跟一个目录路径。" % arg)
            opts[VALUE_FLAGS[arg]] = argv[index + 1]
            index += 2
            continue
        matched = False
        for flag, key in VALUE_FLAGS.items():
            if arg.startswith(flag + "="):
                opts[key] = arg[len(flag) + 1:]
                matched = True
                break
        if matched:
            index += 1
            continue
        if arg == "--force":
            opts["force"] = True
        elif arg == "--dry-run":
            opts["dry"] = True
        elif arg in ("-h", "--help"):
            return "help", [], opts
        elif arg == "--version":
            return "version", [], opts
        else:
            rest.append(arg)
        index += 1

    cmd = ALIASES.get(rest[0], rest[0]) if rest else "sync"
    opts["names"] = rest[1:]
    return cmd, opts["names"], opts


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd, _, opts = parse_argv(argv)

    if cmd == "help":
        print(__doc__)
        return 0
    if cmd == "version":
        print("%s %s" % (PROG, VERSION))
        return 0

    handler = COMMANDS.get(cmd)
    if handler is None:
        print("未知命令：%s\n" % cmd)
        print(__doc__)
        return 2

    # 路径在解析完参数后再定，好让 --app-root / --config-dir 生效。
    global P
    P = resolve_paths(opts["app_root"], opts["config_dir"])
    # 显式指定的安装目录若结构对不上，当场报错退出：这种情况多半是路径写错了，
    # 让它继续跑只会得到一堆"找不到/无原件"的噪声，反而看不出真正的病因。
    if opts["app_root"] and not is_app_root(P.app_root):
        print("指定的安装目录结构对不上：%s" % P.app_root)
        print("它下面没有 resources/app.asar.unpacked，不像 WorkBuddy 的安装目录。")
        return 2
    return handler(opts)


if __name__ == "__main__":
    sys.exit(main())
