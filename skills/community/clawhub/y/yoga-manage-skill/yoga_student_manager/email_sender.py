import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import get_email_config, get_alert_thresholds


def send_email(subject, body, to_email=None):
    config = get_email_config()
    if not config:
        raise ValueError("邮箱未配置，请先运行配置")

    sender = config['email']
    password = config['password']
    smtp_server = config['smtp_server']
    smtp_port = config['smtp_port']
    use_ssl = config.get('use_ssl', True)

    recipient = to_email or sender

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    server = None
    try:
        if use_ssl:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=15)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=15)
            server.ehlo()
            server.starttls()
            server.ehlo()

        server.login(sender, password)
        server.sendmail(sender, [recipient], msg.as_string())
        return True
    except smtplib.SMTPAuthenticationError:
        print("邮件发送失败: 邮箱认证失败，请检查账号和授权码")
        return False
    except smtplib.SMTPConnectError:
        print("邮件发送失败: 无法连接SMTP服务器，请检查服务器地址和端口")
        return False
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False
    finally:
        if server:
            try:
                server.quit()
            except Exception:
                pass


def format_student_data(student_data):
    lines = []
    lines.append("=" * 60)
    lines.append("瑜伽学员课时扣除记录")
    lines.append("=" * 60)
    lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    if isinstance(student_data, list):
        lines.append(f"学员总数: {len(student_data)}")
        lines.append("")
        for student in student_data:
            lines.extend(_format_single_student(student))
            lines.append("")
    else:
        lines.extend(_format_single_student(student_data))

    return "\n".join(lines)


def _format_single_student(student):
    thresholds = get_alert_thresholds()
    urgent = thresholds['urgent']
    warn = thresholds['warn']

    lines = []
    lines.append("-" * 60)
    lines.append(f"学员姓名: {student.get('name', 'N/A')}")
    lines.append(f"电话: {student.get('phone', 'N/A')}")
    lines.append(f"微信: {student.get('wechat', 'N/A')}")
    lines.append(f"备注: {student.get('notes', 'N/A')}")
    lines.append("")

    courses = student.get('courses', [])
    if courses:
        lines.append("课程信息:")
        for c in courses:
            lines.append(f"  [{c['id']}] {'线上' if c['course_type'] == 'online' else '线下'}课 | {'包年' if c['package_type'] == 'yearly' else '包课时'}")
            if c['package_type'] == 'hourly':
                remaining = c['remaining_hours']
                lines.append(f"      总课时: {c['total_hours']} | 剩余课时: {remaining}")
                if remaining == 0:
                    lines.append("      >>> ⚠️  该课程课时已全部用完，请及时联系学员续费！")
                elif remaining <= urgent:
                    lines.append(f"      >>> ⚠️  课时即将用完，仅剩 {remaining} 次，请及时联系学员续费！")
                elif remaining <= warn:
                    lines.append(f"      >>> 提醒：剩余课时较少（{remaining} 次），建议关注续费意向")
            else:
                lines.append(f"      有效期: {c['start_date']} ~ {c['end_date']}")
    else:
        lines.append("暂无课程信息")

    logs = student.get('deduction_logs', [])
    if logs:
        lines.append("")
        lines.append("课时扣除记录:")
        for log in logs:
            lines.append(f"  [{log['created_at'][:16]}] 扣除 {log['deducted_hours']} 课时 | 扣除前: {log['remaining_before']} | 扣除后: {log['remaining_after']}")
            if log['notes']:
                lines.append(f"      备注: {log['notes']}")
    else:
        lines.append("暂无扣除记录")

    return lines


def send_student_record(student_data, subject_prefix=""):
    body = format_student_data(student_data)
    name = student_data.get('name', '学员') if isinstance(student_data, dict) else '全部学员'
    subject = f"{subject_prefix}瑜伽学员记录 - {name} - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    return send_email(subject, body)
