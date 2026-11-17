# -*- coding: utf-8 -*-
"""
双色球数据源 - huiniao API
免费无限制，支持HTTPS，返回JSON
API: http://api.huiniao.top/interface/home/lotteryHistory?type=ssq&page=1&limit=100

双色球字段映射:
  one..six : 红球 6 个 (1-33)
  seven    : 蓝球 1 个 (1-16)
  code     : 期号, 如 2026089
  day      : 开奖日期 YYYY-MM-DD
"""
import json
import urllib.request
import urllib.error


def fetch_huiniao_ssq(page=1, limit=100):
    """从huiniao API获取双色球历史数据

    Returns:
        list of dict: [{period, date, front:[6], back:[1]}, ...]
    """
    url = f"http://api.huiniao.top/interface/home/lotteryHistory?type=ssq&page={page}&limit={limit}"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })

    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode('utf-8'))

    if data.get('code') != 1:
        raise ValueError(f"API返回错误: {data.get('info')}")

    items = data['data']['data']['list']
    results = []

    for item in items:
        front = [int(item[k]) for k in ('one', 'two', 'three', 'four', 'five', 'six')]
        front.sort()
        back = [int(item['seven'])]
        results.append({
            'period': item['code'],
            'date': item['day'],
            'front': front,
            'back': back,
            'open_time': item.get('open_time', '')
        })

    return results


def fetch_all_huiniao(total_pages=None):
    """获取全部双色球历史数据

    Returns:
        list: 全部历史数据，按期号升序
    """
    if total_pages is None:
        first_batch = fetch_huiniao_ssq(page=1, limit=100)
        url = "http://api.huiniao.top/interface/home/lotteryHistory?type=ssq&page=1&limit=100"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        total_pages = int(data['data']['data']['totalPage'])
        print(f"  总页数: {total_pages}, 总记录: {data['data']['data']['totalCount']}")

        all_data = list(first_batch)
        for p in range(2, total_pages + 1):
            batch = fetch_huiniao_ssq(page=p, limit=100)
            all_data.extend(batch)
            if p % 10 == 0:
                print(f"  已获取 {p}/{total_pages} 页, {len(all_data)} 期")
    else:
        all_data = []
        for p in range(1, total_pages + 1):
            batch = fetch_huiniao_ssq_batch(p, 100)
            all_data.extend(batch)

    all_data.sort(key=lambda x: x['period'])
    return all_data


def fetch_huiniao_ssq_batch(page, limit=100):
    """别名, 与 fetch_huiniao_ssq 同义 (供 fetch_all_huiniao 调用)"""
    return fetch_huiniao_ssq(page=page, limit=limit)


def fetch_latest_huiniao(limit=20):
    """获取最新N期数据（用于增量更新校验）"""
    data = fetch_huiniao_ssq(page=1, limit=limit)
    data.sort(key=lambda x: x['period'])
    return data


def merge_huiniao_with_existing(existing_data, new_data):
    """合并huiniao数据与现有数据，保留更完整的"""
    existing_periods = {d['period'] for d in existing_data}
    merged = list(existing_data)
    added = 0
    for item in new_data:
        if item['period'] not in existing_periods:
            merged.append(item)
            added += 1
    merged.sort(key=lambda x: x['period'])
    if added > 0:
        print(f"  huiniao新增 {added} 期数据")
    else:
        print(f"  huiniao数据与现有数据一致，无新增")
    return merged


if __name__ == '__main__':
    print("测试huiniao双色球API...")
    latest = fetch_latest_huiniao(limit=5)
    for item in latest:
        print(f"  {item['period']} ({item['date']}): 红球={item['front']} 蓝球={item['back']}")
    print(f"\n最新期号: {latest[-1]['period']}")
