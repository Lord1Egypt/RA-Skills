import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
import json
from dotenv import load_dotenv
import yaml

# add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fetch_data import DataFetcher
from analyze import MarketAnalyzer
from generate_report import ReportGenerator
from post_to_blog import BlogPoster
from post_to_wechat import WeChatPoster
from utils.logger import setup_logger
from config import Settings

class StockReview:
    """A-share market review and analysis skill main class"""
    
    def __init__(self, 
                 config_path: Optional[str] = None,
                #  env_file: Optional[str] = None,
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize the stock review with flexible configuration options
        
        Args:
            config_path: path to YAML/JSON configuration file
            env_file: path to .env file (default: auto-discover)
            config: direct dictionary config (highest priority)
        
        Configuration priority (higher overrides lower):
            1. Direct `config` dict argument
            2. Environment variables
            3. Configuration file (YAML/JSON)
            4. Default values
        """
        self.logger = setup_logger(__name__)
        # Load environment variables from .env file if specified
        # if env_file:
        #     load_dotenv(env_file)
        #     self.logger.info(f"Loaded environment variables from: {env_file}")
        # else:
        #     # Auto-discover .env file in current directory or parent directories
        #     load_dotenv()
        #     self.logger.info("Auto-discovered and loaded .env file")
        
        # Initialize with empty config
        self.config = {}

        # Load from config file if provided
        if config_path is None:
            config_path = self._find_config_file()
        
        file_config = self._load_config_file(config_path)
        self.config.update(file_config)
        self.logger.info(f"Loaded config from: {config_path}")

        # Override with direct config dict (highest priority)
        if config:
            self.config.update(config)
            self.logger.info("Applied direct config overrides")

        # Environment variables will be used by components via os.getenv

        # Convert to Settings object
        self.config = Settings(self.config)
        
        # Initialize components
        self.data_fetcher = DataFetcher(self.config)
        self.analyzer = MarketAnalyzer(self.config)
        self.report_generator = ReportGenerator(self.config)
        self.blog_poster = BlogPoster(self.config)
        self.wechat_poster = WeChatPoster(self.config) if self.config.has_wechat else None
        
        self.logger.info("StockReview initialized successfully")

    def _find_config_file(self) -> str:
        """Find configuration file in common locations"""
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent
        
        possible_paths = [
            project_root / "config.yaml",
            current_dir / "../config.yaml",
            current_dir / "../../config.yaml",
            Path.cwd() / "config.yaml",
            Path.home() / ".stock-review" / "config.yaml",
        ]
        
        for path in possible_paths:
            if path.exists():
                self.logger.info(f"Found config at: {path}")
                return str(path)
        
        # if not found, create default config at project root
        default_path = project_root / "config.yaml"
        self._create_default_config(default_path)
        return str(default_path)

    def _load_config_file(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML or JSON file"""
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        if path.suffix in ['.yaml', '.yml']:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        elif path.suffix == '.json':
            import json
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            raise ValueError(f"Unsupported config file format: {path.suffix}")
    
    def _create_default_config(self, path: Path) -> None:
        """Create default configuration file (optional)"""
        default_config = {
            'review': {
                'markets': ['shanghai', 'shenzhen', 'hongkong'],
                'default_period': 'daily',
                'date': None,
                'force_refresh': False,
                'skip_ai_analysis': False,
                'platforms': ['hugo']
            },
            'paths': {
                'data_dir': None
            },
            'parameters': {
                'max_retries': 3,
                'request_delay': 0.5,
                'backtrack_days': 0
            },
            'models': {
                'type': 'gemini',
                'model_name': 'gemini-2.5-flash'
            }
        }
        
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(default_config, f, allow_unicode=True)
        
        self.logger.info(f"Created default config at: {path}")

    def execute(self) -> Dict[str, Any]:
        """
        Execute the full review and analysis process
        
        Args:
            None (all parameters are taken from configuration)
        
        Returns:
            execution result dictionary
        """        
        try:
            # 1. prepare parameters
            date = self.config.date
            force_refresh = self.config.force_refresh
            skip_ai_analysis = self.config.skip_ai_analysis
            platforms = self.config.platforms
            
            # 2. get latest date if not specified
            if self.config.date is None:
                date = self.data_fetcher.get_latest_date()
                self.logger.info(f"Using latest available date: {date}")
            
            # 3. get market data
            market_data = self.data_fetcher.fetch_all(date, force_refresh)
            if not market_data:
                error_msg = "Failed to fetch market data"
                self.logger.error(error_msg)
                raise Exception(error_msg)
            
            # 4. generate market summary
            market_summary = self.report_generator.create_market_summary(
                market_data, date
            )
            
            # 5. AI analysis (optional)
            ai_analysis = None
            if not skip_ai_analysis and self.config.gemini_api_key:
                ai_analysis = self.analyzer.analyze(market_summary)
                self.logger.info("AI analysis completed")
            
            # 6. generate reports
            reports = self.report_generator.generate_all(
                market_data, market_summary, ai_analysis, date
            )
            
            # 7. post to platforms
            results = {
                "date": date,
                "market_summary": market_summary[:500] + "...",  # 摘要
                "reports": list(reports.keys()),
                "published": []
            }
            
            if 'hugo' in platforms:
                post_path = self.blog_poster.create_post(
                    market_summary, ai_analysis, date
                )
                results["published"].append({
                    "platform": "hugo",
                    "path": post_path
                })
            
            if 'wechat' in platforms and self.wechat_poster:
                draft_id = self.wechat_poster.create_draft(
                    market_summary, ai_analysis, date
                )
                results["published"].append({
                    "platform": "wechat",
                    "draft_id": draft_id
                })
            
            self.logger.info(f"Stock review completed successfully for {date},\
                                summary: {market_summary[:100]}..., \
                                    published to: {[p['platform'] for p in results['published']]}")
            return results
            
        except Exception as e:
            self.logger.error(f"Execution failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def validate(self) -> bool:
        """
        Validate if the skill configuration is valid by
        checking necessary parameters and testing data fetching
        
        Returns:
            Configuration is valid
        """
        try:
            # Check necessary configuration
            if not self.config.gemini_api_key:
                self.logger.warning("GEMINI_API_KEY not set")
            
            # # Try to connect to data source
            # test_date = datetime.now().strftime("%Y%m%d")
            # self.data_fetcher.fetch_all(test_date, force_refresh=True)
            
            return True
        except Exception as e:
            self.logger.error(f"Validation failed: {str(e)}")
            return False

class PathJSONEncoder(json.JSONEncoder):
    """Path and datetime to string for JSON serialization"""
    
    def default(self, obj):
        if isinstance(obj, Path):
            return str(obj)             # convert Path to string
        if isinstance(obj, datetime):
            return obj.isoformat()      # convert datetime to ISO format string
        if hasattr(obj, '__dict__'):    # handle custom objects
            return obj.__dict__
        return super().default(obj)


if __name__ == "__main__":
    skill = StockReview()
    if skill.validate():
        result = skill.execute()
        print(json.dumps(result, ensure_ascii=False, indent=2, cls=PathJSONEncoder))
    else:
        print("Configuration validation failed. Please check the logs for details.")    