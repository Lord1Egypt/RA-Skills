# -*- coding: utf-8 -*-
"""通用 SMTP 邮件发送脚本
首次使用前需配置邮箱地址和密码（通过环境变量或注册表）：
  Windows:  setx SMTP_MAIL_ADDR "your_email@domain.com"
            setx SMTP_MAIL_PWD "your_password"
  或脚本自动引导设置。

用法:
  python send_email.py --to "a@b.com,c@d.com" --subject "标题" --body "纯文本正文"
  python send_email.py --to "a@b.com" --subject "标题" --html body.html --attach report.csv
  python send_email.py --to "a@b.com" --subject "标题" --body "正文" --html-body "<b>HTML正文</b>"
"""
import argparse, os, sys, smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# ===== SMTP 服务器自动匹配 =====
SMTP_MAP = {
    'chinatelecom.cn': ('smtp.chinatelecom.cn', 465, 'ssl'),
    '189.cn':          ('smtp.189.cn', 465, 'ssl'),
    '139.com':         ('smtp.139.com', 465, 'ssl'),
    '163.com':         ('smtp.163.com', 465, 'ssl'),
    '126.com':         ('smtp.126.com', 465, 'ssl'),
    'qq.com':          ('smtp.qq.com', 465, 'ssl'),
    'foxmail.com':     ('smtp.qq.com', 465, 'ssl'),
    'sina.com':        ('smtp.sina.com', 465, 'ssl'),
    'sina.cn':         ('smtp.sina.cn', 465, 'ssl'),
    'sohu.com':        ('smtp.sohu.com', 465, 'ssl'),
    'aliyun.com':      ('smtp.qiye.aliyun.com', 465, 'ssl'),
    'outlook.com':     ('smtp-mail.outlook.com', 587, 'starttls'),
    'hotmail.com':     ('smtp-mail.outlook.com', 587, 'starttls'),
    'gmail.com':       ('smtp.gmail.com', 465, 'ssl'),
    'yeah.net':        ('smtp.yeah.net', 465, 'ssl'),
    '263.net':         ('smtp.263.net', 465, 'ssl'),
    'wo.cn':           ('smtp.wo.cn', 465, 'ssl'),
}


def detect_smtp(email_addr):
    """根据邮箱地址后缀自动匹配SMTP服务器"""
    domain = email_addr.split('@')[-1].lower()
    return SMTP_MAP.get(domain, (None, None, None))


def get_credential():
    """读取已配置的邮箱凭据（环境变量 → Windows注册表）
    优先读取 SMTP_MAIL_ADDR/SMTP_MAIL_PWD，
    回退到旧版 CT_MAIL_ADDR/CT_MAIL_PWD。
    """
    addr = os.environ.get('SMTP_MAIL_ADDR', '') or os.environ.get('CT_MAIL_ADDR', '')
    pwd = os.environ.get('SMTP_MAIL_PWD', '') or os.environ.get('CT_MAIL_PWD', '')

    if not addr or not pwd:
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment') as k:
                if not addr:
                    try:
                        addr = winreg.QueryValueEx(k, 'SMTP_MAIL_ADDR')[0]
                    except FileNotFoundError:
                        pass
                if not addr:
                    try:
                        addr = winreg.QueryValueEx(k, 'CT_MAIL_ADDR')[0]
                    except FileNotFoundError:
                        pass
                if not pwd:
                    try:
                        pwd = winreg.QueryValueEx(k, 'SMTP_MAIL_PWD')[0]
                    except FileNotFoundError:
                        pass
                if not pwd:
                    try:
                        pwd = winreg.QueryValueEx(k, 'CT_MAIL_PWD')[0]
                    except FileNotFoundError:
                        pass
        except Exception:
            pass

    return addr, pwd


def setup_credential(addr, pwd):
    """将邮箱凭据写入Windows注册表（用户级，持久化）"""
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_SET_VALUE) as k:
            winreg.SetValueEx(k, 'SMTP_MAIL_ADDR', 0, winreg.REG_SZ, addr)
            winreg.SetValueEx(k, 'SMTP_MAIL_PWD', 0, winreg.REG_SZ, pwd)
        # 同时写入当前进程环境变量
        os.environ['SMTP_MAIL_ADDR'] = addr
        os.environ['SMTP_MAIL_PWD'] = pwd
        print(f'凭据已保存: {addr}')
        return True
    except Exception as e:
        print(f'保存凭据失败: {e}')
        return False


def send_email(recipients, subject, body=None, html_body=None, html_file=None,
               attachments=None, smtp_server=None, smtp_port=None, smtp_mode='ssl',
               sender=None, sender_pwd=None, sender_name=None):
    """发送邮件

    Args:
        recipients: 收件人列表 (str 或 list)
        subject: 邮件主题
        body: 纯文本正文
        html_body: HTML正文字符串
        html_file: HTML文件路径（读取为HTML正文）
        attachments: 附件路径列表
        smtp_server: SMTP服务器地址（不传则自动检测）
        smtp_port: SMTP端口
        smtp_mode: 'ssl' 或 'starttls'
        sender: 发件人邮箱（不传则使用已配置的凭据）
        sender_pwd: 发件人密码（不传则使用已配置的凭据）
        sender_name: 发件人显示名称
    """
    # 统一收件人为列表
    if isinstance(recipients, str):
        recipients = [r.strip() for r in recipients.split(',') if r.strip()]

    # 获取凭据
    if not sender or not sender_pwd:
        cred_addr, cred_pwd = get_credential()
        sender = sender or cred_addr
        sender_pwd = sender_pwd or cred_pwd

    if not sender or not sender_pwd:
        print('ERROR: 邮箱凭据未配置！')
        print('请运行: python send_email.py --setup')
        print('或手动设置环境变量 SMTP_MAIL_ADDR 和 SMTP_MAIL_PWD')
        return False

    # 自动检测 SMTP 服务器
    if not smtp_server:
        srv, port, mode = detect_smtp(sender)
        if srv:
            smtp_server = srv
            smtp_port = smtp_port or port
            smtp_mode = mode
        else:
            print(f'ERROR: 无法自动识别 {sender} 的SMTP服务器')
            print('请通过 --smtp-server 参数指定')
            return False

    smtp_port = smtp_port or 465
    smtp_mode = smtp_mode or 'ssl'

    # 构建 HTML 正文
    if html_file:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
    else:
        html_content = html_body

    # 发件人显示名称
    from_header = formataddr((sender_name or '', sender)) if sender_name else sender

    success = 0
    for recipient in recipients:
        try:
            msg = MIMEMultipart()
            msg['From'] = from_header
            msg['To'] = recipient
            msg['Subject'] = subject

            # 正文
            if html_content:
                msg.attach(MIMEText(html_content, 'html', 'utf-8'))
            elif body:
                msg.attach(MIMEText(body, 'plain', 'utf-8'))
            else:
                msg.attach(MIMEText('', 'plain', 'utf-8'))

            # 附件
            if attachments:
                if isinstance(attachments, str):
                    attachments = [attachments]
                for att_path in attachments:
                    if not os.path.exists(att_path):
                        print(f'  警告: 附件不存在，跳过: {att_path}')
                        continue
                    with open(att_path, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                    encoders.encode_base64(part)
                    att_name = os.path.basename(att_path)
                    part.add_header('Content-Disposition', 'attachment',
                                    filename=('utf-8', '', att_name))
                    msg.attach(part)

            # 发送
            if smtp_mode == 'starttls':
                server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
                server.ehlo()
                server.starttls(context=ssl.create_default_context())
                server.ehlo()
            else:
                server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=30)

            server.login(sender, sender_pwd)
            server.sendmail(sender, recipient, msg.as_string())
            server.quit()
            print(f'发送成功 -> {recipient}')
            success += 1
        except Exception as e:
            print(f'发送失败 -> {recipient}: {e}')

    return success == len(recipients)


def interactive_setup():
    """交互式配置邮箱凭据"""
    print('=' * 50)
    print('  SMTP 邮箱凭据配置')
    print('=' * 50)
    print()

    # 检查是否已配置
    existing_addr, existing_pwd = get_credential()
    if existing_addr:
        print(f'当前已配置邮箱: {existing_addr}')
        confirm = input('是否重新配置？(y/N): ').strip().lower()
        if confirm != 'y':
            print('配置保持不变。')
            return

    addr = input('请输入邮箱地址: ').strip()
    if not addr or '@' not in addr:
        print('邮箱地址格式不正确，配置取消。')
        return

    srv, port, mode = detect_smtp(addr)
    if srv:
        print(f'  自动识别 SMTP: {srv}:{port} ({mode})')
    else:
        srv = input('  无法自动识别，请输入SMTP服务器地址: ').strip()
        if not srv:
            print('SMTP服务器不能为空，配置取消。')
            return

    import getpass
    pwd = getpass.getpass('请输入邮箱密码/授权码（输入不可见）: ')
    if not pwd:
        print('密码不能为空，配置取消。')
        return

    if setup_credential(addr, pwd):
        # 如果SMTP服务器不是自动识别的，也保存
        if not detect_smtp(addr)[0]:
            try:
                import winreg
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_SET_VALUE) as k:
                    winreg.SetValueEx(k, 'SMTP_MAIL_SERVER', 0, winreg.REG_SZ, srv)
                os.environ['SMTP_MAIL_SERVER'] = srv
            except Exception:
                pass
        print()
        print('配置完成！现在可以使用 send_email.py 发送邮件了。')
    else:
        print('配置失败，请检查权限后重试。')


def main():
    parser = argparse.ArgumentParser(description='通用 SMTP 邮件发送工具')
    parser.add_argument('--setup', action='store_true', help='交互式配置邮箱凭据')
    parser.add_argument('--to', type=str, help='收件人（多个用逗号分隔）')
    parser.add_argument('--subject', type=str, default='', help='邮件主题')
    parser.add_argument('--body', type=str, help='纯文本正文')
    parser.add_argument('--html-body', type=str, help='HTML正文（字符串）')
    parser.add_argument('--html-file', type=str, help='HTML正文文件路径')
    parser.add_argument('--attach', action='append', help='附件路径（可多次指定）')
    parser.add_argument('--smtp-server', type=str, help='SMTP服务器地址（默认自动检测）')
    parser.add_argument('--smtp-port', type=int, help='SMTP端口')
    parser.add_argument('--smtp-mode', type=str, choices=['ssl', 'starttls'], help='加密模式')
    parser.add_argument('--sender', type=str, help='发件人邮箱（默认使用已配置的凭据）')
    parser.add_argument('--sender-pwd', type=str, help='发件人密码（默认使用已配置的凭据）')
    parser.add_argument('--sender-name', type=str, help='发件人显示名称')
    parser.add_argument('--check', action='store_true', help='检查当前配置状态')

    args = parser.parse_args()

    if args.setup:
        interactive_setup()
        return

    if args.check:
        addr, pwd = get_credential()
        if addr and pwd:
            srv, port, mode = detect_smtp(addr)
            print(f'已配置邮箱: {addr}')
            print(f'密码: {"*" * len(pwd)}')
            if srv:
                print(f'SMTP服务器: {srv}:{port} ({mode}) [自动检测]')
            else:
                custom_srv = os.environ.get('SMTP_MAIL_SERVER', '')
                if custom_srv:
                    print(f'SMTP服务器: {custom_srv} [手动配置]')
                else:
                    print('SMTP服务器: 未配置（需要手动指定）')
        else:
            print('尚未配置邮箱凭据。运行 --setup 进行配置。')
        return

    if not args.to:
        parser.error('--to 是必需的（除非使用 --setup 或 --check）')

    if not args.subject:
        parser.error('--subject 是必需的')

    ok = send_email(
        recipients=args.to,
        subject=args.subject,
        body=args.body,
        html_body=args.html_body,
        html_file=args.html_file,
        attachments=args.attach,
        smtp_server=args.smtp_server,
        smtp_port=args.smtp_port,
        smtp_mode=args.smtp_mode or 'ssl',
        sender=args.sender,
        sender_pwd=args.sender_pwd,
        sender_name=args.sender_name,
    )

    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
