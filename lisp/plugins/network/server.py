# -*- coding: utf-8 -*-
#
# This file is part of Linux Show Player
#
# Copyright 2012-2018 Francesco Ceruti <ceppofrancy@gmail.com>
#
# Linux Show Player is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Linux Show Player is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Linux Show Player.  If not, see <http://www.gnu.org/licenses/>.

import logging
from threading import Thread
from wsgiref.simple_server import make_server, WSGIRequestHandler

logger = logging.getLogger(__name__)


class APIServerThread(Thread):
    def __init__(self, host, port, api):
        super().__init__(daemon=True)
        self.wsgi_server = make_server(
            host, port, api, handler_class=APIRequestHandler)

    def run(self):
        try:
            logger.info(
                'Start serving network API at: http://{}:{}/'.format(
                    self.wsgi_server.server_address[0],
                    self.wsgi_server.server_address[1],
                )
            )

            self.wsgi_server.serve_forever()

            logger.info('Stop serving network API')
        except Exception:
            logger.exception('Network API server stopped working.')

    def stop(self):
        self.wsgi_server.shutdown()
        self.wsgi_server.server_close()

        self.join()


class APIRequestHandler(WSGIRequestHandler):

    def log_message(self, format, *args):
        logger.debug(format % args)