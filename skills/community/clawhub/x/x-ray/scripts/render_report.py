from pathlib import Path
import json
import sys


def render_report(data_path):
    # 读取扫描数据
    data = json.loads(
        Path(data_path).read_text(encoding="utf-8")
    )

    # 找到 HTML 模板
    script_dir = Path(__file__).resolve().parent
    template_path = (
        script_dir.parent
        / "assets"
        / "report-template.html"
    )

    template = template_path.read_text(
        encoding="utf-8"
    )

    project = data["project"]
    stack = data["stack"]
    complexity = data["complexity"]
    key_files = data["key_files"]

    # 技术栈
    tech_stack = ", ".join(
        stack["technology_stack"]
    )

    # 关键文件
    key_files_text = ""

    for item in key_files["key_files"]:
        key_files_text += (
            f"<p>{item['path']} —— "
            f"{item['reason']}</p>"
        )

    # 替换 HTML 里的占位符
    template = template.replace(
        "{{PROJECT_NAME}}",
        project["project_name"]
    )

    template = template.replace(
        "{{TOTAL_FILES}}",
        str(project["total_files"])
    )

    template = template.replace(
        "{{TOTAL_DIRECTORIES}}",
        str(project["total_directories"])
    )

    template = template.replace(
        "{{COMPLEXITY_SCORE}}",
        str(complexity["score"])
    )

    template = template.replace(
        "{{TECH_STACK}}",
        tech_stack
    )

    template = template.replace(
        "{{KEY_FILES}}",
        key_files_text
    )

    # 报告生成到被扫描项目旁边
    output_path = (
        Path(data_path).parent
        / "xray-report.html"
    )

    output_path.write_text(
        template,
        encoding="utf-8"
    )

    print("✅ X-ray 报告生成完成")
    print(output_path)


if __name__ == "__main__":
    render_report(sys.argv[1])