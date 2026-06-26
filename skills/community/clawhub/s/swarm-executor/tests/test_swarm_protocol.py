"""
测试Swarm协议处理器
"""
import pytest
import json
import time
from coordinator.swarm_protocol import (
    SwarmProtocol, SwarmCommand, AgentType, 
    CommandPriority, CommandStatus, OutputFormat
)


class TestSwarmProtocol:
    """SwarmProtocol测试类"""
    
    @pytest.fixture
    def protocol(self):
        """创建协议处理器实例"""
        return SwarmProtocol()
    
    @pytest.fixture
    def sample_command(self):
        """创建示例命令"""
        return SwarmCommand(
            sender_type=AgentType.CEO,
            sender_id="001",
            target_type=AgentType.DEVELOPER_A,
            target_id="003",
            command={
                "action": "develop",
                "module": "login",
                "requirements": ["JWT认证", "手机验证码"],
                "output_format": "python_code"
            },
            priority=CommandPriority.HIGH,
            token_budget=1500,
            deadline="2026-04-02T12:00:00Z",
            dependencies=["cmd_12345678"]
        )
    
    def test_create_command(self, protocol):
        """测试创建命令"""
        # 创建命令
        command = protocol.create_command(
            agent_type="牢A",
            command={
                "action": "analyze",
                "module": "performance",
                "requirements": ["基准测试", "优化建议"]
            },
            priority="high",
            token_budget=2000,
            deadline="2026-04-02T14:00:00Z",
            dependencies=["cmd_11111111", "cmd_22222222"]
        )
        
        # 验证命令属性
        assert command.target_type == AgentType.DEVELOPER_A
        assert command.priority == CommandPriority.HIGH
        assert command.token_budget == 2000
        assert command.deadline == "2026-04-02T14:00:00Z"
        assert command.dependencies == ["cmd_11111111", "cmd_22222222"]
        assert command.command["action"] == "analyze"
        assert command.status == CommandStatus.PENDING
    
    def test_validate_command_valid(self, protocol, sample_command):
        """测试验证有效命令"""
        # 验证命令
        is_valid, errors = protocol.validate_command(sample_command)
        
        # 验证结果
        assert is_valid == True
        assert len(errors) == 0
    
    def test_validate_command_invalid(self, protocol):
        """测试验证无效命令"""
        # 创建无效命令（缺少必需字段）
        invalid_command = {
            "command_id": "invalid_id",  # 不符合格式
            "timestamp": "invalid_time",  # 无效时间格式
            "sender": {"type": "InvalidAgent"},  # 无效Agent类型
            "target": {"id": "999"},  # 缺少type字段
            "command": {}
        }
        
        # 验证命令
        is_valid, errors = protocol.validate_command(invalid_command)
        
        # 验证结果
        assert is_valid == False
        assert len(errors) > 0
    
    def test_parse_response(self, protocol):
        """测试解析响应"""
        # 原始响应数据
        raw_response = {
            "result": "任务完成",
            "code": "def login():\n    pass",
            "metadata": {
                "processing_time": 2.5,
                "tokens_used": 850,
                "model_used": "DeepSeek Chat"
            }
        }
        
        # 解析响应
        standardized_response = protocol.parse_response(raw_response)
        
        # 验证标准化响应
        assert "response_id" in standardized_response
        assert standardized_response["response_id"].startswith("resp_")
        assert "timestamp" in standardized_response
        assert standardized_response["status"] == "success"
        assert standardized_response["data"] == raw_response
        assert standardized_response["metadata"]["processing_time"] == 2.5
        assert standardized_response["metadata"]["tokens_used"] == 850
    
    def test_create_negotiation_request(self, protocol):
        """测试创建协商请求"""
        # 创建协商请求
        negotiation = protocol.create_negotiation_request(
            task_id="task_001",
            agents=[
                {"agent_id": "003", "agent_type": "牢A"},
                {"agent_id": "004", "agent_type": "牢B"},
                {"agent_id": "005", "agent_type": "牢C"}
            ],
            constraints={
                "max_tokens": 2000,
                "deadline": "2026-04-02T15:00:00Z",
                "required_skills": ["coding", "analysis"]
            }
        )
        
        # 验证协商请求
        assert "negotiation_id" in negotiation
        assert negotiation["negotiation_id"].startswith("neg_")
        assert negotiation["task_id"] == "task_001"
        assert len(negotiation["participants"]) == 3
        assert negotiation["constraints"]["max_tokens"] == 2000
        assert negotiation["status"] == "pending"
        assert negotiation["proposals"] == []
        assert negotiation["result"] is None
    
    def test_create_task_assignment(self, protocol, sample_command):
        """测试创建任务分配"""
        # 创建任务分配
        assignment = protocol.create_task_assignment(
            command=sample_command,
            assigned_agent="003"
        )
        
        # 验证任务分配
        assert "assignment_id" in assignment
        assert assignment["assignment_id"].startswith("assign_")
        assert assignment["command_id"] == sample_command.command_id
        assert assignment["assigned_to"] == "003"
        assert assignment["priority"] == "high"
        assert assignment["token_budget"] == 1500
        assert assignment["deadline"] == "2026-04-02T12:00:00Z"
        assert assignment["status"] == "assigned"
    
    def test_create_completion_notification(self, protocol, sample_command):
        """测试创建完成通知"""
        # 任务结果
        result = {
            "success": True,
            "output": "登录模块开发完成",
            "files_created": ["login.py", "auth_utils.py"],
            "tests_passed": 5,
            "tests_failed": 0
        }
        
        # 创建完成通知
        completion = protocol.create_completion_notification(
            command=sample_command,
            result=result
        )
        
        # 验证完成通知
        assert "completion_id" in completion
        assert completion["completion_id"].startswith("complete_")
        assert completion["command_id"] == sample_command.command_id
        assert completion["status"] == "completed"
        assert completion["result"] == result
        assert completion["quality_score"] == 1.0
    
    def test_command_to_dict_and_back(self, sample_command):
        """测试命令的字典转换和反向转换"""
        # 转换为字典
        command_dict = sample_command.to_dict()
        
        # 验证字典格式
        assert command_dict["command_id"] == sample_command.command_id
        assert command_dict["sender"]["type"] == "小小兵CEO"
        assert command_dict["target"]["type"] == "牢A"
        assert command_dict["command"]["action"] == "develop"
        assert command_dict["metadata"]["priority"] == "high"
        
        # 从字典创建新命令
        new_command = SwarmCommand.from_dict(command_dict)
        
        # 验证新命令属性
        assert new_command.command_id == sample_command.command_id
        assert new_command.sender_type == sample_command.sender_type
        assert new_command.target_type == sample_command.target_type
        assert new_command.command == sample_command.command
        assert new_command.priority == sample_command.priority
        assert new_command.token_budget == sample_command.token_budget
    
    def test_command_json_serialization(self, sample_command):
        """测试命令的JSON序列化"""
        # 转换为JSON
        json_str = sample_command.to_json()
        
        # 验证JSON格式
        json_data = json.loads(json_str)
        assert json_data["command_id"] == sample_command.command_id
        assert json_data["sender"]["type"] == "小小兵CEO"
        
        # 从JSON创建新命令
        new_command = SwarmCommand.from_json(json_str)
        
        # 验证新命令属性
        assert new_command.command_id == sample_command.command_id
        assert new_command.sender_type == sample_command.sender_type
        assert new_command.command == sample_command.command
    
    def test_command_status_transitions(self):
        """测试命令状态转换"""
        command = SwarmCommand()
        
        # 初始状态
        assert command.status == CommandStatus.PENDING
        assert command.assigned_to is None
        assert command.started_at is None
        assert command.completed_at is None
        
        # 分配任务
        command.assigned_to = "003"
        command.status = CommandStatus.ASSIGNED
        
        # 开始执行
        command.started_at = "2026-04-02T10:00:00Z"
        command.status = CommandStatus.IN_PROGRESS
        
        # 完成任务
        command.completed_at = "2026-04-02T10:30:00Z"
        command.status = CommandStatus.COMPLETED
        command.result = {"output": "任务完成"}
        
        # 验证最终状态
        assert command.status == CommandStatus.COMPLETED
        assert command.assigned_to == "003"
        assert command.started_at == "2026-04-02T10:00:00Z"
        assert command.completed_at == "2026-04-02T10:30:00Z"
        assert command.result["output"] == "任务完成"
    
    def test_global_protocol_singleton(self):
        """测试全局协议处理器的单例模式"""
        from coordinator.swarm_protocol import get_global_protocol
        
        # 获取第一个实例
        protocol1 = get_global_protocol()
        
        # 获取第二个实例
        protocol2 = get_global_protocol()
        
        # 验证是同一个实例
        assert protocol1 is protocol2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])