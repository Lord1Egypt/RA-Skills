"""TIA Openness核心封装，基于pythonnet调用.NET API"""

import clr
import sys
from typing import Optional, List, Dict, Any
import logging
from .utils import get_openness_dll_path

logger = logging.getLogger(__name__)

class TiaPortal:
    """TIA Portal实例封装"""

    def __init__(self, tia_version: str = "V18", mode: str = "WithUserInterface"):
        """
        初始化TIA Portal连接
        :param tia_version: TIA版本，如 "V16","V17","V18"
        :param mode: 启动模式，"WithUserInterface" 或 "WithoutUserInterface"
        """
        self.tia_version = tia_version
        self.mode = mode
        self._portal = None
        self._project = None
        self._load_assemblies()

    def _load_assemblies(self):
        """加载Openness程序集"""
        try:
            eng_dll, hmi_dll = get_openness_dll_path(self.tia_version)
            clr.AddReference(eng_dll)
            clr.AddReference(hmi_dll)

            from Siemens.Engineering import TiaPortal as TiaPortalNet, TiaPortalMode
            from Siemens.Engineering import TiaPortalProcess
            from Siemens.Engineering.HW import Device, DeviceItem
            from Siemens.Engineering.SW.Blocks import PlcBlock, PlcBlockType, PlcProgrammingLanguage, ICompilable
            from Siemens.Engineering.SW.Tags import PlcTagTable, PlcTag
            from Siemens.Engineering.SW.Types import PlcType
            from Siemens.Engineering.Compiler import CompilerResultState
            from Siemens.Engineering.Online import OnlineProvider
            from Siemens.Engineering.Download import DownloadProvider, DownloadOptions
            from Siemens.Engineering.Connection import ConnectionConfiguration
            from Siemens.Engineering.HW.Features import SoftwareContainer

            self.TiaPortalNet = TiaPortalNet
            self.TiaPortalMode = TiaPortalMode
            self.TiaPortalProcess = TiaPortalProcess
            self.Device = Device
            self.DeviceItem = DeviceItem
            self.PlcBlock = PlcBlock
            self.PlcBlockType = PlcBlockType
            self.PlcProgrammingLanguage = PlcProgrammingLanguage
            self.ICompilable = ICompilable
            self.PlcTagTable = PlcTagTable
            self.PlcTag = PlcTag
            self.PlcType = PlcType
            self.CompilerResultState = CompilerResultState
            self.OnlineProvider = OnlineProvider
            self.DownloadProvider = DownloadProvider
            self.DownloadOptions = DownloadOptions
            self.ConnectionConfiguration = ConnectionConfiguration
            self.SoftwareContainer = SoftwareContainer

            logger.info(f"成功加载TIA Openness {self.tia_version} 程序集")
        except Exception as e:
            logger.error(f"加载Openness程序集失败: {e}")
            raise

    def start(self):
        """启动或附加到TIA Portal"""
        processes = self.TiaPortalProcess.GetProcesses()
        if len(processes) > 0:
            self._portal = processes[0].Attach()
            logger.info("已附加到运行中的TIA Portal进程")
        else:
            mode_map = {
                "WithUserInterface": self.TiaPortalMode.WithUserInterface,
                "WithoutUserInterface": self.TiaPortalMode.WithoutUserInterface
            }
            self._portal = self.TiaPortalNet(mode_map.get(self.mode, self.TiaPortalMode.WithUserInterface))
            logger.info("已启动新的TIA Portal实例")

    def close(self):
        """关闭TIA Portal连接"""
        if self._portal:
            self._portal.Dispose()
            self._portal = None
            self._project = None
            logger.info("TIA Portal连接已关闭")

    @property
    def portal(self):
        if self._portal is None:
            self.start()
        return self._portal

    @property
    def project(self):
        return self._project

    # ---------- 项目操作 ----------
    def create_project(self, path: str, name: str, author: str = "", comment: str = ""):
        """创建新项目"""
        from System.IO import DirectoryInfo
        from Siemens.Engineering import ProjectInfo

        proj_info = ProjectInfo()
        proj_info.Name = name
        proj_info.Path = DirectoryInfo(path)
        proj_info.Author = author
        proj_info.Comment = comment

        self._project = self.portal.Projects.Create(proj_info)
        logger.info(f"项目创建成功: {path}\\{name}")
        return self._project

    def open_project(self, project_path: str, user: Optional[str] = None, password: Optional[str] = None):
        """打开现有项目，支持UMAC认证"""
        from System.IO import FileInfo
        from System import Security

        def handle_auth(sender, args):
            if user and password:
                ss = Security.SecureString()
                for ch in password:
                    ss.AppendChar(ch)
                creds = args.UmacCredentials
                creds.Type = self._get_enum("UmacUserType", "Project")
                creds.Name = user
                creds.SetPassword(ss)

        if user and password:
            self.portal.Authentication += handle_auth

        file_info = FileInfo(project_path)
        self._project = self.portal.Projects.Open(file_info)
        logger.info(f"项目打开成功: {project_path}")
        return self._project

    def save_project(self):
        """保存项目"""
        if self._project:
            self._project.Save()
            logger.info("项目已保存")
            return True
        return False

    def close_project(self):
        """关闭项目（不保存）"""
        if self._project:
            self._project.Close()
            self._project = None
            logger.info("项目已关闭")
            return True
        return False

    # ---------- 硬件操作 ----------
    def add_plc_device(self, device_name: str, catalog_path: str, firmware: str = "V4.0"):
        """
        添加PLC设备
        :param device_name: 设备名称，如 "PLC_1"
        :param catalog_path: 硬件目录路径，如 "SIMATIC.PLC.S71500.CPU 1511-1 PN"
        :param firmware: 固件版本，如 "V4.0"
        :return: 设备对象
        """
        identifier = f"{catalog_path}/{firmware}"
        device_info = self.portal.HardwareCatalog.Find(identifier)
        if device_info is None:
            raise Exception(f"未找到硬件设备: {identifier}")
        device = self._project.Devices.CreateWithItem(device_info, device_name)
        logger.info(f"添加PLC设备: {device_name} ({catalog_path})")
        return device

    def get_plc_software(self, device_name: str):
        """获取PLC软件对象"""
        for device in self._project.Devices:
            if device.Name == device_name:
                for item in device.DeviceItems:
                    if "PLCSoftware" in item.Classification.ToString():
                        sc = item.GetService(self.SoftwareContainer)
                        if sc:
                            return sc.Software
        raise Exception(f"未找到PLC软件: {device_name}")

    # ---------- 程序块操作 ----------
    def create_block(self, plc_software, block_type: str, name: str,
                     number: int = 0, language: str = "SCL", code: str = None):
        """
        创建程序块
        :param block_type: "OB", "FB", "FC", "DB"
        :param name: 块名称
        :param number: 编号（0表示自动）
        :param language: 编程语言（SCL/LAD/FBD）
        :param code: SCL代码内容
        """
        type_map = {
            "OB": self.PlcBlockType.OB,
            "FB": self.PlcBlockType.FB,
            "FC": self.PlcBlockType.FC,
            "DB": self.PlcBlockType.GlobalDB
        }
        lang_map = {
            "SCL": self.PlcProgrammingLanguage.SCL,
            "LAD": self.PlcProgrammingLanguage.LAD,
            "FBD": self.PlcProgrammingLanguage.FBD
        }
        block_group = plc_software.BlockGroup
        if number > 0:
            block = block_group.Blocks.CreateBlock(type_map[block_type], lang_map[language], name, number)
        else:
            block = block_group.Blocks.CreateBlock(type_map[block_type], lang_map[language], name)
        if code:
            block.Code.SetText(code)
        logger.info(f"创建块: {block_type} {name} (编号: {number if number else '自动'})")
        return block

    # ---------- 编译 ----------
    def compile_plc(self, plc_software) -> tuple:
        """编译PLC软件，返回 (成功标志, 消息列表)"""
        compile_service = plc_software.GetService(self.ICompilable)
        result = compile_service.Compile()
        msgs = [msg.Text for msg in result.Messages]
        if result.State == self.CompilerResultState.Success:
            logger.info("编译成功")
            return True, msgs
        else:
            logger.error(f"编译失败: {result.State}")
            return False, msgs

    # ---------- 下载 ----------
    def download_to_plc(self, plc_software, interface: str = "PN/IE",
                        ip_address: str = None, password: Optional[str] = None):
        """
        下载到PLC
        :param interface: 接口类型，如 "PN/IE"
        :param ip_address: PLC的IP地址（如果与项目中配置不同）
        :param password: PLC保护密码
        """
        from Siemens.Engineering.Download.Configurations import DownloadPasswordConfiguration
        from System import Security

        # 获取下载服务
        device_item = plc_software.Parent.Parent  # 获取PLC的DeviceItem
        download_provider = device_item.GetService(self.DownloadProvider)
        if download_provider is None:
            raise Exception("无法获取下载服务")

        # 配置连接
        conn_config = download_provider.Configuration
        mode = conn_config.Modes.Find(interface)
        if mode is None:
            raise Exception(f"未找到接口模式: {interface}")
        pc_interface = mode.PcInterfaces[0]  # 简化：取第一个
        if ip_address:
            # 使用指定IP
            target_config = pc_interface.Addresses.Create(ip_address)
        else:
            target_config = pc_interface.TargetInterfaces[0]

        # 设置下载选项
        options = self.DownloadOptions.Hardware | self.DownloadOptions.Software

        # 定义回调处理密码等
        def pre_download(config):
            if isinstance(config, DownloadPasswordConfiguration) and password:
                ss = Security.SecureString()
                for ch in password:
                    ss.AppendChar(ch)
                config.SetPassword(ss)

        result = download_provider.Download(target_config, pre_download, None, options)
        if result.State == self.CompilerResultState.Success:
            logger.info("下载成功")
            return True, "下载成功"
        else:
            msgs = [msg.Message for msg in result.Messages]
            return False, msgs

    # ---------- 辅助 ----------
    def _get_enum(self, enum_type_name: str, value_name: str):
        """获取.NET枚举值"""
        try:
            from Siemens.Engineering import UmacUserType
            if enum_type_name == "UmacUserType":
                return getattr(UmacUserType, value_name)
        except:
            pass
        raise ValueError(f"无法获取枚举 {enum_type_name}.{value_name}")