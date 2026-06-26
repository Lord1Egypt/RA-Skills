"""
主程序模块 - CLI 入口
"""
import os
import sys
import json
import argparse
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

from .config import config, SKILL_DATA_DIR
from .database import MailTracker
from .mail_handler import EmailClient, EmailStorage
from .analyzer_factory import create_analyzer
from .outbox import OutboxManager
from .dispatcher import MessageDispatcher
from .logger import setup_logging
from .get_email_by_id import get_email_by_id, format_output


def init_command():
    """初始化命令"""
    print("初始化 Smart Email...")
    
    # 创建必要的目录
    dirs = [
        config.get_storage_path(),
        config.get_storage_path(test_mode=True),
        config.get_outbox_path(),
        config.get_outbox_path(test_mode=True),
        config.get_logs_path(),
        Path(config.get_db_path()).parent
    ]
    
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ 创建目录: {d}")
    
    # 初始化数据库
    tracker = MailTracker(config.get_db_path())
    print(f"  ✓ 初始化数据库: {config.get_db_path()}")
    
    # 检查配置
    accounts = config.get_email_accounts()
    print(f"\n配置的邮箱账号: {len(accounts)} 个")
    for acc in accounts:
        print(f"  - {acc['provider']}: {acc['email']}")
    
    ai_config = config.get_ai_config()
    if ai_config['api_key']:
        print(f"\n✓ AI 配置正常")
        print(f"  - 分析限制: {ai_config.get('analyze_limit', 20)} 封/次")
        print(f"  - 并发限制: {ai_config.get('max_concurrent', 5)}")
        print(f"  - 重试次数: {ai_config.get('retry_count', 3)}")
    else:
        print(f"\n⚠ AI 配置不完整")
    
    # 显示其他配置
    download_limit = config.get_download_limit()
    cron_config = config.get_cron_config()
    print(f"\n其他配置:")
    print(f"  - 下载限制: {download_limit} 封/次")
    print(f"  - 检查间隔: {cron_config['check_interval_minutes']} 分钟")
    print(f"  - 汇总时间: {', '.join(cron_config['digest_times'])}")
    
    print("\n初始化完成！")


def parse_since(since_str: str) -> datetime:
    """解析时间范围字符串为 datetime"""
    if not since_str:
        return datetime.now() - timedelta(days=1)
    
    since_str = since_str.lower().strip()
    
    if since_str.endswith('h'):
        try:
            hours = int(since_str[:-1])
            return datetime.now() - timedelta(hours=hours)
        except ValueError:
            pass
    
    if since_str.endswith('d'):
        try:
            days = int(since_str[:-1])
            return datetime.now() - timedelta(days=days)
        except ValueError:
            pass
    
    try:
        date = datetime.strptime(since_str, '%Y-%m-%d')
        return date
    except ValueError:
        pass
    
    print(f"警告: 无法解析时间格式 '{since_str}'，使用默认72小时")
    return datetime.now() - timedelta(hours=72)


def check_command(test_mode: bool = False, since: str = None):
    """
    检查邮件命令 (v2 重构版)
    
    流程：
    - 阶段1: 下载所有新邮件到本地，标记 is_analyzed=0
    - 阶段2: 分析最早的 is_analyzed=0 且 retry_count<3 的邮件
      - 调用 LLM，一次返回 {is_urgent, reason, summary}
      - 检查结果有效性，无效则重试（retry_count++）
      - 重试 3 次仍失败：写入 summary="[分析失败]"，生成 error 消息到 outbox
      - 分析成功：写入数据库（is_analyzed=1, reason, summary），紧急邮件生成 urgent 消息
    """
    # 初始化日志系统
    log_dir = config.get_logs_path() if not test_mode else config.get_test_logs_path()
    logger = setup_logging('check', log_dir=log_dir)
    
    since_dt = parse_since(since) if since else None
    since_str = since_dt.strftime('%Y-%m-%d %H:%M') if since_dt else None
    
    mode_str = ""
    if test_mode:
        mode_str += "[测试模式] "
    if since_str:
        mode_str += f"[时间范围: {since_str}起] "
    
    print(f"{mode_str}开始检查邮件...")

    # 初始化组件
    if test_mode:
        test_db_path = config.get_test_db_path()
        test_db_path.parent.mkdir(parents=True, exist_ok=True)
        tracker = MailTracker(str(test_db_path))
        print(f"  [测试模式] 使用测试数据库: {test_db_path}")
        config.get_test_logs_path().mkdir(parents=True, exist_ok=True)
    else:
        tracker = MailTracker(config.get_db_path())
    
    storage = EmailStorage(config.get_storage_path(test_mode))
    outbox = OutboxManager(SKILL_DATA_DIR, test_mode=test_mode)

    # 使用工厂创建 Analyzer
    ai_config = config.get_ai_config()
    analyzer = None
    provider = os.getenv("SMART_EMAIL_LLM_PROVIDER", "openai").lower()

    if provider == "openai" and ai_config['api_key']:
        analyzer = create_analyzer(
            provider="openai",
            api_key=ai_config['api_key'],
            base_url=ai_config['base_url'],
            model=ai_config['model'],
            max_concurrent=ai_config.get('max_concurrent', 5),
            multimodal_analysis=ai_config.get('multimodal_analysis', False),
            retry_count=ai_config.get('retry_count', 3),
            retry_base_delay=ai_config.get('retry_base_delay', 1.0)
        )
        if ai_config.get('multimodal_analysis', False):
            print("  [多模态分析已开启] AI 将分析邮件正文图片")
    elif provider == "anthropic":
        anthropic_key = os.getenv("SMART_EMAIL_ANTHROPIC_API_KEY")
        if anthropic_key:
            analyzer = create_analyzer(
                provider="anthropic",
                api_key=anthropic_key,
                model=os.getenv("SMART_EMAIL_ANTHROPIC_MODEL"),
                base_url=os.getenv("SMART_EMAIL_ANTHROPIC_API_URL", ""),
                max_concurrent=ai_config.get('max_concurrent', 5),
                multimodal_analysis=ai_config.get('multimodal_analysis', False),
                retry_count=ai_config.get('retry_count', 3),
                retry_base_delay=ai_config.get('retry_base_delay', 1.0)
            )
            print(f"  [Anthropic Analyzer] 模型: {os.getenv('SMART_EMAIL_ANTHROPIC_MODEL')}")
        else:
            print("  ⚠️ SMART_EMAIL_ANTHROPIC_API_KEY 未配置，跳过 AI 分析")
    elif provider == "subagent":
        concurrency = int(os.getenv("SMART_EMAIL_SUBAGENT_CONCURRENCY", "3"))
        analyzer = create_analyzer(
            provider="subagent",
            max_concurrent=concurrency,
            retry_count=ai_config.get('retry_count', 3),
            retry_base_delay=ai_config.get('retry_base_delay', 1.0)
        )
        print(f"  [Subagent Analyzer] 并发数: {concurrency}")
    else:
        print(f"  ⚠️ 未配置 AI 分析 (provider: {provider})")
    
    # 获取邮箱账号
    accounts = config.get_email_accounts()
    if not accounts:
        print("错误: 没有配置的邮箱账号")
        return
    
    # 获取下载限制
    download_limit = config.get_download_limit()
    
    new_emails_count = 0
    connection_errors = []  # 用于聚合错误消息
    
    # ========== 第一阶段：下载所有新邮件（标记为 is_analyzed=0）==========
    print(f"\n【阶段1】下载新邮件（限制: {download_limit} 封）...")
    
    for account in accounts:
        print(f"\n  检查 {account['provider']} ({account['email']})...")
        
        client = EmailClient(
            provider=account['provider'],
            email_account=account['email'],
            password=account['password'],
            server=account['server'],
            port=account['port'],
            use_ssl=account['use_ssl']
        )
        
        try:
            emails = client.fetch_new_emails(limit=download_limit)
            print(f"    获取到 {len(emails)} 封邮件")
            
            # 时间范围过滤
            if since_dt:
                filtered_emails = []
                for email_data in emails:
                    try:
                        email_dt = datetime.fromisoformat(email_data.get('received_at', ''))
                        if email_dt >= since_dt:
                            filtered_emails.append(email_data)
                    except Exception:
                        filtered_emails.append(email_data)
                emails = filtered_emails
                print(f"    时间过滤后: {len(emails)} 封")
            
            # 保存新邮件（去重）
            saved_count = 0
            for email_data in emails:
                uid = email_data['uid']
                message_id = email_data.get('message_id')
                
                if tracker.is_email_exists(account['provider'], account['email'], uid, message_id):
                    continue
                
                email_data['provider'] = account['provider']
                local_path = storage.save_email(account['provider'], email_data)
                
                # 添加到数据库，标记为未分析（is_analyzed=0, retry_count=0）
                tracker.add_email(
                    provider=account['provider'],
                    email_account=account['email'],
                    uid=uid,
                    message_id=message_id,
                    subject=email_data['subject'],
                    sender=email_data['sender'],
                    received_at=email_data['received_at'],
                    local_path=local_path
                )
                
                saved_count += 1
                new_emails_count += 1
            
            if saved_count > 0:
                print(f"    ✓ 保存 {saved_count} 封新邮件")
            else:
                print(f"    没有新邮件")
                
        except Exception as e:
            error_msg = f"{account['provider']} 邮箱检查失败: {str(e)}"
            print(f"    ✗ {error_msg}")
            # 收集错误，稍后统一生成错误消息
            connection_errors.append({
                "provider": account['provider'],
                "error": str(e)
            })
        finally:
            client.disconnect()
    
    print(f"\n  阶段1完成: 新增 {new_emails_count} 封邮件到本地")
    
    # 生成聚合错误消息（如果有连接错误）
    if connection_errors:
        error_msg_id = outbox.write_error_message(connection_errors, error_type="connection")
        if error_msg_id:
            print(f"  ✓ 已生成错误消息: {error_msg_id}")
    
    # ========== 第二阶段：分析邮件（带重试机制）==========
    if not analyzer:
        print("\n【阶段2】跳过AI分析（未配置API Key）")
    else:
        analyze_limit = ai_config.get('analyze_limit', 20)
        # 只分析最近72小时内接收的邮件（与digest保持一致）
        since_dt = datetime.now() - timedelta(hours=72)
        since_str = since_dt.isoformat()
        print(f"\n【阶段2】AI分析最近72小时内最早的 {analyze_limit} 封未分析邮件...")

        # 从数据库获取最早的待分析邮件（is_analyzed=0 且 retry_count<3）
        pending_emails = tracker.get_pending_analysis_emails(limit=analyze_limit, since=since_str)
        
        if not pending_emails:
            print("  没有待分析的邮件")
        else:
            print(f"  找到 {len(pending_emails)} 封待分析邮件")
            
            # 准备邮件数据（从本地文件读取内容）
            emails_to_analyze = []
            for email_record in pending_emails:
                local_path = email_record.get('local_path', '')
                md_path = Path(local_path) / 'email.md'
                attachments_json = Path(local_path) / 'attachments.json'

                if not md_path.exists():
                    # 文件不存在，标记为分析失败
                    tracker.mark_analysis_failed(email_record['id'], "邮件文件不存在")
                    continue

                try:
                    with open(md_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # 读取附件信息（用于多模态分析）
                    saved_attachments = []
                    if attachments_json.exists():
                        with open(attachments_json, 'r', encoding='utf-8') as f:
                            saved_attachments = json.load(f)

                    email_data = {
                        'id': email_record['id'],
                        'subject': email_record['subject'],
                        'sender': email_record['sender'],
                        'received_at': email_record['received_at'],
                        'body_text': content,
                        'provider': email_record['provider'],
                        'local_path': local_path,
                        'saved_attachments': saved_attachments,
                        'retry_count': email_record.get('retry_count', 0)
                    }
                    emails_to_analyze.append(email_data)
                except Exception as e:
                    print(f"    ✗ 读取邮件失败: {e}")
                    tracker.mark_analysis_failed(email_record['id'], f"读取邮件失败: {str(e)}")
                    continue
            
            if emails_to_analyze:
                print(f"  开始分析（并发: {ai_config.get('max_concurrent', 5)}）...")
                
                urgent_count = 0
                failed_count = 0
                
                for email_data in emails_to_analyze:
                    email_record_id = email_data['id']
                    current_retry = email_data['retry_count']
                    email_id_str = email_data['local_path'].rstrip('/').split('/')[-1]
                    
                    try:
                        # 调用 LLM，一次返回 {is_urgent, reason, summary}
                        is_urgent, reason, summary = analyzer.analyze_email(email_data)
                        
                        # 分析成功，写入数据库
                        tracker.update_analysis_result(email_record_id, is_urgent, reason, summary)
                        
                        print(f"    [{'是' if is_urgent else '否'}] {email_data['subject'][:40]}... (重试{current_retry}次)")
                        
                        # 紧急邮件生成消息到 outbox
                        if is_urgent:
                            # 收集图片和附件路径
                            images = []
                            attachments = []
                            for att in email_data.get('saved_attachments', []):
                                local_path = att.get('local_path', '')
                                if att.get('is_inline') and att.get('content_type', '').startswith('image/'):
                                    images.append(local_path)
                                else:
                                    attachments.append(local_path)
                            
                            msg_id = outbox.write_urgent_message(
                                email_data=email_data,
                                reason=reason,
                                summary=summary,
                                images=images,
                                attachments=attachments
                            )
                            print(f"      ✓ 已生成紧急消息: {msg_id}")
                            urgent_count += 1
                            
                    except Exception as e:
                        error_msg = str(e)
                        print(f"    ✗ 分析失败: {email_data['subject'][:40]}... 错误: {error_msg[:50]}")
                        
                        # 递增重试次数
                        tracker.increment_retry_count(email_record_id, error_msg)
                        
                        # 检查是否达到重试上限
                        new_retry = current_retry + 1
                        if new_retry >= 3:
                            # 达到重试上限，标记为分析失败，生成 error 消息
                            tracker.mark_analysis_failed(email_record_id, error_msg)
                            
                            # 生成错误消息
                            msg_id = outbox.write_analysis_error_message(
                                email_id=email_id_str,
                                local_path=email_data['local_path'],
                                sender=email_data['sender'],
                                subject=email_data['subject'],
                                retry_count=new_retry,
                                last_error=error_msg
                            )
                            print(f"      ✓ 已生成错误消息: {msg_id}")
                            failed_count += 1
                
                print(f"\n  阶段2完成: 分析 {len(emails_to_analyze)} 封，紧急 {urgent_count} 封，失败 {failed_count} 封")
                
                # 检查是否还有未分析的邮件
                remaining = len(tracker.get_pending_analysis_emails(limit=9999))
                if remaining > 0:
                    print(f"  还有 {remaining} 封邮件待下次分析")
    
    print(f"\n{'='*50}")
    print(f"检查完成: 新增 {new_emails_count} 封邮件到本地")
    
    if test_mode:
        print("\n[测试模式] 邮件已保存到 tmp/ 目录，消息已生成到 tmp/outbox/pending/")
        print("          请检查生成的消息文件，不会实际发送")


def digest_command(test_mode: bool = False):
    """
    发送每日汇总命令 (v2 重构版)
    
    流程：
    - 查询所有 is_analyzed=1 的邮件（分析成功的）
    - 读取 outbox/sent/{date}/ 下已有 digest 的 email_ids
    - 过滤掉已通知的邮件
    - 复用数据库的 reason + summary 生成 digest 消息
    - 不调用任何 LLM API
    - 静默跳过分析失败的邮件（is_analyzed=0，不会被查询到）
    """
    # 初始化日志系统
    log_dir = config.get_logs_path() if not test_mode else config.get_test_logs_path()
    logger = setup_logging('digest', log_dir=log_dir)
    
    mode_str = "[测试模式] " if test_mode else ""
    print(f"{mode_str}生成每日邮件汇总...")
    
    if test_mode:
        test_db_path = config.get_test_db_path()
        test_db_path.parent.mkdir(parents=True, exist_ok=True)
        tracker = MailTracker(str(test_db_path))
        print(f"  [测试模式] 使用测试数据库: {test_db_path}")
        config.get_test_logs_path().mkdir(parents=True, exist_ok=True)
    else:
        tracker = MailTracker(config.get_db_path())
    
    outbox = OutboxManager(SKILL_DATA_DIR, test_mode=test_mode)
    
    # 只处理最近72小时内的已分析邮件
    since = (datetime.now() - timedelta(hours=72)).isoformat()
    analyzed_emails = tracker.get_analyzed_emails(since)
    
    if not analyzed_emails:
        print("没有已分析的邮件需要汇总")
        return
    
    print(f"找到 {len(analyzed_emails)} 封已分析邮件")
    
    # ========== 过滤已通知的邮件 ==========
    # 读取72小时内所有日期目录的已发送digest，防止重复通知
    notified_email_ids = set()
    for i in range(3):  # 72小时 = 3天
        check_date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        sent_dir = outbox.sent_dir / check_date
        if sent_dir.exists():
            for digest_file in sent_dir.glob("*.json"):
                try:
                    with open(digest_file, 'r', encoding='utf-8') as f:
                        digest_msg = json.load(f)
                        # 从 context.related_emails 中提取已包含的邮件ID
                        context = digest_msg.get('context', {})
                        email_ids = context.get('related_emails', [])
                        notified_email_ids.update(email_ids)
                except Exception as e:
                    print(f"  警告: 读取已发送digest失败 {digest_file}: {e}")
    
    # 过滤掉已通知的邮件
    new_emails = []
    skipped_count = 0
    for email in analyzed_emails:
        email_id = email.get('local_path', '').rstrip('/').split('/')[-1]
        if email_id in notified_email_ids:
            skipped_count += 1
        else:
            # 静默跳过分析失败的邮件（summary="[分析失败]"）
            if email.get('summary') == '[分析失败]':
                continue
            new_emails.append(email)
    
    if skipped_count > 0:
        print(f"  过滤掉 {skipped_count} 封已通知的邮件")
    
    if not new_emails:
        print("没有新邮件需要汇总")
        return
    
    print(f"待汇总 {len(new_emails)} 封新邮件")
    
    # ========== 分类：重要/一般 ==========
    # v2 统一使用 is_urgent 布尔值判断（与紧急通知一致）
    important = []
    normal = []

    for email in new_emails:
        summary = email.get('summary', email.get('subject', '无主题'))

        # 使用 is_urgent 布尔值判断（非紧急但重要的邮件归入"一般"）
        if email.get('is_urgent'):
            email['summary'] = summary
            important.append(email)
        else:
            email['summary'] = summary
            normal.append(email)
    
    print(f"重要: {len(important)} 封, 一般: {len(normal)} 封")
    
    # ========== 生成 digest 消息 ==========
    # 复用数据库的 reason + summary，不调用任何 LLM API
    date_str = datetime.now().strftime('%Y-%m-%d')
    msg_id = outbox.write_digest_message(important, normal, date_str)
    
    if msg_id:
        print(f"✓ 汇总消息已生成{'（带[测试]标识）' if test_mode else ''}: {msg_id}")
    else:
        print("✗ 汇总消息生成失败")


def setup_cron_command(print_only: bool = False, apply: bool = False):
    """设置定时任务命令 - 使用 OpenClaw 内置 cron"""
    # 获取 cron 配置
    cron_config = config.get_cron_config()
    check_interval = cron_config['check_interval_minutes']
    digest_times = cron_config['digest_times']

    # 构建检查任务的 cron 表达式
    if check_interval < 60:
        check_cron = f"*/{check_interval} * * * *"
    else:
        hours = check_interval // 60
        check_cron = f"0 */{hours} * * *"

    # 构建汇总任务的 cron 表达式
    digest_hours = [t.split(':')[0] for t in digest_times]
    digest_cron = f"0 {','.join(digest_hours)} * * *"
    digest_times_str = ', '.join(digest_times)

    if print_only:
        print("建议的 OpenClaw cron 配置：")
        print("="*50)
        print(f"任务1: smart-email-check")
        print(f"  计划: {check_cron}")
        print(f"  命令: python3 -m smart_email check")
        print()
        print(f"任务2: smart-email-digest")
        print(f"  计划: {digest_cron}")
        print(f"  命令: python3 -m smart_email digest")
        print("="*50)
        print(f"\n配置说明：")
        print(f"  - 检查间隔: {check_interval} 分钟")
        print(f"  - 汇总时间: {digest_times_str}")
        print(f"\n添加方法：")
        print(f"  自动添加: python3 -m smart_email setup-cron --apply")
        return

    if not apply:
        print("请使用 --apply 参数添加任务，或使用 --print 查看配置")
        return

    # 使用 OpenClaw cron 工具直接添加任务
    added_jobs = []
    failed_jobs = []

    # 查找 openclaw 命令路径
    openclaw_cmd = shutil.which("openclaw")
    if not openclaw_cmd:
        print("❌ 未找到 openclaw 命令，请确保 OpenClaw 已安装并添加到 PATH")
        print("\n请手动使用 openclaw cron 命令添加：")
        print(f"  openclaw cron add --name smart-email-check --schedule \"{check_cron}\" --command \"python3 -m smart_email check\"")
        print(f"  openclaw cron add --name smart-email-digest --schedule \"{digest_cron}\" --command \"python3 -m smart_email digest\"")
        return

    # 任务1: smart-email-check
    check_job_cmd = [
        openclaw_cmd, "cron", "add",
        "--name", "smart-email-check",
        "--cron", check_cron,
        "--message", "请执行 smart-email check 命令，收取并分析邮件，生成待发送消息到 outbox/pending/",
        "--session", "isolated",
        "--timeout-seconds", "600",
        "--tz", "Asia/Shanghai",
        "--no-deliver"
    ]

    try:
        result = subprocess.run(
            check_job_cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            added_jobs.append("smart-email-check")
        else:
            failed_jobs.append(("smart-email-check", result.stderr or result.stdout))
    except Exception as e:
        failed_jobs.append(("smart-email-check", str(e)))

    # 任务2: smart-email-digest
    digest_job_cmd = [
        openclaw_cmd, "cron", "add",
        "--name", "smart-email-digest",
        "--cron", digest_cron,
        "--message", "请执行 smart-email digest 命令，生成每日邮件汇总消息到 outbox/pending/",
        "--session", "isolated",
        "--timeout-seconds", "1200",
        "--tz", "Asia/Shanghai",
        "--no-deliver"
    ]

    try:
        result = subprocess.run(
            digest_job_cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            added_jobs.append("smart-email-digest")
        else:
            failed_jobs.append(("smart-email-digest", result.stderr or result.stdout))
    except Exception as e:
        failed_jobs.append(("smart-email-digest", str(e)))

    if added_jobs:
        print("✅ 成功添加以下 OpenClaw cron 任务：")
        for name in added_jobs:
            print(f"  - {name}")

    if failed_jobs:
        print("\n❌ 以下任务添加失败：")
        for name, error in failed_jobs:
            print(f"  - {name}: {error}")

    # 任务3: smart-email-dispatch
    dispatch_cron = "*/5 * * * *"
    dispatch_job_cmd = [
        openclaw_cmd, "cron", "add",
        "--name", "smart-email-dispatch",
        "--cron", dispatch_cron,
        "--message", "请执行 smart-email dispatch 命令，将 outbox 中的消息发送到用户指定渠道",
        "--session", "isolated",
        "--timeout-seconds", "300",
        "--tz", "Asia/Shanghai",
        "--no-deliver"
    ]

    try:
        result = subprocess.run(
            dispatch_job_cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            added_jobs.append("smart-email-dispatch")
        else:
            failed_jobs.append(("smart-email-dispatch", result.stderr or result.stdout))
    except Exception as e:
        failed_jobs.append(("smart-email-dispatch", str(e)))

    if added_jobs:
        print("✅ 成功添加以下 OpenClaw cron 任务：")
        for name in added_jobs:
            print(f"  - {name}")

    if failed_jobs:
        print("\n❌ 以下任务添加失败：")
        for name, error in failed_jobs:
            print(f"  - {name}: {error}")

    if added_jobs and not failed_jobs:
        print(f"\n配置说明：")
        print(f"  - 检查间隔: {check_interval} 分钟 ({check_cron})")
        print(f"  - 汇总时间: {digest_times_str} ({digest_cron})")
        print(f"  - 分发间隔: 5 分钟 ({dispatch_cron})")
        print(f"\n查看任务: openclaw cron list")
        print(f"删除任务: openclaw cron remove --id <job-id>")


def download_command(test_mode: bool = False, since: str = None, limit: int = 100):
    """仅下载邮件到本地，不进行AI分析"""
    # 初始化日志系统
    log_dir = config.get_logs_path() if not test_mode else config.get_test_logs_path()
    logger = setup_logging('download', log_dir=log_dir)
    
    since_dt = parse_since(since) if since else None
    since_str = since_dt.strftime('%Y-%m-%d %H:%M') if since_dt else None
    
    mode_str = "[测试模式] " if test_mode else ""
    if since_str:
        mode_str += f"[时间范围: {since_str}起] "
    
    print(f"{mode_str}开始下载邮件（仅保存，不分析）...")
    print(f"下载限制: {limit} 封")

    storage = EmailStorage(config.get_storage_path(test_mode))
    
    if test_mode:
        config.get_test_db_path().parent.mkdir(parents=True, exist_ok=True)
        config.get_test_logs_path().mkdir(parents=True, exist_ok=True)
        print(f"  [测试模式] 使用目录: {config.get_storage_path(test_mode)}")
    
    accounts = config.get_email_accounts()
    if not accounts:
        print("错误: 没有配置的邮箱账号")
        return
    
    downloaded_count = 0
    
    for account in accounts:
        print(f"\n连接 {account['provider']} ({account['email']})...")
        
        client = EmailClient(
            provider=account['provider'],
            email_account=account['email'],
            password=account['password'],
            server=account['server'],
            port=account['port'],
            use_ssl=account['use_ssl']
        )
        
        try:
            emails = client.fetch_new_emails(limit=limit)
            print(f"  获取到 {len(emails)} 封邮件")
            
            if since_dt:
                filtered_emails = []
                for email_data in emails:
                    try:
                        email_dt = datetime.fromisoformat(email_data.get('received_at', ''))
                        if email_dt >= since_dt:
                            filtered_emails.append(email_data)
                    except Exception:
                        filtered_emails.append(email_data)
                emails = filtered_emails
                print(f"  时间过滤后: {len(emails)} 封邮件")
            
            for email_data in emails:
                email_data['provider'] = account['provider']
                local_path = storage.save_email(account['provider'], email_data)
                print(f"  ✓ 已保存: {email_data['subject'][:40]}... -> {local_path}")
                downloaded_count += 1
                
        except Exception as e:
            print(f"  ✗ {account['provider']} 下载失败: {e}")
        finally:
            client.disconnect()
    
    print(f"\n{'='*50}")
    print(f"下载完成: 共 {downloaded_count} 封邮件")
    print(f"保存位置: {config.get_storage_path(test_mode)}")


def analyze_command(test_mode: bool = False, since: str = None, limit: int = None):
    """批量分析本地已下载的邮件（使用并发控制）"""
    # 初始化日志系统
    log_dir = config.get_logs_path() if not test_mode else config.get_test_logs_path()
    logger = setup_logging('analyze', log_dir=log_dir)
    
    since_dt = parse_since(since) if since else None
    since_str = since_dt.strftime('%Y-%m-%d %H:%M') if since_dt else None
    
    mode_str = "[测试模式] " if test_mode else ""
    if since_str:
        mode_str += f"[时间范围: {since_str}起] "
    if limit:
        mode_str += f"[限制: {limit}封] "
    
    print(f"{mode_str}开始批量分析本地邮件...")
    
    if test_mode:
        test_db_path = config.get_test_db_path()
        test_db_path.parent.mkdir(parents=True, exist_ok=True)
        tracker = MailTracker(str(test_db_path))
        storage_path = config.get_storage_path(test_mode)
        print(f"  [测试模式] 使用测试数据库: {test_db_path}")
        config.get_test_logs_path().mkdir(parents=True, exist_ok=True)
    else:
        tracker = MailTracker(config.get_db_path())
        storage_path = config.get_storage_path(test_mode)
    
    outbox = OutboxManager(SKILL_DATA_DIR, test_mode=test_mode)

    # 使用工厂创建 Analyzer
    ai_config = config.get_ai_config()
    analyzer = None
    provider = os.getenv("SMART_EMAIL_LLM_PROVIDER", "openai").lower()

    if provider == "openai" and ai_config['api_key']:
        analyzer = create_analyzer(
            provider="openai",
            api_key=ai_config['api_key'],
            base_url=ai_config['base_url'],
            model=ai_config['model'],
            max_concurrent=ai_config.get('max_concurrent', 5),
            multimodal_analysis=ai_config.get('multimodal_analysis', False),
            retry_count=ai_config.get('retry_count', 3),
            retry_base_delay=ai_config.get('retry_base_delay', 1.0)
        )
        if ai_config.get('multimodal_analysis', False):
            print("  [多模态分析已开启] AI 将分析邮件正文图片")
    elif provider == "anthropic":
        anthropic_key = os.getenv("SMART_EMAIL_ANTHROPIC_API_KEY")
        if anthropic_key:
            analyzer = create_analyzer(
                provider="anthropic",
                api_key=anthropic_key,
                model=os.getenv("SMART_EMAIL_ANTHROPIC_MODEL"),
                base_url=os.getenv("SMART_EMAIL_ANTHROPIC_API_URL", ""),
                max_concurrent=ai_config.get('max_concurrent', 5),
                multimodal_analysis=ai_config.get('multimodal_analysis', False),
                retry_count=ai_config.get('retry_count', 3),
                retry_base_delay=ai_config.get('retry_base_delay', 1.0)
            )
            print(f"  [Anthropic Analyzer] 模型: {os.getenv('SMART_EMAIL_ANTHROPIC_MODEL')}")
        else:
            print("错误: 未配置 SMART_EMAIL_ANTHROPIC_API_KEY")
            return
    elif provider == "subagent":
        concurrency = int(os.getenv("SMART_EMAIL_SUBAGENT_CONCURRENCY", "3"))
        analyzer = create_analyzer(
            provider="subagent",
            max_concurrent=concurrency,
            retry_count=ai_config.get('retry_count', 3),
            retry_base_delay=ai_config.get('retry_base_delay', 1.0)
        )
        print(f"  [Subagent Analyzer] 并发数: {concurrency}")
    else:
        print(f"错误: 未配置 AI 分析 (provider: {provider})")
        return
    
    if not storage_path.exists():
        print(f"错误: 邮件目录不存在: {storage_path}")
        return
    
    # 使用 analyze_limit 或传入的 limit
    analyze_limit = limit or ai_config.get('analyze_limit', 20)

    # 只分析最近72小时内接收的邮件（与digest保持一致）
    since_dt = datetime.now() - timedelta(hours=72)
    since_str = since_dt.isoformat()

    # 从数据库获取最早的未分析邮件（72小时内）
    pending_emails = tracker.get_pending_analysis_emails(limit=analyze_limit, since=since_str)
    
    if not pending_emails:
        print("没有需要分析的邮件")
        return
    
    print(f"\n找到 {len(pending_emails)} 封待分析邮件，开始批量分析 (并发: {ai_config.get('max_concurrent', 5)})...")
    
    # 准备邮件数据
    emails_to_analyze = []
    for email_record in pending_emails:
        local_path = email_record.get('local_path', '')
        md_path = Path(local_path) / 'email.md'
        attachments_json = Path(local_path) / 'attachments.json'

        if not md_path.exists():
            continue

        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 读取附件信息（用于多模态分析）
            saved_attachments = []
            if attachments_json.exists():
                with open(attachments_json, 'r', encoding='utf-8') as f:
                    saved_attachments = json.load(f)

            email_data = {
                'id': email_record['id'],
                'subject': email_record['subject'],
                'sender': email_record['sender'],
                'received_at': email_record['received_at'],
                'body_text': content,
                'provider': email_record['provider'],
                'local_path': local_path,
                'saved_attachments': saved_attachments
            }
            emails_to_analyze.append(email_data)
        except Exception as e:
            print(f"  读取邮件失败: {e}")
            continue
    
    if not emails_to_analyze:
        print("没有可分析的邮件")
        return
    
    analyzed_emails = []
    urgent_emails = []
    
    def on_analyzed(email_data, is_urgent, reason, summary):
        email_id = email_data['id']
        
        tracker.update_email_analysis(email_id, is_urgent=is_urgent)
        
        print(f"  [{'是' if is_urgent else '否'}] {email_data['subject'][:40]}...")
        analyzed_emails.append(email_data)
        
        if is_urgent:
            # 收集图片和附件路径
            images = []
            attachments = []
            for att in email_data.get('saved_attachments', []):
                local_path = att.get('local_path', '')
                if att.get('is_inline') and att.get('content_type', '').startswith('image/'):
                    images.append(local_path)
                else:
                    attachments.append(local_path)
            
            email_data['summary'] = summary
            msg_id = outbox.write_urgent_message(
                email_data=email_data,
                reason=reason,
                summary=summary,
                images=images,
                attachments=attachments
            )
            print(f"    ✓ 已生成紧急消息: {msg_id}")
            urgent_emails.append(email_data)
    
    results = analyzer.analyze_emails_batch(emails_to_analyze, callback=on_analyzed)
    
    print(f"\n{'='*50}")
    print(f"分析完成: 共 {len(analyzed_emails)} 封邮件")
    print(f"紧急邮件: {len(urgent_emails)} 封")
    
    # 检查是否还有未分析的邮件
    remaining = len(tracker.get_pending_analysis_emails(limit=9999))
    if remaining > 0:
        print(f"还有 {remaining} 封邮件待下次分析")


def test_error_notification(test_mode: bool = True):
    """测试错误通知功能"""
    print("🧪 测试错误通知...")

    outbox = OutboxManager(SKILL_DATA_DIR, test_mode=test_mode)
    
    # 生成测试错误消息
    test_errors = [
        {"provider": "qq", "error": "这是一条测试错误消息，用于验证错误通知功能是否正常工作。"}
    ]
    
    msg_id = outbox.write_error_message(test_errors, error_type="connection")
    
    if msg_id:
        print(f"✅ 测试错误消息已生成{'（带[测试]标识）' if test_mode else ''}: {msg_id}")
        print(f"   文件位置: {outbox.pending_dir / f'{msg_id}.json'}")
    else:
        print("❌ 测试错误消息生成失败")


def dispatch_command(test_mode: bool = False):
    """分发 outbox 消息到用户渠道"""
    # 初始化日志系统
    log_dir = config.get_logs_path() if not test_mode else config.get_test_logs_path()
    logger = setup_logging('dispatch', log_dir=log_dir)
    
    mode_str = "[测试模式] " if test_mode else ""
    print(f"{mode_str}开始分发消息...")
    
    # 创建分发器
    dispatcher = MessageDispatcher(test_mode=test_mode)
    
    # 检查配置
    delivery_config = config.get_delivery_config()
    if not delivery_config["enabled"]:
        print("⚠️ 发送渠道未配置")
        print("请配置以下环境变量：")
        print("  SMART_EMAIL_DELIVERY_CHANNEL=telegram  # 或 dingtalk, wecom")
        print("  SMART_EMAIL_DELIVERY_TARGET=@your_username")
        return
    
    print(f"发送渠道: {delivery_config['channel']}")
    print(f"发送目标: {delivery_config['target']}")
    
    # 获取待发送消息数量
    pending_count = dispatcher.get_pending_count()
    if pending_count == 0:
        print("没有待发送的消息")
        return
    
    print(f"\n发现 {pending_count} 条待发送消息")
    
    # 执行分发
    results = dispatcher.dispatch_all()
    
    # 显示结果
    print(f"\n{'='*50}")
    print(f"分发完成:")
    print(f"  总计: {results['total']} 条")
    print(f"  成功: {results['success']} 条")
    print(f"  失败: {results['failed']} 条")
    if test_mode:
        print(f"  跳过: {results['skipped']} 条（测试模式）")
    
    if results['failed'] > 0:
        print(f"\n失败的消息将保留在 pending/ 目录，下次自动重试")


def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def clean_command(test_mode: bool = False, force: bool = False):
    """删除本地邮件存储数据（不包括配置数据）

    删除内容：
    - 邮件存档 (mail-archives/)
    - Outbox 消息 (outbox/)
    - 运行日志 (logs/)
    - 数据库 (data/mail_tracker.db)

    保留内容：
    - 配置文件 (data/config.json)
    - 环境变量 (~/.openclaw/.env)
    """
    mode_str = "[测试模式] " if test_mode else "[正式版] "
    print(f"{mode_str}清理本地邮件存储数据...")

    if test_mode:
        # 测试模式：删除 tmp/ 目录下的所有内容
        tmp_dir = config.get_skill_data_path() / "tmp"
        paths_to_clean = [
            (tmp_dir / "mail-archives", "测试邮件存档"),
            (tmp_dir / "outbox", "测试 Outbox 消息"),
            (tmp_dir / "logs", "测试日志"),
            (tmp_dir / "data", "测试数据库"),
        ]
    else:
        # 正式模式：删除正式数据，但保留 config.json
        skill_data_dir = config.get_skill_data_path()
        paths_to_clean = [
            (skill_data_dir / "mail-archives", "邮件存档"),
            (skill_data_dir / "outbox", "Outbox 消息"),
            (skill_data_dir / "logs", "运行日志"),
            (skill_data_dir / "data" / "mail_tracker.db", "邮件数据库"),
        ]

    # 显示将要删除的内容
    print("\n以下数据将被删除：")
    total_size = 0
    for path, desc in paths_to_clean:
        if path.exists():
            if path.is_dir():
                size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
                file_count = sum(1 for _ in path.rglob('*') if _.is_file())
                print(f"  📁 {desc}: {path} ({file_count} 个文件, {format_size(size)})")
            else:
                size = path.stat().st_size
                print(f"  📄 {desc}: {path} ({format_size(size)})")
            total_size += size
        else:
            print(f"  ⚠️  {desc}: {path} (不存在)")

    if total_size > 0:
        print(f"\n总计: {format_size(total_size)}")
    else:
        print("\n没有需要清理的数据")
        return

    # 确认删除
    if not force:
        confirm = input("\n确认删除以上所有数据? [y/N]: ").strip().lower()
        if confirm not in ('y', 'yes'):
            print("已取消")
            return

    # 执行删除
    print("\n开始清理...")
    deleted_count = 0
    for path, desc in paths_to_clean:
        try:
            if path.exists():
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                print(f"  ✓ 已删除: {desc}")
                deleted_count += 1
        except Exception as e:
            print(f"  ✗ 删除失败 {desc}: {e}")

    print(f"\n{'='*50}")
    print(f"清理完成: 删除 {deleted_count} 项数据")

    if test_mode:
        print(f"测试数据已清空，配置文件保持不变")
    else:
        print(f"注意: 配置文件 config.json 和环境变量已保留")
        print(f"如需重新初始化，请运行: python3 -m smart_email init")


def get_email_command(email_id: str, test_mode: bool = False, format_type: str = "text"):
    """通过邮件ID查询原文件路径"""
    if not email_id:
        print("错误: 请提供邮件ID")
        print("用法: python3 -m smart_email get-email <email_id>")
        print("示例: python3 -m smart_email get-email qq_20250321_143022_abc123")
        return

    mode_str = "[测试模式] " if test_mode else ""
    print(f"{mode_str}查询邮件ID: {email_id}")
    print("-" * 50)

    result = get_email_by_id(email_id, test_mode=test_mode)
    print(format_output(result, format_type))

    if not result["found"]:
        sys.exit(1)


def main():
    """主入口"""
    parser = argparse.ArgumentParser(description='Smart Email - AI智能邮件管理助手')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    subparsers.add_parser('init', help='初始化配置和目录')
    
    check_parser = subparsers.add_parser('check', help='检查新邮件')
    check_parser.add_argument('--test', action='store_true', help='测试模式（消息标注[测试]）')
    check_parser.add_argument('--since', help='时间范围 (如: 12h, 24h, 3d, 2025-03-10)')
    
    # 分阶段测试命令
    test_check_parser = subparsers.add_parser('test-check', help='【阶段1/3】测试邮件检查与AI分析')
    test_check_parser.add_argument('--since', default='12h', help='时间范围 (默认: 12h)')
    
    test_error_parser = subparsers.add_parser('test-error', help='【阶段2/4】测试错误通知功能')

    test_digest_parser = subparsers.add_parser('test-digest', help='【阶段3/4】测试每日汇总功能')

    test_dispatch_parser = subparsers.add_parser('test-dispatch', help='【阶段4/4】测试消息分发功能')
    
    digest_parser = subparsers.add_parser('digest', help='发送每日汇总')
    digest_parser.add_argument('--test', action='store_true', help='测试模式（消息标注[测试]）')

    dispatch_parser = subparsers.add_parser('dispatch', help='分发 outbox 消息到用户渠道')
    dispatch_parser.add_argument('--test', action='store_true', help='测试模式（不实际发送）')
    
    cron_parser = subparsers.add_parser('setup-cron', help='设置定时任务')
    cron_parser.add_argument('--print', action='store_true', dest='print_only', help='仅打印配置')
    cron_parser.add_argument('--apply', action='store_true', help='自动添加到 crontab')
    
    download_parser = subparsers.add_parser('download', help='仅下载邮件到本地（不进行AI分析）')
    download_parser.add_argument('--test', action='store_true', help='测试模式')
    download_parser.add_argument('--since', help='时间范围')
    download_parser.add_argument('--limit', type=int, default=100, help='下载邮件数量限制 (默认: 100)')
    
    analyze_parser = subparsers.add_parser('analyze', help='批量分析本地已下载的邮件')
    analyze_parser.add_argument('--test', action='store_true', help='测试模式')
    analyze_parser.add_argument('--since', help='时间范围')
    analyze_parser.add_argument('--limit', type=int, help='分析邮件数量限制 (默认: 20)')
    
    # 添加清理命令 - 正式版
    clean_parser = subparsers.add_parser('clean', help='删除正式版本地邮件存储数据（保留配置）')
    clean_parser.add_argument('--force', '-f', action='store_true', help='跳过确认提示')

    # 添加清理命令 - 测试版
    clean_test_parser = subparsers.add_parser('clean-test', help='删除测试版本地邮件存储数据（保留配置）')
    clean_test_parser.add_argument('--force', '-f', action='store_true', help='跳过确认提示')

    # 添加 get-email 命令
    get_email_parser = subparsers.add_parser('get-email', help='通过邮件ID查询原文件路径')
    get_email_parser.add_argument('id', nargs='?', help='邮件ID，如 qq_20250321_143022_abc123')
    get_email_parser.add_argument('--id', dest='email_id', help='邮件ID（与位置参数二选一）')
    get_email_parser.add_argument('--test', '-t', action='store_true', help='查询测试目录')
    get_email_parser.add_argument('--format', '-f', choices=['json', 'text'], default='text', help='输出格式 (默认: text)')

    args = parser.parse_args()
    
    if args.command == 'init':
        init_command()
    elif args.command == 'check':
        check_command(test_mode=args.test, since=args.since)
    elif args.command == 'test-check':
        print("🧪 【阶段1/3】测试邮件检查与AI分析...")
        print("="*50)
        check_command(test_mode=True, since=args.since)
        print("\n✅ 阶段1测试完成！请检查生成的消息文件（tmp/outbox/pending/）")
    elif args.command == 'test-error':
        print("🧪 【阶段2/4】测试错误通知功能...")
        print("="*50)
        test_error_notification(test_mode=True)
        print("\n✅ 阶段2测试完成！请检查生成的错误消息文件（tmp/outbox/pending/）")
    elif args.command == 'test-digest':
        print("🧪 【阶段3/4】测试每日汇总功能...")
        print("="*50)
        digest_command(test_mode=True)
        print("\n✅ 阶段3测试完成！请检查生成的汇总消息文件（tmp/outbox/pending/）")
    elif args.command == 'test-dispatch':
        print("🧪 【阶段4/4】测试消息分发功能...")
        print("="*50)
        dispatch_command(test_mode=True)
        print("\n✅ 阶段4测试完成！")
    elif args.command == 'digest':
        digest_command(test_mode=args.test)
    elif args.command == 'dispatch':
        dispatch_command(test_mode=args.test)
    elif args.command == 'setup-cron':
        setup_cron_command(print_only=args.print_only, apply=args.apply)
    elif args.command == 'download':
        download_command(test_mode=args.test, since=args.since, limit=args.limit)
    elif args.command == 'analyze':
        analyze_command(test_mode=args.test, since=args.since, limit=args.limit)
    elif args.command == 'clean':
        clean_command(test_mode=False, force=args.force)
    elif args.command == 'clean-test':
        clean_command(test_mode=True, force=args.force)
    elif args.command == 'get-email':
        email_id = args.email_id or args.id
        get_email_command(email_id=email_id, test_mode=args.test, format_type=args.format)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
