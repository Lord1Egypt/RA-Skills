from typing import Dict, Any


class FeatureExtractor:
    """Extract task features for mode selection."""

    @staticmethod
    def extract(task_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract features from task payload for mode selection.
        Returns a dict with:
          - parallelism_potential: float 0~1
          - total_data_size: int (bytes)
          - estimated_node_count: int
          - requires_validation: bool
        """
        text = task_payload.get("text", "")
        attachments = task_payload.get("attachments", [])

        # Simple heuristic extraction
        data_size = sum(a.get("size_bytes", 0) for a in attachments)

        # Estimate parallelism from keywords
        parallel_keywords = ["并行", "分片", "扫描", "分析", "批量", "distributed", "parallel"]
        has_parallel = any(kw in text.lower() for kw in parallel_keywords)

        return {
            "parallelism_potential": 0.9 if has_parallel else 0.3,
            "total_data_size": data_size,
            "estimated_node_count": 3,  # simplified
            "requires_validation": True,
        }
