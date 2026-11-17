#!/usr/bin/env python3
"""
飞书推送脚本
- 接收 daily_recommend.py 生成的推荐 JSON
- 创建飞书云文档
- 发送飞书卡片消息
"""
import json
import os
import argparse
import sys
import requests
from pathlib import Path


class FeishuAPI:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self._token = None

    def get_token(self):
        if self._token:
            return self._token
        resp = requests.post(
            "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            json={"app_id": self.app_id, "app_secret": self.app_secret},
            timeout=15
        )
        data = resp.json()
        if data.get('code') != 0:
            raise Exception(f"获取 token 失败: {data}")
        self._token = data['tenant_access_token']
        return self._token

    def create_document(self, title):
        """创建飞书云文档"""
        token = self.get_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        resp = requests.post(
            "https://open.feishu.cn/open-apis/docx/v1/documents",
            headers=headers,
            json={"title": title},
            timeout=20
        )
        data = resp.json()
        if data.get('code') != 0:
            raise Exception(f"创建文档失败: {data}")
        return data['data']['document']['document_id']

    def insert_blocks(self, doc_id, blocks, batch_size=45):
        """分批插入 blocks"""
        token = self.get_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children"
        total = len(blocks)
        print(f"  [Feishu] 开始插入 {total} 个 blocks（每批 {batch_size}）")
        for i in range(0, total, batch_size):
            batch = blocks[i:i+batch_size]
            resp = requests.post(url, headers=headers, json={"children": batch}, timeout=30)
            data = resp.json()
            if data.get('code') != 0:
                print(f"  [Feishu] 批次 {i//batch_size+1} 失败: {data}")
                return False
            print(f"  [Feishu] 批次 {i//batch_size+1}: {len(batch)} blocks ✅")
        return True

    def send_card_message(self, user_open_id, title, content, doc_url=None):
        """发送飞书卡片消息"""
        token = self.get_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        elements = [
            {"tag": "div", "text": {"tag": "lark_md", "content": content}}
        ]
        if doc_url:
            elements.append({"tag": "hr"})
            elements.append({
                "tag": "action",
                "actions": [{
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": "📄 查看完整简报"},
                    "type": "primary",
                    "url": doc_url
                }]
            })
        elements.append({
            "tag": "note",
            "elements": [{"tag": "plain_text", "content": "📅 ClawHub 每日洞察 | 4 维度轮换 | 10 天去重"}]
        })

        card = {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": title},
                "template": "blue"
            },
            "elements": elements
        }

        msg = {
            "receive_id": user_open_id,
            "msg_type": "interactive",
            "content": json.dumps(card)
        }
        resp = requests.post(
            "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
            headers=headers, json=msg, timeout=20
        )
        data = resp.json()
        if data.get('code') != 0:
            raise Exception(f"发送消息失败: {data}")
        return data


def load_config(config_path):
    """从 config.json 加载飞书凭证（用户自填）"""
    path = Path(config_path)
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"  [Warn] 读取 config 失败: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="推送推荐到飞书")
    parser.add_argument("--recommendation", required=True, help="daily_recommend.py 生成的 JSON")
    parser.add_argument("--config", default="references/config.json", help="凭证配置文件路径")
    parser.add_argument("--app-id", default=None, help="飞书 app_id（也可放 config.json）")
    parser.add_argument("--app-secret", default=None, help="飞书 app_secret（也可放 config.json）")
    parser.add_argument("--user-open-id", default=None, help="用户 open_id（也可放 config.json）")
    parser.add_argument("--skip-doc", action="store_true", help="跳过创建文档")
    parser.add_argument("--skip-msg", action="store_true", help="跳过发送消息")
    args = parser.parse_args()

    # 凭证优先级：CLI 参数 > 环境变量 > config.json
    config = load_config(args.config) or {}
    app_id = args.app_id or os.environ.get("FEISHU_APP_ID") or config.get("feishu_app_id")
    app_secret = args.app_secret or os.environ.get("FEISHU_APP_SECRET") or config.get("feishu_app_secret")
    user_open_id = args.user_open_id or os.environ.get("FEISHU_USER_OPEN_ID") or config.get("feishu_user_open_id")

    if not app_id or not app_secret:
        print("[Error] 缺少飞书凭证。请通过以下任一方式提供：")
        print("  1. --app-id <your_app_id> --app-secret <your_app_secret>")
        print("  2. 环境变量 FEISHU_APP_ID / FEISHU_APP_SECRET")
        print("  3. 在 references/config.json 中配置 feishu_app_id / feishu_app_secret")
        return 1
    if not user_open_id:
        print("[Error] 缺少 user_open_id。请通过以下任一方式提供：")
        print("  1. --user-open-id <your_open_id>")
        print("  2. 环境变量 FEISHU_USER_OPEN_ID")
        print("  3. 在 references/config.json 中配置 feishu_user_open_id")
        return 1

    rec_path = Path(args.recommendation)
    if not rec_path.exists():
        print(f"[Error] 推荐文件不存在: {rec_path}")
        return 1

    with open(rec_path, "r", encoding="utf-8") as f:
        rec = json.load(f)

    date = rec['date']
    dimension = rec['dimension']
    recs = rec['recommendations']
    blocks = rec.get('feishu_blocks', [])
    total_scanned = rec.get('total_scanned', 0)
    deduplicated = rec.get('deduplicated', 0)

    print(f"[Feishu] 推送 {date} ({dimension}) - {len(recs)} 个推荐")

    # 准备
    feishu = FeishuAPI(app_id, app_secret)
    dim_stats = rec.get('dim_stats', {})
    if dimension == "all":
        title = f"🦞 ClawHub 每日洞察 | {date}"
    else:
        dim_name = dim_stats.get(dimension, {}).get('name', dimension) if dim_stats else dimension
        title = f"🦞 ClawHub 每日洞察 | {date}（{dim_name}维度）"
    doc_url = None

    # 1. 创建文档
    if not args.skip_doc and blocks:
        try:
            doc_id = feishu.create_document(title)
            print(f"  [Feishu] 文档已创建: {doc_id}")
            ok = feishu.insert_blocks(doc_id, blocks)
            if ok:
                doc_url = f"https://feishu.cn/docx/{doc_id}"
                print(f"  [Feishu] 文档 URL: {doc_url}")
        except Exception as e:
            print(f"  [Feishu] 创建文档失败: {e}")

    # 2. 发送卡片消息
    if not args.skip_msg and recs:
        try:
            # 按维度分组展示
            by_dim = {}
            for r in recs:
                dim_key = r.get('dimension', 'trending')
                by_dim.setdefault(dim_key, []).append(r)

            highlights_lines = []
            for dim_key in ["trending", "quality", "newcomers", "panorama", "actively_maintained", "verified"]:
                if dim_key not in by_dim:
                    continue
                dim_recs = by_dim[dim_key]
                dim_config = {
                    "trending": ("🔥 趋势", "热装"),
                    "quality": ("⭐ 质量", "口碑"),
                    "newcomers": ("🚀 新星", "崛起"),
                    "panorama": ("🏆 全景", "热议"),
                    "actively_maintained": ("🔧 活跃", "维护"),
                    "verified": ("🛡️ 可信", "推荐"),
                }.get(dim_key, (dim_key, ""))
                for r in dim_recs:
                    highlights_lines.append(
                        f"**{r['display_name']}** ({dim_config[0]}) ⭐{r['stars']} 📥{r['downloads']}\n"
                        f"  💡 {r['recommend_reason']}\n"
                        f"  🏷️ {', '.join(r.get('pain_points_matched', [])) or '通用工具'}"
                    )
            highlights = "\n\n".join(highlights_lines)

            # 统计摘要
            pain_scenes = set()
            for r in recs:
                pain_scenes.update(r.get('pain_points_matched', []))
            scene_text = "、".join(sorted(pain_scenes)[:3]) if pain_scenes else "通用推荐"

            # 维度概况
            dim_summary_parts = []
            for dim_key, stats in dim_stats.items():
                dim_summary_parts.append(f"{stats['module']} {stats['recommended']}/{stats['limit']}")

            # 云文档直达链接（放在卡片底部）
            doc_link_section = ""
            if doc_url:
                doc_link_section = f"\n\n📄 **完整简报**: [点击查看云文档]({doc_url})"

            # 总字数控制在 400-600
            dim_text = " | ".join(dim_summary_parts) if dim_summary_parts else f"{dimension}维度"
            content = (
                f"**🦞 {date} | 全维度**\n\n"
                f"扫描 {total_scanned} 个 Skill → 推荐 {len(recs)} 个新发现，去重 {deduplicated} 个\n"
                f"维度：{dim_text}\n"
                f"匹配场景：{scene_text}\n\n"
                f"━━━━━━━━━━━━━━━\n"
                f"**🌟 今日推荐**\n\n"
                f"{highlights}\n\n"
                f"━━━━━━━━━━━━━━━\n"
                f"📚 完整简报包含所有推荐详情：作者、数据、指标、匹配场景、推荐理由、下一步行动"
                f"{doc_link_section}"
            )
            result = feishu.send_card_message(user_open_id, title, content, doc_url)
            print(f"  [Feishu] 消息已发送 ✅")
        except Exception as e:
            print(f"  [Feishu] 发送消息失败: {e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
