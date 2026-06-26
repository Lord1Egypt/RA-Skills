from dataclasses import dataclass
from typing import Literal

SourceType = Literal["gmail_thread", "google_doc", "whatsapp_export"]
IngestionStatus = Literal["stub", "completed", "completed_with_warnings", "failed"]


@dataclass(slots=True)
class IngestionResult:
    source_type: SourceType
    status: IngestionStatus
    detail: str
    run_id: str | None = None
