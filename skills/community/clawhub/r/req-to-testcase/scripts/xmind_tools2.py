#!/usr/bin/env python3
"""
xmind_tools2.py
XMind 文件生成工具 —— 基于 xmind 库，生成兼容 XMind8 与 XMind2020 的 .xmind 文件。

依赖安装：
    pip install xmind --break-system-packages

用法（作为模块导入）：
    from scripts.xmind_tools2 import build_xmind_from_cases
    path = build_xmind_from_cases(test_cases, project_name="登录模块", output_dir="/mnt/user-data/outputs")

test_cases 格式：
    [
      {
        "id":          "TC-REG-001",       # 用例ID
        "module":      "用户注册",           # 所属模块
        "type":        "功能测试",           # 测试类型（正向/逆向/边界/业务规则/兼容/性能/体验）
        "title":       "正常注册成功",        # 用例标题
        "priority":    "P0",               # 优先级 P0/P1/P2/P3
        "precondition": "未注册的邮箱",      # 前置条件
        "steps":       "1. 填写信息\n2. 提交", # 操作步骤
        "expected":    "注册成功，跳转首页"    # 预期结果
      },
      ...
    ]
"""

import os
import time
import shutil
import zipfile

# ── 脚本自身所在目录，用于定位 META-INF/manifest.xml ──────────────────────────
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_MANIFEST_SRC = os.path.join(_SCRIPT_DIR, "META-INF", "manifest.xml")


# ─────────────────────────────────────────────────────────────────────────────
# 内部工具：aftertreatment & extract
# 作用：将 xmind 库生成的文件注入 META-INF/manifest.xml，使其兼容 XMind2020
# ─────────────────────────────────────────────────────────────────────────────

def _extract(d_path: str, f_path: str):
    """解压 ZIP，处理文件名编码乱码问题。"""
    if not os.path.exists(d_path):
        os.makedirs(d_path)

    with zipfile.ZipFile(f_path, "r") as zf:
        for n in zf.infolist():
            src_name = n.filename
            try:
                decode_name = src_name.encode("cp437").decode("utf-8")
            except Exception:
                try:
                    decode_name = src_name.encode("cp437").decode("gbk")
                except Exception:
                    decode_name = src_name

            parts = decode_name.split("/")
            dest = d_path
            for part in parts:
                dest = os.path.join(dest, part)

            if decode_name.endswith("/"):
                os.makedirs(dest, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, "wb") as f:
                    f.write(zf.read(src_name))


def _aftertreatment(xmind_path: str):
    """
    注入 META-INF/manifest.xml，使生成的文件同时兼容 XMind8 和 XMind2020。

    流程：
      1. 将 .xmind 重命名为 .zip
      2. 解压
      3. 注入 META-INF/manifest.xml
      4. 重新打包为 .zip → 改回 .xmind
      5. 清理临时目录
    """
    folder = os.path.dirname(xmind_path)
    name = os.path.basename(xmind_path)                      # xxx.xmind
    stem = os.path.splitext(name)[0]                         # xxx
    zip_path = os.path.join(folder, stem + ".zip")
    unzip_dir = os.path.join(folder, stem)

    # 1. rename → .zip
    os.rename(xmind_path, zip_path)

    # 2. 解压
    _extract(unzip_dir, zip_path)

    # 3. 注入 manifest.xml
    inf_dir = os.path.join(unzip_dir, "META-INF")
    os.makedirs(inf_dir, exist_ok=True)
    shutil.copyfile(_MANIFEST_SRC, os.path.join(inf_dir, "manifest.xml"))

    # 4. 删除旧 zip，重新打包
    os.remove(zip_path)
    shutil.make_archive(unzip_dir, "zip", unzip_dir)       # 生成 xxx.zip

    # 5. 改回 .xmind
    os.rename(unzip_dir + ".zip", xmind_path)

    # 6. 清理解压目录
    shutil.rmtree(unzip_dir)


# ─────────────────────────────────────────────────────────────────────────────
# 节点构建辅助
# ─────────────────────────────────────────────────────────────────────────────

def _create_topic(workbook, parent, title: str):
    """在 parent 下新建子节点并返回。"""
    try:
        from xmind.core.topic import TopicElement
    except ImportError:
        raise ImportError("请先安装 xmind 库：pip install xmind --break-system-packages")

    topic = TopicElement(ownerWorkbook=workbook)
    topic.setTitle(title)
    parent.addSubTopic(topic)
    return topic


# ─────────────────────────────────────────────────────────────────────────────
# 公开接口
# ─────────────────────────────────────────────────────────────────────────────

def build_xmind_from_cases(
    test_cases: list,
    project_name: str = "测试用例",
    output_dir: str = "/mnt/user-data/outputs",
) -> str:
    """
    根据测试用例列表生成 XMind 文件。

    脑图结构：
        项目名（根节点）
        └── 模块
            └── 测试类型
                └── [优先级] 用例标题
                    ├── pc: 前置条件
                    └── 步骤
                        └── 预期结果

    返回生成文件的绝对路径。
    """
    try:
        import xmind
    except ImportError:
        raise ImportError("请先安装 xmind 库：pip install xmind --break-system-packages")

    os.makedirs(output_dir, exist_ok=True)
    timestamp = int(time.time())
    filename = f"测试用例导图-{timestamp}.xmind"
    file_path = os.path.join(output_dir, filename)

    workbook = xmind.load(file_path)
    sheet = workbook.getPrimarySheet()
    sheet.setTitle("测试用例")
    root_topic = sheet.getRootTopic()
    root_topic.setTitle(project_name)

    # 按 模块 → 测试类型 分组
    groups: dict[str, dict[str, list]] = {}
    for tc in test_cases:
        mod = tc.get("module", "未分类")
        tc_type = tc.get("type", "功能测试")
        groups.setdefault(mod, {}).setdefault(tc_type, []).append(tc)

    for mod_name, type_dict in groups.items():
        mod_topic = _create_topic(workbook, root_topic, mod_name)

        for type_name, cases in type_dict.items():
            type_topic = _create_topic(workbook, mod_topic, type_name)

            for tc in cases:
                priority = tc.get("priority", "P2")
                title = f"[{priority}] {tc.get('title', '').strip()}"
                case_topic = _create_topic(workbook, type_topic, title)

                # 前置条件
                pre = tc.get("precondition", "").strip()
                if pre:
                    _create_topic(workbook, case_topic, f"pc: {pre}")

                # 步骤 → 预期结果（子节点）
                steps = tc.get("steps", "").strip()
                expected = tc.get("expected", "").strip()
                if steps:
                    step_topic = _create_topic(workbook, case_topic, steps)
                    if expected:
                        _create_topic(workbook, step_topic, expected)
                elif expected:
                    _create_topic(workbook, case_topic, expected)

                # 标记 AI 生成
                _create_topic(workbook, case_topic, "tag: AI")

    xmind.save(workbook, path=file_path)
    _aftertreatment(file_path)

    print(f"✅ XMind 文件已生成：{file_path}")
    return file_path


# ─────────────────────────────────────────────────────────────────────────────
# 命令行快速测试入口
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sample = [
        {
            "id": "TC-001", "module": "用户注册", "type": "正向功能测试",
            "title": "正常注册成功", "priority": "P0",
            "precondition": "使用未注册邮箱",
            "steps": "1. 填写用户名\n2. 填写邮箱\n3. 设置密码\n4. 提交",
            "expected": "注册成功，跳转首页，收到欢迎邮件",
        },
        {
            "id": "TC-002", "module": "用户注册", "type": "逆向/异常测试",
            "title": "邮箱格式错误提示", "priority": "P1",
            "precondition": "打开注册页",
            "steps": "1. 邮箱输入 'abc'\n2. 提交",
            "expected": "提示「邮箱格式不正确」，不允许提交",
        },
    ]
    build_xmind_from_cases(sample, project_name="演示项目", output_dir="/tmp")
