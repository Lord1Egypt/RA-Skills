#!/usr/bin/env python3
"""
野狐围棋 - 通过昵称下载棋谱
支持：昵称查UID → 获取棋谱列表 → 下载SGF

用法:
    python3 download_by_name.py <昵称> [--limit N] [--output-dir DIR]
    python3 download_by_name.py 星阵谈兵
    python3 download_by_name.py 星阵谈兵 --limit 10 --output-dir /tmp/qipu

注意：本脚本通过平台提供的公开API获取数据，仅供个人学习研究使用。
"""

import sys
import os
import json
import re
import urllib.request
import urllib.parse
import time

# API 配置（来源：开源项目 GetFoxRequest.java）
QUERY_USER_URL = "https://newframe.foxwq.com/cgi/QueryUserInfoPanel"
CHESS_LIST_URL = "https://h5.foxwq.com/yehuDiamond/chessbook_local/YHWQFetchChessList"
FETCH_CHESS_URL = "https://h5.foxwq.com/yehuDiamond/chessbook_local/YHWQFetchChess"
MOBILE_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15"


def http_get(url, timeout=20):
    """发送HTTP GET请求"""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", MOBILE_USER_AGENT)
    req.add_header("Accept", "application/json,text/plain,*/*")
    
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode('utf-8')


def query_user_by_name(nickname):
    """
    通过昵称查询用户信息
    
    调用平台的用户查询接口，根据昵称获取UID等基本信息。
    需要提供正确的 API 端点才能正常工作。
    """
    encoded_name = urllib.parse.quote(nickname)
    # 构造请求URL：srcuid=0 表示游客身份查询
    url = f"{QUERY_USER_URL}?srcuid=0&username={encoded_name}"
    
    response = http_get(url)
    data = json.loads(response)
    
    if data.get("result") != 0:
        error_msg = data.get("resultstr") or data.get("errmsg") or "未知错误"
        raise Exception(f"查询用户失败: {error_msg}")
    
    uid = str(data.get("uid", "")).strip()
    if not uid:
        raise Exception("未找到该昵称对应的UID")
    
    return {
        "uid": uid,
        "nickname": data.get("username") or data.get("name") or data.get("englishname") or nickname,
        "dan": data.get("dan", 0),
        "total_win": data.get("totalwin", 0),
        "total_lost": data.get("totallost", 0),
        "total_equal": data.get("totalequal", 0),
    }


def fetch_chess_list(uid, lastcode="0"):
    """
    获取棋谱列表
    
    调用平台的棋谱列表接口，获取指定用户的公开对局记录。
    type=1 表示查询类型，lastcode 用于分页。
    """
    encoded_uid = urllib.parse.quote(uid)
    # 构造请求URL：type=1 表示获取对局列表
    url = f"{CHESS_LIST_URL}?srcuid=0&dstuid={encoded_uid}&type=1&lastcode={lastcode}&searchkey=&uin={encoded_uid}"
    
    response = http_get(url)
    data = json.loads(response)
    
    if data.get("result") != 0:
        error_msg = data.get("resultstr") or "获取棋谱列表失败"
        raise Exception(error_msg)
    
    return data.get("chesslist", [])


def fetch_sgf(chessid):
    """
    下载单局SGF
    
    根据棋谱ID获取SGF格式的棋谱数据。
    """
    url = f"{FETCH_CHESS_URL}?chessid={chessid}"
    
    response = http_get(url)
    data = json.loads(response)
    
    if data.get("result") != 0:
        raise Exception(f"下载棋谱失败: {data.get('resultstr', '未知错误')}")
    
    return data.get("chess", "")


def format_dan(dan_value):
    """格式化段位显示"""
    if dan_value >= 100:
        return f"职业{dan_value - 100}段"
    elif dan_value >= 24:
        return f"业{dan_value - 20}段"
    elif dan_value >= 20:
        return f"业{dan_value - 20}段"
    elif dan_value >= 10:
        return f"{dan_value - 10}级"
    else:
        return f"{dan_value}级"


def parse_result(winner, point, reason):
    """
    解析对局结果
    
    参数说明:
    - winner: 1=黑胜, 2=白胜, 0=和棋
    - point: 胜子数（数子胜时有效）
    - reason: 1=数子胜, 2=超时, 3=中盘胜, 4=认输
    """
    if winner == 0:
        return "和棋"
    
    winner_str = "黑胜" if winner == 1 else "白胜"
    
    if reason == 1:
        if point > 0:
            return f"{winner_str} {point}子"
        return winner_str
    elif reason == 2:
        return f"{winner_str} (超时)"
    elif reason == 3:
        return f"{winner_str} (中盘)"
    elif reason == 4:
        return f"{winner_str} (认输)"
    else:
        return winner_str


# 工具函数


def main():
    if len(sys.argv) < 2:
        print("用法: python3 download_by_name.py <昵称> [--limit N] [--output-dir DIR]")
        print("示例: python3 download_by_name.py 星阵谈兵")
        print("      python3 download_by_name.py 星阵谈兵 --limit 5 --output-dir /tmp/qipu")
        sys.exit(1)
    
    nickname = sys.argv[1]
    limit = None
    output_dir = "/tmp/foxwq_by_name"
    
    # 解析参数
    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == "--limit" and i + 1 < len(sys.argv):
            try:
                limit = int(sys.argv[i + 1])
            except ValueError:
                pass
        elif arg == "--output-dir" and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]
    
    print("=" * 60)
    print("🎯 野狐围棋 - 通过昵称下载棋谱")
    print("=" * 60)
    print()
    
    start_time = time.time()
    
    # 1. 查询用户信息
    print(f"🔍 正在查询昵称: {nickname} ...")
    try:
        user_info = query_user_by_name(nickname)
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        sys.exit(1)
    
    uid = user_info["uid"]
    print(f"✅ 找到用户!")
    print(f"   UID: {uid}")
    print(f"   昵称: {user_info['nickname']}")
    print(f"   段位: {format_dan(user_info['dan'])}")
    print(f"   战绩: {user_info['total_win']}胜 {user_info['total_lost']}负 {user_info['total_equal']}和")
    print()
    
    # 2. 获取棋谱列表
    print("📋 正在获取棋谱列表...")
    try:
        chess_list = fetch_chess_list(uid)
    except Exception as e:
        print(f"❌ 获取棋谱列表失败: {e}")
        sys.exit(1)
    
    if not chess_list:
        print("⚠️ 该用户没有公开的棋谱")
        sys.exit(0)
    
    total_games = len(chess_list)
    print(f"✅ 找到 {total_games} 盘棋谱")
    print()
    
    # 3. 显示棋谱列表
    print("=" * 60)
    print("📊 棋谱列表 (最近{}盘)".format(limit if limit else total_games))
    print("=" * 60)
    print()
    
    games_to_show = chess_list[:limit] if limit else chess_list
    
    for idx, game in enumerate(games_to_show, 1):
        chessid = game.get("chessid", "")
        black_nick = game.get("blacknick", "黑棋")
        white_nick = game.get("whitenick", "白棋")
        black_dan = format_dan(game.get("blackdan", 0))
        white_dan = format_dan(game.get("whitedan", 0))
        start_time_str = game.get("starttime", "未知")
        movenum = game.get("movenum", 0)
        winner = game.get("winner", 0)
        point = game.get("point", 0)
        reason = game.get("reason", 0)
        result = parse_result(winner, point, reason)
        
        print(f"{idx}. [{start_time_str}] {black_nick}({black_dan}) vs {white_nick}({white_dan})")
        print(f"   结果: {result} | 手数: {movenum} | ID: {chessid}")
        print()
    
    # 4. 询问是否下载
    if sys.stdin.isatty():  # 交互模式
        response = input("💾 是否下载以上棋谱? (y/n): ").strip().lower()
        if response != 'y':
            print("已取消下载")
            return
    
    # 5. 下载棋谱
    print()
    print("=" * 60)
    print("⬇️  开始下载棋谱...")
    print("=" * 60)
    print()
    
    os.makedirs(output_dir, exist_ok=True)
    success_count = 0
    failed_list = []
    
    for idx, game in enumerate(games_to_show, 1):
        chessid = game.get("chessid", "")
        start_time_str = game.get("starttime", "unknown").replace(" ", "_").replace(":", "-")
        
        # 生成文件名
        safe_nickname = re.sub(r'[^\w\u4e00-\u9fff]', '_', nickname)
        filename = f"{idx:03d}_{safe_nickname}_{start_time_str}_{chessid}.sgf"
        filepath = os.path.join(output_dir, filename)
        
        print(f"[{idx}/{len(games_to_show)}] 下载 {chessid} ...", end=" ")
        
        try:
            sgf_content = fetch_sgf(chessid)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(sgf_content)
            print(f"✅ 已保存: {filename}")
            success_count += 1
            time.sleep(0.2)  # 避免请求过快
        except Exception as e:
            print(f"❌ 失败: {e}")
            failed_list.append((chessid, str(e)))
    
    # 6. 报告
    elapsed = time.time() - start_time
    print()
    print("=" * 60)
    print("📈 下载报告")
    print("=" * 60)
    print(f"   用户: {nickname} (UID: {uid})")
    print(f"   保存目录: {output_dir}")
    print(f"   成功: {success_count}/{len(games_to_show)}")
    print(f"   耗时: {elapsed:.2f}秒")
    
    if failed_list:
        print()
        print("❌ 下载失败列表:")
        for chessid, error in failed_list:
            print(f"   - {chessid}: {error}")
    
    print()
    print("✅ 完成!")


if __name__ == "__main__":
    main()
