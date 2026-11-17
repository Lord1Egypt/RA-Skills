import json
import os
from dataclasses import dataclass
from http.client import HTTPSConnection
import argparse
from typing import Optional

HOST = "api.wsa.cloud.tencent.com"

@dataclass
class Doc:
    url : str
    title: str
    snippet: str
    date: str
    site: str
    score: float
    pics: list[str]

    def __post_init__(self):
        if self.pics is None:
            self.pics = []

@dataclass
class Option:
    query: str
    site: str = ""
    mode: Optional[int] = None
    cnt: int = 10
    industry: str = ""
    freshness: str = ""



def generate_header_and_payload(params: Option, secret_key: str):
    # ************* 构造header *************
    headers = {
        "Authorization": "Bearer " + secret_key,
        "Content-Type": "application/json; charset=utf-8",
        "Host": HOST
    }

    # ************* 构造payload *************
    body = {"Query": params.query}
    if len(params.site) > 0:
        body["Site"] = params.site
    if params.mode is not None:
        body["Mode"] = params.mode
    if params.cnt is not None:
        body["Cnt"] = params.cnt  # pyright: ignore[reportArgumentType]
    if len(params.industry) > 0:
        body["Industry"] = params.industry
    if len(params.freshness) > 0:
        body["Freshness"] = params.freshness
    payload = json.dumps(body)

    return headers, payload


# api-key可前往官网控制台 https://console.cloud.tencent.com/wsapi/index 进行获取

def search(params: Option, secret_key: str):
    headers, payload = generate_header_and_payload(params, secret_key=secret_key)
    query = params.query
    try:
        req = HTTPSConnection(HOST)
        req.request("POST", "/SearchPro", headers=headers, body=payload.encode("utf-8"))
        resp = req.getresponse()
        rsp = resp.read()
        ret = json.loads(rsp)
        docs, error_msg = parse(ret)
        if error_msg:
            print(f"## 搜索失败\n原因：{error_msg}")
            return
        print(f"## 查询词:{query}, 搜索结果:{len(docs)}条")
        for idx, doc in enumerate(docs):
            line = (
                f"{idx + 1}. [{doc.title}]({doc.url})\n"
                f"    - 摘要: {doc.snippet}\n"
                f"    - 内容发布时间: {doc.date}\n"
                f"    - 网站: {doc.site}"
            )
            if doc.score:
                line += f"\n    - 相关性得分: {doc.score}"
            if doc.pics and len(doc.pics) > 0:
                pics_info = "\t".join([f"[{p.get('caption', '图片')}]({p.get('origin_url', '')})" for p in doc.pics])
                line += f"\n    - 相关图片: {pics_info}"
            print(line)
    except Exception as err:
        print(f"request error: {err}")


def parse(rsp: dict):
    error_msg = ""
    res = rsp.get("Response")
    if res is None or not isinstance(res, dict):
        print("response is null")
        return [], error_msg

    error = res.get("Error")
    if error is not None:
        error_msg = error.get("Message", "")
        return [], error_msg

    pages = res.get("Pages")
    if pages is None:
        return [], error_msg

    docs = []
    for page in pages:
        json_page = json.loads(page)
        is_vr = json_page.get("vr", False)
        if is_vr:
            display = json_page.pop("display", None)
            url = json_page.get("url")
            title = json_page.get("title")
            date = json_page.get("date")
            site = json_page.get("site", "")
            score = json_page.get("score", 0.0)
            pics = json_page.get("pics", [])
            if display is None:
                # 垂直信源（天气/金价/股价等）可能只有 content/passage，没有 display 结构
                content = json_page.get("content") or json_page.get("passage") or ""
                if not content:
                    continue
                docs.append(Doc(url=url, title=title, site=site, date=date, snippet=content, score=score, pics=pics))
                continue
            url = display.get("url") or url
            title = display.get("title") or title
            date = display.get("date") or date
            content = page
            docs.append(Doc(url=url, title=title, site=site, date=date, snippet=content, score=score, pics=pics))
        else:
            passage = json_page.get("passage")
            url = json_page.get("url")
            title = json_page.get("title")
            site = json_page.get("site")
            date = json_page.get("date")
            score = json_page.get("score", 0.0)
            pics = json_page.get("pics", [])
            if len(title) == 0 or len(passage) == 0:
                continue
            docs.append(Doc(url=url, title=title, site=site, date=date, snippet=passage, score=score, pics=pics))
    return docs, error_msg


if __name__ == "__main__":
    api_key = os.getenv("TENCENTCLOUD_WSA_APIKEY")

    if api_key is None:
        print("api-key are not set, 前往 https://console.cloud.tencent.com/wsapi/index 进行获取")
        exit(1)

    parser = argparse.ArgumentParser(description="websearch command arguments")
    parser.add_argument("--query", type=str, help="search query", required=True)
    parser.add_argument("--site", type=str, help="指定站点搜索", default="")
    parser.add_argument("--mode", type=int, choices=[0, 1, 2], default=None,
                        help="返回结果类型，不传默认为0。取值：0，公开网页信源结果；1，优质权威垂直信源结果；2，混合结果")
    parser.add_argument("--cnt", type=int, choices=[10, 20, 30, 40, 50],
                        help="返回结果条数，取值 10/20/30/40/50", default=None)
    parser.add_argument("--industry", type=str, choices=["gov", "news", "acad", "finance"],
                        help="垂直领域搜索: gov/新闻/acad/金融", default="")
    parser.add_argument("--freshness", type=str,
                        help="搜索时效范围: d[N]天(1-30) / m[N]月(1-12) / y[N]年(1-5)", default="")

    args = parser.parse_args()
    if len(args.query) == 0:
        print("invalid input arguments, query is empty")
        exit(1)

    reqOptions = Option(
        query=args.query,
        site=args.site,
        mode=args.mode,
        cnt=args.cnt,
        industry=args.industry,
        freshness=args.freshness,
    )

    search(reqOptions, api_key)

