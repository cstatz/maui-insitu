#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

__author__ = 'Christoph Statz'

import logging

from .output import MauiInSitu


try:
    from nicelog.formatters import ColorLineFormatter
    import sys
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(ColorLineFormatter(show_date=True, show_function=True, show_filename=True, message_inline=True))
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
except:
    pass
