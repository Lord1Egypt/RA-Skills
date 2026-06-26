#!/usr/bin/env python3
"""
Fetch task counters from students.myofek.cet.ac.il for each child.
Login: students portal → Ministry of Education SSO (username/password).
"""
import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional

from playwright.sync_api import sync_playwright

STUDENTS_URL = "https://students.myofek.cet.ac.il/he"
DEFAULT_ENV_PATH = Path('/root/.openclaw/workspace/.env/webtop-galim.env')
LEGACY_ENV_PATH = Path('/root/.openclaw/workspace/.env/galim.env')


@dataclass
class OfekActivity:
    title: str
    subject: str
    due_at: str
    teacher: Optional[str] = None
    is_urgent: bool = False
    is_overdue: bool = False


@dataclass
class TaskSummary:
    child_name: str
    source: str
    open_count: Optional[int] = None
    fix_count: Optional[int] = None
    checked_count: Optional[int] = None
    waiting_count: Optional[int] = None
    urgent_activities: List[OfekActivity] = None
    overdue_activities: List[OfekActivity] = None
    raw: Dict = None
    error: Optional[str] = None


def load_env(path: Path) -> dict:
    env = {}
    for line in path.read_text(encoding='utf-8', errors='ignore').splitlines():
        if '=' in line and not line.strip().startswith('#'):
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()
    return env


def choose_env_path() -> Path:
    override = Path(__import__('os').environ['WEBTOP_GALIM_ENV']) if 'WEBTOP_GALIM_ENV' in __import__('os').environ else None
    if override and override.exists():
        return override
    if DEFAULT_ENV_PATH.exists():
        env = load_env(DEFAULT_ENV_PATH)
        if any(env.get(k) for k in ('OFEK_USERNAME_CHILD1', 'OFEK_USERNAME_CHILD2')):
            return DEFAULT_ENV_PATH
    return LEGACY_ENV_PATH


def load_kids() -> List[Dict[str, str]]:
    env = load_env(choose_env_path())

    if env.get('OFEK_USERNAME_CHILD1') and env.get('OFEK_PASSWORD_CHILD1'):
        return [
            {"name": env.get("OFEK_NAME_CHILD1", "Child 1").strip('"'), "username": env["OFEK_USERNAME_CHILD1"], "password": env["OFEK_PASSWORD_CHILD1"]},
            {"name": env.get("OFEK_NAME_CHILD2", "Child 2").strip('"'), "username": env["OFEK_USERNAME_CHILD2"], "password": env["OFEK_PASSWORD_CHILD2"]},
        ]

    if env.get('OFEK_USERNAME_YUVAL') and env.get('OFEK_PASSWORD_YUVAL'):
        return [
            {"name": env.get("OFEK_NAME_YUVAL", "Child 1").strip('"'), "username": env["OFEK_USERNAME_YUVAL"], "password": env["OFEK_PASSWORD_YUVAL"]},
            {"name": env.get("OFEK_NAME_SHIRA", "Child 2").strip('"'), "username": env["OFEK_USERNAME_SHIRA"], "password": env["OFEK_PASSWORD_SHIRA"]},
        ]

    raise RuntimeError('Missing Ofek credentials in webtop-galim.env or legacy galim.env')


def extract_count(text: str, label: str) -> Optional[int]:
    """Extract number from pattern like 'לביצוע (9)' or 'הוחזר לתיקון (1)'."""
    m = re.search(re.escape(label) + r'\s*\((\d+)\)', text)
    return int(m.group(1)) if m else None


def parse_activity_blocks(lines: List[str], start_label: str, stop_labels: List[str]) -> List[OfekActivity]:
    start = None
    for idx, line in enumerate(lines):
        if line.startswith(start_label):
            start = idx + 1
            break
    if start is None:
        return []

    items: List[OfekActivity] = []
    i = start
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if any(line.startswith(label) for label in stop_labels):
            break
        if line == 'פתיחת הפעילות':
            i += 1
            continue
        if i + 2 >= len(lines):
            break

        title = lines[i].strip()
        subject_line = lines[i + 1].strip()
        due_line = lines[i + 2].strip()
        if due_line == 'פתיחת הפעילות' or not due_line.startswith('להגשה עד '):
            i += 1
            continue

        teacher = None
        subject = subject_line
        m = re.match(r'^(.*?)\s+\((.*?)\)$', subject_line)
        if m:
            subject = m.group(1).strip()
            teacher = m.group(2).strip()

        items.append(OfekActivity(
            title=title,
            subject=subject,
            due_at=due_line.replace('להגשה עד ', '').strip(),
            teacher=teacher,
            is_urgent=(start_label == 'הפעילויות הכי דחופות'),
            is_overdue=(start_label == 'הפעילויות שאיחרת להגיש'),
        ))

        i += 3
        if i < len(lines) and lines[i].strip() == 'פתיחת הפעילות':
            i += 1

    return items


def fetch_summary(page, username: str, password: str, child_name: str) -> TaskSummary:
    result = TaskSummary(child_name=child_name, source="ofek", raw={})
    try:
        page.goto(STUDENTS_URL, wait_until='networkidle', timeout=60000)

        # Click "Ministry of Education" login option
        page.get_by_text("התחברות משרד החינוך").click()
        page.wait_for_load_state('networkidle', timeout=30000)

        # Fill credentials on MOE SSO page
        page.locator('#userName').fill(username)
        page.locator('#password').evaluate("el => el.removeAttribute('readonly')")
        page.locator('#password').fill(password)
        page.get_by_role('button', name='כניסה', exact=True).click()

        page.wait_for_timeout(8000)

        body = page.locator('body').inner_text(timeout=10000)

        if 'פרטי ההזדהות שגויים' in body or 'שגיאה' in body[:200]:
            result.error = 'פרטי הזדהות שגויים'
            return result

        if child_name not in body and 'הפעילויות שלך' not in body:
            result.error = f'לא נמסרת כניסה. URL: {page.url}'
            return result

        result.open_count   = extract_count(body, 'לביצוע')
        result.fix_count    = extract_count(body, 'הוחזר לתיקון')
        result.checked_count = extract_count(body, 'בוצע ונבדק')
        result.waiting_count = extract_count(body, 'מחכה לבדיקת מורה')
        lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
        result.urgent_activities = parse_activity_blocks(
            lines,
            'הפעילויות הכי דחופות',
            ['הפעילויות שאיחרת להגיש', '© כל הזכויות שמורות', 'כל המקצועות']
        )
        result.overdue_activities = parse_activity_blocks(
            lines,
            'הפעילויות שאיחרת להגיש',
            ['© כל הזכויות שמורות', 'כל המקצועות']
        )
        result.raw = {
            "todo": str(result.open_count),
            "tofix": str(result.fix_count),
            "checked": str(result.checked_count),
            "waiting": str(result.waiting_count),
            "urgent_activities": [asdict(x) for x in (result.urgent_activities or [])],
            "overdue_activities": [asdict(x) for x in (result.overdue_activities or [])],
        }
        return result
    except Exception as e:
        result.error = str(e)
        return result


def format_hebrew(results: List[TaskSummary]) -> str:
    lines = ["📚 אופק", ""]
    for item in results:
        lines.append(f"👤 {item.child_name}")
        if item.error:
            lines.append(f"❌ שגיאה: {item.error}")
        else:
            lines.append(f"• לביצוע: {item.open_count if item.open_count is not None else '?'}")
            lines.append(f"• לתיקון: {item.fix_count if item.fix_count is not None else '?'}")
            lines.append(f"• ממתינות לבדיקה: {item.waiting_count if item.waiting_count is not None else '?'}")
            lines.append(f"• נבדקו: {item.checked_count if item.checked_count is not None else '?'}")
            if item.urgent_activities:
                lines.append('• הכי דחופות:')
                for act in item.urgent_activities[:5]:
                    due = f" | יעד: {act.due_at}" if act.due_at else ''
                    lines.append(f"  - {act.title} — {act.subject}{due}")
            if item.overdue_activities:
                lines.append('• באיחור:')
                for act in item.overdue_activities[:5]:
                    due = f" | יעד: {act.due_at}" if act.due_at else ''
                    lines.append(f"  - {act.title} — {act.subject}{due}")
        lines.append("")
    return "\n".join(lines).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--show-browser", action="store_true")
    args = parser.parse_args()

    kids = load_kids()
    results: List[TaskSummary] = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not args.show_browser)
        for kid in kids:
            page = browser.new_page()
            try:
                results.append(fetch_summary(page, kid["username"], kid["password"], kid["name"]))
            finally:
                page.close()
        browser.close()

    if args.json:
        print(json.dumps([asdict(x) for x in results], ensure_ascii=False, indent=2))
    else:
        print(format_hebrew(results))


if __name__ == "__main__":
    main()
