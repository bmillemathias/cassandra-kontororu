class command():

    def __init__(self, command_name, command):
        self.command_name = command_name
        self.command = command

    def run(self, args):
        self.args = args
        logger.info("launching command %s %s" % (self.command, self.args))
        # TODO: Add exception when a job fails to start
        p = subprocess.Popen([self.command, self.args])
        logger.info("launched command %s %s" % (self.command, self.args))
        self.process = p

    def __repr__(self):
        return self.command_name


