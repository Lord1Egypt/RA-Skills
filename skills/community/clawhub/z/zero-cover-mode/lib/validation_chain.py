"""零稀泥模式 — 校验链 validation_chain.py

串联 root_cause → fake_data → backend_check 的完整校验流程。
从 Pipeline.phase2_test() 中抽取，职责单一。

Usage:
    from .validation_chain import ValidationChain, ValidationResult
    chain = ValidationChain()
    result = chain.validate_test(test_path, workspace_root)
"""

import os
import logging
from typing import Optional, List
from pydantic import BaseModel, Field

from . import root_cause_validator as rcv
from . import fake_data_detector as fdd
from . import backend_checker as bc
from .contracts import BackendCheckVerdict

log = logging.getLogger("validation")


class ValidationResult(BaseModel):
    """校验链结果 — Pydantic 契约"""
    passed: bool = True
    blocking: bool = False
    details: str = ""
    issues: List[str] = Field(default_factory=list)
    root_cause_analysis: Optional[dict] = None
    fake_data_result: Optional[dict] = None
    backend_check_result: Optional[dict] = None


class ValidationChain:
    """校验链 — 串联 root_cause + fake_data + backend_check

    职责：执行 Phase 1/2 中所有校验逻辑，返回统一的 ValidationResult。
    """

    def validate_root_cause(self, filepath: str) -> ValidationResult:
        result = ValidationResult()
        try:
            levels, analysis = rcv.check_depth(filepath)
            result.root_cause_analysis = analysis
            if analysis.get("blocking"):
                result.passed = False
                result.blocking = True
                result.details = (
                    f"根因深度不足: L{analysis['max_level']} "
                    f"(要求 >= L{analysis['min_required']}), "
                    f"缺失 {analysis['missing_levels']}"
                )
            else:
                result.details = (
                    f"5-Whys 深度 L{analysis['max_level']}, "
                    f"has_l4={analysis.get('has_l4')}"
                )
        except Exception as e:
            result.passed = False
            result.blocking = True
            result.details = f"根因验证异常: {e}"
            result.issues.append(str(e))
        return result

    def validate_test(self, test_path: str, workspace_root: str = "") -> ValidationResult:
        result = ValidationResult()

        # L1 + L3: 假数据检测
        try:
            fd_result = fdd.detect(test_path)
            result.fake_data_result = fd_result
            fake_data_blocking = (
                fd_result.get("L1", {}).get("blocking", False) or
                fd_result.get("L3", {}).get("blocking", False)
            )
            if fake_data_blocking:
                result.passed = False
                result.blocking = True
                result.details = "假数据检测 blocking (L1/L3)"
                result.issues.append("fake_data_blocking")
                return result
        except Exception as e:
            result.issues.append(f"fake_data_detector: {e}")
            log.warning("假数据检测异常: %s", e)

        # 活代码验证
        try:
            bc_result = bc.full_check(
                test_file=test_path if os.path.exists(test_path) else "",
                workspace_root=workspace_root,
            )
            result.backend_check_result = bc_result

            verdict = bc_result.get("overall_verdict")
            if verdict == BackendCheckVerdict.BLOCKING:
                blocking_reason = "; ".join(bc_result.get("blocking_issues", []))
                result.passed = False
                result.blocking = True
                result.details = f"活代码验证未通过: {blocking_reason}"
                result.issues.append("backend_blocking")
            elif verdict == BackendCheckVerdict.WARN:
                log.warning("活代码验证警告: %s", bc_result.get("blocking_issues", []))
        except Exception as e:
            result.issues.append(f"backend_checker: {e}")
            log.warning("活代码验证异常: %s", e)

        return result
