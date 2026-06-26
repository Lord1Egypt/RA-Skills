#!/bin/bash
# 一键启动旅游攻略获取任务
# 
# 使用方式:
# ./start-tourism-guide.sh "台州亲子游" 3
# ./start-tourism-guide.sh "黄山三日游" 1 xiaohongshu

DEST="$1"          # 目的地，比如 "台州亲子游"
NUM="$2"           # 获取数量，默认 5
PLATFORMS="$3"     # 指定平台，默认 "xiaohongshu mafengwo ctrip weixin"

# 默认值
[ -z "$DEST" ] && echo "错误：请指定目的地" && exit 1
[ -z "$NUM" ] && NUM=5
[ -z "$PLATFORMS" ] && PLATFORMS="xiaohongshu mafengwo ctrip weixin"

# 格式化目的地（URL编码由脚本处理）
DATE=$(date +%Y-%m-%d)
TASKS_DIR="$HOME/.openclaw/workspace/tasks"
mkdir -p "$TASKS_DIR"

echo "=== 旅游攻略获取任务启动 ==="
echo "目的地: $DEST"
echo "获取数量: $NUM 篇/平台"
echo "平台: $PLATFORMS"
echo "日期: $DATE"
echo "任务目录: $TASKS_DIR"
echo

# 检查浏览器是否启动
if ! curl -s "http://localhost:18800/json" 2>/dev/null | grep -q .; then
  echo "⚠️  Chrome浏览器未启动，CDP端口 18800 不可用"
  echo "正在尝试启动浏览器..."
  if command -v google-chrome >/dev/null 2>&1; then
    google-chrome --remote-debugging-port=18800 --no-first-run --no-default-browser-check &
    echo "✅ 已启动 google-chrome --remote-debugging-port=18800 &"
    sleep 3
  elif command -v chrome >/dev/null 2>&1; then
    chrome --remote-debugging-port=18800 --no-first-run --no-default-browser-check &
    echo "✅ 已启动 chrome --remote-debugging-port=18800 &"
    sleep 3
  else
    echo "❌ 无法自动找到chrome，请手动启动："
    echo "   google-chrome --remote-debugging-port=18800 &"
    exit 1
  fi
fi

echo "✅ 浏览器CDP端口 18800 已就绪"
echo

# 创建任务文件
ORDER=1
for platform in $PLATFORMS; do
  case $platform in
    xiaohongshu)
      NAME="小红书"
      SORT="按收藏数排序 (collect_count)"
      CHECK="点赞数、收藏数"
      ;;
    mafengwo)
      NAME="马蜂窝"
      SORT="按浏览量排序"
      CHECK="浏览量"
      ;;
    ctrip)
      NAME="携程"
      SORT="按评分/点评数排序"
      CHECK="⭐x.x/5 评分"
      ;;
    weixin)
      NAME="微信公众号"
      SORT="按搜索结果排序"
      CHECK="来源公众号名称"
      ;;
    *)
      NAME="$platform"
      SORT="默认排序"
      CHECK="未知"
      ;;
  esac

  TASK_FILE="$TASKS_DIR/${NAME}_${DEST}_$DATE.md"
  
  cat > "$TASK_FILE" << EOF
# $NAME 攻略获取任务 ($DEST - $DATE)

## 任务要求
- 目标平台: $NAME ($platform)
- 目的地: $DEST
- 获取数量: 至少 $NUM 篇排名最高的攻略
- 排序方式: $SORT
- 数据纯正确认: $CHECK

## 浏览器状态
- CDP端口: 1880
- 执行顺序: 第 $ORDER 个（避免浏览器冲突）

## 操作提示
EOF

  # 添加平台特有操作提示
  case $platform in
    xiaohongshu)
      cat >> "$TASK_FILE" << EOF
- 搜索URL: https://www.xiaohongshu.com/search_result?keyword=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$DEST'))")&type=note&sort=collect_count
- 三种排序都要获取: hot / collect_count / time_descending
- 正文提取: 必须使用 eval + 提取脚本
  agent-browser --cdp 18800 eval "\$(cat $HOME/.openclaw/workspace/skills/xiaohongshu-crawler/scripts/extract-article.js)" --json
- 特有问题: 二维码拦截 → 通知用户扫码登录
EOF
      ;;
    mafengwo)
      cat >> "$TASK_FILE" << EOF
- 搜索URL: https://www.mafengwo.cn/search/q.php?q=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$DEST'))")&t=blog
- 必须提取浏览量（马蜂窝特有指标）
- 特有问题: 目的地页面404 → 改用搜索
EOF
      ;;
    ctrip)
      cat >> "$TASK_FILE" << EOF
- 景点页面: https://you.ctrip.com/sight/$(python3 -c "import urllib.parse; print(urllib.parse.quote('$DEST'))").html
- 游记页面: https://you.ctrip.com/travels/$(python3 -c "import urllib.parse; print(urllib.parse.quote('$DEST'))").html
- 必须提取 ⭐x.x/5 格式评分（携程特有）
EOF
      ;;
    weixin)
      cat >> "$TASK_FILE" << EOF
- 使用搜狗微信搜索
- 必须确认 URL 包含 mp.weixin.qq.com
- 遇到验证码 → 停止并建议用户提供具体文章URL
EOF
      ;;
  esac

  cat >> "$TASK_FILE" << EOF

## 输出要求
- 文件路径: $TASK_FILE
- 必须包含: 标题、作者、[$CHECK]、正文摘要
- 增量更新: 每完成一步更新文件末尾的进度

---
## 执行进度（Subagent更新）
- $(date +%H:%M) 任务启动

---
## 任务状态（完成后填写）
- 状态: ⏳ 进行中
- 获取数量: 0 篇
- 文件路径: $TASK_FILE

## 待解决问题
- 无
EOF

  echo "✅ 创建任务文件: $TASK_FILE"
  ORDER=$((ORDER + 1))
done

echo
echo "=== 所有任务文件创建完成 ==="
echo
echo "下一步:"
echo "1. 按顺序启动subagent，第一个: $TASKS_DIR/$(echo $PLATFORMS | cut -d' ' -f1)_${DEST}_$DATE.md"
echo "2. 每个subagent完成后，启动下一个"
echo "3. 全部完成后，Main Agent整合输出到: ~/llm-wiki/raw/articles/${DEST}综合攻略.md"
echo
