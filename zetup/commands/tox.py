# zetup.py
#
# Zimmermann's Python package setup.
#
# Copyright (C) 2014 Stefan Zimmermann <zimmermann.code@gmail.com>
#
# zetup.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# zetup.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with zetup.py. If not, see <http://www.gnu.org/licenses/>.

from textwrap import dedent
from subprocess import call

from path import path as Path

from zetup import Zetup


@Zetup.command
def tox(self):
    tox_ini = Path('tox.ini')
    create_tox_ini = not tox_ini.exists()
    if create_tox_ini:
        tox_ini.write_text(dedent("""
          [tox]
          envlist = %s""" % ','.join(
            'py' + version.replace('.', '')
            for version in self.PYTHON)
          + """

          [testenv]
          deps =
            zetup
          """))
    status = call(['tox'])
    if create_tox_ini:
        tox_ini.remove()
    return status
