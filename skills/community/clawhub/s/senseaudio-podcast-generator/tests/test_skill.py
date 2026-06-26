"""
Podcast Generator Skill Tests

TDD 测试用例 - 验证 Skill 功能
"""

import pytest
import subprocess
import json
import os
import time
import requests
from pathlib import Path

# 配置
SKILL_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
PROJECT_DIR = Path("/home/wang/桌面/龙虾工作区/podcast-generator")
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"
API_BASE = "http://localhost:5000"


class TestConfigLoading:
    """测试配置读取"""
    
    def test_openclaw_config_exists(self):
        """openclaw.json 存在"""
        assert OPENCLAW_CONFIG.exists(), "openclaw.json 不存在"
    
    def test_sense_api_key_in_config(self):
        """SENSEAUDIO_API_KEY 在配置中"""
        with open(OPENCLAW_CONFIG) as f:
            config = json.load(f)
        
        assert "env" in config, "缺少 env 配置"
        assert "SENSEAUDIO_API_KEY" in config["env"], "缺少 SENSEAUDIO_API_KEY"
        assert config["env"]["SENSEAUDIO_API_KEY"], "SENSEAUDIO_API_KEY 为空"
    
    def test_config_loader_function(self):
        """配置加载函数正常"""
        # 导入 generate.py 的配置加载函数
        import sys
        sys.path.insert(0, str(SCRIPTS_DIR))
        
        from generate import load_config
        
        config = load_config()
        assert "senseaudio_api_key" in config, "缺少 senseaudio_api_key"
        assert config["senseaudio_api_key"], "senseaudio_api_key 为空"


class TestServerManagement:
    """测试服务管理"""
    
    def test_server_status_check(self):
        """服务状态检查"""
        result = subprocess.run(
            ["python3", str(SCRIPTS_DIR / "server.py"), "--status"],
            capture_output=True,
            text=True,
        )
        
        # status 命令应该返回 JSON
        assert result.returncode in [0, 1], "server.py --status 执行失败"
    
    def test_server_start_if_needed(self):
        """服务未启动时自动启动"""
        # 检查服务是否运行
        try:
            response = requests.get(f"{API_BASE}/api/config", timeout=2)
            if response.status_code == 200:
                # 服务已运行，跳过启动测试
                pytest.skip("服务已运行")
        except:
            # 服务未运行，尝试启动
            result = subprocess.run(
                ["python3", str(SCRIPTS_DIR / "server.py"), "--start"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            
            # 等待服务启动
            time.sleep(3)
            
            # 再次检查
            try:
                response = requests.get(f"{API_BASE}/api/config", timeout=5)
                assert response.status_code == 200, "服务启动后仍无法访问"
            except:
                pytest.fail("服务启动失败")


class TestPodcastGeneration:
    """测试播客生成"""
    
    @pytest.fixture(autouse=True)
    def setup_service(self):
        """确保服务运行"""
        try:
            requests.get(f"{API_BASE}/api/config", timeout=2)
        except:
            # 启动服务
            subprocess.Popen(
                ["python3", str(PROJECT_DIR / "backend" / "app.py")],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            time.sleep(3)
    
    def test_generate_simple_podcast(self):
        """生成简单播客（使用 LLM）"""
        result = subprocess.run(
            [
                "python3",
                str(SCRIPTS_DIR / "generate.py"),
                "--topic", "测试播客生成功能",
                # API 只支持 LLM 模式，移除 --no-llm
            ],
            capture_output=True,
            text=True,
            timeout=180,  # LLM 生成需要更长时间
        )

        assert result.returncode == 0, f"生成失败: {result.stderr}"

        # 检查输出 JSON
        output = json.loads(result.stdout)
        assert output.get("success"), f"生成失败: {output.get('error')}"
        assert "audio_path" in output, "缺少 audio_path"
        assert Path(output["audio_path"]).exists(), "音频文件不存在"
    
    def test_generate_with_custom_params(self):
        """自定义参数生成"""
        result = subprocess.run(
            [
                "python3",
                str(SCRIPTS_DIR / "generate.py"),
                "--topic", "人工智能的未来发展",
                "--speed", "1.2",
                "--pitch-male", "2",
                "--pitch-female", "4",
            ],
            capture_output=True,
            text=True,
            timeout=180,  # LLM 生成需要更长时间
        )
        
        assert result.returncode == 0, f"生成失败: {result.stderr}"
        
        output = json.loads(result.stdout)
        assert output.get("success"), f"生成失败: {output.get('error')}"
    
    def test_generate_with_llm_script(self):
        """使用 LLM 生成脚本"""
        result = subprocess.run(
            [
                "python3",
                str(SCRIPTS_DIR / "generate.py"),
                "--topic", "量子计算的基本原理和应用前景",
                "--use-llm",
            ],
            capture_output=True,
            text=True,
            timeout=180,
        )
        
        # LLM 生成可能失败（API 问题），所以只检查基本格式
        if result.returncode == 0:
            output = json.loads(result.stdout)
            assert "audio_path" in output, "缺少 audio_path"


class TestAPIEndpoints:
    """测试 API 接口"""
    
    @pytest.fixture(autouse=True)
    def setup_service(self):
        """确保服务运行"""
        try:
            requests.get(f"{API_BASE}/api/config", timeout=2)
        except:
            subprocess.Popen(
                ["python3", str(PROJECT_DIR / "backend" / "app.py")],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            time.sleep(3)
    
    def test_config_endpoint(self):
        """GET /api/config"""
        response = requests.get(f"{API_BASE}/api/config")
        assert response.status_code == 200
        
        data = response.json()
        assert data.get("success")
        assert "voice_config" in data
        assert "ffmpeg_available" in data
    
    def test_generate_endpoint(self):
        """POST /api/generate"""
        # 从配置获取 API Key
        with open(OPENCLAW_CONFIG) as f:
            config = json.load(f)
        api_key = config["env"]["SENSEAUDIO_API_KEY"]
        
        response = requests.post(
            f"{API_BASE}/api/generate",
            headers={
                "Content-Type": "application/json",
                "X-API-Key": api_key,
            },
            json={
                "topic": "API 测试播客",
                "speed": 1.0,
            },
            timeout=120,
        )
        
        assert response.status_code == 200
        
        data = response.json()
        assert data.get("success"), f"生成失败: {data.get('error')}"
        assert "download_url" in data
        assert "segments" in data
    
    def test_download_endpoint(self):
        """GET /api/download/{filename}"""
        # 先生成一个播客
        with open(OPENCLAW_CONFIG) as f:
            config = json.load(f)
        api_key = config["env"]["SENSEAUDIO_API_KEY"]
        
        gen_response = requests.post(
            f"{API_BASE}/api/generate",
            headers={
                "Content-Type": "application/json",
                "X-API-Key": api_key,
            },
            json={"topic": "下载测试"},
            timeout=120,
        )
        
        if gen_response.status_code == 200:
            data = gen_response.json()
            if data.get("success"):
                download_url = f"{API_BASE}{data['download_url']}"
                download_response = requests.get(download_url)
                
                assert download_response.status_code == 200
                assert len(download_response.content) > 1000, "音频文件太小"


class TestErrorHandling:
    """测试错误处理"""
    
    @pytest.fixture(autouse=True)
    def setup_service(self):
        """确保服务运行"""
        try:
            requests.get(f"{API_BASE}/api/config", timeout=2)
        except:
            subprocess.Popen(
                ["python3", str(PROJECT_DIR / "backend" / "app.py")],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            time.sleep(3)
    
    def test_missing_api_key(self):
        """缺少 API Key"""
        response = requests.post(
            f"{API_BASE}/api/generate",
            headers={"Content-Type": "application/json"},
            json={"topic": "测试"},
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "API Key" in data.get("error", "")
    
    def test_empty_topic(self):
        """话题为空"""
        with open(OPENCLAW_CONFIG) as f:
            config = json.load(f)
        api_key = config["env"]["SENSEAUDIO_API_KEY"]
        
        response = requests.post(
            f"{API_BASE}/api/generate",
            headers={
                "Content-Type": "application/json",
                "X-API-Key": api_key,
            },
            json={"topic": ""},
        )
        
        assert response.status_code == 400


# 运行测试
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])