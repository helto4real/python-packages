import re
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# Auto detect the library version from the __init__.py file
with open('smhi/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)
                        
setuptools.setup(
    name="smhi_pkg",
    version="0.0.1",
    author="helto4real",
    author_email="info@joysoftware.org",
    description="Gets the weather forecast data from Swedish weather institute",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/helto4real/python-packages/smhi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
    ],
)