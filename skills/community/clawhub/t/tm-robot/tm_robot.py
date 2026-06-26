"""
TM Robot API - TMRobot 封装类
使用 techmanpy 连接和控制 OMRON TM 协作机器人

支持：
- SCT 连接（实时控制）
- SVR 连接（状态读取）
- 关节运动、直线运动
- I/O 控制
- 状态监控

📚 TMflow 变量文档：https://docs.tm-robot.com/
"""

import asyncio
import time
import socket
import struct
import logging
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('tm_robot')


# 全局配置
DEFAULT_IP = "192.168.1.13"
DEFAULT_SPEED = 0.1  # 10% 速度
DEFAULT_ACCEL = 50   # 50% 加速度


# ==================== SVR 协议解析 ====================

class SVRParser:
    r"""TMflow SVR 协议解析器"""
    
    def __init__(self, ip: str, port: int = 5891) -> None:
        self.ip: str = ip
        self.port: int = port
        self._sock: Optional[socket.socket] = None
        self._cache: Dict[str, Any] = {}
        self._raw_body: bytes = b''
    
    def connect(self, timeout: float = 5.0) -> bool:
        """建立 SVR 连接（订阅数据流）"""
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.settimeout(timeout)
            self._sock.connect((self.ip, self.port))
            self._sock.send(bytearray([0x01, 0x00, 0x00, 0x00, 0x00]))
            time.sleep(0.3)
            self._receive_and_parse()
            logger.info(f"SVR connected to {self.ip}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"SVR connect failed: {e}")
            return False
    
    def disconnect(self) -> None:
        """断开连接"""
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass
            self._sock = None
        logger.info("SVR disconnected")
    
    def _receive_and_parse(self, max_bytes: int = 8192) -> Dict[str, Any]:
        """接收并解析 SVR 数据包"""
        if not self._sock:
            return {}
        try:
            data = self._sock.recv(max_bytes)
            if not data:
                return {}
            header_end = data.find(b'\n')
            if header_end < 0:
                return {}
            self._raw_body = data[header_end + 1:]
            self._cache = {}
            return self._cache
        except socket.timeout:
            logger.debug("SVR receive timeout")
            return {}
        except Exception as e:
            logger.warning(f"SVR receive error: {e}")
            return {}
    
    def _parse_variable(self, name: str) -> Optional[Any]:
        """解析单个变量"""
        if not self._raw_body:
            return None
        
        idx = self._raw_body.find(name.encode('ascii'))
        if idx < 0:
            return None
        
        name_len = len(name)
        if idx + name_len + 2 >= len(self._raw_body):
            return None
        
        type_code = self._raw_body[idx + name_len]
        data_pos = idx + name_len + 2
        
        try:
            if type_code == 0x01:  # bool
                return self._raw_body[data_pos] != 0
            elif type_code == 0x04:  # int32
                return int.from_bytes(self._raw_body[data_pos:data_pos+4], 'little')
            elif type_code == 0x18:  # 6 floats
                return struct.unpack('<6f', self._raw_body[data_pos:data_pos+24])
            elif type_code == 0x24:  # 9 floats
                return struct.unpack('<9f', self._raw_body[data_pos:data_pos+36])
            elif type_code == 0x0C:  # 3 floats
                return struct.unpack('<3f', self._raw_body[data_pos:data_pos+12])
            elif type_code == 0x08:  # string
                end = self._raw_body.find(b'\x00', data_pos)
                if end > 0:
                    return self._raw_body[data_pos:end].decode('ascii', errors='replace')
        except Exception as e:
            logger.debug(f"Parse {name} failed: {e}")
        
        return None
    
    def get_value(self, name: str, refresh: bool = True) -> Optional[Any]:
        """获取变量值"""
        if refresh:
            self._receive_and_parse()
        if name in self._cache:
            return self._cache[name]
        value = self._parse_variable(name)
        if value is not None:
            self._cache[name] = value
        return value
    
    def get_all(self) -> Dict[str, Any]:
        """获取所有变量"""
        self._receive_and_parse()
        common_vars = [
            'Error_Code', 'Robot_Error', 'Project_Run', 'Project_Pause',
            'Joint_Angle', 'Coord_Robot_Flange', 'Coord_Base_Flange',
            'TCP_Force', 'Joint_Torque', 'Robot_Light', 'Ctrl_DO0', 'Ctrl_DI0'
        ]
        for var in common_vars:
            self.get_value(var, refresh=False)
        return self._cache.copy()


# ==================== 数据类型 ====================

@dataclass
class JointAngles:
    """关节角度（度）"""
    j1: float
    j2: float
    j3: float
    j4: float
    j5: float
    j6: float

    def to_list(self) -> List[float]:
        return [self.j1, self.j2, self.j3, self.j4, self.j5, self.j6]

    def __repr__(self) -> str:
        return f"Joints: {[round(j, 2) for j in self.to_list()]} deg"


@dataclass
class CartesianPose:
    """笛卡尔位姿（mm + 度）"""
    x: float
    y: float
    z: float
    rx: float
    ry: float
    rz: float

    def to_list(self) -> List[float]:
        return [self.x, self.y, self.z, self.rx, self.ry, self.rz]

    def __repr__(self) -> str:
        return f"Pos: [{self.x:.1f}, {self.y:.1f}, {self.z:.1f}]"


@dataclass
class RobotState:
    """机器人状态"""
    connected: bool
    mode: str
    error_code: int
    joints: Optional[JointAngles] = None
    pose: Optional[CartesianPose] = None
    project: Optional[str] = None

    def __repr__(self) -> str:
        return f"Mode:{self.mode} Err:{self.error_code}"


# ==================== 机器人控制类 ====================

class TMRobot:
    """TM 协作机器人控制封装类"""

    def __init__(self, ip: str = DEFAULT_IP, use_custom_svr: bool = True) -> None:
        self.ip: str = ip
        self._sct_client: Optional[Any] = None
        self._svr_client: Optional[Any] = None
        self._sct_conn: Optional[Any] = None
        self._svr_conn: Optional[Any] = None
        self._svr_parser: Optional[SVRParser] = None
        self._use_custom_svr: bool = use_custom_svr
        self._connected: bool = False

    async def connect_sct(self, timeout: float = 5.0) -> bool:
        """建立 SCT 连接（实时控制）"""
        try:
            from techmanpy import connect_sct
            self._sct_client = connect_sct(robot_ip=self.ip, conn_timeout=timeout)
            self._sct_conn = await self._sct_client.__aenter__()
            self._connected = True
            logger.info(f"SCT connected to {self.ip}")
            print(f"[OK] SCT 连接成功 ({self.ip})")
            return True
        except ImportError:
            logger.error("techmanpy not installed")
            print("[错误] techmanpy 未安装：pip install techmanpy")
            return False
        except Exception as e:
            logger.error(f"SCT connect failed: {e}")
            print(f"[错误] SCT 连接失败：{e}")
            return False

    async def connect_svr(self, timeout: float = 5.0) -> bool:
        """建立 SVR 连接（状态读取）"""
        if self._use_custom_svr:
            self._svr_parser = SVRParser(self.ip)
            if self._svr_parser.connect(timeout):
                logger.info(f"SVR connected to {self.ip} (custom parser)")
                print(f"[OK] SVR 连接成功 ({self.ip}, 自定义解析器)")
                return True
            return False
        else:
            try:
                from techmanpy import connect_svr
                self._svr_client = connect_svr(robot_ip=self.ip, conn_timeout=timeout)
                self._svr_conn = await self._svr_client.__aenter__()
                logger.info(f"SVR connected to {self.ip} (techmanpy)")
                print(f"[OK] SVR 连接成功 ({self.ip}, techmanpy)")
                return True
            except Exception as e:
                logger.error(f"SVR connect failed: {e}")
                print(f"[错误] SVR 连接失败：{e}")
                return False

    async def connect_all(self, timeout: float = 5.0) -> bool:
        """同时建立 SCT 和 SVR 连接"""
        sct_ok = await self.connect_sct(timeout)
        svr_ok = await self.connect_svr(timeout)
        return sct_ok and svr_ok

    async def disconnect(self) -> None:
        """断开所有连接"""
        if self._sct_client:
            try:
                await self._sct_client.__aexit__(None, None, None)
            except Exception:
                pass
            self._sct_client = None
            self._sct_conn = None
        
        if self._svr_client:
            try:
                await self._svr_client.__aexit__(None, None, None)
            except Exception:
                pass
            self._svr_client = None
            self._svr_conn = None
        
        if self._svr_parser:
            self._svr_parser.disconnect()
            self._svr_parser = None
        
        self._connected = False
        logger.info("All connections closed")
        print("[信息] 已断开连接")

    async def get_state(self) -> RobotState:
        """读取完整机器人状态"""
        if not self._svr_conn and not self._svr_parser:
            await self.connect_svr()

        state = RobotState(connected=self._connected, mode="Unknown", error_code=0)

        try:
            if self._use_custom_svr:
                state.mode = "Auto" if self._svr_parser.get_value("Project_Run") else "Manual"
                state.error_code = self._svr_parser.get_value("Error_Code") or 0
                joints_data = self._svr_parser.get_value("Joint_Angle")
                pose_data = self._svr_parser.get_value("Coord_Robot_Flange")
            else:
                state.mode = await self._svr_conn.get_value("RobotMode")
                val = await self._svr_conn.get_value("RobotErrCode")
                state.error_code = int(val) if val else 0
                joints_data = await self._svr_conn.get_value("Joint_Angle")
                pose_data = await self._svr_conn.get_value("Pos_Actual")
            
            if joints_data and len(joints_data) >= 6:
                state.joints = JointAngles(*joints_data[:6])
            if pose_data and len(pose_data) >= 6:
                state.pose = CartesianPose(*pose_data[:6])
        except Exception as e:
            logger.warning(f"Get state failed: {e}")

        return state

    async def get_joints(self) -> Optional[JointAngles]:
        """读取当前关节角度"""
        if not self._svr_conn and not self._svr_parser:
            await self.connect_svr()
        try:
            if self._use_custom_svr:
                data = self._svr_parser.get_value("Joint_Angle")
            else:
                data = await self._svr_conn.get_value("Joint_Angle")
            if data and len(data) >= 6:
                return JointAngles(*data[:6])
        except Exception as e:
            logger.warning(f"Get joints failed: {e}")
        return None

    async def get_pose(self) -> Optional[CartesianPose]:
        """读取当前笛卡尔位姿"""
        if not self._svr_conn and not self._svr_parser:
            await self.connect_svr()
        try:
            if self._use_custom_svr:
                data = self._svr_parser.get_value("Coord_Robot_Flange")
            else:
                data = await self._svr_conn.get_value("Pos_Actual")
            if data and len(data) >= 6:
                return CartesianPose(*data[:6])
        except Exception as e:
            logger.warning(f"Get pose failed: {e}")
        return None

    async def move_joint(self, joints: List[float], speed: float = DEFAULT_SPEED, accel: float = DEFAULT_ACCEL) -> bool:
        """关节运动 (PTP)"""
        if not self._sct_conn:
            logger.error("SCT not connected")
            print("[错误] 未建立 SCT 连接")
            return False
        try:
            await self._sct_conn.move_to_joint_angles_ptp(
                joint_angles_goal=joints,
                speed_perc=speed,
                acceleration_duration=accel
            )
            logger.info(f"Move joint: {joints}")
            print(f"[OK] 关节运动：{[round(j, 1) for j in joints]} deg")
            return True
        except Exception as e:
            logger.error(f"Move joint failed: {e}")
            print(f"[错误] 关节运动失败：{e}")
            return False

    async def move_joints_zero(self, speed: float = 0.1) -> bool:
        """移动所有关节到 0 度（回零）"""
        return await self.move_joint([0, 0, 0, 0, 0, 0], speed=speed)

    async def move_relative_line(self, delta: List[float], speed: float = 0.2, accel: float = 50) -> bool:
        """
        笛卡尔空间直线运动（相对运动）
        
        Args:
            delta: [dX, dY, dZ, dRx, dRy, dRz] - 相对位移 (mm, deg)
            speed: 速度百分比 (0.0-1.0)
            accel: 加速度百分比 (0-100)
        
        示例:
            # X 轴正向运动 100mm
            await robot.move_relative_line([100, 0, 0, 0, 0, 0])
            
            # Z 轴下降 50mm
            await robot.move_relative_line([0, 0, -50, 0, 0, 0])
        """
        if not self._sct_conn:
            logger.error("SCT not connected")
            print("[错误] 未建立 SCT 连接")
            return False
        try:
            await self._sct_conn.move_to_relative_point_line(
                relative_point_goal=delta,
                speed=speed,
                acceleration_duration=accel
            )
            logger.info(f"Move relative line: {delta}")
            print(f"[OK] 直线运动：dX={delta[0]:.1f}, dY={delta[1]:.1f}, dZ={delta[2]:.1f} mm")
            return True
        except Exception as e:
            logger.error(f"Move relative line failed: {e}")
            print(f"[错误] 直线运动失败：{e}")
            return False

    async def move_absolute_line(self, target: List[float], speed: float = 0.2, accel: float = 50) -> bool:
        """
        笛卡尔空间直线运动（绝对坐标）
        
        Args:
            target: [X, Y, Z, RX, RY, RZ] - 目标位姿 (mm, deg)
            speed: 速度百分比 (0.0-1.0)
            accel: 加速度百分比 (0-100)
        """
        if not self._sct_conn:
            logger.error("SCT not connected")
            return False
        try:
            # 获取当前位姿，计算相对位移
            current_pose = await self.get_pose()
            if not current_pose:
                print("[错误] 无法读取当前位姿")
                return False
            
            delta = [
                target[0] - current_pose.x,
                target[1] - current_pose.y,
                target[2] - current_pose.z,
                target[3] - current_pose.rx,
                target[4] - current_pose.ry,
                target[5] - current_pose.rz
            ]
            return await self.move_relative_line(delta, speed, accel)
        except Exception as e:
            logger.error(f"Move absolute line failed: {e}")
            return False

    async def move_circle(self, point1: List[float], point2: List[float], speed: float = 0.2, accel: float = 50, arc_angle: float = 0) -> bool:
        """
        圆弧运动
        
        Args:
            point1: [X, Y, Z, RX, RY, RZ] - 圆弧中间点 (mm, deg)
            point2: [X, Y, Z, RX, RY, RZ] - 圆弧终点 (mm, deg)
            speed: 速度百分比 (0.0-1.0)
            accel: 加速度百分比 (0-100)
            arc_angle: 圆弧角度（可选，度）
        
        示例:
            # 从当前位置，经过中间点，到终点画圆弧
            point1 = [500, -100, 400, 180, 0, 90]  # 中间点
            point2 = [500, 0, 400, 180, 0, 90]     # 终点
            await robot.move_circle(point1, point2, speed=0.3)
        """
        if not self._sct_conn:
            logger.error("SCT not connected")
            print("[错误] 未建立 SCT 连接")
            return False
        try:
            await self._sct_conn.move_on_circle(
                tcp_point_1=point1,
                tcp_point_2=point2,
                speed=speed,
                acceleration_duration=accel,
                arc_angle=arc_angle
            )
            logger.info(f"Move circle: via={point1}, end={point2}")
            print(f"[OK] 圆弧运动：中间点 {point1[:3]}, 终点 {point2[:3]}")
            return True
        except Exception as e:
            logger.error(f"Move circle failed: {e}")
            print(f"[错误] 圆弧运动失败：{e}")
            return False

    async def stop_motion(self) -> bool:
        """停止当前运动"""
        if not self._sct_conn:
            return False
        try:
            await self._sct_conn.stop_motion()
            logger.info("Motion stopped")
            return True
        except Exception as e:
            logger.error(f"Stop motion failed: {e}")
            return False

    async def reset_alarm(self) -> bool:
        """复位报警状态"""
        return await self.stop_motion()

    async def set_digital_output(self, pin: int, value: bool) -> bool:
        """设置数字输出"""
        if not self._sct_conn:
            logger.error("SCT not connected")
            return False
        try:
            # techmanpy uses set_output instead of set_digital_output
            if hasattr(self._sct_conn, 'set_output'):
                await self._sct_conn.set_output(pin, value)
            elif hasattr(self._sct_conn, 'set_DO'):
                await self._sct_conn.set_DO(pin, value)
            else:
                # Fallback: try to find any method that works
                logger.warning("No DO method found, trying alternative...")
                return False
            logger.info(f"DO{pin} = {value}")
            print(f"[OK] DO{pin} = {'ON' if value else 'OFF'}")
            return True
        except Exception as e:
            logger.error(f"Set DO{pin} failed: {e}")
            return False

    async def get_digital_input(self, pin: int) -> Optional[bool]:
        """读取数字输入"""
        if not self._svr_conn and not self._svr_parser:
            await self.connect_svr()
        try:
            if self._use_custom_svr:
                value = self._svr_parser.get_value(f"Ctrl_DI{pin}")
            else:
                value = await self._svr_conn.get_value(f"DI{pin}", "")
            return bool(value)
        except Exception:
            return None

    async def __aenter__(self) -> 'TMRobot':
        await self.connect_all()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.disconnect()


# ==================== 快捷函数 ====================

async def connect_robot(ip: str = DEFAULT_IP) -> TMRobot:
    """快速连接机器人"""
    robot = TMRobot(ip)
    await robot.connect_all()
    return robot


# ==================== 命令行工具 ====================

def print_help() -> None:
    """打印帮助信息"""
    print("""
TM Robot CLI - 使用方法

作为模块导入:
    from tm_robot import TMRobot, connect_robot

    async def demo():
        async with TMRobot("192.168.1.13") as robot:
            state = await robot.get_state()
            print(state)

命令行运行:
    python tm_robot.py state    - 读取机器人状态
    python tm_robot.py joints   - 读取关节角度
    python tm_robot.py pose     - 读取笛卡尔位姿
    python tm_robot.py zero     - 回零（所有关节到 0°）
    python tm_robot.py stop     - 停止运动
    python tm_robot.py reset    - 复位报警
""")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)
    
    cmd = sys.argv[1]
    ip = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_IP
    
    async def run_cmd() -> None:
        robot = TMRobot(ip)
        
        if cmd == "state":
            await robot.connect_svr()
            state = await robot.get_state()
            print(state)
        elif cmd == "joints":
            await robot.connect_svr()
            joints = await robot.get_joints()
            print(joints)
        elif cmd == "pose":
            await robot.connect_svr()
            pose = await robot.get_pose()
            print(pose)
        elif cmd == "zero":
            await robot.connect_sct()
            await robot.move_joints_zero()
        elif cmd == "stop":
            await robot.connect_sct()
            await robot.stop_motion()
        elif cmd == "reset":
            await robot.connect_sct()
            await robot.reset_alarm()
        else:
            print(f"未知命令：{cmd}")
            print_help()
        
        await robot.disconnect()
    
    asyncio.run(run_cmd())
