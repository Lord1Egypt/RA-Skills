#!/usr/bin/env python3
"""
邮件汇报系统 - 小龙虾工作流 v0.3.0 辅助组件

功能：
1. 发送任务进度报告邮件
2. 支持HTML和纯文本格式
3. 错误处理和重试机制
4. 邮件模板系统
"""

import os
import json
import smtplib
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, List, Optional
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailReporter:
    """邮件汇报系统"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化邮件汇报系统
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.smtp_client = None
        self.email_history: List[Dict[str, Any]] = []
        logger.info("邮件汇报系统初始化完成")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """加载配置"""
        default_config = {
            'enabled': False,
            'recipient': '',
            'sender': 'workflow@openclaw.ai',
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'use_tls': True,
            'username': '',
            'password': '',
            'default_subject': '小龙虾工作流进度报告',
            'send_delay_seconds': 2,
            'max_retries': 3,
            'retry_delay_seconds': 5,
            'log_emails_to_file': True,
            'log_directory': '/tmp/xlx_email_logs'
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                
                # 深度合并
                if 'email' in user_config:
                    for key, value in user_config['email'].items():
                        default_config[key] = value
            except Exception as e:
                logger.warning(f"加载邮件配置失败，使用默认配置: {e}")
        
        return default_config
    
    def _connect_smtp(self) -> bool:
        """连接SMTP服务器"""
        if not self.config['enabled']:
            logger.warning("邮件功能未启用")
            return False
        
        try:
            logger.info(f"连接SMTP服务器: {self.config['smtp_server']}:{self.config['smtp_port']}")
            self.smtp_client = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            
            if self.config['use_tls']:
                self.smtp_client.starttls()
            
            if self.config['username'] and self.config['password']:
                self.smtp_client.login(self.config['username'], self.config['password'])
            
            logger.info("SMTP连接成功")
            return True
        except Exception as e:
            logger.error(f"SMTP连接失败: {e}")
            self.smtp_client = None
            return False
    
    def _disconnect_smtp(self):
        """断开SMTP连接"""
        if self.smtp_client:
            try:
                self.smtp_client.quit()
                logger.info("SMTP连接已关闭")
            except Exception as e:
                logger.warning(f"关闭SMTP连接时出错: {e}")
            finally:
                self.smtp_client = None
    
    def _log_email_locally(self, recipient: str, subject: str, content_html: str, content_text: str):
        """本地记录邮件（用于调试和备份）"""
        if not self.config['log_emails_to_file']:
            return
        
        try:
            log_dir = Path(self.config['log_directory'])
            log_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_file = log_dir / f"email_{timestamp}.json"
            
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'recipient': recipient,
                'subject': subject,
                'content_html': content_html,
                'content_text': content_text,
                'status': 'logged_locally'
            }
            
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(log_entry, f, ensure_ascii=False, indent=2)
            
            logger.debug(f"邮件已记录到本地: {log_file}")
        except Exception as e:
            logger.warning(f"记录邮件到本地失败: {e}")
    
    def _create_task_progress_email(self, task_id: str, task_summary: Dict[str, Any], 
                                   progress_data: Dict[str, Any]) -> tuple[str, str, str]:
        """创建任务进度邮件"""
        # 收件人
        recipient = self.config['recipient'] or progress_data.get('notification_email', '')
        
        # 主题
        subject = f"任务进度报告: {task_summary.get('task_name', '未命名任务')} [{task_id}]"
        
        # HTML内容
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; border-radius: 8px; margin-bottom: 30px; }}
        .section {{ margin-bottom: 25px; padding: 15px; border-left: 4px solid #4CAF50; background-color: #f9f9f9; }}
        .progress-bar {{ height: 20px; background-color: #e0e0e0; border-radius: 10px; overflow: hidden; margin: 10px 0; }}
        .progress-fill {{ height: 100%; background-color: #4CAF50; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 20px 0; }}
        .stat-box {{ background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: #4CAF50; }}
        .stat-label {{ font-size: 14px; color: #666; margin-top: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #f2f2f2; }}
        .success {{ color: #4CAF50; }}
        .warning {{ color: #FF9800; }}
        .error {{ color: #F44336; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #666; text-align: center; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>小龙虾工作流进度报告</h1>
        <p>任务ID: {task_id} | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="section">
        <h2>任务概览</h2>
        <p><strong>任务名称:</strong> {task_summary.get('task_name', '未命名任务')}</p>
        <p><strong>任务描述:</strong> {task_summary.get('task_description', '无描述')}</p>
        <p><strong>复杂度评分:</strong> {task_summary.get('complexity_score', 0)}/10</p>
        <p><strong>预计总耗时:</strong> {task_summary.get('estimated_hours', 0)} 小时</p>
    </div>
    
    <div class="section">
        <h2>进度统计</h2>
        <div class="stats">
            <div class="stat-box">
                <div class="stat-value">{progress_data.get('completed_steps', 0)}/{progress_data.get('total_steps', 0)}</div>
                <div class="stat-label">已完成步骤</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{progress_data.get('success_rate', 0)}%</div>
                <div class="stat-label">成功率</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{progress_data.get('elapsed_hours', 0):.1f}h</div>
                <div class="stat-label">已用时间</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{progress_data.get('remaining_hours', 0):.1f}h</div>
                <div class="stat-label">剩余时间</div>
            </div>
        </div>
        
        <h3>整体进度</h3>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress_data.get('completion_percentage', 0)}%;"></div>
        </div>
        <p style="text-align: center;">{progress_data.get('completion_percentage', 0)}% 完成</p>
    </div>
    
    <div class="section">
        <h2>阶段进展</h2>
        <table>
            <thead>
                <tr>
                    <th>阶段</th>
                    <th>状态</th>
                    <th>完成率</th>
                    <th>预计剩余</th>
                </tr>
            </thead>
            <tbody>
"""
        
        # 添加阶段行
        for phase in progress_data.get('phases', []):
            status_class = {
                'completed': 'success',
                'in_progress': 'warning',
                'pending': 'error'
            }.get(phase.get('status', 'pending'), '')
            
            html_content += f"""
                <tr>
                    <td>{phase.get('name', '未命名阶段')}</td>
                    <td class="{status_class}">{phase.get('status', 'pending')}</td>
                    <td>{phase.get('completion', 0)}%</td>
                    <td>{phase.get('remaining_hours', 0)} 小时</td>
                </tr>
"""
        
        html_content += """
            </tbody>
        </table>
    </div>
    
    <div class="section">
        <h2>最近活动</h2>
        <ul>
"""
        
        # 添加最近活动
        for activity in progress_data.get('recent_activities', []):
            html_content += f"<li><strong>{activity.get('time', '')}:</strong> {activity.get('description', '')}</li>\n"
        
        html_content += """
        </ul>
    </div>
    
    <div class="section">
        <h2>下一步计划</h2>
        <ul>
"""
        
        # 添加下一步计划
        for plan in progress_data.get('next_steps', []):
            html_content += f"<li>{plan}</li>\n"
        
        html_content += """
        </ul>
    </div>
    
    <div class="footer">
        <p>本邮件由小龙虾分层任务工作流系统自动生成</p>
        <p>系统版本: 0.3.0 | 报告时间: {}</p>
        <p>如需取消订阅或调整报告频率，请更新工作流配置</p>
    </div>
</body>
</html>
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        # 纯文本内容（简化版）
        text_content = f"""
小龙虾工作流进度报告
====================

任务ID: {task_id}
任务名称: {task_summary.get('task_name', '未命名任务')}
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

概览
----
- 复杂度: {task_summary.get('complexity_score', 0)}/10
- 预计总耗时: {task_summary.get('estimated_hours', 0)} 小时

进度统计
--------
- 已完成步骤: {progress_data.get('completed_steps', 0)}/{progress_data.get('total_steps', 0)}
- 成功率: {progress_data.get('success_rate', 0)}%
- 已用时间: {progress_data.get('elapsed_hours', 0):.1f} 小时
- 剩余时间: {progress_data.get('remaining_hours', 0):.1f} 小时
- 完成率: {progress_data.get('completion_percentage', 0)}%

阶段进展
--------
"""
        
        for phase in progress_data.get('phases', []):
            text_content += f"- {phase.get('name', '未命名阶段')}: {phase.get('status', 'pending')} ({phase.get('completion', 0)}%)\n"
        
        text_content += """
最近活动
--------
"""
        
        for activity in progress_data.get('recent_activities', []):
            text_content += f"- {activity.get('time', '')}: {activity.get('description', '')}\n"
        
        text_content += """
下一步计划
--------
"""
        
        for plan in progress_data.get('next_steps', []):
            text_content += f"- {plan}\n"
        
        text_content += f"""
---
本邮件由小龙虾分层任务工作流系统自动生成
系统版本: 0.3.0
"""
        
        return recipient, subject, html_content, text_content
    
    def send_task_progress(self, task_id: str, task_summary: Dict[str, Any], 
                          progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        发送任务进度报告
        
        Args:
            task_id: 任务ID
            task_summary: 任务摘要
            progress_data: 进度数据
            
        Returns:
            Dict[str, Any]: 发送结果
        """
        if not self.config['enabled']:
            logger.warning("邮件功能未启用，跳过发送")
            return {'success': False, 'reason': 'email_disabled'}
        
        result = {
            'success': False,
            'recipient': '',
            'subject': '',
            'sent_at': datetime.now().isoformat(),
            'error': None,
            'retries': 0
        }
        
        # 创建邮件内容
        recipient, subject, html_content, text_content = self._create_task_progress_email(
            task_id, task_summary, progress_data
        )
        
        if not recipient:
            result['error'] = '未指定收件人'
            logger.warning("未指定收件人，跳过发送")
            return result
        
        result['recipient'] = recipient
        result['subject'] = subject
        
        # 记录到本地
        self._log_email_locally(recipient, subject, html_content, text_content)
        
        # 发送邮件（重试机制）
        for attempt in range(self.config['max_retries']):
            try:
                # 连接SMTP
                if not self._connect_smtp():
                    raise ConnectionError("SMTP连接失败")
                
                # 创建邮件消息
                msg = MIMEMultipart('alternative')
                msg['From'] = self.config['sender']
                msg['To'] = recipient
                msg['Subject'] = subject
                
                # 添加纯文本和HTML版本
                part1 = MIMEText(text_content, 'plain', 'utf-8')
                part2 = MIMEText(html_content, 'html', 'utf-8')
                
                msg.attach(part1)
                msg.attach(part2)
                
                # 发送邮件
                self.smtp_client.send_message(msg)
                
                # 记录成功
                result['success'] = True
                result['retries'] = attempt + 1
                logger.info(f"邮件发送成功 (第 {attempt + 1} 次尝试)")
                
                # 添加到历史
                self.email_history.append({
                    'timestamp': result['sent_at'],
                    'recipient': recipient,
                    'subject': subject,
                    'status': 'sent',
                    'retries': attempt + 1
                })
                
                break
                
            except Exception as e:
                logger.warning(f"邮件发送失败 (第 {attempt + 1} 次尝试): {e}")
                result['error'] = str(e)
                
                # 断开连接
                self._disconnect_smtp()
                
                # 如果不是最后一次尝试，等待后重试
                if attempt < self.config['max_retries'] - 1:
                    wait_time = self.config['retry_delay_seconds'] * (attempt + 1)
                    logger.info(f"等待 {wait_time} 秒后重试...")
                    import time
                    time.sleep(wait_time)
        
        # 最终断开连接
        self._disconnect_smtp()
        
        # 记录到历史（即使失败）
        if not result['success']:
            self.email_history.append({
                'timestamp': result['sent_at'],
                'recipient': recipient,
                'subject': subject,
                'status': 'failed',
                'error': result['error'],
                'retries': result['retries']
            })
        
        return result
    
    def send_simple_notification(self, title: str, message: str, 
                                recipient: Optional[str] = None) -> Dict[str, Any]:
        """
        发送简单通知邮件
        
        Args:
            title: 邮件标题
            message: 邮件内容
            recipient: 收件人（可选，使用配置中的默认收件人）
            
        Returns:
            Dict[str, Any]: 发送结果
        """
        if not self.config['enabled']:
            logger.warning("邮件功能未启用，跳过发送")
            return {'success': False, 'reason': 'email_disabled'}
        
        recipient = recipient or self.config['recipient']
        if not recipient:
            logger.warning("未指定收件人，跳过发送")
            return {'success': False, 'reason': 'no_recipient'}
        
        # 创建简单邮件
        msg = MIMEMultipart()
        msg['From'] = self.config['sender']
        msg['To'] = recipient
        msg['Subject'] = f"工作流通知: {title}"
        
        text_content = f"""
工作流通知
==========

标题: {title}

时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

内容:
{message}

---
小龙虾工作流系统自动发送
"""
        
        msg.attach(MIMEText(text_content, 'plain', 'utf-8'))
        
        # 发送邮件
        result = {'success': False}
        
        try:
            if not self._connect_smtp():
                raise ConnectionError("SMTP连接失败")
            
            self.smtp_client.send_message(msg)
            result['success'] = True
            logger.info(f"通知邮件发送成功: {title}")
            
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"通知邮件发送失败: {e}")
        
        finally:
            self._disconnect_smtp()
        
        return result
    
    def get_email_stats(self) -> Dict[str, Any]:
        """获取邮件统计信息"""
        total = len(self.email_history)
        successful = sum(1 for email in self.email_history if email.get('status') == 'sent')
        failed = total - successful
        
        recent_emails = self.email_history[-10:] if self.email_history else []
        
        return {
            'total_emails': total,
            'successful': successful,
            'failed': failed,
            'success_rate': successful / total if total > 0 else 0,
            'recent_emails': recent_emails,
            'config_enabled': self.config['enabled']
        }


def test_email_reporter():
    """测试邮件汇报系统"""
    print("🧪 测试邮件汇报系统...")
    
    import tempfile
    from pathlib import Path
    
    # 创建测试配置
    test_config = {
        'email': {
            'enabled': False,  # 测试中禁用实际发送
            'recipient': 'test@example.com',
            'sender': 'test@openclaw.ai',
            'log_emails_to_file': True,
            'log_directory': '/tmp/xlx_email_test'
        }
    }
    
    with tempfile.TemporaryDirectory(prefix='xlx_email_') as tmpdir:
        config_file = Path(tmpdir) / "test_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(test_config, f, indent=2)
        
        # 初始化汇报系统
        reporter = EmailReporter(str(config_file))
        
        # 测试配置加载
        print(f"✅ 邮件汇报系统初始化完成")
        print(f"   启用状态: {reporter.config['enabled']}")
        print(f"   收件人: {reporter.config['recipient']}")
        
        # 测试任务进度邮件创建
        task_summary = {
            'task_id': 'test_task_001',
            'task_name': '测试电商平台开发',
            'task_description': '开发一个包含商品管理和支付功能的电商平台',
            'complexity_score': 7,
            'estimated_hours': 40
        }
        
        progress_data = {
            'completed_steps': 15,
            'total_steps': 56,
            'success_rate': 93.3,
            'elapsed_hours': 12.5,
            'remaining_hours': 27.5,
            'completion_percentage': 35,
            'phases': [
                {'name': '需求分析', 'status': 'completed', 'completion': 100, 'remaining_hours': 0},
                {'name': '架构设计', 'status': 'completed', 'completion': 100, 'remaining_hours': 0},
                {'name': '核心开发', 'status': 'in_progress', 'completion': 45, 'remaining_hours': 20},
                {'name': '测试部署', 'status': 'pending', 'completion': 0, 'remaining_hours': 7.5}
            ],
            'recent_activities': [
                {'time': '14:30', 'description': '完成用户认证模块'},
                {'time': '15:45', 'description': '开始支付集成开发'},
                {'time': '16:20', 'description': '修复商品搜索bug'}
            ],
            'next_steps': [
                '完成支付网关集成',
                '开发订单管理系统',
                '进行系统性能测试'
            ]
        }
        
        recipient, subject, html, text = reporter._create_task_progress_email(
            'test_task_001', task_summary, progress_data
        )
        
        print(f"✅ 邮件内容创建完成")
        print(f"   收件人: {recipient}")
        print(f"   主题: {subject}")
        print(f"   HTML长度: {len(html)} 字符")
        print(f"   文本长度: {len(text)} 字符")
        
        # 测试本地日志
        reporter._log_email_locally(recipient, subject, html, text)
        log_dir = Path(reporter.config['log_directory'])
        if log_dir.exists():
            log_files = list(log_dir.glob("*.json"))
            print(f"✅ 邮件日志已保存: {len(log_files)} 个文件")
        
        # 测试简单通知
        notification_result = reporter.send_simple_notification(
            "测试通知", "这是一个测试通知消息"
        )
        print(f"✅ 简单通知测试完成: 成功={notification_result.get('success', False)}")
        
        # 测试统计信息
        stats = reporter.get_email_stats()
        print(f"📊 邮件统计: 总数={stats['total_emails']}, 成功率={stats['success_rate']:.1%}")
    
    print("\n✅ 邮件汇报系统测试完成")
    return True


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_email_reporter()
    else:
        print("用法:")
        print("  python email_reporter.py test")
        print("\n注意: 需要配置SMTP服务器信息才能实际发送邮件")