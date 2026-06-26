"""
Outbox 消息队列模块 - 生成和管理待发送消息
"""
import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


class OutboxManager:
    """消息队列管理器"""
    
    def __init__(self, base_path: Path, test_mode: bool = False):
        """
        初始化消息队列管理器
        
        Args:
            base_path: smart-email-data 根目录
            test_mode: 是否为测试模式
        """
        self.test_mode = test_mode
        if test_mode:
            self.outbox_base = base_path / "tmp" / "outbox"
        else:
            self.outbox_base = base_path / "outbox"
        
        self.pending_dir = self.outbox_base / "pending"
        self.sent_dir = self.outbox_base / "sent"
        
        # 确保目录存在
        self.pending_dir.mkdir(parents=True, exist_ok=True)
        self.sent_dir.mkdir(parents=True, exist_ok=True)
    
    def _generate_message_id(self) -> str:
        """生成消息ID"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        short_uuid = uuid.uuid4().hex[:8]
        return f"{timestamp}_{short_uuid}"
    
    def _get_message_path(self, message_id: str) -> Path:
        """获取消息文件路径"""
        return self.pending_dir / f"{message_id}.json"
    
    def write_message(
        self,
        msg_type: str,  # urgent | digest | error
        priority: str,  # high | normal | low
        title: str,
        body: str,
        images: List[str] = None,
        attachments: List[str] = None,
        context: Dict[str, Any] = None
    ) -> str:
        """
        写入消息到待发送队列
        
        Args:
            msg_type: 消息类型 (urgent/digest/error)
            priority: 优先级 (high/normal/low)
            title: 消息标题
            body: 消息正文 (Markdown格式)
            images: 图片路径列表 (相对于 smart-email-data/)
            attachments: 附件路径列表 (相对于 smart-email-data/)
            context: 额外上下文信息
            
        Returns:
            message_id: 消息ID
        """
        message_id = self._generate_message_id()
        
        # 测试模式添加前缀
        if self.test_mode:
            title = f"🧪 [测试] {title}"
        
        message = {
            "id": message_id,
            "created_at": datetime.now().isoformat(),
            "source": "smart-email",
            "type": msg_type,
            "priority": priority,
            "test_mode": self.test_mode,
            "content": {
                "title": title,
                "body": body,
                "images": images or [],
                "attachments": attachments or []
            },
            "context": context or {}
        }
        
        message_path = self._get_message_path(message_id)
        with open(message_path, 'w', encoding='utf-8') as f:
            json.dump(message, f, indent=2, ensure_ascii=False)
        
        return message_id
    
    def _extract_email_id(self, local_path: str) -> str:
        """从本地路径提取邮件ID（目录名）"""
        if not local_path:
            return ""
        # 移除末尾的斜杠，然后取最后一部分
        return local_path.rstrip('/').split('/')[-1]

    def write_urgent_message(
        self,
        email_data: Dict[str, Any],
        reason: str,
        summary: str,
        images: List[str] = None,
        attachments: List[str] = None
    ) -> str:
        """
        写入紧急邮件消息

        Args:
            email_data: 邮件数据
            reason: 紧急原因
            summary: 邮件摘要
            images: 图片路径列表
            attachments: 附件路径列表

        Returns:
            message_id: 消息ID
        """
        provider_map = {
            'qq': 'QQ邮箱',
            '126': '126邮箱',
            '163': '163邮箱',
            'outlook': 'Outlook'
        }
        provider_name = provider_map.get(email_data.get('provider'), email_data.get('provider', '未知'))

        # 格式化时间
        received_at = email_data.get('received_at', '')
        try:
            dt = datetime.fromisoformat(received_at)
            time_str = dt.strftime('%m-%d %H:%M')
        except (ValueError, TypeError):
            time_str = received_at

        # 提取邮件ID
        email_id = self._extract_email_id(email_data.get('local_path', ''))

        # 提取发件人邮箱地址
        sender = email_data.get('sender', '未知')
        # 尝试从 "Name <email@domain>" 格式中提取邮箱
        email_addr = sender
        if '<' in sender and '>' in sender:
            start = sender.find('<') + 1
            end = sender.find('>')
            email_addr = sender[start:end]

        # 简化标题，移除方括号中的ID
        title = f"🚨 紧急邮件"
        
        # 美观化方案C：时间提前，发件人单独一行，内容缩进
        body = f"""📧 [{time_str}] {email_addr}
📌 主题：{email_data.get('subject', '无主题')}

⚠️ 紧急原因：{reason}

📝 摘要：{summary}

<!-- email_id: {email_id} -->

---
_Provided by smart-email skill_"""

        context = {
            "related_emails": [email_id],
            "mail_count": 1,
            "email_data": {
                "subject": email_data.get('subject'),
                "sender": email_data.get('sender'),
                "received_at": received_at,
                "local_path": email_data.get('local_path'),
                "email_id": email_id
            }
        }

        return self.write_message(
            msg_type="urgent",
            priority="high",
            title=title,
            body=body,
            images=images,
            attachments=attachments,
            context=context
        )
    
    def write_digest_message(
        self,
        important_emails: List[Dict[str, Any]],
        normal_emails: List[Dict[str, Any]],
        date_str: str
    ) -> str:
        """
        写入每日汇总消息

        Args:
            important_emails: 重要邮件列表
            normal_emails: 一般邮件列表
            date_str: 日期字符串

        Returns:
            message_id: 消息ID
        """
        # 统一日期格式为 YYYY-MM-DD
        # date_str 应该是 YYYY-MM-DD 格式
        title = f"📧 邮件摘要 ({date_str})"

        body_lines = []
        email_id_list = []

        # 始终显示重要邮件分类（即使为0封）
        body_lines.append(f"📌 重要 ({len(important_emails)}封)")
        if important_emails:
            for email in important_emails:
                summary = email.get('summary', email.get('subject', '无主题'))
                email_id = self._extract_email_id(email.get('local_path', ''))
                sender = email.get('sender', '')
                
                # 提取发件人邮箱地址
                sender_display = sender
                if '<' in sender and '>' in sender:
                    start = sender.find('<') + 1
                    end = sender.find('>')
                    sender_display = sender[start:end]
                
                # 如果没有发件人信息，使用 provider 名称
                if not sender or sender in ['未知', '']:
                    sender_display = email.get('provider', '邮箱') + '邮箱'
                
                # 格式化时间
                received_at = email.get('received_at', '')
                try:
                    dt = datetime.fromisoformat(received_at)
                    time_str = dt.strftime('%m-%d %H:%M')
                except (ValueError, TypeError):
                    time_str = ''
                
                # 美观化方案C：📧 [时间] 发件人，内容缩进
                body_lines.append(f"📧 [{time_str}] {sender_display}")
                body_lines.append(f"   {summary}")
                email_id_list.append(email_id)
        body_lines.append("")

        # 一般邮件
        body_lines.append(f"📋 一般 ({len(normal_emails)}封)")
        if normal_emails:
            for email in normal_emails:
                summary = email.get('summary', email.get('subject', '无主题'))
                email_id = self._extract_email_id(email.get('local_path', ''))
                sender = email.get('sender', '')
                
                # 提取发件人邮箱地址
                sender_display = sender
                if '<' in sender and '>' in sender:
                    start = sender.find('<') + 1
                    end = sender.find('>')
                    sender_display = sender[start:end]
                
                # 如果没有发件人信息，使用 provider 名称
                if not sender or sender in ['未知', '']:
                    sender_display = email.get('provider', '邮箱') + '邮箱'
                
                # 格式化时间
                received_at = email.get('received_at', '')
                try:
                    dt = datetime.fromisoformat(received_at)
                    time_str = dt.strftime('%m-%d %H:%M')
                except (ValueError, TypeError):
                    time_str = ''
                
                # 美观化方案C：📧 [时间] 发件人，内容缩进
                body_lines.append(f"📧 [{time_str}] {sender_display}")
                body_lines.append(f"   {summary}")
                email_id_list.append(email_id)
            body_lines.append("")

        total_count = len(important_emails) + len(normal_emails)
        body_lines.append(f"📎 共{total_count}封新邮件")
        body_lines.append("")
        
        # 邮件ID列表改为注释形式
        if email_id_list:
            body_lines.append(f"<!-- email_ids: {', '.join(email_id_list)} -->")

        body_lines.append("")
        body_lines.append("---")
        body_lines.append("_Provided by smart-email skill_")

        body = "\n".join(body_lines)

        # 构建邮件ID列表，包含更多信息
        related_emails = []
        for email in important_emails + normal_emails:
            email_id = self._extract_email_id(email.get('local_path', ''))
            related_emails.append({
                "email_id": email_id,
                "subject": email.get('subject'),
                "sender": email.get('sender'),
                "local_path": email.get('local_path')
            })

        context = {
            "related_emails": [e.get('local_path', '').split('/')[-1] for e in important_emails + normal_emails],
            "mail_count": total_count,
            "important_count": len(important_emails),
            "normal_count": len(normal_emails),
            "email_details": related_emails
        }

        return self.write_message(
            msg_type="digest",
            priority="normal",
            title=title,
            body=body,
            context=context
        )
    
    def write_error_message(
        self,
        errors: List[Dict[str, str]],
        error_type: str = "connection"
    ) -> Optional[str]:
        """
        写入错误消息（聚合多个错误）
        
        Args:
            errors: 错误列表，每项包含 provider 和 error 字段
            error_type: 错误类型 (connection/save/database/analyze_failed)
            
        Returns:
            message_id: 消息ID，如果错误列表为空则返回 None
        """
        if not errors:
            return None
        
        provider_map = {
            'qq': 'QQ邮箱',
            '126': '126邮箱',
            '163': '163邮箱',
            'outlook': 'Outlook'
        }
        
        title = "⚠️ 邮件检查异常"
        
        if len(errors) == 1:
            # 单条错误
            error = errors[0]
            provider_name = provider_map.get(error.get('provider'), error.get('provider', '未知'))
            body = f"{provider_name}: {error.get('error', '未知错误')}\n\n---\n_Provided by smart-email skill_"
        else:
            # 多条错误聚合
            body_lines = ["以下邮箱连接失败："]
            for error in errors:
                provider_name = provider_map.get(error.get('provider'), error.get('provider', '未知'))
                body_lines.append(f"• {provider_name}: {error.get('error', '未知错误')}")
            body_lines.append("")
            body_lines.append("---")
            body_lines.append("_Provided by smart-email skill_")
            body = "\n".join(body_lines)
        
        context = {
            "errors": errors,
            "error_type": error_type,
            "error_count": len(errors)
        }
        
        return self.write_message(
            msg_type="error",
            priority="high" if error_type in ['database', 'save', 'analyze_failed'] else "normal",
            title=title,
            body=body,
            context=context
        )
    
    def write_analysis_error_message(
        self,
        email_id: str,
        local_path: str,
        sender: str,
        subject: str,
        retry_count: int,
        last_error: str
    ) -> str:
        """
        写入邮件分析失败错误消息（v2 新方法）

        Args:
            email_id: 邮件ID
            local_path: 邮件本地路径
            sender: 发件人
            subject: 邮件主题
            retry_count: 已重试次数
            last_error: 最后一次错误信息

        Returns:
            message_id: 消息ID
        """
        # 提取发件人邮箱地址
        sender_display = sender
        if '<' in sender and '>' in sender:
            start = sender.find('<') + 1
            end = sender.find('>')
            sender_display = sender[start:end]
        
        title = "⚠️ 邮件分析异常"
        
        body = f"""📧 邮件分析失败
邮件ID: {email_id}
发件人: {sender_display}
主题: {subject}

重试次数: {retry_count}/3

错误原因: {last_error}

---
_Provided by smart-email skill_"""

        context = {
            "email_id": email_id,
            "local_path": local_path,
            "retry_count": retry_count,
            "last_error": last_error
        }

        return self.write_message(
            msg_type="error",
            priority="high",
            title=title,
            body=body,
            context=context
        )
    
    def list_pending_messages(self) -> List[Dict[str, Any]]:
        """获取所有待发送消息列表"""
        messages = []
        for msg_file in sorted(self.pending_dir.glob("*.json")):
            try:
                with open(msg_file, 'r', encoding='utf-8') as f:
                    msg = json.load(f)
                    messages.append(msg)
            except Exception:
                continue
        return messages
    
    def get_message(self, message_id: str) -> Optional[Dict[str, Any]]:
        """获取指定消息内容"""
        message_path = self._get_message_path(message_id)
        if not message_path.exists():
            return None
        
        try:
            with open(message_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None
    
    def mark_as_sent(self, message_id: str) -> bool:
        """
        将消息标记为已发送（移动到 sent 目录）
        
        Args:
            message_id: 消息ID
            
        Returns:
            bool: 是否成功
        """
        pending_path = self._get_message_path(message_id)
        if not pending_path.exists():
            return False
        
        # 创建日期子目录
        today_str = datetime.now().strftime('%Y-%m-%d')
        today_sent_dir = self.sent_dir / today_str
        today_sent_dir.mkdir(parents=True, exist_ok=True)
        
        # 使用原子操作移动文件
        sent_path = today_sent_dir / f"{message_id}.json"
        try:
            # 优先使用 os.rename（原子操作）
            os.rename(pending_path, sent_path)
            return True
        except OSError:
            # 跨文件系统时回退到 Path.rename
            try:
                pending_path.rename(sent_path)
                return True
            except Exception:
                return False
    
    def delete_message(self, message_id: str) -> bool:
        """删除消息"""
        message_path = self._get_message_path(message_id)
        if message_path.exists():
            try:
                message_path.unlink()
                return True
            except Exception:
                return False
        return False
    
    def get_stats(self) -> Dict[str, int]:
        """获取队列统计信息"""
        pending_count = len(list(self.pending_dir.glob("*.json")))
        
        # 计算已发送消息数（所有日期子目录）
        sent_count = 0
        if self.sent_dir.exists():
            for date_dir in self.sent_dir.iterdir():
                if date_dir.is_dir():
                    sent_count += len(list(date_dir.glob("*.json")))
        
        return {
            "pending": pending_count,
            "sent": sent_count
        }
