# SPDX-FileCopyrightText: 2023-present m.raziei <mohammadraziei1375@gmail.com>
#
# SPDX-License-Identifier: MIT
import sys
from pathlib import Path

CMD = Path(__file__).parent
RESOURCES_PATH = CMD / "resources"
sys.path.append(CMD.parent.joinpath("src").as_posix())
