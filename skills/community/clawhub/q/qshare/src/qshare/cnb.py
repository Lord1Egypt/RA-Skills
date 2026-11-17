"""Upload a file as an asset in the configured CNB release repository."""

import datetime
import http.client
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

TOKEN = "67emzlY14b8RDEHMJmuevI6GuON"
REPO = "steinveni/qshare"
API = "https://api.cnb.cool/{}".format(REPO)
ACCEPT = "application/vnd.cnb.api+json"
CHUNK_SIZE = 1024 * 1024


def request_json(url, method="GET", payload=None):
    headers = {"Accept": ACCEPT, "Authorization": "Bearer " + TOKEN}
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode("utf-8")
    request = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(request, timeout=120) as response:
            body = response.read()
        return json.loads(body.decode("utf-8")) if body else {}
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise RuntimeError("CNB API HTTP {}: {}".format(exc.code, detail)) from exc
    except URLError as exc:
        raise RuntimeError("CNB network error: {}".format(exc.reason)) from exc


def get_or_create_release(tag):
    releases = request_json(API + "/-/releases")
    for release in releases:
        if release.get("tag_name") == tag:
            return str(release["id"])
    release = request_json(
        API + "/-/releases",
        method="POST",
        payload={
            "tag_name": tag,
            "name": tag,
            "body": "Release " + tag,
            "target_commitish": "main",
        },
    )
    return str(release["id"])


def upload_file(path, release_id):
    name = os.path.basename(path)
    size = os.path.getsize(path)
    info = request_json(
        API + "/-/releases/{}/asset-upload-url".format(release_id),
        method="POST",
        payload={"asset_name": name, "size": size, "overwrite": False, "ttl": 0},
    )
    parts = urlsplit(info["upload_url"])
    if parts.scheme != "https" or not parts.hostname:
        raise RuntimeError("CNB returned an invalid upload URL")
    connection = http.client.HTTPSConnection(parts.hostname, parts.port, timeout=600)
    target = parts.path + ("?" + parts.query if parts.query else "")
    connection.putrequest("PUT", target)
    connection.putheader("Content-Length", str(size))
    connection.endheaders()
    sent = 0
    last_percent = -1
    try:
        with open(path, "rb") as source:
            while True:
                chunk = source.read(CHUNK_SIZE)
                if not chunk:
                    break
                connection.send(chunk)
                sent += len(chunk)
                percent = 100 if size == 0 else sent * 100 // size
                if percent != last_percent:
                    print("\rUploading to CNB... {}%".format(percent), end="", flush=True)
                    last_percent = percent
        response = connection.getresponse()
        body = response.read()
        if response.status < 200 or response.status >= 300:
            raise RuntimeError(
                "CNB upload HTTP {}: {}".format(response.status, body.decode("utf-8", "replace"))
            )
    except OSError as exc:
        raise RuntimeError("CNB upload network error: {}".format(exc)) from exc
    finally:
        connection.close()
    print("\rUploading to CNB... 100%".ljust(32), flush=True)

    verify_url = info["verify_url"]
    if verify_url.startswith("/"):
        verify_url = urljoin("https://api.cnb.cool", verify_url)
    if not verify_url.startswith("https://api.cnb.cool/"):
        raise RuntimeError("unexpected CNB confirmation URL")
    request_json(verify_url, method="POST")


def get_download_url(tag, name):
    for release in request_json(API + "/-/releases"):
        if release.get("tag_name") == tag:
            for asset in release.get("assets", []):
                if asset.get("name") == name:
                    return asset["browser_download_url"]
    raise RuntimeError("uploaded asset was not found in CNB release")


def delete_cnb_assets(tag, name):
    """Delete every server-side copy of an asset from its release."""
    deleted = 0
    for release in request_json(API + "/-/releases"):
        if release.get("tag_name") != tag:
            continue
        release_id = release.get("id")
        if release_id is None:
            continue
        for asset in release.get("assets", []):
            if asset.get("name") != name:
                continue
            request_json(
                "{}/-/releases/{}/assets/{}".format(API, release_id, asset["id"]),
                method="DELETE",
            )
            deleted += 1
    return deleted


def upload_to_cnb(path):
    tag = datetime.date.today().isoformat()
    release_id = get_or_create_release(tag)
    upload_file(path, release_id)
    return get_download_url(tag, os.path.basename(path)), tag
