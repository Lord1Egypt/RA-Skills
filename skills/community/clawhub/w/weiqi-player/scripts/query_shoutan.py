#!/usr/bin/env python3
"""
手谈等级分查询 - 性能计时版（修复多同名选手问题）
查询围棋选手的手谈等级分、排名等信息
支持显示多个同名选手

使用方法:
    python3 query_shoutan.py 张三
    python3 query_shoutan.py 李四
    python3 query_shoutan.py 王五
"""

import sys
import base64
import time
import requests
from contextlib import contextmanager
from collections import OrderedDict

import re





# ===== 性能计时工具 =====
class PerformanceTimer:
    """性能计时器 - 追踪每个步骤的执行耗时"""
    def __init__(self):
        self.timings = OrderedDict()
        self.start_time = None
    
    def start(self):
        """开始总计时"""
        self.start_time = time.time()
        return self
    
    @contextmanager
    def step(self, name):
        """上下文管理器 - 计时单个步骤"""
        step_start = time.time()
        try:
            yield self
        finally:
            elapsed = time.time() - step_start
            self.timings[name] = elapsed
    
    def get_total(self):
        """获取总耗时"""
        if self.start_time:
            return time.time() - self.start_time
        return 0
    
    def format_report(self):
        """格式化计时报告"""
        lines = []
        lines.append("\n" + "="*50)
        lines.append("⏱️  性能计时报告（手谈查询）")
        lines.append("="*50)
        
        total_step_time = 0
        for name, elapsed in self.timings.items():
            total_step_time += elapsed
            lines.append(f"  {name:20s} : {elapsed:>8.3f}s")
        
        lines.append("-"*50)
        lines.append(f"  {'步骤累计':20s} : {total_step_time:>8.3f}s")
        lines.append(f"  {'总耗时':20s} : {self.get_total():>8.3f}s")
        lines.append("="*50)
        return "\n".join(lines)


def fetch_url(url, timeout=30):
    """获取URL内容"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(url, headers=headers, timeout=timeout)
    return response.text


def parse_shoutan_basic(html, name):
    """
    解析手谈基本信息HTML
    支持多个同名选手
    """
    players = []
    
    # 从DataTxt提取所有选手信息
    data_match = re.search(r'DataTxt = \'([^\']+)\'', html)
    if data_match:
        data_content = data_match.group(1)
        # 查找所有Xs标签（在<PkList>内）
        xs_matches = re.findall(r'<Xs ([^>]+)/>', data_content)
        
        for xs_attrs in xs_matches:
            info = {
                '姓名': name,
                '编号': None,
                'Yh': None,
                '等级分': None,
                '省份': None,
                '地区': None,
                '对局次数': None,
                '参赛次数': None,
                '注册日期': None,
                '注册等级分': None,
                '全国排名': None,
                '省份排名': None,
                '地区排名': None,
                '称谓': None,
            }
            
            # 提取各个属性
            info['编号'] = re.search(r'编号="(\d+)"', xs_attrs).group(1) if re.search(r'编号="(\d+)"', xs_attrs) else None
            info['等级分'] = re.search(r'等级分="([\d.]+)"', xs_attrs).group(1) if re.search(r'等级分="([\d.]+)"', xs_attrs) else None
            info['省份'] = re.search(r'省份="([^"]+)"', xs_attrs).group(1) if re.search(r'省份="([^"]+)"', xs_attrs) else None
            info['地区'] = re.search(r'地区="([^"]+)"', xs_attrs).group(1) if re.search(r'地区="([^"]+)"', xs_attrs) else None
            info['对局次数'] = re.search(r'对局次数="(\d+)"', xs_attrs).group(1) if re.search(r'对局次数="(\d+)"', xs_attrs) else None
            info['参赛次数'] = re.search(r'参赛次数="(\d+)"', xs_attrs).group(1) if re.search(r'参赛次数="(\d+)"', xs_attrs) else None
            info['注册日期'] = re.search(r'注册日期="([^"]+)"', xs_attrs).group(1) if re.search(r'注册日期="([^"]+)"', xs_attrs) else None
            info['注册等级分'] = re.search(r'注册等级分="([\d.]+)"', xs_attrs).group(1) if re.search(r'注册等级分="([\d.]+)"', xs_attrs) else None
            info['全国排名'] = re.search(r'全国排名="(\d+)"', xs_attrs).group(1) if re.search(r'全国排名="(\d+)"', xs_attrs) else None
            info['省份排名'] = re.search(r'省份排名="(\d+)"', xs_attrs).group(1) if re.search(r'省份排名="(\d+)"', xs_attrs) else None
            info['地区排名'] = re.search(r'地区排名="(\d+)"', xs_attrs).group(1) if re.search(r'地区排名="(\d+)"', xs_attrs) else None
            info['称谓'] = re.search(r'称谓="([^"]+)"', xs_attrs).group(1) if re.search(r'称谓="([^"]+)"', xs_attrs) else None
            
            players.append(info)
    
    # 从RediTxt提取Yh（所有选手共用同一个Yh）
    redi_match = re.search(r'var RediTxt = \'<Redi[^>]+Yh="(\d+)"[^>]*/>\'', html)
    if redi_match and players:
        yh = redi_match.group(1)
        for player in players:
            player['Yh'] = yh
    
    return players


def query_shoutan_detail(player, timer):
    """
    查询手谈详细比赛记录
    
    Args:
        player: 选手信息字典（包含编号和Yh）
        timer: 性能计时器实例
    """
    base_url = "https://v.dzqzd.com/SpBody.aspx"
    
    # 构造详细查询
    with timer.step(f"查询详细记录({player['姓名']}-{player['地区']})"):
        xml = f'<Redi Ns="Sp" Jk="等级分明细" Yh="{player["Yh"]}" 选手号="{player["编号"]}"/>'
        encoded = base64.b64encode(xml.encode('utf-8')).decode('utf-8')
        url = f"{base_url}?r={encoded}"
        
        try:
            html = fetch_url(url)
        except Exception as e:
            print(f"  ❌ 详细记录查询失败: {e}")
            return None
    
    # 检查是否有错误
    if '系统信息' in html or 'sysError' in html or '未将对象引用' in html:
        return None
    
    # 尝试解析对局记录（简化版）
    return url  # 返回链接供用户自行查看


def query_shoutan(name, timer):
    """
    查询手谈等级分（支持多同名选手）
    
    Args:
        name: 选手姓名
        timer: 性能计时器实例
    
    Returns:
        list: 选手信息列表（可能包含多个同名选手）
    """
    base_url = "https://v.dzqzd.com/SpBody.aspx"
    
    # 步骤1: 构造查询参数
    with timer.step("构造查询参数"):
        xml = f'<Redi Ns="Sp" Jk="选手查询" 姓名="{name}"/>'
        encoded = base64.b64encode(xml.encode('utf-8')).decode('utf-8')
        url = f"{base_url}?r={encoded}"
    
    # 步骤2: 发送HTTP请求
    with timer.step("HTTP请求"):
        print(f"🌐 查询手谈等级分: {name}")
        try:
            html = fetch_url(url)
        except Exception as e:
            print(f"❌ 查询失败: {e}")
            return []
    
    # 步骤3: 解析HTML内容
    with timer.step("解析HTML"):
        players = parse_shoutan_basic(html, name)
    
    return players


def format_player_info_single_line(player):
    """格式化单个选手信息为单行 Markdown 格式"""
    parts = []
    parts.append(f"**{player['姓名']}** ({player['地区']})")
    
    if player.get('称谓'):
        parts.append(f"段位: {player['称谓']}")
    if player.get('等级分'):
        parts.append(f"等级分: {player['等级分']}")
    if player.get('全国排名'):
        parts.append(f"全国排名: {player['全国排名']}")
    if player.get('对局次数'):
        parts.append(f"对局: {player['对局次数']}局")
    
    return " | ".join(parts)


def format_output(players, timer):
    """格式化输出结果 - 单行 Markdown 格式"""
    name = players[0]['姓名'] if players else '未知'
    print(f"\n📋 **{name}** - 手谈等级分查询结果\n")
    
    if len(players) > 1:
        print(f"⚠️ 找到 {len(players)} 位同名选手\n")
    
    for i, player in enumerate(players, 1):
        if len(players) > 1:
            print(f"{i}. {format_player_info_single_line(player)}")
        else:
            print(format_player_info_single_line(player))
        
        # 生成详细记录链接
        xml_detail = f'<Redi Ns="Sp" Jk="等级分明细" Yh="{player["Yh"]}" 选手号="{player["编号"]}"/>'
        encoded_detail = base64.b64encode(xml_detail.encode('utf-8')).decode('utf-8')
        detail_url = f"https://v.dzqzd.com/SpBody.aspx?r={encoded_detail}"
        display_name = player['地区']
        print(f"   👉 [查看{display_name}详细记录]({detail_url})\n")
    
    # 输出性能报告
    print(timer.format_report())


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n用法: python3 query_shoutan.py <姓名>")
        print("示例: python3 query_shoutan.py 张三")
        sys.exit(1)
    
    name = sys.argv[1]
    
    # 创建计时器并启动
    timer = PerformanceTimer()
    timer.start()
    
    # 执行查询
    players = query_shoutan(name, timer)
    
    if players:
        format_output(players, timer)
    else:
        print(f"\n❌ 未找到选手 '{name}' 的信息")
        print(timer.format_report())


if __name__ == "__main__":
    main()
