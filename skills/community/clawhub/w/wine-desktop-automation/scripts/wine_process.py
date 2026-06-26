import subprocess
import time
import re
from typing import List, Optional, Dict
from dataclasses import dataclass
from ..utils.logger import get_logger
from ..utils.config import get_config

logger = get_logger(__name__)
config = get_config()


@dataclass
class WineProcess:
    pid: int
    name: str
    exe_path: str
    start_time: float

    def __repr__(self):
        return f'WineProcess(pid={self.pid}, name="{self.name}")'


class WineProcessManager:
    def __init__(self):
        self._wine_prefix = config.get('WINE_PREFIX', '~/.wine')

    def list_processes(self) -> List[WineProcess]:
        processes = []
        
        try:
            result = subprocess.run(
                ['ps', 'aux'],
                capture_output=True,
                text=True
            )
            
            lines = result.stdout.split('\n')
            for line in lines[1:]:
                if 'wine' in line.lower() or 'wineserver' in line.lower():
                    parts = line.split(None, 10)
                    if len(parts) >= 11:
                        pid = int(parts[1])
                        command = parts[10]
                        
                        process = WineProcess(
                            pid=pid,
                            name=self._extract_process_name(command),
                            exe_path=command,
                            start_time=0.0
                        )
                        processes.append(process)
            
            logger.info(f'Found {len(processes)} Wine processes')
            return processes
            
        except Exception as e:
            logger.error(f'Error listing Wine processes: {e}')
            return []

    def _extract_process_name(self, command: str) -> str:
        if 'wineserver' in command:
            return 'wineserver'
        elif 'explorer.exe' in command:
            return 'explorer.exe'
        elif 'notepad.exe' in command:
            return 'notepad.exe'
        else:
            match = re.search(r'(\w+\.exe)', command)
            if match:
                return match.group(1)
            return 'wine'

    def find_process(self, name: str) -> Optional[WineProcess]:
        processes = self.list_processes()
        for process in processes:
            if name.lower() in process.name.lower():
                return process
        return None

    def find_process_by_pid(self, pid: int) -> Optional[WineProcess]:
        processes = self.list_processes()
        for process in processes:
            if process.pid == pid:
                return process
        return None

    def kill(self, name: str) -> bool:
        process = self.find_process(name)
        if process:
            return self.kill_by_pid(process.pid)
        return False

    def kill_by_pid(self, pid: int) -> bool:
        try:
            subprocess.run(['kill', str(pid)], check=True)
            logger.info(f'Killed Wine process: {pid}')
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f'Failed to kill process {pid}: {e}')
            return False

    def kill_all(self) -> bool:
        try:
            processes = self.list_processes()
            for process in processes:
                self.kill_by_pid(process.pid)
            
            logger.info('Killed all Wine processes')
            return True
        except Exception as e:
            logger.error(f'Error killing all Wine processes: {e}')
            return False

    def terminate(self, name: str) -> bool:
        process = self.find_process(name)
        if process:
            return self.terminate_by_pid(process.pid)
        return False

    def terminate_by_pid(self, pid: int) -> bool:
        try:
            subprocess.run(['kill', '-TERM', str(pid)], check=True)
            logger.info(f'Terminated Wine process: {pid}')
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f'Failed to terminate process {pid}: {e}')
            return False

    def wait_for_process(self, name: str, timeout: int = 10) -> bool:
        start_time = time.time()
        while time.time() - start_time < timeout:
            process = self.find_process(name)
            if process:
                return True
            time.sleep(0.5)
        return False

    def wait_for_process_end(self, name: str, timeout: int = 30) -> bool:
        start_time = time.time()
        while time.time() - start_time < timeout:
            process = self.find_process(name)
            if not process:
                return True
            time.sleep(0.5)
        return False

    def get_process_info(self, pid: int) -> Optional[Dict]:
        try:
            result = subprocess.run(
                ['ps', '-p', str(pid), '-o', 'pid,ppid,cmd,etime,pcpu,pmem'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    parts = lines[1].split(None, 5)
                    return {
                        'pid': int(parts[0]),
                        'ppid': int(parts[1]),
                        'cmd': parts[2],
                        'elapsed': parts[3],
                        'cpu': float(parts[4]),
                        'mem': float(parts[5])
                    }
            return None
            
        except Exception as e:
            logger.error(f'Error getting process info for {pid}: {e}')
            return None

    def get_process_count(self) -> int:
        return len(self.list_processes())

    def is_running(self, name: str) -> bool:
        return self.find_process(name) is not None

    def restart_wineserver(self) -> bool:
        try:
            self.kill('wineserver')
            time.sleep(2)
            
            result = subprocess.run(
                ['wineserver', '-w'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info('Wineserver restarted successfully')
                return True
            else:
                logger.error(f'Failed to restart wineserver: {result.stderr}')
                return False
                
        except Exception as e:
            logger.error(f'Error restarting wineserver: {e}')
            return False

    def get_wine_processes_by_app(self, app_name: str) -> List[WineProcess]:
        processes = self.list_processes()
        return [p for p in processes if app_name.lower() in p.name.lower()]

    def kill_app(self, app_name: str) -> bool:
        processes = self.get_wine_processes_by_app(app_name)
        if not processes:
            logger.warning(f'No processes found for app: {app_name}')
            return False
        
        success = True
        for process in processes:
            if not self.kill_by_pid(process.pid):
                success = False
        
        return success

    def monitor_process(self, pid: int, callback=None, interval: float = 1.0) -> None:
        while True:
            process = self.find_process_by_pid(pid)
            if not process:
                logger.info(f'Process {pid} has ended')
                if callback:
                    callback(pid)
                break
            time.sleep(interval)

    def get_memory_usage(self, pid: int) -> Optional[float]:
        info = self.get_process_info(pid)
        if info:
            return info['mem']
        return None

    def get_cpu_usage(self, pid: int) -> Optional[float]:
        info = self.get_process_info(pid)
        if info:
            return info['cpu']
        return None

    def set_wine_prefix(self, prefix: str) -> None:
        self._wine_prefix = prefix
        logger.info(f'Wine prefix set to: {prefix}')

    def get_wine_prefix(self) -> str:
        return self._wine_prefix


wine_process = WineProcessManager()
