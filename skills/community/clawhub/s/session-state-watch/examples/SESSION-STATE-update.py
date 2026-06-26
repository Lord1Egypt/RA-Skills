#!/usr/bin/env python3
"""
Example: How to write SESSION-STATE.md updates from cron tasks.

This pattern allows cron tasks to write results to SESSION-STATE.md,
and the main agent session will automatically detect and read them
via the session-state-watch skill.

Usage:
    from SESSION-STATE-update import write_session_state_update

    result = "**今日学习完成**\\n- 因子权重分析: MA多头 1.5\\n- 持仓检查: 东鹏 OK..."
    write_session_state_update(result, title="梦境学习更新")
"""

import os
import sys
from datetime import datetime

SESSION_STATE_PATH = os.path.expanduser("~/.openclaw/workspace/SESSION-STATE.md")


def write_session_state_update(content: str, title: str = "后台更新") -> bool:
    """
    Append content to SESSION-STATE.md.

    The main session will detect the mtime change and read the new content
    on its next response.

    Args:
        content: Markdown-formatted update text.
        title: Section title for the update block.

    Returns:
        True if write succeeded, False otherwise.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    update_block = f"""
---

## 📡 {title} ({timestamp})

{content}

"""

    try:
        with open(SESSION_STATE_PATH, "a", encoding="utf-8") as f:
            f.write(update_block)
    except (IOError, OSError) as e:
        print(f"[session-state-watch] ERROR: Failed to write to SESSION-STATE.md: {e}", file=sys.stderr)
        return False

    print(f"[session-state-watch] ✓ Written {len(content)} chars to SESSION-STATE.md")
    print(f"[session-state-watch]   Title: {title}")
    print(f"[session-state-watch]   Time: {timestamp}")
    print(f"[session-state-watch]   Main session will detect on next response")
    return True


def write_report(report: str, category: str = "学习") -> bool:
    """
    Convenience function: write a structured learning report.

    Args:
        report: Pre-formatted markdown report text.
        category: Category string (e.g., "梦境学习", "收盘后学习", "选股报告").
    """
    header = f"### 🧠 {category} 报告"
    return write_session_state_update(f"{header}\n\n{report}", title=category)


# --- Example usage ---
if __name__ == "__main__":
    # Dream learning example
    dream_result = """
| 因子 | 前值 | 最新 | 变化 |
|------|------|------|------|
| MA多头 | 1.5 | 1.5 | 持平 |
| 放量 | 1.0 | 1.0 | 持平 |
| 低波动买入 | 1.8 | 1.8 | 持平 |

**结论**: 权重体系稳定，无需调整。
"""
    write_report(dream_result, "梦境学习")

    # Post-market example
    post_market = """
**持仓更新**:
- 东鹏饮料 605499: 25% @ 203.84 ✅ 正常
- 茅台 600519: 20% 等待1343回调 ⏳
- 赤峰黄金 600988: 35% 等待MA10回调40.09 ⏳

**风控检查**: 无异常
"""
    write_report(post_market, "收盘后学习")
