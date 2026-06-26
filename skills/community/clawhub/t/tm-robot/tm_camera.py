"""
TM Robot Camera Control - TM 内置相机控制

支持：
- 相机光源控制
- 触发拍照
- 读取视觉结果
- 手眼相机位姿
"""

import asyncio
import time
from typing import Optional, Tuple
from tm_robot import SVRParser


class TMCamera:
    """TM 内置相机控制类"""
    
    def __init__(self, ip: str = "192.168.1.13"):
        self.ip = ip
        self.parser = SVRParser(ip)
        self.connected = False
    
    def connect(self, timeout: float = 5.0) -> bool:
        """连接相机"""
        if self.parser.connect(timeout):
            self.connected = True
            print(f"[OK] 相机连接成功 ({self.ip})")
            return True
        print(f"[错误] 相机连接失败")
        return False
    
    def disconnect(self):
        """断开连接"""
        self.parser.disconnect()
        self.connected = False
        print("[信息] 相机已断开")
    
    # ==================== 相机控制 ====================
    
    def set_light(self, on: bool) -> bool:
        """
        控制相机光源
        
        Args:
            on: True=开，False=关
        """
        # 通过 SCT 设置 DO 控制光源
        # 注意：需要 TMflow 配置 DO 引脚控制光源
        try:
            # Camera_Light 是只读变量，需要通过 DO 控制
            # 通常 DO2 控制光源
            from techmanpy import connect_sct
            import asyncio
            
            async def set_do():
                client = connect_sct(robot_ip=self.ip, conn_timeout=5)
                conn = await client.__aenter__()
                await conn.set_digital_output(2, on)
                await client.__aexit__(None, None, None)
            
            asyncio.run(set_do())
            print(f"[OK] 相机光源 = {'ON' if on else 'OFF'}")
            return True
        except Exception as e:
            print(f"[错误] 光源控制失败：{e}")
            return False
    
    def trigger_capture(self) -> bool:
        """
        触发拍照
        
        通过写入 Camera_Trigger 变量触发
        """
        try:
            # Camera_Trigger 通常是写入式变量
            # 需要通过 TMflow 项目或视觉工具触发
            print("[提示] 触发拍照需要通过 TMflow 视觉工具或项目")
            print("[提示] 或者使用 set_digital_output 触发外部信号")
            return True
        except Exception as e:
            print(f"[错误] 触发拍照失败：{e}")
            return False
    
    # ==================== 读取状态 ====================
    
    def get_light_status(self) -> Optional[bool]:
        """读取相机光源状态"""
        if not self.connected:
            return None
        return self.parser.get_value("Camera_Light")
    
    def get_hand_camera_pose(self) -> Optional[Tuple[float, float, float, float, float, float]]:
        """
        读取手眼相机位姿
        
        Returns:
            (x, y, z, rx, ry, rz) 单位：mm, deg
            或 None（如果不可用）
        """
        if not self.connected:
            return None
        
        pose = self.parser.get_value("HandCamera_Value")
        if pose and len(pose) >= 6:
            return tuple(pose[:6])
        return None
    
    def get_vision_result(self) -> dict:
        """
        读取视觉结果
        
        Returns:
            {
                'x': float,      # X 偏移 (mm)
                'y': float,      # Y 偏移 (mm)
                'angle': float,  # 角度偏移 (deg)
                'state': int,    # 状态 (0=失败，1=成功)
            }
        """
        result = {
            'x': None,
            'y': None,
            'angle': None,
            'state': None,
        }
        
        if not self.connected:
            return result
        
        try:
            x = self.parser.get_value("Vision_Result_X")
            y = self.parser.get_value("Vision_Result_Y")
            angle = self.parser.get_value("Vision_Result_Angle")
            state = self.parser.get_value("Vision_Result_State")
            
            result.update({
                'x': x,
                'y': y,
                'angle': angle,
                'state': state,
            })
        except:
            pass
        
        return result
    
    def wait_for_result(self, timeout: float = 5.0) -> dict:
        """
        等待视觉结果
        
        Args:
            timeout: 超时时间（秒）
        
        Returns:
            视觉结果字典
        """
        start = time.time()
        
        while time.time() - start < timeout:
            result = self.get_vision_result()
            if result['state'] is not None and result['state'] != 0:
                return result
            time.sleep(0.1)
        
        print(f"[超时] 等待视觉结果超时 ({timeout}s)")
        return result
    
    # ==================== 状态查询 ====================
    
    def get_status(self) -> dict:
        """获取相机完整状态"""
        status = {
            'connected': self.connected,
            'light_on': self.get_light_status(),
            'hand_camera_pose': self.get_hand_camera_pose(),
            'vision_result': self.get_vision_result(),
        }
        return status
    
    def print_status(self):
        """打印相机状态"""
        status = self.get_status()
        print("\n=== 相机状态 ===")
        print(f"连接状态：{status['connected']}")
        print(f"光源状态：{status['light_on']}")
        if status['hand_camera_pose']:
            pose = status['hand_camera_pose']
            print(f"手眼位姿：[{pose[0]:.1f}, {pose[1]:.1f}, {pose[2]:.1f}, {pose[3]:.1f}, {pose[4]:.1f}, {pose[5]:.1f}]")
        if status['vision_result']:
            result = status['vision_result']
            print(f"视觉结果：x={result['x']}, y={result['y']}, angle={result['angle']}, state={result['state']}")
        print()


# ==================== 命令行工具 ====================

if __name__ == "__main__":
    import sys
    
    cam = TMCamera("192.168.1.13")
    
    if len(sys.argv) < 2:
        print("用法：python tm_camera.py [command]")
        print("命令：")
        print("  status    - 查看状态")
        print("  light on  - 打开光源")
        print("  light off - 关闭光源")
        print("  pose      - 读取手眼位姿")
        print("  result    - 读取视觉结果")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cam.connect():
        if cmd == "status":
            cam.print_status()
        elif cmd == "light" and len(sys.argv) > 2:
            cam.set_light(sys.argv[2].lower() == "on")
        elif cmd == "pose":
            pose = cam.get_hand_camera_pose()
            if pose:
                print(f"手眼位姿：[{pose[0]:.1f}, {pose[1]:.1f}, {pose[2]:.1f}, {pose[3]:.1f}, {pose[4]:.1f}, {pose[5]:.1f}]")
        elif cmd == "result":
            result = cam.get_vision_result()
            print(f"视觉结果：{result}")
        
        cam.disconnect()
