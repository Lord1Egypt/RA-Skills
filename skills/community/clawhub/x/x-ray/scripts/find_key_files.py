from pathlib import Path
import json
import sys

KEY_FILE_RULES = {
    "README.md": "项目说明",
    "README": "项目说明",

    "package.json": "Node.js 项目配置",
    "pyproject.toml": "Python 项目配置",
    "requirements.txt": "Python 依赖",
    "Cargo.toml": "Rust 项目配置",
    "go.mod": "Go 项目配置",

    "Dockerfile": "容器部署",
    "docker-compose.yml": "容器编排",
    "docker-compose.yaml": "容器编排",

    "next.config.js": "Next.js 配置",
    "next.config.mjs": "Next.js 配置",
    "next.config.ts": "Next.js 配置",

    "vite.config.js": "Vite 配置",
    "vite.config.ts": "Vite 配置",

    "tsconfig.json": "TypeScript 配置",

    "prisma/schema.prisma": "数据库模型",

    "src/main.py": "Python 程序入口",
    "main.py": "Python 程序入口",

    "src/main.ts": "程序入口",
    "src/main.tsx": "前端程序入口",

    "src/app/layout.tsx": "Next.js 根布局",
    "src/app/page.tsx": "Next.js 首页",

    "middleware.ts": "中间件",
    "middleware.js": "中间件",
}


def find_key_files(root: Path):
    key_files = []

    for relative_path, reason in KEY_FILE_RULES.items():
        path = root / relative_path

        if path.exists():
            key_files.append({
                "path": relative_path,
                "reason": reason
            })

    return {
        "key_files": key_files
    }


def main():
    target = Path(
        sys.argv[1] if len(sys.argv) > 1 else "."
    ).resolve()

    result = find_key_files(target)

    print(json.dumps(
        result,
        ensure_ascii=False,
        indent=2
    ))


if __name__ == "__main__":
    main()