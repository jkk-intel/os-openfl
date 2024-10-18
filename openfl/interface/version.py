# Copyright 2020-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

"""Version module."""
from logging import getLogger

from click import group, pass_context

logger = getLogger(__name__)


@group()
@pass_context
def version(context):
    """Manage Federated Learning version.

    Args:
        context (click.core.Context): Click context.
    """
    context.obj["group"] = "version"


@version.command(name='info')
@pass_context
def info(
    context,
):
   logger.info('my custom command from opensource OpenFL dev branch')
