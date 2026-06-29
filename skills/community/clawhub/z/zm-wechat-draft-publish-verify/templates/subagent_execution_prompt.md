# 可复制给 SubAgent 的执行提示词

你正在执行 `zm-wechat-draft-publish-verify` Skill。

请把已准备好的公众号 Markdown/HTML 推送到草稿箱，并完成真实落库核验。

## 最小必填

- 待发布文件路径
- 标题
- 作者/署名
- 封面图路径（如需要）
- 摘要
- 公众号凭据环境是否可用
- 是否需要仅创建草稿，不群发

## 执行顺序

1. 检查文件存在
2. 清理操作备注/脏文本
3. 检查图片引用
4. zm-md2wechat-conversion-tool 转换/推草稿
5. draft/get 获取草稿
6. 核验标题、正文、图片、排版
7. 记录 media_id / draft_id / 日志
8. 输出 PASS / NEEDS_REVISION / BLOCKED

## 硬门禁

- 不得把本地转换成功当作草稿成功。
- 必须 draft/get 核验真实落库。
- 只创建草稿，不得未经确认群发。
- 失败不得重复创建多个草稿，先核验再补发。
