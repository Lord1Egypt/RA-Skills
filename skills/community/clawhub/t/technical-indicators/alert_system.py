"""
实时预警系统
支持价格预警、指标预警、量价预警、形态预警
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class AlertType(Enum):
    """预警类型枚举"""
    PRICE = "price"          # 价格预警：突破阻力/支撑、创新高/新低
    INDICATOR = "indicator"  # 指标预警：MACD/KDJ/RSI 金叉死叉
    VOLUME = "volume"        # 量价预警：异常放量(量比>3)、异常缩量
    PATTERN = "pattern"      # 形态预警：K线形态完成


@dataclass
class AlertSignal:
    """预警信号数据类"""
    symbol: str              # 股票代码
    alert_type: AlertType    # 预警类型
    signal_name: str         # 信号名称
    current_value: float     # 当前值
    threshold: float         # 阈值
    direction: str           # 方向：'up', 'down'
    timestamp: datetime      # 时间戳
    additional_info: Dict[str, Any] = None  # 额外信息


class TechnicalAlertSystem:
    """技术面实时预警系统"""
    
    def __init__(self):
        self.alert_signals = []
        self.subscribers = []  # 订阅者列表
        self.is_running = False
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        """设置日志"""
        logger = logging.getLogger('TechnicalAlertSystem')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
    def subscribe(self, callback_func):
        """订阅预警信号"""
        self.subscribers.append(callback_func)
        self.logger.info(f"新增订阅者: {callback_func.__name__}")
    
    def unsubscribe(self, callback_func):
        """取消订阅预警信号"""
        if callback_func in self.subscribers:
            self.subscribers.remove(callback_func)
            self.logger.info(f"移除订阅者: {callback_func.__name__}")
    
    async def send_alert(self, signal: AlertSignal):
        """发送预警信号"""
        self.logger.info(f"触发预警: {signal.symbol} - {signal.signal_name}")
        
        # 保存预警信号
        self.alert_signals.append(signal)
        
        # 通知所有订阅者
        for subscriber in self.subscribers:
            try:
                if asyncio.iscoroutinefunction(subscriber):
                    await subscriber(signal)
                else:
                    subscriber(signal)
            except Exception as e:
                self.logger.error(f"通知订阅者失败 {subscriber.__name__}: {str(e)}")
    
    def check_price_alerts(self, symbol: str, current_price: float, 
                          resistance: float = None, support: float = None,
                          high_20d: float = None, low_20d: float = None) -> List[AlertSignal]:
        """检查价格预警"""
        signals = []
        now = datetime.now()
        
        # 检查阻力位突破
        if resistance and current_price >= resistance:
            signal = AlertSignal(
                symbol=symbol,
                alert_type=AlertType.PRICE,
                signal_name="阻力位突破",
                current_value=current_price,
                threshold=resistance,
                direction="up",
                timestamp=now,
                additional_info={"break_type": "resistance"}
            )
            signals.append(signal)
        
        # 检查支撑位跌破
        if support and current_price <= support:
            signal = AlertSignal(
                symbol=symbol,
                alert_type=AlertType.PRICE,
                signal_name="支撑位跌破",
                current_value=current_price,
                threshold=support,
                direction="down",
                timestamp=now,
                additional_info={"break_type": "support"}
            )
            signals.append(signal)
        
        # 检查创20日新高
        if high_20d and current_price >= high_20d:
            signal = AlertSignal(
                symbol=symbol,
                alert_type=AlertType.PRICE,
                signal_name="创20日新高",
                current_value=current_price,
                threshold=high_20d,
                direction="up",
                timestamp=now,
                additional_info={"break_type": "new_high_20d"}
            )
            signals.append(signal)
        
        # 检查创20日新低
        if low_20d and current_price <= low_20d:
            signal = AlertSignal(
                symbol=symbol,
                alert_type=AlertType.PRICE,
                signal_name="创20日新低",
                current_value=current_price,
                threshold=low_20d,
                direction="down",
                timestamp=now,
                additional_info={"break_type": "new_low_20d"}
            )
            signals.append(signal)
        
        return signals
    
    def check_indicator_alerts(self, symbol: str, 
                              macd_golden_cross: bool = False,
                              macd_death_cross: bool = False,
                              kdj_golden_cross: bool = False,
                              kdj_death_cross: bool = False,
                              rsi_overbought: bool = False,  # RSI > 70
                              rsi_oversold: bool = False     # RSI < 30
                             ) -> List[AlertSignal]:
        """检查指标预警"""
        signals = []
        now = datetime.now()
        
        if macd_golden_cross:
            signal = AlertSignal(
                symbol=symbol,
                alert_type=AlertType.INDICATOR,
                signal_name="MACD金叉",
                current_value=0,
                threshold=0,
                direction="up",
                timestamp=now,
                additional_info={"indicator": "macd", "cross_type": "golden"}
            )
            signals.append(signal)
        
        if macd_death_cross:
            signal = AlertSignal(
                symbol=symbol,
                alert_type=AlertType.INDICATOR,
                signal_name="MACD死叉",
                current_value=0,
                threshold=0,
                direction="down",
                timestamp=now,
                additional_info={"indicator": "macd", "cross_type": "death"}
            )
            signals.append(signal)
        
        if kdj_golden_cross:
            signal = AlertSignal(
                symbol=symbol,
                alert_type=AlertType.INDICATOR,
                signal_name="KDJ金叉",
                current_value=0,
                threshold=0,
                direction="up",
                timestamp=now,
                additional_info={"indicator": "kdj", "cross_type": "golden"}
            )
            signals.append(signal)
        
        if kdj_death_cross:
            signal = AlertSignal(
                symbol=symbol,
                alert_type=AlertType.INDICATOR,
                signal_name="KDJ死叉",
                current_value=0,
                threshold=0,
                direction="down",
                timestamp=now,
                additional_info={"indicator": "kdj", "cross_type": "death"}
            )
            signals.append(signal)
        
        if rsi_overbought:
            signal = AlertSignal(
                symbol=symbol,
                alert_type=AlertType.INDICATOR,
                signal_name="RSI超买",
                current_value=70,
                threshold=70,
                direction="up",
                timestamp=now,
                additional_info={"indicator": "rsi", "condition": "overbought"}
            )
            signals.append(signal)
        
        if rsi_oversold:
            signal = AlertSignal(
                symbol=symbol,
                alert_type=AlertType.INDICATOR,
                signal_name="RSI超卖",
                current_value=30,
                threshold=30,
                direction="down",
                timestamp=now,
                additional_info={"indicator": "rsi", "condition": "oversold"}
            )
            signals.append(signal)
        
        return signals
    
    def check_volume_alerts(self, symbol: str, volume_ratio: float,
                           is_abnormal_shrinkage: bool = False) -> List[AlertSignal]:
        """检查量价预警"""
        signals = []
        now = datetime.now()
        
        # 检查异常放量 (量比>3)
        if volume_ratio > 3:
            signal = AlertSignal(
                symbol=symbol,
                alert_type=AlertType.VOLUME,
                signal_name="异常放量",
                current_value=volume_ratio,
                threshold=3,
                direction="up",
                timestamp=now,
                additional_info={"volume_ratio": volume_ratio}
            )
            signals.append(signal)
        
        # 检查异常缩量
        if is_abnormal_shrinkage:
            signal = AlertSignal(
                symbol=symbol,
                alert_type=AlertType.VOLUME,
                signal_name="异常缩量",
                current_value=volume_ratio,
                threshold=0.5,  # 假设缩量阈值为0.5
                direction="down",
                timestamp=now,
                additional_info={"volume_ratio": volume_ratio, "condition": "shrinkage"}
            )
            signals.append(signal)
        
        return signals
    
    def check_pattern_alerts(self, symbol: str, pattern_name: str,
                            is_completed: bool = True) -> List[AlertSignal]:
        """检查形态预警"""
        signals = []
        now = datetime.now()
        
        if is_completed:
            signal = AlertSignal(
                symbol=symbol,
                alert_type=AlertType.PATTERN,
                signal_name=f"{pattern_name}形态完成",
                current_value=0,
                threshold=0,
                direction="neutral",
                timestamp=now,
                additional_info={"pattern_name": pattern_name}
            )
            signals.append(signal)
        
        return signals
    
    async def process_alerts(self, symbol: str, market_data: Dict[str, Any]):
        """处理单个股票的所有预警"""
        all_signals = []
        
        # 检查价格预警
        price_signals = self.check_price_alerts(
            symbol=symbol,
            current_price=market_data.get('current_price'),
            resistance=market_data.get('resistance'),
            support=market_data.get('support'),
            high_20d=market_data.get('high_20d'),
            low_20d=market_data.get('low_20d')
        )
        all_signals.extend(price_signals)
        
        # 检查指标预警
        indicator_signals = self.check_indicator_alerts(
            symbol=symbol,
            macd_golden_cross=market_data.get('macd_golden_cross', False),
            macd_death_cross=market_data.get('macd_death_cross', False),
            kdj_golden_cross=market_data.get('kdj_golden_cross', False),
            kdj_death_cross=market_data.get('kdj_death_cross', False),
            rsi_overbought=market_data.get('rsi_overbought', False),
            rsi_oversold=market_data.get('rsi_oversold', False)
        )
        all_signals.extend(indicator_signals)
        
        # 检查量价预警
        volume_signals = self.check_volume_alerts(
            symbol=symbol,
            volume_ratio=market_data.get('volume_ratio', 1.0),
            is_abnormal_shrinkage=market_data.get('is_abnormal_shrinkage', False)
        )
        all_signals.extend(volume_signals)
        
        # 检查形态预警
        if market_data.get('pattern_name'):
            pattern_signals = self.check_pattern_alerts(
                symbol=symbol,
                pattern_name=market_data['pattern_name'],
                is_completed=market_data.get('pattern_completed', False)
            )
            all_signals.extend(pattern_signals)
        
        # 发送所有预警信号
        for signal in all_signals:
            await self.send_alert(signal)
    
    async def start_monitoring(self):
        """开始监控"""
        self.is_running = True
        self.logger.info("开始实时预警监控...")
        
        while self.is_running:
            try:
                # 这里应该从数据源获取实时数据
                # 示例数据，实际应用中应替换为真实的数据源
                sample_data = {
                    'symbol': '000001',
                    'current_price': 10.5,
                    'resistance': 10.4,
                    'support': 10.0,
                    'high_20d': 10.6,
                    'low_20d': 9.8,
                    'macd_golden_cross': False,
                    'macd_death_cross': True,
                    'kdj_golden_cross': True,
                    'kdj_death_cross': False,
                    'rsi_overbought': False,
                    'rsi_oversold': False,
                    'volume_ratio': 3.5,
                    'is_abnormal_shrinkage': False,
                    'pattern_name': '锤子线',
                    'pattern_completed': True
                }
                
                await self.process_alerts(sample_data['symbol'], sample_data)
                
                # 模拟等待下一轮监控
                await asyncio.sleep(60)  # 每分钟检查一次
                
            except Exception as e:
                self.logger.error(f"监控过程中出错: {str(e)}")
                await asyncio.sleep(10)  # 出错后等待10秒再继续
    
    def stop_monitoring(self):
        """停止监控"""
        self.is_running = False
        self.logger.info("已停止实时预警监控")


# 飞书消息推送相关功能
class FeishuPusher:
    """飞书消息推送器"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    async def send_message(self, signal: AlertSignal):
        """发送预警消息到飞书"""
        import aiohttp
        
        # 构建消息内容
        message = self._build_alert_message(signal)
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.webhook_url, json=message) as resp:
                    if resp.status == 200:
                        print(f"飞书消息发送成功: {signal.signal_name}")
                    else:
                        print(f"飞书消息发送失败: {resp.status}")
            except Exception as e:
                print(f"发送飞书消息异常: {str(e)}")
    
    def _build_alert_message(self, signal: AlertSignal):
        """构建预警消息"""
        content = f"""
【实时预警】
股票代码: {signal.symbol}
预警类型: {signal.alert_type.value}
信号名称: {signal.signal_name}
当前值: {signal.current_value}
触发时间: {signal.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        return {
            "msg_type": "text",
            "content": {
                "text": content
            }
        }


async def main():
    """主函数 - 示例用法"""
    # 创建预警系统实例
    alert_system = TechnicalAlertSystem()
    
    # 创建飞书推送器实例（需要替换为真实的webhook地址）
    # feishu_pusher = FeishuPusher(webhook_url="YOUR_FEISHU_WEBHOOK_URL")
    # alert_system.subscribe(feishu_pusher.send_message)
    
    # 添加一个简单的控制台输出订阅者用于演示
    def console_output(signal: AlertSignal):
        print(f"[ALERT] {signal.symbol}: {signal.signal_name} at {signal.timestamp}")
    
    alert_system.subscribe(console_output)
    
    try:
        # 启动监控
        await alert_system.start_monitoring()
    except KeyboardInterrupt:
        print("\n收到停止信号，正在关闭...")
        alert_system.stop_monitoring()


if __name__ == "__main__":
    asyncio.run(main())