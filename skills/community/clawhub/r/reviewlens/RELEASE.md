# ReviewLens Release Notes

## Short Description

把海量商品评论压成购买结论卡，告诉你大家到底在夸什么、骂什么，谁适合买、谁容易踩坑。

## Marketplace Card Copy

Title:
- 评论透镜

Alternate title:
- ReviewLens

Short description:
- 把海量评论压成购买结论卡，告诉你大家到底在夸什么、骂什么，谁适合买、谁容易踩坑

Install hook:
- 不是看评分，而是读出评论背后的真实购买结论

## Announcement Copy

评论透镜（ReviewLens）不是看评分的工具。

它解决的是一个更靠近真实购买判断的问题：
- 真实买家到底在反复抱怨什么
- 差评是不是集中在同一个问题
- 这是产品缺陷，还是卖家 / 物流问题
- 这件商品适合谁
- 谁最容易踩坑
- 这个低价版本是便宜但有瑕疵，还是贵一点更稳

一句话说，它要交付的是：

`3 分钟看完 300 条评论后的那张结论卡。`

默认它会给出：
- Repeated Praise
- Repeated Complaints
- Is The Negative Signal Concentrated
- Best Fit / Likely Regret
- Cheap With Flaws Or Pricier But Steadier
- Final Call

也就是说，它不是复述评论，而是直接替用户做评论判断。

## Official Launch Post

今天发一个我很喜欢的新 OpenClaw skill：`评论透镜（ReviewLens）`。

很多购物工具都在解决这些问题：
- 哪个更便宜
- 哪个平台更值
- 哪个卖家更稳

但用户真正卡住的，往往是下一层：

看完一大堆评论以后，到底该怎么判断。

所以 `评论透镜` 做的不是看评分，也不是评论摘要。

它会直接把海量评论压成一张购买结论卡：
- 大家反复在夸什么
- 大家反复在骂什么
- 差评是不是集中在同一个问题
- 这是产品问题，还是卖家 / 物流问题
- 适合谁，不适合谁
- 便宜版是在省钱，还是在买缺点

我最喜欢它的一句话定位是：

`3 分钟看完 300 条评论后的那张结论卡。`

如果你也经常遇到这种场景：
- 不缺评论，缺结论
- 不缺评分，缺判断
- 不缺信息，缺一句可信的购买建议

那这个 skill 会很顺手。

## Suggested Tags

- latest
- reviews
- shopping
- review-intelligence
- review-analysis
- buyer-regret
- user-fit
- ecommerce
- taobao
- tmall
- jd
- pdd

## Suggested Repo Name

- `openclaw-skill-reviewlens`

## Preflight

```bash
cd /absolute/path/to/reviewlens
clawhub whoami
bash /absolute/path/to/codex/tmp/validate_clawhub_skill_dir.sh .
```

## Publish Command

### One command

```bash
cd /absolute/path/to/reviewlens
sh scripts/publish.sh
```

### Preview command

```bash
cd /absolute/path/to/reviewlens
sh scripts/publish.sh --print
```

### Manual command

```bash
clawhub publish /absolute/path/to/reviewlens \
  --slug reviewlens \
  --name "评论透镜" \
  --version "1.0.0" \
  --changelog "Launch 评论透镜 (ReviewLens), a review-intelligence skill that compresses marketplace reviews into a decision card with repeated praise, repeated complaints, fit, regret risk, and cheap-versus-steady judgment." \
  --tags "latest,reviews,shopping,review-intelligence,review-analysis,buyer-regret,user-fit,ecommerce,taobao,tmall,jd,pdd"
```
