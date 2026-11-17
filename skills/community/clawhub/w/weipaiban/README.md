# weipaiban

微排版公众号 SVG 交互作品：为微信公众号制作并可直接发布的整篇 SVG 互动图文。选择 format 后完成创意设计、图片准备、交互 HTML 制作和发布。

图片默认从微排版 AI 素材库按一个 tag 取全量已发布图，再分配到背景、透明装饰和场景槽位。用户可以改为提供图片，或点名自己的生图技能。需要入库时用技能自带的 `scripts/upload_images.py`，不另装上传技能。tag 没有图时，图片槽位只用占位图。

当前 format：带中间固定内容层的三层视差滑动（`layered-scroll`），背景容器加多层不同速度的 3D 视差滑动（`parallax-scroll`），后层上色板加竖向镂空滑动的滑动上色（`coloring-scroll`），每题一个正确选项、选择后锁定的计分答题（`quiz`），左右封面点选展开的选择其一（`choice-expand`，二选一、四选一或六选一），以及点击播放后画布高度归零的场景转场（`scene-transition`）。

入口与工作流见 [SKILL.md](SKILL.md)。

## 获取密钥

取素材、上传图片和发布作品都要读取环境变量 `WEIPAIBAN_API_KEY`。

1. 登录 [微排版](https://weipaiban.cn)。
2. 打开 [API 密钥](https://weipaiban.cn/settings/api-keys)，创建或复制一把以 `sk-` 开头的密钥。
3. 把它设到当前环境，例如：`export WEIPAIBAN_API_KEY=sk-...`

密钥只放在环境变量里。不要贴进对话，也不要写进作品或任务文件。

## 开源

源码仓库：[https://github.com/21epub/weipaiban-skill](https://github.com/21epub/weipaiban-skill)

## 交流群

使用问题、格式反馈可以进微信群。用微信扫描下面的二维码加入。

![微排版交流群二维码](assets/contact-me-qr.png)
