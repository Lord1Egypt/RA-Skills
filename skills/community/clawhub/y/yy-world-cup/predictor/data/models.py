"""
数据模型定义模块
定义比赛中使用的所有数据结构：比赛信息、伤病、天气、球队等
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum


class TeamStyle(Enum):
    """球队战术风格"""
    TECHNICAL = "technical"  # 技术型
    PHYSICAL = "physical"    # 身体型
    DEFENSIVE = "defensive"  # 防守型
    ATTACKING = "attacking"  # 进攻型
    BALANCED = "balanced"    # 平衡型
    COUNTER = "counter_attack"  # 反击型
    LONG_BALL = "long_ball"  # 长传冲吊型


class Position(Enum):
    """球员位置"""
    GK = "GK"  # 守门员
    DF = "DF"  # 后卫
    MF = "MF"  # 中场
    FW = "FW"  # 前锋


class WeatherCondition(Enum):
    """天气状况"""
    SUNNY = "晴"
    CLOUDY = "多云"
    OVERCAST = "阴"
    RAINY = "雨"
    SNOWY = "雪"
    FOGGY = "雾"


@dataclass
class Team:
    """球队信息"""
    id: int
    name: str
    abbreviation: str
    country_code: str
    confederation: str
    elo: int = 1700
    style: TeamStyle = TeamStyle.BALANCED


@dataclass
class Stadium:
    """球场信息"""
    id: int
    name: str
    city: str
    country: str
    capacity: int
    latitude: float = 0.0
    longitude: float = 0.0


@dataclass
class InjuryInfo:
    """伤病信息"""
    player_name: str
    is_starter: bool
    playing_probability: float  # 0-1.0
    position: Position
    impact_score: float = 0.0  # 影响评分


@dataclass
class WeatherInfo:
    """天气信息"""
    temperature: float  # 摄氏度
    precipitation_probability: float  # 0-100%
    wind_level: int  # 风力等级
    weather_condition: WeatherCondition
    humidity: float = 50.0  # 湿度


@dataclass
class RecentMatch:
    """近期比赛记录"""
    result: str  # "win" / "draw" / "loss"
    goals: int
    conceded: int
    opponent_elo: int = 1700
    is_home: bool = True


@dataclass
class MatchInfo:
    """比赛基础信息"""
    match_id: Optional[int]
    home_team: Team
    away_team: Team
    match_time: str
    stadium: Stadium
    stage: str = "group"  # group/knockout/quarter/semi/final
    is_neutral: bool = False  # 是否中立球场（世界杯、欧洲杯等通常为True）
    home_goals_per_match: float = 1.5
    away_goals_per_match: float = 1.0
    home_conceded_per_match: float = 1.0
    away_conceded_per_match: float = 1.5
    home_recent: List[RecentMatch] = field(default_factory=list)
    away_recent: List[RecentMatch] = field(default_factory=list)
    home_injuries: List[InjuryInfo] = field(default_factory=list)
    away_injuries: List[InjuryInfo] = field(default_factory=list)
    weather: Optional[WeatherInfo] = None
    group_standings_home: Optional[Dict] = None
    group_standings_away: Optional[Dict] = None


@dataclass
class PredictionResult:
    """预测结果"""
    home_win_prob: float
    draw_prob: float
    away_win_prob: float
    predicted_scores: List[tuple]  # [(score_str, probability), ...]
    total_goals_prob: List[tuple]  # [(goals, probability), ...]
    ht_ft_probs: Dict[str, float]  # 半全场概率
    predict_mode: str  # "爆冷模式" / "平衡模式"


@dataclass
class BettingStrategy:
    """购票策略"""
    strategy_name: str
    risk_level: str
    suggested_bet_ratio: str
    play_types: List[Dict]
    expected_win_rate: float
    expected_odds: float
    expected_value: float  # 预期收益
