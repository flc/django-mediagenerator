from django.conf import settings
from django.utils.encoding import smart_str
from mediagenerator.generators.bundles.base import Filter

class UglifyJS(Filter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        assert self.filetype == 'js', (
            'UglifyJS only supports compilation to js. '
            'The parent filter expects "%s".' % self.filetype)

    def get_output(self, variation):
        # We import this here, so App Engine Helper users don't get import
        # errors.
        from subprocess import Popen, PIPE
        for input in self.get_input(variation):
            args = ['uglifyjs']
            try:
                args = args + settings.UGLIFYJS_OPTIONS
            except AttributeError:
                pass
            try:
                cmd = Popen(args,
                            stdin=PIPE, stdout=PIPE, stderr=PIPE,
                            universal_newlines=True)
                output, error = cmd.communicate(smart_str(input))
                assert cmd.wait() == 0, 'Command returned bad result:\n%s' % error
                yield output.decode('utf-8')
            except Exception as e:
                raise ValueError("Failed to run UglifyJS. "
                    "Please make sure you have Node.js and UglifyJS installed "
                    "and that it's in your PATH.\n"
                    "Error was: %s" % e)
