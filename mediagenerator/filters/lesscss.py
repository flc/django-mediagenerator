from hashlib import sha1
from mediagenerator.generators.bundles.base import Filter
from mediagenerator.utils import find_file
from subprocess import Popen, PIPE
import os, sys

class LessCSS(Filter):    
    """
    LessCSS filter
    You need node.js and lessc on your path
    """

    takes_input = False

    def __init__(self, **kwargs):
        print('less css')
        self.config(kwargs, module=None)
        super().__init__(**kwargs)
        assert self.filetype == 'css', (
            'LessCSS only supports compilation to css. '
            'The parent filter expects "%s".' % self.filetype)
        self._compiled = None
        self._compiled_hash = None
        self._mtime = None

    @classmethod
    def from_default(cls, name):
        return {'module': name}

    def get_output(self, variation):
        self._regenerate(debug=False)
        yield self._compiled

    def get_dev_output(self, name, variation):
        assert name == self.module
        self._regenerate(debug=True)
        return self._compiled

    def get_dev_output_names(self, variation):
        self._regenerate(debug=True)
        yield self.module, self._compiled_hash

    def _regenerate(self, debug=False):
        path = find_file(self.module)
        mtime = os.path.getmtime(path)
        if mtime == self._mtime:
            return

        self._compiled = self._compile(path, debug=debug)
        self._compiled_hash = sha1(self._compiled).hexdigest()
        self._mtime = mtime

    def _compile(self, path, debug=False):
        try:
            filepath, filename = os.path.split(path)
            cmd = Popen(['lessc', filename], stdin=PIPE, stdout=PIPE, stderr=PIPE,
                        shell=sys.platform == 'win32', universal_newlines=True, cwd=filepath)
            output, error = cmd.communicate("")
            assert cmd.wait() == 0, ('LessCSS command returned bad '
                                     'result:\n%s' % error)
            return output
        except Exception as e:
            raise ValueError("Failed to run LessCSS compiler for this "
                "file. Please confirm that the \"lessc\" application is "
                "on your path and that you can run it from your own command "
                "line.\n"\
                "File: %s\n"\
                "Error was: %s" % (path, e))
