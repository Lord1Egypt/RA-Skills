#!/usr/bin/env python3
"""
L1: Session Scanner with Byte Offset
扫描 OpenClaw session JSONL 文件，自维护 byte offset，支持断点续扫。

流程原则（防断裂 + 高质量）：
  Stage 0: 保护性写入（scan 后立即落盘，不在内存堆积）
  Stage 1: Scanner 层过滤（只丢弃100%确定是噪音的内容）
           边界情况 → 交给 Classifier 二次判断（不丢弃）

过滤优先级（从高到低）：
  1. 空内容 / 纯系统指令 → 丢弃
  2. cron 系统命令 → 丢弃（用户不会以 [cron: 开头）
  3. 极短 metadata（<10字符）→ 丢弃
  4. UUID 行 → 丢弃
  5. metadata prefix 截断（不丢弃，只清理）
  6. 时间戳前缀截断（不丢弃，只清理）
  7. 残留 JSON 代码块 → 截断
  8. 边界情况 → 保留，交给 Classifier 语义密度检查

存储位置: /workspace/fusion/memory/_state/scan_sessions_incremental.json
"""

import json
import os
import re
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


# 项目根目录（向上推导）
PROJECT_ROOT = Path(__file__).parent.parent.parent
# 配置
SESSIONS_DIR = os.path.expanduser("~/.openclaw/agents/main/sessions")
STATE_FILE = str(PROJECT_ROOT / "memory" / "_state" / "scan_sessions_incremental.json")
MAX_CONTENT_LENGTH = 5000

# 7天滚动 TTL
TTL_DAYS = 7

# 保护性写入临时文件（crash 可恢复）
RAW_CHUNKS_TMP_FILE = str(PROJECT_ROOT / "memory" / "_state" / "l1_raw_chunks_tmp.jsonl")


class ByteOffsetScanner:
    """字节偏移量扫描器，自维护 offset，支持断点续扫。"""

    def __init__(self, sessions_dir: str = SESSIONS_DIR, state_file: str = STATE_FILE):
        self.sessions_dir = Path(sessions_dir)
        self.state_file = Path(state_file)
        self.state = self._load_state()

    def _load_state(self) -> dict:
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {"offsets": {}, "last_scan": None}
        return {"offsets": {}, "last_scan": None}

    def _save_state(self):
        """保存状态文件（atomic write）。"""
        tmp_file = self.state_file.with_suffix('.tmp')
        with open(tmp_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
        tmp_file.rename(self.state_file)

    def _get_session_files(self) -> list[Path]:
        """获取所有 session JSONL 文件（排除 .reset / .checkpoint / .lock）。"""
        if not self.sessions_dir.exists():
            return []
        return [
            f for f in self.sessions_dir.iterdir()
            if f.suffix == '.jsonl'
            and '.reset' not in f.name
            and '.checkpoint' not in f.name
            and '.lock' not in f.name
        ]

    def _clean_stale_offsets(self):
        """清理超过 7 天的 offset 记录（滚动 TTL）。"""
        now = datetime.now(timezone.utc)
        cutoff = now.timestamp() - (TTL_DAYS * 86400)

        offsets = self.state.get("offsets", {})
        cleaned = {}
        for session_id, offset_info in offsets.items():
            last_position_time = offset_info.get("last_position_time", 0)
            if last_position_time >= cutoff:
                cleaned[session_id] = offset_info

        removed_count = len(offsets) - len(cleaned)
        self.state["offsets"] = cleaned
        if removed_count > 0:
            print(f"[L1 Scanner] 清理了 {removed_count} 条超过 7 天的 offset 记录")
        return removed_count

    def _stage0_protective_write(self, chunks: list[dict]):
        """
        Stage 0: 保护性写入
        扫描完成后立即写入 tmp 文件，不在内存堆积。
        crash 后可从 tmp 文件恢复。
        """
        os.makedirs(os.path.dirname(RAW_CHUNKS_TMP_FILE), exist_ok=True)
        tmp_file = RAW_CHUNKS_TMP_FILE + ".writing"
        with open(tmp_file, 'w', encoding='utf-8') as f:
            for chunk in chunks:
                f.write(json.dumps(chunk, ensure_ascii=False) + '\n')
        Path(tmp_file).rename(Path(RAW_CHUNKS_TMP_FILE))

    def scan(self) -> list[dict]:
        """
        扫描所有 session 文件，返回需要处理的 chunks。
        使用 byte offset 断点续扫，只处理新内容。
        """
        self._clean_stale_offsets()

        session_files = self._get_session_files()
        if not session_files:
            print(f"[L1 Scanner] 未找到 session 文件: {self.sessions_dir}")
            return []

        results = []
        for session_file in session_files:
            session_id = session_file.stem
            chunks = self._scan_session(session_id, session_file)
            results.extend(chunks)

        self.state["last_scan"] = datetime.now(timezone.utc).isoformat()
        self._save_state()

        # Stage 0: 保护性写入
        if results:
            self._stage0_protective_write(results)

        print(f"[L1 Scanner] 扫描完成，处理 {len(results)} 条 chunks")
        return results

    def _scan_session(self, session_id: str, session_file: Path) -> list[dict]:
        """扫描单个 session 文件，使用 byte offset 断点续扫。"""
        current_offset = self.state["offsets"].get(session_id, {}).get("position", 0)
        file_size = session_file.stat().st_size

        if current_offset >= file_size:
            return []

        chunks = []

        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                if current_offset > 0:
                    f.seek(current_offset)

                while f.tell() < file_size:
                    line_pos = f.tell()
                    line = f.readline()
                    if not line:
                        break

                    try:
                        obj = json.loads(line)
                        if obj.get('type') == 'message':
                            msg = obj.get('message', {})
                            if msg.get('role') == 'user':
                                content = self._extract_content(msg.get('content', []))
                                # 只过滤极短内容（<10），其他交给 Stage 1
                                if content and len(content.strip()) >= 5:
                                    chunk = self._parse_user_message(session_id, content, line_pos)
                                    if chunk:
                                        chunks.append(chunk)
                    except json.JSONDecodeError:
                        continue

                new_offset = f.tell()
                self.state["offsets"][session_id] = {
                    "position": new_offset,
                    "last_position_time": datetime.now(timezone.utc).timestamp(),
                    "file_size": file_size
                }

        except Exception as e:
            print(f"[L1 Scanner] 扫描 session {session_id} 失败: {e}")

        return chunks

    def _extract_content(self, content: list) -> str:
        """从 message content 列表中提取文本。"""
        if not content:
            return ""
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            texts = []
            for block in content:
                if isinstance(block, dict):
                    if block.get('type') == 'text':
                        texts.append(block.get('text', ''))
                    elif block.get('type') == 'image':
                        texts.append('[IMAGE]')
                    elif block.get('type') == 'file':
                        texts.append('[FILE]')
            return '\n'.join(texts)
        return str(content)

    def _stage1_filter(self, content: str) -> tuple[bool, str, str]:
        """
        Stage 1: Scanner 层过滤
        原则：只丢弃100%确定是噪音的内容
              边界情况 → 保留，交给 Classifier 语义密度检查

        返回 (should_keep, filtered_content, reason)
        """
        original = content

        # ===== 过滤器 1: 极短内容（<10字符）→ 丢弃 =====
        # 但：如果有 ≥4 个中文字符，说明有语义内容，不丢弃（交给 Classifier 判断）
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', content)
        if len(content.strip()) < 10 and len(chinese_chars) < 4:
            return False, "", "too_short"
        # 有中文内容的短内容，交给 Classifier 做语义密度检查

        # ===== 过滤器 2: cron 系统命令（用户不会以 [cron: 开头）=====
        # 格式: [cron:uuid L1_scan_07UTC]
        if re.match(r'^\[cron:[a-f0-9\-]+\s+\w+\]', content):
            # 二次确认：检查是否包含系统命令关键字（确保不是用户输入的假 cron）
            if 'cd /workspace' in content or 'python' in content or '&&' in content:
                return False, "", "cron_system_command"
            # 否则保留（用户可能以 [cron: 开头写别的东西）

        # ===== 过滤器 3: 纯系统指令 → 丢弃 =====
        if re.match(r'^(HEARTBEAT(_OK)?|_SESSION|_CONTEXT|_AGENT)\s*$', content.strip()):
            return False, "", "pure_system_instruction"

        # ===== 过滤器 4: 纯 UUID 行 → 丢弃 =====
        if re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\s*$', content.strip()):
            return False, "", "pure_uuid"

        # ===== 过滤器 5: 空代码块残留 → 丢弃 =====
        if re.match(r'^```(json|python|bash)?\s*$', content.strip()) or content.strip() == '```':
            return False, "", "empty_code_block"

        # ===== 过滤器 6: metadata prefix 截断（不丢弃，只清理）=====
        # 格式: Sender (untrusted metadata):\n```json\n{...}\n```\n...
        if content.startswith('Sender '):
            lines = content.split('\n')
            filtered_lines = []
            skip_until_bracket = False
            hit_timestamp = False

            for line in lines:
                # 跳过 json 代码块
                if line.strip().startswith('```json'):
                    skip_until_bracket = True
                    continue
                if line.strip().startswith('```'):
                    skip_until_bracket = False
                    continue
                if skip_until_bracket:
                    continue

                # 遇到时间戳停止，但保留时间戳后的内容
                if re.match(r'^\[(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+\d{4}', line.strip()):
                    hit_timestamp = True
                    # 时间戳本身不保留（用户不需要看到时间戳）
                    # 但这个时间戳后的内容可能很重要，继续处理
                    # 不 break，继续检查后续行
                    continue

                filtered_lines.append(line)

            content = '\n'.join(filtered_lines).strip()

            # 如果截断后内容 < 10 字符，检查原始内容中文字符数
            if len(content) < 10:
                chinese_chars = re.findall(r'[\u4e00-\u9fff]', original)
                if len(chinese_chars) < 4:
                    return False, "", "metadata_content_too_short"
                # 否则保留（有中文内容，只是被 metadata 分割了）

        # ===== 过滤器 7: 时间戳前缀截断（不丢弃，只清理）=====
        # 格式: [Sat 2026-04-25 09:23 GMT+8] 或 [Fri 2026-04-24 14:00 GMT+8]
        before_strip_len = len(content)
        content = re.sub(
            r'^\[(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\s+GMT[+-]\d+\]\s*',
            '',
            content
        )

        # 如果截断后内容 < 10 字符，检查原始内容中是否有实质内容
        if len(content.strip()) < 10 and before_strip_len > 30:
            chinese_chars = re.findall(r'[\u4e00-\u9fff]', original)
            if len(chinese_chars) < 4:
                return False, "", "timestamp_content_too_short"
            # 否则保留（有实质内容，只是消息很短）

        # ===== 过滤器 8: 残留 metadata JSON → 截断 =====
        # 残留的 json metadata block（如 {"label": "..."}）
        if re.match(r'^[{]\s*["\']?label["\']?\s*:', content.strip()) or \
           re.match(r'^[{]\s*["\']?id["\']?\s*:', content.strip()):
            # 保留后续内容，只截断前面的 JSON
            content = re.sub(r'^[{]\s*["\']?(label|id)["\']?\s*:\s*["\'][^"\']+["\']\s*[,}]?\s*', '', content).strip()
            if not content:
                return False, "", "residual_json_only"

        # ===== 过滤器 9: metadata 前缀标签 → 丢弃 =====
        # 格式: Sender (untrusted metadata):
        # 这是系统元信息标签，不是用户内容，直接丢弃
        if content.startswith('Sender (untrusted metadata):'):
            return False, "", "metadata_label"

        # ===== 过滤器 10: OpenClaw system prefix 截断（不丢弃，只清理）=====
        if re.match(r'^\[(system|agent|openclaw)[^]]+\]', content):
            content = re.sub(r'^\[(system|agent|openclaw)[^]]+\]\s*', '', content)

        # ===== 最终：内容为空 → 丢弃 =====
        if not content or len(content.strip()) < 5:
            return False, "", "content_empty_after_filter"

        return True, content, "ok"

    def _parse_user_message(self, session_id: str, content: str, line_pos: int) -> Optional[dict]:
        """
        Stage 1: Scanner 层过滤入口
        应用 Stage 1 过滤规则。
        边界情况 → 保留，交给 Classifier 做语义密度检查。
        """
        should_keep, filtered_content, reason = self._stage1_filter(content)

        if not should_keep:
            return None

        if not filtered_content or len(filtered_content.strip()) < 20:
            return None

        # 生成唯一 ID：使用 session_id + byte_offset + content 前100字符
        # 保证同一位置、同样内容的 chunk 产生相同的 ID
        chunk_id = hashlib.sha256(
            f"{session_id}:{line_pos}:{filtered_content[:100]}".encode()
        ).hexdigest()[:16]

        timestamp = datetime.now(timezone.utc).isoformat()

        return {
            "id": chunk_id,
            "session_id": session_id,
            "content": filtered_content[:MAX_CONTENT_LENGTH],
            "byte_offset": line_pos,
            "timestamp": timestamp,
            "source": "user_message",
            "_scan_filter_reason": reason,
        }


def run():
    """L1 扫描入口。"""
    scanner = ByteOffsetScanner()
    chunks = scanner.scan()
    return chunks


if __name__ == "__main__":
    chunks = run()
    print(f"扫描完成，获得 {len(chunks)} 条 chunks")
    for chunk in chunks[:3]:
        print(f"  - {chunk['id']}: {chunk['content'][:100]}...")