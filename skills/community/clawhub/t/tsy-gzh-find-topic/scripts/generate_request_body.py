#!/usr/bin/env python3
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


TZ = ZoneInfo("Asia/Shanghai")


def main() -> None:
    now = datetime.now(TZ)
    start = (now - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0)

    body = {
        "likeOutlierValue": "3",
        "publishStartDate": str(int(start.timestamp() * 1000)),
        "publishEndDate": str(int(now.timestamp() * 1000)),
    }

    print(json.dumps(body, ensure_ascii=False))


if __name__ == "__main__":
    main()
