from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from pathlib import Path
import json
from dataclasses import dataclass


@dataclass
class UnifiedMessage:
    sender: str
    content: str
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "sender": self.sender,
            "content": self.content,
            "timestamp": self.timestamp,
            "metadata": self.metadata or {}
        }


class BaseImporter(ABC):
    @abstractmethod
    def parse(self, file_path: Path) -> List[UnifiedMessage]:
        pass
    
    def import_file(self, file_path: Path, storage_path: Path) -> Dict[str, Any]:
        messages = self.parse(file_path)
        
        dest_path = storage_path / file_path.name
        import shutil
        shutil.copy2(file_path, dest_path)
        
        return {
            "success": True,
            "file_path": str(dest_path),
            "message_count": len(messages)
        }
