#! /bin/env python
# -*- coding: utf-8 -*-

import os.path
import sys
import logging
import time
import configobj
from flask import Flask, abort
try:
    import subprocess32 as subprocess
except:
    import subprocess
import threading
import argparse
from utils import command


FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel('INFO')

parser = argparse.ArgumentParser(
    description="A deamon to manage Cassandra Cluster")
parser.add_argument("--port", "-p", default=9876,
    help="port used by the webservice", type=int)
parser.add_argument(
    "config", help="Configuration file for authorized commands")
parser.add_argument("--debug", "-d", action="store_true")
args = parser.parse_args()

if args.debug:
    logger.setLevel('DEBUG')


# TODO: move in the module utils
class command_tracker(object):
    """ Object responsible to store and track existence of commands """

    def __init__(self):
        self.commands = []

    def list_commands(self):
        return [command for command in commands]

    def add(self, command):
        if not self.__is_active(command):
            self.commands.append(command)
        else:
            return False

    def __is_active(self, command):
        """ Check if a command is already is the list """
        return True


# TODO: move in a module utils
class command(object):
    """ An object that match a command """

    def __init__(self, command_name, command):
        self.command_name = command_name
        self.command = command
        self.starttime = None

    def run(self, args):
        self.args = args
        logger.info("launching command %s %s" % (self.command, self.args))
        # TODO: Add exception when a job fails to start
        p = subprocess.Popen([self.command, self.args])
        self.starttime = time.time()
        logger.info("launched command %s %s" % (self.command, self.args))
        self.process = p

    def __repr__(self):
        return self.command_name


def commands_status(commands):
    logging.debug('thread %s' % t.getName())
    while True:
        if len(commands) == 0:
            logger.debug('No currently running commands')
        else:
            logger.info("Number of commands: %d" % len(commands))
            for command in commands:
                logger.info(command.__dict__)
                # check the status of the process
                code = command.process.poll()
                logger.info("code: %s" % code)
                # if poll returns a value the command is terminated
                if code is not None:
                    status = command.process.returncode
                    logger.info(
                        "command %s is terminated with status %s"
                        % (command, status))
                    # TODO: delete the command from the list as it is terminated

        time.sleep(5)

web_server = Flask(__name__)

if not os.path.isfile(args.config):
    logger.error(
        "Config file %s does not exist or is not a file" % args.config)
    sys.exit(1)


@web_server.route('/')
def index():
    return "Nothing here"


@web_server.route('/cmd/<string:cmd>')
@web_server.route('/cmd/<string:cmd>/<string:args>')
def run_command(cmd, args=None):
    if cmd not in commands:
        logger.warn("Command %s is not authorized" % cmd)
        abort(403)
    else:
        cmd = command(cmd, cmd)
        # if a problem arises when launching the command an exception is throw
        cmd.run(args)
        commands_list.append(cmd)
        return "Job %s is launched" % cmd.__dict__


@web_server.route('/status/cmd/')
def print_list_commands():
    print commands_list
    return commands_list


@web_server.route('/status/node/')
def cassandra_node_status()
    pass


if __name__ == "__main__":
    logger.info('Starting %s' % __name__)
    web_server.debug = True

    config = configobj.ConfigObj(args.config)
    try:
        commands = config['commands'].keys()
        logger.debug("Authorized commands are %s" % commands)
    except KeyError:
        logger.error(
            "Unable to find required 'commands' section in the config file %s"
            % config)
        sys.exit(1)

    try:
        commands = config['cassandra'].keys()
    except KeyError:
        logger.error(
            "Unable to find required 'cassandra' section in the config file %s"
            % config)
        sys.exit(1)

    global commands_list
    commands_list = []

    t = threading.Thread(target=commands_status, args=(commands_list,))
    t.setName('commands_status')
    t.daemon = True
    t.start()

    # TODO: connexion to cassandra cluster goes here

    web_server.run(port=args.port)
