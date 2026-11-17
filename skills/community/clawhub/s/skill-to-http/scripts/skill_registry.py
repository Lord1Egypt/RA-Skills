#!/usr/bin/env python3
"""skill-to-http Skill Registry

扫描 Skill 目录，加载元信息和参数 schema，提供内存缓存。
"""

from __future__ import annotations

import json
import logging
import os
import re
from pathlib import Path

from params_generator import ParamsGenerator

logger = logging.getLogger("skill-to-http.registry")

# Frontmatter 正则：匹配 --- 包裹的 YAML 头部
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _parse_frontmatter(content: str) -> dict[str, str]:
    """解析 SKILL.md 的 YAML frontmatter。"""
    m = FRONTMATTER_RE.match(content)
    if not m:
        return {}
    yaml_text = m.group(1)
    result: dict[str, str] = {}
    for line in yaml_text.strip().split("\n"):
        line = line.strip()
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and val:
                result[key] = val
    return result


def _load_params_json(params_path: Path, required_fields: list[str] | None = None) -> dict | None:
    """安全加载 params.json，校验基本结构。"""
    try:
        if not params_path.exists():
            return None
        data = json.loads(params_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            logger.warning(f"Invalid params.json (not a dict): {params_path}")
            return None
        if required_fields:
            for field in required_fields:
                if field not in data:
                    logger.warning(f"params.json missing required field '{field}': {params_path}")
                    return None
        return data
    except json.JSONDecodeError as e:
        logger.warning(f"Invalid JSON in {params_path}: {e}")
        return None
    except Exception as e:
        logger.warning(f"Failed to load {params_path}: {e}")
        return None


class SkillRegistry:
    """Skill 注册中心。

    按 4 级查找链加载 params.json：
    1. Skill 目录自身内的 params.json
    2. data_dir/{skill_name}/params.json
    3. 模板目录 params-template/{skill_name}/params.json
    4. 自动生成（调用 params_generator）
    """

    def __init__(
        self,
        skill_dirs: list[str] | None = None,
        data_dir: str | None = None,
        expose_skills: list[str] | None = None,
        deny_skills: list[str] | None = None,
    ) -> None:
        self.skill_dirs: list[str] = skill_dirs or []
        self.data_dir: Path = Path(data_dir) if data_dir else __import__("_paths", fromlist=["DATA_DIR"]).DATA_DIR
        self.expose_skills: list[str] = expose_skills or []  # 空列表 = 不暴露任何
        # 反向黑名单：即使在 expose 内，命中 deny 也拒绝。用于 expose=["*"] 场景下排除危险 skill
        self.deny_skills: set[str] = set(deny_skills or [])
        self._skills: dict[str, dict] = {}
        self._params: dict[str, dict] = {}
        self._generator = ParamsGenerator(data_dir=str(self.data_dir))

    def scan(self) -> int:
        """扫描 skill 目录，发现并注册 Skill。
        
        当 expose_skills 指定了具体 skill 名称时（非 * 通配），
        只扫描匹配的目标目录，跳过无关 skill 以加速启动。
        """
        self._skills.clear()
        self._params.clear()

        # 确定是否按需扫描：指定了具体 skill 名（非通配）
        targeted = (
            self.expose_skills
            and "*" not in self.expose_skills
        )
        targets: set[str] | None = set(self.expose_skills) if targeted else None
        unmatched: set[str] = set(targets) if targets else set()

        for dir_path in self.skill_dirs:
            path = Path(dir_path).expanduser().resolve()
            if not path.is_dir():
                logger.debug(f"Skill dir not found, skipping: {path}")
                continue

            if targeted:
                logger.info(f"Scanning skill dir (targeted: {', '.join(sorted(targets))}): {path}")
            else:
                logger.info(f"Scanning skill dir: {path}")

            skill_md = path / "SKILL.md"
            # 修复：如果是 "skills" 汇总目录，即使根有 SKILL.md（历史残留 / 安装漏拆）
            # 也忽略它，避免吃掉整个目录的扫描。仅当目录本身明确是一个 skill 包时才注册自身。
            is_aggregate_dir = path.name in ("skills", "skill")
            if skill_md.exists() and not is_aggregate_dir:
                # 当前目录本身就是个 skill
                if not targeted or path.name in targets:
                    self._register_skill(path)
                    if targeted:
                        unmatched.discard(path.name)
            else:
                if skill_md.exists() and is_aggregate_dir:
                    logger.warning(
                        f"Ignoring SKILL.md in aggregate dir '{path}' "
                        "(treating as legacy residue; continuing to scan subdirs)"
                    )
                # 扫描子目录找 skill
                for subdir in sorted(path.iterdir()):
                    if not subdir.is_dir():
                        continue
                    # 按需扫描：跳过不匹配的目录
                    if targeted and subdir.name not in targets:
                        continue
                    if (subdir / "SKILL.md").exists():
                        self._register_skill(subdir)
                        if targeted:
                            unmatched.discard(subdir.name)

        # 如果指定了 skill 但按目录名没找到，尝试 frontmatter 兜底扫描
        if targeted and unmatched:
            logger.info(
                f"Skills not found by directory name: {', '.join(sorted(unmatched))}. "
                f"Trying frontmatter fallback..."
            )
            for dir_path in self.skill_dirs:
                path = Path(dir_path).expanduser().resolve()
                if not path.is_dir():
                    continue
                for subdir in sorted(path.iterdir()):
                    if not subdir.is_dir() or subdir.name in self._skills:
                        continue
                    skill_md = subdir / "SKILL.md"
                    if not skill_md.exists():
                        continue
                    # 只读 frontmatter 做快速匹配
                    try:
                        fm = _parse_frontmatter(
                            skill_md.read_text(encoding="utf-8", errors="replace")
                        )
                        name = fm.get("name", "")
                        if name in unmatched:
                            self._register_skill(subdir)
                            unmatched.discard(name)
                            if not unmatched:
                                break
                    except Exception:
                        pass
                if not unmatched:
                    break
            if unmatched:
                logger.warning(
                    f"Skills still not found after frontmatter fallback: "
                    f"{', '.join(sorted(unmatched))}"
                )

        count = len(self._skills)
        logger.info(f"Registered {count} skills")
        return count

    SKILL_MD_MAX_SIZE = 512 * 1024  # 512 KB

    def _register_skill(self, skill_dir: Path) -> None:
        """注册单个 Skill。"""
        skill_md_path = skill_dir / "SKILL.md"
        # 文件大小检查，防止 OOM
        try:
            file_size = skill_md_path.stat().st_size
            if file_size > self.SKILL_MD_MAX_SIZE:
                logger.warning(f"Skipping '{skill_dir.name}': SKILL.md too large ({file_size} bytes > {self.SKILL_MD_MAX_SIZE})")
                return
        except Exception:
            pass
        try:
            content = skill_md_path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            logger.warning(f"Failed to read {skill_md_path}: {e}")
            return

        frontmatter = _parse_frontmatter(content)
        name = frontmatter.get("name", skill_dir.name)

        # 跳过 skill-to-http 自身
        if name == "skill-to-http" or skill_dir.name == "skill-to-http":
            logger.debug("Skipping self-registration of skill-to-http")
            return

        self._skills[name] = {
            "name": name,
            "description": frontmatter.get("description", ""),
            "path": str(skill_dir),
            "skill_md": content,
        }

        # 加载 params
        params = self._load_params(name, skill_dir)
        if params:
            self._params[name] = params

        logger.debug(f"Registered skill: {name}")

    def _load_params(self, skill_name: str, skill_dir: Path) -> dict | None:
        """4 级查找链加载 params.json。"""
        # Level 1: Skill 目录自身
        params = _load_params_json(skill_dir / "params.json")
        if params:
            logger.debug(f"params loaded from skill dir for '{skill_name}'")
            return params

        # Level 2: data_dir/params/
        data_params = self.data_dir / "params" / skill_name / "params.json"
        params = _load_params_json(data_params)
        if params:
            logger.debug(f"params loaded from data_dir for '{skill_name}'")
            return params

        # Level 3: 模板目录
        from _paths import PARAMS_TEMPLATE_DIR; template_dir = PARAMS_TEMPLATE_DIR / skill_name
        params = _load_params_json(template_dir / "params.json")
        if params:
            logger.debug(f"params loaded from template for '{skill_name}'")
            return params

        # Level 4: 自动生成（带超时保护）
        logger.info(f"No params.json found for '{skill_name}', auto-generating...")
        skill_md = self._skills.get(skill_name, {}).get("skill_md", "")
        try:
            params = self._generator.generate(skill_name, skill_md)
        except Exception as e:
            logger.warning(f"Failed to auto-generate params for '{skill_name}': {e}")
            params = None
        if params:
            self._save_data_params(skill_name, params)
            return params

        return None

    def _save_data_params(self, skill_name: str, params: dict) -> None:
        """保存 params 到 data_dir/params/。"""
        out_dir = self.data_dir / "params" / skill_name
        out_dir.mkdir(parents=True, exist_ok=True)
        params_path = out_dir / "params.json"
        params_path.write_text(
            json.dumps(params, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        logger.info(f"Saved params to {params_path}")

    def is_exposed(self, name: str) -> bool:
        """检查 skill 是否可对外暴露。

        规则：先匹配 expose（白名单），再过 deny（反向黑名单）。
        即 expose=["*"] + deny=["im-send"] → im-send 不暴露。
        """
        # 反向黑名单优先级最高
        if name in self.deny_skills:
            return False
        if "*" in self.expose_skills:
            return True
        return name in self.expose_skills

    def list_skills(self) -> list[str]:
        """只返回白名单内的 skill。"""
        return sorted(k for k in self._skills if self.is_exposed(k))

    def get_skill(self, name: str) -> dict | None:
        """获取单个 skill 元信息（仅白名单内可访问）。"""
        if not self.is_exposed(name):
            return None
        return self._skills.get(name)

    def get_params_schema(self, name: str) -> dict | None:
        """获取 skill 的 params schema（仅白名单内可访问）。"""
        if not self.is_exposed(name):
            return None
        return self._params.get(name)

    def get_stats(self) -> dict:
        """返回统计信息。"""
        return {
            "total": len(self._skills),
            "skill_dirs": self.skill_dirs,
            "names": self.list_skills(),
        }