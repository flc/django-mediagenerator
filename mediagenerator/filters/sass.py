from mediagenerator.base import Filter
from mediagenerator.utils import get_media_dirs
from subprocess import Popen, PIPE
import os

class Sass(Filter):
    def __init__(self, **kwargs):
        self.config(kwargs, path=())
        if isinstance(self.path, basestring):
            self.path = (self.path,)
        super(Sass, self).__init__(**kwargs)
        assert self.filetype == 'css', (
            'Sass only supports compilation to css. '
            'The parent filter expects "%s".' % self.filetype)

        self.input_filetype = 'sass'

        self.path += tuple(get_media_dirs())
        self.path_args = []
        for path in self.path:
            self.path_args.extend(('-I', path))

    def get_output(self, variation):
        for input in self.get_input(variation):
            yield self._compile(input)

    def get_dev_output(self, name, variation):
        input = super(Sass, self).get_dev_output(name, variation)
        return self._compile(input)

    def _compile(self, input):
        cmd = Popen(['sass', '-C', '-t', 'expanded', '-E', 'utf-8']
                    + self.path_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        import logging
        logging.info(cmd.stdout.read())
        logging.info(cmd.stderr.read())
        output = cmd.communicate(input)[0]
        assert cmd.wait() == 0, 'Command returned bad result'
        return output.replace(os.linesep, '\n')
