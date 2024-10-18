# Copyright 2020-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

"""Version module."""
from logging import getLogger

from click import group, pass_context

logger = getLogger(__name__)


@group()
@pass_context
def version(context):
    context.obj["group"] = "version"


@version.command(name='info')
def info():
   logger.info('my custom command from opensource OpenFL dev branch')
