from setuptools import setup, find_packages
from os import path

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_d = f.read()

setup(
    name='nite',
    version='0.1.0',
    description='Nitter scraping tool',
    long_description=long_d,
    long_description_content_type="text/markdown",
    author='Your Future Boyfriend',
    author_email='n1ghtpe0ple@protonmail.com',
    url='https://github.com/xrce/nite',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(),
    install_requires=["requests", "argparse", "termcolor", "beautifulsoup4"],
    project_urls={"Source":"https://github.com/xrce/nite"}
)