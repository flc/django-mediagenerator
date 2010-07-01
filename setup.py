from setuptools import setup
import os

DESCRIPTION = 'Extensible JavaScript/CSS combiner and compressor'

LONG_DESCRIPTION = None
try:
    LONG_DESCRIPTION = open('README.rst').read()
except:
    pass

setup(name='django-mediagenerator',
      packages=['mediagenerator'],
      author='Waldemar Kornewald',
      url='http://www.allbuttonspressed.com/projects/django-mediagenerator',
      include_package_data=True,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      platforms=['any'],
      install_requires=[],
)
