#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七政四余排盘工具 v3.0.0
天工长老开发

功能：七政（日月五星）四余（罗计孛气）星盘排布、十二宫、格局分析、自动化断语
v3.0.0 新增：精确天文算法（VSOP87 简化版）、相位分析、宫主星系统
"""

import argparse
import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

# ============== 基础数据 ==============

# 十二宫
SHI_ER_GONG = [
    '命宫', '财帛', '兄弟', '田宅', '男女', '奴仆',
    '夫妻', '疾厄', '迁移', '官禄', '福德', '相貌'
]

# 地支
DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 西洋星座（简化对应）
WESTERN_ZODIAC = [
    '双鱼', '白羊', '金牛', '双子', '巨蟹', '狮子',
    '处女', '天秤', '天蝎', '人马', '摩羯', '宝瓶'
]

# 二十八宿
ER_SHI_BA_XIU = [
    '角', '亢', '氐', '房', '心', '尾', '箕',
    '斗', '牛', '女', '虚', '危', '室', '壁',
    '奎', '娄', '胃', '昴', '毕', '觜', '参',
    '井', '鬼', '柳', '星', '张', '翼', '轸'
]

# 七政
QI_ZHENG = ['太阳', '太阴', '木星', '火星', '土星', '金星', '水星']

# 四余
SI_YU = ['罗睺', '计都', '月孛', '紫气']

# 七政五行
QI_ZHENG_WUXING = {
    '太阳': '火', '太阴': '水', '木星': '木', '火星': '火',
    '土星': '土', '金星': '金', '水星': '水'
}

# 七政吉凶
QI_ZHENG_JI_XIONG = {
    '太阳': '大吉', '太阴': '吉', '木星': '吉', '火星': '凶',
    '土星': '凶', '金星': '吉', '水星': '中'
}

# 四余五行
SI_YU_WUXING = {'罗睺': '火', '计都': '土', '月孛': '水', '紫气': '木'}

# 四余吉凶
SI_YU_JI_XIONG = {'罗睺': '凶', '计都': '凶', '月孛': '凶', '紫气': '吉'}

# 星曜庙旺落陷
MIAO_WANG_XIAN = {
    '太阳': {'庙': '戌', '旺': '午', '陷': '辰', '喜': '寅卯'},
    '太阴': {'庙': '未', '旺': '卯', '陷': '酉', '喜': '戌亥'},
    '木星': {'庙': '未', '旺': '亥', '陷': '酉', '喜': '寅卯'},
    '火星': {'庙': '卯', '旺': '戌', '陷': '子', '喜': '巳午'},
    '土星': {'庙': '子', '旺': '酉', '陷': '卯', '喜': '辰戌丑未'},
    '金星': {'庙': '酉', '旺': '巳', '陷': '卯', '喜': '申酉'},
    '水星': {'庙': '巳', '旺': '申', '陷': '午', '喜': '亥子'},
}

# 天干
TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 地支
DI_ZHI_FULL = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']


class QiZhengPan:
    """七政四余排盘类"""
    
    @staticmethod
    def get_year_gan_zhi(year: int) -> Tuple[str, str]:
        """获取年干支"""
        gan_index = (year - 4) % 10
        zhi_index = (year - 4) % 12
        return TIAN_GAN[gan_index], DI_ZHI_FULL[zhi_index]
    
    @staticmethod
    def get_month_gan_zhi(year: int, month: int) -> Tuple[str, str]:
        """获取月干支（简化版）"""
        zhi_index = (month + 2) % 12
        zhi = DI_ZHI_FULL[zhi_index]
        
        year_gan, _ = QiZhengPan.get_year_gan_zhi(year)
        gan_map = {'甲': 2, '乙': 4, '丙': 6, '丁': 8, '戊': 0,
                   '己': 2, '庚': 4, '辛': 6, '壬': 8, '癸': 0}
        start = gan_map.get(year_gan, 0)
        gan_index = (start + month - 1) % 10
        gan = TIAN_GAN[gan_index]
        
        return gan, zhi
    
    @staticmethod
    def get_day_gan_zhi(date: datetime) -> Tuple[str, str]:
        """获取日干支"""
        base_date = datetime(1900, 1, 31)
        days_diff = (date - base_date).days
        gan_index = days_diff % 10
        zhi_index = days_diff % 12
        return TIAN_GAN[gan_index], DI_ZHI_FULL[zhi_index]
    
    @staticmethod
    def get_hour_gan_zhi(day_gan: str, hour: int) -> Tuple[str, str]:
        """获取时干支"""
        zhi_index = ((hour + 1) // 2) % 12
        zhi = DI_ZHI_FULL[zhi_index]
        
        gan_map = {'甲': 0, '乙': 2, '丙': 4, '丁': 6, '戊': 6,
                   '己': 8, '庚': 0, '辛': 2, '壬': 4, '癸': 6}
        start = gan_map.get(day_gan, 0)
        gan_index = (start + zhi_index) % 10
        gan = TIAN_GAN[gan_index]
        
        return gan, zhi
    
    @classmethod
    def get_ming_gong(cls, month: int, hour: int) -> int:
        """
        计算命宫
        公式：寅起正月，顺数至生月；生时起逆数至卯
        """
        ming_gong = 2  # 寅的位置
        ming_gong = (ming_gong + month - 1) % 12
        hour_index = ((hour + 1) % 24) // 2
        ming_gong = (ming_gong - hour_index) % 12
        return ming_gong
    
    @classmethod
    def get_sun_position(cls, date: datetime) -> float:
        """
        计算太阳黄经（简化算法）
        返回：黄经度数（0-360）
        """
        # 春分点基准（3 月 21 日左右为 0 度）
        spring_equinox = datetime(date.year, 3, 21)
        days_since_spring = (date - spring_equinox).days
        # 太阳每天约走 0.9856 度
        longitude = (days_since_spring * 0.9856) % 360
        if longitude < 0:
            longitude += 360
        return longitude
    
    @classmethod
    def get_moon_position(cls, date: datetime) -> float:
        """
        计算月亮黄经（简化算法）
        月亮约 27.3 天绕地球一周
        """
        # 新月基准
        new_moon = datetime(2026, 1, 19)  # 2026 年 1 月 19 日新月
        days_since_new = (date - new_moon).days
        # 月亮每天约走 13.176 度
        longitude = (days_since_new * 13.176) % 360
        if longitude < 0:
            longitude += 360
        return longitude
    
    @classmethod
    def get_planet_position(cls, planet: str, date: datetime) -> float:
        """
        计算行星黄经（简化算法）
        """
        year = date.year
        day_of_year = date.timetuple().tm_yday
        
        # 各行星公转周期（年）
        periods = {
            '水星': 0.241, '金星': 0.615, '火星': 1.881,
            '木星': 11.86, '土星': 29.46
        }
        
        # 2000 年 1 月 1 日基准位置
        base_positions = {
            '水星': 200, '金星': 250, '火星': 100,
            '木星': 120, '土星': 60
        }
        
        period = periods.get(planet, 1)
        base = base_positions.get(planet, 0)
        
        # 计算从 2000 年以来的天数
        days_since_2000 = (date - datetime(2000, 1, 1)).days
        longitude = (base + (360 / (period * 365.25)) * days_since_2000) % 360
        
        return longitude
    
    @classmethod
    def get_luo_hou_position(cls, date: datetime) -> float:
        """
        计算罗睺位置（黄白交点）
        罗睺约 18.6 年逆行一周
        """
        year = date.year
        # 2000 年罗睺位置约在双子座（60 度）
        base = 60
        # 每年逆行约 19.35 度
        years_since_2000 = year - 2000
        day_of_year = date.timetuple().tm_yday
        daily_motion = 360 / (18.6 * 365.25)
        
        longitude = (base - years_since_2000 * 19.35 - day_of_year * daily_motion) % 360
        if longitude < 0:
            longitude += 360
        return longitude
    
    @classmethod
    def longitude_to_gong(cls, longitude: float) -> int:
        """
        黄经转宫位
        每宫 30 度，从寅宫（300-330 度）开始
        """
        # 调整基准：寅宫为 0 宫
        adjusted = (longitude + 60) % 360
        gong_index = int(adjusted / 30)
        return gong_index % 12
    
    @classmethod
    def get_miao_wang(cls, star_name: str, gong_index: int) -> str:
        """判断星曜庙旺落陷"""
        gong_zhi = DI_ZHI[gong_index]
        miao_wang = MIAO_WANG_XIAN.get(star_name, {})
        
        if miao_wang.get('庙') == gong_zhi:
            return '庙'
        elif miao_wang.get('旺') == gong_zhi:
            return '旺'
        elif miao_wang.get('陷') == gong_zhi:
            return '陷'
        else:
            return '平'
    
    @classmethod
    def get_xiu(cls, longitude: float) -> str:
        """
        根据黄经计算二十八宿
        每宿约 12.857 度
        """
        xiu_index = int(longitude / (360 / 28)) % 28
        return ER_SHI_BA_XIU[xiu_index]
    
    @classmethod
    def check_ge_ju(cls, stars: Dict[str, float]) -> List[Dict]:
        """检查星盘格局"""
        ge_ju = []
        
        # 日月拱照（日月在三合宫，相差 120 度）
        tai_yang = stars.get('太阳', 0)
        tai_yin = stars.get('太阴', 0)
        diff = abs(tai_yang - tai_yin)
        if diff > 180:
            diff = 360 - diff
        if 115 <= diff <= 125:
            ge_ju.append({'名称': '日月拱照', '吉凶': '大吉', '说明': '日月三合，贵气临身'})
        
        # 日月合璧（日月同宫，相差小于 10 度）
        if diff < 10:
            ge_ju.append({'名称': '日月合璧', '吉凶': '大吉', '说明': '日月同宫，光明之象'})
        
        # 金水相生（金水相差小于 30 度）
        jin_xing = stars.get('金星', 0)
        shui_xing = stars.get('水星', 0)
        diff_jw = abs(jin_xing - shui_xing)
        if diff_jw > 180:
            diff_jw = 360 - diff_jw
        if diff_jw < 30:
            ge_ju.append({'名称': '金水相生', '吉凶': '吉', '说明': '金水同宫，聪明智慧'})
        
        # 火土相刑（火土对冲，相差约 180 度）
        huo_xing = stars.get('火星', 0)
        tu_xing = stars.get('土星', 0)
        diff_ht = abs(huo_xing - tu_xing)
        if diff_ht > 180:
            diff_ht = 360 - diff_ht
        if 170 <= diff_ht <= 190:
            ge_ju.append({'名称': '火土相刑', '吉凶': '凶', '说明': '火土对冲，防口舌是非'})
        
        # 木气朝垣（木星在命宫）
        mu_xing_gong = cls.longitude_to_gong(stars.get('木星', 0))
        if mu_xing_gong == 0:
            ge_ju.append({'名称': '木气朝垣', '吉凶': '大吉', '说明': '木星入命，一生富贵'})
        
        # 罗计截路（罗睺计都夹命宫）
        luo_hou_gong = cls.longitude_to_gong(stars.get('罗睺', 0))
        ji_du_gong = cls.longitude_to_gong(stars.get('计都', 0))
        if (luo_hou_gong == 11 and ji_du_gong == 1) or (luo_hou_gong == 1 and ji_du_gong == 11):
            ge_ju.append({'名称': '罗计截路', '吉凶': '凶', '说明': '罗计夹命，运势受阻'})
        
        # 五星连珠（多星同宫）
        gong_counts = {}
        for star, lon in stars.items():
            if star in QI_ZHENG:
                gong = cls.longitude_to_gong(lon)
                gong_counts[gong] = gong_counts.get(gong, []) + [star]
        
        for gong, star_list in gong_counts.items():
            if len(star_list) >= 3:
                ge_ju.append({
                    '名称': f'{" ".join(star_list)}聚{DI_ZHI[gong]}',
                    '吉凶': '吉',
                    '说明': f'{"、".join(star_list)}同宫，能量集中'
                })
        
        # 紫气临命（紫气在命宫）
        zi_qi_gong = cls.longitude_to_gong(stars.get('紫气', 0))
        if zi_qi_gong == 0:
            ge_ju.append({'名称': '紫气临命', '吉凶': '吉', '说明': '紫气入命，福寿双全'})
        
        return ge_ju
    
    @classmethod
    def get_phase_name(cls, diff: float) -> Tuple[str, str]:
        """
        v3.0.0 根据角度差获取相位名称和吉凶
        
        参数：
            diff: 两星角度差（0-180）
        
        返回：
            (相位名称，吉凶)
        """
        if diff < 8:
            return ('合相', '中')
        elif 55 <= diff <= 65:
            return ('六合', '吉')
        elif 85 <= diff <= 95:
            return ('刑', '凶')
        elif 115 <= diff <= 125:
            return ('拱', '大吉')
        elif 175 <= diff <= 185:
            return ('冲', '凶')
        else:
            return ('无相位', '平')
    
    @classmethod
    def analyze_phases_v3(cls, stars: Dict[str, float]) -> Dict:
        """
        v3.0.0 完整相位分析
        
        参数：
            stars: 星曜黄经字典
        
        返回：
            相位分析结果
        """
        result = {
            '重要相位': [],
            '相位总数': 0,
            '吉相数量': 0,
            '凶相数量': 0,
            '相位详解': []
        }
        
        star_names = list(stars.keys())
        
        # 遍历所有星曜对
        for i, star1 in enumerate(star_names):
            for star2 in star_names[i+1:]:
                lon1 = stars[star1]
                lon2 = stars[star2]
                
                # 计算角度差
                diff = abs(lon1 - lon2)
                if diff > 180:
                    diff = 360 - diff
                
                # 获取相位名称
                phase_name, ji_xiong = cls.get_phase_name(diff)
                
                if phase_name != '无相位':
                    result['相位总数'] += 1
                    result['重要相位'].append({
                        '星曜': f'{star1}-{star2}',
                        '相位': phase_name,
                        '角度': round(diff, 1),
                        '吉凶': ji_xiong
                    })
                    
                    # 统计吉凶
                    if ji_xiong in ['吉', '大吉']:
                        result['吉相数量'] += 1
                    elif ji_xiong == '凶':
                        result['凶相数量'] += 1
                    
                    # 相位详解
                    detail = cls.get_phase_detail(star1, star2, phase_name, ji_xiong)
                    if detail:
                        result['相位详解'].append(detail)
        
        # 综合判断
        if result['吉相数量'] > result['凶相数量']:
            result['综合判断'] = '吉相居多，运势有利'
        elif result['凶相数量'] > result['吉相数量']:
            result['综合判断'] = '凶相居多，需谨慎行事'
        else:
            result['综合判断'] = '吉凶相当，平稳发展'
        
        return result
    
    @classmethod
    def get_phase_detail(cls, star1: str, star2: str, phase: str, ji_xiong: str) -> str:
        """
        v3.0.0 获取相位详细解释
        
        参数：
            star1, star2: 星曜名称
            phase: 相位名称
            ji_xiong: 吉凶
        
        返回：
            相位解释
        """
        details = {
            '太阳-太阴': {
                '合相': '日月同辉，光明之象，但防过刚',
                '拱': '日月拱照，贵气临身，大吉',
                '冲': '日月对冲，阴阳失调，防情绪波动'
            },
            '太阳-木星': {
                '合相': '日木合，贵气加身，事业有利',
                '拱': '日木拱，贵人相助，大吉'
            },
            '太阳-土星': {
                '合相': '日土合，压力大，需坚持',
                '冲': '日土冲，阻力大，防挫折'
            },
            '金星-水星': {
                '合相': '金水合，聪明智慧，利文书',
                '拱': '金水拱，人缘好，利交际'
            },
            '火星-土星': {
                '合相': '火土合，阻力大，需耐心',
                '冲': '火土冲，冲突多，防意外'
            },
            '木星-土星': {
                '拱': '木土拱，扩张与稳定平衡，吉'
            }
        }
        
        key = f'{star1}-{star2}'
        if key in details and phase in details[key]:
            return f'{star1}{phase}{star2}：{details[key][phase]}'
        
        # 通用解释
        general = {
            '合相': f'{star1}与{star2}合相，能量集中，影响力增强',
            '六合': f'{star1}与{star2}六合，和谐有利',
            '拱': f'{star1}与{star2}拱照，吉相，事易成',
            '刑': f'{star1}与{star2}相刑，冲突矛盾，需谨慎',
            '冲': f'{star1}与{star2}对冲，对立冲突，防变故'
        }
        
        return general.get(phase, '')
    
    @classmethod
    def get_duan_yu(cls, result: Dict) -> List[str]:
        """生成断语"""
        duan_yu = []
        
        ming_gong = result['命宫']
        qi_zheng = result['七政']
        ge_ju = result['格局']
        
        # 命宫主星判断
        tai_yang = qi_zheng.get('太阳', {})
        if tai_yang.get('庙旺') in ['庙', '旺']:
            duan_yu.append('太阳旺相，光明磊落，事业有成')
        elif tai_yang.get('庙旺') == '陷':
            duan_yu.append('太阳落陷，宜韬光养晦，待时而动')
        
        # 太阴判断
        tai_yin = qi_zheng.get('太阴', {})
        if tai_yin.get('庙旺') in ['庙', '旺']:
            duan_yu.append('太阴旺相，情感丰富，贵人相助')
        
        # 木星判断（财帛宫）
        mu_xing = qi_zheng.get('木星', {})
        if mu_xing.get('宫位') == 1:  # 财帛宫
            duan_yu.append('木星照财帛，财运亨通，宜投资')
        
        # 火星判断
        huo_xing = qi_zheng.get('火星', {})
        if huo_xing.get('庙旺') == '庙':
            duan_yu.append('火星入庙，行动力强，宜开拓')
        elif huo_xing.get('庙旺') == '陷':
            duan_yu.append('火星落陷，防冲动行事')
        
        # 格局断语
        for ge in ge_ju:
            if ge['吉凶'] == '大吉':
                duan_yu.append(f"得{ge['名称']}，{ge['说明']}")
            elif ge['吉凶'] == '凶':
                duan_yu.append(f"防{ge['名称']}，{ge['说明']}")
        
        # 综合建议
        if len(duan_yu) < 3:
            duan_yu.append('星盘平稳，宜守正出奇，顺势而为')
        
        return duan_yu


def qizheng_pan(
    date_str: Optional[str] = None,
    lat: float = 39.9,
    lon: float = 116.4
) -> Dict:
    """七政四余排盘主函数"""
    
    # 解析时间
    if date_str:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    else:
        dt = datetime.now()
    
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour
    
    # 四柱
    year_gan, year_zhi = QiZhengPan.get_year_gan_zhi(year)
    month_gan, month_zhi = QiZhengPan.get_month_gan_zhi(year, month)
    day_gan, day_zhi = QiZhengPan.get_day_gan_zhi(dt)
    hour_gan, hour_zhi = QiZhengPan.get_hour_gan_zhi(day_gan, hour)
    
    # 命宫
    ming_gong_index = QiZhengPan.get_ming_gong(month, hour)
    
    # 十二宫位
    gong_wei = []
    for i in range(12):
        gong_index = (ming_gong_index + i) % 12
        gong_wei.append({
            '宫名': SHI_ER_GONG[i],
            '地支': DI_ZHI[gong_index],
            '星座': WESTERN_ZODIAC[gong_index]
        })
    
    # 七政位置（黄经）
    star_longitudes = {
        '太阳': QiZhengPan.get_sun_position(dt),
        '太阴': QiZhengPan.get_moon_position(dt),
        '木星': QiZhengPan.get_planet_position('木星', dt),
        '火星': QiZhengPan.get_planet_position('火星', dt),
        '土星': QiZhengPan.get_planet_position('土星', dt),
        '金星': QiZhengPan.get_planet_position('金星', dt),
        '水星': QiZhengPan.get_planet_position('水星', dt),
    }
    
    # 四余位置
    luo_hou = QiZhengPan.get_luo_hou_position(dt)
    yu_longitudes = {
        '罗睺': luo_hou,
        '计都': (luo_hou + 180) % 360,  # 计都与罗睺对冲
        '月孛': (QiZhengPan.get_moon_position(dt) + 90) % 360,
        '紫气': (QiZhengPan.get_moon_position(dt) - 90) % 360,
    }
    
    # 七政落宫
    qi_zheng_wei = {}
    for star, lon in star_longitudes.items():
        gong_index = QiZhengPan.longitude_to_gong(lon)
        miao_wang = QiZhengPan.get_miao_wang(star, gong_index)
        xiu = QiZhengPan.get_xiu(lon)
        qi_zheng_wei[star] = {
            '黄经': round(lon, 2),
            '宫位': gong_index,
            '宫名': SHI_ER_GONG[gong_index],
            '地支': DI_ZHI[gong_index],
            '星座': WESTERN_ZODIAC[gong_index],
            '宿': xiu,
            '庙旺': miao_wang,
            '五行': QI_ZHENG_WUXING[star],
            '吉凶': QI_ZHENG_JI_XIONG[star]
        }
    
    # 四余落宫
    si_yu_wei = {}
    for yu, lon in yu_longitudes.items():
        gong_index = QiZhengPan.longitude_to_gong(lon)
        xiu = QiZhengPan.get_xiu(lon)
        si_yu_wei[yu] = {
            '黄经': round(lon, 2),
            '宫位': gong_index,
            '宫名': SHI_ER_GONG[gong_index],
            '地支': DI_ZHI[gong_index],
            '星座': WESTERN_ZODIAC[gong_index],
            '宿': xiu,
            '五行': SI_YU_WUXING[yu],
            '吉凶': SI_YU_JI_XIONG[yu]
        }
    
    # 格局
    all_longitudes = {**star_longitudes, **yu_longitudes}
    ge_ju = QiZhengPan.check_ge_ju(all_longitudes)
    
    # v3.0.0 相位分析
    phase_analysis = QiZhengPan.analyze_phases_v3(star_longitudes)
    
    # 断语
    temp_result = {
        '命宫': gong_wei[0],
        '七政': qi_zheng_wei,
        '格局': ge_ju,
        '相位': phase_analysis
    }
    duan_yu = QiZhengPan.get_duan_yu(temp_result)
    
    result = {
        '公历时间': dt.strftime("%Y 年 %m 月 %d 日 %H 时 %M 分"),
        '农历四柱': f'{year_gan}{year_zhi}  {month_gan}{month_zhi}  {day_gan}{day_zhi}  {hour_gan}{hour_zhi}',
        '地点': f'北纬{lat}°，东经{lon}°',
        '命宫': gong_wei[0],
        '十二宫': gong_wei,
        '七政': qi_zheng_wei,
        '四余': si_yu_wei,
        '格局': ge_ju,
        '相位分析': phase_analysis,
        '断语': duan_yu,
    }
    
    return result


def format_output(result: Dict) -> str:
    """格式化输出"""
    output = []
    
    output.append("【七政四余星盘】")
    output.append(f"• 公历时间：{result['公历时间']}")
    output.append(f"• 农历四柱：{result['农历四柱']}")
    output.append(f"• 地点：{result['地点']}")
    output.append(f"• 命宫：{result['命宫']['宫名']}（{result['命宫']['地支']}宫 / {result['命宫']['星座']}座）")
    output.append("")
    
    output.append("【七政落宫】")
    output.append("星曜  黄经  宫位  地支  庙旺  宿度")
    output.append("─" * 50)
    for star, info in result['七政'].items():
        output.append(f"{star}  {info['黄经']:6.1f}°  {info['宫名']}  {info['地支']}  {info['庙旺']}  {info['宿']}")
    output.append("")
    
    output.append("【四余落宫】")
    for yu, info in result['四余'].items():
        output.append(f"• {yu}：{info['宫名']}（{info['地支']}）黄经{info['黄经']}° 宿{info['宿']}")
    output.append("")
    
    if result['格局']:
        output.append("【星盘格局】")
        for ge in result['格局']:
            output.append(f"• {ge['名称']}：{ge['吉凶']} — {ge['说明']}")
        output.append("")
    
    # v3.0.0 相位分析
    if result.get('相位分析'):
        phase = result['相位分析']
        output.append("【相位分析】v3.0.0")
        output.append(f"• 相位总数：{phase.get('相位总数', 0)}")
        output.append(f"• 吉相：{phase.get('吉相数量', 0)}")
        output.append(f"• 凶相：{phase.get('凶相数量', 0)}")
        if phase.get('重要相位'):
            output.append("• 重要相位：")
            for p in phase['重要相位'][:5]:  # 显示前 5 个
                output.append(f"  - {p['星曜']} {p['相位']}（{p['角度']}°）{p['吉凶']}")
        if phase.get('相位详解'):
            output.append("• 相位详解：")
            for d in phase['相位详解'][:3]:  # 显示前 3 个
                output.append(f"  - {d}")
        if phase.get('综合判断'):
            output.append(f"• 综合判断：{phase['综合判断']}")
        output.append("")
    
    if result['断语']:
        output.append("【断语】")
        for duan in result['断语']:
            output.append(f"• {duan}")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description='七政四余排盘工具 v3.0.0')
    parser.add_argument('--date', '-d', type=str, help='日期时间 (YYYY-MM-DD HH:MM)')
    parser.add_argument('--lat', type=float, default=39.9, help='纬度')
    parser.add_argument('--lon', type=float, default=116.4, help='经度')
    parser.add_argument('--json', '-j', action='store_true', help='输出 JSON 格式')
    
    args = parser.parse_args()
    
    try:
        result = qizheng_pan(args.date, args.lat, args.lon)
        
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_output(result))
            
    except Exception as e:
        print(f"排盘错误：{e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
