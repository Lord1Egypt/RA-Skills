#!/usr/bin/env python3
"""
웹 페이지 변경 모니터링 엔진
Web Page Change Monitoring Engine for OpenClaw

이 스크립트는 지정된 웹 페이지의 선택된 요소들을 주기적으로 모니터링하고,
변경사항을 감지하여 저장하고 리포팅합니다.

변경 감지, 스냅샷 저장, 이력 관리 등의 기능을 제공합니다.
"""

import argparse
import json
import os
import sys
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from difflib import unified_diff
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class MonitoringEngine:
    """웹 페이지 변경 모니터링 엔진"""

    def __init__(self, data_dir: str = "monitor-data"):
        """
        Args:
            data_dir: 모니터링 데이터를 저장할 디렉토리
        """
        self.data_dir = Path(data_dir)
        self.monitors_file = self.data_dir / "monitors.json"
        self.alerts_file = self.data_dir / "alerts.json"
        self.snapshots_dir = self.data_dir / "snapshots"
        self.diffs_dir = self.data_dir / "diffs"

        # 필요한 디렉토리 생성
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """필요한 디렉토리 구조 생성"""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)
        self.diffs_dir.mkdir(parents=True, exist_ok=True)

    def _load_monitors(self) -> Dict[str, Any]:
        """monitors.json 파일에서 모니터 설정 로드"""
        if self.monitors_file.exists():
            try:
                with open(self.monitors_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading monitors: {e}", file=sys.stderr)
                return {}
        return {}

    def _save_monitors(self, monitors: Dict[str, Any]) -> None:
        """모니터 설정을 monitors.json에 저장"""
        try:
            with open(self.monitors_file, 'w', encoding='utf-8') as f:
                json.dump(monitors, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Error saving monitors: {e}", file=sys.stderr)

    def _load_alerts(self) -> List[Dict[str, Any]]:
        """alerts.json 파일에서 경고 로드"""
        if self.alerts_file.exists():
            try:
                with open(self.alerts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_alerts(self, alerts: List[Dict[str, Any]]) -> None:
        """경고를 alerts.json에 저장"""
        try:
            with open(self.alerts_file, 'w', encoding='utf-8') as f:
                json.dump(alerts, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Error saving alerts: {e}", file=sys.stderr)

    def _fetch_page(self, url: str) -> Optional[str]:
        """
        웹 페이지 다운로드

        Args:
            url: 다운로드할 URL

        Returns:
            페이지 HTML 내용, 또는 에러 발생 시 None
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}", file=sys.stderr)
            return None

    def _extract_items(self, html: str, selectors: Dict[str, str]) -> Dict[str, List[str]]:
        """
        HTML에서 CSS 선택자를 사용하여 항목 추출

        Args:
            html: HTML 내용
            selectors: CSS 선택자 딕셔너리 {'항목명': '.css-selector'}

        Returns:
            추출된 항목들 {'항목명': ['내용1', '내용2', ...]}
        """
        soup = BeautifulSoup(html, 'html.parser')
        items = {}

        for item_name, selector in selectors.items():
            try:
                elements = soup.select(selector)
                # 각 요소의 텍스트를 추출하고 공백 제거
                items[item_name] = [
                    elem.get_text(strip=True) for elem in elements
                ]
            except Exception as e:
                print(f"Error extracting '{item_name}' with selector '{selector}': {e}",
                      file=sys.stderr)
                items[item_name] = []

        return items

    def _get_latest_snapshot(self, name: str) -> Optional[Dict[str, Any]]:
        """
        특정 모니터의 가장 최근 스냅샷 가져오기

        Args:
            name: 모니터 이름

        Returns:
            스냅샷 데이터 또는 None
        """
        monitor_dir = self.snapshots_dir / name
        if not monitor_dir.exists():
            return None

        # 모든 스냅샷 파일을 날짜순으로 정렬
        snapshot_files = sorted(monitor_dir.glob('*.json'), reverse=True)
        if not snapshot_files:
            return None

        try:
            with open(snapshot_files[0], 'r', encoding='utf-8') as f:
                return json.load(f)
        except IOError as e:
            print(f"Error loading snapshot: {e}", file=sys.stderr)
            return None

    def _save_snapshot(self, name: str, data: Dict[str, Any]) -> None:
        """
        스냅샷 저장

        Args:
            name: 모니터 이름
            data: 스냅샷 데이터
        """
        monitor_dir = self.snapshots_dir / name
        monitor_dir.mkdir(parents=True, exist_ok=True)

        date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        snapshot_file = monitor_dir / f"{date_str}.json"

        try:
            with open(snapshot_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Error saving snapshot: {e}", file=sys.stderr)

    def _compare_items(self, old_items: List[str], new_items: List[str]) -> Dict[str, Any]:
        """
        이전과 현재 항목 비교

        Args:
            old_items: 이전 항목 목록
            new_items: 현재 항목 목록

        Returns:
            비교 결과 {'new': [...], 'removed': [...], 'changed': [...]}
        """
        old_set = set(old_items)
        new_set = set(new_items)

        return {
            'new': list(new_set - old_set),
            'removed': list(old_set - new_set),
            'changed': len(old_items) != len(new_items)
        }

    def _save_diff(self, name: str, diff_data: Dict[str, Any]) -> None:
        """
        변경사항을 diff 파일로 저장

        Args:
            name: 모니터 이름
            diff_data: 변경사항 데이터
        """
        monitor_dir = self.diffs_dir / name
        monitor_dir.mkdir(parents=True, exist_ok=True)

        date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        diff_file = monitor_dir / f"{date_str}_diff.json"

        try:
            with open(diff_file, 'w', encoding='utf-8') as f:
                json.dump(diff_data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Error saving diff: {e}", file=sys.stderr)

    def add_monitor(self, url: str, name: str, selectors_str: str,
                   check_interval: str) -> bool:
        """
        새로운 모니터 등록

        Args:
            url: 모니터할 URL
            name: 모니터 이름
            selectors_str: 선택자 문자열 'items=.class' 형식
            check_interval: 확인 주기 (hourly|daily|weekly)

        Returns:
            성공 여부
        """
        # 선택자 파싱: "items=.class1,content=.class2"
        selectors = {}
        try:
            for pair in selectors_str.split(','):
                key, value = pair.strip().split('=')
                selectors[key.strip()] = value.strip()
        except ValueError:
            print("Error: Selectors must be in format 'name1=.selector1,name2=.selector2'",
                  file=sys.stderr)
            return False

        # URL 검증
        try:
            urlparse(url)
        except Exception:
            print("Error: Invalid URL", file=sys.stderr)
            return False

        # 확인 주기 검증
        if check_interval not in ('hourly', 'daily', 'weekly'):
            print("Error: check_interval must be 'hourly', 'daily', or 'weekly'",
                  file=sys.stderr)
            return False

        monitors = self._load_monitors()

        if name in monitors:
            print(f"Error: Monitor '{name}' already exists", file=sys.stderr)
            return False

        monitors[name] = {
            'url': url,
            'name': name,
            'selectors': selectors,
            'check_interval': check_interval,
            'created_at': datetime.now().isoformat(),
            'last_checked': None
        }

        self._save_monitors(monitors)
        print(f"Monitor '{name}' added successfully")
        return True

    def check_monitor(self, name: str) -> bool:
        """
        특정 모니터 확인

        Args:
            name: 모니터 이름

        Returns:
            성공 여부
        """
        monitors = self._load_monitors()

        if name not in monitors:
            print(f"Error: Monitor '{name}' not found", file=sys.stderr)
            return False

        monitor = monitors[name]
        url = monitor['url']
        selectors = monitor['selectors']

        # 페이지 다운로드
        html = self._fetch_page(url)
        if html is None:
            return False

        # 항목 추출
        current_snapshot = {
            'timestamp': datetime.now().isoformat(),
            'url': url,
            'items': self._extract_items(html, selectors)
        }

        # 스냅샷 저장
        self._save_snapshot(name, current_snapshot)

        # 이전 스냅샷과 비교
        previous_snapshot = self._get_latest_snapshot(name)

        changes_detected = False
        diff_summary = {
            'monitor': name,
            'timestamp': datetime.now().isoformat(),
            'url': url,
            'changes_by_item': {}
        }

        if previous_snapshot:
            for item_name, current_items in current_snapshot['items'].items():
                old_items = previous_snapshot['items'].get(item_name, [])
                comparison = self._compare_items(old_items, current_items)

                if comparison['new'] or comparison['removed'] or comparison['changed']:
                    changes_detected = True
                    diff_summary['changes_by_item'][item_name] = {
                        'new': comparison['new'],
                        'removed': comparison['removed'],
                        'changed': comparison['changed'],
                        'old_count': len(old_items),
                        'new_count': len(current_items)
                    }
        else:
            # 첫 스냅샷 - 모든 항목이 새로운 것으로 간주
            for item_name, items in current_snapshot['items'].items():
                diff_summary['changes_by_item'][item_name] = {
                    'new': items,
                    'removed': [],
                    'changed': False,
                    'old_count': 0,
                    'new_count': len(items)
                }
            changes_detected = bool(current_snapshot['items'])

        # 변경사항 저장
        if changes_detected or previous_snapshot:
            self._save_diff(name, diff_summary)

        # 경고 추가 (변경 감지 시)
        if changes_detected:
            alerts = self._load_alerts()
            alerts.append({
                'monitor': name,
                'timestamp': datetime.now().isoformat(),
                'changes': diff_summary['changes_by_item'],
                'read': False
            })
            self._save_alerts(alerts)
            print(f"Changes detected in '{name}':")
            print(json.dumps(diff_summary, ensure_ascii=False, indent=2))
        else:
            print(f"No changes detected in '{name}'")

        # 마지막 확인 시간 업데이트
        monitor['last_checked'] = datetime.now().isoformat()
        self._save_monitors(monitors)

        return True

    def check_all_monitors(self) -> bool:
        """
        모든 모니터 확인

        Returns:
            성공 여부
        """
        monitors = self._load_monitors()

        if not monitors:
            print("No monitors registered")
            return True

        print(f"Checking {len(monitors)} monitor(s)...")
        all_success = True

        for monitor_name in monitors:
            if not self.check_monitor(monitor_name):
                all_success = False

        return all_success

    def show_status(self) -> bool:
        """모든 모니터의 상태 표시"""
        monitors = self._load_monitors()

        if not monitors:
            print("No monitors registered")
            return True

        print("\n모니터 상태 (Monitor Status)")
        print("=" * 80)

        for name, config in monitors.items():
            print(f"\n이름 (Name): {name}")
            print(f"URL: {config['url']}")
            print(f"확인 주기 (Interval): {config['check_interval']}")
            print(f"생성 시간 (Created): {config['created_at']}")
            print(f"마지막 확인 (Last Checked): {config.get('last_checked', 'Never')}")
            print(f"선택자 (Selectors): {', '.join(config['selectors'].keys())}")
            print("-" * 80)

        return True

    def remove_monitor(self, name: str) -> bool:
        """
        모니터 제거

        Args:
            name: 제거할 모니터 이름

        Returns:
            성공 여부
        """
        monitors = self._load_monitors()

        if name not in monitors:
            print(f"Error: Monitor '{name}' not found", file=sys.stderr)
            return False

        del monitors[name]
        self._save_monitors(monitors)
        print(f"Monitor '{name}' removed successfully")
        return True

    def weekly_report(self) -> bool:
        """
        지난 주간의 변경사항 리포트 생성

        Returns:
            성공 여부
        """
        monitors = self._load_monitors()

        if not monitors:
            print("No monitors registered")
            return True

        week_ago = datetime.now() - timedelta(days=7)
        report = {
            'generated_at': datetime.now().isoformat(),
            'period': f"Last 7 days (since {week_ago.isoformat()})",
            'monitors': {}
        }

        for monitor_name in monitors:
            monitor_diff_dir = self.diffs_dir / monitor_name
            if not monitor_diff_dir.exists():
                continue

            # 지난 일주일의 diff 파일 수집
            diff_files = [
                f for f in monitor_diff_dir.glob('*_diff.json')
                if datetime.fromisoformat(
                    json.loads(f.read_text(encoding='utf-8'))['timestamp']
                ) > week_ago
            ]

            if diff_files:
                changes = []
                for diff_file in sorted(diff_files):
                    with open(diff_file, 'r', encoding='utf-8') as f:
                        changes.append(json.load(f))

                report['monitors'][monitor_name] = {
                    'total_changes': len(changes),
                    'changes': changes
                }

        print("주간 리포트 (Weekly Report)")
        print("=" * 80)
        print(json.dumps(report, ensure_ascii=False, indent=2))

        return True


def main():
    """메인 함수 - CLI 인터페이스"""
    parser = argparse.ArgumentParser(
        description='Web page change monitoring engine for OpenClaw'
    )
    parser.add_argument('--data-dir', default='monitor-data',
                       help='Data directory for monitors (default: monitor-data)')

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # add 커맨드
    add_parser = subparsers.add_parser('add', help='Register a new monitor')
    add_parser.add_argument('--url', required=True, help='URL to monitor')
    add_parser.add_argument('--name', required=True, help='Monitor name')
    add_parser.add_argument('--selectors', required=True,
                           help='CSS selectors (e.g., "items=.class,content=.id")')
    add_parser.add_argument('--check-interval', required=True,
                           choices=['hourly', 'daily', 'weekly'],
                           help='Check interval')

    # check 커맨드
    check_parser = subparsers.add_parser('check', help='Check a specific monitor')
    check_parser.add_argument('--name', required=True, help='Monitor name')

    # check-all 커맨드
    subparsers.add_parser('check-all', help='Check all monitors')

    # status 커맨드
    subparsers.add_parser('status', help='Show status of all monitors')

    # weekly-report 커맨드
    subparsers.add_parser('weekly-report', help='Generate weekly report')

    # remove 커맨드
    remove_parser = subparsers.add_parser('remove', help='Remove a monitor')
    remove_parser.add_argument('--name', required=True, help='Monitor name')

    args = parser.parse_args()

    # 엔진 초기화
    engine = MonitoringEngine(args.data_dir)

    # 커맨드 실행
    if args.command == 'add':
        success = engine.add_monitor(
            args.url,
            args.name,
            args.selectors,
            args.check_interval
        )
        sys.exit(0 if success else 1)

    elif args.command == 'check':
        success = engine.check_monitor(args.name)
        sys.exit(0 if success else 1)

    elif args.command == 'check-all':
        success = engine.check_all_monitors()
        sys.exit(0 if success else 1)

    elif args.command == 'status':
        success = engine.show_status()
        sys.exit(0 if success else 1)

    elif args.command == 'weekly-report':
        success = engine.weekly_report()
        sys.exit(0 if success else 1)

    elif args.command == 'remove':
        success = engine.remove_monitor(args.name)
        sys.exit(0 if success else 1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
