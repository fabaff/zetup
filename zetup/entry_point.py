from __future__ import absolute_import, print_function

import sys

from .zetup import Zetup
from .resolve import resolve

__all__ = ('setup_entry_point', )


def setup_entry_point(dist, keyword='use_zetup', value=True):
    """
    Zetup's ``entry_point`` handler for the ``setup()`` process in a project's
    **setup.py**, setting all setup keyword parameters based on zetup config

    Activated with ``setup(setup_requires=['zetup'], use_zetup=True)``
    """
    assert keyword == 'use_zetup'
    if not value:
        return

    from .zetup import Zetup
    # read config from current working directory (where setup.py is run)
    zfg = Zetup()
    keywords = zfg.setup_keywords()
    for name, value in keywords.items():
        # generally, setting stuff on dist.metadata is enough (and necessary)
        setattr(dist.metadata, name, value)
        # but *pip* only works correct if some stuff is also set directly on
        # dist object (pip seems to read at least package infos somehow from
        # there)
        if name.startswith('package') or name.endswith((
                'requires', 'require')):
            setattr(dist, name, value)

    if zfg.in_repo:
        # resolve requirements for zetup make
        resolve(['zetup[commands]>={}'.format(
            __import__('zetup').__version__)])
        import zetup.commands as _

        # make necessary files and store make result in distribution object,
        # so that files can be removed by del dist.zetup_made after setup()
        make_targets = ['VERSION', 'setup.py', 'zetup_config']
        dist.zetup_made = zfg.make(targets=make_targets)

    # finally run any custom setup hooks defined in project's zetup config
    if zfg.SETUP_HOOKS:
        sys.path.insert(0, '.')
        for hook in zfg.SETUP_HOOKS:
            modname, funcname = hook.split(':')
            mod = __import__(modname)
            for subname in modname.split('.')[1:]:
                mod = getattr(mod, subname)
            func = getattr(mod, funcname)
            func(dist)
