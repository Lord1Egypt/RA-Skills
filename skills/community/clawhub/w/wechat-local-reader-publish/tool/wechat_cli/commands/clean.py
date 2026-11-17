"""clean 命令 — 删除解密缓存（明文数据库），避免隐私残留"""

import click

from ..core.db_cache import DBCache


@click.command("clean")
def clean():
    """删除解密缓存（明文数据库），避免隐私明文残留于本机临时目录

    仅删除本工具在系统临时目录下生成的解密副本，不会触碰微信原始加密数据库。
    建议：在公共/共享电脑上用完本工具后执行一次；或在自动化任务里配合 --clean 使用。
    """
    removed = DBCache.clear_cache()
    if removed > 0:
        click.echo(f"[+] 已清理 {removed} 个解密缓存文件")
    else:
        click.echo("[+] 没有需要清理的解密缓存")
