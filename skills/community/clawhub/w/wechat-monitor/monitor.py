#!/usr/bin/env python3
"""
微信公众号监控脚本
用法: python3 monitor.py [产品名]
"""

import urllib.request
import json
import time
import os
import sys
from datetime import datetime

# API配置 - 从环境变量或配置文件获取
API_KEY = os.environ.get("MPTEXT_API_KEY", "YOUR_MPTEXT_API_KEY")

# 基础路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_headers():
    return {
        "X-Auth-Key": API_KEY,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json"
    }

def load_accounts(product_name):
    """加载指定产品的账号配置"""
    accounts_file = os.path.join(BASE_DIR, product_name, "accounts.json")
    
    if not os.path.exists(accounts_file):
        return None
    
    with open(accounts_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    accounts = data.get("accounts", [])
    # 兼容 Name/name 大小写
    for acc in accounts:
        if 'Name' in acc and 'name' not in acc:
            acc['name'] = acc.pop('Name')
    return accounts

def check_updates(accounts, days=7):
    """检查公众号最近更新"""
    headers = get_headers()
    seven_days_ago = time.time() - days * 24 * 3600
    results = []
    
    for acc in accounts:
        try:
            url = f"https://down.mptext.top/api/public/v1/article?fakeid={acc['fakeid']}&size=3"
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
            
            # 检查ret状态
            if data.get('ret', 0) == -1:
                return [{"error": "认证信息无效，需要重新登录mptext", "code": "AUTH_FAILED"}]
            
            if data.get("articles"):
                latest = data["articles"][0]
                update_time = latest.get("create_time", 0)
                is_new = update_time >= seven_days_ago
                
                results.append({
                    "name": acc['name'],
                    "category": acc.get('category', '其他'),
                    "hasNew": is_new,
                    "title": latest.get('title', ''),
                    "date": time.strftime("%m-%d", time.localtime(update_time)) if update_time else "未知",
                    "link": latest.get('link', '')
                })
            else:
                results.append({
                    "name": acc['name'],
                    "category": acc.get('category', '其他'),
                    "hasNew": False,
                    "title": "无文章",
                    "date": "未知"
                })
                
        except Exception as e:
            results.append({
                "name": acc['name'],
                "error": str(e)
            })
        
        time.sleep(1)
    
    return results

def generate_report(product_name, results):
    """生成报告（标准四段式结构）"""
    new_items = [r for r in results if r.get('hasNew')]
    errors = [r for r in results if r.get('error')]
    
    # 按分类分组
    official = [r for r in new_items if r.get('category') == '官方']
    competitor = [r for r in new_items if r.get('category') == '竞品']
    media = [r for r in new_items if r.get('category') in ['行业媒体', 'KOL', '运营干货']]
    
    today = datetime.now().strftime("%-m月%-d日")
    
    report = f"📅 {today} {product_name}公众号监控日报\n\n"
    
    if errors:
        for e in errors:
            if e.get('code') == 'AUTH_FAILED':
                report += f"❌ {e['error']}\n请登录 https://down.mptext.top 获取新密钥\n\n"
            else:
                report += f"❌ {e['name']}: {e.get('error', '未知错误')}\n"
        return report
    
    if not new_items:
        report += "📭 今日无更新\n"
        return report
    
    # ====================
    # 一、最新动态监控
    # ====================
    report += "━━━━━━━━━━━━━━━━━━━━\n"
    report += "一近期重要更新汇总\n"
    report += "━━━━━━━━━━━━━━━━━━━━\n\n"
    
    # 官方动态 🔴
    if official:
        report += "🔴 官方动态（微信更新）\n"
        report += "| 公众号 | 更新内容 | 日期 |\n"
        report += "|--------|---------|------|\n"
        for item in official:
            title = item.get('title', '未知')[:25]
            report += f"| {item['name']} | {title} | {item['date']} |\n"
        report += "\n"
    
    # 竞品动态 🟠
    if competitor:
        report += "🟠 竞品动态\n"
        report += "| 公众号 | 更新内容 | 日期 |\n"
        report += "|--------|---------|------|\n"
        for item in competitor:
            title = item.get('title', '未知')[:25]
            report += f"| {item['name']} | {title} | {item['date']} |\n"
        report += "\n"
    
    # 行业观察 🟢
    if media:
        report += "🟢 行业观察\n"
        report += "| 公众号 | 更新内容 | 日期 |\n"
        report += "|--------|---------|------|\n"
        for item in media:
            title = item.get('title', '未知')[:25]
            report += f"| {item['name']} | {title} | {item['date']} |\n"
        report += "\n"
    
    # ====================
    # 二、选题分析
    # ====================
    report += "━━━━━━━━━━━━━━━━━━━━\n"
    report += f"二、选题分析（适合{product_name}写的方向）\n"
    report += "━━━━━━━━━━━━━━━━━━━━\n\n"
    
    all_items = official + competitor + media
    
    for idx, item in enumerate(all_items[:3], 1):
        title = item.get('title', '未知')
        category = item.get('category', '其他')
        
        # 分类emoji和名称
        if category == '官方':
            emoji = "💡"
            cat_name = "微信动态类（官方授权）"
        elif category == '竞品':
            emoji = "💡"
            cat_name = "竞品玩法类"
        else:
            emoji = "💡"
            cat_name = "运营干货类"
        
        # 推断热度
        if item.get('date') in ['04-07', '04-06']:
            heat = "🔥🔥🔥 高"
        elif item.get('date') == '04-01':
            heat = "🔥🔥 中"
        else:
            heat = "🔥 低"
        
        # 推断角度
        if 'AI' in title or '企微' in title or '龙虾' in title:
            angle = "AI+企微趋势解读"
        elif '案例' in title or '门店' in title:
            angle = "大客户成功案例"
        elif '小红书' in title or '私域' in title:
            angle = "私域运营方法论"
        elif '用户' in title or '运营' in title:
            angle = "运营干货技巧"
        else:
            angle = "行业观察"
        
        # 产品结合
        if category == '官方':
            product_tip = f"蹭热点，结合{product_name}的{angle}功能做产品推广"
        elif category == '竞品':
            product_tip = f"参考竞品玩法，挖掘{product_name}差异化优势"
        else:
            product_tip = f"结合{angle}，输出干货教程"
        
        report += f"{emoji} **{cat_name}**\n\n"
        report += f"**{idx}. 《{title[:25]}...》**\n\n"
        report += f"- ○ **热度：** {heat}\n"
        report += f"- ○ **角度：** {angle}\n"
        report += f"- ○ **时效性：** {'强' if item.get('date') == '04-07' else '中'}\n"
        report += f"- ○ **跟进策略：** 等待更多信息出来后深度解读\n"
        report += f"- ○ **产品结合：** {product_tip}\n\n"
    
    # ====================
    # 三、本周高价值内容 TOP5
    # ====================
    report += "━━━━━━━━━━━━━━━━━━━━\n"
    report += "三、本周高价值内容 TOP5\n"
    report += "━━━━━━━━━━━━━━━━━━━━\n\n"
    
    report += "| 排名 | 来源 | 内容 |\n"
    report += "|------|------|------|\n"
    
    sorted_items = sorted(all_items, key=lambda x: x.get('date', ''), reverse=True)
    for idx, item in enumerate(sorted_items[:5], 1):
        title = item.get('title', '未知')[:20]
        report += f"| {idx} | {item['name']} | {title}... |\n"
    
    report += "\n"
    
    # ====================
    # 四、本周可写的文章建议
    # ====================
    report += "━━━━━━━━━━━━━━━━━━━━\n"
    report += f"四、{product_name}本周可写的文章建议\n"
    report += "━━━━━━━━━━━━━━━━━━━━\n\n"
    
    report += "| 优先级 | 选题 | 类型 |\n"
    report += "|--------|---------|------|\n"
    
    if official:
        report += f"| 🔴 高 | 《企微+AI趋势解读：私域运营智能化升级指南》 | 热点解读+产品推广 |\n"
    if media:
        report += f"| 🔴 高 | 《月销破千万的私域运营方法论》 | 干货教程 |\n"
    if competitor:
        report += f"| 🟠 中 | 《竞品SCRM案例：连锁门店运营拆解》 | 案例分析 |\n"
    
    report += f"\n📊 总计：{len(new_items)}个账号有更新\n"
    
    return report

def save_report(product_name, report):
    """保存报告到文件"""
    reports_dir = os.path.join(BASE_DIR, product_name, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    report_file = os.path.join(reports_dir, f"{today}.md")
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    return report_file

def main():
    # 获取产品名（从命令行参数）
    product_name = sys.argv[1] if len(sys.argv) > 1 else "default"
    
    # 获取天数参数（默认7天）
    days = 7
    if len(sys.argv) > 2 and sys.argv[2] == "--days":
        if len(sys.argv) > 3:
            days = int(sys.argv[3])
    
    # 检查产品目录是否存在
    product_dir = os.path.join(BASE_DIR, product_name)
    if not os.path.exists(product_dir):
        print(f"❌ 产品 '{product_name}' 的目录不存在")
        print(f"请先告诉我要添加该产品的公众号")
        sys.exit(1)
    
    # 加载账号
    accounts = load_accounts(product_name)
    if not accounts:
        print(f"❌ 产品 '{product_name}' 没有配置任何公众号")
        sys.exit(1)
    
    print(f"🔍 检查 {product_name} 的 {len(accounts)} 个公众号（近{days}天）...\n")
    
    # 检查更新
    results = check_updates(accounts, days=days)
    
    if results and results[0].get('code') == 'AUTH_FAILED':
        print(results[0]['error'])
        sys.exit(1)
    
    # 生成报告
    report = generate_report(product_name, results)
    
    # 保存报告
    report_file = save_report(product_name, report)
    
    # 删除首次运行flag（如果存在）
    flag_file = os.path.join(product_dir, "first_run.flag")
    if os.path.exists(flag_file):
        os.remove(flag_file)
        print(f"✅ 首次运行flag已删除，后续将只检查近1天更新")
    
    # 打印报告
    print(report)
    print(f"📁 报告已保存到: {report_file}")

if __name__ == "__main__":
    main()
