import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
INSTALL_REQUIREMENTS = ["Pillow"]

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'django-initialcon',
    version = '0.1.3',
    packages = ['initialcon'],
    include_package_data = True,
    license = 'MIT License',
    description = 'A small django application for generating small colourful icons for users profile pictures',
    long_description = README,
    url = 'https://github.com/bettsmatt/django-initialcon',
    author = 'Matthew Betts',
    author_email = 'matt.je.betts@gmail.com',
    classifiers =[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ]
)
