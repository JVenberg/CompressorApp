"""
 py2app/py2exe build script for MyApplication.

 Will automatically ensure that all build prerequisites are available
 via ez_setup

 Usage (Mac OS X):
     python setup.py py2app

 Usage (Windows):
     python setup.py py2exe
"""
# import ez_setup
# ez_setup.use_setuptools()

import sys
from setuptools import setup

mainscript = 'Compressor.py'

if sys.platform == 'darwin':
	extra_options = dict(
		setup_requires=['py2app'],
		app=[mainscript],
		options=dict(
			py2app=dict(
				argv_emulation=True,
				iconfile='icon.icns',
				bdist_base="mac/build",
				dist_dir="mac/dist"
				)
			)
		)

elif (sys.platform == 'win32'):
	extra_options = dict(
		setup_requires=['py2exe'],
		app=[mainscript],
	)

else:
	extra_options = dict(
	 	windows=[{'script':[mainscript], "icon_resources": [(1,"icon.ico")]}],
	)

setup(
    name="Compressor",
    **extra_options
)