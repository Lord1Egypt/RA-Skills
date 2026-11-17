# -*- coding: utf-8 -*-
"""让测试从仓库根导入包"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
