#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
공식 문서 추천 엔진 (Official Document Recommendation Engine)

항공 규정, 표준, 지침 등의 공식 문서를 분석하고 추천하는 엔진입니다.
주제와 키워드를 기반으로 관련 문서를 찾아 적합도 순으로 정렬합니다.

사용법:
    python doc_recommender.py analyze --input data.json
    python doc_recommender.py recommend --keywords "eVTOL UAM" --top 5 --output recommendations.json
    python doc_recommender.py compare --topic "remote-id" --issuers "FAA,EASA" --output comparison.json
    python doc_recommender.py history --document "AD-2024-001" --output history.json
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple, Set, Optional


class KeywordExtractor:
    """
    키워드 추출기

    텍스트, JSON 파일, URL 등 다양한 소스에서 키워드를 추출하고 정규화합니다.
    """

    # 항공 도메인 특화 용어 정규식
    AVIATION_TERMS = {
        r'\b(AD|Airworthiness\s+Directive)\b': 'airworthiness_directive',
        r'\b(NOTAM)\b': 'notam',
        r'\b(eVTOL|electric\s+vertical\s+takeoff)\b': 'evtol',
        r'\b(UAM|Urban\s+Air\s+Mobility)\b': 'uam',
        r'\b(Annex\s+\d+)\b': 'icao_annex',
        r'\bPart\s+(\d+)\b': 'cfr_part',
        r'\b(CFR|Code\s+of\s+Federal\s+Regulations)\b': 'cfr',
        r'\b(UAS|Unmanned\s+Aircraft\s+System)\b': 'uas',
        r'\b(RPAS)\b': 'rpas',
        r'\b(FASS|Flight\s+Airworthiness\s+Support\s+Service)\b': 'fass',
        r'\b(TSO|Technical\s+Standard\s+Order)\b': 'tso',
        r'\b(AC|Advisory\s+Circular)\b': 'advisory_circular',
        r'\b(FAA)\b': 'faa',
        r'\b(EASA)\b': 'easa',
        r'\b(ICAO)\b': 'icao',
        r'\b(CASA)\b': 'casa',
        r'\b(remote\s+identification|remote-?id)\b': 'remote_id',
        r'\b(detect\s+and\s+avoid|DAA)\b': 'detect_avoid',
        r'\b(sense\s+and\s+avoid|SAA)\b': 'sense_avoid',
    }

    # 일반 정지어 (불필요한 키워드 제거)
    STOPWORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'from', 'by', 'is', 'are', 'be', 'been', 'being', 'have', 'has',
        'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
        'might', 'can', 'must', 'shall', 'this', 'that', 'these', 'those',
        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who',
        'when', 'where', 'why', 'how', 'as', 'if', 'unless', 'because', 'so',
        'than', 'with', 'without', 'as', 'up', 'down', 'out', 'about', 'over',
    }

    def __init__(self):
        """키워드 추출기 초기화"""
        self.extracted_keywords: Set[str] = set()

    def extract_from_text(self, text: str) -> Set[str]:
        """
        텍스트에서 키워드를 추출합니다.

        Args:
            text: 분석할 텍스트

        Returns:
            추출된 키워드 집합
        """
        keywords = set()

        # 1. 항공 도메인 특화 용어 추출
        for pattern, normalized_term in self.AVIATION_TERMS.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                keywords.add(normalized_term)

        # 2. 일반 용어 추출 (3글자 이상의 단어)
        words = re.findall(r'\b\w{3,}\b', text.lower())
        for word in words:
            if word not in self.STOPWORDS:
                keywords.add(word)

        # 3. 하이픈으로 연결된 복합어 추출
        hyphenated = re.findall(r'\b\w+-\w+\b', text.lower())
        for term in hyphenated:
            keywords.add(term)

        self.extracted_keywords = keywords
        return keywords

    def extract_from_json(self, json_data: Dict[str, Any]) -> Set[str]:
        """
        JSON 구조에서 키워드를 추출합니다.

        expected JSON schema:
        {
            "items": [
                {
                    "title": "...",
                    "content": "...",
                    "tags": [...],
                    "category": "..."
                }
            ]
        }

        Args:
            json_data: JSON 데이터 객체

        Returns:
            추출된 키워드 집합
        """
        keywords = set()

        if not isinstance(json_data, dict) or 'items' not in json_data:
            return keywords

        items = json_data.get('items', [])
        if not isinstance(items, list):
            return keywords

        for item in items:
            if not isinstance(item, dict):
                continue

            # title에서 키워드 추출
            if 'title' in item and isinstance(item['title'], str):
                keywords.update(self.extract_from_text(item['title']))

            # content에서 키워드 추출
            if 'content' in item and isinstance(item['content'], str):
                keywords.update(self.extract_from_text(item['content']))

            # tags를 직접 추가
            if 'tags' in item and isinstance(item['tags'], list):
                for tag in item['tags']:
                    if isinstance(tag, str):
                        keywords.add(tag.lower().strip())

            # category를 추가
            if 'category' in item and isinstance(item['category'], str):
                keywords.add(item['category'].lower().strip())

        self.extracted_keywords = keywords
        return keywords

    def extract_from_file(self, file_path: str) -> Set[str]:
        """
        파일에서 키워드를 추출합니다.

        Args:
            file_path: JSON 파일 경로

        Returns:
            추출된 키워드 집합
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            return self.extract_from_json(json_data)
        except (json.JSONDecodeError, IOError) as e:
            print(f"오류: 파일을 읽을 수 없습니다 ({file_path}): {e}", file=sys.stderr)
            return set()

    def normalize_keywords(self, keywords: Set[str]) -> Set[str]:
        """
        키워드를 정규화합니다 (중복 제거, 소문자 변환 등).

        Args:
            keywords: 정규화할 키워드 집합

        Returns:
            정규화된 키워드 집합
        """
        normalized = set()
        for keyword in keywords:
            # 공백 정리, 소문자 변환
            keyword = keyword.strip().lower()
            # 빈 문자열 제거
            if keyword:
                normalized.add(keyword)

        return normalized

    def expand_abbreviations(self, keywords: Set[str]) -> Set[str]:
        """
        약자를 확장합니다.

        Args:
            keywords: 확장할 키워드 집합

        Returns:
            확장된 키워드 집합
        """
        abbrev_map = {
            'ad': ['airworthiness_directive', 'ad'],
            'uam': ['urban_air_mobility', 'uam'],
            'evtol': ['electric_vertical_takeoff', 'evtol'],
            'uas': ['unmanned_aircraft_system', 'uas'],
            'faa': ['federal_aviation_administration', 'faa'],
            'easa': ['european_aviation_safety_agency', 'easa'],
            'icao': ['international_civil_aviation_organization', 'icao'],
        }

        expanded = set(keywords)
        for keyword in keywords:
            if keyword in abbrev_map:
                expanded.update(abbrev_map[keyword])

        return expanded


class DocumentMatcher:
    """
    문서 매칭 엔진

    지식 기반(Knowledge Base)을 로드하고 키워드와 매칭하여
    관련 문서를 찾습니다.
    """

    def __init__(self, knowledge_base_path: str):
        """
        문서 매칭기 초기화

        Args:
            knowledge_base_path: 지식 기반 JSON 파일 경로
        """
        self.knowledge_base_path = knowledge_base_path
        self.documents: List[Dict[str, Any]] = []
        self.load_knowledge_base()

    def load_knowledge_base(self) -> bool:
        """
        지식 기반을 로드합니다.

        Expected KB schema:
        {
            "documents": [
                {
                    "id": "AD-2024-001",
                    "title": "...",
                    "type": "airworthiness_directive",
                    "issuer": "FAA",
                    "url": "...",
                    "status": "active",
                    "tags": [...],
                    "keywords": [...],
                    "last_updated": "2024-01-15T10:30:00Z"
                }
            ],
            "version": "1.0"
        }

        Returns:
            성공 여부
        """
        try:
            path = Path(self.knowledge_base_path)
            if not path.exists():
                print(f"경고: 지식 기반 파일을 찾을 수 없습니다: {self.knowledge_base_path}", file=sys.stderr)
                self.documents = []
                return False

            with open(path, 'r', encoding='utf-8') as f:
                kb_data = json.load(f)

            # 최상위 documents 키 또는 domains.*.documents 구조 모두 지원
            if 'documents' in kb_data and isinstance(kb_data['documents'], list):
                self.documents = kb_data['documents']
            elif 'domains' in kb_data:
                # domains 구조에서 모든 도메인의 documents를 합침
                all_docs = []
                for domain_name, domain_data in kb_data['domains'].items():
                    if isinstance(domain_data, dict) and 'documents' in domain_data:
                        for doc in domain_data['documents']:
                            doc['domain'] = domain_name  # 도메인 태그 추가
                            all_docs.append(doc)
                self.documents = all_docs
            else:
                self.documents = []
            return True
        except (json.JSONDecodeError, IOError) as e:
            print(f"오류: 지식 기반을 로드할 수 없습니다: {e}", file=sys.stderr)
            self.documents = []
            return False

    def calculate_relevance_score(
        self,
        keywords: Set[str],
        document: Dict[str, Any],
        domain: Optional[str] = None
    ) -> float:
        """
        문서의 적합도 점수를 계산합니다.

        TF-IDF 스타일의 키워드 오버랩 점수를 기반으로 합니다.

        Args:
            keywords: 검색 키워드
            document: 문서 객체
            domain: 도메인 (예: 'aviation')

        Returns:
            적합도 점수 (0.0 ~ 1.0)
        """
        if not keywords:
            return 0.0

        # 문서의 키워드와 태그 추출 (소문자로 정규화)
        doc_keywords = set()
        for kw in document.get('keywords', []):
            doc_keywords.add(kw.lower() if isinstance(kw, str) else str(kw).lower())
        for tag in document.get('tags', []):
            doc_keywords.add(tag.lower() if isinstance(tag, str) else str(tag).lower())

        # 제목에서도 키워드 추출
        title = document.get('title', '').lower()
        title_words = set(re.findall(r'\b\w+\b', title))
        doc_keywords.update(title_words)

        # description에서도 키워드 추출
        desc = document.get('description', '').lower()
        desc_words = set(re.findall(r'\b\w{2,}\b', desc))
        doc_keywords.update(desc_words)

        # id에서도 키워드 추출
        doc_id = document.get('id', '').lower()
        id_words = set(re.findall(r'\b\w+\b', doc_id))
        doc_keywords.update(id_words)

        if not doc_keywords:
            return 0.0

        # 기본 점수: 양방향 매칭
        # 소문자로 정규화된 검색 키워드
        lower_keywords = {kw.lower() for kw in keywords}
        matched_keywords = lower_keywords & doc_keywords

        if not matched_keywords:
            return 0.0

        # 매칭 비율: 문서 핵심 키워드 중 몇 개가 매칭되었나
        core_keywords = set()
        for kw in document.get('keywords', []):
            core_keywords.add(kw.lower() if isinstance(kw, str) else str(kw).lower())
        core_match_count = len(lower_keywords & core_keywords) if core_keywords else 0
        keyword_match_score = min(core_match_count / max(len(core_keywords), 1), 1.0) if core_keywords else len(matched_keywords) / max(len(doc_keywords), 1)

        # 도메인 보너스
        domain_bonus = 0.0
        if domain and document.get('domain') == domain:
            domain_bonus = 0.1

        # 최근성 보너스
        recency_bonus = 0.0
        if 'last_updated' in document:
            try:
                last_updated = datetime.fromisoformat(
                    document['last_updated'].replace('Z', '+00:00')
                )
                days_old = (datetime.now(last_updated.tzinfo) - last_updated).days
                # 최근 30일: 0.05, 그 이전: 0.0
                if days_old <= 30:
                    recency_bonus = 0.05
                elif days_old <= 180:
                    recency_bonus = 0.02
            except (ValueError, TypeError):
                pass

        # 상태 가중치 (활성 문서 선호)
        status_weight = 1.0
        if document.get('status') == 'active':
            status_weight = 1.0
        elif document.get('status') == 'deprecated':
            status_weight = 0.3
        else:
            status_weight = 0.5

        # 최종 점수 계산 (0.0 ~ 1.0)
        final_score = (keyword_match_score * 0.7 + domain_bonus + recency_bonus) * status_weight
        return min(final_score, 1.0)

    def match_documents(
        self,
        keywords: Set[str],
        domain: Optional[str] = None,
        top_n: int = 10
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        키워드와 매칭되는 문서를 찾습니다.

        Args:
            keywords: 검색 키워드
            domain: 도메인 필터 (선택사항)
            top_n: 반환할 상위 문서 개수

        Returns:
            (문서, 점수) 튜플 리스트, 점수 내림차순 정렬
        """
        scored_docs = []

        for doc in self.documents:
            score = self.calculate_relevance_score(keywords, doc, domain)
            if score > 0.0:
                scored_docs.append((doc, score))

        # 점수 기준으로 내림차순 정렬
        scored_docs.sort(key=lambda x: x[1], reverse=True)

        return scored_docs[:top_n]


class RecommendationEngine:
    """
    추천 엔진

    전체 파이프라인을 조율합니다: 키워드 추출 -> 문서 매칭 -> 추천 생성
    """

    def __init__(self, knowledge_base_path: str):
        """
        추천 엔진 초기화

        Args:
            knowledge_base_path: 지식 기반 파일 경로
        """
        self.extractor = KeywordExtractor()
        self.matcher = DocumentMatcher(knowledge_base_path)

    def analyze(
        self,
        input_file: Optional[str] = None,
        keywords: Optional[str] = None,
        url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        주어진 입력에서 키워드를 추출합니다.

        Args:
            input_file: JSON 입력 파일 경로
            keywords: 직접 입력한 키워드 (공백으로 구분)
            url: URL (현재 미지원)

        Returns:
            분석 결과
        """
        extracted_keywords = set()
        source = ""

        if input_file:
            extracted_keywords = self.extractor.extract_from_file(input_file)
            source = f"파일: {input_file}"
        elif keywords:
            extracted_keywords = set(kw.strip().lower() for kw in keywords.split())
            source = "직접 입력"
        elif url:
            # URL 지원은 추후 구현
            print("오류: URL 분석은 아직 지원되지 않습니다.", file=sys.stderr)
            return {}
        else:
            print("오류: 입력 소스를 지정해주세요 (--input, --keywords, or --url)", file=sys.stderr)
            return {}

        # 키워드 정규화 및 확장
        normalized = self.extractor.normalize_keywords(extracted_keywords)
        expanded = self.extractor.expand_abbreviations(normalized)

        return {
            "source": source,
            "extracted_keywords": sorted(list(extracted_keywords)),
            "normalized_keywords": sorted(list(normalized)),
            "expanded_keywords": sorted(list(expanded)),
            "keyword_count": len(expanded),
        }

    def recommend(
        self,
        input_file: Optional[str] = None,
        keywords: Optional[str] = None,
        domain: str = "aviation",
        top_n: int = 10
    ) -> Dict[str, Any]:
        """
        키워드 기반 문서를 추천합니다.

        Args:
            input_file: JSON 입력 파일
            keywords: 직접 입력한 키워드
            domain: 도메인 (기본값: 'aviation')
            top_n: 반환할 추천 문서 개수

        Returns:
            추천 결과
        """
        # 키워드 추출
        extracted_keywords = set()
        if input_file:
            extracted_keywords = self.extractor.extract_from_file(input_file)
        elif keywords:
            extracted_keywords = set(kw.strip().lower() for kw in keywords.split())
        else:
            print("오류: 입력 소스를 지정해주세요", file=sys.stderr)
            return {}

        # 키워드 정규화 및 확장
        normalized = self.extractor.normalize_keywords(extracted_keywords)
        expanded = self.extractor.expand_abbreviations(normalized)

        # 문서 매칭
        matched_docs = self.matcher.match_documents(expanded, domain, top_n)

        # 결과 포맷팅
        recommendations = []
        for rank, (doc, score) in enumerate(matched_docs, 1):
            recommendations.append({
                "rank": rank,
                "relevance_score": round(score, 4),
                "document": {
                    "id": doc.get("id", ""),
                    "title": doc.get("title", ""),
                    "type": doc.get("type", ""),
                    "issuer": doc.get("issuer", ""),
                    "url": doc.get("url", ""),
                    "status": doc.get("status", ""),
                },
                "relevance_context": self._build_relevance_context(doc, expanded),
                "related_documents": doc.get("related_documents", []),
                "tags": doc.get("tags", []),
            })

        return {
            "query": {
                "keywords": sorted(list(expanded)),
                "domain": domain,
                "context": "",
            },
            "recommendations": recommendations,
            "metadata": {
                "total_recommendations": len(recommendations),
                "generated_at": datetime.utcnow().isoformat() + "Z",
                "knowledge_base_version": "1.0",
            },
        }

    def compare(
        self,
        topic: str,
        issuers: List[str],
        top_n: int = 5
    ) -> Dict[str, Any]:
        """
        여러 발행처의 문서를 비교합니다.

        Args:
            topic: 주제
            issuers: 발행처 목록 (예: ['FAA', 'EASA'])
            top_n: 각 발행처당 반환할 문서 개수

        Returns:
            비교 결과
        """
        topic_keywords = set(topic.lower().split())
        comparison = {
            "topic": topic,
            "issuers": {},
            "generated_at": datetime.utcnow().isoformat() + "Z",
        }

        for issuer in issuers:
            # 발행처별로 문서 필터링
            issuer_docs = [doc for doc in self.matcher.documents if doc.get("issuer") == issuer]

            # 점수 계산
            scored_docs = []
            for doc in issuer_docs:
                score = self.matcher.calculate_relevance_score(topic_keywords, doc)
                if score > 0.0:
                    scored_docs.append((doc, score))

            scored_docs.sort(key=lambda x: x[1], reverse=True)

            comparison["issuers"][issuer] = [
                {
                    "id": doc.get("id", ""),
                    "title": doc.get("title", ""),
                    "type": doc.get("type", ""),
                    "url": doc.get("url", ""),
                    "relevance_score": round(score, 4),
                }
                for doc, score in scored_docs[:top_n]
            ]

        return comparison

    def history(
        self,
        document_id: str
    ) -> Dict[str, Any]:
        """
        문서의 개정 이력을 조회합니다.

        Args:
            document_id: 문서 ID

        Returns:
            개정 이력
        """
        # 문서 찾기
        target_doc = None
        for doc in self.matcher.documents:
            if doc.get("id") == document_id:
                target_doc = doc
                break

        if not target_doc:
            return {
                "document_id": document_id,
                "found": False,
                "message": "문서를 찾을 수 없습니다.",
            }

        # 이력 데이터 추출
        history_data = {
            "document_id": document_id,
            "found": True,
            "current": {
                "id": target_doc.get("id", ""),
                "title": target_doc.get("title", ""),
                "status": target_doc.get("status", ""),
                "last_updated": target_doc.get("last_updated", ""),
            },
            "revisions": target_doc.get("revisions", []),
            "generated_at": datetime.utcnow().isoformat() + "Z",
        }

        return history_data

    def _build_relevance_context(
        self,
        document: Dict[str, Any],
        keywords: Set[str]
    ) -> str:
        """
        문서가 왜 관련성이 있는지 설명하는 텍스트를 생성합니다.

        Args:
            document: 문서
            keywords: 검색 키워드

        Returns:
            관련성 설명 텍스트
        """
        doc_keywords = set(document.get('keywords', []))
        doc_keywords.update(document.get('tags', []))

        matched = keywords & doc_keywords

        if not matched:
            return f"{document.get('type', '문서')}로서 도움이 될 수 있습니다."

        matched_str = ", ".join(sorted(list(matched))[:3])
        return f"다음 키워드를 포함합니다: {matched_str}"


def main():
    """
    메인 함수 - argparse CLI 실행
    """
    parser = argparse.ArgumentParser(
        description="공식 문서 추천 엔진",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예제:
  # 파일에서 키워드 추출
  %(prog)s analyze --input data.json

  # 직접 입력한 키워드로 추천
  %(prog)s recommend --keywords "eVTOL UAM" --top 5 --output recommendations.json

  # 여러 발행처 비교
  %(prog)s compare --topic "remote-id" --issuers FAA EASA --output comparison.json

  # 문서 개정 이력 조회
  %(prog)s history --document "AD-2024-001" --output history.json
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='실행할 명령어')

    # ========== analyze 명령어 ==========
    analyze_parser = subparsers.add_parser('analyze', help='키워드 추출 분석')
    analyze_group = analyze_parser.add_mutually_exclusive_group(required=True)
    analyze_group.add_argument(
        '--input',
        type=str,
        help='분석할 JSON 입력 파일 경로'
    )
    analyze_group.add_argument(
        '--keywords',
        type=str,
        help='공백으로 구분한 키워드'
    )
    analyze_group.add_argument(
        '--url',
        type=str,
        help='분석할 URL (현재 미지원)'
    )
    analyze_parser.add_argument(
        '--output',
        type=str,
        help='결과를 저장할 JSON 파일 경로 (선택사항)'
    )

    # ========== recommend 명령어 ==========
    recommend_parser = subparsers.add_parser('recommend', help='문서 추천')
    recommend_group = recommend_parser.add_mutually_exclusive_group(required=True)
    recommend_group.add_argument(
        '--input',
        type=str,
        help='분석할 JSON 입력 파일 경로'
    )
    recommend_group.add_argument(
        '--keywords',
        type=str,
        help='공백으로 구분한 키워드'
    )
    recommend_parser.add_argument(
        '--domain',
        type=str,
        default='aviation',
        help='필터링할 도메인 (기본값: aviation)'
    )
    recommend_parser.add_argument(
        '--top',
        type=int,
        default=10,
        dest='top_n',
        help='반환할 상위 추천 개수 (기본값: 10)'
    )
    recommend_parser.add_argument(
        '--output',
        type=str,
        help='결과를 저장할 JSON 파일 경로'
    )

    # ========== compare 명령어 ==========
    compare_parser = subparsers.add_parser('compare', help='발행처별 문서 비교')
    compare_parser.add_argument(
        '--topic',
        type=str,
        required=True,
        help='비교할 주제'
    )
    compare_parser.add_argument(
        '--issuers',
        type=str,
        required=True,
        nargs='+',
        help='비교할 발행처 (예: FAA EASA ICAO)'
    )
    compare_parser.add_argument(
        '--top',
        type=int,
        default=5,
        dest='top_n',
        help='각 발행처당 반환할 문서 개수 (기본값: 5)'
    )
    compare_parser.add_argument(
        '--output',
        type=str,
        help='결과를 저장할 JSON 파일 경로'
    )

    # ========== history 명령어 ==========
    history_parser = subparsers.add_parser('history', help='문서 개정 이력 조회')
    history_parser.add_argument(
        '--document',
        type=str,
        required=True,
        help='조회할 문서 ID (예: AD-2024-001)'
    )
    history_parser.add_argument(
        '--output',
        type=str,
        help='결과를 저장할 JSON 파일 경로'
    )

    args = parser.parse_args()

    # 명령어가 없으면 도움말 출력
    if not args.command:
        parser.print_help()
        sys.exit(0)

    # 지식 기반 경로 구성
    script_dir = Path(__file__).parent
    kb_path = script_dir.parent / 'references' / 'doc_knowledge_base.json'

    # 추천 엔진 초기화
    engine = RecommendationEngine(str(kb_path))

    result = None

    # ========== analyze 실행 ==========
    if args.command == 'analyze':
        result = engine.analyze(
            input_file=args.input,
            keywords=args.keywords,
            url=args.url if hasattr(args, 'url') else None
        )

        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))

            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print(f"결과가 저장되었습니다: {args.output}", file=sys.stderr)

    # ========== recommend 실행 ==========
    elif args.command == 'recommend':
        result = engine.recommend(
            input_file=args.input if hasattr(args, 'input') else None,
            keywords=args.keywords if hasattr(args, 'keywords') else None,
            domain=args.domain,
            top_n=args.top_n
        )

        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))

            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print(f"결과가 저장되었습니다: {args.output}", file=sys.stderr)

    # ========== compare 실행 ==========
    elif args.command == 'compare':
        result = engine.compare(
            topic=args.topic,
            issuers=args.issuers,
            top_n=args.top_n
        )

        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))

            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print(f"결과가 저장되었습니다: {args.output}", file=sys.stderr)

    # ========== history 실행 ==========
    elif args.command == 'history':
        result = engine.history(document_id=args.document)

        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))

            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print(f"결과가 저장되었습니다: {args.output}", file=sys.stderr)


if __name__ == '__main__':
    main()
