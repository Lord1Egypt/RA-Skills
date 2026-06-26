import os
import sys
import click
from quark_lazy_cli.app import QasLazyCli
from quark_lazy_cli.config import get_settings

# 统一设置
CONTEXT_SETTINGS = dict(help_option_names=["--help"])

class OrderedGroup(click.Group):
    """
    深度定制的 Group 类：
    1. 强制修改 Usage 字符串
    2. 调整帮助文档顺序：Usage -> Help -> Commands -> Options
    3. 修复对齐问题
    """
    def __init__(self, *args, **kwargs):
        self.custom_usage = kwargs.pop("custom_usage", "")
        super().__init__(*args, **kwargs)

    def collect_usage_pieces(self, ctx):
        if self.custom_usage:
            return [self.custom_usage]
        return super().collect_usage_pieces(ctx)

    def format_help(self, ctx, formatter):
        """完全接管渲染，确保 Commands 和 Options 块独立且对齐[cite: 1]"""
        self.format_usage(ctx, formatter)
        self.format_help_text(ctx, formatter)
        
        # 1. 渲染 Commands 部分[cite: 1]
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            if cmd is None or cmd.hidden:
                continue
            # 获取定义的 short_help (如 "all [TASK_NAME]")[cite: 1]
            commands.append((subcommand, cmd.get_short_help_str()))
        
        if commands:
            with formatter.section("Commands"):
                formatter.write_dl(commands)
        
        # 2. 渲染 Options 部分[cite: 1]
        # 注意：这里必须提取真实的 help records 才能触发 Click 的自动对齐[cite: 1]
        opts = []
        for param in self.get_params(ctx):
            rv = param.get_help_record(ctx)
            if rv is not None:
                opts.append(rv)
        
        if opts:
            with formatter.section("Options"):
                formatter.write_dl(opts)
        
        self.format_epilog(ctx, formatter)

def _get_app(ctx, env=None):
    """延迟初始化 APP"""
    if "APP" not in ctx.obj:
        cfg = get_settings(env)
        ctx.obj["APP"] = QasLazyCli(host=cfg.qas_host, token=cfg.qas_token)
    return ctx.obj["APP"]

def _resolve_params(ctx, **local_kwargs):
    """参数合并逻辑[cite: 1]"""
    group_params = ctx.obj.get("group_params", {})
    final_params = {}
    for key, val in local_kwargs.items():
        final_params[key] = val if val is not None else group_params.get(key)
    return final_params

def update_shared_options(f):
    """通用的业务 Options[cite: 1]"""
    # 调整顺序，让 env 和 help 出现在最后面更美观[cite: 1]

    f = click.option("--url", metavar="", help="指定分享资源URL，格式: https://pan.quark.cn/s/xxx?pwd=xx&maxep=79，跳过搜索直接转存目标剧集")(f)
    f = click.option("--add-prompt", metavar="", help="LLM顾问的附加指令")(f)
    f = click.option("--env", type=click.Path(exists=True), metavar="", help=".env配置文件的全路径")(f)

    return f

@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
    """QAS Lazy CLI 工具"""
    ctx.ensure_object(dict)

# --- 1. Update 组 ---

@cli.group(
    name="update", 
    cls=OrderedGroup, 
    custom_usage="[COMMAND] [TASK_NAME] [OPTIONS]",
    help="剧集更新命令。"
)
@update_shared_options
@click.pass_context
def update_group(ctx, **kwargs):
    ctx.obj["group_params"] = kwargs

@update_group.command(name="all", short_help="all [TASK_NAME] 执行缺失剧集补全和更新新剧集")
@click.argument("identifier")
@update_shared_options
@click.pass_context
def update_all(ctx, identifier, **kwargs):
    """全量更新[cite: 1]"""
    ctx.command.get_usage = lambda ctx: f"qslazy update all {identifier} [OPTIONS]"
    params = _resolve_params(ctx, **kwargs)
    app = _get_app(ctx, params["env"])
    app._handle_update_command(identifier, params["url"], "all", params["add_prompt"])

@update_group.command(name="new", short_help="new [TASK_NAME] 执行更新新剧集")
@click.argument("identifier")
@update_shared_options
@click.pass_context
def update_new(ctx, identifier, **kwargs):
    """增量更新[cite: 1]"""
    ctx.command.get_usage = lambda ctx: f"qslazy update new {identifier} [OPTIONS]"
    params = _resolve_params(ctx, **kwargs)
    app = _get_app(ctx, params["env"])
    app._handle_update_command(identifier, params["url"], "new", params["add_prompt"])

# --- 2. Task 组 ---

@cli.group(
    name="task", 
    cls=OrderedGroup, 
    custom_usage="[COMMAND] [TASK_NAME] [OPTIONS]",
    help="任务管理命令。"
)
@click.option("--env", type=click.Path(exists=True), metavar="", help=".env配置文件的全路径")
@click.pass_context
def task_group(ctx, env):
    ctx.obj["group_env"] = env

@task_group.command(name="list", short_help="查看订阅任务列表")
@click.option("--env", type=click.Path(exists=True), metavar="", help=".env配置文件的全路径")
@click.pass_context
def task_list(ctx, env):
    """查看订阅任务列表[cite: 1]"""
    ctx.command.get_usage = lambda ctx: "qslazy task list [OPTIONS]"
    target_env = env if env else ctx.obj.get("group_env")
    _get_app(ctx, target_env).task_list()

@task_group.command(name="status", short_help="status [TASK_NAME] 查看特定订阅任务状态")
@click.argument("identifier")
@click.option("--env", type=click.Path(exists=True), metavar="", help=".env配置文件的全路径")
@click.pass_context
def task_status(ctx, identifier, env):
    """查看特定任务状态[cite: 1]"""
    ctx.command.get_usage = lambda ctx: "qslazy task status [TASK_NAME] [OPTIONS]"
    target_env = env if env else ctx.obj.get("group_env")
    _get_app(ctx, target_env).task_status(identifier)

if __name__ == "__main__":
    cli()