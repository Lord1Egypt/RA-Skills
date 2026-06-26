"""
代码混淆器
开发模式：明文代码
生产模式：编译为二进制 + 混淆
"""

import os
import sys
import hashlib
import base64
import shutil
from pathlib import Path


class CodeObfuscator:
    """代码混淆器"""
    
    # 需要保护的模块
    PROTECTED_MODULES = [
        "secure_api_config.py",
        "key_manager.py", 
        "token_manager.py",
        "crypto_utils.py",
    ]
    
    # 混淆后的目录
    OBF_DIR = "e:\\workbuddy\\wy\\equipment_skill\\obfuscated"
    
    @staticmethod
    def obfuscate_string(s: str) -> str:
        """字符串混淆"""
        return base64.b64encode(s.encode()).decode()
    
    @staticmethod
    def deobfuscate_string(s: str) -> str:
        """字符串解混淆"""
        return base64.b64decode(s.encode()).decode()
    
    @classmethod
    def obfuscate_code(cls, source_file: str, output_file: str):
        """
        混淆 Python 代码
        
        Args:
            source_file: 源文件路径
            output_file: 输出文件路径
        """
        with open(source_file, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # 1. 移除注释和 docstring
        source = cls._remove_comments(source)
        
        # 2. 变量名混淆
        source = cls._obfuscate_names(source)
        
        # 3. 添加反调试代码
        source = cls._add_anti_debug(source)
        
        # 4. 添加完整性校验
        source = cls._add_integrity_check(source, source_file)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(source)
    
    @classmethod
    def _remove_comments(cls, code: str) -> str:
        """移除注释"""
        import re
        # 移除单行注释
        code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
        # 移除多行字符串（docstring）
        code = re.sub(r'"""[\s\S]*?"""', '', code)
        code = re.sub(r"'''[\s\S]*?'''", '', code)
        return code
    
    @classmethod
    def _obfuscate_names(cls, code: str) -> str:
        """混淆变量名（简单版）"""
        import re
        
        # 保护的关键字和内置函数
        protected = {'self', 'cls', 'super', 'print', 'len', 'str', 'int', 'dict', 'list'}
        
        # 简单的变量名替换映射
        name_map = {}
        counter = 0
        
        def replace_name(match):
            nonlocal counter
            name = match.group(1)
            if name in protected or name.startswith('_'):
                return name
            if name not in name_map:
                name_map[name] = f'_{counter:04x}'
                counter += 1
            return name_map[name]
        
        # 替换函数定义
        code = re.sub(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', lambda m: f'def {replace_name(m)}', code)
        # 替换变量名（简化处理）
        
        return code
    
    @classmethod
    def _add_anti_debug(cls, code: str) -> str:
        """添加反调试代码"""
        anti_debug = '''
import sys
if sys.flags.debug:
    raise RuntimeError("Debug mode detected")
'''
        return anti_debug + code
    
    @classmethod
    def _add_integrity_check(cls, code: str, filename: str) -> str:
        """添加完整性校验"""
        file_hash = hashlib.sha256(code.encode()).hexdigest()[:16]
        
        check_code = f'''
import hashlib
_def _verify():
    with open(__file__, 'r') as _f:
        _h = hashlib.sha256(_f.read().encode()).hexdigest()[:16]
    if _h != "{file_hash}":
        raise RuntimeError("Code modified")
_verify()
'''
        return check_code + code
    
    @classmethod
    def compile_to_binary(cls, source_file: str, output_dir: str):
        """
        使用 Cython 编译为二进制
        
        Args:
            source_file: 源文件路径
            output_dir: 输出目录
        """
        try:
            from Cython.Build import cythonize
            from distutils.core import setup
            from distutils.extension import Extension
        except ImportError:
            print("Cython not installed, using obfuscation only")
            return False
        
        module_name = Path(source_file).stem
        
        # 创建 setup.py
        setup_code = f'''
from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("{source_file}",
        compiler_directives={{
            'language_level': "3",
            'embedsignature': False,
        }},
        annotate=False,
    ),
    script_args=["build_ext", "--inplace", "-b", "{output_dir}"]
)
'''
        
        setup_file = os.path.join(output_dir, f"setup_{module_name}.py")
        with open(setup_file, 'w') as f:
            f.write(setup_code)
        
        # 执行编译
        import subprocess
        result = subprocess.run(
            [sys.executable, setup_file],
            capture_output=True,
            text=True
        )
        
        return result.returncode == 0
    
    @classmethod
    def build_production(cls, skill_dir: str = None):
        """
        构建生产版本
        
        Args:
            skill_dir: Skill 目录路径
        """
        if skill_dir is None:
            skill_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 创建混淆目录
        if os.path.exists(cls.OBF_DIR):
            shutil.rmtree(cls.OBF_DIR)
        os.makedirs(cls.OBF_DIR)
        
        print("Building production version...")
        
        for module in cls.PROTECTED_MODULES:
            source = os.path.join(skill_dir, module)
            if not os.path.exists(source):
                continue
            
            # 尝试编译为二进制
            if cls.compile_to_binary(source, cls.OBF_DIR):
                print(f"  Compiled: {module}")
            else:
                # 退回到代码混淆
                output = os.path.join(cls.OBF_DIR, module)
                cls.obfuscate_code(source, output)
                print(f"  Obfuscated: {module}")
        
        # 复制其他文件
        for item in os.listdir(skill_dir):
            if item in cls.PROTECTED_MODULES or item == '__pycache__':
                continue
            
            src = os.path.join(skill_dir, item)
            dst = os.path.join(cls.OBF_DIR, item)
            
            if os.path.isfile(src):
                shutil.copy2(src, dst)
            elif os.path.isdir(src) and item != 'obfuscated':
                shutil.copytree(src, dst)
        
        print(f"Production build complete: {cls.OBF_DIR}")
        return cls.OBF_DIR


if __name__ == "__main__":
    CodeObfuscator.build_production()
