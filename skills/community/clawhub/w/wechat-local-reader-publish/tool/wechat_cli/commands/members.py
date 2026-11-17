"""members 命令 — 查询群聊成员列表"""

import click

from ..core.contacts import get_contact_names, resolve_username, get_group_members
from ..output.formatter import output


@click.command("members")
@click.argument("group_name")
@click.option("--format", "fmt", default="json", type=click.Choice(["json", "text"]), help="输出格式")
@click.pass_context
def members(ctx, group_name, fmt):
    """查询群聊成员列表

    \b
    示例:
      wechat-cli members "AI交流群"
      wechat-cli members "群名" --format text
    """
    app = ctx.obj

    username = resolve_username(group_name, app.cache, app.decrypted_dir)
    if not username:
        click.echo(f"找不到: {group_name}", err=True)
        ctx.exit(1)

    if '@chatroom' not in username:
        click.echo(f"{group_name} 不是一个群聊", err=True)
        ctx.exit(1)

    names = get_contact_names(app.cache, app.decrypted_dir)
    display_name = names.get(username, username)

    result = get_group_members(username, app.cache, app.decrypted_dir)

    if fmt == 'json':
        output({
            'group': display_name,
            'username': username,
            'member_count': len(result['members']),
            'owner': result['owner'],
            'members': result['members'],
        }, 'json')
    else:
        lines = [f"{m['display_name']}  ({m['username']})"]
        if m['remark']:
            lines[-1] += f"  备注: {m['remark']}"
        header = f"{display_name} 的群成员（共 {len(result['members'])} 人）"
        if result['owner']:
            header += f"，群主: {result['owner']}"
        output(header + ":\n\n" + "\n".join(lines), 'text')
