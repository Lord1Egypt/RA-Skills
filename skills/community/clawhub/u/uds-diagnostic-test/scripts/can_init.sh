#!/bin/bash
# CAN 接口初始化脚本 — 支持 Linux SocketCAN (原生/WSL2)
# 唯一入口，所有 CAN 初始化统一经过此处
# 用法:
#   默认 (CAN FD): bash can_init.sh
#                  bash can_init.sh --bitrate 500000 --dbitrate 2000000
#   Classic CAN:  bash can_init.sh --classic
#   强制释放占用: bash can_init.sh --force
# 默认值:
#   默认 CAN FD:  bitrate=500000(仲裁段), dbitrate=2000000(数据段), sp=0.800(仲裁段采样点), dsp=0.800(数据段采样点)
#   指定 --classic: bitrate=500000, sp=0.800
# 支持驱动: peak_usb, gs_usb, mttcan, kvaser_usb, ems_usb, esd_usb2, vcan

CHANNEL="can0"
FD_MODE=true
BITRATE=500000
DBITRATE=2000000
SAMPLE_POINT=0.800
DSAMPLE_POINT=0.800
FORCE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --classic) FD_MODE=false; shift ;;
        --fd|-f) FD_MODE=true; shift ;;
        --channel|-c) CHANNEL="$2"; shift 2 ;;
        --bitrate|-b) BITRATE="$2"; shift 2 ;;
        --dbitrate|-d) DBITRATE="$2"; shift 2 ;;
        --sp|-s) SAMPLE_POINT="$2"; shift 2 ;;
        --dsp) DSAMPLE_POINT="$2"; shift 2 ;;
        --force) FORCE=true; shift ;;
        --help|-h)
            echo "用法: can_init.sh [选项]"
            echo ""
            echo "=== 默认 (CAN FD, 向下兼容 Classic CAN) ==="
            echo "  bash can_init.sh"
            echo "  bash can_init.sh --bitrate 500000 --dbitrate 2000000"
            echo ""
            echo "=== Classic CAN (仅旧硬件) ==="
            echo "  bash can_init.sh --classic"
            echo "  bash can_init.sh --classic --bitrate 500000 --sp 0.800"
            echo ""
            echo "=== 其他 ==="
            echo "  bash can_init.sh --channel can1               # 指定通道"
            echo "  bash can_init.sh --force                       # 强制释放占用后初始化"
            echo ""
            echo "支持驱动: peak_usb | gs_usb | mttcan | kvaser_usb | ems_usb | esd_usb2"
            echo ""
            echo "默认值:"
            echo "  默认 CAN FD:  bitrate=500000(仲裁段), dbitrate=2000000(数据段)"
            echo "               sp=0.800(仲裁段采样点), dsp=0.800(数据段采样点)"
            echo "  --classic:    bitrate=500000, sp=0.800"
            exit 0
            ;;
        *)
            # 位置参数兼容: 含小数点→采样点, 否则→bitrate(或dbitrate)
            case "$1" in
                *.*) SAMPLE_POINT="$1" ;;
                *) if [ "$FD_MODE" = true ] && [ "$BITRATE" != "500000" ]; then DBITRATE="$1"
                   else BITRATE="$1"; fi ;;
            esac
            shift
            ;;
    esac
done

echo "=== CAN 初始化 (${CHANNEL}) ==="
if [ "$FD_MODE" = true ]; then
    echo "[INFO] 模式: CAN FD (仲裁段 bitrate=${BITRATE}, 数据段 dbitrate=${DBITRATE}, sp=${SAMPLE_POINT}, dsp=${DSAMPLE_POINT})"
else
    echo "[INFO] 模式: Classic CAN (bitrate=${BITRATE}, sp=${SAMPLE_POINT})"
fi

# 1. 加载内核模块 (SocketCAN 协议栈 + 硬件驱动自动检测)
CAN_DRIVERS=("peak_usb" "gs_usb" "mttcan" "kvaser_usb" "ems_usb" "esd_usb2")
LOADED_COUNT=0

for mod in can can_raw; do
    if ! lsmod | grep -q "^${mod} "; then
        sudo modprobe ${mod} 2>/dev/null && ((LOADED_COUNT++)) || true
    fi
done

# 自动检测已连接的 CAN 硬件驱动
for drv in "${CAN_DRIVERS[@]}"; do
    if lsmod | grep -q "^${drv} "; then
        echo "[INFO] 驱动 ${drv} 已加载"
        ((LOADED_COUNT++))
        break
    fi
    if sudo modprobe ${drv} 2>/dev/null; then
        echo "[INFO] 已加载驱动: ${drv}"
        ((LOADED_COUNT++))
        break
    fi
done

if [ $LOADED_COUNT -eq 0 ]; then
    echo "[WARN] 未检测到 CAN 硬件驱动，请确认设备已连接且驱动已安装"
    echo "      常见驱动包: apt install can-utils (Debian/Ubuntu)"
fi
echo "[OK] 内核模块已就绪"

# 2. 检查接口是否存在
if ! ip link show ${CHANNEL} &>/dev/null; then
    echo "[ERROR] ${CHANNEL} 接口不存在，请检查 CAN 设备连接及驱动"
    exit 1
fi

# 3. 强制 down (释放可能占用的 socket, 确保可重新配置)
if [ "$FORCE" = true ]; then
    echo "[INFO] 强制模式: 清理占用 ${CHANNEL} 的进程..."
    sudo fuser -k /sys/class/net/${CHANNEL}/ 2>/dev/null || true
    sleep 0.3
fi

sudo ip link set ${CHANNEL} down 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[INFO] ${CHANNEL} down 失败 (可能被占用), 尝试 fuser 释放..."
    sudo fuser -k /sys/class/net/${CHANNEL}/ 2>/dev/null || true
    sleep 0.3
    sudo ip link set ${CHANNEL} down 2>/dev/null || true
fi

# 4. 配置接口参数 (Classic CAN / CAN FD 统一路径)
if [ "$FD_MODE" = true ]; then
    sudo ip link set ${CHANNEL} type can \
        bitrate ${BITRATE} \
        dbitrate ${DBITRATE} \
        fd on \
        sample-point ${SAMPLE_POINT} \
        dsample-point ${DSAMPLE_POINT}
else
    sudo ip link set ${CHANNEL} type can \
        bitrate ${BITRATE} \
        sample-point ${SAMPLE_POINT}
fi

if [ $? -ne 0 ]; then
    echo "[ERROR] 配置 ${CHANNEL} 失败"
    exit 1
fi

# 5. 启用接口
sudo ip link set ${CHANNEL} up
if [ $? -ne 0 ]; then
    echo "[ERROR] 启用 ${CHANNEL} 失败"
    exit 1
fi

MODE_STR="bitrate=${BITRATE}"
if [ "$FD_MODE" = true ]; then
    MODE_STR="${MODE_STR}, dbitrate=${DBITRATE}, fd=on, dsp=${DSAMPLE_POINT}"
fi
echo "[OK] ${CHANNEL} 已就绪 (${MODE_STR}, sp=${SAMPLE_POINT})"
ip -details link show ${CHANNEL} | grep -E 'state|bitrate|dbitrate|sample-point|FD' | sed 's/^/  /'
echo "=== 初始化完成 ==="
