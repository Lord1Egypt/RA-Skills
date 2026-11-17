# -*- coding: utf-8 -*-
"""版本升级/紧急通知 UI 展示模块（#3-3 双通道 + #3-5 紧急通知）

功能：
1. 控制台顶部蓝色横幅（可关闭）：不打断用户操作，仅输出一段格式化文本
2. 右下角非阻塞弹窗（HTML 浮窗）：生成临时 HTML 文件，5 秒自动淡出，不打断用户正在执行的崩溃修复/翻译任务
3. 紧急通知模式（urgent_notice）：红色背景横幅，优先级高于普通版本升级提醒
4. 三按钮：[立即前往平台更新] [7 天后再提醒] [跳过此版本]
5. 顺带嵌入「查看我的机器码」按钮入口（#3-4 要求）

注意：UI 设计原则
- 控制台横幅：兼容任何终端（无 ANSI 颜色时自动降级为 ASCII 边框）
- HTML 弹窗：独立文件，不依赖 main.py 的本地服务器；用 <script>setTimeout</script> 实现 5 秒自动淡出
"""

import json
import logging
import os
import platform
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from core.version_checker import (
    skip_version, remind_me_later, PLATFORM_DISPLAY_NAMES
)

logger = logging.getLogger(__name__)

# ANSI 颜色代码（控制台横幅使用）
ANSI_BLUE_BG = "\033[44m"
ANSI_RED_BG = "\033[41m"
ANSI_YELLOW_BG = "\033[43m"
ANSI_WHITE = "\033[97m"
ANSI_BOLD = "\033[1m"
ANSI_RESET = "\033[0m"

# 本次会话内是否已经显示过横幅（避免每次调用 Skill 都重复打印）
_session_banner_shown = False
_session_popup_shown = False


def _supports_ansi() -> bool:
    """粗略判断当前终端是否支持 ANSI 颜色"""
    if os.environ.get("NO_COLOR"):
        return False
    if platform.system() == "Windows":
        # Windows Terminal 和 PowerShell 7+ 支持 ANSI
        term = os.environ.get("TERM", "")
        return term != "" or "WT_SESSION" in os.environ
    return True


def _get_machine_id_for_banner() -> str:
    """获取机器码（供横幅二级菜单使用）
    
    从 auth_manager 导入，若失败则返回占位提示
    """
    try:
        from core.auth_manager import get_current_auth_state
        state = get_current_auth_state()
        mid = state.get("machine_id", "")
        return mid[:16] + "..." if len(mid) > 16 else mid
    except Exception:
        return ""  # 获取失败时降级为空，由上层渲染逻辑决定是否显示


def render_console_banner(update_info: Dict[str, Any]) -> str:
    """渲染控制台顶部横幅文本
    
    返回一个可直接 print 的字符串。
    支持 ANSI 颜色时用蓝/红底白字，否则降级为 ASCII + === 边框。
    """
    info_type = update_info.get("type", "update")
    is_urgent = info_type == "urgent_notice" or bool(update_info.get("urgent_notice", ""))
    platform_name = update_info.get("platform_display_name", "该平台")
    cur_ver = update_info.get("current_version", "?")
    rem_ver = update_info.get("remote_version", "?")
    release_notes = update_info.get("release_notes", "")
    urgent_text = update_info.get("urgent_notice", "")
    download_url = update_info.get("download_url", "（请前往 " + platform_name + " 搜索本 Skill 下载）")

    supports_ansi = _supports_ansi()

    if is_urgent and urgent_text:
        # ===== 紧急通知横幅（红底）=====
        title = "📢 紧急通知"
        headline = urgent_text
    else:
        # ===== 版本升级横幅（蓝底）=====
        title = "📢 版本更新提醒"
        headline = "您从 {} 下载的版本已有更新 V{} → V{}".format(
            platform_name, cur_ver, rem_ver
        )

    # 构建亮点摘要（从 release_notes 取前 2 行）
    highlights = []
    if release_notes:
        lines = [ln.strip() for ln in release_notes.split("\n") if ln.strip()]
        highlights = lines[:2]

    lines = []
    border_char = "=" if not supports_ansi else ""
    W = 82

    if not supports_ansi:
        # ASCII 降级模式
        lines.append(border_char * W)
        lines.append("【{}】".format(title))
        lines.append("  " + headline)
        if highlights:
            lines.append("  ▸ 更新亮点：")
            for h in highlights:
                lines.append("    · " + h[:70])
        lines.append("  📥 更新地址：{}".format(download_url[:70]))
        lines.append("  操作：[1] 记住该URL手动更新  [2] 7天后再提醒  [3] 跳过V{}".format(rem_ver))
        lines.append("  💡 提示：「查看我的机器码」→ {}".format(_get_machine_id_for_banner()))
        lines.append(border_char * W)
    else:
        # ANSI 彩色模式
        bg = ANSI_RED_BG if is_urgent else ANSI_BLUE_BG
        bar_top = bg + ANSI_WHITE + ANSI_BOLD + " " * W + ANSI_RESET
        def color_line(text: str) -> str:
            # 每一行都填满 W 宽度，背景一致
            padded = text + " " * max(0, W - 2 - len(text))
            return bg + ANSI_WHITE + " " + padded + " " + ANSI_RESET

        lines.append("")  # 顶部留一行空
        lines.append(bar_top)
        lines.append(color_line("【{}】 {}".format(title, headline)))
        lines.append(color_line(""))
        if highlights:
            lines.append(color_line("▸ 更新亮点："))
            for h in highlights:
                lines.append(color_line("  · " + h[:72]))
        if is_urgent:
            # 紧急通知时也显示版本升级链接（如果有）
            if rem_ver != cur_ver:
                lines.append(color_line("▸ 同时有新版本 V{} → V{}".format(cur_ver, rem_ver)))
        lines.append(color_line(""))
        lines.append(color_line("📥 更新地址：{}".format(download_url[:70])))
        lines.append(color_line("💡 机器码预览：{}   【反馈/帮助 → 可发送机器码给作者手动开通】".format(
            _get_machine_id_for_banner()
        )))
        lines.append(color_line(""))
        lines.append(bar_top)
        lines.append("")  # 底部留一行空

    return "\n".join(lines)


def show_console_banner_if_needed(update_info: Optional[Dict[str, Any]]) -> bool:
    """调用版本检查结果，如果需要显示横幅则 print 出来
    
    Args:
        update_info: check_for_updates() 的返回值，None 表示不需要提醒
    
    Returns:
        True 表示本次调用实际打印了横幅，False 表示未打印
    """
    global _session_banner_shown
    if update_info is None:
        return False
    if _session_banner_shown:
        # 本次会话已显示过，不再重复
        return False
    banner_text = render_console_banner(update_info)
    print(banner_text, flush=True)
    _session_banner_shown = True
    logger.info("[版本UI] 控制台横幅已输出（来源: {}, 远端版本: {}）".format(
        update_info.get("download_source"), update_info.get("remote_version")
    ))
    return True


# === HTML 右下角弹窗 ===

def _build_popup_html(update_info: Dict[str, Any]) -> str:
    """构建右下角非阻塞弹窗的 HTML 内容
    
    设计要点：
    - fixed 定位在右下角，宽度 420px
    - 5 秒后自动淡出（不透明度 0 → 再 1 秒后 display:none，不影响用户操作页面）
    - 三个按钮（跳转更新 / 7天后 / 跳过）通过 query 参数重定向到本地 API 或直接提示用户
    - 顺带提供一键复制机器码按钮（#3-4）
    - 紧急通知时用红黄色渐变背景
    """
    info_type = update_info.get("type", "update")
    is_urgent = info_type == "urgent_notice" or bool(update_info.get("urgent_notice", ""))
    platform_name = update_info.get("platform_display_name", "该平台")
    cur_ver = update_info.get("current_version", "?")
    rem_ver = update_info.get("remote_version", "?")
    release_notes = update_info.get("release_notes", "")
    urgent_text = update_info.get("urgent_notice", "")
    download_url = update_info.get("download_url", "#")
    remote_ver_safe = json.dumps(rem_ver, ensure_ascii=False)

    # 亮点 HTML
    highlights_html = ""
    if release_notes:
        lines = [ln.strip() for ln in release_notes.split("\n") if ln.strip()]
        for h in lines[:3]:
            highlights_html += "<li>{}</li>".format(h[:100])

    # 标题/副标题
    if is_urgent and urgent_text:
        title_text = "📢 紧急通知"
        subtitle_html = '<div class="urgent-text">{}</div>'.format(urgent_text)
        card_class = "card urgent"
    else:
        title_text = "📢 版本更新提醒"
        subtitle_html = '<div class="ver">您从 <b>{}</b> 下载的版本有更新<br><span class="v-pill">V{}</span> → <span class="v-pill new">V{}</span></div>'.format(
            platform_name, cur_ver, rem_ver
        )
        card_class = "card"

    # 机器码
    machine_id = _get_machine_id_for_banner()

    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>MC Skill - 版本提醒</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; font-family: "Microsoft YaHei", system-ui, -apple-system, sans-serif; }}
  body {{ background: transparent; }}
  /* 右下角卡片 */
  .card {{
    position: fixed;
    right: 24px;
    bottom: 24px;
    width: 420px;
    border-radius: 14px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.18), 0 2px 6px rgba(0,0,0,0.1);
    overflow: hidden;
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    color: #fff;
    z-index: 99999;
    animation: slideIn 0.35s cubic-bezier(0.2, 0.9, 0.3, 1.2);
    transition: opacity 0.8s ease, transform 0.8s ease;
  }}
  .card.urgent {{
    background: linear-gradient(135deg, #dc2626 0%, #b91c1c 50%, #f59e0b 100%);
  }}
  .card.hide {{
    opacity: 0;
    transform: translateY(20px);
    pointer-events: none;
  }}
  @keyframes slideIn {{
    from {{ opacity: 0; transform: translateY(40px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
  }}
  .card-header {{
    padding: 16px 20px 10px 20px;
    display: flex; align-items: center; justify-content: space-between;
  }}
  .card-title {{ font-size: 17px; font-weight: 700; }}
  .close-btn {{
    cursor: pointer; background: rgba(255,255,255,0.2);
    width: 26px; height: 26px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; color: #fff; border: none;
  }}
  .close-btn:hover {{ background: rgba(255,255,255,0.3); }}
  .card-body {{ padding: 6px 20px 14px 20px; }}
  .urgent-text {{
    font-size: 15px; line-height: 1.55;
    background: rgba(255,255,255,0.15);
    padding: 10px 12px; border-radius: 8px;
    margin-bottom: 10px;
  }}
  .ver {{ font-size: 14px; line-height: 1.6; margin-bottom: 10px; }}
  .v-pill {{
    display: inline-block; background: rgba(255,255,255,0.2);
    padding: 2px 8px; border-radius: 999px; font-size: 12px; margin: 0 2px;
  }}
  .v-pill.new {{ background: #fbbf24; color: #1f2937; font-weight: 700; }}
  .highlights {{
    font-size: 13px; line-height: 1.65;
    background: rgba(255,255,255,0.12);
    border-radius: 8px; padding: 8px 12px 8px 26px;
    margin-bottom: 10px;
  }}
  .mid-row {{
    font-size: 12px; opacity: 0.9;
    display: flex; align-items: center; justify-content: space-between;
    background: rgba(0,0,0,0.12);
    padding: 6px 10px; border-radius: 6px;
    margin-bottom: 12px;
  }}
  .mid-row code {{
    background: rgba(255,255,255,0.18);
    padding: 1px 6px; border-radius: 4px;
    font-family: Consolas, monospace;
  }}
  .copy-btn {{
    cursor: pointer; background: rgba(255,255,255,0.2);
    border: none; color: #fff; padding: 2px 8px;
    border-radius: 4px; font-size: 11px;
  }}
  .copy-btn:hover {{ background: rgba(255,255,255,0.3); }}
  .actions {{
    display: flex; gap: 8px; flex-wrap: wrap;
  }}
  .btn {{
    flex: 1; min-width: 100px;
    padding: 8px 10px; border: none; border-radius: 8px;
    font-size: 13px; font-weight: 600; cursor: pointer;
    transition: transform 0.15s;
  }}
  .btn:hover {{ transform: translateY(-1px); }}
  .btn-primary {{ background: #ffffff; color: #1d4ed8; }}
  .card.urgent .btn-primary {{ color: #b91c1c; }}
  .btn-secondary {{
    background: rgba(255,255,255,0.18); color: #fff;
    border: 1px solid rgba(255,255,255,0.3);
  }}
  .btn-ghost {{
    background: transparent; color: #fff;
    border: 1px solid rgba(255,255,255,0.25);
    opacity: 0.85;
  }}
  .card-footer {{
    font-size: 11px; opacity: 0.75;
    padding: 8px 20px 14px 20px;
    text-align: center;
  }}
  /* 复制成功提示 */
  .toast {{
    position: fixed; right: 24px; bottom: 180px;
    background: rgba(0,0,0,0.8); color: #fff;
    padding: 8px 16px; border-radius: 6px; font-size: 13px;
    opacity: 0; transition: opacity 0.3s;
    z-index: 100000;
  }}
  .toast.show {{ opacity: 1; }}
</style>
</head>
<body>

<div class="{card_class}" id="card">
  <div class="card-header">
    <div class="card-title">{title_text}</div>
    <button class="close-btn" onclick="closeCard()" title="本次会话不再显示">✕</button>
  </div>
  <div class="card-body">
    {subtitle_html}
    {highlights_block}
    <div class="mid-row">
      <span>💡 我的机器码：<code id="mid">{mid}</code></span>
      <button class="copy-btn" onclick="copyMid()">一键复制</button>
    </div>
    <div class="actions">
      <a href="{download_url}" target="_blank" class="btn btn-primary" onclick="markDismissed()">
        🔗 前往 {platform_name} 更新
      </a>
      <button class="btn btn-secondary" onclick="remindLater()">7 天后提醒</button>
      <button class="btn btn-ghost" onclick="skipVersion()">跳过 V{rem_ver}</button>
    </div>
  </div>
  <div class="card-footer">5 秒后自动收起 · 也可点右上角 ✕ 立即关闭</div>
</div>

<div class="toast" id="toast">✅ 已复制到剪贴板</div>

<script>
  const card = document.getElementById('card');
  const toast = document.getElementById('toast');

  // 5 秒后自动淡出
  let autoTimer = setTimeout(() => closeCard(), 5000);

  function closeCard() {{
    clearTimeout(autoTimer);
    card.classList.add('hide');
    // 0.8 秒后完全消失
    setTimeout(() => {{ card.style.display = 'none'; }}, 900);
  }}

  function showToast(msg) {{
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 1800);
  }}

  function copyMid() {{
    const mid = document.getElementById('mid').textContent;
    try {{
      navigator.clipboard.writeText(mid).then(() => {{
        showToast('✅ 机器码已复制，请发给作者开通授权');
      }}).catch(() => fallbackCopy(mid));
    }} catch (e) {{
      fallbackCopy(mid);
    }}
  }}
  function fallbackCopy(text) {{
    const ta = document.createElement('textarea');
    ta.value = text; document.body.appendChild(ta);
    ta.select(); document.execCommand('copy');
    document.body.removeChild(ta);
    showToast('✅ 机器码已复制（兼容模式）');
  }}

  // 用户操作：通过锚点写入 hash，下次打开页面时读取（轻量回写）
  function remindLater() {{
    showToast('⏰ 好的，7 天后再提醒您');
    setTimeout(closeCard, 600);
    // 通过 query 参数尝试触发外部 API 回写
    try {{
      const img = new Image();
      img.src = 'http://127.0.0.1:8765/api/version-action?action=remind_later&_=' + Date.now();
    }} catch(e) {{}}
  }}
  function skipVersion() {{
    const ver = {remote_ver_safe};
    showToast('⏭️ 已跳过 V' + ver + '，不再提醒此版本');
    setTimeout(closeCard, 600);
    try {{
      const img = new Image();
      img.src = 'http://127.0.0.1:8765/api/version-action?action=skip&version=' + encodeURIComponent(ver) + '&_=' + Date.now();
    }} catch(e) {{}}
  }}
  function markDismissed() {{
    // 用户点击跳转，视为已处理
    setTimeout(closeCard, 300);
  }}
</script>

</body>
</html>
""".format(
        card_class=card_class,
        title_text=title_text,
        subtitle_html=subtitle_html,
        highlights_block='<ul class="highlights">{}</ul>'.format(highlights_html) if highlights_html else "",
        mid=machine_id,
        download_url=download_url,
        platform_name=platform_name,
        rem_ver=rem_ver,
        remote_ver_safe=remote_ver_safe,
    )
    return html


def show_popup_html_if_needed(update_info: Optional[Dict[str, Any]]) -> Optional[str]:
    """生成右下角弹窗 HTML 文件到 output/ 目录
    
    Args:
        update_info: check_for_updates() 的返回值
    
    Returns:
        返回生成的 HTML 文件路径（如果生成了），否则 None
        注意：本函数只生成文件，不自动打开浏览器——避免打断用户正在执行的崩溃修复/翻译任务
              调用方可以在合适时机（如任务结束后）用 webbrowser.open() 打开
    """
    global _session_popup_shown
    if update_info is None:
        return None
    if _session_popup_shown:
        return None
    _session_popup_shown = True

    project_root = Path(__file__).resolve().parent.parent
    output_dir = project_root / "output"
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = output_dir / "version_update_{}.html".format(timestamp)
    try:
        html = _build_popup_html(update_info)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
        logger.info("[版本UI] 弹窗HTML已生成: {}".format(file_path))
        return str(file_path)
    except Exception as e:
        logger.warning("[版本UI] 生成弹窗HTML失败: {}".format(e))
        return None


def handle_version_action(action: str, version: Optional[str] = None) -> Dict[str, Any]:
    """处理用户在 HTML 弹窗中点击按钮的 API 回调（供 main.py 路由调用）
    
    Args:
        action: "remind_later" | "skip" | "dismiss"
        version: 仅 skip 时需要（跳过的版本号）
    
    Returns:
        可 JSON 序列化的响应
    """
    try:
        if action == "remind_later":
            remind_me_later(7)
            return {"ok": True, "action": "remind_later", "msg": "7 天后再提醒"}
        elif action == "skip" and version:
            skip_version(version)
            return {"ok": True, "action": "skip", "msg": "已跳过版本 {}".format(version)}
        elif action == "dismiss":
            return {"ok": True, "action": "dismiss", "msg": "已关闭横幅"}
        else:
            return {"ok": False, "msg": "未知 action: {}".format(action)}
    except Exception as e:
        logger.warning("[版本UI] 处理操作失败: {}".format(e))
        return {"ok": False, "msg": str(e)}
