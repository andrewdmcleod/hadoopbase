from charms.reactive import (
    set_state,
    is_state,
    hook,
    when,
    when_not
)
from charmhelpers.core import hookenv
from charmhelpers.core import unitdata
import setup
setup.pre_install()

import jujuresources

def bootstrap_resources():
    """
    Install required resources defined in resources.yaml
    """
    if unitdata.kv().get('charm.bootstrapped', False):
        return True
    hookenv.status_set('maintenance', 'Installing base resources')
    mirror_url = jujuresources.config_get('resources_mirror')
    if not jujuresources.fetch(mirror_url=mirror_url):
        missing = jujuresources.invalid()
        hookenv.status_set('blocked', 'Unable to fetch required resource%s: %s' % (
            's' if len(missing) > 1 else '',
            ', '.join(missing),
        ))
        return False
    jujuresources.install(['pathlib', 'jujubigdata', 'charm-benchmark'])
    unitdata.kv().set('charm.bootstrapped', True)
    return True


@hook('install')
def install():
    if not bootstrap_resources():
        return
    import jujubigdata
    client_reqs = ['vendor', 'hadoop_version', 'packages', 'groups', 'users',
                   'dirs']
    dist_config = jujubigdata.utils.DistConfig(filename='dist.yaml',
                                               required_keys=client_reqs)
    hadoop = jujubigdata.handlers.HadoopBase(dist_config)
    if not hadoop.verify_conditional_resources():
        return
    hadoop.install()
    

