"""sources/learn.py — learn.tsinghua.edu.cn 网络学堂搜索

复用 base-cas 登录的 learn session，搜索课件文件名/公告标题。
基于 learn_api 的 get_files/get_announcements 做关键词过滤。
"""
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "learn", "scripts"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "shared", "scripts"))
import common
import learn_api

SOURCE_NAME = "learn"


def _ensure_api():
    """获取 learn API（复用 base-cas session），失败返回 None。"""
    api = learn_api.LearnAPI()
    if api.reload_session():
        return api
    return None


def search(query, limit=5):
    """learn 搜索：课件名 + 公告标题 含关键词。"""
    common.log(f"[learn] 搜索: {query}")
    api = _ensure_api()
    if api is None:
        common.log("[learn] session 无效，跳过")
        return []

    results = []
    try:
        courses = api.get_courses()
        for c in courses:
            wlkcid, kcm = c.get("wlkcid"), c.get("kcm", "")
            # 课件
            for f in api.get_files(wlkcid):
                name = str(f.get("bt", ""))
                if query in name:
                    results.append({
                        "source": SOURCE_NAME,
                        "title": f"[课件]{kcm}: {name}",
                        "url": f"https://learn.tsinghua.edu.cn/f/wlxt/index/course/student/#{wlkcid}",
                        "snippet": f"课件: {name}",
                    })
            # 公告
            for a in api.get_announcements(wlkcid):
                title = str(a.get("bt", ""))
                if query in title:
                    results.append({
                        "source": SOURCE_NAME,
                        "title": f"[公告]{kcm}: {title}",
                        "url": f"https://learn.tsinghua.edu.cn/f/wlxt/index/course/student/#{wlkcid}",
                        "snippet": f"公告: {a.get('fbsjStr', '')}",
                    })
            if len(results) >= limit:
                break
    except Exception as e:
        common.log(f"[learn] 搜索异常: {e}")

    common.log(f"[learn] 结果 {len(results)} 条")
    return results[:limit]


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "课件"
    common.output_json(search(q))
