#!/usr/bin/env python3
"""
SQL 拆分工具 - 配置文件管理模块
支持保存和加载常用配置
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Optional, List, Any
from dataclasses import dataclass, asdict, field


@dataclass
class SplitConfig:
    """拆分配置"""
    # 基本配置
    dialect: str = "auto"
    output_dir: str = ""
    verbose: bool = True
    dry_run: bool = False
    no_merge: bool = False
    show_progress: bool = True

    # 高级配置
    max_workers: int = 4
    use_checkpoint: bool = True
    checkpoint_dir: str = ""

    # 输出配置
    output_format: str = "sql"  # sql, txt, md
    include_comments: bool = True
    include_stats: bool = True

    # 过滤配置
    include_types: List[str] = field(default_factory=list)
    exclude_types: List[str] = field(default_factory=list)
    include_patterns: List[str] = field(default_factory=list)
    exclude_patterns: List[str] = field(default_factory=list)

    # 其他配置
    encoding: str = "utf-8"
    line_ending: str = "\n"

    def to_dict(self) -> dict:
        """转换为字典"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'SplitConfig':
        """从字典创建"""
        return cls(**data)

    def validate(self) -> List[str]:
        """
        验证配置

        Returns:
            错误信息列表
        """
        errors = []

        # 验证方言
        valid_dialects = ["auto", "mysql", "postgresql", "oracle", "sqlserver", "dm", "generic"]
        if self.dialect not in valid_dialects:
            errors.append(f"无效的方言: {self.dialect}")

        # 验证输出格式
        valid_formats = ["sql", "txt", "md"]
        if self.output_format not in valid_formats:
            errors.append(f"无效的输出格式: {self.output_format}")

        # 验证编码
        try:
            "test".encode(self.encoding)
        except LookupError:
            errors.append(f"无效的编码: {self.encoding}")

        # 验证行结束符
        if self.line_ending not in ["\n", "\r\n", "\r"]:
            errors.append(f"无效的行结束符: {repr(self.line_ending)}")

        return errors


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_dir: Optional[Path] = None):
        """
        初始化配置管理器

        Args:
            config_dir: 配置目录，默认为 ~/.sql_splitter_configs
        """
        if config_dir is None:
            config_dir = Path.home() / ".sql_splitter_configs"

        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # 默认配置文件
        self.default_config_file = self.config_dir / "default.json"

    def get_config_file(self, name: str) -> Path:
        """
        获取配置文件路径

        Args:
            name: 配置名称

        Returns:
            配置文件路径
        """
        return self.config_dir / f"{name}.json"

    def save_config(self, config: SplitConfig, name: str = "default") -> bool:
        """
        保存配置

        Args:
            config: 配置
            name: 配置名称

        Returns:
            是否保存成功
        """
        try:
            config_file = self.get_config_file(name)

            # 验证配置
            errors = config.validate()
            if errors:
                print(f"配置验证失败: {', '.join(errors)}")
                return False

            # 保存配置
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config.to_dict(), f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False

    def load_config(self, name: str = "default") -> Optional[SplitConfig]:
        """
        加载配置

        Args:
            name: 配置名称

        Returns:
            配置，如果不存在则返回 None
        """
        try:
            config_file = self.get_config_file(name)
            if not config_file.exists():
                return None

            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return SplitConfig.from_dict(data)
        except Exception as e:
            print(f"加载配置失败: {e}")
            return None

    def list_configs(self) -> List[Dict[str, Any]]:
        """
        列出所有配置

        Returns:
            配置列表
        """
        configs = []

        for config_file in self.config_dir.glob("*.json"):
            try:
                name = config_file.stem
                config = self.load_config(name)
                if config:
                    configs.append({
                        'name': name,
                        'dialect': config.dialect,
                        'output_dir': config.output_dir,
                        'max_workers': config.max_workers,
                        'use_checkpoint': config.use_checkpoint,
                        'file': str(config_file)
                    })
            except Exception as e:
                print(f"读取配置失败 {config_file}: {e}")

        return configs

    def delete_config(self, name: str) -> bool:
        """
        删除配置

        Args:
            name: 配置名称

        Returns:
            是否删除成功
        """
        try:
            config_file = self.get_config_file(name)
            if config_file.exists():
                config_file.unlink()
            return True
        except Exception as e:
            print(f"删除配置失败: {e}")
            return False

    def export_config(self, name: str, export_path: str, format: str = "json") -> bool:
        """
        导出配置

        Args:
            name: 配置名称
            export_path: 导出路径
            format: 导出格式 (json, yaml)

        Returns:
            是否导出成功
        """
        try:
            config = self.load_config(name)
            if not config:
                print(f"配置不存在: {name}")
                return False

            export_file = Path(export_path)

            if format == "json":
                with open(export_file, 'w', encoding='utf-8') as f:
                    json.dump(config.to_dict(), f, indent=2, ensure_ascii=False)
            elif format == "yaml":
                with open(export_file, 'w', encoding='utf-8') as f:
                    yaml.dump(config.to_dict(), f, allow_unicode=True)
            else:
                print(f"不支持的导出格式: {format}")
                return False

            return True
        except Exception as e:
            print(f"导出配置失败: {e}")
            return False

    def import_config(self, import_path: str, name: str) -> bool:
        """
        导入配置

        Args:
            import_path: 导入路径
            name: 配置名称

        Returns:
            是否导入成功
        """
        try:
            import_file = Path(import_path)
            if not import_file.exists():
                print(f"文件不存在: {import_path}")
                return False

            # 根据文件扩展名确定格式
            if import_file.suffix == ".json":
                with open(import_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            elif import_file.suffix in [".yaml", ".yml"]:
                with open(import_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
            else:
                print(f"不支持的文件格式: {import_file.suffix}")
                return False

            config = SplitConfig.from_dict(data)

            # 验证配置
            errors = config.validate()
            if errors:
                print(f"配置验证失败: {', '.join(errors)}")
                return False

            return self.save_config(config, name)
        except Exception as e:
            print(f"导入配置失败: {e}")
            return False

    def create_default_config(self) -> SplitConfig:
        """
        创建默认配置

        Returns:
            默认配置
        """
        config = SplitConfig()
        self.save_config(config, "default")
        return config

    def get_or_create_default(self) -> SplitConfig:
        """
        获取或创建默认配置

        Returns:
            默认配置
        """
        config = self.load_config("default")
        if config is None:
            config = self.create_default_config()
        return config


def main():
    """测试函数"""
    manager = ConfigManager()

    # 创建默认配置
    print("创建默认配置:")
    config = manager.get_or_create_default()
    print(f"默认配置: {config.to_dict()}")

    # 保存自定义配置
    print("\n保存自定义配置:")
    custom_config = SplitConfig(
        dialect="oracle",
        output_dir="/test/output",
        max_workers=8,
        use_checkpoint=True
    )
    manager.save_config(custom_config, "oracle")

    # 列出所有配置
    print("\n列出所有配置:")
    for cfg in manager.list_configs():
        print(f"  {cfg['name']}: {cfg['dialect']}")

    # 加载配置
    print("\n加载配置:")
    loaded_config = manager.load_config("oracle")
    if loaded_config:
        print(f"  方言: {loaded_config.dialect}")
        print(f"  输出目录: {loaded_config.output_dir}")
        print(f"  最大并发: {loaded_config.max_workers}")

    # 删除配置
    print("\n删除配置:")
    manager.delete_config("oracle")


if __name__ == "__main__":
    main()
