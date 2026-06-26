#!/usr/bin/env python3
"""
邮件发送器 - 小龙虾工作流 v0.4.0 组件

功能：
1. 发送任务进度报告邮件
2. 支持HTML和纯文本格式
3. 错误处理和安全重试
4. 模拟发送模式（开发环境）
"""

import os
import json
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailSender:
    """邮件发送器"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化邮件发送器
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.smtp_connection = None
        logger.info("邮件发送器初始化完成")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            'enabled': False,
            'sender': 'workflow@example.com',
            'recipient': '',
            'subject_prefix': '[小龙虾工作流] ',
            'smtp_server': 'smtp.example.com',
            'smtp_port': 587,
            'use_tls': True,
            'username': '',
            'password': '',
            'simulate': True,  # 模拟发送，不实际连接SMTP
            'log_dir': 'logs',
            'max_retries': 3,
            'retry_delay_seconds': 5,
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                
                # 检查email配置
                if 'email' in user_config:
                    email_config = user_config['email']
                    for key, value in email_config.items():
                        if key in default_config:
                            default_config[key] = value
            except Exception as e:
                logger.warning(f"加载邮件配置失败，使用默认配置: {e}")
        
        return default_config
    
    def _connect_smtp(self) -> bool:
        """连接SMTP服务器"""
        if self.config['simulate']:
            logger.info("模拟模式，跳过SMTP连接")
            return True
        
        if not self.config['enabled']:
            logger.warning("邮件功能未启用")
            return False
        
        try:
            logger.info(f"连接SMTP服务器: {self.config['smtp_server']}:{self.config['smtp_port']}")
            
            if self.config['use_tls']:
                self.smtp_connection = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
                self.smtp_connection.starttls()
            else:
                self.smtp_connection = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            
            # 登录
            if self.config['username'] and self.config['password']:
                self.smtp_connection.login(self.config['username'], self.config['password'])
            
            logger.info("SMTP连接成功")
            return True
        except Exception as e:
            logger.error(f"SMTP连接失败: {e}")
            self.smtp_connection = None
            return False
    
    def _disconnect_smtp(self):
        """断开SMTP连接"""
        if self.smtp_connection:
            try:
                self.smtp_connection.quit()
                logger.debug("SMTP连接已关闭")
            except Exception as e:
                logger.warning(f"关闭SMTP连接失败: {e}")
            finally:
                self.smtp_connection = None
    
    def _create_message(self, subject: str, body_text: str, body_html: Optional[str] = None) -> MIMEMultipart:
        """创建邮件消息"""
        # 创建消息容器
        msg = MIMEMultipart('alternative')
        msg['From'] = self.config['sender']
        msg['To'] = self.config['recipient']
        msg['Subject'] = Header(self.config['subject_prefix'] + subject, 'utf-8')
        
        # 添加纯文本版本
        part1 = MIMEText(body_text, 'plain', 'utf-8')
        msg.attach(part1)
        
        # 添加HTML版本（如果提供）
        if body_html:
            part2 = MIMEText(body_html, 'html', 'utf-8')
            msg.attach(part2)
        
        return msg
    
    def _log_email(self, subject: str, body_text: str, body_html: Optional[str] = None):
        """记录邮件到日志文件（用于模拟模式）"""
        log_dir = Path(self.config['log_dir'])
        log_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f"email_{timestamp}.log"
        
        log_content = f"""邮件记录 ({timestamp})
主题: {subject}
收件人: {self.config['recipient']}
发件人: {self.config['sender']}
启用状态: {self.config['enabled']}
模拟模式: {self.config['simulate']}

正文:
{body_text}
"""
        
        if body_html:
            log_content += f"\nHTML版本:\n{body_html}"
        
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(log_content)
            logger.info(f"邮件已记录到: {log_file}")
        except Exception as e:
            logger.error(f"记录邮件失败: {e}")
    
    def send_email(self, subject: str, body_text: str, body_html: Optional[str] = None) -> bool:
        """
        发送邮件
        
        Args:
            subject: 邮件主题
            body_text: 纯文本正文
            body_html: HTML正文（可选）
            
        Returns:
            bool: 发送是否成功
        """
        if not self.config['enabled']:
            logger.info("邮件功能未启用，跳过发送")
            return False
        
        # 创建消息
        msg = self._create_message(subject, body_text, body_html)
        
        # 模拟模式
        if self.config['simulate']:
            logger.info(f"模拟发送邮件: {subject}")
            self._log_email(subject, body_text, body_html)
            return True
        
        # 实际发送
        retries = 0
        max_retries = self.config['max_retries']
        
        while retries <= max_retries:
            try:
                # 连接SMTP（如果需要）
                if not self.smtp_connection:
                    if not self._connect_smtp():
                        retries += 1
                        continue
                
                # 发送邮件
                self.smtp_connection.send_message(msg)
                logger.info(f"邮件发送成功: {subject}")
                
                # 记录
                self._log_email(subject, body_text, body_html)
                
                # 断开连接
                self._disconnect_smtp()
                
                return True
                
            except Exception as e:
                logger.error(f"邮件发送失败 (尝试 {retries+1}/{max_retries+1}): {e}")
                retries += 1
                
                if retries <= max_retries:
                    import time
                    time.sleep(self.config['retry_delay_seconds'])
                    
                    # 重新连接
                    self._disconnect_smtp()
                else:
                    logger.error(f"邮件发送失败，已达到最大重试次数")
                    self._disconnect_smtp()
                    return False
        
        return False
    
    def send_task_summary(self, task_info: Dict[str, Any], project_dir: Path) -> bool:
        """发送任务概要邮件"""
        if not self.config['enabled']:
            return False
        
        # 构建邮件内容
        task_id = task_info.get('task_id', '未知')
        task_description = task_info.get('task_description', '')
        complexity = task_info.get('complexity_score', 0)
        estimated_hours = task_info.get('estimated_hours', 0)
        
        subject = f"任务已创建: {task_id}"
        
        # 纯文本版本
        body_text = f"""小龙虾工作流 - 任务创建通知

任务ID: {task_id}
任务描述: {task_description}
复杂度: {complexity}/10
预计耗时: {estimated_hours} 小时
项目目录: {project_dir}
创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

您可以进入项目目录查看详细计划:
cd {project_dir}

下一步建议:
1. 查看任务概要: cat task_summary.md
2. 查看顶层方案: cat top_level_plan.md
3. 开始执行: python run_workflow.py --execute "任务描述"

---
小龙虾分层任务工作流 v0.4.0
"""
        
        # HTML版本
        body_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .header h1 {{ color: #2c3e50; margin: 0; }}
        .content {{ background-color: white; padding: 20px; border-radius: 5px; border: 1px solid #ddd; }}
        .info {{ margin-bottom: 15px; }}
        .info-label {{ font-weight: bold; color: #2c3e50; }}
        .next-steps {{ background-color: #e8f4fd; padding: 15px; border-radius: 5px; margin-top: 20px; }}
        .footer {{ margin-top: 20px; font-size: 12px; color: #777; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🦞 小龙虾工作流 - 任务创建通知</h1>
        </div>
        
        <div class="content">
            <div class="info">
                <span class="info-label">任务ID:</span> {task_id}
            </div>
            <div class="info">
                <span class="info-label">任务描述:</span> {task_description}
            </div>
            <div class="info">
                <span class="info-label">复杂度:</span> {complexity}/10
            </div>
            <div class="info">
                <span class="info-label">预计耗时:</span> {estimated_hours} 小时
            </div>
            <div class="info">
                <span class="info-label">项目目录:</span> {project_dir}
            </div>
            <div class="info">
                <span class="info-label">创建时间:</span> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
            
            <div class="next-steps">
                <h3>下一步建议</h3>
                <ol>
                    <li>查看任务概要: <code>cat task_summary.md</code></li>
                    <li>查看顶层方案: <code>cat top_level_plan.md</code></li>
                    <li>开始执行: <code>python run_workflow.py --execute "任务描述"</code></li>
                </ol>
            </div>
        </div>
        
        <div class="footer">
            小龙虾分层任务工作流 v0.4.0<br>
            此邮件由系统自动发送，请勿直接回复
        </div>
    </div>
</body>
</html>"""
        
        return self.send_email(subject, body_text, body_html)
    
    def send_execution_report(self, task_id: str, project_dir: Path, 
                            execution_stats: Dict[str, Any]) -> bool:
        """发送执行报告邮件"""
        if not self.config['enabled']:
            return False
        
        subject = f"执行报告: {task_id}"
        
        # 构建统计信息
        total_steps = execution_stats.get('total_steps', 0)
        completed_steps = execution_stats.get('completed_steps', 0)
        failed_steps = execution_stats.get('failed_steps', 0)
        success_rate = execution_stats.get('success_rate', 0)
        total_hours = execution_stats.get('total_hours', 0)
        
        # 纯文本版本
        body_text = f"""小龙虾工作流 - 执行报告

任务ID: {task_id}
执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

执行统计:
- 总步骤数: {total_steps}
- 完成步骤: {completed_steps}
- 失败步骤: {failed_steps}
- 成功率: {success_rate:.1%}
- 总耗时: {total_hours:.2f} 小时

项目目录: {project_dir}

详细报告:
{project_dir}/execution_report.md

---
小龙虾分层任务工作流 v0.4.0
"""
        
        # HTML版本
        body_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .header h1 {{ color: #2c3e50; margin: 0; }}
        .stats {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 20px; }}
        .stat-card {{ background-color: #f1f8ff; padding: 15px; border-radius: 5px; text-align: center; }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: #2c3e50; }}
        .stat-label {{ font-size: 14px; color: #666; margin-top: 5px; }}
        .success {{ color: #28a745; }}
        .failure {{ color: #dc3545; }}
        .footer {{ margin-top: 20px; font-size: 12px; color: #777; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 小龙虾工作流 - 执行报告</h1>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{total_steps}</div>
                <div class="stat-label">总步骤数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value success">{completed_steps}</div>
                <div class="stat-label">完成步骤</div>
            </div>
            <div class="stat-card">
                <div class="stat-value failure">{failed_steps}</div>
                <div class="stat-label">失败步骤</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{success_rate:.1%}</div>
                <div class="stat-label">成功率</div>
            </div>
        </div>
        
        <div style="background-color: white; padding: 20px; border-radius: 5px; border: 1px solid #ddd; margin-bottom: 20px;">
            <div style="margin-bottom: 10px;">
                <strong>任务ID:</strong> {task_id}
            </div>
            <div style="margin-bottom: 10px;">
                <strong>执行时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
            <div style="margin-bottom: 10px;">
                <strong>总耗时:</strong> {total_hours:.2f} 小时
            </div>
            <div style="margin-bottom: 10px;">
                <strong>项目目录:</strong> {project_dir}
            </div>
            <div style="margin-bottom: 10px;">
                <strong>详细报告:</strong> {project_dir}/execution_report.md
            </div>
        </div>
        
        <div class="footer">
            小龙虾分层任务工作流 v0.4.0<br>
            此邮件由系统自动发送，请勿直接回复
        </div>
    </div>
</body>
</html>"""
        
        return self.send_email(subject, body_text, body_html)


def test_email_sender():
    """测试邮件发送器"""
    print("🧪 测试邮件发送器...")
    
    import tempfile
    from pathlib import Path
    
    # 创建临时配置文件
    with tempfile.TemporaryDirectory(prefix='xlx_email_') as tmpdir:
        config_file = Path(tmpdir) / "test_config.json"
        config_data = {
            'email': {
                'enabled': True,
                'simulate': True,
                'sender': 'test@example.com',
                'recipient': 'recipient@example.com',
                'subject_prefix': '[测试] ',
                'log_dir': str(Path(tmpdir) / "logs")
            }
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2)
        
        # 测试邮件发送器
        sender = EmailSender(str(config_file))
        
        # 测试发送任务概要
        task_info = {
            'task_id': 'test_task_001',
            'task_description': '测试任务描述',
            'complexity_score': 6,
            'estimated_hours': 8.5
        }
        
        project_dir = Path(tmpdir) / "test_project"
        project_dir.mkdir()
        
        success = sender.send_task_summary(task_info, project_dir)
        
        if success:
            print("✅ 任务概要邮件发送测试成功")
        else:
            print("❌ 任务概要邮件发送测试失败")
        
        # 测试发送执行报告
        execution_stats = {
            'total_steps': 25,
            'completed_steps': 23,
            'failed_steps': 2,
            'success_rate': 0.92,
            'total_hours': 12.5
        }
        
        success = sender.send_execution_report('test_task_001', project_dir, execution_stats)
        
        if success:
            print("✅ 执行报告邮件发送测试成功")
        else:
            print("❌ 执行报告邮件发送测试失败")
        
        # 检查日志文件
        log_dir = Path(tmpdir) / "logs"
        if log_dir.exists():
            log_files = list(log_dir.glob("*.log"))
            print(f"📧 邮件日志文件: {len(log_files)} 个")
            for log_file in log_files[:2]:
                print(f"   - {log_file.name}")
        else:
            print("⚠️  日志目录未创建")
    
    print("\n✅ 邮件发送器测试完成")
    return True


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_email_sender()
    else:
        print("用法:")
        print("  python email_sender.py test")
        print("\n注意: 完整使用需要与其他模块集成")