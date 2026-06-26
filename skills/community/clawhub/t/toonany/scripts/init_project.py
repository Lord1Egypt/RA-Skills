#!/usr/bin/env python3
"""Initialize a new Toonany project. Cross-platform replacement for bash scripts."""

import argparse
import json
import os
import sys
from pathlib import Path


# Project types and art styles for interactive selection
PROJECT_TYPES = ["都市", "古风", "悬疑", "科幻", "奇幻", "武侠", "民国", "现代"]
VIDEO_RATIOS = ["16:9", "9:16", "1:1", "4:3", "3:4", "21:9"]

DEFAULT_STYLE = "2D动漫风格"
DEFAULT_TYPE = "都市"
DEFAULT_RATIO = "16:9"


def load_template(template_path: Path) -> dict:
    """Load and return template JSON data."""
    with open(template_path, "r", encoding="utf-8") as f:
        return json.load(f)


def render_template(template: dict, project_name: str) -> dict:
    """Render template with project name."""
    data = json.loads(json.dumps(template))  # Deep copy
    data["name"] = project_name
    data["createTime"] = int(__import__("time").time())
    return data


def create_project_directories(project_dir: Path) -> None:
    """Create standard project directory structure."""
    dirs = [
        "outline",
        "assets/images/characters",
        "assets/images/scenes",
        "assets/images/props",
        "script",
        "storyboard/images",
        "video",
        "audio",
        "subtitle",
        "final",
    ]
    for d in dirs:
        (project_dir / d).mkdir(parents=True, exist_ok=True)


def create_template_files(project_dir: Path) -> None:
    """Create initial template markdown files."""
    storyline_path = project_dir / "storyline.md"
    if not storyline_path.exists():
        storyline_path.write_text(
            "# 故事线\n\n"
            "## 主题\n（待填写）\n\n"
            "## 主线剧情\n（待填写）\n\n"
            "## 主要人物关系\n（待填写）\n\n"
            "## 情感基调\n（待填写）\n",
            encoding="utf-8",
        )

    assets_dir = project_dir / "assets"
    for name in ["characters", "props", "scenes"]:
        md_path = assets_dir / f"{name}.md"
        if not md_path.exists():
            md_path.write_text(
                f"# {name.capitalize()} 资产\n\n"
                "## 列表\n\n"
                "| 名称 | 描述 |\n"
                "|------|------|\n"
                "| （待填写） | |\n",
                encoding="utf-8",
            )


def prompt_input(prompt_text: str, default: str = "", choices: list[str] = None) -> str:
    """Prompt user for input with optional default and choices."""
    if choices:
        print(f"\n{prompt_text}")
        for i, choice in enumerate(choices, 1):
            marker = " (默认)" if choice == default else ""
            print(f"  {i}. {choice}{marker}")
        while True:
            user_input = input("> ").strip()
            if not user_input and default:
                return default
            if user_input.isdigit():
                idx = int(user_input) - 1
                if 0 <= idx < len(choices):
                    return choices[idx]
            if user_input in choices:
                return user_input
            print("无效选择，请重新输入。")
    else:
        full_prompt = f"{prompt_text}"
        if default:
            full_prompt += f" [{default}]: "
        else:
            full_prompt += ": "
        user_input = input(full_prompt).strip()
        return user_input if user_input else default


def interactive_config() -> dict:
    """Interactive project configuration."""
    print("=" * 50)
    print("  欢迎使用 Toonany！")
    print("  让我们创建你的漫剧项目")
    print("=" * 50)

    name = prompt_input("\n项目名称")
    while not name:
        print("项目名称不能为空。")
        name = prompt_input("项目名称")

    project_type = prompt_input("项目类型", default=DEFAULT_TYPE, choices=PROJECT_TYPES)
    art_style = prompt_input("艺术风格", default=DEFAULT_STYLE)
    video_ratio = prompt_input("视频比例", default=DEFAULT_RATIO, choices=VIDEO_RATIOS)

    episode_count_str = prompt_input("计划集数", default="1")
    try:
        episode_count = int(episode_count_str)
    except ValueError:
        episode_count = 1

    return {
        "name": name,
        "type": project_type,
        "artStyle": art_style,
        "videoRatio": video_ratio,
        "episodeCount": episode_count,
    }


def check_api_keys() -> list[dict]:
    """Check if essential API keys are configured."""
    from utils.config_loader import PROVIDER_GUIDES

    keys_to_check = [
        ("DEEPSEEK_API_KEY", "deepseek", "文本生成"),
        ("VOLC_API_KEY", "volcengine", "图像生成"),
        ("KLING_API_KEY", "kling", "视频生成"),
    ]

    missing = []
    for env_var, provider, purpose in keys_to_check:
        if not os.environ.get(env_var):
            guide = PROVIDER_GUIDES.get(provider, {})
            missing.append({
                "purpose": purpose,
                "provider": guide.get("name", provider),
                "env_var": env_var,
                "apply_url": guide.get("apply_url"),
                "guide": guide.get("guide", ""),
            })

    return missing


def print_api_key_guide(missing: list[dict]) -> None:
    """Print friendly API key configuration guide."""
    if not missing:
        print("\n✓ 所有 API Key 已配置。")
        return

    print("\n" + "=" * 50)
    print("  检测到以下 API Key 未配置")
    print("=" * 50)

    for item in missing:
        print(f"\n【{item['provider']}】- 用于 {item['purpose']}")
        if item["apply_url"]:
            print(f"申请地址: {item['apply_url']}")
        print(f"配置步骤:\n{item['guide']}")
        print(f"环境变量名: {item['env_var']}")

    print("\n" + "=" * 50)
    print("配置完成后，重新运行命令即可继续。")
    print("=" * 50)


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a new Toonany project")
    parser.add_argument("name", nargs="?", default=None, help="Project name")
    parser.add_argument("--output", "-o", default="output", help="Output directory")
    parser.add_argument("--type", default=DEFAULT_TYPE, help="Project type")
    parser.add_argument("--style", default=DEFAULT_STYLE, help="Art style")
    parser.add_argument("--ratio", default=DEFAULT_RATIO, help="Video ratio")
    parser.add_argument("--episodes", type=int, default=1, help="Episode count")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    args = parser.parse_args()

    # Determine project name
    if args.interactive or not args.name:
        config = interactive_config()
        project_name = config["name"]
        project_type = config["type"]
        art_style = config["artStyle"]
        video_ratio = config["videoRatio"]
        episode_count = config["episodeCount"]
    else:
        project_name = args.name
        project_type = args.type
        art_style = args.style
        video_ratio = args.ratio
        episode_count = args.episodes

    # Create project directory
    output_dir = Path(args.output)
    project_dir = output_dir / project_name

    if project_dir.exists():
        print(f"\n警告: 项目目录已存在: {project_dir}")
        confirm = input("是否覆盖? [y/N]: ").strip().lower()
        if confirm not in ("y", "yes"):
            print("已取消。")
            return 1

    project_dir.mkdir(parents=True, exist_ok=True)
    create_project_directories(project_dir)

    # Load and render project.json template
    skill_dir = Path(__file__).parent.parent
    template_path = skill_dir / "config" / "default-project.json"
    template = load_template(template_path)
    project_data = render_template(template, project_name)

    # Override with user choices
    project_data["type"] = project_type
    project_data["artStyle"] = art_style
    project_data["videoRatio"] = video_ratio
    project_data["episodeCount"] = episode_count

    # Write project.json
    project_json_path = project_dir / "project.json"
    with open(project_json_path, "w", encoding="utf-8") as f:
        json.dump(project_data, f, ensure_ascii=False, indent=2)

    # Create template markdown files
    create_template_files(project_dir)

    print(f"\n{'=' * 50}")
    print(f"  项目创建成功！")
    print(f"{'=' * 50}")
    print(f"  名称: {project_name}")
    print(f"  路径: {project_dir.absolute()}")
    print(f"  类型: {project_type}")
    print(f"  风格: {art_style}")
    print(f"  比例: {video_ratio}")
    print(f"  集数: {episode_count}")
    print(f"{'=' * 50}")

    # Check API keys
    missing_keys = check_api_keys()
    print_api_key_guide(missing_keys)

    if not missing_keys:
        print("\n下一步：")
        print("  1. 导入小说原文到项目目录")
        print("  2. 执行 /toonany quick 开始快速创作")
        print("  或 /toonany story 开始专业模式")

    return 0


if __name__ == "__main__":
    sys.exit(main())
