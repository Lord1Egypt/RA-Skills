import subprocess
import os
import time
from typing import Optional, List, Dict
from ..utils.logger import get_logger
from ..utils.config import get_config

logger = get_logger(__name__)
config = get_config()


class WineLauncher:
    def __init__(self):
        self._wine_path = config.get('WINE_PATH', 'wine')
        self._wine_prefix = os.path.expanduser(config.get('WINE_PREFIX', '~/.wine'))
        self._check_wine()

    def _check_wine(self):
        try:
            result = subprocess.run([self._wine_path, '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            logger.info(f'Wine version: {result.stdout.strip()}')
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.error('Wine not found or not working. Please install Wine with: sudo apt-get install wine64')
            raise RuntimeError('Wine is required but not installed or not working')

    def launch(self, executable: str, args: Optional[List[str]] = None,
               working_dir: Optional[str] = None, 
               wait: bool = False,
               timeout: Optional[int] = None) -> Optional[subprocess.Popen]:
        if not os.path.exists(executable):
            logger.error(f'Executable not found: {executable}')
            return None

        cmd = [self._wine_path, executable]
        if args:
            cmd.extend(args)

        env = os.environ.copy()
        env['WINEPREFIX'] = self._wine_prefix

        try:
            logger.info(f'Launching Wine application: {executable}')
            logger.debug(f'Command: {" ".join(cmd)}')
            
            process = subprocess.Popen(
                cmd,
                cwd=working_dir,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            if wait:
                try:
                    process.wait(timeout=timeout)
                    logger.info(f'Application finished with exit code: {process.returncode}')
                except subprocess.TimeoutExpired:
                    logger.warning(f'Application timeout after {timeout} seconds')
                    process.kill()
                    return None

            return process

        except Exception as e:
            logger.error(f'Failed to launch application: {e}')
            return None

    def launch_with_config(self, executable: str, 
                          config_options: Dict[str, str],
                          args: Optional[List[str]] = None,
                          working_dir: Optional[str] = None) -> Optional[subprocess.Popen]:
        cmd = [self._wine_path]
        
        for key, value in config_options.items():
            cmd.extend([key, value])
        
        cmd.append(executable)
        if args:
            cmd.extend(args)

        env = os.environ.copy()
        env['WINEPREFIX'] = self._wine_prefix

        try:
            logger.info(f'Launching Wine application with config: {executable}')
            logger.debug(f'Command: {" ".join(cmd)}')
            
            process = subprocess.Popen(
                cmd,
                cwd=working_dir,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            return process

        except Exception as e:
            logger.error(f'Failed to launch application with config: {e}')
            return None

    def launch_explorer(self) -> Optional[subprocess.Popen]:
        return self.launch('explorer.exe')

    def launch_notepad(self) -> Optional[subprocess.Popen]:
        return self.launch('notepad.exe')

    def launch_cmd(self) -> Optional[subprocess.Popen]:
        return self.launch('cmd.exe')

    def launch_control_panel(self) -> Optional[subprocess.Popen]:
        return self.launch('control.exe')

    def launch_taskmgr(self) -> Optional[subprocess.Popen]:
        return self.launch('taskmgr.exe')

    def launch_mspaint(self) -> Optional[subprocess.Popen]:
        return self.launch('mspaint.exe')

    def launch_calc(self) -> Optional[subprocess.Popen]:
        return self.launch('calc.exe')

    def launch_regedit(self) -> Optional[subprocess.Popen]:
        return self.launch('regedit.exe')

    def launch_uninstaller(self) -> Optional[subprocess.Popen]:
        return self.launch('uninstaller.exe')

    def launch_winecfg(self) -> Optional[subprocess.Popen]:
        try:
            logger.info('Launching winecfg')
            process = subprocess.Popen(
                ['winecfg'],
                env={'WINEPREFIX': self._wine_prefix}
            )
            return process
        except Exception as e:
            logger.error(f'Failed to launch winecfg: {e}')
            return None

    def launch_winefile(self) -> Optional[subprocess.Popen]:
        return self.launch('winefile.exe')

    def launch_with_virtual_desktop(self, executable: str,
                                   desktop_size: str = '1024x768',
                                   args: Optional[List[str]] = None,
                                   working_dir: Optional[str] = None) -> Optional[subprocess.Popen]:
        config_options = {
            'explorer.exe': '/desktop=Wine,' + desktop_size
        }
        return self.launch_with_config(executable, config_options, args, working_dir)

    def set_wine_prefix(self, prefix: str) -> None:
        self._wine_prefix = os.path.expanduser(prefix)
        logger.info(f'Wine prefix set to: {self._wine_prefix}')

    def get_wine_prefix(self) -> str:
        return self._wine_prefix

    def get_wine_path(self) -> str:
        return self._wine_path

    def create_prefix(self, prefix: Optional[str] = None) -> bool:
        if prefix:
            self.set_wine_prefix(prefix)
        
        try:
            os.makedirs(self._wine_prefix, exist_ok=True)
            
            result = subprocess.run(
                [self._wine_path, 'wineboot', '--init'],
                env={'WINEPREFIX': self._wine_prefix},
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f'Wine prefix created: {self._wine_prefix}')
                return True
            else:
                logger.error(f'Failed to create Wine prefix: {result.stderr}')
                return False
                
        except Exception as e:
            logger.error(f'Error creating Wine prefix: {e}')
            return False

    def run_command(self, command: str, args: Optional[List[str]] = None,
                   working_dir: Optional[str] = None) -> Optional[str]:
        cmd = [self._wine_path, command]
        if args:
            cmd.extend(args)

        env = os.environ.copy()
        env['WINEPREFIX'] = self._wine_prefix

        try:
            logger.debug(f'Running Wine command: {" ".join(cmd)}')
            result = subprocess.run(
                cmd,
                cwd=working_dir,
                env=env,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return result.stdout
            else:
                logger.error(f'Command failed: {result.stderr}')
                return None
                
        except Exception as e:
            logger.error(f'Error running command: {e}')
            return None

    def install_font(self, font_path: str) -> bool:
        if not os.path.exists(font_path):
            logger.error(f'Font file not found: {font_path}')
            return False

        fonts_dir = os.path.join(self._wine_prefix, 'drive_c/windows/Fonts')
        os.makedirs(fonts_dir, exist_ok=True)
        
        try:
            import shutil
            shutil.copy(font_path, fonts_dir)
            logger.info(f'Font installed: {font_path}')
            return True
        except Exception as e:
            logger.error(f'Failed to install font: {e}')
            return False


wine_launcher = WineLauncher()
