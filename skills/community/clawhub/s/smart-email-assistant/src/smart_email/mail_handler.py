"""
邮件处理模块 - IMAP 收取和解析
"""
import os
import re
import json
import imaplib
import email
from email import policy
from email.parser import BytesParser
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# 尝试导入 imaplib2（支持 IMAP ID 扩展），否则使用标准库
try:
    from imaplib2 import IMAP4_SSL as IMAP4_SSL_CLASS
    from imaplib2 import IMAP4 as IMAP4_CLASS
    HAS_IMAPLIB2 = True
except ImportError:
    from imaplib import IMAP4_SSL as IMAP4_SSL_CLASS
    from imaplib import IMAP4 as IMAP4_CLASS
    HAS_IMAPLIB2 = False

# 注册 IMAP ID 命令（RFC 2971）- 网易/QQ 邮箱需要
# 网易官方文档要求在登录后发送 ID 命令，但某些服务器可能需要在登录前发送
# 因此同时支持 NONAUTH 和 AUTH 状态
if 'ID' not in imaplib.Commands:
    imaplib.Commands['ID'] = ('NONAUTH', 'AUTH')


class EmailClient:
    """IMAP 邮件客户端"""
    
    # IMAP ID 信息（用于网易邮箱等需要身份识别的服务器）
    IMAP_ID_INFO = {
        'name': 'SmartEmail',
        'version': '1.0.0',
        'vendor': 'OpenClaw',
        'support-email': 'support@openclaw.local'
    }
    
    def __init__(self, provider: str, email_account: str, password: str,
                 server: str, port: int = 993, use_ssl: bool = True):
        self.provider = provider
        self.email_account = email_account
        self.password = password
        self.server = server
        self.port = port
        self.use_ssl = use_ssl
        self.conn = None
    
    def connect(self) -> bool:
        """连接 IMAP 服务器"""
        try:
            if self.use_ssl:
                self.conn = IMAP4_SSL_CLASS(self.server, self.port)
            else:
                self.conn = IMAP4_CLASS(self.server, self.port)

            self.conn.login(self.email_account, self.password)

            # 发送 IMAP ID 信息（网易邮箱等需要在登录后发送）
            # 参考网易官方文档: https://mail.163.com/
            self._send_imap_id()

            return True
        except Exception as e:
            print(f"连接 {self.provider} 邮箱失败: {e}")
            return False
    
    def _send_imap_id(self):
        """发送 IMAP ID 信息（RFC 2971）
        
        网易邮箱等服务器要求客户端表明身份，否则会返回：
        "Unsafe Login. Please contact kefu@188.com for help"
        
        参考: https://www.cnblogs.com/dyfblog/p/15546756.html
        """
        try:
            # 将 ID 信息格式化为 IMAP 协议格式: ("name" "value" "name2" "value2" ...)
            id_params = ' '.join([f'"{k}" "{v}"' for k, v in self.IMAP_ID_INFO.items()])
            id_cmd = f'({id_params})'
            
            # 使用 _simple_command 发送 ID 命令（标准 imaplib 兼容方式）
            # 这是网易/QQ 邮箱识别的正确方式
            typ, dat = self.conn._simple_command('ID', id_cmd)
            
            if typ == 'OK':
                print(f"    [IMAP ID] 已发送身份标识")
            else:
                print(f"    [IMAP ID] 服务器返回: {typ} {dat}")
                
        except Exception as e:
            # IMAP ID 发送失败不一定是致命错误，某些服务器可能不支持
            print(f"    [IMAP ID] 发送失败（可能服务器不支持）: {e}")
    
    def disconnect(self):
        """断开连接，close() 出错不阻止 logout()，最后 conn=None"""
        if self.conn:
            try:
                self.conn.close()
            except Exception:
                pass
            try:
                self.conn.logout()
            except Exception:
                pass
            self.conn = None
    
    def fetch_new_emails(self, limit: int = 50) -> List[Dict]:
        """获取新邮件"""
        emails = []
        
        if not self.conn:
            if not self.connect():
                return emails
        
        try:
            # 选择收件箱
            status, _ = self.conn.select('INBOX')
            if status != 'OK':
                print(f"无法选择 {self.provider} 收件箱")
                return emails
            
            # 搜索所有邮件（按日期倒序）
            status, messages = self.conn.search(None, 'ALL')
            if status != 'OK':
                return emails
            
            # 获取最新的 limit 封邮件
            msg_ids = messages[0].split()
            msg_ids = msg_ids[-limit:] if len(msg_ids) > limit else msg_ids
            
            for msg_id in reversed(msg_ids):
                try:
                    email_data = self._fetch_email(msg_id)
                    if email_data:
                        emails.append(email_data)
                except Exception as e:
                    print(f"解析邮件 {msg_id} 失败: {e}")
                    continue
            
        except Exception as e:
            print(f"获取 {self.provider} 邮件失败: {e}")
        
        return emails
    
    def _fetch_email(self, msg_id: bytes) -> Optional[Dict]:
        """获取单封邮件详情"""
        status, msg_data = self.conn.fetch(msg_id, '(RFC822)')
        if status != 'OK':
            return None
        
        raw_email = msg_data[0][1]
        msg = BytesParser(policy=policy.default).parsebytes(raw_email)
        
        # 提取基本信息
        subject = self._decode_header(msg.get('Subject', ''))
        sender = self._decode_header(msg.get('From', ''))
        date_str = msg.get('Date', '')
        message_id = msg.get('Message-ID', '')
        
        # 解析日期
        received_at = self._parse_date(date_str)
        
        # 提取正文
        body_text, body_html = self._extract_body(msg)
        
        # 检查紧急标记
        priority = msg.get('X-Priority', '')
        importance = msg.get('Importance', '')
        priority_header = msg.get('Priority', '')
        
        is_flagged_urgent = any([
            priority in ['1', 'high'],
            importance.lower() == 'high',
            priority_header.lower() == 'high'
        ])
        
        # 提取附件信息
        attachments = self._extract_attachments(msg)
        
        # 注意：不保存 raw_email 完整内容，避免大附件导致内存溢出
        # 邮件正文和附件信息已提取，原始邮件不再保留在内存中
        return {
            'uid': msg_id.decode(),
            'message_id': message_id.strip('<>') if message_id else None,
            'subject': subject,
            'sender': sender,
            'received_at': received_at,
            'date_str': date_str,
            'body_text': body_text,
            'body_html': body_html,
            'is_flagged_urgent': is_flagged_urgent,
            'attachments': attachments,
            'headers': dict(msg.items())
        }
    
    def _decode_header(self, header: str) -> str:
        """解码邮件头"""
        if not header:
            return ''
        
        decoded_parts = email.header.decode_header(header)
        result = []
        
        for part, charset in decoded_parts:
            if isinstance(part, bytes):
                try:
                    result.append(part.decode(charset or 'utf-8', errors='replace'))
                except Exception:
                    result.append(part.decode('utf-8', errors='replace'))
            else:
                result.append(part)
        
        return ''.join(result)
    
    def _parse_date(self, date_str: str) -> str:
        """解析日期为 ISO 格式"""
        try:
            from email.utils import parsedate_to_datetime
            dt = parsedate_to_datetime(date_str)
            return dt.isoformat()
        except Exception:
            return datetime.now().isoformat()
    
    def _extract_body(self, msg) -> Tuple[str, str]:
        """提取邮件正文"""
        text_content = []
        html_content = []
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition', ''))
                
                # 跳过附件
                if 'attachment' in content_disposition:
                    continue
                
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or 'utf-8'
                        content = payload.decode(charset, errors='replace')
                        
                        if content_type == 'text/plain':
                            text_content.append(content)
                        elif content_type == 'text/html':
                            html_content.append(content)
                except Exception:
                    continue
        else:
            try:
                payload = msg.get_payload(decode=True)
                if payload:
                    charset = msg.get_content_charset() or 'utf-8'
                    content = payload.decode(charset, errors='replace')
                    
                    if msg.get_content_type() == 'text/plain':
                        text_content.append(content)
                    elif msg.get_content_type() == 'text/html':
                        html_content.append(content)
            except Exception:
                pass
        
        return '\n'.join(text_content), '\n'.join(html_content)
    
    def _extract_attachments(self, msg, email_dir: Optional[Path] = None) -> List[Dict]:
        """提取附件信息
        
        Args:
            msg: 邮件消息对象
            email_dir: 邮件存储目录，如果提供则直接写入附件文件
        
        Returns:
            附件信息列表，包含 filename, content_type, size, local_path/is_inline 等字段
            - 当 email_dir 不为空时，返回的附件包含 local_path 字段，不含 content 字段
            - 当 email_dir 为空时，返回的附件包含 content 字段（向后兼容）
        """
        attachments = []
        
        if msg.is_multipart():
            for part in msg.walk():
                content_disposition = str(part.get('Content-Disposition', ''))
                content_type = part.get_content_type()
                
                # 处理附件 (Content-Disposition: attachment)
                if 'attachment' in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        filename = self._decode_header(filename)
                        payload = part.get_payload(decode=True) or b''
                        attachment_info = {
                            'filename': filename,
                            'content_type': content_type,
                            'size': len(payload),
                            'is_inline': False
                        }
                        
                        if email_dir:
                            # 直接写入文件
                            attachments_dir = email_dir / 'attachments'
                            attachments_dir.mkdir(exist_ok=True)
                            safe_filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
                            file_path = attachments_dir / safe_filename
                            try:
                                with open(file_path, 'wb') as f:
                                    f.write(payload)
                                attachment_info['local_path'] = str(file_path)
                                print(f"    保存附件: {filename} ({len(payload)} bytes)")
                            except Exception as e:
                                print(f"    保存附件失败 {filename}: {e}")
                        else:
                            # 向后兼容：返回 content
                            attachment_info['content'] = payload
                        
                        attachments.append(attachment_info)
                
                # 处理内嵌图片 (Content-Disposition: inline 或没有 disposition 的图片)
                elif content_type.startswith('image/') and 'attachment' not in content_disposition:
                    # 尝试获取内嵌图片的文件名
                    filename = part.get_filename()
                    if not filename:
                        # 生成默认文件名
                        ext = content_type.split('/')[-1] if '/' in content_type else 'png'
                        content_id = part.get('Content-ID', '').strip('<>')
                        if content_id:
                            filename = f"inline_{content_id}.{ext}"
                        else:
                            filename = f"inline_image_{len(attachments)}.{ext}"
                    else:
                        filename = self._decode_header(filename)
                    
                    payload = part.get_payload(decode=True) or b''
                    attachment_info = {
                        'filename': filename,
                        'content_type': content_type,
                        'size': len(payload),
                        'is_inline': True,
                        'content_id': part.get('Content-ID', '').strip('<>')
                    }
                    
                    if email_dir:
                        # 直接写入文件
                        attachments_dir = email_dir / 'attachments'
                        attachments_dir.mkdir(exist_ok=True)
                        safe_filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
                        file_path = attachments_dir / safe_filename
                        try:
                            with open(file_path, 'wb') as f:
                                f.write(payload)
                            attachment_info['local_path'] = str(file_path)
                            print(f"    保存内嵌图片: {filename} ({len(payload)} bytes)")
                        except Exception as e:
                            print(f"    保存内嵌图片失败 {filename}: {e}")
                    else:
                        # 向后兼容：返回 content
                        attachment_info['content'] = payload
                    
                    attachments.append(attachment_info)
        
        return attachments


class EmailStorage:
    """邮件存储管理"""
    
    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)
    
    def save_email(self, provider: str, email_data: Dict) -> str:
        """保存邮件到本地"""
        # 使用邮件接收日期作为目录名
        received_at = email_data.get('received_at', datetime.now().isoformat())
        try:
            # received_at 是 ISO 格式字符串，如 "2026-03-10T08:30:00+00:00"
            dt = datetime.fromisoformat(received_at.replace('Z', '+00:00'))
            mail_date = dt.strftime('%Y-%m-%d')
        except Exception:
            mail_date = datetime.now().strftime('%Y-%m-%d')  # 兜底
        
        date_dir = self.base_path / mail_date
        date_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成文件名前缀 (简化格式: provider_timestamp)
        # 使用邮件接收时间而非当前时间，避免同一秒内多封邮件相互覆盖
        timestamp = dt.strftime('%Y%m%d_%H%M%S')
        
        folder_name = f"{provider}_{timestamp}"
        email_dir = date_dir / folder_name
        email_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存原始 .eml（如 raw_email 不存在则创建空文件）
        # 注意：raw_email 不再存储在内存中，避免大附件导致内存溢出
        eml_path = email_dir / 'email.eml'
        raw_email = email_data.get('raw_email')
        if raw_email:
            with open(eml_path, 'wb') as f:
                f.write(raw_email)
        else:
            # 创建空的 .eml 文件作为占位（或根据需要从其他来源重建）
            eml_path.touch()
        
        # 保存 Markdown
        md_path = email_dir / 'email.md'
        self._save_markdown(md_path, email_data)
        
        # 保存附件
        attachments_dir = email_dir / 'attachments'
        attachments_dir.mkdir(exist_ok=True)
        saved_attachments = []
        
        for attachment in email_data.get('attachments', []):
            filename = attachment['filename']
            
            # 如果附件已有 local_path，说明已在提取时写入文件
            if 'local_path' in attachment:
                saved_attachments.append({
                    'filename': filename,
                    'local_path': attachment['local_path'],
                    'content_type': attachment.get('content_type', 'application/octet-stream'),
                    'size': attachment.get('size', 0),
                    'is_inline': attachment.get('is_inline', False)
                })
            else:
                # 向后兼容：从 content 字段写入文件
                safe_filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
                file_path = attachments_dir / safe_filename
                
                try:
                    with open(file_path, 'wb') as f:
                        f.write(attachment.get('content', b''))
                    saved_attachments.append({
                        'filename': filename,
                        'local_path': str(file_path),
                        'content_type': attachment.get('content_type', 'application/octet-stream'),
                        'size': attachment.get('size', 0),
                        'is_inline': attachment.get('is_inline', False)
                    })
                    print(f"    保存附件: {filename} ({attachment.get('size', 0)} bytes)")
                except Exception as e:
                    print(f"    保存附件失败 {filename}: {e}")
        
        # 更新 email_data 中的附件信息为保存后的路径
        email_data['saved_attachments'] = saved_attachments

        # 保存附件信息到 JSON 文件（供多模态分析使用）
        attachments_json_path = email_dir / 'attachments.json'
        try:
            with open(attachments_json_path, 'w', encoding='utf-8') as f:
                json.dump(saved_attachments, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"    保存附件信息失败: {e}")

        # 清理内存：删除附件的 content 字段以释放大附件占用的内存
        for attachment in email_data.get('attachments', []):
            if 'content' in attachment:
                del attachment['content']

        return str(email_dir)
    
    def _save_markdown(self, path: Path, email_data: Dict):
        """保存为 Markdown 格式"""
        subject = email_data.get('subject', '无主题')
        sender = email_data.get('sender', '')
        received_at = email_data.get('received_at', '')
        body_text = email_data.get('body_text', '')
        
        # 构建附件列表
        attachments_section = ""
        saved_attachments = email_data.get('saved_attachments', [])
        
        if saved_attachments:
            attachments_section = "\n\n## 附件\n\n"
            for att in saved_attachments:
                filename = att['filename']
                local_path = att['local_path']
                content_type = att.get('content_type', '')
                size = att.get('size', 0)
                
                # 图片类型显示为图片链接
                if content_type.startswith('image/'):
                    rel_path = Path(local_path).name
                    attachments_section += f"- 📷 `{filename}` ({size} bytes)\n"
                    attachments_section += f"  ![{filename}](./attachments/{rel_path})\n\n"
                else:
                    attachments_section += f"- 📎 `{filename}` ({size} bytes)\n"
                    attachments_section += f"  [下载](./attachments/{Path(local_path).name})\n\n"
        
        md_content = f"""# {subject}

**发件人**: {sender}
**时间**: {received_at}
**Message-ID**: {email_data.get('message_id', 'N/A')}

---

{body_text}
{attachments_section}"""
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(md_content)
