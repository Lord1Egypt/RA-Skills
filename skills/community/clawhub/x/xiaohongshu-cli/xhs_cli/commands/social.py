"""Social commands: follow, unfollow, favorites, following, followers."""

import click

from ..formatter import maybe_print_structured, print_info, print_success
from ._common import exit_for_error, run_client_action, structured_output_options


def _resolve_user_id(ctx, user_id: str | None) -> str:
    """Resolve user_id: use provided value or fall back to current user."""
    if user_id:
        return user_id
    info = run_client_action(ctx, lambda client: client.get_self_info())
    uid = info.get("user_id", "") if isinstance(info, dict) else ""
    if not uid:
        raise click.UsageError("Cannot determine current user_id. Please specify user_id explicitly.")
    return uid


@click.command()
@click.argument("user_id")
@structured_output_options
@click.pass_context
def follow(ctx, user_id: str, as_json: bool, as_yaml: bool):
    """Follow a user."""
    try:
        data = run_client_action(ctx, lambda client: client.follow_user(user_id))

        if not maybe_print_structured(data, as_json=as_json, as_yaml=as_yaml):
            print_success(f"Followed user {user_id}")

    except Exception as exc:
        exit_for_error(exc, as_json=as_json, as_yaml=as_yaml)


@click.command()
@click.argument("user_id")
@structured_output_options
@click.pass_context
def unfollow(ctx, user_id: str, as_json: bool, as_yaml: bool):
    """Unfollow a user."""
    try:
        data = run_client_action(ctx, lambda client: client.unfollow_user(user_id))

        if not maybe_print_structured(data, as_json=as_json, as_yaml=as_yaml):
            print_success(f"Unfollowed user {user_id}")

    except Exception as exc:
        exit_for_error(exc, as_json=as_json, as_yaml=as_yaml)


@click.command()
@click.argument("user_id", required=False, default=None)
@click.option("--cursor", default="", help="Pagination cursor")
@structured_output_options
@click.pass_context
def favorites(ctx, user_id: str | None, cursor: str, as_json: bool, as_yaml: bool):
    """List favorited (bookmarked) notes. Defaults to current user if user_id is omitted."""
    try:
        uid = _resolve_user_id(ctx, user_id)
        data = run_client_action(ctx, lambda client: client.get_user_favorites(uid, cursor=cursor))

        if not maybe_print_structured(data, as_json=as_json, as_yaml=as_yaml):
            from ..formatter import render_user_posts
            notes = data.get("notes", []) if isinstance(data, dict) else []
            render_user_posts(notes)
            if isinstance(data, dict) and data.get("has_more"):
                print_info(f"More notes — use --cursor {data.get('cursor', '')}")

    except Exception as exc:
        exit_for_error(exc, as_json=as_json, as_yaml=as_yaml)

