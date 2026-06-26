#!/usr/bin/env python3
"""Verify weread-plus can reach the official WeRead gateway."""

from __future__ import annotations

from weread_common import WeReadError, api_post, fail, official_skill_dir, official_skill_version


EXPECTED_APIS = {
    "/review/single",
    "/book/readreviews",
    "/book/bestbookmarks",
    "/book/underlines",
    "/book/recommend",
    "/book/info",
    "/book/bookmarklist",
    "/book/chapterinfo",
    "/store/search",
    "/shelf/sync",
    "/review/list",
    "/book/getprogress",
    "/review/list/mine",
    "/readdata/detail",
    "/user/notebooks",
    "/book/similar",
}


def main() -> None:
    try:
        data = api_post("/_list", {})
    except WeReadError as exc:
        fail(str(exc))

    apis = {item.get("api_name") for item in data.get("apis") or [] if item.get("api_name")}
    missing = sorted(EXPECTED_APIS - apis)
    extra = sorted(apis - EXPECTED_APIS)

    print("weread-plus verification")
    print(f"official_skill_dir: {official_skill_dir()}")
    print(f"official_skill_version: {official_skill_version()}")
    print(f"gateway_errcode: {data.get('errcode')}")
    print(f"api_count: {len(apis)}")
    if missing:
        print(f"missing_expected_apis: {', '.join(missing)}")
    if extra:
        print(f"extra_apis: {', '.join(extra)}")
    if not missing:
        print("status: ok")


if __name__ == "__main__":
    main()
