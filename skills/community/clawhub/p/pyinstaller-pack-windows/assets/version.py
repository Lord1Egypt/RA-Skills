# 版本号唯一来源。
# - 本地/clone 默认用这个值；
# - CI 在出包时会重写本文件：发布 Release 时写成 tag 名（去 v），
#   push 到 main 时追加 "-dev"，这样两个 exe 自带的版本号永远和发版一致。
__version__ = "1.0.0"
