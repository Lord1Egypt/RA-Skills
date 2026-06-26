#!/usr/bin/env bash
# weread.sh — WeRead Agent API CLI
# Usage: weread.sh <subcommand> [--param=value ...] [-h]

set -euo pipefail

GATEWAY="https://i.weread.qq.com/api/agent/gateway"

resolve_api() {
  case "$1" in
    search)          echo "/store/search" ;;
    book-info)       echo "/book/info" ;;
    chapters)        echo "/book/chapterinfo" ;;
    progress)        echo "/book/getprogress" ;;
    bookmarks)       echo "/book/bookmarklist" ;;
    best-bookmarks)  echo "/book/bestbookmarks" ;;
    underlines)      echo "/book/underlines" ;;
    read-reviews)    echo "/book/readreviews" ;;
    my-reviews)      echo "/review/list/mine" ;;
    review-detail)   echo "/review/single" ;;
    readdata)        echo "/readdata/detail" ;;
    reviews)         echo "/review/list" ;;
    shelf)           echo "/shelf/sync" ;;
    notebooks)       echo "/user/notebooks" ;;
    recommend)       echo "/book/recommend" ;;
    similar)         echo "/book/similar" ;;
    list-apis)       echo "/_list" ;;
    *) return 1 ;;
  esac
}

show_global_help() {
  cat <<'EOF'
weread.sh <subcommand> [--param=value ...] [-h]

Subcommands:
  search --keyword          搜索书籍
  book-info --bookId        书籍基本信息
  chapters --bookId         章节目录
  progress --bookId         阅读进度
  shelf                     书架同步
  notebooks                 笔记本概览
  bookmarks --bookId        单本书划线内容
  best-bookmarks --bookId   书籍热门划线
  underlines --bookId --chapterUid  章节划线热度
  read-reviews --bookId --chapterUid --reviews=JSON  划线下想法
  my-reviews --bookid       单本书个人想法与点评
  review-detail --reviewId  单条想法详情
  reviews --bookId          书籍公开点评
  readdata --mode           阅读统计
  recommend                 个性化推荐
  similar --bookId          相似书推荐
  list-apis                 列出所有可用接口

Auth: $WEREAD_API_KEY (格式 wrk-xxxxxxxx)
EOF
}

help_search() {
  cat <<'EOF'
weread.sh search | API: /store/search | Ref: references/search.md

Params:
  --keyword=STR    (必填) 搜索关键词
  --scope=INT      搜索类型: 0=全部 10=电子书 16=网文 14=听书 6=作者 12=全文 13=书单 2=公众号 4=文章
  --maxIdx=INT     翻页偏移, 默认 0
  --count=INT      每页数量, 服务端默认 15

Response:
  sid                                  搜索会话 ID
  hasMore                              1=有更多 0=无
  results[].title                      分组标题
  results[].scope                      分组类型
  results[].scopeCount                 该分组总结果数
  results[].currentCount               本次返回数量
  results[].books[].searchIdx          翻页序号 (传入 maxIdx)
  results[].books[].bookInfo.bookId    书籍 ID
  results[].books[].bookInfo.title     书名
  results[].books[].bookInfo.author    作者
  results[].books[].bookInfo.cover     封面图 URL
  results[].books[].bookInfo.intro     简介
  results[].books[].bookInfo.publisher 出版社
  results[].books[].bookInfo.category  分类
  results[].books[].bookInfo.payType   付费类型
  results[].books[].bookInfo.soldout   是否下架
  results[].books[].readingCount       在读人数
  results[].books[].newRating          评分 (0-100)
  results[].books[].newRatingCount     评分人数
  results[].books[].newRatingDetail    评分标签
EOF
}

help_book_info() {
  cat <<'EOF'
weread.sh book-info | API: /book/info | Ref: references/book.md

Params:
  --bookId=STR     (必填) 书籍 ID

Response:
  bookId           书籍 ID
  title            书名
  author           作者
  translator       译者
  cover            封面 URL
  intro            简介
  category         分类
  publisher        出版社
  publishTime      出版时间
  isbn             ISBN
  wordCount        总字数
  newRating        评分 (百分制)
  newRatingCount   评分人数
  newRatingDetail  评分分布详情
EOF
}

help_chapters() {
  cat <<'EOF'
weread.sh chapters | API: /book/chapterinfo | Ref: references/book.md

Params:
  --bookId=STR     (必填) 书籍 ID

Response:
  bookId                    书籍 ID
  synckey                   同步 key
  chapterUpdateTime         章节最后更新时间
  chapters[].chapterUid     章节 UID (后续接口参数)
  chapters[].chapterIdx     章节序号
  chapters[].title          章节标题
  chapters[].wordCount      章节字数
  chapters[].level          目录层级 (1=一级 2=二级...)
  chapters[].updateTime     更新时间
  chapters[].price          价格 (0=免费)
  chapters[].paid           是否已购买
  chapters[].isMPChapter    是否公众号章节
  chapters[].anchors        章节内锚点/子标题数组
EOF
}

help_progress() {
  cat <<'EOF'
weread.sh progress | API: /book/getprogress | Ref: references/book.md

Params:
  --bookId=STR     (必填) 书籍 ID

Response:
  bookId                    书籍 ID
  book.chapterUid           当前阅读章节 UID
  book.chapterOffset        章节内偏移
  book.progress             阅读进度 (0-100 整数, 1=1% 非 100%)
  book.updateTime           最后阅读时间
  book.recordReadingTime    累计阅读时长 (秒)
  book.finishTime           读完时间 (仅 progress=100 时存在)
  book.isStartReading       是否已开始阅读
  timestamp                 服务端时间戳
EOF
}

help_shelf() {
  cat <<'EOF'
weread.sh shelf | API: /shelf/sync | Ref: references/shelf.md

Params: 无 (用户身份通过 API Key 自动识别)

Response:
  books[]                              电子书/导入书/公众号类条目数组
  books[].bookId                       书籍 ID
  books[].title                        书名
  books[].author                       作者
  books[].cover                        封面图 URL
  books[].category                     分类
  books[].readUpdateTime               最近阅读时间 (Unix 时间戳)
  books[].finishReading                是否读完 (1=读完)
  books[].updateTime                   更新时间
  books[].isTop                        是否置顶
  books[].secret                       是否私密 (1=私密)
  albums[]                             专辑/有声书数组 (与 books 独立)
  albums[].albumInfo.albumId           专辑 ID
  albums[].albumInfo.name              专辑名称
  albums[].albumInfo.authorName        演播/作者
  albums[].albumInfo.cover             封面图 URL
  albums[].albumInfo.trackCount        音频集数
  albums[].albumInfo.finishStatus      完结状态
  albums[].albumInfo.finish            是否完结
  albums[].albumInfo.payType           付费类型
  albums[].albumInfo.intro             简介
  albums[].albumInfo.updateTime        更新时间
  albums[].albumInfoExtra.secret       是否私密
  albums[].albumInfoExtra.lecturePaid  是否已购买
  albums[].albumInfoExtra.lectureReadUpdateTime  最近收听时间
  albums[].albumInfoExtra.isTop        是否置顶
  mp                                   文章收藏入口对象 (非空=有 1 个文章收藏条目)
  archive[].name                       书单名称
  archive[].bookIds                    书单内 bookId 列表
  bookCount                            电子书数量 (不含 albums 和 mp)
EOF
}

help_notebooks() {
  cat <<'EOF'
weread.sh notebooks | API: /user/notebooks | Ref: references/notes.md

Params:
  --count=INT      每页数量, 默认 20
  --lastSort=INT   翻页游标 (上页最后一条的 sort 值)

Response:
  totalBookCount            有笔记的书籍总数
  totalNoteCount            笔记总条数 (汇总值)
  hasMore                   1=有更多
  books[].bookId            书籍 ID
  books[].book              书籍信息 (title, author, cover 等)
  books[].reviewCount       想法/点评数
  books[].noteCount         划线数
  books[].bookmarkCount     书签数
  books[].readingProgress   阅读进度
  books[].markedStatus      标记状态 (1=读完)
  books[].sort              排序值 (翻页游标)
EOF
}

help_bookmarks() {
  cat <<'EOF'
weread.sh bookmarks | API: /book/bookmarklist | Ref: references/notes.md

Params:
  --bookId=STR     (必填) 书籍 ID

Response:
  updated[]                 划线数组 (已过滤书签, 只含划线)
  updated[].bookmarkId      划线 ID
  updated[].bookId          书籍 ID
  updated[].chapterUid      所在章节 UID
  updated[].markText        划线原文
  updated[].createTime      创建时间 (Unix 时间戳)
  updated[].type            类型
  updated[].range           位置范围
  updated[].colorStyle      划线颜色样式
  chapters[]                章节信息数组
  chapters[].chapterUid     章节 UID
  chapters[].chapterIdx     章节序号
  chapters[].title          章节标题
  book                      书籍信息
EOF
}

help_best_bookmarks() {
  cat <<'EOF'
weread.sh best-bookmarks | API: /book/bestbookmarks | Ref: references/notes.md

Params:
  --bookId=STR     (必填) 书籍 ID
  --chapterUid=INT 章节 UID (0=全部章节), 默认 0
  --synckey=INT    增量同步 key, 默认 0

Response:  (服务端固定返回前 20 条, 不支持分页)
  synckey                   同步 key
  totalCount                热门划线总数
  items[].bookId            书籍 ID
  items[].userVid           代表用户 VID
  items[].bookmarkId        划线 ID
  items[].chapterUid        所在章节 UID
  items[].range             位置范围
  items[].markText          划线原文
  items[].totalCount        划线人数
  chapters[]                章节信息数组
  chapters[].chapterUid     章节 UID
  chapters[].chapterIdx     章节序号
  chapters[].title          章节标题
EOF
}

help_underlines() {
  cat <<'EOF'
weread.sh underlines | API: /book/underlines | Ref: references/notes.md

Params:
  --bookId=STR     (必填) 书籍 ID
  --chapterUid=INT (必填) 章节 UID
  --synckey=INT    增量同步 key, 默认 0

Response:  (热度统计, 不含划线文本)
  bookId                    书籍 ID
  chapterUid                章节 UID
  underlines[].range        位置范围
  underlines[].count        划线人数
  underlines[].score        热度分数
  underlines[].type         划线类型
  synckey                   同步 key
EOF
}

help_read_reviews() {
  cat <<'EOF'
weread.sh read-reviews | API: /book/readreviews | Ref: references/notes.md

Params:
  --bookId=STR     (必填) 书籍 ID
  --chapterUid=INT (必填) 章节 UID
  --reviews=JSON   (必填) 划线范围数组, 如 [{"range":"900-2004","count":10}]

Response:
  bookId                                    书籍 ID
  chapterUid                                章节 UID
  reviews[].range                           划线范围
  reviews[].totalCount                      该范围下想法总数
  reviews[].hasMore                         1=有更多
  reviews[].maxIdx                          翻页偏移
  reviews[].synckey                         翻页游标
  reviews[].pageReviews[].reviewId          想法 ID
  reviews[].pageReviews[].review.abstract   划线原文
  reviews[].pageReviews[].review.content    想法内容
  reviews[].pageReviews[].review.range      位置范围
  reviews[].pageReviews[].review.createTime 创建时间
  reviews[].pageReviews[].review.author     作者信息
EOF
}

help_my_reviews() {
  cat <<'EOF'
weread.sh my-reviews | API: /review/list/mine | Ref: references/notes.md

Params:
  --bookid=STR     (必填) 书籍 ID  (注意: 小写 bookid)
  --synckey=INT    翻页游标, 默认 0
  --count=INT      每页数量, 默认 20

Response:
  reviews[].review.reviewId      ID
  reviews[].review.content       内容文本
  reviews[].review.createTime    创建时间
  reviews[].review.star          评分 (0-5, -1=无评分)
  reviews[].review.chapterName   所在章节名 (章节点评时有值)
  reviews[].review.isFinish      是否读完 (书评时有值)
  totalCount                     总条数
  hasMore                        1=有更多
  synckey                        翻页游标
EOF
}

help_review_detail() {
  cat <<'EOF'
weread.sh review-detail | API: /review/single | Ref: references/notes.md

Params:
  --reviewId=STR          (必填) 想法/评论 ID
  --commentsCount=INT     拉取评论数量, 默认 10
  --commentsDirection=INT 评论排序: 0=倒序 1=正序
  --likesCount=INT        拉取点赞数量, 默认 10
  --likesDirection=INT    点赞排序: 0=倒序
  --synckey=INT           增量同步 key, 默认 0

Response:
  reviewId       想法 ID
  review         想法详情对象
  htmlContent    富文本内容
  synckey        同步 key
EOF
}

help_readdata() {
  cat <<'EOF'
weread.sh readdata | API: /readdata/detail | Ref: references/readdata.md

Params:
  --mode=STR       统计维度: weekly/monthly/annually/overall, 默认 monthly
  --baseTime=INT   基准时间戳 (0=当前周期), 服务端归一化到周期起点

Response:
  baseTime                         周期基准时间戳
  totalReadTime                    总阅读时长 (秒)
  readDays                         有效阅读天数 (单日满 1 分钟)
  dayAverageReadTime               日均时长 (秒, 分母=自然日数)
  compare                          与上期日均对比比例 (0.2=增长20%)
  readTimes                        分桶时长 (对象, key=时间戳 value=秒)
  dailyReadTimes                   每日时长明细 (annually 可能返回)
  readLongest[].book               书籍信息
  readLongest[].albumInfo          有声内容信息
  readLongest[].readTime           阅读时长 (秒)
  readLongest[].tags               标签 (如 "笔记最多")
  readStat[].stat                  统计项 (读过/读完/阅读/笔记)
  readStat[].counts                统计值文案
  preferCategory[].categoryTitle   分类名称
  preferCategory[].val             偏好权重
  preferCategory[].readingTime     分类阅读时长 (秒)
  preferCategory[].readingCount    分类阅读本数
  preferCategoryWord               偏好分类文案
  preferTime                       24h 时段分布数组 (秒, 从 6 点起)
  preferTimeWord                   偏好时段文案
  preferAuthor[].name              作者名
  preferAuthor[].count             阅读本数
  preferAuthor[].readTime          时长 (格式化字符串, 非秒数)
  preferPublisher[].name           出版社名
  preferPublisher[].count          阅读本数
  readRate                         文字阅读占比 (百分比)
  wrReadTime                       文字阅读时长 (秒)
  wrListenTime                     听书时长 (秒)
  rank.text                        排行文案
  registTime                       注册时间戳
EOF
}

help_reviews() {
  cat <<'EOF'
weread.sh reviews | API: /review/list | Ref: references/review.md

Params:
  --bookId=STR          (必填) 书籍 ID
  --reviewListType=INT  筛选: 0=全部 1=推荐 2=不行 3=最新 4=一般, 默认 0
  --count=INT           每页数量, 默认 20
  --maxIdx=INT          翻页偏移, 默认 0
  --synckey=INT         翻页游标, 默认 0

Response:
  synckey                                翻页游标
  reviewsCnt                             点评总数
  reviewsHasMore                         1=有更多
  deepVRecommendInfo.title               资深会员推荐摘要
  deepVRecommendInfo.subtitle            推荐比例文案
  deepVRecommendValue                    推荐比例 (862=86.2%)
  friendCommentCount                     好友点评数
  reviews[].idx                          翻页序号 (传入 maxIdx)
  reviews[].review.review.content        点评文本
  reviews[].review.review.htmlContent    富文本内容
  reviews[].review.review.star           评分 (20/40/60/80/100)
  reviews[].review.review.isFinish       是否读完
  reviews[].review.review.createTime     创建时间
  reviews[].review.review.chapterName    章节名
  reviews[].review.review.author.name    评论者昵称
  reviews[].review.review.author.avatar  评论者头像
EOF
}

help_recommend() {
  cat <<'EOF'
weread.sh recommend | API: /book/recommend | Ref: references/discover.md

Params:
  --count=INT      每页数量, 默认 12
  --maxIdx=INT     翻页偏移, 默认 0

Response:
  books[].bookId             书籍 ID
  books[].title              书名
  books[].author             作者
  books[].cover              封面图 URL
  books[].intro              简介
  books[].category           分类
  books[].reason             推荐理由
  books[].readingCount       在读人数
  books[].searchIdx          翻页序号 (传入 maxIdx)
  books[].newRating          评分 (0-100)
  books[].newRatingCount     评分人数
  books[].newRatingDetail.title  评分标签
  books[].price              价格 (分)
  books[].payType            付费类型
EOF
}

help_similar() {
  cat <<'EOF'
weread.sh similar | API: /book/similar | Ref: references/discover.md

Params:
  --bookId=STR     (必填) 书籍 ID
  --count=INT      每页数量, 默认 12
  --maxIdx=INT     翻页偏移, 默认 0
  --sessionId=STR  翻页会话 ID (首次不传, 后续传回包值)

Response:
  booksimilar.sessionId                翻页会话 ID
  booksimilar.books[].idx              翻页序号 (传入 maxIdx)
  booksimilar.books[].book.bookInfo    书籍信息 (bookId, title, author, cover 等)
EOF
}

help_list_apis() {
  cat <<'EOF'
weread.sh list-apis | API: /_list

Params: 无
Response: 所有可用接口及参数定义
EOF
}

show_subcmd_help() {
  case "$1" in
    search)         help_search ;;
    book-info)      help_book_info ;;
    chapters)       help_chapters ;;
    progress)       help_progress ;;
    shelf)          help_shelf ;;
    notebooks)      help_notebooks ;;
    bookmarks)      help_bookmarks ;;
    best-bookmarks) help_best_bookmarks ;;
    underlines)     help_underlines ;;
    read-reviews)   help_read_reviews ;;
    my-reviews)     help_my_reviews ;;
    review-detail)  help_review_detail ;;
    readdata)       help_readdata ;;
    reviews)        help_reviews ;;
    recommend)      help_recommend ;;
    similar)        help_similar ;;
    list-apis)      help_list_apis ;;
  esac
}

call_api() {
  local api_name="$1"; shift

  if [ -z "${WEREAD_API_KEY:-}" ]; then
    echo "Error: WEREAD_API_KEY not set. Run: export WEREAD_API_KEY=wrk-xxxxxxxx" >&2
    return 1
  fi

  local json
  if [ $# -eq 0 ]; then
    json=$(jq -nc --arg a "$api_name" '{api_name: $a}')
  else
    json=$(printf '%s\n' "$@" | jq -Rnc --arg a "$api_name" '
      {api_name: $a} + ([inputs | ltrimstr("--") |
        (index("=") // length) as $i |
        {(.[0:$i]): (.[$i+1:] |
          if test("^-?[0-9]+$") then tonumber
          elif test("^[\\[{]") then fromjson
          else . end)}
      ] | add)')
  fi

  curl -sS -X POST "$GATEWAY" \
    -H "Authorization: Bearer $WEREAD_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$json"
}

main() {
  if [ $# -eq 0 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_global_help
    return
  fi

  local subcmd="$1"; shift

  if ! resolve_api "$subcmd" > /dev/null 2>&1; then
    echo "Error: unknown subcommand '$subcmd'. Run 'weread.sh -h' for list." >&2
    return 1
  fi

  for arg in "$@"; do
    if [ "$arg" = "-h" ] || [ "$arg" = "--help" ]; then
      show_subcmd_help "$subcmd"
      return
    fi
  done

  call_api "$(resolve_api "$subcmd")" "$@"
}

main "$@"
