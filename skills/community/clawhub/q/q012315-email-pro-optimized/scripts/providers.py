#!/usr/bin/env python3
"""
邮件提供商处理 - 支持 QQ、Gmail、Outlook
"""

import imaplib
import smtplib
import ssl
import json
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.parser import BytesParser
from email import encoders
from pathlib import Path
import time

OAUTH_TOKENS_FILE = Path.home() / '.openclaw' / 'credentials' / 'oauth_tokens.json'

class EmailProvider:
    """邮件提供商基类"""
    
    def __init__(self, config):
        self.config = config
        self.provider_type = config.get('provider', 'imap')
    
    def connect_imap(self):
        raise NotImplementedError
    
    def connect_smtp(self):
        raise NotImplementedError
    
    def check_emails(self, limit=10, unread_only=False, mailbox='INBOX'):
        raise NotImplementedError
    
    def send_email(self, to, subject, body, html=False, attachments=None):
        raise NotImplementedError

class QQEmailProvider(EmailProvider):
    """QQ 邮箱提供商"""
    
    def __init__(self, config):
        super().__init__(config)
        self.imap = None
        self.smtp = None
    
    def connect_imap(self):
        if self.imap is None:
            context = ssl.create_default_context()
            self.imap = imaplib.IMAP4_SSL(
                self.config['imap_server'],
                self.config['imap_port'],
                ssl_context=context
            )
            self.imap.login(self.config['email'], self.config['auth_code'])
        return self.imap
    
    def connect_smtp(self):
        if self.smtp is None:
            self.smtp = smtplib.SMTP(
                self.config['smtp_server'],
                self.config['smtp_port']
            )
            self.smtp.starttls()
            self.smtp.login(self.config['email'], self.config['auth_code'])
        return self.smtp
    
    def disconnect_imap(self):
        if self.imap:
            try:
                self.imap.close()
                self.imap.logout()
            except:
                pass
            self.imap = None
    
    def disconnect_smtp(self):
        if self.smtp:
            try:
                self.smtp.quit()
            except:
                pass
            self.smtp = None
    
    def check_emails(self, limit=10, unread_only=False, mailbox='INBOX'):
        try:
            imap = self.connect_imap()
            imap.select(mailbox)
            
            criteria = 'UNSEEN' if unread_only else 'ALL'
            status, messages = imap.search(None, criteria)
            
            if not messages[0]:
                return []
            
            msg_ids = messages[0].split()[-limit:]
            
            if msg_ids:
                status, msg_data_list = imap.fetch(b','.join(msg_ids), '(RFC822)')
            else:
                return []
            
            results = []
            i = 0
            while i < len(msg_data_list):
                if isinstance(msg_data_list[i], tuple):
                    try:
                        msg = BytesParser().parsebytes(msg_data_list[i][1])
                        results.append({
                            'from': msg.get('From', 'Unknown'),
                            'subject': msg.get('Subject', '(no subject)'),
                            'date': msg.get('Date', ''),
                            'uid': msg_data_list[i][0].decode() if isinstance(msg_data_list[i][0], bytes) else str(msg_data_list[i][0]),
                            'snippet': self._get_snippet(msg),
                        })
                    except:
                        pass
                i += 1
            
            return results
        
        except Exception as e:
            print(f"❌ 检查邮件失败: {e}")
            return []
    
    def send_email(self, to, subject, body, html=False, attachments=None):
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.config['email']
            msg['To'] = to
            msg['Subject'] = subject
            
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            if attachments:
                for file_path in attachments:
                    self._attach_file(msg, file_path)
            
            smtp = self.connect_smtp()
            smtp.send_message(msg)
            
            return True
        
        except Exception as e:
            print(f"❌ 发送邮件失败: {e}")
            return False
    
    def _get_snippet(self, msg):
        body = self._get_body(msg)
        return body[:200] if body else '(no content)'
    
    def _get_body(self, msg):
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    payload = part.get_payload(decode=True)
                    if payload:
                        return payload.decode('utf-8', errors='ignore')
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                return payload.decode('utf-8', errors='ignore')
        return ''
    
    def _attach_file(self, msg, file_path):
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        with open(file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={file_path.name}')
        msg.attach(part)

class GmailProvider(EmailProvider):
    """Gmail 提供商（OAuth）"""
    
    def __init__(self, config):
        super().__init__(config)
        self.access_token = None
        self.refresh_token = None
        self._load_oauth_token()
    
    def _load_oauth_token(self):
        account_name = self.config.get('account_name', 'gmail')
        if OAUTH_TOKENS_FILE.exists():
            with open(OAUTH_TOKENS_FILE, 'r') as f:
                tokens = json.load(f)
                if account_name in tokens:
                    token_data = tokens[account_name]
                    self.access_token = token_data.get('access_token')
                    self.refresh_token = token_data.get('refresh_token')
    
    def _refresh_access_token(self):
        """刷新访问令牌"""
        if not self.refresh_token:
            raise ValueError("没有刷新令牌，请先授权")
        
        client_id = self.config.get('client_id')
        client_secret = self.config.get('client_secret')
        
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token'
        }
        
        response = requests.post('https://oauth2.googleapis.com/token', data=data)
        token_data = response.json()
        
        if 'access_token' in token_data:
            self.access_token = token_data['access_token']
            return True
        
        return False
    
    def check_emails(self, limit=10, unread_only=False, mailbox='INBOX'):
        """使用 Gmail API 检查邮件"""
        try:
            if not self.access_token:
                self._refresh_access_token()
            
            headers = {'Authorization': f'Bearer {self.access_token}'}
            
            # 构建查询
            query = 'is:unread' if unread_only else ''
            params = {
                'q': query,
                'maxResults': limit,
                'fields': 'messages(id,threadId)'
            }
            
            response = requests.get(
                'https://www.googleapis.com/gmail/v1/users/me/messages',
                headers=headers,
                params=params
            )
            
            if response.status_code != 200:
                print(f"❌ Gmail API 错误: {response.text}")
                return []
            
            messages = response.json().get('messages', [])
            results = []
            
            for msg in messages:
                msg_id = msg['id']
                msg_response = requests.get(
                    f'https://www.googleapis.com/gmail/v1/users/me/messages/{msg_id}',
                    headers=headers,
                    params={'format': 'metadata', 'metadataHeaders': ['From', 'Subject', 'Date']}
                )
                
                if msg_response.status_code == 200:
                    msg_data = msg_response.json()
                    headers_list = msg_data.get('payload', {}).get('headers', [])
                    
                    header_dict = {h['name']: h['value'] for h in headers_list}
                    
                    results.append({
                        'from': header_dict.get('From', 'Unknown'),
                        'subject': header_dict.get('Subject', '(no subject)'),
                        'date': header_dict.get('Date', ''),
                        'uid': msg_id,
                        'snippet': msg_data.get('sni', ''),
                    })
            
            return results
        
        except Exception as e:
            print(f"❌ 检查 Gmail 邮件失败: {e}")
            return []
    
    def send_email(self, to, subject, body, html=False, attachments=None):
        """使用 Gmail API 发送邮件"""
        try:
            if not self.access_token:
                self._refresh_access_token()
            
            headers = {'Authorization': f'Bearer {self.access_token}'}
            
            msg = MIMEMultipart('alternative')
            msg['To'] = to
            msg['Subject'] = subject
            
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            if attachments:
                for file_path in attachments:
                    self._attach_file(msg, file_path)
            
            # 编码消息
            import base64
            raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()
            
            data = {'raw': raw_message}
            
            response = requests.post(
                'https://www.googleapis.com/gmail/v1/users/me/messages/send',
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                return True
            else:
                print(f"❌ Gmail 发送失败: {response.text}")
                return False
        
        except Exception as e:
            print(f"❌ 发送 Gmail 邮件失败: {e}")
            return False
    
    def _attach_file(self, msg, file_path):
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        with open(file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={file_path.name}')
        msg.attach(part)

class OutlookProvider(EmailProvider):
    """Outlook 提供商（OAuth）"""
    
    def __init__(self, config):
        super().__init__(config)
        self.access_token = None
        self.refresh_token = None
        self._load_oauth_token()
    
    def _load_oauth_token(self):
        account_name = self.config.get('account_name', 'outlook')
        if OAUTH_TOKENS_FILE.exists():
            with open(OAUTH_TOKENS_FILE, 'r') as f:
                tokens = json.load(f)
                if account_name in tokens:
                    token_data = tokens[account_name]
                    self.access_token = token_data.get('access_token')
                    self.refresh_token = token_data.get('refresh_token')
    
    def _refresh_access_token(self):
        """刷新访问令牌"""
        if not self.refresh_token:
            raise ValueError("没有刷新令牌，请先授权")
        
        client_id = self.config.get('client_id')
        client_secret = self.config.get('client_secret')
        tenant_id = self.config.get('tenant_id')
        
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token',
            'scope': 'https://graph.microsoft.com/.default'
        }
        
        response = requests.post(
            f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token',
            data=data
        )
        token_data = response.json()
        
        if 'access_token' in token_data:
            self.access_token = token_data['access_token']
            return True
        
        return False
    
    def check_emails(self, limit=10, unread_only=False, mailbox='INBOX'):
        """使用 Microsoft Graph API 检查邮件"""
        try:
            if not self.access_token:
                self._refresh_access_token()
            
            headers = {'Authorization': f'Bearer {self.access_token}'}
            
            # 构建查询
            filter_str = "isRead eq false" if unread_only else ""
            params = {
                '$top': limit,
                '$select': 'from,subject,receivedDateTime,bodyPreview,id'
            }
            
            if filter_str:
                params['$filter'] = filter_str
            
            response = requests.get(
                f'https://graph.microsoft.com/v1.0/me/mailFolders/{mailbox}/messages',
                headers=headers,
                params=params
            )
            
            if response.status_code != 200:
                print(f"❌ Outlook API 错误: {response.text}")
                return []
            
            messages = response.json().get('value', [])
            results = []
            
            for msg in messages:
                from_addr = msg.get('from', {}).get('emailAddress', {})
                results.append({
                    'from': f"{from_addr.get('name', '')} <{from_addr.get('address', '')}>",
                    'subject': msg.get('subject', '(no subject)'),
                    'date': msg.get('receivedDateTime', ''),
                    'uid': msg.get('id'),
                    'snippet': msg.get('bodyPreview', ''),
                })
            
            return results
        
        except Exception as e:
            print(f"❌ 检查 Outlook 邮件失败: {e}")
            return []
    
    def send_email(self, to, subject, body, html=False, attachments=None):
        """使用 Microsoft Graph API 发送邮件"""
        try:
            if not self.access_token:
                self._refresh_access_token()
            
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            message = {
                'subject': subject,
                'body': {
                    'contentType': 'HTML' if html else 'text',
                    'content': body
                },
                'toRecipients': [
                    {
                        'emailAddress': {
                            'address': to
                        }
                    }
                ]
            }
            
            data = {'message': message}
            
            response = requests.post(
                'https://graph.microsoft.com/v1.0/me/sendMail',
                headers=headers,
                json=data
            )
            
            if response.status_code == 202:
                return True
            else:
                print(f"❌ Outlook 发送失败: {response.text}")
                return False
        
        except Exception as e:
            print(f"❌ 发送 Outlook 邮件失败: {e}")
            return False

def get_provider(config):
    """根据配置获取邮件提供商"""
    provider_type = config.get('provider', 'imap')
    
    if provider_type == 'imap':
        return QQEmailProvider(config)
    elif provider_type == 'gmail':
        return GmailProvider(config)
    elif provider_type == 'outlook':
        return OutlookProvider(config)
    else:
        raise ValueError(f"未知的提供商类型: {provider_type}")
