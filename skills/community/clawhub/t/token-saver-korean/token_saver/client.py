#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TokenSaver Korean - 한국어 + 영어 Context DB 클라이언트 v2.0

토큰 절감 91% 달성을 위한 다국어 최적화 클라이언트
신규 기능: 임베딩 기반 의미 검색, 중복 자동 병합, 자동 만료/아카이브, 메모리 계층화
"""

import json
import os
import re
import shutil
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable, Set, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
import time
import threading
import requests

# 한국어 형태소 분석 (선택적)
try:
    from konlpy.tag import Okt
    KONLPY_AVAILABLE = True
except ImportError:
    KONLPY_AVAILABLE = False

# 영어 NLP (선택적)
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False


@dataclass
class Context:
    """Context 객체"""
    uri: str
    abstract: str = ""
    content: str = ""
    level: int = 2  # L0=abstract, L1=overview, L2=detail
    category: str = "general"
    language: str = "auto"  # auto, ko, en
    version: int = 1  # 버전 관리
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_accessed_at: datetime = field(default_factory=datetime.now)  # NEW: 마지막 접근 시간
    access_count: int = 0  # NEW: 접근 횟수
    tier: str = "hot"  # NEW: hot/warm/cold
    meta: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "uri": self.uri,
            "abstract": self.abstract,
            "content": self.content,
            "level": self.level,
            "category": self.category,
            "language": self.language,
            "version": self.version,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_accessed_at": self.last_accessed_at.isoformat(),
            "access_count": self.access_count,
            "tier": self.tier,
            "meta": self.meta
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Context":
        """딕셔너리에서 Context 객체 생성"""
        # ISO 형식 문자열을 datetime으로 변환
        for field_name in ["created_at", "updated_at", "last_accessed_at"]:
            if field_name in data and isinstance(data[field_name], str):
                try:
                    data[field_name] = datetime.fromisoformat(data[field_name])
                except:
                    data[field_name] = datetime.now()
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class EmbeddingManager:
    """Fireworks 임베딩 API 관리자"""
    
    EMBEDDING_MODEL = "qwen3-embedding-8b"
    API_ENDPOINT = "https://api.fireworks.ai/inference/v1/embeddings"
    SIMILARITY_THRESHOLD = 0.85  # 중복 병합 임계값
    
    def __init__(self, api_key: Optional[str] = None, embeddings_path: Optional[Path] = None):
        self.api_key = api_key or os.environ.get("FIREWORKS_API_KEY")
        self.embeddings_path = embeddings_path
        self._embeddings_cache: Dict[str, List[float]] = {}
        self._lock = threading.Lock()
        
        # 기존 임베딩 로드
        if self.embeddings_path and self.embeddings_path.exists():
            self._load_embeddings()
    
    def _load_embeddings(self):
        """임베딩 파일 로드"""
        try:
            with open(self.embeddings_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._embeddings_cache = {k: v for k, v in data.items()}
        except Exception as e:
            print(f"[Embedding] 임베딩 로드 실패: {e}")
    
    def _save_embeddings(self):
        """임베딩 파일 저장"""
        if not self.embeddings_path:
            return
        try:
            self.embeddings_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.embeddings_path, 'w', encoding='utf-8') as f:
                json.dump(self._embeddings_cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[Embedding] 임베딩 저장 실패: {e}")
    
    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """Fireworks API로 임베딩 생성"""
        if not self.api_key:
            print("[Embedding] API 키 없음, 임베딩 생성 불가")
            return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": f"accounts/fireworks/models/{self.EMBEDDING_MODEL}",
                "input": text[:2000]  # 최대 2000자로 제한
            }
            
            response = requests.post(
                self.API_ENDPOINT,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if "data" in result and len(result["data"]) > 0:
                    embedding = result["data"][0].get("embedding")
                    return embedding
            else:
                print(f"[Embedding] API 오류: {response.status_code} - {response.text[:200]}")
                
        except Exception as e:
            print(f"[Embedding] 임베딩 생성 실패: {e}")
        
        return None
    
    def get_embedding(self, uri: str, text: Optional[str] = None) -> Optional[List[float]]:
        """임베딩 조회 또는 생성"""
        # 캐시 확인
        if uri in self._embeddings_cache:
            return self._embeddings_cache[uri]
        
        # 새로 생성
        if text:
            embedding = self.generate_embedding(text)
            if embedding:
                with self._lock:
                    self._embeddings_cache[uri] = embedding
                    self._save_embeddings()
                return embedding
        
        return None
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """코사인 유사도 계산"""
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def find_similar(self, text: str, threshold: float = SIMILARITY_THRESHOLD) -> List[Tuple[str, float]]:
        """유사한 메모리 찾기"""
        query_embedding = self.generate_embedding(text)
        if not query_embedding:
            return []
        
        similar_items = []
        with self._lock:
            for uri, embedding in self._embeddings_cache.items():
                similarity = self.cosine_similarity(query_embedding, embedding)
                if similarity >= threshold:
                    similar_items.append((uri, similarity))
        
        # 유사도 높은 순으로 정렬
        similar_items.sort(key=lambda x: x[1], reverse=True)
        return similar_items
    
    def delete_embedding(self, uri: str):
        """임베딩 삭제"""
        with self._lock:
            if uri in self._embeddings_cache:
                del self._embeddings_cache[uri]
                self._save_embeddings()
    
    def update_embedding(self, uri: str, text: str) -> Optional[List[float]]:
        """임베딩 업데이트"""
        embedding = self.generate_embedding(text)
        if embedding:
            with self._lock:
                self._embeddings_cache[uri] = embedding
                self._save_embeddings()
        return embedding


class MultilingualTokenizer:
    """다국어 토크나이저 - 한국어 + 영어 지원"""
    
    def __init__(self):
        # 한국어 분석기
        self.okt = Okt() if KONLPY_AVAILABLE else None
        
        # 영어 분석기
        if NLTK_AVAILABLE:
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                nltk.download('punkt', quiet=True)
                nltk.download('punkt_tab', quiet=True)
                nltk.download('stopwords', quiet=True)
            try:
                self.english_stopwords = set(stopwords.words('english'))
            except:
                self.english_stopwords = set()
        else:
            self.english_stopwords = set()
    
    def detect_language(self, text: str) -> str:
        """언어 감지 (한국어/영어)"""
        korean_chars = len(re.findall(r'[가-힣]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        
        if korean_chars > english_chars:
            return "ko"
        elif english_chars > 0:
            return "en"
        else:
            return "ko"  # 기본값
    
    def tokenize_korean(self, text: str) -> List[str]:
        """한국어 토큰화"""
        if self.okt:
            tokens = self.okt.morphs(text, stem=True)
            filtered = [t for t in tokens if len(t) > 1]
            return filtered
        else:
            return text.split()
    
    def tokenize_english(self, text: str) -> List[str]:
        """영어 토큰화"""
        if NLTK_AVAILABLE:
            tokens = word_tokenize(text.lower())
            # 불용어 제거 + 2글자 이상
            filtered = [t for t in tokens if t.isalpha() and len(t) > 1 and t not in self.english_stopwords]
            return filtered
        else:
            # 기본 토큰화
            tokens = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
            return tokens
    
    def tokenize(self, text: str, language: str = "auto") -> List[str]:
        """다국어 토큰화"""
        if language == "auto":
            language = self.detect_language(text)
        
        if language == "ko":
            return self.tokenize_korean(text)
        else:
            return self.tokenize_english(text)
    
    def extract_keywords(self, text: str, top_n: int = 5, language: str = "auto") -> List[str]:
        """핵심 키워드 추출"""
        if language == "auto":
            language = self.detect_language(text)
        
        tokens = self.tokenize(text, language)
        
        # 빈도 기반 키워드 추출
        freq = {}
        for token in tokens:
            freq[token] = freq.get(token, 0) + 1
        
        sorted_tokens = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [t[0] for t in sorted_tokens[:top_n]]


# 한국어 전용 토크나이저 (하위 호환)
class KoreanTokenizer(MultilingualTokenizer):
    """한국어 토크나이저 (하위 호환용)"""
    pass


class SimilarityChecker:
    """자카드 유사도 기반 중복 제거"""
    
    def __init__(self, threshold: float = 0.8):
        """
        Args:
            threshold: 유사도 임계값 (0.8 = 80% 이상이면 중복으로 간주)
        """
        self.threshold = threshold
    
    def jaccard_similarity(self, text_a: str, text_b: str, tokenizer: MultilingualTokenizer) -> float:
        """자카드 유사도 계산"""
        tokens_a = set(tokenizer.tokenize(text_a))
        tokens_b = set(tokenizer.tokenize(text_b))
        
        if not tokens_a or not tokens_b:
            return 0.0
        
        intersection = tokens_a & tokens_b
        union = tokens_a | tokens_b
        
        return len(intersection) / len(union)
    
    def is_duplicate(self, new_text: str, existing_text: str, tokenizer: MultilingualTokenizer) -> bool:
        """중복 여부 확인"""
        similarity = self.jaccard_similarity(new_text, existing_text, tokenizer)
        return similarity >= self.threshold


class CategorySuggester:
    """자동 카테고리 추천"""
    
    # 카테고리 키워드 맵
    CATEGORY_MAP = {
        "biz": ["매출", "ROAS", "광고", "마케팅", "CS", "주문", "매출", "객단가", "전환율", "ROAS", "CPA", "CTR"],
        "health": ["영양제", "운동", "수면", "피로", "복싱", "웨이트", "마그네슘", "단식", "IF"],
        "gov": ["특허", "지원사업", "정부", "신청", "지원금", "과제"],
        "personal": ["여자친구", "설현", "찬혁", "밤토리", "장꾸", "영현"],
        "drlady": ["이너앰플", "클렌저", "PDRN", "글루타티온", "유산균", "닥터레이디"],
        "dev": ["API", "코드", "Python", "클래스", "함수", "버그", "에러"]
    }
    
    def suggest(self, text: str, tokenizer: MultilingualTokenizer) -> str:
        """텍스트 기반 카테고리 추천"""
        tokens = set(tokenizer.tokenize(text))
        
        scores = {}
        for category, keywords in self.CATEGORY_MAP.items():
            matches = tokens & set(keywords)
            scores[category] = len(matches)
        
        best_category = max(scores, key=scores.get)
        best_score = scores[best_category]
        
        # 매칭이 없으면 기본값
        return best_category if best_score > 0 else "memories"


class WALManager:
    """Write-Ahead Log 프로토콜 - 응답 전에 먼저 저장"""
    
    def __init__(self, wal_path: str = "./wal.json"):
        self.wal_path = Path(wal_path)
        self._lock = threading.Lock()
    
    def begin_transaction(self, operation: str, data: Dict[str, Any]) -> str:
        """트랜잭션 시작 - 작업 로깅"""
        transaction_id = f"tx_{int(time.time() * 1000)}"
        
        wal_entry = {
            "id": transaction_id,
            "operation": operation,
            "data": data,
            "status": "pending",
            "timestamp": datetime.now().isoformat()
        }
        
        with self._lock:
            self._append_wal(wal_entry)
        
        return transaction_id
    
    def commit(self, transaction_id: str):
        """트랜잭션 커밋"""
        with self._lock:
            entries = self._read_wal()
            for entry in entries:
                if entry["id"] == transaction_id:
                    entry["status"] = "committed"
            self._write_wal(entries)
    
    def rollback(self, transaction_id: str):
        """트랜잭션 롤백"""
        with self._lock:
            entries = self._read_wal()
            for entry in entries:
                if entry["id"] == transaction_id:
                    entry["status"] = "rolledback"
            self._write_wal(entries)
    
    def get_pending(self) -> List[Dict[str, Any]]:
        """대기 중인 트랜잭션 조회"""
        entries = self._read_wal()
        return [e for e in entries if e["status"] == "pending"]
    
    def _append_wal(self, entry: Dict[str, Any]):
        """WAL에 항목 추가"""
        entries = self._read_wal()
        entries.append(entry)
        self._write_wal(entries)
    
    def _read_wal(self) -> List[Dict[str, Any]]:
        """WAL 읽기"""
        if self.wal_path.exists():
            try:
                with open(self.wal_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _write_wal(self, entries: List[Dict[str, Any]]):
        """WAL 쓰기"""
        self.wal_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.wal_path, 'w', encoding='utf-8') as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)


class SessionStateManager:
    """SESSION-STATE.md 관리 - 세션 간 맥락 유지"""
    
    TEMPLATE = """# SESSION-STATE.md — Active Working Memory

This file is the agent's "RAM" — survives compaction, restarts, distractions.

## Current Task
{current_task}

## Key Context
{key_context}

## Pending Actions
{pending_actions}

## Recent Decisions
{recent_decisions}

---
*Last updated: {timestamp}*
"""
    
    def __init__(self, workspace_path: str = None):
        if workspace_path is None:
            workspace_path = str(Path(__file__).parent.parent)  # token-saver 루트 디렉토리
        self.workspace_path = Path(workspace_path).resolve()
        self.session_file = self.workspace_path / "SESSION-STATE.md"
        
        if not self.session_file.exists():
            self._init_session()
    
    def _init_session(self):
        """세션 파일 초기화"""
        self.session_file.parent.mkdir(parents=True, exist_ok=True)
        self.save_session(
            current_task="[None]",
            key_context="[None yet]",
            pending_actions="- [ ] None",
            recent_decisions="[None yet]"
        )
    
    def save_session(self, current_task: str = "", key_context: str = "", 
                     pending_actions: str = "", recent_decisions: str = ""):
        """세션 상태 저장 (WAL: 응답 전에 호출!)"""
        content = self.TEMPLATE.format(
            current_task=current_task or "[None]",
            key_context=key_context or "[None yet]",
            pending_actions=pending_actions or "- [ ] None",
            recent_decisions=recent_decisions or "[None yet]",
            timestamp=datetime.now().isoformat()
        )
        
        with open(self.session_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def load_session(self) -> Dict[str, str]:
        """세션 상태 로드"""
        if not self.session_file.exists():
            return {
                "current_task": "[None]",
                "key_context": "[None yet]",
                "pending_actions": "- [ ] None",
                "recent_decisions": "[None yet]"
            }
        
        with open(self.session_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 파싱
        result = {}
        sections = ["Current Task", "Key Context", "Pending Actions", "Recent Decisions"]
        
        for i, section in enumerate(sections):
            pattern = rf"## {section}\s*\n(.*?)(?=\n##|\n---)"
            match = re.search(pattern, content, re.DOTALL)
            if match:
                result[section.lower().replace(" ", "_")] = match.group(1).strip()
            else:
                result[section.lower().replace(" ", "_")] = ""
        
        return result
    
    def update_task(self, task: str):
        """현재 작업 업데이트"""
        session = self.load_session()
        session["current_task"] = task
        self.save_session(**session)
    
    def add_context(self, context: str):
        """키 컨텍스트 추가"""
        session = self.load_session()
        existing = session.get("key_context", "")
        if existing == "[None yet]":
            existing = ""
        session["key_context"] = f"{existing}\n- {context}".strip()
        self.save_session(**session)
    
    def add_decision(self, decision: str):
        """결정 추가"""
        session = self.load_session()
        existing = session.get("recent_decisions", "")
        if existing == "[None yet]":
            existing = ""
        timestamp = datetime.now().strftime("%H:%M")
        session["recent_decisions"] = f"{existing}\n- [{timestamp}] {decision}".strip()
        self.save_session(**session)


class EntityExtractor:
    """엔티티 추출 - 사람/브랜드/제품 자동 인식"""
    
    # 사전 정의 엔티티
    KNOWN_ENTITIES = {
        "person": ["명진", "설현", "영현", "찬혁", "마스터", "보라"],
        "brand": ["Dr.Lady", "닥터레이디", "메디큐브", "비오템"],
        "product": ["이너앰플", "이너 클렌저", "클렌저", "앰플", "PDRN"],
        "pet": ["밤토리", "장꾸"],
        "org": ["바른연구소", "식약처", "ClawHub"]
    }
    
    # 패턴 기반 추출
    PATTERNS = {
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "phone": r'\b\d{2,3}[-.\s]?\d{3,4}[-.\s]?\d{4}\b',
        "url": r'https?://[^\s<>"{}|\\^`\[\]]+',
        "date": r'\b\d{4}[-./]\d{1,2}[-./]\d{1,2}\b|\b\d{1,2}[-./]\d{1,2}[-./]\d{4}\b',
        "money_krw": r'\b\d{1,3}(,\d{3})*원\b|\b\d+만원\b|\b\d+억원\b',
        "percent": r'\b\d+(\.\d+)?%\b',
        "hashtag": r'#[\w가-힣]+'
    }
    
    def extract(self, text: str, tokenizer: Optional[MultilingualTokenizer] = None) -> Dict[str, List[str]]:
        """텍스트에서 엔티티 추출"""
        entities = {category: [] for category in self.KNOWN_ENTITIES}
        entities["pattern"] = {}
        
        # 사전 정의 엔티티 매칭
        text_lower = text.lower()
        for category, names in self.KNOWN_ENTITIES.items():
            for name in names:
                if name.lower() in text_lower or name in text:
                    entities[category].append(name)
        
        # 패턴 기반 추출
        for pattern_name, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                entities["pattern"][pattern_name] = list(set(matches))
        
        # NER 기반 추가 추출 (tokenizer 있을 때)
        if tokenizer and KONLPY_AVAILABLE:
            nouns = tokenizer.okt.nouns(text) if tokenizer.okt else []
            # 사람 이름 패턴 (2-3글자 한글)
            potential_names = [n for n in nouns if 2 <= len(n) <= 3 and re.match(r'^[가-힣]+$', n)]
            # 이미 알려진 것 제외
            known_flat = [n.lower() for names in self.KNOWN_ENTITIES.values() for n in names]
            new_names = [n for n in potential_names if n.lower() not in known_flat]
            if new_names:
                entities["potential_person"] = list(set(new_names))[:5]  # 최대 5개
        
        # 빈 리스트 제거
        entities = {k: v for k, v in entities.items() if v}
        
        return entities
    
    def get_persons(self, text: str) -> List[str]:
        """사람만 추출"""
        entities = self.extract(text)
        return entities.get("person", []) + entities.get("potential_person", [])
    
    def get_products(self, text: str) -> List[str]:
        """제품만 추출"""
        entities = self.extract(text)
        return entities.get("product", [])
    
    def get_brands(self, text: str) -> List[str]:
        """브랜드만 추출"""
        entities = self.extract(text)
        return entities.get("brand", [])


class VersionBackup:
    """버전 백업 관리자"""
    
    def __init__(self, backup_dir: str = "./backup_memories"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def backup(self, file_path: Path, uri: str) -> Optional[Path]:
        """파일 백업"""
        if not file_path.exists():
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        safe_uri = uri.replace("/", "_").replace("\\", "_")
        backup_path = self.backup_dir / f"{timestamp}_{safe_uri}.json"
        
        shutil.copy(file_path, backup_path)
        print(f"(System) 백업 완료: {backup_path}")
        
        return backup_path
    
    def list_backups(self, uri: Optional[str] = None) -> List[Path]:
        """백업 목록 조회"""
        if uri:
            safe_uri = uri.replace("/", "_").replace("\\", "_")
            return list(self.backup_dir.glob(f"*_{safe_uri}.json"))
        return list(self.backup_dir.glob("*.json"))


class CacheManager:
    """캐시 관리자 - TTL 기반 캐싱"""
    
    def __init__(self, ttl: int = 300):
        """
        Args:
            ttl: 캐시 유효시간 (초), 기본 5분
        """
        self._cache: Dict[str, tuple] = {}  # (data, timestamp)
        self._ttl = ttl
    
    def get(self, key: str) -> Optional[Any]:
        """캐시 조회"""
        if key in self._cache:
            data, timestamp = self._cache[key]
            if time.time() - timestamp < self._ttl:
                return data
            else:
                # 만료된 캐시 삭제
                del self._cache[key]
        return None
    
    def set(self, key: str, data: Any):
        """캐시 저장"""
        self._cache[key] = (data, time.time())
    
    def delete(self, key: str):
        """캐시 삭제"""
        self._cache.pop(key, None)
    
    def clear(self):
        """전체 캐시 삭제"""
        self._cache.clear()
    
    def size(self) -> int:
        """캐시 크기"""
        return len(self._cache)


class ContextStore:
    """Context 저장소 - 파일시스템 기반 + 캐싱 + 가중치 검색 + 임베딩"""
    
    # 메모리 계층 설정
    HOT_DAYS = 7
    WARM_DAYS = 30
    ARCHIVE_DAYS = 30  # 30일 이상 접근 없으면 아카이브
    
    def __init__(self, base_path: str = "~/.token-saver/korean", cache_ttl: int = 300, 
                 embeddings_path: Optional[str] = None):
        self.base_path = Path(base_path).expanduser()
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # 캐시 매니저
        self._cache = CacheManager(ttl=cache_ttl)
        
        # 임베딩 매니저
        if embeddings_path is None:
            embeddings_path = str(self.base_path / "embeddings.json")
        self.embeddings = EmbeddingManager(embeddings_path=Path(embeddings_path))
        
        # 중복 제거
        self.similarity_checker = SimilarityChecker()
        
        # 버전 백업
        self.version_backup = VersionBackup(str(self.base_path / "backups"))
        
        # 카테고리 디렉토리 생성
        for category in ["memories", "resources", "skills", "biz", "health", "gov", 
                        "personal", "drlady", "dev", "archive"]:
            (self.base_path / category).mkdir(exist_ok=True)
    
    def save(self, context: Context, tokenizer: Optional[MultilingualTokenizer] = None, 
             check_duplicate: bool = True, merge_if_similar: bool = True) -> Tuple[bool, str]:
        """
        Context 저장 (중복 제거 + 버전 백업 + 캐시 무효화 + 임베딩 + 중복 병합)
        
        Returns:
            (성공여부, 메시지)
        """
        try:
            # 토크나이저
            if tokenizer is None:
                tokenizer = MultilingualTokenizer()
            
            # 1. 임베딩 기반 중복 체크 (신규)
            if merge_if_similar:
                similar_items = self.embeddings.find_similar(context.content, threshold=0.85)
                if similar_items:
                    # 가장 유사한 항목에 병합
                    most_similar_uri, similarity = similar_items[0]
                    return self._merge_context(most_similar_uri, context, tokenizer)
            
            # 2. URI에서 파일 경로 생성
            path = self._uri_to_path(context.uri)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # 3. 기존 파일 중복 체크 (자카드 유사도)
            if check_duplicate and path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                
                existing_text = existing_data.get("content", "")
                if self.similarity_checker.is_duplicate(context.content, existing_text, tokenizer):
                    # 80% 이상 유사 → 덮어쓰기 (버전 증가)
                    print(f"(System) 유사한 내용 감지, 버전 업그레이드: v{existing_data.get('version', 1)} → v{existing_data.get('version', 1) + 1}")
                    context.version = existing_data.get('version', 1) + 1
                    context.access_count = existing_data.get('access_count', 0)
                    context.created_at = datetime.fromisoformat(existing_data.get('created_at', datetime.now().isoformat()))
                    
                    # 백업
                    self.version_backup.backup(path, context.uri)
            
            # 4. 임베딩 생성 및 저장
            embedding = self.embeddings.get_embedding(context.uri, context.content)
            if embedding:
                context.meta['has_embedding'] = True
            
            # 5. JSON으로 저장
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(context.to_dict(), f, ensure_ascii=False, indent=2)
            
            # 6. 캐시 무효화
            self._cache.delete(f"load:{context.uri}")
            self._cache.delete(f"search:{context.category}")
            
            return True, f"저장 완료: {context.uri}"
            
        except PermissionError as e:
            raise IOError(f"파일 쓰기 권한 없음: {path}")
        except json.JSONEncodeError as e:
            raise ValueError(f"JSON 인코딩 실패: {e}")
        except Exception as e:
            raise IOError(f"저장 실패: {e}")
    
    def _merge_context(self, existing_uri: str, new_context: Context, tokenizer: MultilingualTokenizer) -> Tuple[bool, str]:
        """기존 컨텍스트에 새 내용 병합"""
        try:
            existing = self.load(existing_uri, level=2, use_cache=False)
            if not existing:
                return False, "기존 컨텍스트를 찾을 수 없음"
            
            # 내용 병합 (중복 제거)
            existing_text = existing.content
            new_text = new_context.content
            
            # 간단한 병합: 기존 내용 + 새 내용 (구분선 추가)
            if new_text not in existing_text:
                merged_content = f"{existing_text}\n\n---\n\n[추가됨 {datetime.now().strftime('%Y-%m-%d %H:%M')}]\n{new_text}"
                existing.content = merged_content
                existing.version += 1
                existing.updated_at = datetime.now()
                
                # 저장
                path = self._uri_to_path(existing_uri)
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(existing.to_dict(), f, ensure_ascii=False, indent=2)
                
                # 임베딩 업데이트
                self.embeddings.update_embedding(existing_uri, merged_content)
                
                # 캐시 무효화
                self._cache.delete(f"load:{existing_uri}")
                
                return True, f"병합 완료: {existing_uri} (v{existing.version})"
            else:
                return True, f"이미 동일한 내용 존재: {existing_uri}"
                
        except Exception as e:
            return False, f"병합 실패: {e}"
    
    def load(self, uri: str, level: int = 2, use_cache: bool = True, update_access: bool = True) -> Optional[Context]:
        """Context 로드 (계층적 + 캐싱 + 접근 시간 업데이트)"""
        cache_key = f"load:{uri}:{level}"
        
        # 캐시 확인
        if use_cache:
            cached = self._cache.get(cache_key)
            if cached:
                if update_access:
                    self._update_access_time(uri)
                return cached
        
        path = self._uri_to_path(uri)
        
        if not path.exists():
            return None
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Context 객체 생성
            context = Context.from_dict(data)
            
            # 레벨에 따른 내용 로드
            if level == 0:
                context.content = context.abstract
            elif level == 1:
                context.content = self._get_overview(context)
            
            # 티어에 따른 콘텐츠 조정
            context = self._apply_tier_constraints(context)
            
            # 접근 시간 업데이트
            if update_access:
                self._update_access_time(uri)
            
            # 캐시 저장
            if use_cache:
                self._cache.set(cache_key, context)
            
            return context
            
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 파싱 실패: {path}")
        except Exception as e:
            raise IOError(f"로드 실패: {e}")
        
        return None
    
    def _update_access_time(self, uri: str):
        """접근 시간 및 카운트 업데이트"""
        try:
            path = self._uri_to_path(uri)
            if not path.exists():
                return
            
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            data['last_accessed_at'] = datetime.now().isoformat()
            data['access_count'] = data.get('access_count', 0) + 1
            
            # 티어 자동 업데이트
            last_accessed = datetime.fromisoformat(data['last_accessed_at'])
            days_since_access = (datetime.now() - last_accessed).days
            
            if days_since_access <= self.HOT_DAYS:
                data['tier'] = 'hot'
            elif days_since_access <= self.WARM_DAYS:
                data['tier'] = 'warm'
            else:
                data['tier'] = 'cold'
            
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"[Access Update] 실패: {e}")
    
    def _apply_tier_constraints(self, context: Context) -> Context:
        """티어에 따른 콘텐츠 제약 적용"""
        if context.tier == 'cold':
            # Cold: abstract만, 압축
            context.content = context.abstract
            context.meta['compressed'] = True
        elif context.tier == 'warm':
            # Warm: abstract + 일부 content
            if len(context.content) > 1000:
                context.content = context.content[:1000] + "... [Warm Tier: 일부만 표시]"
        # Hot: full content 유지
        return context
    
    def search(self, query: str, category: Optional[str] = None, use_cache: bool = True, 
               tokenizer: Optional[MultilingualTokenizer] = None, 
               include_archive: bool = False, use_embedding: bool = True) -> List[tuple]:
        """
        다국어 검색 + 캐싱 + 가중치 스코어링 + 임베딩 유사도 검색
        
        Returns:
            List of (Context, score) tuples sorted by score descending
        """
        cache_key = f"search:{query}:{category}:{include_archive}"
        
        # 캐시 확인
        if use_cache:
            cached = self._cache.get(cache_key)
            if cached:
                return cached
        
        results = []
        search_paths = []
        
        if category:
            search_paths = [self.base_path / category]
        else:
            # 모든 카테고리 검색 (archive 제외 옵션)
            for subdir in self.base_path.iterdir():
                if subdir.is_dir():
                    if not include_archive and subdir.name == "archive":
                        continue
                    search_paths.append(subdir)
        
        # 토크나이저
        if tokenizer is None:
            tokenizer = MultilingualTokenizer()
        
        # 검색어 토큰화
        query_tokens = set(tokenizer.tokenize(query))
        
        # 임베딩 기반 검색 (신규)
        embedding_results = {}
        if use_embedding and self.embeddings.api_key:
            query_embedding = self.embeddings.generate_embedding(query)
            if query_embedding:
                for uri, emb in self.embeddings._embeddings_cache.items():
                    similarity = self.embeddings.cosine_similarity(query_embedding, emb)
                    if similarity > 0.6:  # 임베딩 유사도 임계값
                        embedding_results[uri] = similarity
        
        # 파일 검색
        for search_path in search_paths:
            if not search_path.exists():
                continue
                
            for file in search_path.rglob("*.json"):
                # embeddings.json 제외
                if file.name == "embeddings.json":
                    continue
                    
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    uri = data.get('uri', '')
                    
                    # 가중치 점수 계산 (키워드 매칭)
                    keyword_score = self._calculate_search_score(query_tokens, data, tokenizer)
                    
                    # 임베딩 유사도 점수
                    embedding_score = embedding_results.get(uri, 0) * 10  # 가중치
                    
                    # 총점
                    total_score = keyword_score + embedding_score
                    
                    if total_score > 0 or uri in embedding_results:
                        context = Context.from_dict(data)
                        results.append((context, total_score))
                        
                except json.JSONDecodeError:
                    continue
                except Exception:
                    continue
        
        # 점수 순 정렬
        results.sort(key=lambda x: x[1], reverse=True)
        
        # 캐시 저장
        if use_cache:
            self._cache.set(cache_key, results)
        
        return results
    
    def _calculate_search_score(self, query_tokens: set, data: Dict, tokenizer: MultilingualTokenizer) -> float:
        """가중치 검색 점수 계산
        
        점수 = (제목 매칭 × 3) + (키워드 매칭 × 2) + (본문 매칭 × 1)
        """
        score = 0.0
        
        # 제목 (URI) 매칭 × 3
        uri = data.get("uri", "")
        uri_tokens = set(tokenizer.tokenize(uri))
        title_match = len(query_tokens & uri_tokens)
        score += title_match * 3
        
        # abstract 매칭 × 2
        abstract = data.get("abstract", "")
        abstract_tokens = set(tokenizer.tokenize(abstract))
        abstract_match = len(query_tokens & abstract_tokens)
        score += abstract_match * 2
        
        # 본문 매칭 × 1
        content = data.get("content", "")
        content_tokens = set(tokenizer.tokenize(content))
        content_match = len(query_tokens & content_tokens)
        score += content_match * 1
        
        return score
    
    def cleanup_expired(self, days: int = 30, dry_run: bool = False) -> List[str]:
        """
        30일 이상 접근 안 한 메모리를 archive로 이동
        
        Returns:
            이동된 URI 목록
        """
        moved = []
        archive_dir = self.base_path / "archive"
        archive_dir.mkdir(exist_ok=True)
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for category_dir in self.base_path.iterdir():
            if not category_dir.is_dir() or category_dir.name == "archive":
                continue
            
            for file in category_dir.rglob("*.json"):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    last_accessed = data.get('last_accessed_at')
                    if last_accessed:
                        last_accessed_dt = datetime.fromisoformat(last_accessed)
                        if last_accessed_dt < cutoff_date:
                            uri = data.get('uri', '')
                            
                            if not dry_run:
                                # archive로 이동
                                new_path = archive_dir / f"{category_dir.name}_{file.name}"
                                shutil.move(str(file), str(new_path))
                                
                                # 카테고리 업데이트
                                data['category'] = 'archive'
                                data['tier'] = 'cold'
                                with open(new_path, 'w', encoding='utf-8') as f:
                                    json.dump(data, f, ensure_ascii=False, indent=2)
                            
                            moved.append(uri)
                            
                except Exception as e:
                    print(f"[Cleanup] 오류: {e}")
                    continue
        
        if not dry_run:
            print(f"[Cleanup] {len(moved)}개 항목 archive로 이동")
        
        return moved
    
    def get_tier_stats(self) -> Dict[str, int]:
        """티어별 통계"""
        stats = {'hot': 0, 'warm': 0, 'cold': 0, 'archive': 0}
        
        for category_dir in self.base_path.iterdir():
            if not category_dir.is_dir():
                continue
            
            for file in category_dir.rglob("*.json"):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    tier = data.get('tier', 'hot')
                    if category_dir.name == 'archive':
                        stats['archive'] += 1
                    else:
                        stats[tier] = stats.get(tier, 0) + 1
                except:
                    continue
        
        return stats
    
    def clear_cache(self):
        """캐시 전체 삭제"""
        self._cache.clear()
    
    def cache_size(self) -> int:
        """캐시 크기"""
        return self._cache.size()
    
    def _uri_to_path(self, uri: str) -> Path:
        """URI를 파일 경로로 변환"""
        # viking://memories/프로젝트/마케팅.md -> memories/프로젝트/마케팅.json
        if uri.startswith("viking://"):
            uri = uri[9:]  # viking:// 제거
        return self.base_path / f"{uri}.json"
    
    def _get_overview(self, context: Context) -> str:
        """개요 생성 (L1)"""
        # 간단한 개요 생성 로직
        lines = context.content.split('\n')
        overview_lines = lines[:10]  # 첫 10줄
        return '\n'.join(overview_lines)


class TokenSaverKorean:
    """TokenSaver Korean 메인 클래스 + 다국어 지원 + 캐싱 + 에러 처리 + 자동 요약 + 자동 카테고리 + WAL + SESSION-STATE + 엔티티 추출 + 임베딩"""
    
    def __init__(self, config_path: str = "~/.token-saver/ovk.conf", cache_ttl: int = 300, 
                 summarizer: Optional[Callable] = None, workspace_path: str = None):
        self.config_path = Path(config_path).expanduser()
        self.config = self._load_config()
        
        if workspace_path is None:
            workspace_path = str(Path(__file__).parent.parent)  # token-saver 루트
        
        self.workspace_path = Path(workspace_path)
        self.store = ContextStore(
            cache_ttl=cache_ttl,
            embeddings_path=self.workspace_path / "embeddings.json"
        )
        self.tokenizer = MultilingualTokenizer()  # 다국어 토크나이저
        
        # 자동 요약 함수 (외부 주입)
        self.summarizer = summarizer
        
        # 자동 카테고리 추천
        self.category_suggester = CategorySuggester()
        
        # WAL 프로토콜
        self.wal = WALManager(wal_path=str(self.workspace_path / "wal.json"))
        
        # 세션 상태 관리
        self.session_state = SessionStateManager(workspace_path=workspace_path)
        
        # 엔티티 추출
        self.entity_extractor = EntityExtractor()
    
    def _load_config(self) -> Dict[str, Any]:
        """설정 로드 (에러 처리 강화)"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except json.JSONDecodeError:
            pass  # 기본 설정 사용
        except Exception:
            pass  # 기본 설정 사용
        
        return {
            "language": "auto",  # auto, ko, en
            "token_optimization": {
                "enabled": True,
                "target_reduction": 0.91
            }
        }
    
    def save_memory(self, uri: str, content: str, category: str = "auto", 
                    language: str = "auto", check_duplicate: bool = True) -> bool:
        """기억 저장 (에러 처리 + 언어 자동 감지 + 자동 요약 + 자동 카테고리 + 중복 체크 + 병합)"""
        try:
            # 언어 자동 감지
            if language == "auto":
                language = self.tokenizer.detect_language(content)
            
            # 자동 카테고리 추천
            if category == "auto":
                category = self.category_suggester.suggest(content, self.tokenizer)
            
            # 자동 요약 (300자 이상 + summarizer 있을 때)
            processed_content = self._auto_summarize(content)
            
            # 다국어 요약 생성
            abstract = self._generate_abstract(processed_content, language=language)
            
            context = Context(
                uri=f"{category}/{uri}",
                abstract=abstract,
                content=processed_content,
                category=category,
                language=language
            )
            
            success, message = self.store.save(context, tokenizer=self.tokenizer, check_duplicate=check_duplicate)
            print(f"(System) {message}")
            return success
            
        except Exception as e:
            raise IOError(f"메모리 저장 실패: {e}")
    
    def _auto_summarize(self, text: str) -> str:
        """자동 요약 (300자 이상일 때만 작동)"""
        if len(text) > 300 and self.summarizer:
            print(f"(System) 긴 텍스트 감지: {len(text)}자 → 지능형 요약 가동...")
            return self.summarizer(text)
        return text
    
    def find(self, query: str, category: Optional[str] = None, level: int = 2, 
             use_cache: bool = True, limit: int = 10, include_archive: bool = False,
             use_embedding: bool = True) -> List[Dict[str, Any]]:
        """
        Context 검색 (캐싱 적용 + 가중치 스코어링 + 임베딩 유사도)
        """
        results = self.store.search(
            query, category, use_cache=use_cache, tokenizer=self.tokenizer,
            include_archive=include_archive, use_embedding=use_embedding
        )
        
        # 토큰 절감을 위해 레벨에 따른 내용 반환
        return [
            {
                "uri": r.uri,
                "abstract": r.abstract,
                "content": r.content if level == 2 else r.abstract,
                "category": r.category,
                "score": score,
                "version": r.version,
                "tier": r.tier,
                "access_count": r.access_count
            }
            for r, score in results[:limit]
        ]
    
    def clear_cache(self):
        """전체 캐시 삭제"""
        self.store.clear_cache()
    
    def cache_size(self) -> int:
        """캐시 크기"""
        return self.store.cache_size()
    
    def list_backups(self, uri: Optional[str] = None) -> List[str]:
        """백업 목록 조회"""
        backups = self.store.version_backup.list_backups(uri)
        return [str(b) for b in backups]
    
    def suggest_category(self, text: str) -> str:
        """카테고리 추천 (미리보기)"""
        return self.category_suggester.suggest(text, self.tokenizer)
    
    # ============ WAL + SESSION-STATE 메서드 ============
    
    def save_memory_wal(self, uri: str, content: str, category: str = "auto", 
                         language: str = "auto", check_duplicate: bool = True) -> bool:
        """WAL 프로토콜로 저장 - 응답 전에 호출!"""
        # 1. 트랜잭션 시작
        tx_id = self.wal.begin_transaction("save_memory", {
            "uri": uri,
            "category": category,
            "content_length": len(content)
        })
        
        try:
            # 2. 실제 저장 실행
            result = self.save_memory(uri, content, category, language, check_duplicate)
            
            # 3. 커밋
            self.wal.commit(tx_id)
            
            return result
        except Exception as e:
            # 4. 실패 시 롤백
            self.wal.rollback(tx_id)
            raise e
    
    def update_session_task(self, task: str):
        """세션 작업 업데이트 (WAL: 응답 전에 호출!)"""
        self.session_state.update_task(task)
    
    def add_session_context(self, context: str):
        """세션 컨텍스트 추가"""
        self.session_state.add_context(context)
    
    def add_session_decision(self, decision: str):
        """세션 결정 추가"""
        self.session_state.add_decision(decision)
    
    def load_session(self) -> Dict[str, str]:
        """세션 상태 로드"""
        return self.session_state.load_session()
    
    # ============ 엔티티 추출 메서드 ============
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """엔티티 추출"""
        return self.entity_extractor.extract(text, self.tokenizer)
    
    def extract_persons(self, text: str) -> List[str]:
        """사람 추출"""
        return self.entity_extractor.get_persons(text)
    
    def extract_products(self, text: str) -> List[str]:
        """제품 추출"""
        return self.entity_extractor.get_products(text)
    
    def extract_brands(self, text: str) -> List[str]:
        """브랜드 추출"""
        return self.entity_extractor.get_brands(text)
    
    # ============ 메모리 계층화 및 아카이브 메서드 ============
    
    def cleanup_expired(self, days: int = 30, dry_run: bool = False) -> List[str]:
        """만료된 메모리 정리"""
        return self.store.cleanup_expired(days, dry_run)
    
    def get_tier_stats(self) -> Dict[str, int]:
        """티어별 통계 조회"""
        return self.store.get_tier_stats()
    
    def get_embedding_stats(self) -> Dict[str, Any]:
        """임베딩 통계 조회"""
        return {
            "total_embeddings": len(self.store.embeddings._embeddings_cache),
            "api_key_set": bool(self.store.embeddings.api_key),
            "embeddings_path": str(self.store.embeddings.embeddings_path) if self.store.embeddings.embeddings_path else None
        }
    
    # ============ 기존 메서드 (하위 호환) ============
    
    def abstract(self, uri: str) -> str:
        """L0 요약 반환"""
        context = self.store.load(uri, level=0)
        return context.abstract if context else ""
    
    def overview(self, uri: str) -> str:
        """L1 개요 반환"""
        context = self.store.load(uri, level=1)
        return context.content if context else ""
    
    def read(self, uri: str) -> str:
        """L2 전체 내용 반환"""
        context = self.store.load(uri, level=2)
        return context.content if context else ""
    
    def compress_memory(self, content: str, language: str = "auto") -> str:
        """기억 압축 - 토큰 절감 (다국어)"""
        if language == "auto":
            language = self.tokenizer.detect_language(content)
        
        # 간단한 구현: 첫 500자
        compressed = content[:500]
        
        # 토큰 절감률 계산
        original_tokens = len(content.split())
        compressed_tokens = len(compressed.split())
        reduction = 1 - (compressed_tokens / original_tokens) if original_tokens > 0 else 0
        
        print(f"토큰 절감: {reduction:.1%}")
        
        return compressed
    
    def _generate_abstract(self, content: str, language: str = "auto") -> str:
        """다국어 요약 생성"""
        if language == "auto":
            language = self.tokenizer.detect_language(content)
        
        # 키워드 기반 간단한 요약
        keywords = self.tokenizer.extract_keywords(content, top_n=5, language=language)
        abstract = f"[{'/'.join(keywords)}] {content[:100]}..."
        return abstract
    
    def _calculate_relevance(self, query: str, context: Context) -> float:
        """관련도 계산 (다국어)"""
        query_keywords = set(self.tokenizer.extract_keywords(query))
        content_keywords = set(self.tokenizer.extract_keywords(context.content))
        
        if not query_keywords or not content_keywords:
            return 0.0
        
        intersection = query_keywords & content_keywords
        union = query_keywords | content_keywords
        
        return len(intersection) / len(union)


# CLI 진입점
def main():
    """CLI 메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description="TokenSaver Korean CLI v2.0")
    subparsers = parser.add_subparsers(dest="command")
    
    # find 명령어
    find_parser = subparsers.add_parser("find", help="Context 검색 (임베딩 + 키워드)")
    find_parser.add_argument("query", help="검색 쿼리")
    find_parser.add_argument("--category", "-c", help="카테고리 필터")
    find_parser.add_argument("--level", "-l", type=int, default=2, help="Context 레벨 (0=abstract, 1=overview, 2=detail)")
    find_parser.add_argument("--archive", "-a", action="store_true", help="archive 포함")
    find_parser.add_argument("--no-embedding", action="store_true", help="임베딩 검색 비활성화")
    
    # save 명령어
    save_parser = subparsers.add_parser("save", help="Context 저장 (자동 병합)")
    save_parser.add_argument("uri", help="저장 URI")
    save_parser.add_argument("--content", "-c", required=True, help="내용")
    save_parser.add_argument("--category", "-C", default="auto", help="카테고리 (auto=자동)")
    
    # read 명령어
    read_parser = subparsers.add_parser("read", help="Context 읽기")
    read_parser.add_argument("uri", help="읽을 URI")
    
    # stats 명령어 (신규)
    stats_parser = subparsers.add_parser("stats", help="통계 조회")
    
    # cleanup 명령어 (신규)
    cleanup_parser = subparsers.add_parser("cleanup", help="만료 메모리 정리")
    cleanup_parser.add_argument("--days", "-d", type=int, default=30, help="만료 기준 일수")
    cleanup_parser.add_argument("--dry-run", action="store_true", help="실제 이동 없이 미리보기")
    
    args = parser.parse_args()
    
    client = TokenSaverKorean()
    
    if args.command == "find":
        results = client.find(
            args.query, args.category, args.level,
            include_archive=args.archive,
            use_embedding=not args.no_embedding
        )
        for r in results:
            print(f"[{r['score']:.2f}] {r['uri']} (v{r['version']}, {r['tier']})")
            print(f"  {r['abstract']}")
    
    elif args.command == "save":
        client.save_memory(args.uri, args.content, args.category)
        print(f"저장 완료: {args.uri}")
    
    elif args.command == "read":
        content = client.read(args.uri)
        print(content)
    
    elif args.command == "stats":
        tier_stats = client.get_tier_stats()
        embedding_stats = client.get_embedding_stats()
        print("=== 메모리 계층 통계 ===")
        for tier, count in tier_stats.items():
            print(f"  {tier}: {count}")
        print("\n=== 임베딩 통계 ===")
        print(f"  임베딩 수: {embedding_stats['total_embeddings']}")
        print(f"  API 키 설정: {embedding_stats['api_key_set']}")
    
    elif args.command == "cleanup":
        moved = client.cleanup_expired(args.days, args.dry_run)
        if args.dry_run:
            print(f"[Dry Run] 이동 예정: {len(moved)}개")
        else:
            print(f"이동 완료: {len(moved)}개")
        for uri in moved[:5]:
            print(f"  - {uri}")
        if len(moved) > 5:
            print(f"  ... 외 {len(moved) - 5}개")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
