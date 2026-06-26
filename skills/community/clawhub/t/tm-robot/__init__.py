"""
TM Robot Skill - 达明机器人控制技能
Techman Robot (OMROM TM5) Control Skill

使用 techmanpy SDK 连接和控制 TM 协作机器人
"""

from .tm_robot import TMRobot, connect_robot

__version__ = "1.0.0"
__author__ = "RobotQu / JMO"

__all__ = ["TMRobot", "connect_robot"]
