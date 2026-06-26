"""验证修复模块 — 基于 html_lint 管线生成验证清单

职责边界：
- 从 html_lint 管线收集线上验证标准
- 根据站点配置和报告信息，生成需要验证的 URL 清单
- 为每种 URL 类型提供验证标准（agent 用 web_fetch 执行）
- 提供验证失败的常见原因和修复建议

不做的事：
- 不执行 HTTP 请求（由 agent 通过 web_fetch 工具完成）
- 不自动修复问题（由 agent 根据验证结果决策）
- 不部署到 CF（交给 site 模块）
"""

from lib.config import SITE_URL, REPORT_CF_PROJECT, DIST_DIR, INDEX_FILE
from lib.html_lint import lint_online_checks


# ── 验证清单生成 ──

def get_verify_urls(category=None, filename=None):
    """生成需要验证的 URL 清单。

    合并了 html_lint 管线的线上验证标准。
    """
    if not SITE_URL:
        print("❌ 站点 URL 未配置，无法验证")
        print("   请在 TOOLS.md 中设置 REPORT_CF_PROJECT 或 REPORT_CUSTOM_DOMAIN")
        return []

    urls = []

    # Collect online lint checks
    lint_checks = lint_online_checks()

    # 1. 小站首页
    urls.append({
        "url": SITE_URL,
        "type": "home",
        "label": "小站首页",
        "checks": [
            "HTTP 可达（非 404/5xx）",
            "包含页面容器",
            "引用 /index.json 数据",
            "分类导航可点击",
            "页面卡片正常渲染（有标题、日期、分类）",
        ],
    })

    # 2. 报告页面
    if category and filename:
        report_url = f"{SITE_URL}/{category}/{filename}"
        # Merge lint report checks
        report_lint = [c["check"] for c in lint_checks if c["rule"] == "online_report"]
        report_checks = [
            "HTTP 可达（非 404/5xx）",
        ] + report_lint
        urls.append({
            "url": report_url,
            "type": "report",
            "label": "报告页面",
            "checks": report_checks,
        })

    # 3. 静态资源
    for asset, asset_type in [
        ("/styles/base.css", "css"),
        ("/scripts/main.js", "js"),
        ("/index.json", "json"),
    ]:
        checks = [
            "HTTP 可达（非 404/5xx）",
            "内容非空",
        ]
        if asset_type == "json":
            checks.extend([
                "JSON 可解析且包含 pages 数组",
                "site.name 与配置一致",
                "pages 条目数 ≥ 1",
            ])
        # Merge lint asset checks
        asset_lint = [c["check"] for c in lint_checks if c["rule"] == "online_assets"]
        checks.extend(asset_lint)
        urls.append({
            "url": f"{SITE_URL}{asset}",
            "type": asset_type,
            "label": asset,
            "checks": checks,
        })

    # 4. 图片资源（如有引用图片的报告页面）
    if category and filename:
        # Check if the report references any images
        from pathlib import Path
        report_file = DIST_DIR / category / filename
        if report_file.exists():
            html_content = report_file.read_text("utf-8")
            import re
            imgs = re.findall(r'src="/images/([^"]+)"', html_content)
            if imgs:
                for img_name in imgs[:5]:  # Verify first 5 images
                    img_lint = [c["check"] for c in lint_checks if c["rule"] == "online_images"]
                    urls.append({
                        "url": f"{SITE_URL}/images/{img_name}",
                        "type": "image",
                        "label": f"/images/{img_name}",
                        "checks": img_lint,
                    })

    return urls


def print_verify_plan(category=None, filename=None):
    """打印验证计划，供 agent 逐项执行。

    Agent 应按清单顺序使用 web_fetch 访问每个 URL，
    然后根据 checks 列表判断验证是否通过。
    """
    urls = get_verify_urls(category, filename)
    if not urls:
        return False

    print("🔍 部署验证计划")
    print("=" * 50)
    for i, item in enumerate(urls, 1):
        print(f"\n{i}. [{item['type']}] {item['label']}")
        print(f"   URL: {item['url']}")
        print(f"   验证标准:")
        for j, check in enumerate(item['checks'], 1):
            print(f"     {j}) {check}")
    print("\n" + "=" * 50)
    print("⏳ 请使用 web_fetch 工具逐项验证上述 URL")
    return True


# ── 修复建议 ──

FAILURE_DIAGNOSIS = {
    "404_not_found": {
        "symptom": "URL 返回 404",
        "causes": [
            "Cloudflare Pages 部署未生效（需要等待 1-2 分钟）",
            "文件名或路径拼写错误",
            "dist 目录缺少该文件",
        ],
        "fixes": [
            "等待 30 秒后重新验证（CF 缓存刷新）",
            "检查 dist/ 目录是否包含该文件",
            "重新执行 publish 部署",
        ],
    },
    "empty_content": {
        "symptom": "CSS/JS/JSON 返回空内容",
        "causes": [
            "copy_assets 未正确同步到 dist",
            "源文件（templates/base.css 或 scripts/main.js）缺失",
        ],
        "fixes": [
            "执行 copy_assets() 重新同步",
            "检查 templates/ 和 scripts/ 目录",
            "重新部署",
        ],
    },
    "json_parse_error": {
        "symptom": "index.json 返回内容但 JSON 解析失败",
        "causes": [
            "index.json 写入时中断（部分写入）",
            "index.json 编码异常",
            "原子写入的临时文件未正确替换",
        ],
        "fixes": [
            "重新执行 rebuild_index 重建索引",
            "手动检查 dist/index.json 内容",
            "从备份恢复 index.json",
        ],
    },
    "stale_index": {
        "symptom": "index.json 不包含最新部署的页面",
        "causes": [
            "produce 写入索引后未执行 publish",
            "索引被其他操作覆盖",
            "load_index_safe 从旧备份恢复",
        ],
        "fixes": [
            "执行 rebuild_index 重建索引",
            "检查 index.json 的 pages 数量是否与 dist 文件数一致",
            "重新 produce + publish",
        ],
    },
    "missing_structure": {
        "symptom": "HTML 缺少 report-wrap 或 page-body",
        "causes": [
            "报告 HTML 生成时嵌套清理过度",
            "generate_page_html 输出异常",
            "extract_body 解包逻辑误删 wrapper",
        ],
        "fixes": [
            "检查 produce() 输出的 page_html",
            "检查 extract_body() 是否误删内容",
            "重新 produce + publish",
        ],
    },
    "double_wrapped": {
        "symptom": "HTML 中有多层 report-wrap 或 page-body",
        "causes": [
            "extract_body 未正确解包已有的 report-wrap/page-body",
            "对已部署的页面重复执行 produce",
        ],
        "fixes": [
            "检查 extract_body 解包逻辑是否工作",
            "对已有页面使用 update 而非 produce",
            "删除旧文件后重新 produce",
        ],
    },
    "5xx_server_error": {
        "symptom": "URL 返回 5xx 错误或连接失败",
        "causes": [
            "CF Pages 项目配置问题",
            "部署目录结构异常",
            "网络超时或 DNS 解析失败",
            "SSL 证书问题",
        ],
        "fixes": [
            "检查 CF Pages 项目状态",
            "重新部署（deploy_to_cf）",
            "检查网络连接和 DNS",
            "3次失败后通知用户手动排查",
        ],
    },
    "cors_error": {
        "symptom": "资源加载被 CORS 策略阻止（浏览器 Console 可见）",
        "causes": [
            "CF Pages 自定义域名未配置 CORS 头",
            "跨域子资源（字体/CDN）缺少 Access-Control-Allow-Origin",
            "web_fetch 工具不受 CORS 影响，但浏览器内嵌 iframe 可能受限",
        ],
        "fixes": [
            "CORS 对静态文件站通常不是问题（CF Pages 自动处理）",
            "检查 CF Pages 自定义域名的 DNS 配置",
            "如果是 iframe 内嵌问题，检查 sandbox 属性",
            "3次失败后通知用户手动排查",
        ],
    },
    "redirect_loop": {
        "symptom": "URL 无限重定向（302/301 循环）",
        "causes": [
            "CF Pages 自定义域名与默认域名之间的重定向配置冲突",
            "_redirects 文件配置错误",
            "DNS CNAME 链过长",
        ],
        "fixes": [
            "检查 CF Pages 自定义域名配置",
            "检查 dist/ 中是否有 _redirects 文件",
            "暂时用默认 .pages.dev 域名验证",
        ],
    },
}


def diagnose_failure(url, status, content_snippet=None):
    """根据验证失败的症状给出修复建议。

    Args:
        url: 失败的 URL
        status: 失败类型（404/empty/missing_structure/5xx）
        content_snippet: 返回内容的前200字（可选）

    Returns:
        dict: {diagnosis, causes, fixes}
    """
    key = {
        "404": "404_not_found",
        "empty": "empty_content",
        "json_parse_error": "json_parse_error",
        "stale_index": "stale_index",
        "missing_structure": "missing_structure",
        "double_wrapped": "double_wrapped",
        "5xx": "5xx_server_error",
        "timeout": "5xx_server_error",
        "connection_refused": "5xx_server_error",
        "ssl_error": "5xx_server_error",
        "cors_error": "cors_error",
        "redirect_loop": "redirect_loop",
    }.get(status, "404_not_found")

    diag = FAILURE_DIAGNOSIS.get(key, FAILURE_DIAGNOSIS["404_not_found"])
    print(f"\n🔧 诊断: {url}")
    print(f"   症状: {diag['symptom']}")
    print(f"   可能原因:")
    for c in diag["causes"]:
        print(f"     - {c}")
    print(f"   修复建议:")
    for f in diag["fixes"]:
        print(f"     - {f}")
    return diag


# ── 验证主入口 ──

def verify_deployment(category=None, filename=None):
    """验证部署结果的入口函数。

    打印验证计划，agent 用 web_fetch 执行后根据结果决策。
    验证失败时调用 diagnose_failure 获取修复建议。

    注意：此函数仅输出验证计划，不执行实际 HTTP 验证。
    返回 True 表示计划已输出（不等同于部署成功），
    调用方应自行用 web_fetch 逐项验证后再判断。

    Returns:
        True — 验证计划已输出（实际结果由 agent 判断）
        False — 无法生成验证计划（如 SITE_URL 未配置）
    """
    return print_verify_plan(category, filename)