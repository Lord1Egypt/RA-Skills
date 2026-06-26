"""
Skill-H 通知邮件 HTML 构建器。
生成取消通知、改期通知、新会议待确认通知三种邮件正文。
实际发送由 OpenClaw 调用 imap-smtp-email 完成。
"""

from datetime import datetime


def _format_time(dt_or_str):
    """将 datetime 或 ISO 字符串格式化为可读时间。"""
    if isinstance(dt_or_str, str):
        from dateutil.parser import parse as parse_dt
        import pytz
        try:
            dt = parse_dt(dt_or_str).astimezone(pytz.timezone("Asia/Shanghai"))
        except Exception:
            return dt_or_str
    else:
        dt = dt_or_str
    return dt.strftime("%Y-%m-%d %H:%M")


def _base_style():
    return (
        'font-family: Arial, "PingFang SC", sans-serif; '
        'max-width: 600px; margin: 0 auto; padding: 24px; color: #333;'
    )


# ─────────────────────────────────────────────────────────────────────────────
# 取消通知
# ─────────────────────────────────────────────────────────────────────────────

def build_cancel_html(topic, scheduled_time, meeting_code, repo, organizer, reason=""):
    time_str = _format_time(scheduled_time)
    reason_row = (
        f'<tr><td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;'
        f'width:110px;border:1px solid #e0e0e0;">取消原因</td>'
        f'<td style="padding:10px 14px;border:1px solid #e0e0e0;">{reason}</td></tr>'
    ) if reason else ""

    return f"""<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"></head>
<body style="{_base_style()}">
  <h2 style="color:#e53935;margin-bottom:4px;">❌ 会议已取消</h2>
  <p style="color:#666;margin-top:0;">以下会议已从腾讯会议中取消，请知悉。</p>

  <table style="border-collapse:collapse;width:100%;margin:20px 0;font-size:14px;">
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;width:110px;border:1px solid #e0e0e0;">会议主题</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">{topic}</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;border:1px solid #e0e0e0;">原定时间</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">{time_str}（北京时间）</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;border:1px solid #e0e0e0;">会议号</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;font-family:monospace;font-size:15px;letter-spacing:2px;">{meeting_code}</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;border:1px solid #e0e0e0;">所属项目</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">{repo}</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;border:1px solid #e0e0e0;">组织者</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">{organizer}</td>
    </tr>
    {reason_row}
  </table>

  <hr style="border:none;border-top:1px solid #e8e8e8;margin:24px 0;">
  <p style="color:#999;font-size:12px;margin:0;">本邮件由 AIFusion Bot 自动发送，请勿直接回复。</p>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
# 改期通知
# ─────────────────────────────────────────────────────────────────────────────

def build_reschedule_html(topic, old_time, new_time, new_meeting_code,
                          new_join_url, repo, organizer, new_agenda_url=""):
    old_str = _format_time(old_time)
    new_str = _format_time(new_time)

    agenda_btn = (
        f'<a href="{new_agenda_url}" style="background:#34a853;color:white;padding:11px 22px;'
        f'text-decoration:none;border-radius:5px;display:inline-block;font-size:14px;">📝 查看新议程</a>'
    ) if new_agenda_url else ""

    return f"""<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"></head>
<body style="{_base_style()}">
  <h2 style="color:#f57c00;margin-bottom:4px;">🔄 会议已改期</h2>
  <p style="color:#666;margin-top:0;">以下会议已重新安排时间，请更新您的日程。</p>

  <table style="border-collapse:collapse;width:100%;margin:20px 0;font-size:14px;">
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;width:110px;border:1px solid #e0e0e0;">会议主题</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">{topic}</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;background:#fff3e0;font-weight:bold;border:1px solid #e0e0e0;">原定时间</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;text-decoration:line-through;color:#999;">{old_str}</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;background:#e8f5e9;font-weight:bold;border:1px solid #e0e0e0;">新时间</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;font-weight:bold;color:#2e7d32;">{new_str}（北京时间）</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;border:1px solid #e0e0e0;">新会议号</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;font-family:monospace;font-size:15px;letter-spacing:2px;">{new_meeting_code}</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;border:1px solid #e0e0e0;">所属项目</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">{repo}</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;border:1px solid #e0e0e0;">组织者</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">{organizer}</td>
    </tr>
  </table>

  <div style="margin:24px 0;">
    <a href="{new_join_url}" style="background:#1a73e8;color:white;padding:11px 22px;
       text-decoration:none;border-radius:5px;display:inline-block;font-size:14px;margin-right:10px;">
      🎥 加入新腾讯会议
    </a>
    {agenda_btn}
  </div>

  <hr style="border:none;border-top:1px solid #e8e8e8;margin:24px 0;">
  <p style="color:#999;font-size:12px;margin:0;">本邮件由 AIFusion Bot 自动发送，请勿直接回复。</p>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
# 新会议待确认通知（发给组织者/管理员）
# ─────────────────────────────────────────────────────────────────────────────

def build_pending_html(topic, scheduled_time, meeting_code, join_url,
                       meeting_id, meta_repo, meeting_dir):
    time_str = _format_time(scheduled_time)

    return f"""<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"></head>
<body style="{_base_style()}">
  <h2 style="color:#7b1fa2;margin-bottom:4px;">🔔 发现未关联的新会议</h2>
  <p style="color:#666;margin-top:0;">
    腾讯会议中发现一场新会议，尚未关联到任何 Gitea 项目仓库，请确认其归属。
  </p>

  <table style="border-collapse:collapse;width:100%;margin:20px 0;font-size:14px;">
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;width:110px;border:1px solid #e0e0e0;">会议主题</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">{topic}</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;border:1px solid #e0e0e0;">会议时间</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">{time_str}（北京时间）</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;border:1px solid #e0e0e0;">会议号</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;font-family:monospace;font-size:15px;letter-spacing:2px;">{meeting_code}</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;border:1px solid #e0e0e0;">Meeting ID</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;font-family:monospace;">{meeting_id}</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;background:#fff9c4;font-weight:bold;border:1px solid #e0e0e0;">当前状态</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">
        已暂存至 <code>{meta_repo}/meetings/{meeting_dir}/</code>，repo 字段标记为 <strong>pending</strong>
      </td>
    </tr>
  </table>

  <div style="background:#f3e5f5;border-left:4px solid #7b1fa2;padding:16px;margin:20px 0;border-radius:4px;">
    <p style="margin:0 0 8px 0;font-weight:bold;">请选择以下操作之一：</p>
    <ol style="margin:0;padding-left:20px;">
      <li style="margin-bottom:6px;">在 OpenClaw 中说："把 {meeting_dir} 会议归属到 <strong>仓库名</strong>"</li>
      <li>或在 Gitea 中直接编辑 <code>{meta_repo}/meetings/{meeting_dir}/meta.yaml</code>，将 <code>repo: pending</code> 改为对应仓库全名</li>
    </ol>
  </div>

  <div style="margin:24px 0;">
    <a href="{join_url}" style="background:#7b1fa2;color:white;padding:11px 22px;
       text-decoration:none;border-radius:5px;display:inline-block;font-size:14px;">
      🎥 查看腾讯会议
    </a>
  </div>

  <hr style="border:none;border-top:1px solid #e8e8e8;margin:24px 0;">
  <p style="color:#999;font-size:12px;margin:0;">本邮件由 AIFusion Bot 自动发送，请勿直接回复。</p>
</body>
</html>"""
