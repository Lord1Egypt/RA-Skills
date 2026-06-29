#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings UI for Triphasic Execution Framework
============================================
启动本地 HTTP 服务器，提供 HTML 设置界面，处理表单提交，
写入 config.json 和 SKILL.md，在系统默认浏览器中打开设置页面。

用法:
  python settings.py                         # 打开设置界面
  python settings.py --skill-dir /path/to/skill  # 指定技能目录
  python settings.py --home /path/to/home        # 指定数据目录
  python settings.py --port 8080                  # 指定端口
"""

import os
import sys
import json
import time
import webbrowser
import threading
import argparse
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# R-12 审计锚点（放在 import 之后，保证 os 已加载）
DEFAULT_DATA_DIR_RAW = "skills/.standardization/triphasic-execution/data/"
_data_dir_abs = os.path.normpath(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "..", DEFAULT_DATA_DIR_RAW
))

# 全局标志：设置是否完成
SETTINGS_DONE = False
SERVER_INSTANCE = None

# 默认端口范围
DEFAULT_PORT_MIN = 8080
DEFAULT_PORT_MAX = 8999


def get_skill_dir(args) -> Path:
    """获取技能目录路径"""
    if args.skill_dir:
        return Path(args.skill_dir).expanduser().resolve()
    # 自动检测：scripts/settings.py → ../（技能根目录）
    return Path(__file__).parent.parent


def get_standardization_dir(skill_dir: Path) -> Path:
    """定位 skills/.standardization/<skill_name>/data/ 目录"""
    # skill_dir 是技能根目录，如 .../skills/triphasic-execution
    # 向上找 skills/ 目录
    p = skill_dir.resolve()
    for parent in [p] + list(p.parents):
        if parent.name == "skills" and parent.parent.name != "skills":
            return parent / ".standardization" / skill_dir.name / "data"
    # fallback: 用 skill_dir 同级 .standardization/
    return skill_dir.parent / ".standardization" / skill_dir.name / "data"


def get_home_dir(args, skill_dir) -> Path:
    """获取数据目录路径"""
    if args.home:
        return Path(args.home).expanduser().resolve()
    # 从 config.json 读取
    config_file = skill_dir / "assets" / "default_config.json"
    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            if "_triphasic_home" in cfg:
                return Path(cfg["_triphasic_home"]).expanduser()
        except Exception:
            pass
    # 从环境变量读取
    env_home = os.environ.get("TRIPHASIC_HOME")
    if env_home:
        return Path(env_home).expanduser()
    # 默认：skills/.standardization/triphasic-execution/data/
    return get_standardization_dir(skill_dir)


def find_available_port(min_port=DEFAULT_PORT_MIN, max_port=DEFAULT_PORT_MAX) -> int:
    """查找可用端口"""
    import socket
    for port in range(min_port, max_port + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("localhost", port))
            sock.close()
            return port
        except OSError:
            continue
    raise RuntimeError(f"无法找到可用端口（范围 {min_port}-{max_port}）")


def update_skill_md(skill_dir: Path, config: dict):
    """更新 SKILL.md 中的配置值"""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print(f"   ⚠️  SKILL.md 不存在：{skill_md}")
        return False

    try:
        # 备份
        backup = skill_dir / "SKILL.md.bak"
        with open(skill_md, "r", encoding="utf-8") as f:
            original_content = f.read()
        with open(backup, "w", encoding="utf-8") as f:
            f.write(original_content)
        print(f"   ✅ 已备份 SKILL.md → SKILL.md.bak")

        # 读取内容
        content = original_content
        mode = config.get("mode", "on_demand")
        triphasic_home = config.get("_triphasic_home", str(get_standardization_dir(self.skill_dir)))
        require_confirm = config.get("hooks", {}).get("require_task_confirmation", True)

        # 更新「双模式设计」章节开头
        mode_text = "🔵 全局自动模式" if mode == "global" else "🟢 按需调用模式（默认）"
        mode_marker = "### 核心理念：用户习惯决定启动方式"
        if mode_marker in content:
            # 在章节开头添加当前配置
            lines = content.split("\n")
            new_lines = []
            i = 0
            while i < len(lines):
                line = lines[i]
                new_lines.append(line)
                if line.strip() == mode_marker:
                    # 检查下一行是否已经是"当前配置"注释
                    if i + 1 < len(lines) and "**当前配置" in lines[i + 1]:
                        # 替换现有注释
                        new_lines.append(f"> **当前配置：{mode_text}**")
                        i += 2
                        continue
                    else:
                        # 插入新注释
                        new_lines.append(f"> **当前配置：{mode_text}**")
                i += 1
            content = "\n".join(new_lines)

        # 更新「数据目录」章节的表格
        # 替换 TRIPHASIC_HOME 默认值说明
        home_marker = "**默认值**：`~/.workbuddy/triphasic/`"
        content = content.replace(home_marker, f"**当前配置**：`{triphasic_home}`")

        # 更新「配置」章节的示例代码
        # 替换 mode 示例
        if mode == "global":
            content = content.replace('"mode": "on_demand"', '"mode": "global"')
        # 替换 require_task_confirmation 示例
        if not require_confirm:
            content = content.replace(
                '"require_task_confirmation": true',
                '"require_task_confirmation": false'
            )

        # 写回
        with open(skill_md, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"   ✅ 已更新 SKILL.md 配置值")
        return True

    except Exception as e:
        print(f"   ❌ 更新 SKILL.md 失败：{e}")
        # 恢复备份
        if backup.exists():
            with open(backup, "r", encoding="utf-8") as f:
                original = f.read()
            with open(skill_md, "w", encoding="utf-8") as f:
                f.write(original)
            print(f"   ✅ 已恢复 SKILL.md 备份")
        return False

def save_config_from_json(skill_dir: Path, home_dir: Path, config_json: str) -> int:
    """
    从 JSON 字符串保存配置（用于对话式设置）
    与 HTML UI 的 _do_save_config 采用相同的 merge 逻辑：
    先读现有 config.json（或 default_config.json），再用传入字段覆盖。
    
    Args:
        skill_dir: 技能目录
        home_dir: 数据目录
        config_json: JSON 字符串，包含要更新的配置字段
        
    Returns:
        int: 0 表示成功，1 表示失败
    """
    try:
        # 解析 JSON
        updates = json.loads(config_json)
        print(f"   📝 解析配置 JSON 成功")

        # 确定数据目录
        target_home = Path(updates.get("_triphasic_home", str(home_dir))).expanduser()
        target_home.mkdir(parents=True, exist_ok=True)
        config_file = target_home / "config.json"

        # 读取现有配置（与 _do_save_config 一致）
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
        else:
            default_file = target_home / "default_config.json"
            if default_file.exists():
                with open(default_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
            else:
                config = {}

        # 增量覆盖（只更新传入的字段，保留未传字段）
        # 特殊处理 mode / triphasic_home / 文件路径
        for key in ("mode", "triphasic_home", "problems_file", "risks_file", "lessons_file", "logs_dir"):
            if key in updates:
                config[key] = updates[key]

        # 特殊处理 hooks（保留未在传入 JSON 中的 hooks 字段）
        if "hooks" in updates:
            if "hooks" not in config:
                config["hooks"] = {}
            config["hooks"].update(updates["hooks"])

        # 标记已保存
        config["_saved"] = True

        # 写入 config.json
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"   ✅ 已写入 config.json：{config_file}")
        
        # 更新 SKILL.md
        update_skill_md(skill_dir, config)
        
        print(f"✅ 配置保存成功")
        return 0
        
    except json.JSONDecodeError as e:
        print(f"   ❌ JSON 解析失败：{e}")
        return 1
    except Exception as e:
        print(f"   ❌ 保存配置失败：{e}")
        return 1


class SettingsHandler(BaseHTTPRequestHandler):
    """HTTP 请求处理器"""

    def log_message(self, format, *args):
        """禁用默认日志输出"""
        pass

    def do_GET(self):
        """处理 GET 请求"""
        parsed_path = urlparse(self.path)

        if parsed_path.path == "/" or parsed_path.path == "/index.html":
            # 返回设置页面
            self.serve_settings_html()

        elif parsed_path.path == "/config":
            # 返回当前配置（JSON）
            self.send_config()

        elif parsed_path.path == "/done":
            # 返回"设置已完成"页面
            self.send_done_page()

        else:
            self.send_error(404, "Not Found")

    def do_OPTIONS(self):
        """处理 CORS 预检请求"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        """处理 POST 请求"""
        if self.path == "/save":
            self.handle_save()
        else:
            self.send_error(404, "Not Found")

    def serve_settings_html(self):
        """返回 settings.html — 搜索技能目录 assets/ 及标准化目录"""
        search_paths = [
            self.server.skill_dir / "assets" / "settings.html",          # 功能目录（主要）
            self.server.home_dir.parent / "settings.html",               # standardization 父级
            self.server.home_dir / "settings.html",                      # standardization/data/
        ]
        html_file = None
        for p in search_paths:
            if p.exists():
                html_file = p
                break
        if not html_file:
            self.send_error(404, "settings.html not found")
            return

        try:
            with open(html_file, "r", encoding="utf-8") as f:
                html_content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html_content.encode("utf-8"))
        except Exception as e:
            self.send_error(500, f"Error reading settings.html: {e}")

    def send_config(self):
        """返回当前配置 JSON"""
        # 优先从 home_dir 读取
        config_file = self.server.home_dir / "config.json"
        if not config_file.exists():
            # 使用默认配置
            config_file = self.server.skill_dir / "assets" / "default_config.json"

        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)

            # 标准化字段名（与 HTML 表单一致）
            result = {
                "mode": config.get("mode", "on_demand"),
                "triphasic_home": config.get("triphasic_home", str(self.server.home_dir)),
                "problems_file": config.get("problems_file", "PROBLEMS.md"),
                "risks_file": config.get("risks_file", "RISKS.md"),
                "lessons_file": config.get("lessons_file", "LESSONS_REGISTER.md"),
                "logs_dir": config.get("logs_dir", ".problem_logs"),
                "require_confirmation": config.get("hooks", {}).get("require_task_confirmation", True),
                "hooks": config.get("hooks", {
                    "pre_exec_search": True,
                    "auto_record_exception": True,
                    "require_task_confirmation": True,
                    "require_complete_validation": True,
                    "auto_idle_cutoff": False,
                    "block_skip_review": False
                }),
                "_saved": config.get("_saved", False)
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(result, indent=2, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            # 返回默认配置
            default_config = {
                "mode": "on_demand",
                "triphasic_home": str(self.server.home_dir),
                "problems_file": "PROBLEMS.md",
                "risks_file": "RISKS.md",
                "lessons_file": "LESSONS_REGISTER.md",
                "logs_dir": ".problem_logs",
                "require_confirmation": True,
                "_saved": False
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(default_config, indent=2, ensure_ascii=False).encode("utf-8"))

    def handle_save(self):
        """处理保存请求 - 先返回响应，再异步保存配置"""
        try:
            # 读取请求体
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            form_data = json.loads(post_data.decode("utf-8"))

            # 先返回成功响应（确保客户端能收到）
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "message": "保存中..."}).encode("utf-8"))
            self.wfile.flush()

            # 在后台线程中保存配置（避免阻塞响应）
            threading.Thread(
                target=self._do_save_config,
                args=(form_data,),
                daemon=True
            ).start()

        except Exception as e:
            print(f"   ❌ 处理保存请求失败：{e}")
            import traceback
            traceback.print_exc()
            try:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
                self.wfile.flush()
            except:
                pass

    def _do_save_config(self, form_data: dict):
        """实际保存配置的逻辑（在后台线程中执行）"""
        try:
            # 确保数据目录存在
            triphasic_home = form_data.get("triphasic_home", str(get_standardization_dir(self.skill_dir)))
            home_dir = Path(triphasic_home).expanduser()
            home_dir.mkdir(parents=True, exist_ok=True)

            # 读取现有配置或使用默认配置
            config_file = home_dir / "config.json"
            if config_file.exists():
                with open(config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
            else:
                # 使用默认配置模板
                default_file = self.server.skill_dir / "assets" / "default_config.json"
                if default_file.exists():
                    with open(default_file, "r", encoding="utf-8") as f:
                        config = json.load(f)
                else:
                    config = {}

            # 更新配置字段
            config["mode"] = form_data.get("mode", "on_demand")
            config["triphasic_home"] = triphasic_home
            config["problems_file"] = form_data.get("problems_file", "PROBLEMS.md")
            config["risks_file"] = form_data.get("risks_file", "RISKS.md")
            config["lessons_file"] = form_data.get("lessons_file", "LESSONS_REGISTER.md")
            config["logs_dir"] = form_data.get("logs_dir", ".problem_logs")

            # 完整 hooks 配置
            hooks_from_form = form_data.get("hooks", {})
            if hooks_from_form:
                if "hooks" not in config:
                    config["hooks"] = {}
                config["hooks"].update(hooks_from_form)
            # 兼容旧版表单提交（只有 require_confirmation）
            elif "require_confirmation" in form_data:
                if "hooks" not in config:
                    config["hooks"] = {}
                config["hooks"]["require_task_confirmation"] = form_data.get("require_confirmation", True)

            # 添加 _saved 标记（让 HTML 轮询检测到）
            config["_saved"] = True

            # 写入 config.json
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            print(f"   ✅ 配置已保存到：{config_file}")

            # 更新 SKILL.md
            update_skill_md(self.server.skill_dir, config)

            # 注意：不创建 .settings_done，让服务器继续运行
            # .settings_done 只在用户明确结束设置时创建
            print(f"   💡 配置已保存，服务器保持运行")

        except Exception as e:
            print(f"   ❌ 保存配置失败：{e}")
            import traceback
            traceback.print_exc()

    def send_done_page(self):
        """返回"设置已完成"页面，并创建标志文件"""
        # 创建 .settings_done 标志文件（通知主进程退出）
        done_flag = self.server.skill_dir / ".settings_done"
        done_flag.touch()
        print(f"   ✅ 已创建标志文件：{done_flag}")

        html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>设置已完成</title>
    <style>
        body { font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #1a1a2e; color: #4ecdc4; }
        .message { text-align: center; }
        .message h1 { font-size: 48px; }
        .message p { font-size: 18px; color: #e0e0e0; }
    </style>
</head>
<body>
    <div class="message">
        <h1>✅</h1>
        <p>设置已保存！可关闭此页面。</p>
    </div>
</body>
</html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))


def start_server(skill_dir: Path, home_dir: Path, port: int) -> HTTPServer:
    """启动 HTTP 服务器"""
    server = HTTPServer(("localhost", port), SettingsHandler)
    server.skill_dir = skill_dir
    server.home_dir = home_dir
    return server


def main():
    global SERVER_INSTANCE

    parser = argparse.ArgumentParser(description="Triphasic Execution - 设置界面")
    parser.add_argument("--skill-dir", type=str, default=None, help="技能目录路径")
    parser.add_argument("--home", type=str, default=None, help="数据目录路径")
    parser.add_argument("--port", type=int, default=None, help="指定端口（默认随机 8080-8999）")
    parser.add_argument("--save-config", type=str, default=None, help="保存配置（JSON 字符串），不启动服务器")
    parser.add_argument("--serve-only", action="store_true", help="只启动 HTTP 服务器，返回端口号后退出（供 Agent 调用）")
    args = parser.parse_args()

    # 确定路径
    skill_dir = get_skill_dir(args)
    home_dir = get_home_dir(args, skill_dir)

    # 如果提供了 --save-config，直接保存并退出
    if args.save_config:
        return save_config_from_json(skill_dir, home_dir, args.save_config)

    # 查找可用端口
    if args.port:
        port = args.port
    else:
        try:
            port = find_available_port()
        except RuntimeError as e:
            print(f"   ❌ {e}")
            sys.exit(1)

    if args.serve_only:
        # 只启动服务器，打印端口号，然后阻塞等待设置完成
        server = start_server(skill_dir, home_dir, port)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        # 清理旧标志文件
        done_flag = skill_dir / ".settings_done"
        if done_flag.exists():
            done_flag.unlink()
        # 只输出端口号，方便 Agent 解析
        print(f"SERVER_STARTED:{port}")
        # 阻塞等待用户完成设置
        try:
            while not done_flag.exists():
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        print(f"   ✅ 检测到设置完成，正在关闭服务器...")
        server.shutdown()
        server.server_close()
        print(f"✅ 设置完成")
        sys.exit(0)

    print(f"⚙️  启动 Triphasic Execution 设置界面...")
    print(f"   📂 技能目录：{skill_dir}")
    print(f"   📁 数据目录：{home_dir}")

    # 启动 HTTP 服务器
    server = start_server(skill_dir, home_dir, port)
    SERVER_INSTANCE = server

    # 在后台线程中运行服务器
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    # 清理旧的标志文件
    done_flag = skill_dir / ".settings_done"
    if done_flag.exists():
        done_flag.unlink()

    print(f"   ✅ 服务器已启动：http://localhost:{port}/")
    print(f"   💡 Agent 请执行：webbrowser.open('http://localhost:{port}/')")
    print(f"   ⏳ 等待用户完成设置（检查 {done_flag} 标志文件）...")
    print(f"   🛑 设置完成后调用 shutdown_server() 关闭服务器")

    # 阻塞等待用户完成设置
    try:
        while not done_flag.exists():
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n   ⚠️  用户中断")

    # 停止服务器
    print(f"   🛑 正在关闭服务器...")
    server.shutdown()
    server.server_close()
    print(f"✅ 设置完成")
    return 0

def shutdown_server():
    """
    关闭当前运行的 HTTP 服务器（供 Agent 调用）
    通过 .settings_done 标志文件通知主进程退出
    """
    skill_dir = Path(__file__).parent.parent
    done_flag = skill_dir / ".settings_done"
    done_flag.touch()
    print(f"   ✅ 已创建标志文件：{done_flag}")
    print(f"   💡 主进程将在 1 秒内检测到并退出")


if __name__ == "__main__":
    sys.exit(main())
