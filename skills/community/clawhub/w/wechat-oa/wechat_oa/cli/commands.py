import click
from wechat_oa.convert import get_converter
from wechat_oa.api import draft_create, draft_update, draft_list, draft_get, draft_delete
from wechat_oa.api import material_upload, material_count, material_list, material_delete
from wechat_oa.api import get_accounts, select_account, get_current_account, set_default_account
from wechat_oa.features import generate_cover
from wechat_oa.core.utils import validate_digest


@click.group()
def cli():
    pass


@cli.command()
@click.argument("file_path")
@click.option("--digest", default="", help="文章摘要")
@click.option("--author", default="", help="作者名")
@click.option("--force-cover", is_flag=True, help="强制生成封面")
@click.option("-a", "--account", default=None, help="公众号名称")
def create(file_path, digest, author, force_cover, account):
    converter = get_converter(file_path)
    article = converter.convert(file_path, user_digest=digest)
    
    final_digest = article["digest"]
    if digest:
        final_digest, truncated = validate_digest(digest)
        if truncated:
            click.echo(f"[WARN] 摘要过长，已截断")
    
    thumb_media_id = ""
    if force_cover:
        cover_path = generate_cover(article["title"])
        click.echo(f"[COVER] 封面图已生成: {cover_path}")
        upload_result = material_upload(cover_path)
        if upload_result["success"]:
            thumb_media_id = upload_result["media_id"]
            click.echo(f"[UPLOAD] 封面图上传成功")
        else:
            click.echo(f"[WARN] 封面图上传失败: {upload_result.get('error')}")
    
    result = draft_create(
        title=article["title"],
        content=article["body"],
        author=author or article.get("author", ""),
        digest=final_digest,
        thumb_media_id=thumb_media_id,
        account_name=account
    )
    
    if result["success"]:
        click.echo(f"✅ 草稿创建成功: {result['media_id']}")
    else:
        click.echo(f"❌ 创建失败: {result.get('error')}")


@cli.command()
@click.argument("media_id")
@click.argument("file_path")
@click.option("--digest", default="", help="文章摘要")
@click.option("--author", default="", help="作者名")
@click.option("-a", "--account", default=None, help="公众号名称")
def update(media_id, file_path, digest, author, account):
    converter = get_converter(file_path)
    article = converter.convert(file_path, user_digest=digest)
    
    final_digest = article["digest"]
    if digest:
        final_digest, truncated = validate_digest(digest)
        if truncated:
            click.echo(f"[WARN] 摘要过长，已截断")
    
    result = draft_update(
        media_id=media_id,
        title=article["title"],
        content=article["body"],
        author=author or article.get("author", ""),
        digest=final_digest,
        account_name=account
    )
    
    if result["success"]:
        click.echo(f"✅ 草稿更新成功")
    else:
        click.echo(f"❌ 更新失败: {result.get('error')}")


@cli.command()
@click.option("--offset", default=0, help="偏移量")
@click.option("--count", default=20, help="数量")
@click.option("-a", "--account", default=None, help="公众号名称")
def list(offset, count, account):
    result = draft_list(offset=offset, count=count, account_name=account)
    
    if result["success"]:
        data = result.get("data", {})
        drafts = data.get("item", data.get("drafts", []))
        
        if not drafts:
            click.echo("暂无草稿")
            return
        
        for draft in drafts:
            article = draft.get("content", {}).get("news_item", [{}])[0]
            click.echo(f"{draft.get('media_id', '')} | {article.get('title', '')}")
    else:
        click.echo(f"❌ 获取失败: {result.get('error')}")


@cli.command()
@click.argument("media_id")
@click.option("-a", "--account", default=None, help="公众号名称")
def get(media_id, account):
    result = draft_get(media_id=media_id, account_name=account)
    
    if result["success"]:
        data = result.get("data", {})
        article = data.get("content", {}).get("news_item", [{}])[0]
        click.echo(f"标题: {article.get('title', '')}")
        click.echo(f"作者: {article.get('author', '')}")
        click.echo(f"摘要: {article.get('digest', '')}")
    else:
        click.echo(f"❌ 获取失败: {result.get('error')}")


@cli.command()
@click.argument("media_id")
@click.option("-a", "--account", default=None, help="公众号名称")
def delete(media_id, account):
    result = draft_delete(media_id=media_id, account_name=account)
    
    if result["success"]:
        click.echo(f"✅ 草稿删除成功")
    else:
        click.echo(f"❌ 删除失败: {result.get('error')}")


@cli.command()
@click.argument("file_path")
@click.option("--type", default="image", help="素材类型")
def upload(file_path, type):
    result = material_upload(file_path, media_type=type)
    
    if result["success"]:
        click.echo(f"✅ 素材上传成功: {result['media_id']}")
    else:
        click.echo(f"❌ 上传失败: {result.get('error')}")


@cli.command()
def count():
    result = material_count()
    
    if result["success"]:
        data = result.get("data", {})
        click.echo(f"图文素材: {data.get('news_count', 0)}")
        click.echo(f"图片素材: {data.get('image_count', 0)}")
        click.echo(f"语音素材: {data.get('voice_count', 0)}")
        click.echo(f"视频素材: {data.get('video_count', 0)}")
    else:
        click.echo(f"❌ 获取失败: {result.get('error')}")


@cli.command()
@click.option("--type", default="news", help="素材类型")
@click.option("--offset", default=0, help="偏移量")
@click.option("--count", default=20, help="数量")
def materials(type, offset, count):
    result = material_list(media_type=type, offset=offset, count=count)
    
    if result["success"]:
        data = result.get("data", {})
        items = data.get("item", [])
        
        if not items:
            click.echo("暂无素材")
            return
        
        for item in items:
            click.echo(f"{item.get('media_id', '')}")
    else:
        click.echo(f"❌ 获取失败: {result.get('error')}")


@cli.command()
@click.argument("media_id")
def del_material(media_id):
    result = material_delete(media_id=media_id)
    
    if result["success"]:
        click.echo(f"✅ 素材删除成功")
    else:
        click.echo(f"❌ 删除失败: {result.get('error')}")


@cli.command()
@click.argument("title")
@click.option("--output", default="", help="输出路径")
def cover(title, output):
    output_path = generate_cover(title, save_path=output)
    click.echo(f"✅ 封面图已生成: {output_path}")


@cli.command()
def accounts():
    result = get_accounts()
    
    if result["success"]:
        accounts_list = result.get("accounts", [])
        
        if not accounts_list:
            click.echo("暂无公众号")
            return
        
        click.echo("公众号列表:")
        click.echo("-" * 50)
        for acc in accounts_list:
            flags = []
            if acc.get("is_current"):
                flags.append("当前")
            if acc.get("is_default"):
                flags.append("默认")
            flag_str = f" [{', '.join(flags)}]" if flags else ""
            click.echo(f"{acc.get('key', '')} | {acc.get('name', '')}{flag_str}")
            if acc.get("voice_name"):
                click.echo(f"   语音名称: {', '.join(acc['voice_name'])}")
    else:
        click.echo(f"❌ 获取失败: {result.get('error')}")


@cli.command()
@click.argument("account_name")
def switch(account_name):
    result = select_account(account_name)
    
    if result["success"]:
        click.echo(f"✅ {result['message']}")
    else:
        click.echo(f"❌ {result.get('error')}")


@cli.command()
@click.argument("account_name")
def set_default(account_name):
    result = set_default_account(account_name)
    
    if result["success"]:
        click.echo(f"✅ {result['message']}")
    else:
        click.echo(f"❌ {result.get('error')}")


@cli.command()
def current():
    result = get_current_account()
    
    if result["success"]:
        click.echo(f"当前公众号: {result.get('name', '')}")
        click.echo(f"账号标识: {result.get('account_key', '')}")
        click.echo(f"作者: {result.get('author', '')}")
        click.echo(f"APP_ID: {result.get('APP_ID', '')}")
    else:
        click.echo(f"❌ {result.get('error')}")
