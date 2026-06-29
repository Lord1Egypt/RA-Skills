"""
Billing calculator for time-guru.
Calculates billable amounts per project/customer.
"""
import logging
from typing import Dict, List, Optional
from datetime import date, timedelta
from collections import defaultdict

import store as time_logger

logger = logging.getLogger(__name__)

DATA_DIR = "~/.openclaw/data/time-guru"
CONFIG_FILE = "~/.openclaw/data/time-guru/billing_config.json"


def calculate_bill(entries: list, project_rates: Optional[Dict[str, float]] = None,
                   default_rate: float = 0) -> Dict:
    """
    Calculate billing amounts from time entries.
    
    Args:
        entries: List of time entries.
        project_rates: Dict mapping project names to hourly rates.
        default_rate: Default hourly rate for projects without specific rates.
        
    Returns:
        Billing summary dict.
    """
    if project_rates is None:
        project_rates = {}
    
    # Group billable entries by project
    project_minutes = defaultdict(float)
    
    for e in entries:
        if not e.get("billable", False):
            continue
        proj = e.get("project", "Unspecified")
        project_minutes[proj] += e.get("duration_minutes", 0)
    
    # Calculate amounts
    project_lines = []
    total_amount = 0
    total_billable_hours = 0
    
    for proj, minutes in sorted(project_minutes.items(), key=lambda x: -x[1]):
        hours = minutes / 60
        rate = project_rates.get(proj, default_rate)
        amount = round(hours * rate, 2)
        
        project_lines.append({
            "project": proj,
            "hours": round(hours, 1),
            "rate": rate,
            "amount": amount,
        })
        
        total_amount += amount
        total_billable_hours += hours
    
    return {
        "projects": project_lines,
        "total_billable_hours": round(total_billable_hours, 1),
        "total_amount": round(total_amount, 2),
        "currency": "CNY",
        "entry_count": len([e for e in entries if e.get("billable")]),
    }


def format_billing_summary(bill: Dict) -> str:
    """Format billing calculation as readable text."""
    lines = ["💰 Billing Summary", "=" * 40]
    
    for proj in bill.get("projects", []):
        lines.append(f"\n{proj['project']}:")
        lines.append(f"  {proj['hours']}h × ¥{proj['rate']:.0f}/h = ¥{proj['amount']:,.0f}")
    
    if bill.get("entry_count", 0) > 0:
        lines.extend([
            "",
            "─" * 40,
            f"Total: ¥{bill['total_amount']:,.0f} ({bill['total_billable_hours']}h billable)"
        ])
    else:
        lines.append("\nNo billable entries found.")
    
    return "\n".join(lines)
