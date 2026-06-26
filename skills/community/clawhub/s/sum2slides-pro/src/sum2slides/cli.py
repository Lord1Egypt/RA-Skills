"""
Sum2Slides 命令行接口
"""

import os
import sys
import click
import json
from typing import Optional

from .api import Sum2Slides
from .core.validator import InputValidator


@click.group()
@click.version_option()
def cli():
    """Sum2Slides - 将文本摘要自动转换为结构化的幻灯片演示文稿"""
    pass


@cli.command()
@click.argument('text', required=False)
@click.option('--input', '-i', 'input_file', type=click.Path(exists=True),
              help='输入文件路径 (支持 .txt, .md)')
@click.option('--output', '-o', 'output_file', type=click.Path(),
              default='presentation.pptx', show_default=True,
              help='输出文件路径 (.pptx)')
@click.option('--template', '-t', type=click.Choice(['default', 'business', 'academic']),
              default='default', show_default=True, help='模板名称')
@click.option('--theme', type=click.Choice(['light', 'dark', 'colorful', 'minimal', 'professional']),
              default='light', show_default=True, help='主题名称')
@click.option('--max-slides', type=click.IntRange(1, 50),
              default=10, show_default=True, help='最大幻灯片数量')
@click.option('--font-size', type=click.IntRange(8, 72),
              default=18, show_default=True, help='字体大小')
@click.option('--language', type=click.Choice(['zh', 'en']),
              default='zh', show_default=True, help='语言代码')
@click.option('--json', 'output_json', is_flag=True,
              help='输出JSON格式而不是PPTX文件')
@click.option('--verbose', '-v', is_flag=True, help='详细输出')
def convert(text, input_file, output_file, template, theme, max_slides, 
            font_size, language, output_json, verbose):
    """将文本转换为幻灯片演示文稿"""
    
    # 验证输入
    validator = InputValidator()
    
    # 检查是否有输入
    if not text and not input_file:
        click.echo("错误: 必须提供文本内容或输入文件", err=True)
        click.echo("使用 --help 查看帮助信息")
        sys.exit(1)
    
    # 验证输出路径（如果不是JSON输出）
    if not output_json:
        result = validator.validate_output_path(output_file)
        if not result.valid:
            click.echo(f"错误: {result.message}", err=True)
            sys.exit(1)
    
    try:
        # 创建转换器
        converter = Sum2Slides({
            'template': template,
            'theme': theme,
            'max_slides': max_slides,
            'font_size': font_size,
            'language': language,
        })
        
        if verbose:
            click.echo(f"配置: {converter.get_config()}")
            click.echo(f"可用模板: {converter.get_available_templates()}")
        
        if input_file:
            # 从文件转换
            if verbose:
                click.echo(f"读取文件: {input_file}")
            
            if output_json:
                # 读取文件并转换为JSON
                with open(input_file, 'r', encoding='utf-8') as f:
                    text_content = f.read()
                json_output = converter.convert_to_json(text_content)
                click.echo(json_output)
            else:
                # 转换为PPTX文件
                converter.convert_from_file(input_file, output_file)
                if verbose:
                    click.echo(f"生成幻灯片: {output_file}")
                else:
                    click.echo(f"✓ 已生成: {output_file}")
        
        else:
            # 从文本转换
            if verbose:
                click.echo(f"处理文本: {text[:50]}...")
            
            if output_json:
                # 转换为JSON
                json_output = converter.convert_to_json(text)
                click.echo(json_output)
            else:
                # 转换为PPTX文件
                presentation = converter.convert(text, output_file)
                if verbose:
                    click.echo(f"生成 {presentation.total_slides()} 张幻灯片")
                    click.echo(f"保存到: {output_file}")
                else:
                    click.echo(f"✓ 已生成 {presentation.total_slides()} 张幻灯片: {output_file}")
    
    except Exception as e:
        click.echo(f"错误: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('input_files', nargs=-1, type=click.Path(exists=True))
@click.option('--output-dir', '-o', type=click.Path(),
              default='./output', show_default=True,
              help='输出目录')
@click.option('--template', '-t', type=click.Choice(['default', 'business', 'academic']),
              default='default', show_default=True, help='模板名称')
@click.option('--verbose', '-v', is_flag=True, help='详细输出')
def batch(input_files, output_dir, template, verbose):
    """批量转换多个文件"""
    
    if not input_files:
        click.echo("错误: 必须提供至少一个输入文件", err=True)
        click.echo("使用 --help 查看帮助信息")
        sys.exit(1)
    
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        if verbose:
            click.echo(f"创建输出目录: {output_dir}")
    
    # 验证文件
    validator = InputValidator()
    valid_files = []
    
    for input_file in input_files:
        result = validator.validate_file(input_file)
        if not result.valid:
            click.echo(f"跳过文件 {input_file}: {result.message}", err=True)
        else:
            valid_files.append(input_file)
    
    if not valid_files:
        click.echo("错误: 没有有效的输入文件", err=True)
        sys.exit(1)
    
    try:
        # 创建转换器
        converter = Sum2Slides({
            'template': template,
        })
        
        if verbose:
            click.echo(f"批量处理 {len(valid_files)} 个文件")
            click.echo(f"输出目录: {output_dir}")
        
        # 批量转换
        output_files = converter.batch_convert(valid_files, output_dir)
        
        if verbose:
            click.echo(f"成功转换 {len(output_files)} 个文件:")
            for output_file in output_files:
                click.echo(f"  ✓ {output_file}")
        else:
            click.echo(f"✓ 成功转换 {len(output_files)}/{len(valid_files)} 个文件到 {output_dir}")
    
    except Exception as e:
        click.echo(f"错误: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--template', '-t', type=click.Choice(['default', 'business', 'academic']),
              default='default', show_default=True, help='模板名称')
@click.option('--output', '-o', type=click.Path(),
              default='config.json', show_default=True,
              help='配置文件输出路径')
def config(template, output):
    """生成配置文件示例"""
    
    config_example = {
        "defaults": {
            "template": template,
            "theme": "light",
            "max_slides": 10,
            "font_size": 18,
            "language": "zh"
        },
        "templates": {
            "default": {
                "path": "",
                "description": "默认模板"
            },
            "business": {
                "path": "",
                "description": "商务模板"
            },
            "academic": {
                "path": "",
                "description": "学术模板"
            }
        },
        "themes": {
            "light": {
                "primary_color": "#2c3e50",
                "secondary_color": "#3498db",
                "background_color": "#ffffff",
                "text_color": "#333333"
            },
            "dark": {
                "primary_color": "#ecf0f1",
                "secondary_color": "#3498db",
                "background_color": "#2c3e50",
                "text_color": "#ecf0f1"
            }
        }
    }
    
    try:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(config_example, f, indent=2, ensure_ascii=False)
        
        click.echo(f"✓ 配置文件已生成: {output}")
    
    except Exception as e:
        click.echo(f"错误: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
def templates():
    """列出可用模板"""
    
    converter = Sum2Slides()
    templates = converter.get_available_templates()
    
    click.echo("可用模板:")
    for template in templates:
        click.echo(f"  • {template}")
    
    click.echo("\n使用示例:")
    click.echo("  sum2slides convert '你的文本' --template business")
    click.echo("  sum2slides convert --input notes.txt --template academic")


@cli.command()
def validate():
    """验证安装和环境"""
    
    click.echo("验证 Sum2Slides 安装...")
    
    # 检查Python版本
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    click.echo(f"✓ Python 版本: {python_version}")
    
    # 检查必需模块
    required_modules = [
        ('pptx', 'python-pptx'),
        ('markdown', 'markdown'),
        ('pydantic', 'pydantic'),
        ('click', 'click'),
    ]
    
    all_ok = True
    for module_name, display_name in required_modules:
        try:
            __import__(module_name)
            click.echo(f"✓ {display_name} 已安装")
        except ImportError:
            click.echo(f"✗ {display_name} 未安装")
            all_ok = False
    
    if all_ok:
        click.echo("\n✓ 所有依赖已安装，Sum2Slides 可以正常工作")
    else:
        click.echo("\n✗ 缺少依赖，请运行: pip install -r requirements.txt")
        sys.exit(1)


def main():
    """主函数"""
    cli()


if __name__ == '__main__':
    main()