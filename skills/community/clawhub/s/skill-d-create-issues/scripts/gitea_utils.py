"""
Gitea API 工具函数（与其他 Skill 保持一致，新增 issue 相关操作）
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


def update_file_in_repo(owner, repo, filepath, new_content, message, sha,
                         token, base_url, branch="main"):
    encoded = base64.b64encode(new_content.encode("utf-8")).decode()
    resp = gitea_request(
        "PUT",
        f"/repos/{owner}/{repo}/contents/{filepath}",
        token, base_url,
        json={"message": message, "content": encoded, "sha": sha, "branch": branch},
    )
    return resp.json()


def file_exists_in_repo(owner, repo, filepath, token, base_url, branch="main"):
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


# ── Gitea Issue API ────────────────────────────────────────────────────────────

def ensure_label(owner, repo, label_name, token, base_url, color="#0075ca"):
    """
    确保仓库中存在指定 label，不存在则创建。
    返回 label id。
    """
    try:
        resp = gitea_request("GET", f"/repos/{owner}/{repo}/labels", token, base_url)
        for lbl in resp.json():
            if lbl["name"] == label_name:
                return lbl["id"]
    except Exception:
        pass

    try:
        resp = gitea_request(
            "POST",
            f"/repos/{owner}/{repo}/labels",
            token, base_url,
            json={"name": label_name, "color": color},
        )
        return resp.json().get("id")
    except Exception:
        return None


def get_user_id(username, token, base_url):
    """获取 Gitea 用户 ID（建 issue 时 assignees 字段用 ID）。"""
    try:
        resp = gitea_request("GET", f"/users/{username}", token, base_url)
        return resp.json().get("id")
    except Exception:
        return None


def create_issue(owner, repo, title, body, assignees, label_ids, token, base_url):
    """
    在仓库创建 issue。
    assignees：Gitea 用户名列表。
    label_ids：label id 列表。
    返回 (issue_number, issue_url)，失败抛异常。
    """
    payload = {
        "title": title,
        "body":  body,
    }
    if assignees:
        payload["assignees"] = assignees
    if label_ids:
        payload["labels"] = [lid for lid in label_ids if lid is not None]

    resp = gitea_request(
        "POST",
        f"/repos/{owner}/{repo}/issues",
        token, base_url,
        json=payload,
    )
    data = resp.json()
    return data["number"], data["html_url"]


def update_issue_body(owner, repo, issue_number, new_body, token, base_url):
    """更新 issue 正文（用于依赖回填）。"""
    gitea_request(
        "PATCH",
        f"/repos/{owner}/{repo}/issues/{issue_number}",
        token, base_url,
        json={"body": new_body},
    )
