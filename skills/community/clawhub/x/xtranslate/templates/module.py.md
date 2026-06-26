# Python 模块模板

## 标准模块结构

```python
"""
模块名称: xxx_handler
功能描述: 处理 XXX 文件的读取、翻译和保存
"""

import os
from config import CONFIG

class XXXHandler:
    """XXX 文件处理器"""
    
    @staticmethod
    def read(file_path):
        """读取文件内容
        
        Args:
            file_path: 文件路径
            
        Returns:
            内容列表或字符串
        """
        pass
    
    @staticmethod
    def translate_in_place(file_path, translator, output_path):
        """翻译文件并保留格式
        
        Args:
            file_path: 输入文件路径
            translator: 翻译器实例
            output_path: 输出文件路径
            
        Returns:
            输出文件路径
        """
        pass
    
    @staticmethod
    def save(content, output_path):
        """保存内容到文件
        
        Args:
            content: 要保存的内容
            output_path: 输出路径
        """
        pass
```

## 关键规范

1. **类名**: 使用 PascalCase，如 `FileHandler`, `CADHandler`
2. **方法**: 使用 snake_case，静态方法用 `@staticmethod`
3. **文档字符串**: 每个类和公共方法必须有 docstring
4. **导入顺序**: 标准库 → 第三方库 → 本地模块
5. **错误处理**: 使用 try-except 捕获并打印友好错误信息
