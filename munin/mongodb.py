#!/usr/bin/env python

import os
import sys

class MuninMongoDBPlugin(object):
    dbname_in_args = True
    category = "MongoDB"

    def __init__(self):
        super(MuninMongoDBPlugin, self).__init__()

        self.dbname = ((sys.argv[0].rsplit('_', 1)[-1] if self.dbname_in_args else None)
            or os.environ['MONGODB_DATABASE'])
        host = os.environ.get('MONGODB_SERVER') or 'localhost'
        if ':' in host:
            host, port = host.split(':')
            port = int(port)
        else:
            port = 27017
        self.server = (host, 27017)

    @property
    def connection(self):
        if not hasattr(self, '_connection'):
            import pymongo
            self._connection = pymongo.Connection(*self.server)
        return self._connection

    @property
    def db(self):
        if not hasattr(self, '_db'):
            self._db = getattr(self.connection, self.dbname)
        return self._db

    def autoconf(self):
        return bool(self.connection())