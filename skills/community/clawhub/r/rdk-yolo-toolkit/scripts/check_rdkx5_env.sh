#!/bin/bash
# RDK X5 板端环境自检
# 用法：scp 到板端后 bash check_rdkx5_env.sh
#   或：ssh root@<IP> 'bash -s' < check_rdkx5_env.sh

echo "=== RDK X5 部署环境自检 ==="

# 1. RDK OS ≥ 3.5.0（hbm_runtime 前提）
OS_VERSION=$(cat /etc/version)
echo ""
echo "1) OS: $OS_VERSION"
[ "$(printf '%s\n' "3.5.0" "$OS_VERSION" | sort -V | head -n1)" = "3.5.0" ] \
    && echo "   ✅ OS >= 3.5.0" \
    || echo "   ❌ 需 >= 3.5.0，请刷机升级"

# 2. TROS Humble setup
echo ""
echo "2) TROS Humble"
[ -f /opt/tros/humble/setup.bash ] \
    && echo "   ✅ /opt/tros/humble/setup.bash 存在" \
    || echo "   ❌ 未装 TROS Humble"

# 3. dnn_node ≥ 2.6.1（ultralytics_yolo parser 引入）
echo ""
echo "3) dnn_node"
if [ -f /opt/tros/humble/share/dnn_node/package.xml ]; then
    DNN_VER=$(grep -oP '(?<=<version>)[^<]+' /opt/tros/humble/share/dnn_node/package.xml)
    echo "   version: $DNN_VER"
    [ "$(printf '%s\n' "2.6.1" "$DNN_VER" | sort -V | head -n1)" = "2.6.1" ] \
        && echo "   ✅ dnn_node >= 2.6.1（支持 ultralytics_yolo parser）" \
        || echo "   ❌ 需 >= 2.6.1，运行 apt upgrade tros-humble-dnn-node"
else
    echo "   ❌ dnn_node 未装"
fi

# 4. hbm_runtime（Python BPU 推理库）
echo ""
echo "4) hbm_runtime"
python3 -c "import hbm_runtime" 2>/dev/null \
    && echo "   ✅ hbm_runtime 可 import" \
    || echo "   ❌ pip3 install hbm-runtime"

# 5. BPU 设备节点
echo ""
echo "5) BPU 设备"
if ls /dev/bpu* >/dev/null 2>&1; then
    ls /dev/bpu*
    echo "   ✅ BPU 设备就绪"
else
    echo "   ❌ /dev/bpu* 不存在，检查 BPU 驱动"
fi

# 6. cv2 + numpy（runtime 用得到）
echo ""
echo "6) Python 库"
python3 -c "import cv2, numpy; print('   cv2', cv2.__version__, '| numpy', numpy.__version__, '✅')" 2>&1

# 7. tmux（可选）
echo ""
echo "7) tmux（可选）"
which tmux >/dev/null 2>&1 \
    && echo "   ✅ tmux 已装" \
    || echo "   ⚠️  tmux 未装（不重要，Agent 会用 nohup 兜底）"

echo ""
echo "=== 自检结束 ==="
