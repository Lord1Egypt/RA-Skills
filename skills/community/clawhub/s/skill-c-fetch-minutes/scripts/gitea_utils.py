"""
Gitea API 工具函数（与 Skill-A/B/H 保持一致）
"""

import base64
import requests


def gitea_request(method, path, token, base_url, raise_on_error=True, **kwargs):
    url = f"{base_url.rstrip('/')}/api/v1{path}"
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json",
    }
    resp = requests.request(method, url, headers=headers, timeout=15, **kwargs)
    if raise_on_error:
        resp.raise_for_status()
    return resp


def get_user_email(username, token, base_url):
    try:
        resp = gitea_request("GET", f"/users/{username}", token, base_url)
        return resp.json().get("email", "")
    except Exception:
        return ""


def get_repo_member_usernames(owner, repo, token, base_url):
    users = []
    seen = set()
    if owner and owner not in seen:
        users.append(owner)
        seen.add(owner)
    try:
        resp = gitea_request("GET", f"/repos/{owner}/{repo}/collaborators", token, base_url)
        for u in resp.json():
            login = u.get("login", "")
            if login and login not in seen:
                users.append(login)
                seen.add(login)
    except Exception:
        pass
    return users


def get_file_from_repo(owner, repo, filepath, token, base_url, branch="main"):
    try:
        resp = gitea_request(
            "GET",
            f"/repos/{owner}/{repo}/contents/{filepath}",
            token, base_url,
            params={"ref": branch},
        )
        data = resp.json()
        content = base64.b64decode(data["content"]).decode("utf-8")
        return content, data["sha"]
    except Exception:
        return None, None


def create_file_in_repo(owner, repo, filepath, content, message, token, base_url, branch="main"):
    encoded = base64.b64encode(content.encode("utf-8")).decode()
    resp = gitea_request(
        "POST",
        f"/repos/{owner}/{repo}/contents/{filepath}",
        token, base_url,
        json={"message": message, "content": encoded, "branch": branch},
    )
    return resp.json()


def upsert_file_in_repo(owner, repo, filepath, content, message, token, base_url, branch="main"):
    """
    创建或更新文件（自动判断是否已存在）。
    commit-content 使用此函数避免重复提交时的 409 冲突。
    """
    encoded = base64.b64encode(content.encode("utf-8")).decode()
    # 先尝试获取 sha
    existing_content, sha = get_file_from_repo(owner, repo, filepath, token, base_url, branch)
    if sha:
        # 文件已存在：PUT 更新
        resp = gitea_request(
            "PUT",
            f"/repos/{owner}/{repo}/contents/{filepath}",
            token, base_url,
            json={"message": message, "content": encoded, "sha": sha, "branch": branch},
        )
    else:
        # 文件不存在：POST 创建
        resp = gitea_request(
            "POST",
            f"/repos/{owner}/{repo}/contents/{filepath}",
            token, base_url,
            json={"message": message, "content": encoded, "branch": branch},
        )
    return resp.json()


def update_file_in_repo(owner, repo, filepath, new_content, message, sha, token, base_url, branch="main"):
    encoded = base64.b64encode(new_content.encode("utf-8")).decode()
    resp = gitea_request(
        "PUT",
        f"/repos/{owner}/{repo}/contents/{filepath}",
        token, base_url,
        json={"message": message, "content": encoded, "sha": sha, "branch": branch},
    )
    return resp.json()


def list_meetings_in_repo(owner, repo, token, base_url, branch="main"):
    try:
        resp = gitea_request(
            "GET",
            f"/repos/{owner}/{repo}/contents/meetings",
            token, base_url,
            params={"ref": branch},
        )
        items = resp.json()
        return [
            item["name"]
            for item in items
            if item["type"] == "dir" and item["name"] != "archive"
        ]
    except Exception:
        return []


def file_exists_in_repo(owner, repo, filepath, token, base_url, branch="main"):
    """检查文件是否存在于仓库，返回 bool。"""
    try:
        resp = gitea_request(
            "GET",
            f"/repos/{owner}/{repo}/contents/{filepath}",
            token, base_url,
            params={"ref": branch},
            raise_on_error=False,
        )
        return resp.status_code == 200
    except Exception:
        return False


def get_managed_repos(token, base_url):
    repos = []
    page = 1
    while True:
        try:
            resp = gitea_request(
                "GET", "/repos/search", token, base_url,
                params={"limit": 50, "page": page},
            )
            data = resp.json().get("data", [])
        except Exception:
            break
        if not data:
            break
        for repo_info in data:
            owner_name = repo_info["owner"]["login"]
            repo_name  = repo_info["name"]
            check = gitea_request(
                "GET",
                f"/repos/{owner_name}/{repo_name}/contents/meetings",
                token, base_url,
                raise_on_error=False,
            )
            if check.status_code == 200:
                repos.append(repo_info["full_name"])
        page += 1
    return repos
