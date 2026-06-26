"""
TM Robot Unit Tests - SVR Parser

使用 Mock 数据测试 SVR 解析器，不需要真实机器人
"""

import unittest
import struct
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tm_robot import SVRParser, JointAngles, CartesianPose


class MockSVRParser(SVRParser):
    """Mock SVR Parser for testing without robot"""
    
    def __init__(self) -> None:
        self.ip = "127.0.0.1"
        self.port = 5891
        self._sock = None
        self._cache = {}
        self._raw_body = b''
    
    def set_mock_data(self, data: bytes) -> None:
        """Set mock body data"""
        self._raw_body = data
    
    def connect(self, timeout: float = 5.0) -> bool:
        return True
    
    def disconnect(self) -> None:
        pass


class TestSVRParser(unittest.TestCase):
    """SVR Parser unit tests"""
    
    def setUp(self) -> None:
        self.parser = MockSVRParser()
    
    def _create_mock_body(
        self,
        joints: Optional[tuple] = None,
        error_code: Optional[int] = None,
        project_run: Optional[bool] = None
    ) -> bytes:
        """Create mock SVR body data - matching real TMflow format"""
        body = b''
        
        # Format: [name][type][null][data][marker]
        # Note: type code comes IMMEDIATELY after name (no null between)
        
        # Joint_Angle (type 0x18 = 24 bytes = 6 floats)
        if joints:
            body += b'Joint_Angle'  # name (11 chars)
            body += b'\x18\x00'  # type + padding
            body += struct.pack('<6f', *joints)  # data (24 bytes)
            body += b'\x0b\x00'  # marker
        
        # Error_Code (type 0x04 = 4 bytes = int32)
        if error_code is not None:
            body += b'Error_Code'  # name (10 chars)
            body += b'\x04\x00'  # type + padding
            body += struct.pack('<i', error_code)  # data (4 bytes)
            body += b'\x0a\x00'  # marker
        
        # Project_Run (type 0x01 = 1 byte = bool)
        if project_run is not None:
            body += b'Project_Run'  # name (11 chars)
            body += b'\x01\x00'  # type + padding
            body += bytes([1 if project_run else 0])  # data (1 byte)
            body += b'\x0c\x00'  # marker
        
        return body
    
    def test_parse_joint_angle(self) -> None:
        """Test parsing joint angles"""
        expected_joints = (-1.0, 2.0, 1.5, 0.5, -0.5, -1.0)
        body = self._create_mock_body(joints=expected_joints)
        self.parser.set_mock_data(body)
        
        joints = self.parser.get_value("Joint_Angle", refresh=False)
        
        self.assertIsNotNone(joints)
        self.assertEqual(len(joints), 6)
        for i, (exp, got) in enumerate(zip(expected_joints, joints)):
            self.assertAlmostEqual(exp, got, places=5, msg=f"Joint {i} mismatch")
    
    def test_parse_error_code(self) -> None:
        """Test parsing error code"""
        body = self._create_mock_body(error_code=42)
        self.parser.set_mock_data(body)
        
        error_code = self.parser.get_value("Error_Code", refresh=False)
        
        self.assertEqual(error_code, 42)
    
    def test_parse_error_code_zero(self) -> None:
        """Test parsing zero error code"""
        body = self._create_mock_body(error_code=0)
        self.parser.set_mock_data(body)
        
        error_code = self.parser.get_value("Error_Code", refresh=False)
        
        self.assertEqual(error_code, 0)
    
    def test_parse_project_run_true(self) -> None:
        """Test parsing project run (True)"""
        body = self._create_mock_body(project_run=True)
        self.parser.set_mock_data(body)
        
        project_run = self.parser.get_value("Project_Run", refresh=False)
        
        self.assertTrue(project_run)
    
    def test_parse_project_run_false(self) -> None:
        """Test parsing project run (False)"""
        body = self._create_mock_body(project_run=False)
        self.parser.set_mock_data(body)
        
        project_run = self.parser.get_value("Project_Run", refresh=False)
        
        self.assertFalse(project_run)
    
    def test_parse_variable_not_found(self) -> None:
        """Test non-existent variable"""
        body = self._create_mock_body()
        self.parser.set_mock_data(body)
        
        value = self.parser.get_value("NonExistent_Var", refresh=False)
        
        self.assertIsNone(value)
    
    def test_parse_multiple_variables(self) -> None:
        """Test parsing multiple variables"""
        body = self._create_mock_body(
            joints=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
            error_code=0,
            project_run=True
        )
        self.parser.set_mock_data(body)
        
        joints = self.parser.get_value("Joint_Angle", refresh=False)
        error_code = self.parser.get_value("Error_Code", refresh=False)
        project_run = self.parser.get_value("Project_Run", refresh=False)
        
        self.assertIsNotNone(joints)
        self.assertEqual(error_code, 0)
        self.assertTrue(project_run)


class TestDataClasses(unittest.TestCase):
    """Test data classes"""
    
    def test_joint_angles(self) -> None:
        """Test JointAngles"""
        joints = JointAngles(0.0, 1.0, 2.0, 3.0, 4.0, 5.0)
        self.assertEqual(joints.to_list(), [0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    
    def test_cartesian_pose(self) -> None:
        """Test CartesianPose"""
        pose = CartesianPose(100.0, 200.0, 300.0, 0.0, 0.0, 90.0)
        self.assertEqual(pose.to_list(), [100.0, 200.0, 300.0, 0.0, 0.0, 90.0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
