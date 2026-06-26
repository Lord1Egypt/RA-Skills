#!/usr/bin/env python3
"""
Siyuan Wiki 对话归档助手

功能：在对话结束后，自动判断对话内容是否值得保存到 wiki，
      如果值得，自动创建 Synthesis 页并更新索引。

使用方法:
    # 方式1: 直接传入参数
    python3 siyuan_wiki_archiver.py \
        --topic "链接语法问题分析" \
        --question "为什么写入的链接无法正常索引？" \
        --answer "测试发现 [[文档名]] 不建立引用，((块ID)) 才可以..." \
        --sources "siyuan-api-test" \
        --auto

    # 方式2: 交互式（会提示确认）
    python3 siyuan_wiki_archiver.py \
        --topic "链接语法问题分析" \
        --question "为什么写入的链接无法正常索引？" \
        --answer "测试发现..."

环境变量:
    SIYUAN_API      - API地址，默认 http://127.0.0.1:6806
    SIYUAN_TOKEN    - API Token
    SIYUAN_NOTEBOOK - 笔记本ID
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from typing import List, Optional, Tuple

import requests


class SiyuanWikiArchiver:
    """思源 Wiki 归档助手"""

    # 保存条件关键词（用于自动判断）
    SAVE_INDICATORS = [
        "对比", "分析", "总结", "结论", "判断", "决策",
        "方案", "评估", "发现", "矛盾", "关联", "连接",
        "综合", "整合", "推理", "推断", "论证",
    ]

    # 不保存的条件（简单查询）
    SKIP_INDICATORS = [
        "今天星期几", "现在几点", "翻译一下", "简单解释",
        "临时", "试一下", "测试",
    ]

    def __init__(self, base_url: str = None, token: str = None, notebook_id: str = None):
        self.base_url = (base_url or os.environ.get("SIYUAN_API", "http://127.0.0.1:6806")).rstrip("/")
        self.token = token or os.environ.get("SIYUAN_TOKEN", "")
        self.notebook_id = notebook_id or os.environ.get("SIYUAN_NOTEBOOK", "")
        self.headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json"
        }

    def _api(self, endpoint: str, data: dict) -> dict:
        """调用思源 API"""
        url = f"{self.base_url}{endpoint}"
        resp = requests.post(url, headers=self.headers, json=data, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        if result.get("code") != 0:
            raise RuntimeError(f"API Error: {result.get('msg')}")
        return result.get("data", [])

    def should_save(
        self,
        question: str,
        answer: str,
        source_count: int = 0,
        user_explicit: bool = False
    ) -> Tuple[bool, str]:
        """
        判断对话是否值得保存

        返回: (是否保存, 原因)
        """
        full_text = f"{question} {answer}"

        # 1. 用户明确指示
        if user_explicit:
            return True, "用户明确指示保存"

        # 2. 涉及多个来源
        if source_count >= 2:
            return True, f"涉及 {source_count} 个来源的综合分析"

        # 3. 检查保存指标
        for indicator in self.SAVE_INDICATORS:
            if indicator in full_text:
                return True, f"包含综合分析关键词: '{indicator}'"

        # 4. 检查跳过指标
        for indicator in self.SKIP_INDICATORS:
            if indicator in question:
                return False, f"简单查询，关键词: '{indicator}'"

        # 5. 长度判断（较长的回答通常更有价值）
        if len(answer) > 500:
            return True, "回答内容较长，可能包含有价值的分析"

        # 6. 默认不保存
        return False, "不满足保存条件（简单查询/非分析性回答）"

    def get_doc_id_by_title(self, title: str) -> Optional[str]:
        """根据标题查找文档ID"""
        result = self._api("/api/query/sql", {
            "stmt": f"SELECT id FROM blocks WHERE type='d' AND content = '{title}' LIMIT 1"
        })
        if result:
            return result[0]["id"]
        return None

    def get_doc_id_by_path(self, path_keyword: str) -> Optional[str]:
        """根据路径关键词查找文档ID"""
        result = self._api("/api/query/sql", {
            "stmt": f"SELECT id, content, path FROM blocks WHERE type='d' AND path LIKE '%{path_keyword}%' LIMIT 3"
        })
        if result:
            for r in result:
                print(f"    匹配: {r['content']} ({r['id'][:12]}...)")
            return result[0]["id"]
        return None

    def create_synthesis(
        self,
        topic: str,
        question: str,
        answer: str,
        sources: List[str] = None,
        confidence: str = "medium",
        follow_up: List[str] = None
    ) -> str:
        """
        创建 Synthesis 页

        返回: 新文档ID
        """
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")

        # 生成 slug
        slug = re.sub(r'[^\w\u4e00-\u9fff]+', '-', topic).strip('-').lower()
        if len(slug) > 50:
            slug = slug[:50]

        # 构建来源链接
        source_links = ""
        if sources:
            for src in sources:
                # 尝试查找来源文档的ID
                src_id = self.get_doc_id_by_title(src)
                if src_id:
                    source_links += f"- (({src_id} \"{src}\"))\n"
                else:
                    source_links += f"- {src}\n"
        else:
            source_links = "- （本次分析基于对话上下文）\n"

        # 后续问题
        follow_up_section = ""
        if follow_up:
            follow_up_section = "\n## 后续问题\n" + "\n".join(f"- {q}" for q in follow_up) + "\n"

        content = f"""# {topic}

## 元信息
- **类型**: synthesis
- **来源查询**: {question}
- **创建日期**: {date_str}
- **置信度**: {confidence}
- **标签**: #synthesis

## 问题
{question}

## 分析过程
{answer}

## 来源依据
{source_links}

## 结论
<简要总结>

## 后续行动
- [ ] <基于这个结论，应该做什么？>
{follow_up_section}
"""

        doc_id = self._api("/api/filetree/createDocWithMd", {
            "notebook": self.notebook_id,
            "path": f"/syntheses/{slug}",
            "markdown": content
        })
        return doc_id

    def update_index(self, synthesis_id: str, topic: str, date_str: str):
        """更新 index.md"""
        # 查找 index.md
        index_result = self._api("/api/query/sql", {
            "stmt": "SELECT id FROM blocks WHERE type='d' AND content = 'index' LIMIT 1"
        })
        if not index_result:
            print("  ⚠️ index.md 未找到")
            return

        index_id = index_result[0]["id"]

        # 追加到"最新综合研究"
        self._api("/api/block/appendBlock", {
            "parentID": index_id,
            "dataType": "markdown",
            "data": f"\n| (({synthesis_id} \"{topic}\")) | {date_str} | 完成 |"
        })
        print("  ✅ index.md 已更新")

    def update_log(self, topic: str, date_str: str, time_str: str):
        """更新 log.md"""
        log_result = self._api("/api/query/sql", {
            "stmt": "SELECT id FROM blocks WHERE type='d' AND content = 'log' LIMIT 1"
        })
        if not log_result:
            print("  ⚠️ log.md 未找到")
            return

        log_id = log_result[0]["id"]

        # 检查是否已有今天的日期标题
        today_blocks = self._api("/api/query/sql", {
            "stmt": f"SELECT id FROM blocks WHERE root_id = '{log_id}' AND content = '{date_str}' LIMIT 1"
        })

        if today_blocks:
            # 已有今天的日期，直接追加条目
            self._api("/api/block/appendBlock", {
                "parentID": today_blocks[0]["id"],
                "dataType": "markdown",
                "data": f"\n- [{time_str}] [query→synthesis] 归档: {topic}"
            })
        else:
            # 新建今天的日期
            self._api("/api/block/appendBlock", {
                "parentID": log_id,
                "dataType": "markdown",
                "data": f"\n\n## {date_str}\n- [{time_str}] [query→synthesis] 归档: {topic}"
            })
        print("  ✅ log.md 已更新")

    def archive(
        self,
        topic: str,
        question: str,
        answer: str,
        sources: List[str] = None,
        confidence: str = "medium",
        follow_up: List[str] = None,
        auto: bool = False,
        force: bool = False
    ) -> bool:
        """
        归档对话到 wiki

        返回: 是否成功归档
        """
        print(f"\n{'='*60}")
        print("🧠 Siyuan Wiki 归档助手")
        print("="*60)

        # 1. 判断是否保存
        if force:
            should_save = True
            reason = "强制保存"
        else:
            should_save, reason = self.should_save(question, answer, len(sources or []))

        print(f"\n📊 保存判断: {'✅ 保存' if should_save else '❌ 跳过'}")
        print(f"   原因: {reason}")

        if not should_save:
            if auto:
                print("   （自动模式，已跳过）")
                return False
            # 交互式确认
            confirm = input("\n是否仍要保存? [y/N]: ").strip().lower()
            if confirm not in ('y', 'yes'):
                print("已取消")
                return False

        # 2. 创建 Synthesis
        print(f"\n✏️  创建 Synthesis 页...")
        try:
            doc_id = self.create_synthesis(topic, question, answer, sources, confidence, follow_up)
            print(f"   ✅ 创建成功: {doc_id}")
        except Exception as e:
            print(f"   ❌ 创建失败: {e}")
            return False

        # 3. 更新索引和日志
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M")

        print(f"\n📝 更新索引和日志...")
        try:
            self.update_index(doc_id, topic, date_str)
            self.update_log(topic, date_str, time_str)
        except Exception as e:
            print(f"   ⚠️ 更新失败: {e}")

        print(f"\n{'='*60}")
        print("✅ 归档完成！")
        print("="*60)
        return True


def main():
    parser = argparse.ArgumentParser(description="Siyuan Wiki 对话归档助手")
    parser.add_argument("--topic", required=True, help="对话主题（用于生成标题和slug）")
    parser.add_argument("--question", required=True, help="用户的原始问题")
    parser.add_argument("--answer", required=True, help="AI 的回答内容")
    parser.add_argument("--sources", nargs="*", help="涉及的来源文档标题列表")
    parser.add_argument("--confidence", default="medium", choices=["high", "medium", "low"],
                        help="置信度")
    parser.add_argument("--follow-up", nargs="*", help="后续问题列表")
    parser.add_argument("--auto", action="store_true", help="自动模式（不提示，按规则判断）")
    parser.add_argument("--force", action="store_true", help="强制保存（跳过判断）")
    parser.add_argument("--url", default=os.environ.get("SIYUAN_API", "http://127.0.0.1:6806"),
                        help="思源 API 地址")
    parser.add_argument("--token", default=os.environ.get("SIYUAN_TOKEN", ""),
                        help="思源 API Token")
    parser.add_argument("--notebook", default=os.environ.get("SIYUAN_NOTEBOOK", ""),
                        help="笔记本 ID")

    args = parser.parse_args()

    if not args.token:
        print("错误: 请提供 API Token（--token 或环境变量 SIYUAN_TOKEN）")
        sys.exit(1)
    if not args.notebook:
        print("错误: 请提供笔记本 ID（--notebook 或环境变量 SIYUAN_NOTEBOOK）")
        sys.exit(1)

    archiver = SiyuanWikiArchiver(
        base_url=args.url,
        token=args.token,
        notebook_id=args.notebook
    )

    archiver.archive(
        topic=args.topic,
        question=args.question,
        answer=args.answer,
        sources=args.sources,
        confidence=args.confidence,
        follow_up=args.follow_up,
        auto=args.auto,
        force=args.force
    )


if __name__ == "__main__":
    main()
