#!/usr/bin/env python3
"""세션 JSONL 파일에서 중복 메시지 제거

Usage:
    python dedup-session.py <session_file>
    python dedup-session.py <session_file> --dry-run
"""

import json
import hashlib
import sys
from pathlib import Path


def get_content_richness(data: dict) -> int:
    """메시지의 content 풍부함 점수 계산 (높을수록 좋음)"""
    if not data:
        return 0

    msg_type = data.get('type', '')
    if msg_type not in ('assistant', 'user'):
        return len(json.dumps(data))

    content = data.get('message', {}).get('content', [])
    if not isinstance(content, list):
        return 0

    score = 0
    for item in content:
        if not isinstance(item, dict):
            continue
        item_type = item.get('type', '')
        # tool_use/tool_result가 있으면 높은 점수
        if item_type in ('tool_use', 'tool_result'):
            score += 1000
        # text 내용이 있으면 길이만큼 점수
        elif item_type == 'text':
            score += len(item.get('text', ''))
        # thinking은 낮은 점수 (있어도 다른 content가 없으면 별로)
        elif item_type == 'thinking':
            score += 1

    return score


def get_dedup_key(data: dict) -> str:
    """중복 판단용 키 생성

    같은 message.id는 스트리밍 단계와 무관하게 동일 메시지로 취급:
    - 스트리밍 중간 결과(text만)와 최종 결과(tool_use 포함)는 같은 키
    - get_content_richness()로 가장 풍부한 버전을 선택
    """
    msg_type = data.get('type', '')

    # assistant/user 메시지: message.id만으로 판단
    if msg_type in ('assistant', 'user'):
        msg = data.get('message', {})
        if isinstance(msg, dict) and msg.get('id'):
            return f"msg:{msg['id']}"

    # progress: tool_use_id + content 해시
    if msg_type == 'progress':
        tool_use_id = data.get('tool_use_id', '')
        content = json.dumps(data.get('content', {}), sort_keys=True)
        content_hash = hashlib.md5(content.encode()).hexdigest()[:16]
        return f"progress:{tool_use_id}:{content_hash}"

    # 기타: uuid 기준
    uuid = data.get('uuid')
    if uuid:
        return f"uuid:{uuid}"

    return f"line:{json.dumps(data, sort_keys=True)}"


def dedup_session(session_file: Path, dry_run: bool = False) -> dict:
    """세션 파일에서 중복 제거 후 체인 복구

    전략: 중복 제거 → 체인 복구 (aggressive 방식)
    1. 모든 메시지 로드
    2. 중복 그룹에서 첫 번째만 유지 (참조 여부 무관)
    3. 제거로 인해 끊어진 parentUuid 체인을 이전 메시지의 uuid로 복구

    Returns:
        dict: {
            'original_lines': int,
            'unique_lines': int,
            'duplicates_by_type': dict,
            'fixed_chains': int,
            'output_file': str (dry_run=False일 때만)
        }
    """
    # 1차 pass: 모든 메시지 로드
    messages = []

    with open(session_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                messages.append((line, data))
            except json.JSONDecodeError:
                messages.append((line, None))

    # 2차 pass: 중복 그룹화 (dedup_key → [(line, data), ...])
    dedup_groups = {}
    for line, data in messages:
        if data is None:
            key = f"raw:{line}"
        else:
            key = get_dedup_key(data)

        if key not in dedup_groups:
            dedup_groups[key] = []
        dedup_groups[key].append((line, data))

    # 3차 pass: 각 그룹에서 가장 풍부한 메시지 선택 (tool_use 우선, content 길이 기준)
    best_messages = {}  # key -> (line, data)
    for key, group in dedup_groups.items():
        # 풍부함 점수로 정렬, 가장 높은 것 선택
        best = max(group, key=lambda x: get_content_richness(x[1]))
        best_messages[key] = best

    # 원본 순서 유지하며 unique_lines 구성 (best 메시지 사용)
    unique_lines = []
    unique_data = []
    duplicates_by_type = {}
    seen_keys = set()

    for line, data in messages:
        if data is None:
            key = f"raw:{line}"
        else:
            key = get_dedup_key(data)

        if key not in seen_keys:
            # best 메시지 사용 (원본 순서의 첫 위치에 best 삽입)
            best_line, best_data = best_messages[key]
            unique_lines.append(best_line)
            unique_data.append(best_data)
            seen_keys.add(key)
        else:
            # 제거된 중복 카운트
            msg_type = data.get('type', 'unknown') if data else 'unknown'
            duplicates_by_type[msg_type] = duplicates_by_type.get(msg_type, 0) + 1

    # 4차 pass: 남은 메시지에서 모든 tool_use id 수집
    remaining_tool_use_ids = set()
    for data in unique_data:
        if data and data.get('type') == 'assistant':
            content = data.get('message', {}).get('content', [])
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get('type') == 'tool_use':
                        remaining_tool_use_ids.add(item.get('id'))

    # 5차 pass: 고아 tool_result 삭제 (tool_use_id가 남은 tool_use에 없으면 삭제)
    orphan_removed = 0
    filtered_lines = []
    filtered_data = []
    for line, data in zip(unique_lines, unique_data):
        if data and data.get('type') == 'user':
            content = data.get('message', {}).get('content', [])
            if isinstance(content, list):
                # tool_result가 있는 user 메시지인지 확인
                tool_results = [item for item in content if isinstance(item, dict) and item.get('type') == 'tool_result']
                if tool_results:
                    # 모든 tool_result의 tool_use_id가 고아인지 확인
                    all_orphan = all(
                        item.get('tool_use_id') not in remaining_tool_use_ids
                        for item in tool_results
                    )
                    if all_orphan:
                        orphan_removed += 1
                        duplicates_by_type['user (orphan tool_result)'] = duplicates_by_type.get('user (orphan tool_result)', 0) + 1
                        continue
        filtered_lines.append(line)
        filtered_data.append(data)

    unique_lines = filtered_lines
    unique_data = filtered_data

    # 6차 pass: 체인 재구축 (순차적 연결)
    # 모든 메시지가 이전 메시지를 parent로 가리키도록 강제
    fixed_chains = 0
    final_lines = []

    prev_uuid = None
    for i, (line, data) in enumerate(zip(unique_lines, unique_data)):
        if data is None:
            final_lines.append(line)
            continue

        # uuid가 없는 메시지 (file-history-snapshot 등)는 그대로 유지
        if not data.get('uuid'):
            final_lines.append(line)
            continue

        current_parent = data.get('parentUuid')
        expected_parent = prev_uuid  # 이전 메시지의 uuid

        # 첫 메시지는 parentUuid가 null이어야 함
        if i == 0 or prev_uuid is None:
            if current_parent is not None:
                data['parentUuid'] = None
                final_lines.append(json.dumps(data, ensure_ascii=False))
                fixed_chains += 1
            else:
                final_lines.append(line)
        # 이후 메시지는 이전 메시지를 가리켜야 함
        elif current_parent != expected_parent:
            data['parentUuid'] = expected_parent
            final_lines.append(json.dumps(data, ensure_ascii=False))
            fixed_chains += 1
        else:
            final_lines.append(line)

        prev_uuid = data.get('uuid')

    result = {
        'original_lines': len(messages),
        'unique_lines': len(final_lines),
        'duplicates_by_type': duplicates_by_type,
        'fixed_chains': fixed_chains,
    }

    if not dry_run:
        # .jsonl.bak 등에서도 정확한 .dedup 파일명 생성
        output_file = Path(str(session_file) + '.dedup')
        with open(output_file, 'w') as f:
            for line in final_lines:
                f.write(line + '\n')
        result['output_file'] = str(output_file)

    return result


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    session_file = Path(sys.argv[1])
    dry_run = '--dry-run' in sys.argv

    if not session_file.exists():
        print(f"Error: {session_file} not found")
        sys.exit(1)

    result = dedup_session(session_file, dry_run)

    print(f"원본 라인 수: {result['original_lines']}")
    print(f"결과 라인 수: {result['unique_lines']}")
    print(f"제거된 중복: {result['original_lines'] - result['unique_lines']}")

    if result.get('fixed_chains', 0) > 0:
        print(f"복구된 체인: {result['fixed_chains']}")

    if result['duplicates_by_type']:
        print("\n타입별 제거 수:")
        for t, c in sorted(result['duplicates_by_type'].items(), key=lambda x: -x[1]):
            print(f"  {t}: {c}")

    if not dry_run and 'output_file' in result:
        print(f"\n저장: {result['output_file']}")


if __name__ == '__main__':
    main()
