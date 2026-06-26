"""
邮件内容工具。
只负责生成 HTML，不负责发送。
"""


def build_invitation_html(topic, scheduled_time, join_url, meeting_code,
                          organizer, repo, agenda_url):
    time_str = scheduled_time.strftime("%Y-%m-%d %H:%M")
    return f"""<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"></head>
<body style="font-family: Arial, 'PingFang SC', sans-serif; max-width: 600px;
             margin: 0 auto; padding: 24px; color: #333;">

  <h2 style="color: #1a73e8; margin-bottom: 4px;">📅 会议邀请</h2>
  <p style="color: #666; margin-top: 0;">AIFusion Bot 已为您安排以下会议</p>

  <table style="border-collapse: collapse; width: 100%; margin: 20px 0;
                font-size: 14px;">
    <tr>
      <td style="padding: 10px 14px; background: #f8f9fa; font-weight: bold;
                 width: 110px; border: 1px solid #e0e0e0;">会议主题</td>
      <td style="padding: 10px 14px; border: 1px solid #e0e0e0;">{topic}</td>
    </tr>
    <tr>
      <td style="padding: 10px 14px; background: #f8f9fa; font-weight: bold;
                 border: 1px solid #e0e0e0;">时间</td>
      <td style="padding: 10px 14px; border: 1px solid #e0e0e0;">
        {time_str} <span style="color:#666;">（北京时间）</span>
      </td>
    </tr>
    <tr>
      <td style="padding: 10px 14px; background: #f8f9fa; font-weight: bold;
                 border: 1px solid #e0e0e0;">会议号</td>
      <td style="padding: 10px 14px; border: 1px solid #e0e0e0;
                 font-family: monospace; font-size: 16px; letter-spacing: 2px;">
        {meeting_code}
      </td>
    </tr>
    <tr>
      <td style="padding: 10px 14px; background: #f8f9fa; font-weight: bold;
                 border: 1px solid #e0e0e0;">组织者</td>
      <td style="padding: 10px 14px; border: 1px solid #e0e0e0;">{organizer}</td>
    </tr>
    <tr>
      <td style="padding: 10px 14px; background: #f8f9fa; font-weight: bold;
                 border: 1px solid #e0e0e0;">所属项目</td>
      <td style="padding: 10px 14px; border: 1px solid #e0e0e0;">{repo}</td>
    </tr>
  </table>

  <div style="margin: 24px 0;">
    <a href="{join_url}"
       style="background: #1a73e8; color: white; padding: 11px 22px;
              text-decoration: none; border-radius: 5px; display: inline-block;
              font-size: 14px; margin-right: 10px;">
      🎥 加入腾讯会议
    </a>
    <a href="{agenda_url}"
       style="background: #34a853; color: white; padding: 11px 22px;
              text-decoration: none; border-radius: 5px; display: inline-block;
              font-size: 14px;">
      📝 查看 / 编辑议程
    </a>
  </div>

  <hr style="border: none; border-top: 1px solid #e8e8e8; margin: 24px 0;">
  <p style="color: #999; font-size: 12px; margin: 0;">
    本邮件内容由 Skill-A 生成，实际发送由 imap-smtp-email 完成。
  </p>

</body>
</html>"""
