# modules/notion_markers.py
"""
프롬프트 마커를 Notion 블록으로 변환하는 모듈
"""
import re

MARKER_PATTERNS = {
    '핵심요약': {
        'start': r'--핵심요약\s*시작\s*---',
        'end': r'--핵심요약\s*끝\s*---',
        'level': 2,  # heading_2
        'emoji': '🔍'
    },
    '상세분석': {
        'start': r'--상세분석\s*시작\s*---',
        'end': r'--상세분석\s*끝\s*---',
        'level': 2,
        'emoji': '📋'
    },
    '시사점': {
        'start': r'--시사점\s*시작\s*---',
        'end': r'--시사점\s*끝\s*---',
        'level': 2,
        'emoji': '💡'
    },
    '권고사항': {
        'start': r'--권고사항\s*시작\s*---',
        'end': r'--권고사항\s*끝\s*---',
        'level': 2,
        'emoji': '🛡️'
    },
    '요약': {
        'start': r'--요약\s*시작\s*---',
        'end': r'--요약\s*끝\s*---',
        'level': 2,
        'emoji': '📝'
    },
    '키워드': {
        'start': r'--키워드\s*시작\s*---',
        'end': r'--키워드\s*끝\s*---',
        'level': 2,
        'emoji': '📚'
    }
}


def remove_markers(text):
    """
    모든 마커를 제거한 텍스트 반환
    """
    result = text
    for marker_name, patterns in MARKER_PATTERNS.items():
        result = re.sub(patterns['start'], '', result, flags=re.IGNORECASE)
        result = re.sub(patterns['end'], '', result, flags=re.IGNORECASE)
    return result.strip()


def convert_markers_to_headings(text):
    """
    마커를 Notion 헤딩으로 변환
    --섹션 시작--- → ### 🎯 섹션 (섹션 유지)
    --섹션 끝--- → (제거)
    """
    result = text
    converted_sections = []

    for marker_name, patterns in MARKER_PATTERNS.items():
        # 섹션 시작 마커를 헤딩으로 변환
        heading_match = re.search(patterns['start'], result, re.IGNORECASE)

        if heading_match:
            # 섹션 끝 마커 찾기
            end_match = re.search(patterns['end'], result[heading_match.end():], re.IGNORECASE)

            if end_match:
                # 섹션 내용 추출 (헤딩 포함)
                section_start = heading_match.start()
                section_end = heading_match.end() + end_match.end() + end_match.start()

                section_content = result[section_start:section_end]

                # 시작 마커를 헤딩으로 변환
                if patterns['level'] == 2:
                    new_heading = f"### {patterns['emoji']} {marker_name.upper()}"
                elif patterns['level'] == 3:
                    new_heading = f"#### {patterns['emoji']} {marker_name.upper()}"
                else:
                    new_heading = f"## {patterns['emoji']} {marker_name.upper()}"

                # 마커 제거된 섹션 생성
                section_without_markers = re.sub(patterns['start'], '', section_content, flags=re.IGNORECASE, count=1)
                section_without_markers = re.sub(patterns['end'], '', section_without_markers, flags=re.IGNORECASE, count=1)

                # 첫 번째 줄(기존 헤딩) 제거 또는 통합
                lines = section_without_markers.split('\n')
                if lines and lines[0].strip().startswith('###'):
                    # 기존 헤딩과 새 헤딩 통합
                    section_without_markers = new_heading + '\n' + '\n'.join(lines[1:])
                else:
                    section_without_markers = new_heading + '\n' + section_without_markers.strip()

                converted_sections.append(section_without_markers)

                # 결과에서 해당 섹션 제거
                result = result[:section_start] + result[section_end:]

    # 변환된 섹션들을 원래 순서대로 복원
    # (단순 구현: 뒤에서부터 복원)
    for section in reversed(converted_sections):
        # 마지막에 추가 (위치 유지 어려움)
        result += '\n\n' + section

    return result


def extract_sections(text):
    """
    마커 기반으로 섹션별 분리
    반환: {섹션명: 내용} 딕셔너리
    """
    sections = {}

    for marker_name, patterns in MARKER_PATTERNS.items():
        start_match = re.search(patterns['start'], text, re.IGNORECASE)
        if start_match:
            # 섹션 끝 마커 찾기
            remaining = text[start_match.end():]
            end_match = re.search(patterns['end'], remaining, re.IGNORECASE)

            if end_match:
                # 섹션 내용 추출 (마커 제외)
                section_content = remaining[:end_match.start()].strip()
                sections[marker_name] = section_content

    return sections


def get_section_heading(marker_name):
    """
    마커 이름에 해당하는 Notion 헤딩 형식 반환
    """
    patterns = MARKER_PATTERNS.get(marker_name)
    if not patterns:
        return None

    if patterns['level'] == 2:
        return f"### {patterns['emoji']} {marker_name.upper()}"
    elif patterns['level'] == 3:
        return f"#### {patterns['emoji']} {marker_name.upper()}"
    else:
        return f"## {patterns['emoji']} {marker_name.upper()}"
