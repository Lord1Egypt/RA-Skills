"""
Base classes for data sources and analysis.
"""

import os
import logging
from abc import ABC, abstractmethod
from typing import Dict, Optional


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataSourceBase(ABC):
    """Abstract base class for all data sources."""
    
    def __init__(self):
        self.logger = logger
    
    @abstractmethod
    def get_quote(self, symbol: str) -> Dict:
        """
        Get real-time quote.
        
        Args:
            symbol: Stock symbol or code
            
        Returns:
            Dictionary with quote data
        """
        pass
    
    @abstractmethod
    def get_history(self, symbol: str, period: str = '6mo') -> Dict:
        """
        Get historical data.
        
        Args:
            symbol: Stock symbol or code
            period: Time period
            
        Returns:
            Dictionary with historical data
        """
        pass


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
