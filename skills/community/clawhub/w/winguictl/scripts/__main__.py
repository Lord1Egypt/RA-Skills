#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

"""Entry point for python -m winguictl invocation."""

import sys
from .winguictl import main

if __name__ == "__main__":
    sys.exit(main())
