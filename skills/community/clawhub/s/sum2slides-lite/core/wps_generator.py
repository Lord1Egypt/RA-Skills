"""
WPS Office PPT生成器实现
基于AppleScript自动化
"""

from .base_generator import BasePPTGenerator, PPTStructure, SlideContent, PPTSoftware, PPTTemplate
from typing import Any, Optional
import os
import subprocess
import tempfile
import json
from datetime import datetime


class WPSGenerator(BasePPTGenerator):
    """WPS Office PPT生成器"""
    
    def __init__(self, template: PPTTemplate = PPTTemplate.BUSINESS):
        super().__init__(software_type=PPTSoftware.WPS_OFFICE, template=template)
        self.applescript_dir = tempfile.mkdtemp(prefix="wps_ppt_")
        self.script_files = []
        self.slide_count = 0
    
    def _create_apple_script(self, script_content: str) -> str:
        """
        创建AppleScript文件
        
        Args:
            script_content: AppleScript内容
            
        Returns:
            脚本文件路径
        """
        script_file = os.path.join(self.applescript_dir, f"script_{len(self.script_files)}.applescript")
        
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        self.script_files.append(script_file)
        return script_file
    
    def _execute_apple_script(self, script_file: str) -> bool:
        """
        执行AppleScript
        
        Args:
            script_file: 脚本文件路径
            
        Returns:
            执行是否成功
        """
        try:
            result = subprocess.run(['osascript', script_file], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return True
            else:
                print(f"AppleScript执行失败: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("AppleScript执行超时")
            return False
        except Exception as e:
            print(f"AppleScript执行异常: {e}")
            return False
    
    def create_cover(self, structure: PPTStructure) -> Any:
        """
        创建封面页
        
        Args:
            structure: PPT结构
            
        Returns:
            执行状态
        """
        # 创建AppleScript
        script = f'''
tell application "WPS Office"
    activate
    delay 1
    
    -- 创建新演示文稿
    make new presentation
    delay 1
    
    -- 设置标题
    tell active presentation
        tell slide 1
            set title of shape 1 to "{structure.title}"
            
            -- 设置标题格式
            set font of text range of shape 1 to "微软雅黑"
            set size of font of text range of shape 1 to 44
            set color of font of text range of shape 1 to {{0, 122, 255}}
        end tell
        
        -- 添加副标题
        if "{structure.subtitle}" is not "" then
            tell slide 1
                set subtitle_shape to make new shape at end with properties {{type: text box}}
                set content of subtitle_shape to "{structure.subtitle}"
                
                -- 设置位置和大小
                set position of subtitle_shape to {{100, 200}}
                set size of subtitle_shape to {{600, 50}}
                
                -- 设置格式
                set font of text range of subtitle_shape to "微软雅黑"
                set size of font of text range of subtitle_shape to 24
                set color of font of text range of subtitle_shape to {{142, 142, 147}}
            end tell
        end if
    end tell
end tell
'''
        
        script_file = self._create_apple_script(script)
        success = self._execute_apple_script(script_file)
        
        if success:
            self.slide_count = 1
            return {"success": True, "slide_number": 1}
        else:
            return {"success": False, "error": "创建封面失败"}
    
    def create_content_slide(self, content: SlideContent) -> Any:
        """
        创建内容页
        
        Args:
            content: 幻灯片内容
            
        Returns:
            执行状态
        """
        # 构建内容文本
        content_text = "\\n".join(content.content)
        
        # 创建AppleScript
        script = f'''
tell application "WPS Office"
    activate
    delay 0.5
    
    tell active presentation
        -- 添加新幻灯片
        make new slide at end
        delay 0.5
        
        -- 设置标题
        tell slide {self.slide_count + 1}
            set title of shape 1 to "{content.title}"
            
            -- 设置标题格式
            set font of text range of shape 1 to "微软雅黑"
            set size of font of text range of shape 1 to 32
            set color of font of text range of shape 1 to {{0, 122, 255}}
        end tell
        
        -- 添加内容
        tell slide {self.slide_count + 1}
            set content_shape to make new shape at end with properties {{type: text box}}
            set content of content_shape to "{content_text}"
            
            -- 设置位置和大小
            set position of content_shape to {{100, 150}}
            set size of content_shape to {{600, 400}}
            
            -- 设置格式
            set font of text range of content_shape to "微软雅黑"
            set size of font of text range of content_shape to 18
            set color of font of text range of content_shape to {{28, 28, 30}}
        end tell
    end tell
end tell
'''
        
        script_file = self._create_apple_script(script)
        success = self._execute_apple_script(script_file)
        
        if success:
            self.slide_count += 1
            return {"success": True, "slide_number": self.slide_count}
        else:
            return {"success": False, "error": "创建内容页失败"}
    
    def create_two_column_slide(self, content: SlideContent) -> Any:
        """
        创建两栏内容页
        
        Args:
            content: 幻灯片内容
            
        Returns:
            执行状态
        """
        # 构建左侧内容
        left_content = "\\n".join(content.left_content) if content.left_content else ""
        right_content = "\\n".join(content.right_content) if content.right_content else ""
        
        # 创建AppleScript
        script = f'''
tell application "WPS Office"
    activate
    delay 0.5
    
    tell active presentation
        -- 添加新幻灯片
        make new slide at end
        delay 0.5
        
        -- 设置标题
        tell slide {self.slide_count + 1}
            set title of shape 1 to "{content.title}"
            
            -- 设置标题格式
            set font of text range of shape 1 to "微软雅黑"
            set size of font of text range of shape 1 to 32
            set color of font of text range of shape 1 to {{0, 122, 255}}
        end tell
        
        -- 添加左侧内容
        if "{left_content}" is not "" then
            tell slide {self.slide_count + 1}
                set left_shape to make new shape at end with properties {{type: text box}}
                set content of left_shape to "{left_content}"
                
                -- 设置位置和大小
                set position of left_shape to {{50, 150}}
                set size of left_shape to {{300, 400}}
                
                -- 设置格式
                set font of text range of left_shape to "微软雅黑"
                set size of font of text range of left_shape to 16
                set color of font of text range of left_shape to {{28, 28, 30}}
            end tell
        end if
        
        -- 添加右侧内容
        if "{right_content}" is not "" then
            tell slide {self.slide_count + 1}
                set right_shape to make new shape at end with properties {{type: text box}}
                set content of right_shape to "{right_content}"
                
                -- 设置位置和大小
                set position of right_shape to {{400, 150}}
                set size of right_shape to {{300, 400}}
                
                -- 设置格式
                set font of text range of right_shape to "微软雅黑"
                set size of font of text range of right_shape to 16
                set color of font of text range of right_shape to {{28, 28, 30}}
            end tell
        end if
    end tell
end tell
'''
        
        script_file = self._create_apple_script(script)
        success = self._execute_apple_script(script_file)
        
        if success:
            self.slide_count += 1
            return {"success": True, "slide_number": self.slide_count}
        else:
            return {"success": False, "error": "创建两栏页失败"}
    
    def create_comparison_slide(self, content: SlideContent) -> Any:
        """
        创建比较页
        
        Args:
            content: 幻灯片内容
            
        Returns:
            执行状态
        """
        # 简化实现：使用两栏页
        return self.create_two_column_slide(content)
    
    def create_summary_slide(self, content: SlideContent) -> Any:
        """
        创建总结页
        
        Args:
            content: 幻灯片内容
            
        Returns:
            执行状态
        """
        # 构建关键点
        key_points = "• " + "\\n• ".join(content.key_points) if content.key_points else ""
        conclusion = content.conclusion or ""
        
        # 创建AppleScript
        script = f'''
tell application "WPS Office"
    activate
    delay 0.5
    
    tell active presentation
        -- 添加新幻灯片
        make new slide at end
        delay 0.5
        
        -- 设置标题
        tell slide {self.slide_count + 1}
            set title of shape 1 to "{content.title}"
            
            -- 设置标题格式
            set font of text range of shape 1 to "微软雅黑"
            set size of font of text range of shape 1 to 32
            set color of font of text range of shape 1 to {{0, 122, 255}}
        end tell
        
        -- 添加关键点
        if "{key_points}" is not "" then
            tell slide {self.slide_count + 1}
                set points_shape to make new shape at end with properties {{type: text box}}
                set content of points_shape to "{key_points}"
                
                -- 设置位置和大小
                set position of points_shape to {{100, 150}}
                set size of points_shape to {{600, 300}}
                
                -- 设置格式
                set font of text range of points_shape to "微软雅黑"
                set size of font of text range of points_shape to 20
                set color of font of text range of points_shape to {{0, 122, 255}}
                set bold of font of text range of points_shape to true
            end tell
        end if
        
        -- 添加结论
        if "{conclusion}" is not "" then
            tell slide {self.slide_count + 1}
                set conclusion_shape to make new shape at end with properties {{type: text box}}
                set content of conclusion_shape to "{conclusion}"
                
                -- 设置位置和大小
                set position of conclusion_shape to {{100, 450}}
                set size of conclusion_shape to {{600, 100}}
                
                -- 设置格式
                set font of text range of conclusion_shape to "微软雅黑"
                set size of font of text range of conclusion_shape to 18
                set italic of font of text range of conclusion_shape to true
                set color of font of text range of conclusion_shape to {{142, 142, 147}}
            end tell
        end if
    end tell
end tell
'''
        
        script_file = self._create_apple_script(script)
        success = self._execute_apple_script(script_file)
        
        if success:
            self.slide_count += 1
            return {"success": True, "slide_number": self.slide_count}
        else:
            return {"success": False, "error": "创建总结页失败"}
    
    def save_ppt(self, file_path: str) -> str:
        """
        保存PPT文件
        
        Args:
            file_path: 保存路径
            
        Returns:
            保存的文件路径
        """
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # 创建保存脚本
        script = f'''
tell application "WPS Office"
    activate
    delay 1
    
    tell active presentation
        -- 保存文件
        save in "{file_path}" as format presentation
    end tell
    
    -- 关闭文档
    close active presentation saving no
end tell
'''
        
        script_file = self._create_apple_script(script)
        success = self._execute_apple_script(script_file)
        
        if success:
            print(f"✅ WPS PPT保存成功: {file_path}")
            return file_path
        else:
            print(f"❌ WPS PPT保存失败: {file_path}")
            
            # 备用方案：使用python-pptx生成标准.pptx文件
            print("⚠️ 尝试备用方案：使用标准.pptx格式")
            return self._save_as_standard_pptx(file_path)
    
    def _save_as_standard_pptx(self, file_path: str) -> str:
        """
        备用方案：使用python-pptx生成标准.pptx文件
        
        Args:
            file_path: 保存路径
            
        Returns:
            保存的文件路径
        """
        try:
            from .pptx_generator import PPTXGenerator
            from .base_generator import PPTTemplate
            
            # 创建PowerPoint生成器
            pptx_generator = PPTXGenerator(template=self.template)
            
            # 保存为.pptx
            return pptx_generator.save_ppt(file_path)
            
        except Exception as e:
            print(f"❌ 备用方案也失败: {e}")
            raise RuntimeError(f"WPS PPT保存失败: {e}")
    
    def __del__(self):
        """清理临时文件"""
        try:
            import shutil
            if os.path.exists(self.applescript_dir):
                shutil.rmtree(self.applescript_dir)
        except Exception as e:
            print(f"清理临时文件失败: {e}")