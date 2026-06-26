"""
文件检查模块

该模块提供文件安全性检查功能，包括文件权限、完整性、恶意内容等方面的检查。
"""

import os
import stat
import hashlib
import magic
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import re


class FileChecker:
    """
    文件安全检查器
    
    提供多种文件相关的安全检查功能，包括权限检查、完整性校验、
    恶意内容检测、文件类型验证等。
    """
    
    def __init__(self):
        """初始化文件检查器"""
        # 常见的危险文件扩展名
        self.dangerous_extensions = {
            '.exe', '.bat', '.cmd', '.com', '.scr', '.vbs', '.js', '.jse', 
            '.wsf', '.wsh', '.msi', '.msp', '.dll', '.sys', '.bin', '.pif',
            '.lnk', '.inf', '.reg', '.ps1', '.sh', '.bash', '.pl', '.py',
            '.rb', '.php', '.jsp', '.asp', '.aspx', '.cgi', '.jar', '.apk'
        }
        
        # 常见的敏感文件路径模式
        self.sensitive_patterns = [
            r'.*passwd.*',
            r'.*shadow.*',
            r'.*\.ssh.*',
            r'.*\.aws.*',
            r'.*\.azure.*',
            r'.*\.kube.*',
            r'.*config.*',
            r'.*secret.*',
            r'.*key.*',
            r'.*token.*',
            r'.*\.env.*',
            r'.*\.pem.*',
            r'.*\.crt.*',
            r'.*\.cer.*',
            r'.*\.der.*',
            r'.*\.p12.*',
            r'.*\.pfx.*'
        ]
    
    def check_file_permissions(self, file_path: str) -> Dict[str, str]:
        """
        检查文件权限
        
        Args:
            file_path (str): 文件路径
            
        Returns:
            Dict[str, str]: 权限信息
        """
        try:
            file_stat = os.stat(file_path)
            permissions = stat.filemode(file_stat.st_mode)
            
            result = {
                'permissions': permissions,
                'readable': bool(file_stat.st_mode & stat.S_IRUSR),
                'writable': bool(file_stat.st_mode & stat.S_IWUSR),
                'executable': bool(file_stat.st_mode & stat.S_IXUSR),
                'size': file_stat.st_size,
                'owner_uid': file_stat.st_uid,
                'group_gid': file_stat.st_gid
            }
            
            # 检查是否存在不安全的权限设置
            if file_stat.st_mode & stat.S_IROTH:  # 其他用户可读
                result['world_readable'] = True
            if file_stat.st_mode & stat.S_IWOTH:  # 其他用户可写
                result['world_writable'] = True
            if file_stat.st_mode & stat.S_IXOTH:  # 其他用户可执行
                result['world_executable'] = True
                
            return result
        except Exception as e:
            return {'error': str(e)}
    
    def calculate_file_hash(self, file_path: str, algorithm: str = 'sha256') -> Optional[str]:
        """
        计算文件哈希值
        
        Args:
            file_path (str): 文件路径
            algorithm (str): 哈希算法 ('md5', 'sha1', 'sha256', 'sha512')
            
        Returns:
            Optional[str]: 文件哈希值
        """
        try:
            hash_obj = hashlib.new(algorithm)
            
            with open(file_path, 'rb') as f:
                # 分块读取以处理大文件
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
                    
            return hash_obj.hexdigest()
        except Exception:
            return None
    
    def check_file_integrity(self, file_path: str, expected_hash: str, 
                           algorithm: str = 'sha256') -> bool:
        """
        检查文件完整性
        
        Args:
            file_path (str): 文件路径
            expected_hash (str): 期望的哈希值
            algorithm (str): 哈希算法
            
        Returns:
            bool: 文件是否完整
        """
        actual_hash = self.calculate_file_hash(file_path, algorithm)
        return actual_hash is not None and actual_hash.lower() == expected_hash.lower()
    
    def detect_dangerous_extension(self, file_path: str) -> bool:
        """
        检测危险文件扩展名
        
        Args:
            file_path (str): 文件路径
            
        Returns:
            bool: 是否为危险扩展名
        """
        file_ext = Path(file_path).suffix.lower()
        return file_ext in self.dangerous_extensions
    
    def get_file_type(self, file_path: str) -> Optional[str]:
        """
        获取文件真实类型
        
        Args:
            file_path (str): 文件路径
            
        Returns:
            Optional[str]: 文件类型
        """
        try:
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(file_path)
            return file_type
        except Exception:
            return None
    
    def scan_for_sensitive_content(self, file_path: str) -> List[Dict[str, str]]:
        """
        扫描文件中的敏感内容
        
        Args:
            file_path (str): 文件路径
            
        Returns:
            List[Dict[str, str]]: 敏感内容列表
        """
        sensitive_matches = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # 检查常见的敏感信息模式
            patterns = [
                (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 'email'),
                (r'\b(?:\d{1,3}\.){3}\d{1,3}\b', 'ip_address'),
                (r'(?:https?://)?(?:www\.)?[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}(?:/[^\s]*)?', 'url'),
                (r'\b[A-Z0-9]{20,}\b', 'api_key_candidate'),
                (r'[A-Za-z0-9+/]{20,}={0,2}', 'base64_candidate'),
                (r'(?i)(password|pwd|secret|token|key)\s*[=:]\s*["\']?([A-Za-z0-9_\-!@#$%^&*()]+)["\']?', 'credential'),
            ]
            
            for i, (pattern, category) in enumerate(patterns[:-1]):  # 最后一个是特殊处理
                matches = re.finditer(pattern, content)
                for match in matches:
                    sensitive_matches.append({
                        'category': category,
                        'match': match.group(),
                        'line_number': content[:match.start()].count('\n') + 1,
                        'context': content[max(0, match.start()-50):match.end()+50].strip()
                    })
            
            # 处理最后一种模式（包含关键词的）
            last_pattern, last_category = patterns[-1]
            matches = re.finditer(last_pattern, content)
            for match in matches:
                sensitive_matches.append({
                    'category': last_category,
                    'match': match.group(),
                    'line_number': content[:match.start()].count('\n') + 1,
                    'context': content[max(0, match.start()-50):match.end()+50].strip()
                })
                
        except Exception as e:
            sensitive_matches.append({
                'category': 'error',
                'match': str(e),
                'line_number': 0,
                'context': 'Error reading file'
            })
            
        return sensitive_matches
    
    def check_directory_security(self, dir_path: str) -> Dict[str, List[str]]:
        """
        检查目录安全性
        
        Args:
            dir_path (str): 目录路径
            
        Returns:
            Dict[str, List[str]]: 安全检查结果
        """
        results = {
            'dangerous_files': [],
            'world_writable_dirs': [],
            'suspicious_permissions': [],
            'total_files': 0
        }
        
        try:
            for root, dirs, files in os.walk(dir_path):
                results['total_files'] += len(files)
                
                # 检查目录权限
                for d in dirs:
                    dir_full_path = os.path.join(root, d)
                    try:
                        dir_stat = os.stat(dir_full_path)
                        if dir_stat.st_mode & stat.S_IWOTH:  # 其他用户可写
                            results['world_writable_dirs'].append(dir_full_path)
                            
                        # 检查权限是否过于宽松
                        if (dir_stat.st_mode & stat.S_IROTH and dir_stat.st_mode & stat.S_IXOTH and 
                            not (dir_stat.st_mode & stat.S_IWOTH)):
                            # 目录对外可读可执行，但不可写（一般可以接受）
                            pass
                        elif dir_stat.st_mode & stat.S_IWOTH:
                            # 目录对外可写，非常危险
                            results['suspicious_permissions'].append(f"{dir_full_path}: world-writable")
                    except Exception:
                        pass
                
                # 检查文件
                for f in files:
                    file_full_path = os.path.join(root, f)
                    try:
                        if self.detect_dangerous_extension(file_full_path):
                            results['dangerous_files'].append(file_full_path)
                            
                        # 检查文件权限
                        file_stat = os.stat(file_full_path)
                        if file_stat.st_mode & stat.S_IWOTH:  # 其他用户可写
                            results['suspicious_permissions'].append(f"{file_full_path}: world-writable")
                    except Exception:
                        pass
        except Exception as e:
            results['error'] = str(e)
            
        return results
    
    def is_executable_file(self, file_path: str) -> bool:
        """
        检查文件是否可执行
        
        Args:
            file_path (str): 文件路径
            
        Returns:
            bool: 是否可执行
        """
        try:
            return os.access(file_path, os.X_OK)
        except Exception:
            return False
    
    def find_large_files(self, dir_path: str, size_threshold: int = 100*1024*1024) -> List[Tuple[str, int]]:
        """
        查找大文件
        
        Args:
            dir_path (str): 目录路径
            size_threshold (int): 大小阈值（字节），默认100MB
            
        Returns:
            List[Tuple[str, int]]: 大文件列表（路径，大小）
        """
        large_files = []
        
        try:
            for root, dirs, files in os.walk(dir_path):
                for f in files:
                    file_path = os.path.join(root, f)
                    try:
                        size = os.path.getsize(file_path)
                        if size > size_threshold:
                            large_files.append((file_path, size))
                    except Exception:
                        pass
        except Exception as e:
            print(f"Error finding large files: {e}")
            
        return large_files
    
    def check_file_age(self, file_path: str, max_days: int = 30) -> bool:
        """
        检查文件年龄，判断是否为近期修改
        
        Args:
            file_path (str): 文件路径
            max_days (int): 最大天数
            
        Returns:
            bool: 文件是否在指定天数内被修改
        """
        import time
        
        try:
            mod_time = os.path.getmtime(file_path)
            current_time = time.time()
            age_in_days = (current_time - mod_time) / (24 * 60 * 60)
            return age_in_days <= max_days
        except Exception:
            return False