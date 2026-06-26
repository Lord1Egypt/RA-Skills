"""
Base classes for analysis modules.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict


# Configure logging
logger = logging.getLogger(__name__)


class AnalysisBase(ABC):
    """Abstract base class for all analysis modules."""
    
    def __init__(self):
        self.logger = logger
    
    @abstractmethod
    def analyze(self, stock_code: str, **kwargs) -> Dict:
        """
        Perform analysis.
        
        Args:
            stock_code: Stock code
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with analysis results
        """
        pass
