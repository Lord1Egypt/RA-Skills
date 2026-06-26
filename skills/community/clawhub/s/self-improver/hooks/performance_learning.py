"""
Self-Improving Agent - Performance Learning Hook

This hook learns from performance metrics to optimize performance.
"""

import json
from pathlib import Path
from datetime import datetime


class PerformanceLearningHook:
    """Hook for learning from performance metrics."""
    
    def __init__(self):
        self.workspace = Path(__file__).parent.parent
        self.performance_log = self.workspace / 'learnings' / 'performance.json'
        
        # Ensure learnings directory exists
        self.performance_log.parent.mkdir(parents=True, exist_ok=True)
        
    def onPerformanceMetric(self, metric):
        """
        Called when a performance metric is collected.
        Learn from performance to optimize future performance.
        """
        print("📊 Learning from performance metric...")
        
        performance_data = {
            'timestamp': datetime.now().isoformat(),
            'metric_type': self._extract_metric_type(metric),
            'metric_value': self._extract_metric_value(metric),
            'context': self._extract_context(metric),
            'optimization': self._extract_optimization(metric)
        }
        
        # Log the performance metric
        self._log_performance(performance_data)
        
        print(f"✅ Saved performance learning")
    
    def _extract_metric_type(self, metric):
        """Extract metric type from metric object."""
        if isinstance(metric, dict):
            return metric.get('type', 'unknown')
        return 'unknown'
    
    def _extract_metric_value(self, metric):
        """Extract metric value from metric object."""
        if isinstance(metric, dict):
            return metric.get('value', 0)
        return metric if isinstance(metric, (int, float)) else 0
    
    def _extract_context(self, metric):
        """Extract context from metric object."""
        if isinstance(metric, dict):
            return {
                'timestamp': metric.get('timestamp'),
                'operation': metric.get('operation'),
                'duration': metric.get('duration')
            }
        return {}
    
    def _extract_optimization(self, metric):
        """Extract optimization suggestion from metric."""
        suggestions = []
        
        # Analyze performance and suggest optimizations
        if isinstance(metric, dict):
            duration = metric.get('duration', 0)
            if duration > 1000:  # If slower than 1 second
                suggestions.append('Consider caching or optimization')
        
        return suggestions
    
    def _log_performance(self, performance_data):
        """Log performance metric to file."""
        performances = self._load_performances()
        performances.append(performance_data)
        self._save_performances(performances)
    
    def _load_performances(self):
        """Load performances from file."""
        if self.performance_log.exists():
            with open(self.performance_log, 'r') as f:
                return json.load(f)
        return []
    
    def _save_performances(self, performances):
        """Save performances to file."""
        with open(self.performance_log, 'w') as f:
            json.dump(performances, f, indent=2)


# Create global instance
performance_learning_hook = PerformanceLearningHook()


# Export functions for hook system
def apply():
    """Apply the hook (initialization)."""
    print("🪝 PerformanceLearningHook initialized")


def onPerformanceMetric(metric):
    """Called when a performance metric is collected."""
    performance_learning_hook.onPerformanceMetric(metric)
