"""
场景引擎测试
"""
import pytest
import tempfile
import os
from src.services.scene_engine import SceneEngine


@pytest.fixture
def config_file():
    """创建临时配置文件"""
    content = """
scenes:
  movie:
    name: "观影模式"
    keywords: ["看电影", "电影"]
    tasks:
      - entity: light.living
        service: light.turn_on
        data:
          brightness: 50

  bath_prep:
    name: "洗澡准备"
    keywords: ["洗澡"]
    tasks:
      - entity: light.bathroom
        service: light.turn_on
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(content)
        return f.name


def test_load_scenes(config_file):
    """测试加载场景"""
    engine = SceneEngine(config_file)
    assert "movie" in engine.scenes
    assert "bath_prep" in engine.scenes


def test_get_scene(config_file):
    """测试获取场景"""
    engine = SceneEngine(config_file)
    scene = engine.get_scene("movie")
    assert scene is not None
    assert scene.name == "观影模式"
    assert len(scene.tasks) > 0


def test_get_nonexistent_scene(config_file):
    """测试获取不存在的场景"""
    engine = SceneEngine(config_file)
    scene = engine.get_scene("nonexistent")
    assert scene is None


def test_list_scenes(config_file):
    """测试列出场景"""
    engine = SceneEngine(config_file)
    scenes = engine.list_scenes()
    assert "movie" in scenes
    assert "bath_prep" in scenes


def test_reload(config_file):
    """测试热重载"""
    engine = SceneEngine(config_file, auto_reload=True)
    assert len(engine.scenes) == 2


def test_empty_config():
    """测试空配置"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("")
        engine = SceneEngine(f.name)
        assert len(engine.scenes) == 0
