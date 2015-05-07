from setuptools import setup, find_packages

setup (
        name = "cassandra_remote_control",
        version = "0.0.1",
        packages = find_packages(),

        install_requires = ["flask", "subprocess32", "configobj" ],
        scripts = ["remote-control.py"],

        author = "Baptiste Mille-Mathias",
        author_email = "baptiste.millemathias@gmail.com",
        )
