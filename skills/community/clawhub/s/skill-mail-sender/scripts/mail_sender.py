#!/usr/bin/env python3
"""
邮件发送工具 - 支持 HTML 和 Markdown 格式

功能：
- 发送 HTML 格式邮件
- 发送 Markdown 格式邮件（自动转换为 HTML）
- 支持多个收件人（逗号分隔）
- 支持环境变量和配置文件
- 完善的错误处理和日志记录

配置优先级：参数 > 环境变量 > 配置文件 > 默认值
配置文件路径：~/.openclaw/skills/mail-sender/config.json
"""

import smtplib
import json
import os
import re
import logging
from typing import List, Union, Optional, Dict, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import uuid

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============== 默认配置 ==============
DEFAULTS = {
    'smtp_server': 'smtp.163.com',
    'smtp_port': 465,
    'sender_name': 'Wezin'
}

CONFIG_FILE_NAME = 'config.json'
SKILL_NAME = 'mail-sender'


class ConfigError(Exception):
    """配置错误异常"""
    pass


class MailConfig:
    """邮件配置类 - 简单易用的配置管理"""
    
    # 类级别缓存
    _cached_config: Optional['MailConfig'] = None
    
    def __init__(
        self,
        sender_email: Optional[str] = None,
        sender_password: Optional[str] = None,
        smtp_server: Optional[str] = None,
        smtp_port: Optional[int] = None,
        default_receivers: Optional[List[str]] = None,
        sender_name: Optional[str] = None,
        config_path: Optional[str] = None,
        use_cache: bool = True
    ):
        """
        初始化邮件配置
        
        Args:
            sender_email: 发件人邮箱
            sender_password: 发件人密码/授权码
            smtp_server: SMTP 服务器
            smtp_port: SMTP 端口
            default_receivers: 默认收件人列表
            sender_name: 发件人名称
            config_path: 自定义配置文件路径
            use_cache: 是否使用缓存的配置（默认 True）
        """
        # 如果使用缓存且缓存存在，直接返回缓存
        if use_cache and MailConfig._cached_config and not any([
            sender_email, sender_password, smtp_server, smtp_port,
            default_receivers, sender_name, config_path
        ]):
            # 复制缓存的配置
            self._copy_from(MailConfig._cached_config)
            return
        
        # 1. 从环境变量加载
        self._load_from_env()
        
        # 2. 从配置文件加载（会填充尚未设置的值）
        self._load_from_config_file(config_path)
        
        # 3. 用参数覆盖（最高优先级）
        if sender_email:
            self.sender_email = sender_email
        if sender_password:
            self._sender_password = sender_password
        if smtp_server:
            self.smtp_server = smtp_server
        if smtp_port:
            self.smtp_port = smtp_port
        if default_receivers:
            self.default_receivers = default_receivers
        if sender_name:
            self.sender_name = sender_name
        
        # 4. 验证配置
        self._validate()
        
        # 5. 缓存配置
        if use_cache:
            MailConfig._cached_config = self
    
    def _copy_from(self, other: 'MailConfig'):
        """从另一个配置对象复制"""
        self.sender_email = other.sender_email
        self._sender_password = other._sender_password
        self.smtp_server = other.smtp_server
        self.smtp_port = other.smtp_port
        self.default_receivers = other.default_receivers.copy() if other.default_receivers else []
        self.sender_name = other.sender_name
    
    def _load_from_env(self):
        """从环境变量加载配置"""
        self.sender_email = os.getenv('MAIL_SENDER_EMAIL')
        self._sender_password = os.getenv('MAIL_SENDER_PASSWORD')
        self.smtp_server = os.getenv('MAIL_SMTP_SERVER', DEFAULTS['smtp_server'])
        self.sender_name = os.getenv('MAIL_SENDER_NAME', DEFAULTS['sender_name'])
        
        # 安全转换端口
        port_str = os.getenv('MAIL_SMTP_PORT', str(DEFAULTS['smtp_port']))
        try:
            self.smtp_port = int(port_str)
        except ValueError:
            logger.warning(f"MAIL_SMTP_PORT 值无效 '{port_str}'，使用默认值 {DEFAULTS['smtp_port']}")
            self.smtp_port = DEFAULTS['smtp_port']
        
        # 解析默认收件人
        env_receivers = os.getenv('MAIL_DEFAULT_RECEIVERS', '')
        self.default_receivers = [e.strip() for e in env_receivers.split(',') if e.strip()]
    
    def _load_from_config_file(self, custom_path: Optional[str] = None):
        """
        从配置文件加载配置
        
        查找优先级：
        1. custom_path（自定义路径）
        2. MAIL_CONFIG_PATH 环境变量
        3. ~/.openclaw/skills/mail-sender/config.json（推荐）
        4. {skill_dir}/config.json
        5. ./.mail-sender-config.json
        """
        config_paths = self._get_config_paths(custom_path)
        
        for path in config_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    # 只填充尚未设置的值
                    if not self.sender_email:
                        self.sender_email = config.get('sender_email')
                    if not self._sender_password:
                        self._sender_password = config.get('sender_password')
                    if self.smtp_server == DEFAULTS['smtp_server']:
                        self.smtp_server = config.get('smtp_server', DEFAULTS['smtp_server'])
                    if self.smtp_port == DEFAULTS['smtp_port']:
                        self.smtp_port = config.get('smtp_port', DEFAULTS['smtp_port'])
                    if not self.default_receivers:
                        self.default_receivers = config.get('default_receivers', [])
                    if not self.sender_name:
                        self.sender_name = config.get('sender_name', DEFAULTS['sender_name'])
                    
                    logger.info(f"配置加载成功: {path}")
                    return
                    
                except json.JSONDecodeError as e:
                    logger.warning(f"配置文件格式错误 ({path}): {e}")
                except Exception as e:
                    logger.warning(f"加载配置文件失败 ({path}): {e}")
    
    def _get_config_paths(self, custom_path: Optional[str] = None) -> List[str]:
        """获取配置文件路径列表（按优先级排序）"""
        paths = []
        home_dir = os.path.expanduser('~')
        
        # 1. 自定义路径
        if custom_path:
            paths.append(custom_path)
        
        # 2. 环境变量指定路径
        env_path = os.getenv('MAIL_CONFIG_PATH')
        if env_path:
            paths.append(env_path)
        
        # 3. 技能安装目录下的配置（优先）
        paths.append(os.path.join(home_dir, '.openclaw', 'skills', SKILL_NAME, CONFIG_FILE_NAME))
        
        # 4. 独立技能配置目录（不受技能卸载影响，备选）
        paths.append(os.path.join(home_dir, '.openclaw', 'skills', 'config', SKILL_NAME, CONFIG_FILE_NAME))
        
        # 5. Skill 脚本目录
        skill_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(skill_dir)
        if os.path.basename(parent_dir) == 'scripts':
            # 如果当前在 scripts 目录，配置文件在上一级
            paths.append(os.path.join(os.path.dirname(parent_dir), CONFIG_FILE_NAME))
        else:
            paths.append(os.path.join(skill_dir, CONFIG_FILE_NAME))
        
        # 6. 当前工作目录
        paths.append('.mail-sender-config.json')
        
        return paths
    
    def _validate(self):
        """验证配置的有效性"""
        # 检查必需配置
        if not self.sender_email:
            raise ConfigError(
                "缺少发件人邮箱！请通过以下方式之一配置：\n"
                "1. 环境变量：MAIL_SENDER_EMAIL\n"
                "2. 配置文件：~/.openclaw/skills/mail-sender/config.json\n"
                "3. 构造函数参数：sender_email"
            )
        
        if not self._sender_password:
            raise ConfigError(
                "缺少发件人密码/授权码！请通过以下方式之一配置：\n"
                "1. 环境变量：MAIL_SENDER_PASSWORD\n"
                "2. 配置文件：~/.openclaw/skills/mail-sender/config.json\n"
                "3. 构造函数参数：sender_password"
            )
        
        # 验证邮箱格式
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.sender_email):
            raise ConfigError(f"无效的发件人邮箱格式: {self.sender_email}")
        
        # 验证端口范围
        if not (1 <= self.smtp_port <= 65535):
            raise ConfigError(f"无效的 SMTP 端口: {self.smtp_port}")
        
        # 验证默认收件人邮箱格式
        for receiver in self.default_receivers:
            if not re.match(email_pattern, receiver):
                logger.warning(f"默认收件人邮箱格式可能无效: {receiver}")
    
    @property
    def sender_password(self) -> str:
        """获取密码（保护敏感信息）"""
        return self._sender_password
    
    def to_dict(self, include_password: bool = False) -> Dict[str, Any]:
        """转换为字典"""
        result = {
            'sender_email': self.sender_email,
            'smtp_server': self.smtp_server,
            'smtp_port': self.smtp_port,
            'default_receivers': self.default_receivers,
            'sender_name': self.sender_name
        }
        if include_password:
            result['sender_password'] = '***'
        return result
    
    def __repr__(self) -> str:
        return f"MailConfig(email={self.sender_email}, server={self.smtp_server}:{self.smtp_port})"
    
    @classmethod
    def clear_cache(cls):
        """清除配置缓存"""
        cls._cached_config = None


class MailSender:
    """邮件发送器"""
    
    def __init__(self, config: Optional[MailConfig] = None):
        """
        初始化邮件发送器
        
        Args:
            config: 邮件配置对象，如果为 None 则自动加载
        """
        self.config = config or MailConfig()
        logger.info(f"邮件发送器初始化: {self.config}")
    
    def send_mail(
        self,
        subject: str,
        content: str,
        receivers: Optional[Union[str, List[str]]] = None,
        content_type: str = 'html'
    ) -> dict:
        """
        发送邮件
        
        Args:
            subject: 邮件主题
            content: 邮件内容
            receivers: 收件人邮箱（字符串或列表）
            content_type: 内容类型 ('html' 或 'plain')
        
        Returns:
            dict: {'success': bool, 'message': str, 'failed_receivers': list}
        """
        # 解析收件人
        receiver_list = self._parse_receivers(receivers)
        if not receiver_list:
            return {
                'success': False,
                'message': '没有有效的收件人',
                'failed_receivers': []
            }
        
        logger.info(f"发送邮件到: {receiver_list}")
        
        # 创建邮件
        message = MIMEMultipart('alternative')
        message.attach(MIMEText(content, content_type, 'utf-8'))
        
        # 设置邮件头
        message['From'] = Header(self.config.sender_name, 'utf-8')
        message['To'] = ",".join(receiver_list)
        message['Subject'] = Header(subject, 'utf-8')
        message['X-Priority'] = '3'
        message['X-Mailer'] = 'Wezin'
        message['Message-ID'] = f"<{uuid.uuid4()}@wezin.ai>"
        
        # 发送
        try:
            with smtplib.SMTP_SSL(self.config.smtp_server, self.config.smtp_port) as smtp:
                smtp.login(self.config.sender_email, self.config.sender_password)
                logger.info("SMTP 登录成功")
                
                failed = smtp.sendmail(
                    self.config.sender_email,
                    receiver_list,
                    message.as_string()
                )
                
                if failed:
                    logger.warning(f"部分收件人发送失败: {failed}")
                    return {
                        'success': True,
                        'message': f'邮件发送成功，但部分收件人失败: {failed}',
                        'failed_receivers': list(failed.keys())
                    }
                else:
                    logger.info("邮件发送成功")
                    return {
                        'success': True,
                        'message': '邮件发送成功！',
                        'failed_receivers': []
                    }
                    
        except smtplib.SMTPRecipientsRefused as e:
            error_msg = f"所有收件人被拒绝: {e}"
            logger.error(error_msg)
            return {'success': False, 'message': error_msg, 'failed_receivers': receiver_list}
            
        except smtplib.SMTPSenderRefused as e:
            error_msg = f"发件人被拒绝: {e}"
            logger.error(error_msg)
            return {'success': False, 'message': error_msg, 'failed_receivers': []}
            
        except smtplib.SMTPAuthenticationError as e:
            error_msg = f"认证失败，请检查邮箱和授权码: {e}"
            logger.error(error_msg)
            return {'success': False, 'message': error_msg, 'failed_receivers': []}
            
        except smtplib.SMTPException as e:
            error_msg = f"SMTP 错误: {e}"
            logger.error(error_msg)
            return {'success': False, 'message': error_msg, 'failed_receivers': []}
            
        except Exception as e:
            error_msg = f"发送异常: {e}"
            logger.error(error_msg)
            return {'success': False, 'message': error_msg, 'failed_receivers': []}
    
    def send_markdown(
        self,
        subject: str,
        markdown_content: str,
        receivers: Optional[Union[str, List[str]]] = None
    ) -> dict:
        """
        发送 Markdown 格式邮件（自动转换为 HTML）
        
        Args:
            subject: 邮件主题
            markdown_content: Markdown 内容
            receivers: 收件人邮箱
        
        Returns:
            dict: {'success': bool, 'message': str, 'failed_receivers': list}
        """
        try:
            import markdown
            html_content = markdown.markdown(
                markdown_content,
                extensions=['tables', 'fenced_code', 'codehilite']
            )
            logger.info("Markdown 转换成功")
            return self.send_mail(subject, html_content, receivers, content_type='html')
        except ImportError:
            error_msg = "缺少 markdown 库，请安装: pip install markdown"
            logger.error(error_msg)
            return {'success': False, 'message': error_msg, 'failed_receivers': []}
        except Exception as e:
            error_msg = f"Markdown 转换失败: {e}"
            logger.error(error_msg)
            return {'success': False, 'message': error_msg, 'failed_receivers': []}
    
    def _parse_receivers(self, receivers: Optional[Union[str, List[str]]]) -> List[str]:
        """解析收件人列表"""
        if receivers is None:
            return self.config.default_receivers
        
        if isinstance(receivers, str):
            return [e.strip() for e in receivers.split(',') if e.strip()]
        
        if isinstance(receivers, list):
            return [e.strip() for e in receivers if e.strip()]
        
        logger.warning(f"无效的 receivers 类型: {type(receivers)}")
        return self.config.default_receivers


# ============== 便捷函数 ==============

def send_mail(
    subject: str,
    content: str,
    receivers: Optional[Union[str, List[str]]] = None,
    content_type: str = 'html',
    config: Optional[MailConfig] = None
) -> dict:
    """
    快速发送邮件
    
    Args:
        subject: 邮件主题
        content: 邮件内容
        receivers: 收件人邮箱
        content_type: 内容类型 ('html' 或 'plain')
        config: 邮件配置（可选）
    
    Returns:
        dict: {'success': bool, 'message': str, 'failed_receivers': list}
    """
    sender = MailSender(config)
    return sender.send_mail(subject, content, receivers, content_type)


def send_markdown(
    subject: str,
    markdown_content: str,
    receivers: Optional[Union[str, List[str]]] = None,
    config: Optional[MailConfig] = None
) -> dict:
    """
    快速发送 Markdown 邮件
    
    Args:
        subject: 邮件主题
        markdown_content: Markdown 内容
        receivers: 收件人邮箱
        config: 邮件配置（可选）
    
    Returns:
        dict: {'success': bool, 'message': str, 'failed_receivers': list}
    """
    sender = MailSender(config)
    return sender.send_markdown(subject, markdown_content, receivers)


# ============== 测试代码 ==============

if __name__ == '__main__':
    """测试代码"""
    print("=" * 50)
    print("Mail Sender 测试")
    print("=" * 50)
    
    try:
        # 测试配置加载
        config = MailConfig()
        print(f"\n配置加载成功: {config}")
        
        # 测试发送（需要实际配置）
        # result = send_mail(
        #     subject='测试邮件',
        #     content='<h1>测试</h1><p>这是一封测试邮件</p>',
        #     receivers='test@example.com'
        # )
        # print(f"\n发送结果: {result}")
        
    except ConfigError as e:
        print(f"\n配置错误: {e}")
    except Exception as e:
        print(f"\n异常: {e}")
