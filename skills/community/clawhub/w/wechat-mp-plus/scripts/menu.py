#!/usr/bin/env python3
"""菜单管理 - 查询、创建、删除自定义菜单"""

import json
import sys
from wechat_mp import get_access_token, _http_get, _http_post_json, _api_error


def get_menu():
    """查询当前菜单"""
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token={token}"
    data = _http_get(url)
    if "errcode" in data and data["errcode"] != 0:
        _api_error(data)
        return None
    is_open = data.get("is_menu_open", 0)
    print(f"📋 菜单状态: {'已开启' if is_open else '未开启'}")
    info = data.get("selfmenu_info", {})
    buttons = info.get("button", [])
    for btn in buttons:
        name = btn.get("name", "未命名")
        btype = btn.get("type", "")
        sub = btn.get("sub_button", {}).get("list", [])
        if sub:
            print(f"  📁 {name}")
            for s in sub:
                print(f"    - {s.get('name', '')} [{s.get('type', '')}]")
        else:
            print(f"  🔘 {name} [{btype}]")
    return data


def create_menu(menu_data):
    """创建菜单。menu_data: {"button": [...]}"""
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/menu/create?access_token={token}"
    data = _http_post_json(url, menu_data)
    if _api_error(data):
        return False
    print("✅ 菜单创建成功")
    return True


def delete_menu():
    """删除菜单"""
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/menu/delete?access_token={token}"
    data = _http_get(url)
    if _api_error(data):
        return False
    print("✅ 菜单已删除")
    return True


def main():
    if len(sys.argv) < 2:
        print("用法: menu.py <命令> [参数]")
        print("命令: get, create <json>, delete")
        print()
        print("示例JSON:")
        print(json.dumps({"button": [
            {"type": "click", "name": "今日歌曲", "key": "V1001_TODAY_MUSIC"},
            {"type": "view", "name": "官网", "url": "https://example.com"},
            {"name": "更多", "sub_button": [
                {"type": "click", "name": "帮助", "key": "HELP"},
            ]},
        ]}, ensure_ascii=False, indent=2))
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "get":
        get_menu()
    elif cmd == "create":
        menu_data = json.loads(sys.argv[2])
        create_menu(menu_data)
    elif cmd == "delete":
        delete_menu()
    else:
        print(f"未知命令: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
