#!/usr/bin/env python3
"""
禅道 Bug 统计工具
功能：
1. 按起始日期统计版本bug：总数、问题引入、激活、待解决、待验证
2. 今日bug统计：新建、关闭、激活、问题引入
"""

import urllib.request
import urllib.parse
from http.cookiejar import CookieJar
import re
from datetime import datetime, timedelta
import sys


class ZentaoStats:
    def __init__(
        self,
        zentao_url: str = None,
        username: str = None,
        password: str = None
    ):
        import os
        # 从环境变量或参数获取配置
        self.zentao_url = (zentao_url or os.environ.get('ZENTAO_URL', 'http://172.16.16.1:81/zentao/')).rstrip('/') + '/'
        self.username = username or os.environ.get('ZENTAO_USER', 'jinx_robot')
        self.password = password or os.environ.get('ZENTAO_PASS', '!!123Abc')
        self.cookiejar = CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookiejar))
    
    def _login(self) -> bool:
        """登录禅道"""
        self.opener.open(self.zentao_url, timeout=30)
        login_data = urllib.parse.urlencode({
            "account": self.username,
            "password": self.password,
            "submit": "登录",
        }).encode('utf-8')
        
        req = urllib.request.Request(
            f"{self.zentao_url}user-login.html",
            data=login_data,
            headers={'Referer': self.zentao_url}
        )
        self.opener.open(req, timeout=30)
        self.opener.open(self.zentao_url, timeout=30)
        return True
    
    def _query_count(self, params: str) -> int:
        """执行查询并返回总数"""
        search_url = f"{self.zentao_url}search-buildQuery.html"
        data = params.encode('utf-8')
        
        req = urllib.request.Request(
            search_url,
            data=data,
            headers={
                'Referer': self.zentao_url,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        self.opener.open(req, timeout=30)
        
        result_url = f"{self.zentao_url}bug-browse-28-all-bySearch-myQueryID.html"
        resp = self.opener.open(urllib.request.Request(result_url, headers={'Referer': self.zentao_url}), timeout=30)
        html = resp.read().decode('utf-8')
        
        total_match = re.search(r"data-rec-total='(\d+)'", html)
        return int(total_match.group(1)) if total_match else 0
    
    def stats_version(self, start_date: str) -> dict:
        """按起始日期统计版本bug
        
        Args:
            start_date: 起始日期 (YYYY-MM-DD)
            
        Returns:
            dict: {'total': int, 'defect': int, 'activated': int, 'unresolved': int, 'resolved': int}
        """
        # 基础查询参数 (日期范围: start_date ~ today)
        today = datetime.now().strftime('%Y-%m-%d')
        
        base_params = (
            'fieldtitle=&fieldkeywords=&fieldsteps=&fieldassignedTo=&fieldresolvedBy=&fieldstatus='
            '&fieldconfirmed=&fieldstory=&fieldproject=47&fieldproduct=28&fieldplan='
            '&fieldmodule=ZERO&fieldexecution=0&fieldseverity=0&fieldpri=0&fieldtype='
            '&fieldos=&fieldbrowser=&fieldresolution=&fieldactivatedCount='
            '&fieldtoTask=&fieldtoStory=&fieldopenedBy=&fieldclosedBy=&fieldlastEditedBy='
            '&fieldmailto=&fieldopenedBuild=&fieldresolvedBuild=&fieldopenedDate='
            '&fieldassignedDate=&fieldresolvedDate=&fieldclosedDate=&fieldlastEditedDate='
            '&fielddeadline=&fieldactivatedDate=&fieldid='
            f'&andOr1=AND&field1=openedDate&operator1=%3E%3D&value1={start_date}'
            f'&andOr2=and&field2=openedDate&operator2=%3C%3D&value2={today}'
            '&andOr3=and&field3=type&operator3=%3D&value3=&groupAndOr=and'
            '&andOr4=AND&field4=openedBuild&operator4=%21%3D&value4='
            '&andOr5=and&field5=assignedTo&operator5=%3D&value5='
            '&andOr6=and&field6=resolvedBy&operator6=%3D&value6='
            '&module=bug&actionURL=%2Fzentao%2Fbug-browse-28-all-bySearch-myQueryID.html'
            '&groupItems=3&formType=more'
        )
        
        # 1. 总数 (创建日期 >= start_date)
        total = self._query_count(base_params)
        
        # 2. 问题引入 (type=defectIntro)
        q_defect = base_params.replace(
            'field3=type&operator3=%3D&value3=',
            'field3=type&operator3=%3D&value3=defectIntro'
        )
        defect = self._query_count(q_defect)
        
        # 3. 激活次数>=1 (activatedCount>=1, 用field4替换openedBuild条件)
        q_activated = base_params.replace(
            'field4=openedBuild&operator4=%21%3D&value4=',
            'field4=activatedCount&operator4=%3E%3D&value4=1'
        )
        q_activated = q_activated.replace('groupItems=3', 'groupItems=4')
        activated = self._query_count(q_activated)
        
        # 4. 待解决 (status=active)
        q_unresolved = base_params.replace(
            'field3=type&operator3=%3D&value3=',
            'field3=status&operator3=%3D&value3=active'
        )
        q_unresolved = q_unresolved.replace('groupItems=3', 'groupItems=4')
        unresolved = self._query_count(q_unresolved)
        
        # 5. 待验证 (status=resolved)
        q_resolved = base_params.replace(
            'field3=type&operator3=%3D&value3=',
            'field3=status&operator3=%3D&value3=resolved'
        )
        q_resolved = q_resolved.replace('groupItems=3', 'groupItems=4')
        resolved = self._query_count(q_resolved)
        
        return {
            'start_date': start_date,
            'end_date': today,
            'total': total,
            'defect': defect,
            'activated': activated,
            'unresolved': unresolved,
            'resolved': resolved
        }
    
    def stats_today(self) -> dict:
        """今日bug统计
        
        Returns:
            dict: {'created': int, 'closed': int, 'activated': int, 'defect': int}
        """
        today = datetime.now().strftime('%Y-%m-%d')
        
        base_params = (
            'fieldtitle=&fieldkeywords=&fieldsteps=&fieldassignedTo=&fieldresolvedBy=&fieldstatus='
            '&fieldconfirmed=&fieldstory=&fieldproject=47&fieldproduct=28&fieldplan='
            '&fieldmodule=ZERO&fieldexecution=0&fieldseverity=0&fieldpri=0&fieldtype='
            '&fieldos=&fieldbrowser=&fieldresolution=&fieldactivatedCount='
            '&fieldtoTask=&fieldtoStory=&fieldopenedBy=&fieldclosedBy=&fieldlastEditedBy='
            '&fieldmailto=&fieldopenedBuild=&fieldresolvedBuild=&fieldopenedDate='
            '&fieldassignedDate=&fieldresolvedDate=&fieldclosedDate=&fieldlastEditedDate='
            '&fielddeadline=&fieldactivatedDate=&fieldid='
            f'&andOr1=AND&field1=openedDate&operator1=%3E%3D&value1={today}'
            f'&andOr2=and&field2=openedDate&operator2=%3C%3D&value2={today}'
            '&andOr3=and&field3=type&operator3=%3D&value3=&groupAndOr=and'
            '&andOr4=AND&field4=openedBuild&operator4=%21%3D&value4='
            '&andOr5=and&field5=assignedTo&operator5=%3D&value5='
            '&andOr6=and&field6=resolvedBy&operator6=%3D&value6='
            '&module=bug&actionURL=%2Fzentao%2Fbug-browse-28-all-bySearch-myQueryID.html'
            '&groupItems=3&formType=more'
        )
        
        # 1. 今日新建
        created = self._query_count(base_params)
        
        # 2. 今日关闭 (closedDate = today) - 按关闭日期筛选
        q_closed = base_params.replace(
            'field1=openedDate&operator1=%3E%3D&value1=' + today,
            'field1=closedDate&operator1=%3E%3D&value1=' + today
        ).replace(
            'field2=openedDate&operator2=%3C%3D&value2=' + today,
            'field2=closedDate&operator2=%3C%3D&value2=' + today
        )
        closed = self._query_count(q_closed)
        
        # 3. 今日激活 (activatedDate = today)
        q_activated = base_params.replace(
            'fieldopenedDate=',
            'fieldactivatedDate='
        ).replace(
            'field1=openedDate&operator1=%3E%3D&value1=' + today,
            'field1=activatedDate&operator1=%3E%3D&value1=' + today
        ).replace(
            'field2=openedDate&operator2=%3C%3D&value2=' + today,
            'field2=activatedDate&operator2=%3C%3D&value2=' + today
        )
        activated = self._query_count(q_activated)
        
        # 4. 今日问题引入 (type=defectIntro + openedDate = today)
        q_defect = base_params.replace(
            'field3=type&operator3=%3D&value3=',
            'field3=type&operator3=%3D&value3=defectIntro'
        )
        defect = self._query_count(q_defect)
        
        return {
            'date': today,
            'created': created,
            'closed': closed,
            'activated': activated,
            'defect': defect
        }


def main():
    import argparse
    parser = argparse.ArgumentParser(description='禅道 Bug 统计')
    parser.add_argument('--start-date', type=str, help='起始日期 (YYYY-MM-DD)', default=None)
    parser.add_argument('--today', action='store_true', help='今日统计')
    parser.add_argument('--all', action='store_true', help='全部统计')
    
    args = parser.parse_args()
    
    tool = ZentaoStats()
    
    print("=" * 60)
    print("🔐 登录禅道...")
    tool._login()
    print("✅ 登录成功")
    print()
    
    if args.all:
        # 全部统计：今日 + 指定起始日期
        start_date = args.start_date or '2026-02-25'
        
        # 今日统计
        print("=" * 60)
        print("📊 今日 Bug 统计")
        print("=" * 60)
        today_stats = tool.stats_today()
        print(f"日期: {today_stats['date']}")
        print(f"  新建: {today_stats['created']}")
        print(f"  关闭: {today_stats['closed']}")
        print(f"  激活: {today_stats['activated']}")
        print(f"  问题引入: {today_stats['defect']}")
        print()
        
        # 版本统计
        print("=" * 60)
        print(f"📊 版本 Bug 统计 (起始日期: {start_date})")
        print("=" * 60)
        version_stats = tool.stats_version(start_date)
        print(f"日期范围: {version_stats['start_date']} ~ {version_stats['end_date']}")
        print(f"  总数: {version_stats['total']}")
        print(f"  问题引入: {version_stats['defect']}")
        print(f"  激活>=1: {version_stats['activated']}")
        print(f"  待解决: {version_stats['unresolved']}")
        print(f"  待验证: {version_stats['resolved']}")
        
    elif args.today:
        # 只看今日
        print("=" * 60)
        print("📊 今日 Bug 统计")
        print("=" * 60)
        today_stats = tool.stats_today()
        print(f"日期: {today_stats['date']}")
        print(f"  新建: {today_stats['created']}")
        print(f"  关闭: {today_stats['closed']}")
        print(f"  激活: {today_stats['activated']}")
        print(f"  问题引入: {today_stats['defect']}")
        
    elif args.start_date:
        # 只看版本统计
        print("=" * 60)
        print(f"📊 版本 Bug 统计 (起始日期: {args.start_date})")
        print("=" * 60)
        version_stats = tool.stats_version(args.start_date)
        print(f"日期范围: {version_stats['start_date']} ~ {version_stats['end_date']}")
        print(f"  总数: {version_stats['total']}")
        print(f"  问题引入: {version_stats['defect']}")
        print(f"  激活>=1: {version_stats['activated']}")
        print(f"  待解决: {version_stats['unresolved']}")
        print(f"  待验证: {version_stats['resolved']}")
        
    else:
        # 默认显示帮助
        parser.print_help()
        print()
        print("示例:")
        print("  python zentao_stats.py --start-date 2026-02-25")
        print("  python zentao_stats.py --today")
        print("  python zentao_stats.py --all --start-date 2026-02-25")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())