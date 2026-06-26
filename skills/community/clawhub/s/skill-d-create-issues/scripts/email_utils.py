"""
Skill-D 邮件 HTML 构建器。
三种邮件：
  1. 正式纪要邮件（全员）
  2. 个人任务通知邮件（每位 assignee 单独一封）
  3. 跨项目建议邮件（组织者）
"""


def _base_style():
    return (
        'font-family: Arial, "PingFang SC", sans-serif; '
        'max-width: 600px; margin: 0 auto; padding: 24px; color: #333;'
    )


def _format_time(meeting_dir):
    try:
        parts = meeting_dir.split("-")
        return f"{parts[0]}-{parts[1]}-{parts[2]} {parts[3][:2]}:{parts[3][2:]}"
    except Exception:
        return meeting_dir


# ─────────────────────────────────────────────────────────────────────────────
# 1. 正式纪要邮件（全员）
# ─────────────────────────────────────────────────────────────────────────────

def build_minutes_html(topic, meeting_dir, repo, organizer,
                       join_url, created_issues, failed_issues,
                       gitea_base_url, minutes_content_summary=""):
    """
    正式纪要邮件，发给全体参会人。
    created_issues: [{local_id, issue_number, issue_url, assignee, task}]
    failed_issues:  [{local_id, task, error}]
    minutes_content_summary: minutes.md 的前 500 字（OpenClaw 提取的摘要文本）
    """
    time_label   = _format_time(meeting_dir)
    dir_url      = f"{gitea_base_url.rstrip('/')}/{repo}/src/branch/main/meetings/{meeting_dir}/"
    minutes_url  = f"{dir_url}minutes.md"

    # 已建 issue 列表
    if created_issues:
        issue_rows = "".join(
            f'<tr>'
            f'<td style="padding:8px 12px;border:1px solid #e0e0e0;">'
            f'<a href="{i["issue_url"]}" style="color:#1a73e8;">#{i["issue_number"]}</a></td>'
            f'<td style="padding:8px 12px;border:1px solid #e0e0e0;">{i["task"]}</td>'
            f'<td style="padding:8px 12px;border:1px solid #e0e0e0;">@{i["assignee"]}</td>'
            f'</tr>'
            for i in created_issues
        )
        issue_section = f"""
<h3 style="color:#34a853;margin:24px 0 12px;">✅ 已创建 Gitea Issue（{len(created_issues)} 条）</h3>
<table style="border-collapse:collapse;width:100%;font-size:13px;">
  <tr style="background:#f8f9fa;">
    <th style="padding:8px 12px;border:1px solid #e0e0e0;text-align:left;width:70px;">#</th>
    <th style="padding:8px 12px;border:1px solid #e0e0e0;text-align:left;">任务</th>
    <th style="padding:8px 12px;border:1px solid #e0e0e0;text-align:left;width:120px;">负责人</th>
  </tr>
  {issue_rows}
</table>"""
    else:
        issue_section = '<p style="color:#666;">本次会议未创建 Gitea Issue。</p>'

    # 失败提示
    failed_section = ""
    if failed_issues:
        failed_list = "".join(
            f'<li>{f["task"]}（{f["error"]}）</li>'
            for f in failed_issues
        )
        failed_section = f"""
<div style="background:#fff3e0;border-left:4px solid #e65100;padding:12px 16px;
            margin:16px 0;border-radius:4px;">
  <p style="margin:0 0 8px;font-weight:bold;">⚠️ 以下任务创建失败，请手动处理：</p>
  <ul style="margin:0;padding-left:20px;">{failed_list}</ul>
</div>"""

    # 纪要摘要
    summary_section = ""
    if minutes_content_summary:
        summary_section = f"""
<h3 style="color:#1a73e8;margin:24px 0 12px;">📝 会议纪要摘要</h3>
<div style="background:#f8f9fa;padding:16px;border-radius:4px;font-size:13px;
            white-space:pre-line;line-height:1.6;">{minutes_content_summary}</div>"""

    return f"""<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"></head>
<body style="{_base_style()}">

  <h2 style="color:#1a73e8;margin-bottom:4px;">📋 会议纪要正式发布</h2>
  <p style="color:#666;margin-top:0;">以下是本次会议的正式纪要与任务安排。</p>

  <table style="border-collapse:collapse;width:100%;margin:16px 0;font-size:14px;">
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;
                 width:110px;border:1px solid #e0e0e0;">会议主题</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">{topic}</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;
                 border:1px solid #e0e0e0;">会议时间</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">{time_label}</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;
                 border:1px solid #e0e0e0;">组织者</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">{organizer}</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;
                 border:1px solid #e0e0e0;">所属项目</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">{repo}</td>
    </tr>
  </table>

  {summary_section}
  {issue_section}
  {failed_section}

  <div style="margin:24px 0;">
    <a href="{minutes_url}"
       style="background:#1a73e8;color:white;padding:11px 22px;text-decoration:none;
              border-radius:5px;display:inline-block;font-size:14px;margin-right:10px;">
      📝 查看完整会议纪要
    </a>
    <a href="{dir_url}"
       style="background:#34a853;color:white;padding:11px 22px;text-decoration:none;
              border-radius:5px;display:inline-block;font-size:14px;">
      📁 查看会议目录
    </a>
  </div>

  <hr style="border:none;border-top:1px solid #e8e8e8;margin:24px 0;">
  <p style="color:#999;font-size:12px;margin:0;">本邮件由 AIFusion Bot 自动发送，请勿直接回复。</p>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
# 2. 个人任务通知邮件（每位 assignee 单独一封）
# ─────────────────────────────────────────────────────────────────────────────

def build_assignee_html(assignee_username, tasks, topic, meeting_dir,
                        repo, gitea_base_url):
    """
    个人任务通知邮件。
    tasks: [{issue_number, issue_url, task, due_date, depends_on_str, quote}]
    """
    time_label = _format_time(meeting_dir)

    task_cards = ""
    for t in tasks:
        due = t.get("due_date", "")
        due_str = f'<p style="margin:4px 0;color:#666;font-size:13px;">📅 截止日期：{due}</p>' if due else ""
        dep = t.get("depends_on_str", "")
        dep_str = f'<p style="margin:4px 0;color:#666;font-size:13px;">🔗 依赖：{dep}</p>' if dep else ""
        quote = t.get("quote", "")
        quote_str = (
            f'<blockquote style="border-left:3px solid #ccc;margin:8px 0 0;'
            f'padding:6px 12px;color:#666;font-size:12px;">{quote}</blockquote>'
        ) if quote else ""

        task_cards += f"""
<div style="border:1px solid #e0e0e0;border-radius:6px;padding:14px 16px;
            margin:12px 0;background:#fafafa;">
  <p style="margin:0 0 6px;font-weight:bold;">
    <a href="{t.get('issue_url','')}" style="color:#1a73e8;text-decoration:none;">
      #{t.get('issue_number','')}
    </a>
    {t.get('task','')}
  </p>
  {due_str}{dep_str}{quote_str}
</div>"""

    return f"""<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"></head>
<body style="{_base_style()}">

  <h2 style="color:#1a73e8;margin-bottom:4px;">📌 您有新的会议任务</h2>
  <p style="color:#666;margin-top:0;">
    以下任务在 <strong>{topic}</strong>（{time_label}）中分配给您，请及时跟进。
  </p>

  {task_cards}

  <div style="background:#e8f5e9;border-left:4px solid #34a853;padding:12px 16px;
              margin:20px 0;border-radius:4px;">
    <p style="margin:0;font-size:13px;">
      💡 请在 Gitea 中打开对应 issue，更新进度或关闭 issue 以完成任务跟踪。
    </p>
  </div>

  <hr style="border:none;border-top:1px solid #e8e8e8;margin:24px 0;">
  <p style="color:#999;font-size:12px;margin:0;">
    本邮件由 AIFusion Bot 自动发送，请勿直接回复。<br>
    所属项目：{repo}
  </p>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
# 3. 跨项目建议邮件（组织者）
# ─────────────────────────────────────────────────────────────────────────────

def build_cross_project_html(topic, meeting_dir, repo, confirmed_issue_content,
                              gitea_base_url):
    """
    跨项目会议不自动建 issue，向组织者发送建议邮件。
    confirmed_issue_content：confirmed_issue.md 的完整文本。
    """
    time_label = _format_time(meeting_dir)
    dir_url    = f"{gitea_base_url.rstrip('/')}/{repo}/src/branch/main/meetings/{meeting_dir}/"

    # 渲染 confirmed_issue 内容（截断过长内容）
    content_preview = confirmed_issue_content[:3000]
    if len(confirmed_issue_content) > 3000:
        content_preview += "\n\n...（内容过长，已截断，请到 Gitea 查看完整版）"

    return f"""<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"></head>
<body style="{_base_style()}">

  <h2 style="color:#7b1fa2;margin-bottom:4px;">📋 跨项目会议 Issue 建议（需人工处理）</h2>
  <p style="color:#666;margin-top:0;">
    本次会议为跨项目会议，系统不会自动创建 Gitea Issue。
    以下是 AI 从会议转录中提取的 issue 建议，请组织者参考后自行处理。
  </p>

  <table style="border-collapse:collapse;width:100%;margin:16px 0;font-size:14px;">
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;
                 width:110px;border:1px solid #e0e0e0;">会议主题</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">{topic}</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;
                 border:1px solid #e0e0e0;">会议时间</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">{time_label}</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;background:#f8f9fa;font-weight:bold;
                 border:1px solid #e0e0e0;">存档仓库</td>
      <td style="padding:10px 14px;border:1px solid #e0e0e0;">{repo}</td>
    </tr>
  </table>

  <h3 style="color:#7b1fa2;margin:20px 0 10px;">Issue 建议内容</h3>
  <div style="background:#f8f9fa;padding:16px;border-radius:4px;font-size:13px;
              white-space:pre-line;line-height:1.7;border:1px solid #e0e0e0;">
{content_preview}
  </div>

  <div style="margin:24px 0;">
    <a href="{dir_url}"
       style="background:#7b1fa2;color:white;padding:11px 22px;text-decoration:none;
              border-radius:5px;display:inline-block;font-size:14px;">
      📁 查看会议目录
    </a>
  </div>

  <hr style="border:none;border-top:1px solid #e8e8e8;margin:24px 0;">
  <p style="color:#999;font-size:12px;margin:0;">本邮件由 AIFusion Bot 自动发送，请勿直接回复。</p>
</body>
</html>"""
