from setuptools import setup, find_packages

setup(
    name='remote-mouse-driver',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pyserial',
    ],
    entry_points={
        'console_scripts': [
            'remote-mouse-driver = remote_mouse_driver.driver:main',
        ],
    },
    author='Eloi Tisserand',
    author_email='eloi.tisserand@epitech.eu',
    description='A simple driver to control the mouse with an ESP32.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nemesis-deb/remote-mouse-driver',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)