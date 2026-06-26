#!/usr/bin/env python3
"""
依赖检查工具
自动检测并提示缺少的依赖
"""

import sys
import subprocess
import importlib.util
from pathlib import Path

class DependencyChecker:
    """依赖检查器"""
    
    def __init__(self):
        self.dependencies = {
            'basic': {
                'pillow': {
                    'name': 'Pillow',
                    'import_name': 'PIL',
                    'pip_name': 'pillow',
                    'required': True,
                    'purpose': '图像处理库，用于屏幕截图'
                },
                'pyautogui': {
                    'name': 'PyAutoGUI',
                    'import_name': 'pyautogui',
                    'pip_name': 'pyautogui',
                    'required': True,
                    'purpose': '屏幕自动化库，用于获取屏幕信息'
                }
            },
            'ocr': {
                'pytesseract': {
                    'name': 'pytesseract',
                    'import_name': 'pytesseract',
                    'pip_name': 'pytesseract',
                    'required': False,
                    'purpose': 'OCR文字识别库'
                }
            },
            'analysis': {
                'opencv': {
                    'name': 'OpenCV',
                    'import_name': 'cv2',
                    'pip_name': 'opencv-python',
                    'required': False,
                    'purpose': '计算机视觉库，用于图像分析'
                },
                'numpy': {
                    'name': 'NumPy',
                    'import_name': 'numpy',
                    'pip_name': 'numpy',
                    'required': False,
                    'purpose': '数值计算库，用于图像处理'
                }
            }
        }
        
        self.missing_deps = []
        self.available_deps = []
        self.tesseract_path = None
        
    def check_import(self, module_name):
        """检查模块是否可以导入"""
        try:
            spec = importlib.util.find_spec(module_name)
            return spec is not None
        except:
            return False
    
    def check_tesseract(self):
        """检查Tesseract OCR是否安装"""
        print("\n检查Tesseract OCR...")
        
        # 常见Tesseract路径
        common_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files\Tesseract\tesseract.exe",
        ]
        
        # 检查环境变量
        try:
            result = subprocess.run(
                "tesseract --version",
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            if result.returncode == 0:
                print("  [成功] Tesseract在环境变量中可用")
                # 获取版本
                version_line = result.stdout.strip().split('\n')[0]
                print(f"   版本: {version_line}")
                return True
        except:
            pass
        
        # 检查常见路径
        for path in common_paths:
            if Path(path).exists():
                print(f"  [成功] 找到Tesseract: {path}")
                self.tesseract_path = path
                
                # 检查版本
                try:
                    result = subprocess.run(
                        [path, "--version"],
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        errors='ignore'
                    )
                    if result.returncode == 0:
                        version_line = result.stdout.strip().split('\n')[0]
                        print(f"   版本: {version_line}")
                except:
                    pass
                    
                return True
        
        print("  [失败] 未找到Tesseract OCR")
        print("  OCR功能将不可用")
        return False
    
    def check_category(self, category_name, category_deps):
        """检查一个类别的依赖"""
        print(f"\n检查{category_name}依赖...")
        
        for dep_key, dep_info in category_deps.items():
            is_available = self.check_import(dep_info['import_name'])
            
            if is_available:
                print(f"  [成功] {dep_info['name']}: 已安装")
                self.available_deps.append(dep_info['name'])
            else:
                print(f"  [失败] {dep_info['name']}: 未安装")
                print(f"    用途: {dep_info['purpose']}")
                if dep_info['required']:
                    self.missing_deps.append(dep_info)
    
    def run_checks(self):
        """运行所有检查"""
        print("=" * 60)
        print("OPENCLAW(龙虾)-屏幕查看器 - 依赖检查")
        print("=" * 60)
        
        # 检查基础依赖
        self.check_category('基础', self.dependencies['basic'])
        
        # 检查OCR依赖
        self.check_category('OCR', self.dependencies['ocr'])
        
        # 检查分析依赖
        self.check_category('分析', self.dependencies['analysis'])
        
        # 检查Tesseract OCR
        tesseract_installed = self.check_tesseract()
        
        # 显示结果
        print("\n" + "=" * 60)
        print("依赖检查结果:")
        print("=" * 60)
        
        if not self.missing_deps:
            print("\n[成功] 所有必需依赖已安装!")
        else:
            print("\n[警告] 缺少以下必需依赖:")
            for dep in self.missing_deps:
                print(f"  • {dep['name']} ({dep['pip_name']})")
                print(f"    用途: {dep['purpose']}")
        
        # 显示可选依赖状态
        if self.available_deps:
            print(f"\n[信息] 已安装的可选依赖: {', '.join(self.available_deps)}")
        
        # Tesseract状态
        if tesseract_installed:
            print("\n[成功] Tesseract OCR已安装，OCR功能可用")
        else:
            print("\n[警告] Tesseract OCR未安装，OCR功能将不可用")
        
        # 提供安装建议
        if self.missing_deps or not tesseract_installed:
            print("\n" + "=" * 60)
            print("安装建议:")
            print("=" * 60)
            
            if self.missing_deps:
                print("\n安装Python依赖:")
                pip_commands = []
                for dep in self.missing_deps:
                    pip_commands.append(f"pip install {dep['pip_name']}")
                
                print("或运行以下命令:")
                for cmd in pip_commands:
                    print(f"  {cmd}")
                
                print("\n或运行一键安装脚本:")
                print("  python scripts/setup.py")
            
            if not tesseract_installed:
                print("\n安装Tesseract OCR:")
                print("Windows:")
                print("  自动安装: python scripts/install_tesseract.py")
                print("  手动安装: 从 https://github.com/UB-Mannheim/tesseract/wiki 下载")
                print("macOS:")
                print("  brew install tesseract")
                print("Linux:")
                print("  sudo apt-get install tesseract-ocr")
        
        print("\n" + "=" * 60)
        
        # 返回结果
        has_all_required = len(self.missing_deps) == 0
        return has_all_required, tesseract_installed
    
    def get_installation_commands(self):
        """获取安装命令"""
        commands = []
        
        if self.missing_deps:
            commands.append("# 安装Python依赖")
            for dep in self.missing_deps:
                commands.append(f"pip install {dep['pip_name']}")
        
        if not self.tesseract_path:
            commands.append("\n# 安装Tesseract OCR")
            commands.append("# Windows:")
            commands.append("python scripts/install_tesseract.py")
            commands.append("# 或手动下载: https://github.com/UB-Mannheim/tesseract/wiki")
        
        return "\n".join(commands)

def main():
    """主函数"""
    checker = DependencyChecker()
    has_all_required, tesseract_installed = checker.run_checks()
    
    # 导出到环境变量
    if checker.tesseract_path:
        print(f"\nTesseract路径: {checker.tesseract_path}")
        print("建议在Python代码中设置:")
        print(f'pytesseract.pytesseract.tesseract_cmd = r"{checker.tesseract_path}"')
    
    # 返回退出码
    if has_all_required:
        print("\n[成功] 系统准备就绪，可以运行屏幕查看器")
        sys.exit(0)
    else:
        print("\n[失败] 缺少必需依赖，请先安装")
        sys.exit(1)

if __name__ == "__main__":
    main()