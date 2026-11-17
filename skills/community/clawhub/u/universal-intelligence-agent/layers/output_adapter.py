"""
输出适配层 — 内部数据结构到用户可见格式的转换
──────────────────────────────────────────────
所有输出在此层完成：
1. 格式适配（简报/深度报告/对比报告）
2. 副作用管理（文件写入通过 UnitOfWork）
3. 统一成功/失败标准
4. Jinja2 模板渲染（Phase 2 新增）
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Phase 2 新增：模板渲染
try:
    from jinja2 import Environment, FileSystemLoader, TemplateNotFound
    _JINJA2_AVAILABLE = True
except ImportError:
    _JINJA2_AVAILABLE = False
    logger.warning("Jinja2 not installed, falling back to string-based templates")


class DeliveryStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"    # 部分成功（有降级）
    FAILED = "failed"


class ReportFormat(str, Enum):
    BRIEF = "brief"           # 快速简报
    ANALYSIS = "analysis"     # 深度分析
    COMPARISON = "comparison" # 对比报告
    MARKDOWN = "markdown"     # 纯 Markdown
    JSON = "json"             # 结构化 JSON


@dataclass
class OutputResult:
    """
    统一输出结果 — 所有输出层函数的返回标准

    这是输出的唯一契约：无论内部如何实现，对外永远是 {status, data, errors, warnings}
    """
    status: DeliveryStatus
    data: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    output_path: Optional[Path] = None
    report_format: ReportFormat = ReportFormat.MARKDOWN

    @property
    def is_success(self) -> bool:
        return self.status in (DeliveryStatus.SUCCESS, DeliveryStatus.PARTIAL)

    @property
    def is_complete_success(self) -> bool:
        return self.status == DeliveryStatus.SUCCESS


class OutputAdapter:
    """
    输出适配器 — 将内部分析结果转换为用户可见格式

    用法:
        adapter = OutputAdapter()
        result = adapter.generate_report(
            analysis_data={...},
            format=ReportFormat.BRIEF,
            session_id="abc",
        )
        # → OutputResult(status=SUCCESS, output_path=Path("/tmp/report.md"))
    """

    def __init__(self):
        """初始化模板环境"""
        if _JINJA2_AVAILABLE:
            # 查找模板目录
            import os
            template_dirs = []
            # 相对于当前文件
            current_dir = Path(__file__).parent.parent / "templates"
            if current_dir.exists():
                template_dirs.append(str(current_dir))
            # 相对于工作目录
            cwd_templates = Path(os.getcwd()) / "templates"
            if cwd_templates.exists() and str(cwd_templates) not in template_dirs:
                template_dirs.append(str(cwd_templates))
            if template_dirs:
                self._jinja_env = Environment(
                    loader=FileSystemLoader(template_dirs),
                    autoescape=False,  # Markdown 不需要 HTML 转义
                )
            else:
                self._jinja_env = None
        else:
            self._jinja_env = None

    def _render_template(self, template_name: str, context: dict) -> str:
        """使用 Jinja2 渲染模板，降级时使用字符串拼接"""
        if self._jinja_env:
            try:
                template = self._jinja_env.get_template(template_name)
                return template.render(**context)
            except TemplateNotFound:
                logger.debug(f"Template {template_name} not found, using fallback")
            except Exception as e:
                logger.warning(f"Template render failed: {e}, using fallback")
        return ""

    def generate_brief(
        self,
        analysis_data: dict,
        session_id: str,
        uow=None,
    ) -> OutputResult:
        """生成快速简报"""
        try:
            # Phase 5.3: 统一从 resolved 取值（修复数据源不一致）
            resolved = self._resolve_analysis_fields(analysis_data)
            query = resolved["query"]
            total_engines = resolved["total_engines"]
            total_results = resolved["total_results"]
            deduped = resolved["deduplicated"]
            key_findings = resolved.get("key_findings", [])
            sources = resolved["sources"]

            # 可信度：从 resolved["credibility"] 提取（FieldMapper 已映射）
            cred = resolved.get("credibility", {})
            credibility = cred.get("average_score", 0) if isinstance(cred, dict) else 0

            # Phase 2: 尝试使用模板
            template_context = {
                "query": query,
                "total_engines": total_engines,
                "total_results": total_results,
                "deduplicated": deduped,
                "credibility": credibility,
                "key_findings": key_findings,
                "sources": sources,
            }
            report_text = self._render_template("brief_report.md", template_context)

            # 降级：字符串拼接
            if not report_text:
                stars = "★" * min(5, max(1, int(credibility)))
                empty_stars = "☆" * (5 - len(stars))

                lines = [
                    f"=== {query} 简报 ===",
                    f"来源: {total_engines}引擎 ({total_results}条) | 去重后: {deduped}条",
                    f"可信度: {stars}{empty_stars}",
                    "",
                ]

                if key_findings:
                    lines.append("核心发现:")
                    for i, finding in enumerate(key_findings[:5], 1):
                        lines.append(f"{i}. {finding}")
                    lines.append("")

                if sources:
                    lines.append("信息来源:")
                    for src in sources[:10]:
                        trust_val = src.get("trust_level", 3) if isinstance(src, dict) else 3
                        trust_label = {4: "高", 3: "中", 2: "低", 1: "存疑"}.get(
                            int(trust_val), "中"
                        )
                        src_name = src.get("source", "未知") if isinstance(src, dict) else "未知"
                        src_date = src.get("date", "?") if isinstance(src, dict) else "?"
                        src_title = src.get("title", "无标题") if isinstance(src, dict) else "无标题"
                        lines.append(
                            f"- {src_name} "
                            f"({src_date}) "
                            f"[{src_title}] "
                            f"[可信度:{trust_label}]"
                        )

                report_text = "\n".join(lines)

            return self._write_output(
                report_text, session_id, ReportFormat.BRIEF, uow,
            )

        except Exception as e:
            logger.error(f"Brief generation failed: {e}")
            return OutputResult(
                status=DeliveryStatus.FAILED,
                errors=[f"简报生成失败: {e}"],
            )

    def _resolve_analysis_fields(self, analysis_data: dict) -> dict:
        """
        Phase 4.1: 委托给 FieldMapper 处理。
        保留此方法作为兼容层——当 analysis_data 已是映射后的 dict 时直接返回。
        PipelineCoordinator 现在通过 FieldMapper 预先映射，此方法仅做兜底。
        """
        # 如果传入的已经是 PipelineCoordinator 通过 FieldMapper 映射过的 dict
        # （包含 query, total_engines, total_results 等 key），直接返回
        if "query" in analysis_data and "total_engines" in analysis_data:
            return analysis_data

        # 兜底：使用 FieldMapper 兼容旧版 dict 输入
        try:
            from layers.field_mapper import FieldMapper
            mapper = FieldMapper()
            # 尝试从 dict 重建 AnalysisOutput（兼容旧路径）
            from contracts.analysis_schema import AnalysisOutput
            analysis = AnalysisOutput.model_validate(analysis_data)
            return mapper.map_analysis_to_output(analysis)
        except Exception:
            # 无法重建 Schema，返回最小兼容 dict
            return {
                "query": analysis_data.get("query", "未知主题"),
                "total_engines": 0,
                "total_results": 0,
                "deduplicated": 0,
                "cn_count": 0,
                "global_count": 0,
                "date_range": "? ~ ?",
                "entities": {},
                "credibility": {},
                "sentiment": {"overall": "中性"},
                "cross_validation": {},
                "conclusions": [],
                "sources": [],
                "key_findings": [],
            }

    def generate_analysis(
        self,
        analysis_data: dict,
        session_id: str,
        uow=None,
    ) -> OutputResult:
        """生成深度分析报告"""
        try:
            # Phase 6: 统一字段解析
            resolved = self._resolve_analysis_fields(analysis_data)
            query = resolved["query"]
            total_engines = resolved["total_engines"]
            total_results = resolved["total_results"]
            deduped = resolved["deduplicated"]
            cn_count = resolved["cn_count"]
            global_count = resolved["global_count"]
            date_range = resolved["date_range"]
            entities = resolved["entities"]
            credibility = resolved["credibility"]
            sentiment = resolved["sentiment"]
            cross_validation = resolved["cross_validation"]
            conclusions = resolved["conclusions"]
            sources = resolved["sources"]

            lines = [
                f"=== {query} 深度分析 ===",
                "",
                "一、信息汇总",
                f"  引擎: {total_engines}台 | 结果: {total_results}条 | 去重: {deduped}条",
                f"  来源分布: 国内{cn_count}条, 国际{global_count}条",
                f"  时效: {date_range}",
                "",
            ]

            # 关键实体
            if entities:
                lines.append("二、关键实体")
                for entity_type, entity_list in entities.items():
                    if entity_list:
                        lines.append(f"  {entity_type}: {', '.join(entity_list[:10])}")
                lines.append("")

            # 可信度评估
            if credibility:
                lines.append("三、可信度评估")
                high = credibility.get("high", 0)
                medium = credibility.get("medium", 0)
                low = credibility.get("low", 0)
                dubious = credibility.get("dubious", 0)
                lines.append(f"  高可信: {high}条")
                lines.append(f"  中等: {medium}条")
                lines.append(f"  低可信/存疑: {low + dubious}条")
                lines.append("")

            # 情感倾向
            if sentiment:
                lines.append("四、情感/倾向")
                overall = sentiment.get("overall", "中性")
                lines.append(f"  整体: {{{overall}}}")
                lines.append("")

            # 交叉验证
            if cross_validation:
                lines.append("五、交叉验证")
                consistent = cross_validation.get("consistent", [])
                divergent = cross_validation.get("divergent", [])
                unverified = cross_validation.get("unverified", [])
                if consistent:
                    lines.append(f"  一致内容: {'; '.join(consistent[:3])}")
                if divergent:
                    lines.append(f"  分歧内容: {'; '.join(divergent[:3])}")
                if unverified:
                    lines.append(f"  待核实: {'; '.join(unverified[:3])}")
                lines.append("")

            # 结论
            if conclusions:
                lines.append("六、结论")
                for i, c in enumerate(conclusions, 1):
                    lines.append(f"  {i}. {c}")
                lines.append("")

            # 来源列表
            if sources:
                lines.append("---")
                lines.append("参考来源:")
                for src in sources:
                    lines.append(
                        f"- [{src.get('source', '未知')}] "
                        f"{src.get('title', '无标题')} "
                        f"({src.get('date', '?')})"
                    )

            report_text = "\n".join(lines)
            return self._write_output(
                report_text, session_id, ReportFormat.ANALYSIS, uow,
            )

        except Exception as e:
            logger.error(f"Analysis report generation failed: {e}")
            return OutputResult(
                status=DeliveryStatus.FAILED,
                errors=[f"分析报告生成失败: {e}"],
            )

    def generate_comparison(
        self,
        analysis_data: dict,
        session_id: str,
        uow=None,
    ) -> OutputResult:
        """生成对比分析报告 — Phase 5.2: 通过 FieldMapper 统一字段来源"""
        try:
            # Phase 5.2: 通过 _resolve_analysis_fields 统一字段解析
            resolved = self._resolve_analysis_fields(analysis_data)
            query = resolved.get("query", "未知主题")
            total_engines = resolved.get("total_engines", 0)
            total_results = resolved.get("total_results", 0)
            credibility = resolved.get("credibility", {})
            key_findings = resolved.get("key_findings", [])
            conclusions = resolved.get("conclusions", [])
            sources = resolved.get("sources", [])
            sentiment = resolved.get("sentiment", {})

            lines = [
                f"=== {query} 对比分析 ===",
                "",
                f"来源: {total_engines}引擎 ({total_results}条)",
                f"整体可信度: {credibility.get('high', 0)}高/{credibility.get('medium', 0)}中/{credibility.get('low', 0)}低",
                f"整体情感: {sentiment.get('overall', '中性')}",
                "",
            ]

            # 对比项（从 analysis_data 提取 items 列表）
            items = analysis_data.get("items", ["A", "B"])
            for item in items:
                item_data = analysis_data.get(item, {})
                lines.append(f"## {item}")
                lines.append(f"  相关发现: {len(item_data.get('key_findings', []))}条")
                for f in item_data.get("key_findings", [])[:3]:
                    lines.append(f"  - {f}")
                lines.append("")

            # 对比总结
            if conclusions:
                lines.append("## 对比总结")
                for i, c in enumerate(conclusions[:5], 1):
                    lines.append(f"  {i}. {c}")
                lines.append("")

            # 来源列表
            if sources:
                lines.append("---")
                lines.append("参考来源:")
                for src in sources[:10]:
                    src_name = src.get("source", "未知") if isinstance(src, dict) else "未知"
                    src_title = src.get("title", "无标题") if isinstance(src, dict) else "无标题"
                    lines.append(f"- [{src_name}] {src_title}")

            report_text = "\n".join(lines)
            return self._write_output(
                report_text, session_id, ReportFormat.COMPARISON, uow,
            )

        except Exception as e:
            logger.error(f"Comparison report generation failed: {e}")
            return OutputResult(
                status=DeliveryStatus.FAILED,
                errors=[f"对比报告生成失败: {e}"],
            )

    def generate_json(self, analysis_data: dict, session_id: str, uow=None) -> OutputResult:
        """生成 JSON 格式输出"""
        import json

        try:
            report_json = json.dumps(analysis_data, ensure_ascii=False, indent=2, default=str)
            return self._write_output(
                report_json, session_id, ReportFormat.JSON, uow, suffix=".json",
            )
        except Exception as e:
            return OutputResult(
                status=DeliveryStatus.FAILED,
                errors=[f"JSON输出失败: {e}"],
            )

    def _write_output(
        self,
        content: str,
        session_id: str,
        format: ReportFormat,
        uow=None,
        suffix: str = ".md",
    ) -> OutputResult:
        """统一的输出写入 — 通过 UnitOfWork 管理副作用

        Phase 4.1: 增加版本号机制，同一 session_id 重复执行不覆盖。
        """
        import os as _os

        output_dir = Path(_os.path.expanduser("~")) / ".uia" / "reports"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Phase 4.1: 幂等性 — 如果已存在同名文件，追加版本号
        base_name = f"{session_id}_{format.value}"
        output_path = output_dir / f"{base_name}{suffix}"
        version = 1
        while output_path.exists():
            output_path = output_dir / f"{base_name}_v{version}{suffix}"
            version += 1

        content_bytes = content.encode("utf-8")

        if uow:
            # 通过 UnitOfWork 管理写入（支持事务回滚）
            uow.register_write(
                path=output_path,
                content=content_bytes,
                rollback=lambda: output_path.unlink() if output_path.exists() else None,
            )
        else:
            # 无事务时的直接写入（不推荐，但兼容）
            output_path.write_bytes(content_bytes)

        return OutputResult(
            status=DeliveryStatus.SUCCESS,
            data={"content_preview": content[:200]},
            output_path=output_path,
            report_format=format,
        )
