#!/usr/bin/env python3
"""退出站斧客户端（ExitClient）。"""

from __future__ import annotations

import requests

from zhanfu_http import call, clear_opening_malls, configure_stdio, emit, preferred_port


def main() -> int:
    configure_stdio()
    port = preferred_port()
    try:
        data = call("ExitClient", args="", timeout=8, port=port)
    except requests.RequestException:
        print("站斧未打开或无法通讯。")
        return emit({"ok": False, "status": "zhanfu_down"}, 1)
    ro = data.get("returnObj")
    clear_opening_malls()
    print(f"已退出站斧。returnObj={ro!r}")
    return emit({"ok": True, "status": "exited", "returnObj": ro}, 0)


if __name__ == "__main__":
    raise SystemExit(main())
