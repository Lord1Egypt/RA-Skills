# =============================================================================
# modbus.py — Modbus RTU 底层驱动
# 只负责：收发字节、CRC校验、拆分报文。不含业务逻辑。
# =============================================================================

from machine import UART
import ubinascii
import utime


class ModbusRTU:
    """
    Modbus RTU 主机驱动。
    封装串口读写、CRC 计算和报文拆分，供上层业务代码调用。
    """

    def __init__(self, uart_n, baud, bits, parity, stop, flow):
        """
        初始化串口。参数含义同 machine.UART 构造函数。

        参数:
            uart_n : UART 通道号（如 UART.UART2 = 2）
            baud   : 波特率（如 9600）
            bits   : 数据位（如 8）
            parity : 校验位（0=无, 1=偶, 2=奇）
            stop   : 停止位（1 或 2）
            flow   : 流控（0=无, 1=硬件流控）
        """
        self.uart = UART(uart_n, baud, bits, parity, stop, flow)

    # ── 内部工具 ──────────────────────────────────────────────────────────────

    @staticmethod
    def _split_u16(val):
        """把 16 位整数拆成 (高字节, 低字节)。"""
        high, low = divmod(val, 0x100)
        return high, low

    def _crc16(self, data: bytearray):
        """
        计算 Modbus CRC16，返回 (低字节, 高字节)。
        注意 Modbus 报文中 CRC 低字节在前。
        """
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        # 转成小端顺序：低字节 | 高字节
        return (crc & 0xFF), (crc >> 8)

    def _send(self, data: bytearray):
        """追加 CRC 后通过串口发送，发送后等待 200ms 让从机响应。"""
        crc_lo, crc_hi = self._crc16(data)
        data.append(crc_lo)
        data.append(crc_hi)
        print("[Modbus TX]", ubinascii.hexlify(data, " "))
        self.uart.write(data)
        utime.sleep_ms(200)

    def _recv(self):
        """
        等待串口数据（最多重试 5 次，每次 100ms）。
        返回原始 bytes，或空 bytes（超时）。
        """
        for _ in range(5):
            n = self.uart.any()
            if n > 0:
                raw = self.uart.read(n)
                print("[Modbus RX]", ubinascii.hexlify(raw, " "))
                return raw
            utime.sleep_ms(100)
        return b""

    def _recv_hex_list(self):
        """
        读取串口并拆分为十六进制字符串列表。
        例如返回 [b'01', b'03', b'02', b'00', b'05', b'xx', b'xx']
        """
        raw = self._recv()
        return ubinascii.hexlify(raw, ",").split(b",")

    # ── 公开接口 ──────────────────────────────────────────────────────────────

    def read_regs(self, slave, start_addr, reg_count):
        """
        发送 FC=03 读保持寄存器命令，返回解析结果。

        参数:
            slave      : 从机地址
            start_addr : 起始寄存器地址（整数）
            reg_count  : 读取寄存器个数

        返回:
            {
                "ok"  : True/False,         # 是否成功
                "data": [hex_str, ...]       # 原始字节十六进制列表（不含头尾）
            }
        """
        ah, al = self._split_u16(start_addr)
        qh, ql = self._split_u16(reg_count)
        self._send(bytearray([slave, 0x03, ah, al, qh, ql]))

        hex_list = self._recv_hex_list()

        # 最小有效帧长度：从机地址(1)+功能码(1)+字节数(1)+数据(reg_count*2)+CRC(2)
        expected_len = reg_count * 2 + 5
        try:
            func_code = int(hex_list[1], 16)
            if func_code > 0x10:                       # 错误响应（0x83 等异常码）
                print("[Modbus] 从机返回异常码:", hex(func_code))
                return {"ok": False, "data": []}

            byte_count = int(hex_list[2], 16)
            if byte_count != reg_count * 2:
                print("[Modbus] 数据字节数不符，期望", reg_count * 2, "实得", byte_count)
                return {"ok": False, "data": []}

            if len(hex_list) < expected_len:
                print("[Modbus] 报文太短，期望", expected_len, "实得", len(hex_list))
                return {"ok": False, "data": []}

            # 数据区：跳过地址/功能码/字节数，去掉末尾 CRC 两字节
            payload = hex_list[3 : 3 + byte_count]
            return {"ok": True, "data": [b.decode() for b in payload]}

        except Exception as e:
            print("[Modbus] 解析失败:", e)
            return {"ok": False, "data": []}

    def write_regs(self, slave, start_addr, byte_vals):
        """
        发送 FC=16 写多个寄存器命令，返回结果。

        参数:
            slave      : 从机地址
            start_addr : 起始寄存器地址
            byte_vals  : 要写入的字节列表（每个寄存器 2 字节，低位在前）

        返回:
            {"ok": True/False, "reg_count": int}
        """
        ah, al = self._split_u16(start_addr)
        reg_count = len(byte_vals) // 2
        rh, rl = self._split_u16(reg_count)
        header = bytearray([slave, 0x10, ah, al, rh, rl, len(byte_vals)])
        self._send(header + bytearray(byte_vals))

        hex_list = self._recv_hex_list()
        try:
            func_code = int(hex_list[1], 16)
            if func_code != 0x10:                      # FC=16 正常响应为 0x10 (16)
                print("[Modbus] 写寄存器异常响应:", hex(func_code))
                return {"ok": False, "reg_count": 0}
            return {"ok": True, "reg_count": int(hex_list[2], 16)}
        except Exception as e:
            print("[Modbus] 写寄存器响应解析失败:", e)
            return {"ok": False, "reg_count": 0}
