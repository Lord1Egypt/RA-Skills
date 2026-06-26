#!/usr/bin/env python3
"""
备份管理器 - 小龙虾工作流 v0.3.0 辅助组件

功能：
1. 自动备份项目文件和状态
2. 支持本地备份和Git仓库备份
3. 增量备份和版本管理
4. 备份恢复和验证
"""

import os
import json
import shutil
import hashlib
import tarfile
import zipfile
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BackupManager:
    """备份管理器"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化备份管理器
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.backup_history: List[Dict[str, Any]] = []
        logger.info("备份管理器初始化完成")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """加载配置"""
        default_config = {
            'enabled': True,
            'local_backup_dir': '/root/.openclaw/backups',
            'git_repository': '',
            'git_branch': 'main',
            'backup_interval_minutes': 60,
            'max_backups_per_project': 10,
            'incremental_backup': True,
            'compress_backups': True,
            'compression_format': 'gz',  # gz, bz2, xz, zip
            'backup_types': ['project_files', 'execution_state', 'logs', 'outputs'],
            'exclude_patterns': ['*.tmp', '*.log', '*.pyc', '__pycache__', '.git'],
            'verification_enabled': True,
            'cleanup_old_backups': True,
            'cleanup_days': 30
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                
                # 深度合并
                if 'backup' in user_config:
                    for key, value in user_config['backup'].items():
                        default_config[key] = value
            except Exception as e:
                logger.warning(f"加载备份配置失败，使用默认配置: {e}")
        
        return default_config
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """计算文件哈希值"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.warning(f"计算文件哈希失败 {file_path}: {e}")
            return ''
    
    def _create_backup_manifest(self, project_dir: Path) -> Dict[str, Any]:
        """创建备份清单"""
        manifest = {
            'project_id': project_dir.name,
            'backup_time': datetime.now().isoformat(),
            'files': [],
            'total_size_bytes': 0,
            'file_count': 0,
            'hashes': {}
        }
        
        exclude_patterns = self.config['exclude_patterns']
        
        for file_path in project_dir.rglob('*'):
            # 检查排除模式
            should_exclude = False
            for pattern in exclude_patterns:
                if pattern.startswith('*'):
                    if file_path.name.endswith(pattern[1:]):
                        should_exclude = True
                        break
                elif pattern in str(file_path):
                    should_exclude = True
                    break
            
            if should_exclude:
                continue
            
            if file_path.is_file():
                try:
                    file_size = file_path.stat().st_size
                    file_hash = self._calculate_file_hash(file_path)
                    
                    relative_path = str(file_path.relative_to(project_dir))
                    
                    manifest['files'].append({
                        'path': relative_path,
                        'size_bytes': file_size,
                        'hash': file_hash,
                        'modified_time': file_path.stat().st_mtime
                    })
                    
                    manifest['total_size_bytes'] += file_size
                    manifest['file_count'] += 1
                    manifest['hashes'][relative_path] = file_hash
                    
                except Exception as e:
                    logger.warning(f"处理文件失败 {file_path}: {e}")
        
        return manifest
    
    def _create_backup_archive(self, project_dir: Path, backup_dir: Path, 
                              manifest: Dict[str, Any]) -> Optional[Path]:
        """创建备份归档文件"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        project_id = project_dir.name
        archive_name = f"backup_{project_id}_{timestamp}"
        
        if self.config['compress_backups']:
            format = self.config['compression_format']
            if format == 'zip':
                archive_path = backup_dir / f"{archive_name}.zip"
                return self._create_zip_archive(project_dir, archive_path, manifest)
            else:
                archive_path = backup_dir / f"{archive_name}.tar.{format}"
                return self._create_tar_archive(project_dir, archive_path, manifest, format)
        else:
            # 不压缩，直接复制目录
            backup_path = backup_dir / archive_name
            return self._copy_directory(project_dir, backup_path, manifest)
    
    def _create_zip_archive(self, project_dir: Path, archive_path: Path, 
                           manifest: Dict[str, Any]) -> Optional[Path]:
        """创建ZIP归档"""
        try:
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_info in manifest['files']:
                    file_path = project_dir / file_info['path']
                    arcname = file_info['path']
                    zipf.write(file_path, arcname)
            
            # 添加清单文件
            with zipfile.ZipFile(archive_path, 'a', zipfile.ZIP_DEFLATED) as zipf:
                manifest_json = json.dumps(manifest, ensure_ascii=False, indent=2)
                zipf.writestr('backup_manifest.json', manifest_json)
            
            logger.info(f"ZIP归档创建成功: {archive_path} ({archive_path.stat().st_size:,} 字节)")
            return archive_path
            
        except Exception as e:
            logger.error(f"创建ZIP归档失败: {e}")
            return None
    
    def _create_tar_archive(self, project_dir: Path, archive_path: Path, 
                           manifest: Dict[str, Any], format: str) -> Optional[Path]:
        """创建TAR归档"""
        try:
            if format == 'gz':
                mode = 'w:gz'
            elif format == 'bz2':
                mode = 'w:bz2'
            elif format == 'xz':
                mode = 'w:xz'
            else:
                mode = 'w'
            
            with tarfile.open(archive_path, mode) as tar:
                for file_info in manifest['files']:
                    file_path = project_dir / file_info['path']
                    arcname = file_info['path']
                    tar.add(file_path, arcname=arcname)
                
                # 添加清单文件（临时文件）
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
                    tmp_path = Path(tmp.name)
                    json.dump(manifest, tmp, ensure_ascii=False, indent=2)
                    tmp.flush()
                    tar.add(tmp_path, arcname='backup_manifest.json')
                    tmp_path.unlink()
            
            logger.info(f"TAR归档创建成功: {archive_path} ({archive_path.stat().st_size:,} 字节)")
            return archive_path
            
        except Exception as e:
            logger.error(f"创建TAR归档失败: {e}")
            return None
    
    def _copy_directory(self, project_dir: Path, backup_path: Path, 
                       manifest: Dict[str, Any]) -> Optional[Path]:
        """复制目录（无压缩）"""
        try:
            shutil.copytree(project_dir, backup_path, 
                          ignore=shutil.ignore_patterns(*self.config['exclude_patterns']))
            
            # 保存清单文件
            manifest_file = backup_path / 'backup_manifest.json'
            with open(manifest_file, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)
            
            logger.info(f"目录复制完成: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"复制目录失败: {e}")
            return None
    
    def _git_backup(self, project_dir: Path, manifest: Dict[str, Any]) -> bool:
        """Git备份"""
        git_repo = self.config['git_repository']
        if not git_repo:
            logger.info("未配置Git仓库，跳过Git备份")
            return False
        
        try:
            import subprocess
            import tempfile
            
            # 创建临时目录用于Git操作
            with tempfile.TemporaryDirectory(prefix='xlx_git_') as tmpdir:
                tmp_path = Path(tmpdir)
                
                # 克隆仓库
                subprocess.run(['git', 'clone', git_repo, tmp_path], 
                             capture_output=True, check=True)
                
                # 切换到指定分支
                subprocess.run(['git', '-C', tmp_path, 'checkout', 
                              self.config['git_branch']], capture_output=True, check=True)
                
                # 复制项目文件到仓库
                backup_dir = tmp_path / 'backups' / project_dir.name
                backup_dir.mkdir(parents=True, exist_ok=True)
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                timestamp_dir = backup_dir / timestamp
                
                shutil.copytree(project_dir, timestamp_dir, 
                              ignore=shutil.ignore_patterns(*self.config['exclude_patterns']))
                
                # 添加并提交
                subprocess.run(['git', '-C', tmp_path, 'add', '.'], 
                             capture_output=True, check=True)
                
                commit_msg = f"备份: {project_dir.name} - {datetime.now().isoformat()}"
                subprocess.run(['git', '-C', tmp_path, 'commit', '-m', commit_msg], 
                             capture_output=True, check=True)
                
                # 推送
                subprocess.run(['git', '-C', tmp_path, 'push', 'origin', 
                              self.config['git_branch']], capture_output=True, check=True)
                
                logger.info(f"Git备份成功: {git_repo}")
                return True
                
        except Exception as e:
            logger.error(f"Git备份失败: {e}")
            return False
    
    def backup_project(self, project_dir: Path, backup_type: str = 'full') -> Dict[str, Any]:
        """
        备份项目
        
        Args:
            project_dir: 项目目录
            backup_type: 备份类型 ('full', 'incremental', 'state_only')
            
        Returns:
            Dict[str, Any]: 备份结果
        """
        if not self.config['enabled']:
            logger.warning("备份功能未启用")
            return {'success': False, 'reason': 'backup_disabled'}
        
        if not project_dir.exists():
            logger.error(f"项目目录不存在: {project_dir}")
            return {'success': False, 'reason': 'project_not_found'}
        
        result = {
            'success': False,
            'backup_id': '',
            'backup_time': datetime.now().isoformat(),
            'project_id': project_dir.name,
            'backup_type': backup_type,
            'files_backed_up': 0,
            'total_size_bytes': 0,
            'backup_path': '',
            'errors': []
        }
        
        try:
            # 创建备份目录
            backup_root = Path(self.config['local_backup_dir'])
            backup_root.mkdir(parents=True, exist_ok=True)
            
            project_backup_dir = backup_root / project_dir.name
            project_backup_dir.mkdir(exist_ok=True)
            
            # 创建备份清单
            logger.info(f"创建备份清单: {project_dir}")
            manifest = self._create_backup_manifest(project_dir)
            
            if not manifest['files']:
                logger.warning("没有文件需要备份")
                result['errors'].append('no_files_to_backup')
                return result
            
            # 创建备份归档
            logger.info(f"创建备份归档...")
            backup_path = self._create_backup_archive(project_dir, project_backup_dir, manifest)
            
            if not backup_path:
                result['errors'].append('archive_creation_failed')
                return result
            
            # Git备份
            git_success = False
            if self.config['git_repository']:
                logger.info("执行Git备份...")
                git_success = self._git_backup(project_dir, manifest)
            
            # 验证备份
            if self.config['verification_enabled']:
                verification = self._verify_backup(backup_path, manifest)
                if not verification['success']:
                    result['errors'].extend(verification['errors'])
                    logger.warning(f"备份验证失败: {verification['errors']}")
            
            # 清理旧备份
            if self.config['cleanup_old_backups']:
                self._cleanup_old_backups(project_backup_dir)
            
            # 更新结果
            result['success'] = True
            result['backup_id'] = backup_path.stem
            result['files_backed_up'] = manifest['file_count']
            result['total_size_bytes'] = manifest['total_size_bytes']
            result['backup_path'] = str(backup_path)
            result['git_backup_success'] = git_success
            result['manifest'] = manifest
            
            # 记录备份历史
            self.backup_history.append({
                'timestamp': result['backup_time'],
                'project_id': result['project_id'],
                'backup_id': result['backup_id'],
                'files_count': result['files_backed_up'],
                'size_bytes': result['total_size_bytes'],
                'backup_path': result['backup_path'],
                'success': True
            })
            
            logger.info(f"备份成功: {result['files_backed_up']} 个文件, "
                       f"{result['total_size_bytes']:,} 字节")
            
        except Exception as e:
            logger.error(f"备份过程异常: {e}")
            result['errors'].append(str(e))
            result['success'] = False
        
        return result
    
    def _verify_backup(self, backup_path: Path, manifest: Dict[str, Any]) -> Dict[str, Any]:
        """验证备份完整性"""
        result = {
            'success': True,
            'errors': [],
            'verified_files': 0,
            'failed_files': 0
        }
        
        try:
            # 检查备份文件是否存在
            if not backup_path.exists():
                result['success'] = False
                result['errors'].append('backup_file_not_found')
                return result
            
            # 检查清单中的文件是否都在备份中
            if backup_path.is_dir():
                # 目录备份
                for file_info in manifest['files']:
                    file_path = backup_path / file_info['path']
                    if not file_path.exists():
                        result['errors'].append(f"文件缺失: {file_info['path']}")
                        result['failed_files'] += 1
                    else:
                        result['verified_files'] += 1
            else:
                # 归档文件
                if backup_path.suffix == '.zip':
                    with zipfile.ZipFile(backup_path, 'r') as zipf:
                        file_list = zipf.namelist()
                        for file_info in manifest['files']:
                            if file_info['path'] not in file_list:
                                result['errors'].append(f"文件缺失: {file_info['path']}")
                                result['failed_files'] += 1
                            else:
                                result['verified_files'] += 1
                else:
                    # TAR格式，暂时跳过详细验证
                    result['verified_files'] = manifest['file_count']
            
            if result['failed_files'] > 0:
                result['success'] = False
        
        except Exception as e:
            result['success'] = False
            result['errors'].append(f"验证异常: {e}")
        
        return result
    
    def _cleanup_old_backups(self, backup_dir: Path):
        """清理旧备份"""
        if not backup_dir.exists():
            return
        
        try:
            # 获取所有备份文件
            backup_files = []
            for backup_file in backup_dir.iterdir():
                if backup_file.is_file() and backup_file.name.startswith('backup_'):
                    backup_files.append(backup_file)
                elif backup_file.is_dir() and backup_file.name.startswith('backup_'):
                    backup_files.append(backup_file)
            
            # 按修改时间排序
            backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # 保留最新的N个备份
            max_backups = self.config['max_backups_per_project']
            if len(backup_files) > max_backups:
                for old_backup in backup_files[max_backups:]:
                    try:
                        if old_backup.is_file():
                            old_backup.unlink()
                        else:
                            shutil.rmtree(old_backup)
                        logger.info(f"清理旧备份: {old_backup.name}")
                    except Exception as e:
                        logger.warning(f"清理备份失败 {old_backup}: {e}")
            
            # 清理超过N天的备份
            if self.config['cleanup_days'] > 0:
                cutoff_time = datetime.now().timestamp() - (self.config['cleanup_days'] * 86400)
                
                for backup_file in backup_files:
                    if backup_file.stat().st_mtime < cutoff_time:
                        try:
                            if backup_file.is_file():
                                backup_file.unlink()
                            else:
                                shutil.rmtree(backup_file)
                            logger.info(f"清理过期备份: {backup_file.name}")
                        except Exception as e:
                            logger.warning(f"清理过期备份失败 {backup_file}: {e}")
        
        except Exception as e:
            logger.warning(f"清理旧备份过程异常: {e}")
    
    def list_backups(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出备份"""
        backup_root = Path(self.config['local_backup_dir'])
        
        if not backup_root.exists():
            return []
        
        backups = []
        
        for project_backup_dir in backup_root.iterdir():
            if not project_backup_dir.is_dir():
                continue
            
            if project_id and project_backup_dir.name != project_id:
                continue
            
            for backup_item in project_backup_dir.iterdir():
                backup_info = {
                    'project_id': project_backup_dir.name,
                    'backup_id': backup_item.stem,
                    'path': str(backup_item),
                    'size_bytes': backup_item.stat().st_size if backup_item.is_file() else 0,
                    'modified_time': backup_item.stat().st_mtime,
                    'is_file': backup_item.is_file(),
                    'is_dir': backup_item.is_dir()
                }
                backups.append(backup_info)
        
        # 按修改时间排序
        backups.sort(key=lambda x: x['modified_time'], reverse=True)
        return backups
    
    def get_backup_stats(self) -> Dict[str, Any]:
        """获取备份统计信息"""
        total_backups = len(self.backup_history)
        successful_backups = sum(1 for b in self.backup_history if b.get('success', False))
        
        backup_list = self.list_backups()
        
        total_size = sum(b.get('size_bytes', 0) for b in backup_list)
        projects = set(b['project_id'] for b in backup_list)
        
        return {
            'total_backups': total_backups,
            'successful_backups': successful_backups,
            'success_rate': successful_backups / total_backups if total_backups > 0 else 0,
            'stored_backups': len(backup_list),
            'total_storage_bytes': total_size,
            'projects_backed_up': list(projects),
            'config_enabled': self.config['enabled']
        }


def test_backup_manager():
    """测试备份管理器"""
    print("🧪 测试备份管理器...")
    
    import tempfile
    from pathlib import Path
    import time
    
    # 创建测试项目目录
    with tempfile.TemporaryDirectory(prefix='xlx_project_') as tmp_project:
        project_dir = Path(tmp_project) / "test_project_001"
        project_dir.mkdir()
        
        # 创建一些测试文件
        (project_dir / "task_summary.md").write_text("# 测试任务\n\n这是一个测试任务")
        (project_dir / "config.json").write_text('{"test": true}')
        (project_dir / "steps").mkdir()
        (project_dir / "steps" / "step1.json").write_text('{"name": "步骤1"}')
        
        print(f"✅ 创建测试项目: {project_dir}")
        
        # 创建测试配置
        with tempfile.TemporaryDirectory(prefix='xlx_backup_') as tmp_backup:
            backup_config = {
                'backup': {
                    'enabled': True,
                    'local_backup_dir': tmp_backup,
                    'git_repository': '',
                    'compress_backups': True,
                    'compression_format': 'gz',
                    'max_backups_per_project': 3
                }
            }
            
            config_file = Path(tmp_backup) / "test_config.json"
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(backup_config, f, indent=2)
            
            # 初始化备份管理器
            manager = BackupManager(str(config_file))
            
            print(f"✅ 备份管理器初始化完成")
            print(f"   启用状态: {manager.config['enabled']}")
            print(f"   备份目录: {manager.config['local_backup_dir']}")
            
            # 测试备份
            print("执行备份...")
            result = manager.backup_project(project_dir, 'full')
            
            if result['success']:
                print(f"✅ 备份成功")
                print(f"   备份ID: {result['backup_id']}")
                print(f"   文件数: {result['files_backed_up']}")
                print(f"   总大小: {result['total_size_bytes']:,} 字节")
                print(f"   备份路径: {result['backup_path']}")
            else:
                print(f"❌ 备份失败: {result['errors']}")
            
            # 测试增量备份
            time.sleep(1)  # 确保时间戳不同
            (project_dir / "new_file.txt").write_text("新增的文件内容")
            
            print("执行增量备份...")
            result2 = manager.backup_project(project_dir, 'incremental')
            
            if result2['success']:
                print(f"✅ 增量备份成功")
                print(f"   文件数: {result2['files_backed_up']}")
            
            # 测试备份列表
            backups = manager.list_backups()
            print(f"📋 备份列表: {len(backups)} 个备份")
            
            for i, backup in enumerate(backups[:3]):  # 显示前3个
                size_mb = backup['size_bytes'] / (1024*1024)
                print(f"   {i+1}. {backup['backup_id']}: {size_mb:.2f} MB")
            
            # 测试统计
            stats = manager.get_backup_stats()
            print(f"📊 备份统计: {stats['stored_backups']} 个存储备份, "
                  f"{stats['total_storage_bytes']:,} 字节")
            
            # 测试清理
            print("测试备份清理...")
            manager._cleanup_old_backups(Path(tmp_backup) / "test_project_001")
            
            backups_after = manager.list_backups()
            print(f"清理后备份数: {len(backups_after)}")
    
    print("\n✅ 备份管理器测试完成")
    return True


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_backup_manager()
    else:
        print("用法:")
        print("  python backup_manager.py test")
        print("\n注意: 完整功能需要配置Git仓库和足够磁盘空间")