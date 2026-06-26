import json
import subprocess
import os

# 定义所有监控的话题（在seesaw-hourly-check.sh中定义的）
# 为了简单起见，我先只针对我创建的话题检查
# 可以通过调用 seesaw.py list-markets 获取，然后遍历
# 这里先做一个基础框架，通过调用 subprocess 调用 seesaw.py comments 命令
