#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
教学文档智能生成工具
中小学课件、教案、任务单生成
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# Windows 终端编码修复
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class TeachingMaterialsGenerator:
    """教学文档生成器"""

    # 支持的教育平台配置
    PLATFORMS = {
        "bakclass": {
            "name": "贝壳网",
            "url": "https://www.bakclass.com/",
            "description": "湖南教育出版社资源平台"
        },
        "smartedu": {
            "name": "中小学智慧教育平台",
            "url": "https://basic.smartedu.cn/",
            "description": "国家官方教育资源平台"
        },
        "zxxk": {
            "name": "学科网",
            "url": "https://www.zxxk.com/",
            "description": "中小学教育资源库"
        },
        "21cnjy": {
            "name": "21世纪教育网",
            "url": "https://www.21cnjy.com/",
            "description": "中小学教育资源平台"
        }
    }

    def __init__(self, workspace=None):
        """
        初始化生成器

        Args:
            workspace: 工作空间路径，默认为当前目录
        """
        if workspace is None:
            workspace = os.getcwd()

        self.workspace = Path(workspace)
        self.teacher_dir = self.workspace / "MyTeacher"
        self.templates_dir = Path(__file__).parent / "references"
        self.accounts_file = self.workspace / ".workbuddy" / "teaching-materials-accounts.json"

        # 检查并加载账号配置
        self.accounts = self._load_accounts()

    def _load_accounts(self):
        """
        加载账号配置
        如果配置文件不存在，返回空字典
        """
        if self.accounts_file.exists():
            try:
                with open(self.accounts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"警告: 读取账号配置文件失败: {e}")
                return {}
        return {}

    def check_first_time_setup(self):
        """
        检查是否是首次使用
        如果是，返回需要配置的平台列表
        """
        if not self.accounts_file.exists():
            return list(self.PLATFORMS.keys())
        
        # 检查哪些平台还没有配置
        missing_platforms = []
        for key, platform in self.PLATFORMS.items():
            if key not in self.accounts or not self.accounts[key].get("username"):
                missing_platforms.append(key)
        
        return missing_platforms

    def save_accounts(self, accounts_data):
        """
        保存账号配置到文件

        Args:
            accounts_data: 账号数据字典
        """
        # 确保目录存在
        self.accounts_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(self.accounts_file, 'w', encoding='utf-8') as f:
                json.dump(accounts_data, f, ensure_ascii=False, indent=2)
            print(f"✓ 账号配置已保存到: {self.accounts_file}")
            self.accounts = accounts_data
        except Exception as e:
            print(f"错误: 保存账号配置失败: {e}")

    def get_account_setup_prompt(self):
        """
        获取账号配置询问提示
        用于首次使用时向用户展示
        """
        missing = self.check_first_time_setup()
        
        if not missing:
            return None
        
        prompt_lines = [
            "\n" + "="*60,
            "欢迎使用教学资料生成技能！",
            "="*60,
            "",
            "为了帮您下载优质的教学资源，建议配置以下教育平台账号：",
            "（没有账号可直接回车跳过）",
            "",
            "需要配置的平台：",
        ]
        
        for key in missing:
            platform = self.PLATFORMS[key]
            prompt_lines.append(f"\n【{platform['name']}】")
            prompt_lines.append(f"  网址: {platform['url']}")
            prompt_lines.append(f"  说明: {platform['description']}")
        
        prompt_lines.extend([
            "",
            "-"*60,
            "账号信息将保存在您的本地工作区，不会随技能分享。",
            "="*60 + "\n"
        ])
        
        return "\n".join(prompt_lines)

    def setup_accounts_interactive(self):
        """
        交互式配置账号
        询问用户各平台的账号信息
        """
        missing = self.check_first_time_setup()
        
        if not missing:
            print("✓ 账号配置已完成，无需重复配置。")
            return self.accounts
        
        print(self.get_account_setup_prompt())
        
        accounts_data = self.accounts.copy()
        
        print("\n请按提示输入账号信息（直接回车表示跳过）：\n")
        
        for key in missing:
            platform = self.PLATFORMS[key]
            print(f"\n--- {platform['name']} ---")
            
            username = input(f"用户名: ").strip()
            if not username:
                print(f"  跳过 {platform['name']}")
                accounts_data[key] = {
                    "name": platform["name"],
                    "url": platform["url"],
                    "username": "",
                    "password": "",
                    "description": platform["description"]
                }
                continue
            
            password = input(f"密码: ").strip()
            
            accounts_data[key] = {
                "name": platform["name"],
                "url": platform["url"],
                "username": username,
                "password": password,
                "description": platform["description"]
            }
            print(f"  ✓ {platform['name']} 账号已记录")
        
        # 保存配置
        self.save_accounts(accounts_data)
        
        print("\n" + "="*60)
        print("账号配置完成！")
        print(f"配置已保存到: {self.accounts_file}")
        print("="*60 + "\n")
        
        return accounts_data

    # 学科配色方案
    colors = {
            "语文_古诗词": {
                "primary": "#8B0000",   # 深红
                "secondary": "#F5F5DC",  # 米色
                "accent": "#DAA520",    # 金色
                "background": "#FAF8EF"  # 浅米色
            },
            "语文_现代文": {
                "primary": "#2E86AB",   # 蓝色
                "secondary": "#A23B72",  # 紫红
                "accent": "#F18F01",    # 橙色
                "background": "#FFFFFF"
            },
            "数学": {
                "primary": "#0D9488",   # 青绿
                "secondary": "#065F46",  # 深绿
                "accent": "#F97316",    # 橙色
                "background": "#FAFAF9"
            },
            "英语": {
                "primary": "#6366F1",   # 靛蓝
                "secondary": "#8B5CF6",  # 紫色
                "accent": "#EC4899",    # 粉色
                "background": "#F8F9FA"
            },
            "复习课": {
                "primary": "#1E2761",   # 深蓝
                "secondary": "#CADCFC",  # 冰蓝
                "accent": "#FFFFFF",    # 白色
                "background": "#0F172A"
            }
        }

    def generate_folder_name(self, grade, unit, lesson_num, lesson_name):
        """
        生成课程文件夹名称

        Args:
            grade: 年级 (如: 五上, 五下, 六年级)
            unit: 单元 (如: 第一单元, Unit1)
            lesson_num: 课序 (如: 第1课)
            lesson_name: 课程名 (如: 古诗三首)

        Returns:
            文件夹名称
        """
        return f"{grade}_{unit}_{lesson_num}_{lesson_name}"

    def create_course_folder(self, folder_name):
        """
        创建课程文件夹结构

        Args:
            folder_name: 课程文件夹名称

        Returns:
            文件夹路径
        """
        course_dir = self.teacher_dir / folder_name
        course_dir.mkdir(parents=True, exist_ok=True)

        # 创建子文件夹
        (course_dir / "参考资源").mkdir(exist_ok=True)
        (course_dir / "参考资源" / "images").mkdir(exist_ok=True)

        return course_dir

    def load_template(self, template_name):
        """
        加载模板文件

        Args:
            template_name: 模板文件名

        Returns:
            模板内容
        """
        template_file = self.templates_dir / template_name
        if template_file.exists():
            return template_file.read_text(encoding='utf-8')
        else:
            raise FileNotFoundError(f"模板文件不存在: {template_file}")

    def generate_teaching_design(self, info):
        """
        生成教学设计（教案）

        Args:
            info: 教学信息字典，包含:
                - grade: 年级
                - unit: 单元
                - lesson_num: 课序
                - lesson_name: 课程名
                - subject: 学科 (语文/数学)
                - textbook: 教材版本
                - class_type: 课型 (新授课/复习课/练习课)
                - duration: 课时
                - student_level: 学生学情
                - teacher: 授课教师
                - class_name: 授课班级

        Returns:
            生成的教案内容（Markdown格式）
        """
        template = self.load_template("teaching_design_template.md")

        # 替换模板中的占位符
        content = template
        content = content.replace("___", info.get("lesson_name", ""))
        content = content.replace("___", info.get("teacher", ""))
        content = content.replace("___", info.get("class_name", ""))
        content = content.replace("___", datetime.now().strftime("%Y年%m月%d日"))

        # TODO: 这里需要 AI 来填充具体内容
        # 当前只是简单替换，实际使用时需要调用 docx skill 或直接生成 Word 文件

        return content

    def generate_task_sheet(self, info):
        """
        生成学生任务单（导学案）

        Args:
            info: 教学信息字典

        Returns:
            生成的任务单内容（Markdown格式）
        """
        template = self.load_template("task_sheet_template.md")

        content = template
        content = content.replace("___", info.get("lesson_name", ""))
        content = content.replace("___", info.get("class_name", ""))

        # TODO: 同样需要 AI 填充具体内容

        return content

    def get_color_scheme(self, subject, lesson_type="新授课"):
        """
        获取配色方案

        Args:
            subject: 学科
            lesson_type: 课型

        Returns:
            配色字典
        """
        key = f"{subject}_{lesson_type}" if lesson_type == "古诗词" else subject
        return self.colors.get(key, self.colors["数学"])

    def print_info(self, info):
        """
        打印教学信息

        Args:
            info: 教学信息字典
        """
        print("\n" + "="*50)
        print("教学信息确认")
        print("="*50)
        print(f"年级: {info.get('grade')}")
        print(f"单元: {info.get('unit')}")
        print(f"课序: {info.get('lesson_num')}")
        print(f"课程名: {info.get('lesson_name')}")
        print(f"学科: {info.get('subject')}")
        print(f"教材版本: {info.get('textbook')}")
        print(f"课型: {info.get('class_type')}")
        print(f"课时: {info.get('duration')}")
        print(f"授课教师: {info.get('teacher')}")
        print(f"授课班级: {info.get('class_name')}")
        print("="*50 + "\n")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="教学文档智能生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:

1. 生成完整教学文档（需要 AI 辅助）:
   python teaching_materials.py \\
       --grade "五上" \\
       --unit "第一单元" \\
       --lesson_num "第1课" \\
       --lesson_name "古诗三首" \\
       --subject "语文" \\
       --class_type "新授课" \\
       --teacher "张老师" \\
       --class_name "五(1)班"

2. 创建课程文件夹结构:
   python teaching_materials.py \\
       --create-folder \\
       --grade "五上" \\
       --unit "第一单元" \\
       --lesson_num "第1课" \\
       --lesson_name "古诗三首"

3. 查看帮助:
   python teaching_materials.py --help
        """
    )

    parser.add_argument("--grade", help="年级 (如: 五上, 五下, 六年级)")
    parser.add_argument("--unit", help="单元 (如: 第一单元, Unit1)")
    parser.add_argument("--lesson_num", help="课序 (如: 第1课)")
    parser.add_argument("--lesson_name", help="课程名")
    parser.add_argument("--subject", help="学科 (语文/数学)", choices=["语文", "数学"])
    parser.add_argument("--textbook", help="教材版本 (如: 人教版)", default="人教版")
    parser.add_argument("--class_type", help="课型 (新授课/复习课/练习课)",
                       default="新授课", choices=["新授课", "复习课", "练习课"])
    parser.add_argument("--duration", help="课时 (如: 1课时)", default="1课时")
    parser.add_argument("--teacher", help="授课教师", default="")
    parser.add_argument("--class_name", help="授课班级", default="")
    parser.add_argument("--workspace", help="工作空间路径", default=None)

    # 操作类型
    parser.add_argument("--create-folder", action="store_true",
                       help="仅创建文件夹结构")
    parser.add_argument("--generate-design", action="store_true",
                       help="生成教学设计")
    parser.add_argument("--generate-task", action="store_true",
                       help="生成任务单")
    parser.add_argument("--setup-accounts", action="store_true",
                       help="配置教育平台账号（首次使用）")

    args = parser.parse_args()

    # 处理账号配置
    if args.setup_accounts:
        generator = TeachingMaterialsGenerator(workspace=args.workspace)
        generator.setup_accounts_interactive()
        return

    # 初始化生成器
    generator = TeachingMaterialsGenerator(workspace=args.workspace)

    # 检查是否是首次使用，如果是则引导配置账号
    missing_platforms = generator.check_first_time_setup()
    if missing_platforms:
        print("\n" + "="*60)
        print("首次使用检测")
        print("="*60)
        print(f"\n检测到您有 {len(missing_platforms)} 个平台尚未配置账号：")
        for key in missing_platforms:
            platform = generator.PLATFORMS[key]
            print(f"  - {platform['name']}: {platform['description']}")
        print("\n您可以使用以下命令配置账号：")
        print("  python teaching_materials.py --setup-accounts")
        print("="*60 + "\n")

    # 生成文件夹名称
    folder_name = generator.generate_folder_name(
        args.grade,
        args.unit,
        args.lesson_num,
        args.lesson_name
    )

    # 创建文件夹
    course_dir = generator.create_course_folder(folder_name)
    print(f"✓ 课程文件夹已创建: {course_dir}")

    # 收集教学信息
    info = {
        "grade": args.grade,
        "unit": args.unit,
        "lesson_num": args.lesson_num,
        "lesson_name": args.lesson_name,
        "subject": args.subject,
        "textbook": args.textbook,
        "class_type": args.class_type,
        "duration": args.duration,
        "teacher": args.teacher,
        "class_name": args.class_name
    }

    # 根据参数执行相应操作
    if args.create_folder:
        print("\n仅创建了文件夹结构。")
        print("如需生成完整文档，请结合 AI 助手使用。")
    elif args.generate_design:
        generator.print_info(info)
        design_content = generator.generate_teaching_design(info)
        design_file = course_dir / f"{args.lesson_name}_教学设计.md"
        design_file.write_text(design_content, encoding='utf-8')
        print(f"✓ 教学设计已生成: {design_file}")
        print("\n注意: 当前版本生成的是 Markdown 模板，")
        print("请使用 AI 助手或 docx skill 转换为 Word 格式。")
    elif args.generate_task:
        generator.print_info(info)
        task_content = generator.generate_task_sheet(info)
        task_file = course_dir / f"{args.lesson_name}_任务单.md"
        task_file.write_text(task_content, encoding='utf-8')
        print(f"✓ 任务单已生成: {task_file}")
        print("\n注意: 当前版本生成的是 Markdown 模板，")
        print("请使用 AI 助手或 docx skill 转换为 Word 格式。")
    else:
        # 默认显示帮助
        print("请指定要执行的操作。")
        print("\n使用示例:")
        print("  --create-folder     仅创建文件夹结构")
        print("  --generate-design   生成教学设计")
        print("  --generate-task     生成任务单")
        print("\n完整功能请结合 AI 助手使用。")
        parser.print_help()


if __name__ == "__main__":
    main()
