#!/usr/bin/python
import json
import os


"""
WIP - coming soon
"""

if __name__ == '__main__':

    assert 'KONTROL_PORT' in os.environ, '$KONTROL_PORT undefined (bug ?)'
    port = int(os.environ['KONTROL_PORT'])

    def _rpc(pod, cmd):
        
        try:

            #
            # - use zerorpc to request a script invokation against a given pod
            # - default on returning None upon failure
            #
            client = zerorpc.Client()
            client.connect('tcp://%s:%d' % (pod['ip'], port))
            return client.invoke(json.dumps({'cmd': cmd}))
            
        except Exception:
            return None

    #
    # - retrieve the latest state if any via $STATE
    #
    state = json.loads(os.environ['STATE']) if 'STATE' in os.environ else {}

    print json.dumps(state)