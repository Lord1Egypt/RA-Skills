from pathlib import Path
import json
import sys

def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def detect_stack(root: Path):
    detected = []

    # JavaScript / TypeScript
    package_json = root / "package.json"

    if package_json.exists():
        detected.append("Node.js")

        data = load_json(package_json)

        dependencies = {}
        dependencies.update(data.get("dependencies", {}))
        dependencies.update(data.get("devDependencies", {}))

        rules = {
            "react": "React",
            "next": "Next.js",
            "vue": "Vue",
            "nuxt": "Nuxt",
            "svelte": "Svelte",
            "@sveltejs/kit": "SvelteKit",
            "express": "Express",
            "fastify": "Fastify",
            "nestjs": "NestJS",
            "@nestjs/core": "NestJS",
            "tailwindcss": "Tailwind CSS",
            "prisma": "Prisma",
            "@prisma/client": "Prisma",
            "drizzle-orm": "Drizzle ORM",
            "typescript": "TypeScript",
            "vite": "Vite",
            "webpack": "Webpack",
            "vitest": "Vitest",
            "jest": "Jest",
        }

        for package_name, technology in rules.items():
            if package_name in dependencies:
                detected.append(technology)

    # Python
    if (root / "requirements.txt").exists():
        detected.append("Python")

    if (root / "pyproject.toml").exists():
        detected.append("Python")

    # Rust
    if (root / "Cargo.toml").exists():
        detected.append("Rust")

    # Go
    if (root / "go.mod").exists():
        detected.append("Go")

    # Java
    if (root / "pom.xml").exists():
        detected.append("Java / Maven")

    if (root / "build.gradle").exists():
        detected.append("Java / Gradle")

    # Docker
    if (root / "Dockerfile").exists():
        detected.append("Docker")

    if (root / "docker-compose.yml").exists():
        detected.append("Docker Compose")

    if (root / "docker-compose.yaml").exists():
        detected.append("Docker Compose")

    # 去重，同时保持顺序
    detected = list(dict.fromkeys(detected))

    return {
        "technology_stack": detected
    }


def main():
    target = Path(
        sys.argv[1] if len(sys.argv) > 1 else "."
    ).resolve()

    result = detect_stack(target)

    print(json.dumps(
        result,
        ensure_ascii=False,
        indent=2
    ))


if __name__ == "__main__":
    main()