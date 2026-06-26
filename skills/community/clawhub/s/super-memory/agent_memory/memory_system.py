"""
memory_system.py - Agent Memory System 统一入口
一行初始化，一行调用

v9.0: AgentMemory 拆分为 Mixin 架构
  记忆操作 → MemoryMixin
  检索 → RecallMixin
  会话 → SessionMixin
  维护 → MaintenanceMixin
  蒸馏/百科 → DistillMixin / EncyclopediaMixin
  时间旅行 → TimelineMixin
  统计/人格 → StatsMixin / PersonaMixin
  角色/风格 → RoleMixin / MediaStyleMixin
  反应器 → ReactorMixin
  导出/备份 → ExportMixin
"""

from __future__ import annotations

import os
import logging
import threading
import time

from .cache_manager import get_cache_manager
from .resilience import CircuitBreaker, get_breaker, timeout_call, TimeoutError

from .mixins.memory_mixin import MemoryMixin
from .mixins.recall_mixin import RecallMixin
from .mixins.session_mixin import SessionMixin
from .mixins.maintenance_mixin import MaintenanceMixin
from .mixins.distill_mixin import DistillMixin
from .mixins.encyclopedia_mixin import EncyclopediaMixin
from .mixins.timeline_mixin import TimelineMixin
from .mixins.stats_mixin import StatsMixin
from .mixins.persona_mixin import PersonaMixin
from .mixins.role_mixin import RoleMixin
from .mixins.media_style_mixin import MediaStyleMixin
from .mixins.reactor_mixin import ReactorMixin
from .mixins.export_mixin import ExportMixin

logger = logging.getLogger(__name__)


def _can_import(module_name: str) -> bool:
    """Check if a module can be imported without actually importing it."""
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


def _import_class(module_path: str, class_name: str):
    """Import a class from a relative module path, raising ImportError if unavailable."""
    import importlib
    module = importlib.import_module(module_path, package=__package__)
    return getattr(module, class_name)


class AgentMemory(
    MemoryMixin,
    RecallMixin,
    SessionMixin,
    MaintenanceMixin,
    DistillMixin,
    EncyclopediaMixin,
    TimelineMixin,
    StatsMixin,
    PersonaMixin,
    RoleMixin,
    MediaStyleMixin,
    ReactorMixin,
    ExportMixin,
):
    """
    Agent Memory — Unified memory system for AI agents.

    ARCHITECTURE: This class is a FACADE that routes operations to
    specialized services. The Mixin methods are thin wrappers that
    delegate to the appropriate internal component:

    - remember() → IngestEngine (via MemoryMixin)
    - recall() → RecallEngine (via RecallMixin)
    - maintain() → MaintainEngine (via MaintenanceMixin)
    - spirit → Spirit butler

    For direct access to subsystems:
    - mem.store → MemoryStore (data layer)
    - mem.store.versions → VersionManager
    - mem.store.links → LinkManager
    - mem.store.stats → StatsManager
    - mem.recall_engine → RecallEngine
    - mem.ingest_engine → IngestEngine

    For SDK usage (recommended):
    - from agent_memory import Memory

    用法:
        memory = AgentMemory()  # 零配置，自动使用 ~/.agent_memory/default.db

        memory = AgentMemory(db_path="memory.db")

        # 写入（自动过滤 + 去重 + 编码 + 存储）
        memory.remember("用户偏好用 Chroma 做向量库")

        # 检索（结构化 + 语义混合）
        results = memory.recall("用户的向量库偏好")

        # 组装上下文（直接拼入 Agent prompt）
        prompt = memory.build_context(query="用户的问题")

        # 反馈（优化质量评分）
        memory.feedback(memory_id, useful=True)
    """

    DEFAULT_DB_DIR = os.path.expanduser("~/.agent_memory")

    MAX_CONTENT_LENGTH = 50_000
    MAX_CONTENT_WARN = 10_000

    # Component dependency graph — explicit declaration
    _COMPONENT_DEPENDENCIES = {
        "encoder": [],
        "topic_registry": [],
        "embedding_store": ["encoder"],
        "semantic_matcher": ["embedding_store"],
        "pipeline": ["encoder", "embedding_store", "topic_registry", "semantic_matcher"],
        "filter": [],
        "dedup": [],
        "quality": [],
        "reranker": ["encoder"],
        "media_processor": [],
        "causal": [],
        "compressor": [],
        "decay": [],
        "hierarchy": [],
        "self_healing": [],
        "graph": [],
        "timeline": [],
        "reactor": [],
        "recall_engine": ["store", "encoder", "embedding_store", "quality", "reranker"],
        "archiver": [],
        "distiller": [],
        "pack_manager": [],
        "session_context": [],
        "context_builder": [],
        "cleaner": [],
        "agent_network": [],
    }

    # Severity classification
    _COMPONENT_SEVERITY = {
        "store": "critical",      # System cannot function without store
        "encoder": "major",       # Semantic search disabled
        "embedding_store": "major",
        "semantic_matcher": "major",
        "pipeline": "major",
        "recall_engine": "critical",  # Core recall functionality
        "reranker": "minor",      # Results slightly less optimal
        "filter": "minor",
        "dedup": "minor",
        "quality": "minor",
        "topic_registry": "minor",
        "causal": "minor",
        "compressor": "minor",
        "decay": "minor",
        "hierarchy": "minor",
        "self_healing": "minor",
        "graph": "minor",
        "timeline": "minor",
        "reactor": "minor",
        "archiver": "minor",
        "distiller": "minor",
        "pack_manager": "minor",
        "session_context": "minor",
        "context_builder": "minor",
        "cleaner": "minor",
        "agent_network": "minor",
        "media_processor": "minor",
    }

    def __init__(
        self,
        db_path: str = None,
        project_dir: str = None,
        llm_fn=None,
        vision_fn=None,
        audio_fn=None,
        enable_semantic: bool = True,
        enable_filter: bool = True,
        enable_dedup: bool = True,
        agent_id: str = None,
        team_id: str = "default",
        auto_compress: bool = False,
        compress_policy: dict = None,
        recall_config: dict = None,
        ingest_config: dict = None,
        store_config: dict = None,
        feature_flags=None,
    ):
        if db_path is None:
            os.makedirs(self.DEFAULT_DB_DIR, exist_ok=True)
            db_path = os.path.join(self.DEFAULT_DB_DIR, "default.db")
        if agent_id is None:
            agent_id = "default"

        self.db_path = db_path
        self._project_dir = project_dir or os.path.dirname(__file__)
        self._init_time = time.time()

        # Feature flags integration
        self._feature_flags = feature_flags
        if self._feature_flags is None:
            try:
                from .feature_flags import FeatureFlagManager
                self._feature_flags = FeatureFlagManager()
            except Exception:
                self._feature_flags = None

        # Auto-compression configuration
        self._auto_compress = auto_compress
        self._compress_policy = compress_policy or {
            "age_threshold_days": 30,
            "access_threshold": 2,
            "compression_ratio": 0.3,
            "min_memories_to_compress": 100,
        }

        from .store import MemoryStore
        self.store = self._try_init("store", lambda: MemoryStore(db_path))

        self.cache = get_cache_manager()

        self._check_schema_version()

        self._degraded_lock = threading.Lock()
        self._degraded_components: list[str] = []
        self._init_results: dict[str, str | None] = {}

        # ── Optional components — graceful degradation ──────────────
        self._try_init("encoder", lambda: _import_class('.encoder', 'DimensionEncoder')(
            registry_path=os.path.join(self._project_dir, "config", "dimensions.json")))

        self._try_init("topic_registry", lambda: _import_class('.topic_registry', 'TopicRegistry')(
            os.path.join(self._project_dir, "config", "dimensions.json")))

        if enable_semantic:
            def _make_embedding_store():
                from .embedding_store import EmbeddingStore
                es = EmbeddingStore(db_path=db_path, conn_provider=lambda: self.store.conn)
                self.store._embedding_store_ref = es
                logger.info("✅ 向量库已加载（sqlite-vec，共享连接模式）")
                return es
            self._try_init("embedding_store", _make_embedding_store)
        else:
            self.embedding_store = None
            self._mark_degraded("embedding_store")

        self._try_init("semantic_matcher", lambda: _import_class('.semantic_topic', 'SemanticTopicMatcher')(
            embedding_store=self.embedding_store,
            registry_path=os.path.join(self._project_dir, "config", "dimensions.json"),
        ) if self.embedding_store else None)

        self._try_init("pipeline", lambda: _import_class('.pipeline', 'IngestPipeline')(
            self.store, self.encoder,
            index_dir=os.path.join(self._project_dir, "daily_index"),
            embedding_store=self.embedding_store,
            topic_registry=self.topic_registry,
            semantic_matcher=self.semantic_matcher,
            llm_fn=llm_fn,
        ))

        if enable_filter:
            self._try_init("filter", lambda: _import_class('.memory_filter', 'MemoryFilter')(llm_fn=llm_fn))
        else:
            self.filter = None

        if enable_dedup:
            self._try_init("dedup", lambda: _import_class('.dedup', 'MemoryDeduplicator')(self.store, self.embedding_store))
        else:
            self.dedup = None

        self._try_init("quality", lambda: _import_class('.quality', 'MemoryQuality')(
            self.store, os.path.join(self._project_dir, "quality_stats.json")))

        if enable_semantic:
            def _make_reranker():
                from .reranker import Reranker
                r = Reranker(use_reranker=True)
                if r.is_available:
                    logger.info(f"✅ Reranker 已加载: {r.model_type}")
                else:
                    logger.info(f"⚠️ Reranker 降级: {r.model_type}")
                return r
            self._try_init("reranker", _make_reranker)
        else:
            self.reranker = None

        if vision_fn or audio_fn:
            def _make_media_processor():
                from .media_processor import MediaProcessor
                mp = MediaProcessor(vision_fn=vision_fn, audio_fn=audio_fn)
                logger.info(f"✅ 多模态处理器已加载: {mp.get_stats()}")
                return mp
            self._try_init("media_processor", _make_media_processor)
        else:
            self.media_processor = None
            try:
                from .media_processor import MediaProcessor
                self.media_processor = MediaProcessor.auto()
                if self.media_processor.is_available:
                    logger.info(f"✅ 多模态自动检测: {self.media_processor.get_stats()}")
            except Exception as e:
                logger.debug(f"多模态自动检测失败: {e}")

        self._try_init("causal", lambda: _import_class('.causal', 'CausalChain')(self.store, llm_fn=llm_fn))

        self._try_init("compressor", lambda: _import_class('.compressor', 'MemoryCompressor')(self.store, self.encoder, llm_fn=llm_fn))

        self._try_init("decay", lambda: _import_class('.decay', 'MemoryDecay')(self.store, self.encoder, embedding_store=self.embedding_store))

        self._try_init("hierarchy", lambda: _import_class('.hierarchical', 'HierarchicalMemory')(self.store, self.quality))

        self._try_init("self_healing", lambda: _import_class('.self_healing', 'SelfHealing')(self.store, self.embedding_store))

        self._try_init("graph", lambda: _import_class('.memory_graph', 'MemoryGraph')(self.store, self.topic_registry))

        self._try_init("timeline", lambda: _import_class('.timeline', 'MemoryTimeline')(self.store, llm_fn=llm_fn))

        # Lazy-loaded cognitive components (initialized on first access via @property)
        self._self_model = None
        self._metacognition = None
        self._motivation = None
        self._narrative = None
        self._digital_twin = None
        self._role_manager = None
        self._style_analyzer = None
        self._emotion_tracker = None
        self._llm_fn = llm_fn

        # Circuit breakers for external services
        self._llm_breaker = get_breaker("llm_api", failure_threshold=3, recovery_timeout=30)
        self._embedding_breaker = get_breaker("embedding", failure_threshold=3, recovery_timeout=60)

        def _make_reactor():
            from .reactor import MemoryReactor
            r = MemoryReactor()
            r.register_default_hooks()
            return r
        self._try_init("reactor", _make_reactor)

        self._try_init("recall_engine", lambda: _import_class('.recall', 'RecallEngine')(
            self.store, self.encoder, self.embedding_store, quality=self.quality, reranker=self.reranker, self_model=None, config=recall_config))

        self._try_init("archiver", lambda: _import_class('.archiver', 'Archiver')(self.pipeline, self.store, self.encoder))

        self._try_init("distiller", lambda: _import_class('.distill', 'MemoryDistiller')(
            store=self.store, encoder=self.encoder, llm_fn=llm_fn, embedding_store=self.embedding_store))

        self._try_init("pack_manager", lambda: _import_class('.memory_pack', 'MemoryPackManager')(
            store=self.store, encoder=self.encoder, pack_dir=os.path.join(self._project_dir, "packs")))

        self._try_init("session_context", lambda: _import_class('.session_context', 'SessionContext')())

        self._try_init("context_builder", lambda: _import_class('.context_builder', 'ContextBuilder')(
            self.recall_engine, session_context=self.session_context))

        self._enable_filter = enable_filter
        self._enable_dedup = enable_dedup

        self._try_init("cleaner", lambda: _import_class('.content_cleaner', 'ContentCleaner')())

        self.agent_id = agent_id
        self.team_id = team_id

        if agent_id:
            def _make_agent_network():
                from .agent_network import AgentMemoryNetwork, AgentIdentity
                net = AgentMemoryNetwork(self.store)
                net.register(AgentIdentity(agent_id=agent_id, agent_name=agent_id, team_id=team_id))
                logger.info(f"✅ 多 Agent 模式: agent={agent_id}, team={team_id}")
                return net
            self._try_init("agent_network", _make_agent_network)
        else:
            self.agent_network = None

        self._report_capabilities()

        # Lazy-loaded engine components
        self._ingest_engine = None
        self._recall_engine_v2 = None
        self._maintain_engine = None
        self._cognition_engine = None
        self._spirit = None
        self._feedback_learner = None
        self._curiosity_engine = None
        self._knowledge_validator = None
        self._federation_engine = None
        self._sync_engine = None

        # Config for lazy-loaded engines
        self._ingest_config = ingest_config

    def _is_feature_enabled(self, feature_name: str, default: bool = True) -> bool:
        """Check if a feature flag is enabled.

        Args:
            feature_name: Name of the feature flag.
            default: Default value if FeatureFlagManager is unavailable or flag not found.

        Returns:
            True if the feature is enabled, False otherwise.
        """
        if self._feature_flags is None:
            return default
        try:
            return self._feature_flags.is_enabled(feature_name)
        except Exception:
            return default

    def _try_init(self, attr_name: str, factory: callable):
        """Try to initialize a component, with dependency checking and result tracking.

        Args:
            attr_name: Attribute name to set on self (e.g., "encoder")
            factory: Callable that creates the component (e.g., lambda: DimensionEncoder(...))

        The factory should contain the import + instantiation logic.
        On ImportError: set to None, add to degraded, log info.
        On other Exception: set to None, add to degraded, log warning.
        If factory returns None: set to None (no degraded tracking — dependency already tracked).

        Dependency checking: if any declared dependency failed to initialize,
        the component is skipped and marked as degraded.
        """
        # Check if dependencies are available
        deps = self._COMPONENT_DEPENDENCIES.get(attr_name, [])
        missing_deps = [d for d in deps if d != "store" and self._init_results.get(d) is None]

        if missing_deps:
            logger.warning("Component %s skipped — missing dependencies: %s", attr_name, missing_deps)
            setattr(self, attr_name, None)
            self._mark_degraded(attr_name)
            self._init_results[attr_name] = None
            return

        try:
            component = factory()
            setattr(self, attr_name, component)
            self._init_results[attr_name] = "ok"
        except ImportError:
            setattr(self, attr_name, None)
            self._mark_degraded(attr_name)
            self._init_results[attr_name] = None
            logger.info("组件 [%s] 不可用（依赖未安装），已降级", attr_name)
        except Exception as e:
            setattr(self, attr_name, None)
            self._mark_degraded(attr_name)
            self._init_results[attr_name] = f"failed: {e}"
            logger.warning("组件 [%s] 初始化失败: %s", attr_name, e)

            # Special handling for store — create degraded in-memory fallback
            if attr_name == "store":
                logger.error("Store initialization failed, creating degraded in-memory fallback: %s", e)
                try:
                    from .store import MemoryStore
                    fallback = MemoryStore.create_degraded()
                    setattr(self, attr_name, fallback)
                    self._init_results[attr_name] = "degraded"
                    return fallback
                except Exception:
                    pass

    def _mark_degraded(self, component: str):
        """Thread-safe: add a component to the degraded list (no duplicates)."""
        with self._degraded_lock:
            if component not in self._degraded_components:
                self._degraded_components.append(component)

    @property
    def self_model(self):
        if self._self_model is None:
            from .self_model import SelfModel
            self._self_model = SelfModel(store=self.store)
            if self.recall_engine is not None:
                self.recall_engine.self_model = self._self_model
        return self._self_model

    @property
    def metacognition(self):
        if self._metacognition is None:
            from .metacognition import MetacognitiveEngine
            self._metacognition = MetacognitiveEngine(
                store=self.store,
                recall_engine=self.recall_engine,
                self_model=self.self_model,
                memory_system=self,
                llm_fn=self._llm_fn,
            )
        return self._metacognition

    @property
    def motivation(self):
        if self._motivation is None:
            from .motivation import MotivationEngine
            self._motivation = MotivationEngine(
                store=self.store,
                topic_registry=self.topic_registry,
                llm_fn=self._llm_fn,
            )
            self._motivation.load_state()
        return self._motivation

    @property
    def narrative(self):
        if self._narrative is None:
            from .narrative import NarrativeBuilder
            self._narrative = NarrativeBuilder(
                store=self.store,
                motivation=self.motivation,
                llm_fn=self._llm_fn,
                causal=self.causal,
            )
        return self._narrative

    @property
    def digital_twin(self):
        if self._digital_twin is None:
            from .digital_twin import DigitalTwinProfiler
            self._digital_twin = DigitalTwinProfiler(
                store=self.store,
                emotion_analyzer=self.pipeline.emotion_analyzer,
                self_model=self.self_model,
                motivation_engine=self.motivation,
                narrative_builder=self.narrative,
                quality_evaluator=self.quality,
            )
            logger.info("✅ 数字孪生模块已加载（懒加载）")
        return self._digital_twin

    @property
    def role_manager(self):
        if self._role_manager is None:
            try:
                from .role_template import RoleManager
                self._role_manager = RoleManager()
            except Exception as e:
                logger.warning("memory_system: %s", e)
        return self._role_manager

    @property
    def style_analyzer(self):
        if self._style_analyzer is None:
            try:
                from .style_analyzer import StyleAnalyzer
                self._style_analyzer = StyleAnalyzer()
            except Exception as e:
                logger.warning("memory_system: %s", e)
        return self._style_analyzer

    @property
    def emotion_tracker(self):
        if self._emotion_tracker is None:
            try:
                from .emotion_tracker import EmotionTracker
                self._emotion_tracker = EmotionTracker()
            except Exception as e:
                logger.warning("memory_system: %s", e)
        return self._emotion_tracker

    @property
    def ingest_engine(self):
        """v10.0 IngestEngine: filter→cleaner→dedup→pipeline + write cooldown + causal + reactor"""
        if self._ingest_engine is None:
            from .engines.ingest import IngestEngine
            self._ingest_engine = IngestEngine(
                pipeline=self.pipeline,
                store=self.store,
                embedding_store=self.embedding_store,
                llm_fn=self._llm_fn,
                causal_chain=self.causal,
                reactor=self.reactor,
                memory_filter=self.filter,
                content_cleaner=self.cleaner,
                deduplicator=self.dedup,
                emotion_tracker=getattr(self, 'emotion_tracker', None),
                motivation=getattr(self, 'motivation', None),
                config=self._ingest_config,
            )
        return self._ingest_engine

    @property
    def recall_engine_v2(self):
        """v10.0 EnhancedRecallEngine: quality-weighted + assessor + spread + graphrag"""
        if self._recall_engine_v2 is None:
            from .engines.recall_engine import EnhancedRecallEngine
            from .engines.recall_assessor import RecallAssessor
            from .engines.metacognitive_loop import MetacognitiveLoop
            graphrag = None
            try:
                from .graphrag import GraphRAG
                graphrag = GraphRAG(store=self.store, embedding_store=self.embedding_store)
            except Exception as e:
                logger.debug("GraphRAG init failed for recall_engine_v2: %s", e)
                pass
            assessor = RecallAssessor(
                store=self.store,
                embedding_store=self.embedding_store,
                semantic_matcher=self.semantic_matcher,
            )
            meta_loop = MetacognitiveLoop(store=self.store)
            self._recall_engine_v2 = EnhancedRecallEngine(
                quality=self.quality,
                embedding_store=self.embedding_store,
                store=self.store,
                topic_matcher=self.semantic_matcher,
                graphrag=graphrag,
                recall_assessor=assessor,
                metacognitive_loop=meta_loop,
            )
        return self._recall_engine_v2

    @property
    def maintain_engine(self):
        """v10.0 MaintainEngine: three-tier decay + healing + consolidation + timeline + reactor"""
        if self._maintain_engine is None:
            from .engines.maintain import MaintainEngine
            from .engines.knowledge_builder import KnowledgeBuilder
            graphrag = None
            try:
                from .graphrag import GraphRAG
                graphrag = GraphRAG(store=self.store, embedding_store=self.embedding_store)
            except Exception as e:
                logger.debug("GraphRAG init failed for maintain_engine: %s", e)
                pass
            knowledge_builder = KnowledgeBuilder(
                store=self.store,
                embedding_store=self.embedding_store,
                graphrag=graphrag,
                causal=self.causal,
                llm_fn=self._llm_fn,
            )
            self._maintain_engine = MaintainEngine(
                store=self.store,
                encoder=self.encoder,
                embedding_store=self.embedding_store,
                quality=self.quality,
                distill=self.distiller,
                llm_fn=self._llm_fn,
                embedder=getattr(self, 'embedder', None),
                tier_config=None,
                timeline=self.timeline,
                reactor=self.reactor,
                knowledge_builder=knowledge_builder,
                feedback_learner=self.feedback_learner,
            )
        return self._maintain_engine

    @property
    def cognition_engine(self):
        """v10.0 CognitionEngine: read-only cognitive core"""
        if self._cognition_engine is None:
            from .engines.cognition import CognitionEngine
            self._cognition_engine = CognitionEngine(
                store=self.store,
                recall_engine=self.recall_engine,
                embedding_store=self.embedding_store,
                llm_fn=self._llm_fn,
                self_model=self._self_model,
                metacognition=self._metacognition,
                motivation=self._motivation,
                narrative=self._narrative,
                digital_twin=self._digital_twin,
                personality_analyzer=getattr(self, '_personality_analyzer', None),
                personality_memory=getattr(self, '_personality_memory', None),
                style_analyzer=self._style_analyzer,
                emotion_tracker=self._emotion_tracker,
            )
        return self._cognition_engine

    @property
    def spirit(self):
        """v10.0 Spirit: unified butler + awareness system"""
        # Feature flag: spirit_proactive — if disabled, return None
        if not self._is_feature_enabled("spirit_proactive", default=True):
            return None

        if self._spirit is None:
            from .spirit.spirit import Spirit
            llm_client = None
            if hasattr(self, '_llm_client') and self._llm_client is not None:
                llm_client = self._llm_client
            elif self._llm_fn is not None:
                try:
                    from .llm_client import LLMClient
                    llm_client = LLMClient(config={"llm_fn": self._llm_fn})
                except Exception as e:
                    logger.debug("LLMClient init failed: %s", e)
                    pass
            self._spirit = Spirit(
                store=self.store,
                recall_engine=self.recall_engine_v2,
                maintain_engine=self.maintain_engine,
                cognition_engine=self.cognition_engine,
                embedding_store=self.embedding_store,
                llm_client=llm_client,
            )
        return self._spirit

    @property
    def feedback_learner(self):
        """v10.0 FeedbackLearner: continuous learning from user feedback"""
        if self._feedback_learner is None:
            from .engines.feedback_learner import FeedbackLearner
            self._feedback_learner = FeedbackLearner(
                store=self.store,
                quality=self.quality,
            )
        return self._feedback_learner

    @property
    def federation_engine(self):
        """v10.1 FederationEngine: cross-agent knowledge federation"""
        if self._federation_engine is None:
            from .engines.federation import FederationEngine
            self._federation_engine = FederationEngine(
                store=self.store,
                recall_engine=self.recall_engine,
                embedding_store=self.embedding_store,
            )
        return self._federation_engine

    @property
    def sync_engine(self):
        """v6.0 SyncEngine: distributed memory synchronization"""
        if self._sync_engine is None:
            from .engines.sync_engine import SyncEngine
            self._sync_engine = SyncEngine(
                store=self.store,
                node_id=self.agent_id or "local",
            )
        return self._sync_engine

    @property
    def curiosity_engine(self):
        """Level 6.0 CuriosityEngine: autonomous exploration and gap-filling"""
        if self._curiosity_engine is None:
            from .engines.curiosity import CuriosityEngine
            self._curiosity_engine = CuriosityEngine(
                store=self.store,
                recall_engine=self.recall_engine,
                federation_engine=getattr(self, '_federation_engine', None),
                llm_fn=self._llm_fn,
            )
        return self._curiosity_engine

    @property
    def knowledge_validator(self):
        """Level 6.0 KnowledgeValidator: cross-reference and staleness validation"""
        if self._knowledge_validator is None:
            from .engines.knowledge_validator import KnowledgeValidator
            self._knowledge_validator = KnowledgeValidator(
                store=self.store,
                embedding_store=self.embedding_store,
                llm_fn=self._llm_fn,
            )
        return self._knowledge_validator

    def get_degradation_warnings(self) -> list[str]:
        """返回当前降级组件的人类可读警告列表。"""
        with self._degraded_lock:
            degraded = list(self._degraded_components)
        warnings = []
        if "embedding_store" in degraded:
            warnings.append("语义搜索不可用，检索质量将降低")
        if "recall_engine" in degraded:
            warnings.append("高级检索引擎不可用，使用基础检索模式")
        if "encoder" in degraded:
            warnings.append("记忆质量评分不可用")
        if "spirit" in degraded:
            warnings.append("Spirit 管家不可用")
        if "pipeline" in degraded:
            warnings.append("写入管线不可用，使用直接存储模式")
        if "filter" in degraded:
            warnings.append("内容过滤不可用，所有内容将直接写入")
        if "dedup" in degraded:
            warnings.append("去重不可用，可能产生重复记忆")
        if "quality" in degraded:
            warnings.append("质量评分不可用")
        if "reranker" in degraded:
            warnings.append("重排序不可用，检索结果排序精度降低")
        if "causal" in degraded:
            warnings.append("因果链检测不可用")
        if "decay" in degraded:
            warnings.append("记忆衰减管理不可用")
        if "distiller" in degraded:
            warnings.append("记忆蒸馏不可用")
        if "self_healing" in degraded:
            warnings.append("自修复不可用")
        if "timeline" in degraded:
            warnings.append("时间旅行不可用")
        if "graph" in degraded:
            warnings.append("记忆图谱不可用")
        if "reactor" in degraded:
            warnings.append("反应器不可用")
        if "context_builder" in degraded:
            warnings.append("上下文构建不可用")
        if "session_context" in degraded:
            warnings.append("会话上下文不可用")
        if "archiver" in degraded:
            warnings.append("归档不可用")
        if "compressor" in degraded:
            warnings.append("记忆压缩不可用")
        if "hierarchy" in degraded:
            warnings.append("层次化记忆不可用")
        if "cleaner" in degraded:
            warnings.append("内容清洗不可用")
        if "agent_network" in degraded:
            warnings.append("多 Agent 网络不可用")
        if "semantic_matcher" in degraded:
            warnings.append("语义主题匹配不可用")
        if "topic_registry" in degraded:
            warnings.append("主题注册表不可用")
        if "pack_manager" in degraded:
            warnings.append("记忆包管理不可用")
        if "media_processor" in degraded:
            warnings.append("多模态处理不可用")
        return warnings

    def health_check(self) -> dict:
        """Enhanced health check with severity and dependency analysis.

        Returns:
            {
                "healthy": bool,           # True if all critical components work
                "status": str,             # "healthy" / "degraded" / "unhealthy" / "minor_degraded"
                "components": {            # Per-component status
                    "store": str,          # "healthy" / "degraded" / "unhealthy"
                    "fts5": str,
                    "embedding": str,
                    "bm25": str,
                    "causal_chain": str,
                    "spirit": str,
                },
                "degraded_features": list, # List of degraded feature names
                "severity": {              # Severity classification
                    "critical": list,
                    "major": list,
                    "minor": list,
                },
                "cascade_impact": list,    # Components impacted by cascade
                "recommendations": list,   # Actionable recommendations
                "last_error": str or None, # Last critical error message
                "uptime_seconds": float,   # Time since initialization
                "stats": {                 # Quick stats
                    "total_memories": int,
                    "total_links": int,
                    "db_size_mb": float,
                }
            }
        """
        components = {}
        degraded_features = []
        last_error = None

        # ── Critical component: store ──
        try:
            self.store.count()
            components["store"] = "healthy"
        except Exception as e:
            components["store"] = "unhealthy"
            last_error = str(e)

        # ── Critical component: fts5 ──
        try:
            has_fts = getattr(self.store, '_fts_mgr', None) is not None and self.store._fts_mgr.has_fts
            components["fts5"] = "healthy" if has_fts else "degraded"
            if not has_fts:
                degraded_features.append("fts5")
        except Exception as e:
            components["fts5"] = "unhealthy"
            last_error = str(e)

        # ── Non-critical: embedding ──
        if self.embedding_store is None:
            components["embedding"] = "degraded"
            degraded_features.append("embedding")
        else:
            try:
                self.embedding_store.count()
                components["embedding"] = "healthy"
            except Exception:
                components["embedding"] = "degraded"
                degraded_features.append("embedding")

        # ── Non-critical: bm25 ──
        if self.recall_engine is not None and hasattr(self.recall_engine, 'bm25_index'):
            try:
                if self.recall_engine.bm25_index is not None:
                    components["bm25"] = "healthy"
                else:
                    components["bm25"] = "degraded"
                    degraded_features.append("bm25")
            except Exception:
                components["bm25"] = "degraded"
                degraded_features.append("bm25")
        else:
            components["bm25"] = "degraded"
            degraded_features.append("bm25")

        # ── Non-critical: causal_chain ──
        if self.causal is not None:
            try:
                components["causal_chain"] = "healthy"
            except Exception:
                components["causal_chain"] = "degraded"
                degraded_features.append("causal_chain")
        else:
            components["causal_chain"] = "degraded"
            degraded_features.append("causal_chain")

        # ── Non-critical: spirit ──
        if self._spirit is not None:
            components["spirit"] = "healthy"
        else:
            components["spirit"] = "degraded"
            degraded_features.append("spirit")

        # ── Calculate overall severity ──
        degraded = list(self._degraded_components)

        critical_degraded = [c for c in degraded if self._COMPONENT_SEVERITY.get(c) == "critical"]
        major_degraded = [c for c in degraded if self._COMPONENT_SEVERITY.get(c) == "major"]
        minor_degraded = [c for c in degraded if self._COMPONENT_SEVERITY.get(c, "minor") == "minor"]

        # Determine overall status
        if critical_degraded:
            overall_status = "unhealthy"
        elif major_degraded:
            overall_status = "degraded"
        elif minor_degraded:
            overall_status = "minor_degraded"
        else:
            overall_status = "healthy"

        # Calculate impact — which components are affected by cascade
        impacted = set()
        for failed_comp in degraded:
            for comp, deps in self._COMPONENT_DEPENDENCIES.items():
                if failed_comp in deps and self._init_results.get(comp) is None:
                    impacted.add(comp)

        # ── Quick stats ──
        stats = {
            "total_memories": 0,
            "total_links": 0,
            "db_size_mb": 0.0,
        }
        try:
            stats["total_memories"] = self.store.count()
        except Exception as e:
            logger.debug("统计查询失败: %s", e)
        try:
            link_rows = self.store.execute_sql("SELECT COUNT(*) as cnt FROM memory_links", fetch=True)
            stats["total_links"] = link_rows[0]["cnt"] if link_rows else 0
        except Exception as e:
            logger.debug("统计查询失败: %s", e)
        try:
            db_size = os.path.getsize(self.store.db_path)
            stats["db_size_mb"] = round(db_size / (1024 * 1024), 2)
        except Exception as e:
            logger.debug("统计查询失败: %s", e)

        return {
            "healthy": overall_status == "healthy" or overall_status == "minor_degraded",
            "status": overall_status,
            "components": components,
            "degraded_features": degraded_features,
            "severity": {
                "critical": critical_degraded,
                "major": major_degraded,
                "minor": minor_degraded,
            },
            "cascade_impact": list(impacted),
            "recommendations": self._generate_degradation_recommendations(critical_degraded, major_degraded),
            "last_error": last_error,
            "uptime_seconds": time.time() - self._init_time,
            "stats": stats,
        }

    def _generate_degradation_recommendations(self, critical, major):
        """Generate actionable recommendations based on degraded components."""
        recs = []
        if critical:
            recs.append(f"CRITICAL: {', '.join(critical)} unavailable — core functionality impaired")
        if "encoder" in major or "embedding_store" in major:
            recs.append("Install sentence-transformers to enable semantic search: pip install agent-memory[semantic]")
        if "reranker" in major:
            recs.append("Install FlagEmbedding for better result ranking: pip install agent-memory[reranker]")
        return recs

    def _check_auto_compress(self):
        """Check if auto-compression should run and execute if needed."""
        if not self._auto_compress:
            return

        try:
            count = self.store.count()
            policy = self._compress_policy

            if count < policy.get("min_memories_to_compress", 100):
                return

            # Find old, rarely-accessed memories
            cutoff_ts = time.time() - (policy["age_threshold_days"] * 86400)
            candidates = self.store.query(
                time_to=int(cutoff_ts),
                importance="low",
                limit=100,
            )

            if len(candidates) < 10:
                return

            # Compress using distiller
            if hasattr(self, 'distiller') and self.distiller:
                compressed = self.distiller.distill()
                logger.info("auto_compress_completed", extra={
                    "event": "auto_compress_completed",
                    "candidates": len(candidates),
                    "compressed": len(compressed.get("topics_created", [])) if compressed else 0,
                })
        except Exception as e:
            logger.debug("Auto-compress check failed: %s", e)

    def _report_capabilities(self):
        caps = self.check_capabilities()
        available = [k for k, v in caps.items() if v["status"] == "ok"]
        degraded = [k for k, v in caps.items() if v["status"] == "degraded"]
        unavailable = [k for k, v in caps.items() if v["status"] == "unavailable"]

        if available:
            logger.info(f"✅ 可用: {', '.join(available)}")
        if degraded:
            logger.warning(f"⚠️ 降级: {', '.join(degraded)} — {caps[degraded[0]]['detail'] if degraded else ''}")
        if unavailable:
            logger.info(f"ℹ️ 不可用: {', '.join(unavailable)} — {caps[unavailable[0]]['detail'] if unavailable else ''}")

    def check_capabilities(self) -> dict:
        caps = {}

        try:
            has_fts = self.store._has_fts if hasattr(self.store, '_has_fts') else False
            caps["sqlite_fts5"] = {
                "status": "ok" if has_fts else "degraded",
                "detail": "FTS5 trigram 全文搜索" if has_fts else "FTS5 不可用，降级为 LIKE 搜索",
            }
        except Exception as e:
            logger.debug("FTS5 check failed: %s", e)
            caps["sqlite_fts5"] = {"status": "degraded", "detail": "FTS5 状态未知"}

        if self.embedding_store:
            try:
                backend = self.embedding_store._backend
                use_model = self.embedding_store._use_model
                if use_model:
                    caps["semantic_search"] = {
                        "status": "ok",
                        "detail": f"sqlite-vec + {self.embedding_store._model_name} ({backend})",
                    }
                elif backend == "hash":
                    caps["semantic_search"] = {
                        "status": "degraded",
                        "detail": "SimHash 降级模式，语义精度极低",
                    }
                else:
                    caps["semantic_search"] = {
                        "status": "degraded",
                        "detail": f"{backend} 后端初始化失败，将尝试加载",
                    }
            except Exception as e:
                logger.debug("EmbeddingStore status check failed: %s", e)
                caps["semantic_search"] = {"status": "degraded", "detail": "EmbeddingStore 状态异常"}
        else:
            caps["semantic_search"] = {
                "status": "unavailable",
                "detail": "sqlite-vec/sentence-transformers 未安装",
            }

        if self.reranker and self.reranker.is_available:
            caps["reranker"] = {
                "status": "ok",
                "detail": f"交叉编码器重排序 ({self.reranker.model_type})",
            }
        elif self.reranker:
            caps["reranker"] = {
                "status": "degraded",
                "detail": f"FlagEmbedding 未安装，降级为分数排序",
            }
        else:
            caps["reranker"] = {"status": "unavailable", "detail": "未启用"}

        if self.distiller and self.distiller.llm_fn:
            caps["distillation_llm"] = {
                "status": "ok",
                "detail": "LLM 辅助蒸馏（主题摘要 + 实体提取 + 百科生成）",
            }
        else:
            caps["distillation_llm"] = {
                "status": "degraded",
                "detail": "无 LLM，蒸馏使用启发式降级（关键词提取 + 分类拼接）",
            }

        caps["causal_chain"] = {
            "status": "ok",
            "detail": "启发式 + 时间线 + 链式传递 + 主题相似（4层检测）",
        }

        try:
            if self.embedding_store:
                self.embedding_store._ensure_clip()
                if self.embedding_store._clip_model:
                    caps["multimodal_clip"] = {
                        "status": "ok",
                        "detail": "CLIP 图片 embedding（跨模态检索）",
                    }
                else:
                    caps["multimodal_clip"] = {
                        "status": "unavailable",
                        "detail": "transformers/torch 未安装",
                    }
            else:
                caps["multimodal_clip"] = {"status": "unavailable", "detail": "需要 embedding_store"}
        except Exception as e:
            logger.debug("CLIP capability check failed: %s", e)
            caps["multimodal_clip"] = {"status": "unavailable", "detail": "CLIP 加载失败"}

        caps["multi_agent"] = {
            "status": "ok" if self.agent_network else "unavailable",
            "detail": f"agent={self.agent_id}, team={self.team_id}" if self.agent_network else "未设置 agent_id",
        }

        caps["time_travel"] = {"status": "ok", "detail": "快照 / 差异对比 / 来源追溯"}
        caps["self_reference"] = {
            "status": "ok" if self.self_model else "unavailable",
            "detail": "推理追踪 / 置信度历史 / 自我反思",
        }
        caps["metacognition"] = {
            "status": "ok" if self.metacognition else "unavailable",
            "detail": "检索评估 / 反思修正 / 多轮反思检索",
        }
        caps["motivation"] = {
            "status": "ok" if self.motivation else "unavailable",
            "detail": "好奇心 / 无聊度 / 知识空白 / 探索任务",
        }
        caps["narrative"] = {
            "status": "ok" if self.narrative else "unavailable",
            "detail": "身份画像 / 时间线叙事 / 主题叙事 / WhoAmI",
        }
        caps["reactor"] = {"status": "ok", "detail": "记忆驱动的 Agent 行为（提醒/矛盾/衰减）"}

        return caps

    @property
    def backend(self):
        """Access the StorageBackend interface (backend-agnostic)."""
        if self.store:
            return self.store.backend
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def __repr__(self):
        status = "shutting_down" if getattr(self, '_shutting_down', False) else "active"
        degraded = len(getattr(self, '_degraded_components', []))
        return f"AgentMemory(agent_id={self.agent_id!r}, status={status}, degraded={degraded})"

    def close(self):
        """Graceful shutdown: flush buffers, stop background threads, checkpoint WAL."""
        if hasattr(self, '_shutting_down') and self._shutting_down:
            return  # Already shutting down

        self._shutting_down = True
        logger.info("agent_memory_shutting_down", extra={
            "event": "agent_memory_shutting_down",
        })

        # 1. Stop Spirit scheduler
        if hasattr(self, '_spirit') and self._spirit:
            try:
                if hasattr(self._spirit, 'stop'):
                    self._spirit.stop(timeout=5)
            except Exception as e:
                logger.warning("Failed to stop Spirit: %s", e)

        # 2. Stop Backup scheduler
        if hasattr(self, '_backup_scheduler') and self._backup_scheduler:
            try:
                if hasattr(self._backup_scheduler, 'stop'):
                    self._backup_scheduler.stop(timeout=5)
            except Exception as e:
                logger.warning("Failed to stop backup scheduler: %s", e)

        # 3. Flush tenant manager metering
        if hasattr(self, '_tenant_manager') and self._tenant_manager:
            try:
                if hasattr(self._tenant_manager, 'flush'):
                    self._tenant_manager.flush()
            except Exception as e:
                logger.warning("Failed to flush tenant manager: %s", e)

        # 4. Flush billing engine
        if hasattr(self, '_billing_engine') and self._billing_engine:
            try:
                if hasattr(self._billing_engine, 'flush'):
                    self._billing_engine.flush()
            except Exception as e:
                logger.warning("Failed to flush billing engine: %s", e)

        # 5. WAL checkpoint
        if self.store:
            try:
                self.store.conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
            except Exception as e:
                logger.warning("Failed to WAL checkpoint: %s", e)

        # 6. Close store
        if self.store:
            try:
                self.store.close()
            except Exception as e:
                logger.warning("Failed to close store: %s", e)

        logger.info("agent_memory_shutdown_complete", extra={
            "event": "agent_memory_shutdown_complete",
        })

    def close_all(self):
        self.store.close_all()

    def _check_schema_version(self):
        CURRENT_SCHEMA_VERSION = 6

        self.store.register_schema("migration_0", """
            CREATE TABLE IF NOT EXISTS _schema_version (
                version INTEGER PRIMARY KEY,
                applied_at INTEGER NOT NULL DEFAULT (strftime('%s','now'))
            );
        """)

        rows = self.store.execute_sql(
            "SELECT version FROM _schema_version ORDER BY version DESC LIMIT 1",
            fetch=True,
        )
        db_version = rows[0]["version"] if rows else 0

        if db_version == CURRENT_SCHEMA_VERSION:
            self._run_file_migrations(db_version)
            return

        if db_version > CURRENT_SCHEMA_VERSION:
            logger.warning(
                f"⚠️ 数据库版本 (v{db_version}) 高于代码版本 (v{CURRENT_SCHEMA_VERSION})。"
                f"请升级 agent-memory 到 v{db_version}+ 或使用 migrate.py rollback。"
                f"继续运行可能丢失新版本数据。"
            )
            return

        logger.info(f"Schema 迁移: v{db_version} → v{CURRENT_SCHEMA_VERSION}")
        applied = []

        if db_version < 1:
            try:
                from .store import SCHEMA_PATH
            except Exception as e:
                logger.warning("memory_system: %s", e)
            applied.append("v1: base schema")

        if db_version < 2:
            try:
                from .distill import DISTILL_SCHEMA
                self.store.register_schema("migration_2_distill", DISTILL_SCHEMA)
                applied.append("v2: distill tables")
            except Exception as e:
                logger.warning("memory_system: %s", e)

            try:
                from .pipeline import _WRITE_QUEUE_SCHEMA
                self.store.register_schema("migration_2_write_queue", _WRITE_QUEUE_SCHEMA)
                applied.append("v2: write_queue table")
            except Exception as e:
                logger.warning("memory_system: %s", e)

        if db_version < 3:
            try:
                from .timeline import TIMELINE_SCHEMA
                self.store.register_schema("migration_3_timeline", TIMELINE_SCHEMA)
                applied.append("v3: timeline tables")
            except Exception as e:
                logger.warning("memory_system: %s", e)

        if db_version < 4:
            self.self_ref_schema = """
                CREATE TABLE IF NOT EXISTS reasoning_traces (
                    trace_id        TEXT PRIMARY KEY,
                    query           TEXT NOT NULL,
                    result_summary  TEXT,
                    confidence      REAL DEFAULT 0.0,
                    sources_used    TEXT DEFAULT '[]',
                    steps           TEXT DEFAULT '[]',
                    uncertainty     TEXT DEFAULT '[]',
                    created_at      INTEGER NOT NULL DEFAULT (strftime('%s','now'))
                );
                CREATE TABLE IF NOT EXISTS self_reflections (
                    reflection_id   TEXT PRIMARY KEY,
                    trace_id        TEXT,
                    insight         TEXT NOT NULL,
                    action_taken    TEXT,
                    created_at      INTEGER NOT NULL DEFAULT (strftime('%s','now')),
                    FOREIGN KEY (trace_id) REFERENCES reasoning_traces(trace_id)
                );
                CREATE INDEX IF NOT EXISTS idx_trace_query ON reasoning_traces(query);
                CREATE INDEX IF NOT EXISTS idx_trace_confidence ON reasoning_traces(confidence);
                CREATE INDEX IF NOT EXISTS idx_trace_created ON reasoning_traces(created_at DESC);
                CREATE INDEX IF NOT EXISTS idx_reflection_trace ON self_reflections(trace_id);
                CREATE INDEX IF NOT EXISTS idx_reflection_created ON self_reflections(created_at DESC);
            """
            try:
                self.store.register_schema("migration_4_self_ref", self.self_ref_schema)
                applied.append("v4: reasoning_traces + self_reflections")
            except Exception as e:
                logger.warning("memory_system: %s", e)

        if db_version < 5:
            try:
                self.store.register_schema("migration_5_internal_state", """
                    CREATE TABLE IF NOT EXISTS internal_state (
                        state_id        TEXT PRIMARY KEY,
                        curiosity       REAL DEFAULT 0.3,
                        boredom         REAL DEFAULT 0.0,
                        confidence      REAL DEFAULT 0.5,
                        satisfaction    REAL DEFAULT 0.5,
                        urgency         REAL DEFAULT 0.0,
                        dominant_drive  TEXT DEFAULT 'none',
                        updated_at      INTEGER NOT NULL DEFAULT (strftime('%s','now'))
                    );
                """)
                applied.append("v5: internal_state")
            except Exception as e:
                logger.warning("memory_system: %s", e)

        if db_version < 6:
            try:
                self.store.register_schema("migration_6_identity", """
                    CREATE TABLE IF NOT EXISTS identity_model (
                        key             TEXT PRIMARY KEY,
                        value           TEXT NOT NULL,
                        confidence      REAL DEFAULT 0.5,
                        evidence_count  INTEGER DEFAULT 0,
                        updated_at      INTEGER NOT NULL DEFAULT (strftime('%s','now'))
                    );
                    CREATE TABLE IF NOT EXISTS life_narratives (
                        narrative_id        TEXT PRIMARY KEY,
                        narrative_type      TEXT NOT NULL,
                        title               TEXT NOT NULL,
                        content             TEXT NOT NULL,
                        period_start        INTEGER,
                        period_end          INTEGER,
                        source_memory_count INTEGER DEFAULT 0,
                        created_at          INTEGER NOT NULL DEFAULT (strftime('%s','now'))
                    );
                    CREATE INDEX IF NOT EXISTS idx_identity_key ON identity_model(key);
                    CREATE INDEX IF NOT EXISTS idx_narrative_type ON life_narratives(narrative_type);
                    CREATE INDEX IF NOT EXISTS idx_narrative_created ON life_narratives(created_at DESC);
                """)
                applied.append("v6: identity_model + life_narratives")
            except Exception as e:
                logger.warning("memory_system: %s", e)

        self._run_file_migrations(CURRENT_SCHEMA_VERSION)

        self.store.execute_sql(
            "INSERT INTO _schema_version (version) VALUES (?)",
            (CURRENT_SCHEMA_VERSION,),
        )
        if applied:
            logger.info(f"✅ Schema 迁移完成: v{CURRENT_SCHEMA_VERSION} (applied: {', '.join(applied)})")
        else:
            logger.info(f"✅ Schema 版本确认: v{CURRENT_SCHEMA_VERSION}")

    def _run_file_migrations(self, _current_version: int = None):
        try:
            from .migrate import MigrationManager
            mgr = MigrationManager(db_path=self.store.db_path)
            pending = mgr.get_pending_migrations()
            if pending:
                logger.info(f"发现 {len(pending)} 个待应用的文件型迁移")
                result = mgr.upgrade()
                if result.get("applied"):
                    logger.info(f"文件型迁移完成: {result['applied']}")
                if result.get("errors"):
                    for err in result["errors"]:
                        logger.warning(f"迁移错误: {err}")
            mgr.conn.close()
        except Exception as e:
            logger.warning("memory_system: %s", e)