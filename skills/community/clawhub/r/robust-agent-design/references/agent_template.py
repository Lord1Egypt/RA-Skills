#!/usr/bin/env python3
"""
Robust Agent Design Pattern - Complete Template Implementation
"""

import uuid
import json
import time
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, Callable, List
from enum import Enum


class AgentState(Enum):
    """Agent State Enumeration"""
    INITIALIZED = "initialized"
    WAITING = "waiting_for_input"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    COMPENSATING = "compensating"


class RobustAgentException(Exception):
    """Base Agent Exception"""
    pass


class TransientError(RobustAgentException):
    """Transient Fault Exception"""
    pass


class ResourceExhaustedError(RobustAgentException):
    """Resource Fault Exception"""
    pass


class BusinessLogicError(RobustAgentException):
    """Logic Fault Exception"""
    pass


class RobustAgent:
    """
    Robust Agent Base Class
    
    Features:
    - State-driven design
    - Three-level fault handling
    - Compensation transaction support
    - State persistence
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.id = str(uuid.uuid4())
        self.name = config.get('name', 'UnnamedAgent')
        self.state = AgentState.INITIALIZED
        
        # Retry configuration
        self.retry_count = 0
        self.max_retries = config.get('max_retries', 3)
        self.backoff_strategy = config.get('backoff_strategy', 'exponential')
        self.base_delay = config.get('base_delay', 1.0)
        
        # State persistence
        self.state_persistence = config.get('state_persistence', 'file')
        self.state_file = config.get('state_file', f'/tmp/agent_{self.id}.state')
        
        # Compensation transactions
        self.compensation_actions: List[Dict] = []
        
        # Monitoring
        self.metrics = {
            'start_time': None,
            'end_time': None,
            'retry_attempts': 0,
            'errors': []
        }
        
        # Input/Output
        self.input_data: Optional[Any] = None
        self.output_data: Optional[Any] = None
    
    def _persist_state(self):
        """Persist state"""
        state_data = {
            'agent_id': self.id,
            'agent_name': self.name,
            'state': self.state.value,
            'retry_count': self.retry_count,
            'metrics': self.metrics,
            'input_checksum': self._compute_checksum(self.input_data),
            'timestamp': datetime.now().isoformat()
        }
        
        if self.state_persistence == 'file':
            with open(self.state_file, 'w') as f:
                json.dump(state_data, f, indent=2)
        elif self.state_persistence == 'memory':
            # In-memory storage for testing
            self._memory_state = state_data
    
    def _load_state(self) -> Optional[Dict]:
        """Load state"""
        if self.state_persistence == 'file':
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except FileNotFoundError:
                return None
        elif self.state_persistence == 'memory':
            return getattr(self, '_memory_state', None)
        return None
    
    def _compute_checksum(self, data: Any) -> str:
        """Compute data checksum"""
        import hashlib
        if data is None:
            return ""
        data_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.md5(data_str.encode()).hexdigest()[:8]
    
    async def _exponential_backoff(self, attempt: int):
        """Exponential backoff"""
        if self.backoff_strategy == 'exponential':
            delay = self.base_delay * (2 ** (attempt - 1))
        elif self.backoff_strategy == 'linear':
            delay = self.base_delay * attempt
        else:  # fixed
            delay = self.base_delay
        
        print(f"  ⏱️  Waiting {delay:.1f} seconds before retry...")
        await asyncio.sleep(delay)
    
    def _is_transient_error(self, error: Exception) -> bool:
        """Check if error is transient"""
        transient_errors = [
            'timeout', 'connection', 'temporarily unavailable',
            'rate limit', '503', '502', '504'
        ]
        error_str = str(error).lower()
        return any(te in error_str for te in transient_errors)
    
    def _is_resource_error(self, error: Exception) -> bool:
        """Check if error is resource-related"""
        resource_errors = [
            'disk full', 'memory', 'quota exceeded',
            'no space', 'resource exhausted'
        ]
        error_str = str(error).lower()
        return any(re in error_str for re in resource_errors)
    
    async def _cleanup_resources(self):
        """Clean up resources"""
        print(f"  🧹 Cleaning up resources...")
        # Can be overridden by subclasses
        pass
    
    async def _execute_compensation(self):
        """Execute compensation actions"""
        if not self.compensation_actions:
            return
        
        print(f"  🔄 Executing compensation ({len(self.compensation_actions)} actions)...")
        for action in self.compensation_actions:
            try:
                await action['func'](**action.get('params', {}))
            except Exception as e:
                print(f"    ⚠️ Compensation action failed: {e}")
    
    def add_compensation_action(self, func: Callable, params: Dict = None):
        """Add compensation action"""
        self.compensation_actions.append({
            'func': func,
            'params': params or {}
        })
    
    async def _do_work(self, task: Any) -> Any:
        """
        Actual work logic - must be overridden by subclasses
        """
        raise NotImplementedError("Subclasses must implement _do_work method")
    
    async def _validate_result(self, result: Any) -> bool:
        """
        Validate result - can be overridden by subclasses
        """
        return result is not None
    
    async def _handle_failure(self, error: Exception, task: Any) -> Any:
        """
        Fault handling logic
        """
        self.metrics['errors'].append({
            'time': datetime.now().isoformat(),
            'error': str(error),
            'type': type(error).__name__
        })
        
        # L1: Transient fault - retry
        if self._is_transient_error(error) and self.retry_count < self.max_retries:
            self.retry_count += 1
            self.metrics['retry_attempts'] = self.retry_count
            print(f"  🔄 L1 Fault Handling: Transient fault, retry {self.retry_count}...")
            await self._exponential_backoff(self.retry_count)
            return await self.execute(task)
        
        # L2: Resource fault - cleanup and reset
        if self._is_resource_error(error):
            print(f"  🔄 L2 Fault Handling: Resource fault, cleaning up...")
            await self._cleanup_resources()
            self.state = AgentState.WAITING
            self._persist_state()
            raise ResourceExhaustedError(f"Resource fault: {error}")
        
        # L3: Logic fault - compensation
        print(f"  🔄 L3 Fault Handling: Logic fault, executing compensation...")
        self.state = AgentState.FAILED
        self._persist_state()
        await self._execute_compensation()
        raise BusinessLogicError(f"Logic fault: {error}")
    
    async def execute(self, task: Any) -> Any:
        """
        Main execution entry point
        """
        self.input_data = task
        self.metrics['start_time'] = datetime.now().isoformat()
        
        try:
            # 1. State transition
            self.state = AgentState.PROCESSING
            self._persist_state()
            print(f"🚀 Agent [{self.name}] starting execution...")
            
            # 2. Execute work
            result = await self._do_work(task)
            
            # 3. Validate result
            is_valid = await self._validate_result(result)
            if not is_valid:
                raise BusinessLogicError("Result validation failed")
            
            # 4. Complete state
            self.output_data = result
            self.state = AgentState.COMPLETED
            self.metrics['end_time'] = datetime.now().isoformat()
            self._persist_state()
            
            print(f"✅ Agent [{self.name}] execution successful")
            return result
            
        except Exception as error:
            # 5. Fault handling
            return await self._handle_failure(error, task)
    
    def get_status(self) -> Dict[str, Any]:
        """Get Agent status"""
        return {
            'id': self.id,
            'name': self.name,
            'state': self.state.value,
            'retry_count': self.retry_count,
            'metrics': self.metrics
        }


# ==================== Usage Examples ====================

class CrawlerAgent(RobustAgent):
    """Crawler Agent Example"""
    
    async def _do_work(self, task: Dict) -> Dict:
        """Simulate crawling work"""
        url = task.get('url')
        print(f"  📡 Crawling: {url}")
        
        # Simulate network request
        await asyncio.sleep(0.5)
        
        # Simulate random failure (for testing)
        import random
        if random.random() < 0.3:  # 30% failure rate
            raise Exception("Connection timeout")
        
        return {
            'url': url,
            'title': f"Title-{url}",
            'content': f"Content-{url}",
            'timestamp': datetime.now().isoformat()
        }


class ProcessorAgent(RobustAgent):
    """Processor Agent Example"""
    
    async def _do_work(self, task: Dict) -> Dict:
        """Simulate processing work"""
        print(f"  🔄 Processing: {task.get('title')}")
        
        await asyncio.sleep(0.3)
        
        # Add processing marker
        task['processed'] = True
        task['processed_at'] = datetime.now().isoformat()
        
        return task
    
    async def _validate_result(self, result: Dict) -> bool:
        """Validate processing result"""
        return result.get('processed') is True


# ==================== Test Code ====================

async def main():
    """Test Agent workflow"""
    print("=" * 60)
    print("Robust Agent Design Pattern - Test")
    print("=" * 60)
    print()
    
    # Create Agents
    crawler = CrawlerAgent({
        'name': 'CrawlerAgent',
        'max_retries': 3,
        'backoff_strategy': 'exponential'
    })
    
    processor = ProcessorAgent({
        'name': 'ProcessorAgent',
        'max_retries': 2
    })
    
    # Execute tasks
    try:
        # Step 1: Crawl
        raw_data = await crawler.execute({'url': 'https://example.com/info'})
        print(f"Crawl result: {raw_data}")
        print()
        
        # Step 2: Process
        processed_data = await processor.execute(raw_data)
        print(f"Process result: {processed_data}")
        print()
        
    except Exception as e:
        print(f"❌ Workflow failed: {e}")
    
    # Print status
    print("=" * 60)
    print("Agent Status:")
    print(f"  Crawler Agent: {crawler.get_status()}")
    print(f"  Processor Agent: {processor.get_status()}")


if __name__ == '__main__':
    asyncio.run(main())
