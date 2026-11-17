"""
AI & Agent Security Auditor.
Detects risks based on OWASP Top 10 for LLMs / Agentic Systems and SkillSpector:
- Exposure of unauthenticated local LLM inference engines (Ollama, LM Studio, etc.)
- MCP Tool Poisoning and excessive permissions
- Prompt injection patterns in prompt/context files
- AI credential exposure in environment variables
"""

from __future__ import annotations
import os
import re
import json
import logging
import socket
from pathlib import Path
from typing import List, Dict, Any, Optional

from ..models import AISecurityFinding, AIThreatType, SeverityLevel

logger = logging.getLogger(__name__)

# Standard ports used by local AI inference engines
KNOWN_LLM_SERVICES = {
    11434: ("Ollama", "Ollama local LLM inference engine"),
    1234: ("LM Studio", "LM Studio local model server"),
    8080: ("LocalAI / llama.cpp", "OpenAI-compatible local inference API"),
    8000: ("vLLM / TextGenWebUI", "High-performance LLM inference server"),
    5000: ("TextGenWebUI / KoboldAI", "Web UI and inference backend"),
}

# Instruction override and agent manipulation detection patterns
PROMPT_INJECTION_PATTERNS = [
    (re.compile(r"(?i)(ignore\s+(all\s+)?(previous|prior|above)\s+instructions)", re.IGNORECASE), "Explicit override of system instructions"),
    (re.compile(r"(?i)(you\s+are\s+now\s+in\s+unrestricted\s+mode|dan\s+mode|jailbreak)", re.IGNORECASE), "Restriction evasion or jailbreak attempt"),
    (re.compile(r"(?i)(system\s*prompt\s*override|disregard\s+system\s+prompt)", re.IGNORECASE), "System prompt override attempt"),
    (re.compile(r"[\u200B\u200C\u200D\uFEFF]", re.UNICODE), "Invisible zero-width unicode characters"),
]

# Sensitive AI environment variables that should not leak
AI_SENSITIVE_ENV_VARS = [
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GEMINI_API_KEY",
    "MISTRAL_API_KEY",
    "HUGGINGFACE_TOKEN",
    "HF_TOKEN",
    "COHERE_API_KEY",
    "GROQ_API_KEY",
]


class AIAgentSecurityAuditor:
    """Audits AI agent security, local LLM exposure, and MCP tool configuration posture."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

    def audit_all(self, target_dirs: Optional[List[Path]] = None) -> List[AISecurityFinding]:
        """Runs all AI and agent security audits."""
        findings: List[AISecurityFinding] = []
        findings.extend(self.audit_local_llm_services())
        findings.extend(self.audit_mcp_configurations())
        findings.extend(self.audit_prompt_injections(target_dirs))
        findings.extend(self.audit_environment_secrets())
        return findings

    def audit_local_llm_services(self) -> List[AISecurityFinding]:
        """Audits local LLM inference engines listening on unauthenticated interfaces."""
        findings = []
        for port, (service_name, desc) in KNOWN_LLM_SERVICES.items():
            is_local = self._check_socket("127.0.0.1", port)
            if is_local:
                try:
                    local_ip = socket.gethostbyname(socket.gethostname())
                    is_public = False
                    if local_ip and not local_ip.startswith("127."):
                        is_public = self._check_socket(local_ip, port)
                except Exception:
                    is_public = False

                if is_public:
                    findings.append(
                        AISecurityFinding(
                            threat_type=AIThreatType.UNAUTHENTICATED_LLM_SERVICE,
                            title=f"Local LLM Server {service_name} exposed to local network",
                            severity=SeverityLevel.HIGH,
                            target_component=f"{service_name} (Port {port})",
                            description=(
                                f"Service {desc} is listening on an unisolated network interface ({local_ip}:{port}). "
                                "Devices on the local network can dispatch arbitrary prompts without authentication."
                            ),
                            evidence=f"Port {port} open and reachable on {local_ip}",
                            remediation_recommendation=f"Bind {service_name} strictly to localhost / 127.0.0.1 (e.g. OLLAMA_HOST=127.0.0.1)."
                        )
                    )
        return findings

    def audit_mcp_configurations(self, search_paths: Optional[List[Path]] = None) -> List[AISecurityFinding]:
        """Audits user-provided Model Context Protocol (MCP) server definitions for excessive agency."""
        findings: List[AISecurityFinding] = []
        # Strictly inspect only if caller explicitly provides custom configuration targets
        if not search_paths:
            return findings

        for p in search_paths:
            if not p.exists() or not p.is_file():
                continue
            try:
                data = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
                servers = data.get("mcpServers", {})
                for s_name, s_cfg in servers.items():
                    cmd = s_cfg.get("command", "")
                    args = s_cfg.get("args", [])
                    if cmd in ["bash", "sh", "powershell", "pwsh", "cmd.exe", "cmd"]:
                        findings.append(
                            AISecurityFinding(
                                threat_type=AIThreatType.EXCESSIVE_AGENCY,
                                title=f"MCP Server '{s_name}' directly executes shell interpreter",
                                severity=SeverityLevel.HIGH,
                                target_component=f"MCP Server: {s_name}",
                                description="MCP server is configured to invoke raw interactive command interpreters.",
                                evidence=f"command: {cmd}, args: {' '.join(str(a) for a in args)}",
                                remediation_recommendation="Restrict the MCP server to dedicated binaries with strictly validated parameters."
                            )
                        )
            except Exception:
                pass

        return findings

    def audit_prompt_injections(self, search_paths: Optional[List[Path]] = None) -> List[AISecurityFinding]:
        """Audits agent instruction files and prompt contexts for prompt injection and override patterns."""
        findings = []
        paths_to_check = search_paths or [
            Path.home() / ".openclaw" / "workspace",
            Path.cwd()
        ]

        for base in paths_to_check:
            if not base.exists():
                continue

            candidates = []
            try:
                for ext in ["*.md", "*.txt"]:
                    for f in base.glob(ext):
                        if f.is_file() and f.stat().st_size < 100_000:
                            candidates.append(f)
            except Exception:
                pass

            for candidate in candidates:
                try:
                    content = candidate.read_text(encoding="utf-8", errors="ignore")
                    for pattern, desc in PROMPT_INJECTION_PATTERNS:
                        match = pattern.search(content)
                        if match:
                            findings.append(
                                AISecurityFinding(
                                    threat_type=AIThreatType.PROMPT_INJECTION,
                                    title=f"Potential prompt injection pattern in {candidate.name}",
                                    severity=SeverityLevel.MEDIUM,
                                    target_component=str(candidate),
                                    description=f"Agent manipulation indicator detected: {desc}.",
                                    evidence=match.group(0)[:80],
                                    remediation_recommendation="Verify origin of text content and isolate user input from system prompts."
                                )
                            )
                            break
                except Exception as e:
                    logger.debug(f"Error inspecting file {candidate}: {e}")

        return findings

    def audit_environment_secrets(self) -> List[AISecurityFinding]:
        """Audits runtime environment variables for exposed AI service provider credentials."""
        findings = []
        exposed_keys = []
        for var in AI_SENSITIVE_ENV_VARS:
            val = os.environ.get(var)
            if val and len(val) > 8:
                masked = val[:4] + "..." + val[-4:]
                exposed_keys.append(f"{var} ({masked})")

        if exposed_keys:
            findings.append(
                AISecurityFinding(
                    threat_type=AIThreatType.CREDENTIAL_EXPOSURE,
                    title="Environment variables contain readable AI service provider credentials",
                    severity=SeverityLevel.LOW,
                    target_component="Environment Variables",
                    description=(
                        f"Detected {len(exposed_keys)} environment variable(s) holding AI credentials. "
                        "Processes or untrusted tools spawned by agents may have visibility over these tokens."
                    ),
                    evidence=", ".join(exposed_keys),
                    remediation_recommendation="Use secure secret stores or restrict environment variable inheritance for subprocesses."
                )
            )

        return findings

    def _check_socket(self, host: str, port: int, timeout: float = 0.5) -> bool:
        """Performs a quick non-blocking socket connectivity check."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                return s.connect_ex((host, port)) == 0
        except Exception:
            return False
