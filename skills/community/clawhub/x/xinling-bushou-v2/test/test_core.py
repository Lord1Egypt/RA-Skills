"""
test/test_core.py
心灵补手 V2.0 核心功能测试
"""

import unittest
from pathlib import Path
import sys
import json

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.persona_engine import PersonaEngine
from core.persona_registry import PersonaRegistry
from schemas.launch_config import Platform, RelationshipMode, CompiledPersona


class TestPersonaRegistry(unittest.TestCase):
    """人格注册表测试"""
    
    @classmethod
    def setUpClass(cls):
        cls.base_dir = Path.home() / ".xinling-bushou-v2"
        cls.registry = PersonaRegistry(cls.base_dir)
    
    def test_list_personas(self):
        """测试列出所有人格"""
        personas = self.registry.list_personas()
        self.assertIsInstance(personas, list)
        self.assertIn("taijian", personas)
        self.assertIn("songzhiwen", personas)
    
    def test_get_persona_info(self):
        """测试获取人格元信息"""
        info = self.registry.get_persona_info("taijian")
        self.assertIsNotNone(info)
        self.assertEqual(info["name"], "大太监")
        
        info_wen = self.registry.get_persona_info("songzhiwen")
        self.assertIsNotNone(info_wen)
        self.assertEqual(info_wen["name"], "宋之问")
    
    def test_load_persona(self):
        """测试加载人格定义"""
        persona = self.registry.load_persona("taijian")
        self.assertIsInstance(persona, dict)
        self.assertIn("meta", persona)
        self.assertEqual(persona["meta"]["name"], "大太监")
        
        persona_wen = self.registry.load_persona("songzhiwen")
        self.assertIsInstance(persona_wen, dict)
        self.assertEqual(persona_wen["meta"]["name"], "宋之问")


class TestPersonaEngine(unittest.TestCase):
    """人格引擎测试"""
    
    @classmethod
    def setUpClass(cls):
        cls.engine = PersonaEngine()
    
    def test_engine_initialization(self):
        """测试引擎初始化"""
        self.assertIsNotNone(self.engine.registry)
        self.assertIsNotNone(self.engine.session_store)
        self.assertIsNotNone(self.engine.prompt_compiler)
    
    def test_load_persona(self):
        """测试加载人格"""
        persona = self.engine.load_persona("taijian")
        self.assertIsInstance(persona, dict)
        self.assertIn("meta", persona)
    
    def test_get_adapter(self):
        """测试获取适配器"""
        adapter = self.engine._get_adapter(Platform.OPENCLAW)
        self.assertIsNotNone(adapter)
        self.assertTrue(adapter.supports_subagent())
    
    def test_activate_persona(self):
        """测试激活人格"""
        compiled = self.engine.activate_persona(
            session_id="test_session_001",
            persona_id="taijian",
            relationship=RelationshipMode.STACK,
            override_config={"behavior": {"level": 8}}
        )
        self.assertIsInstance(compiled, CompiledPersona)
        self.assertEqual(compiled.id, "taijian")
        self.assertEqual(compiled.level, 8)


class TestScholarPersona(unittest.TestCase):
    """宋之问人格专项测试"""
    
    @classmethod
    def setUpClass(cls):
        cls.engine = PersonaEngine()
        cls.scholar = cls.engine.load_persona("songzhiwen")
    
    def test_scholar_metadata(self):
        """测试宋之问元数据"""
        meta = self.scholar["meta"]
        self.assertEqual(meta["id"], "songzhiwen")
        self.assertEqual(meta["name"], "宋之问")
        self.assertEqual(meta["description"], "文人狗腿，满腹经纶却阿谀奉承")
    
    def test_scholar_pronouns(self):
        """测试宋之问人称"""
        identity = self.scholar["identity"]
        self.assertEqual(identity["pronouns"]["first_person"], "在下")
        self.assertEqual(identity["pronouns"]["second_person"], "先生")
    
    def test_scholar_phrases_exist(self):
        """测试宋之问话术存在"""
        phrases = self.scholar["phrases"]
        self.assertIn("seeds", phrases)
        seeds = phrases["seeds"]
        self.assertIn("task_completed", seeds)
        self.assertIn("1-3", seeds["task_completed"])
        self.assertIn("4-6", seeds["task_completed"])
        self.assertIn("7-9", seeds["task_completed"])
        self.assertIn("10", seeds["task_completed"])
    
    def test_scholar_forbidden_words(self):
        """测试宋之问禁用词"""
        phrases = self.scholar["phrases"]
        forbidden = phrases["generation_rules"]["forbidden_words"]
        self.assertIn("奴才", forbidden)  # 不应用太监词
        self.assertIn("您", forbidden)    # 应用"先生"而非"您"


if __name__ == "__main__":
    unittest.main(verbosity=2)
