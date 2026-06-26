from setuptools import setup, find_packages

setup(
    name='skill-safety-verifier',
    version='1.0.0',
    description='Security-first skill vetting for AI agents',
    author='ttttstc',
    author_email='423310463@qq.com',
    url='https://github.com/ttttstc/skill-safety-verifier',
    packages=find_packages(),
    install_requires=[
        'requests>=2.28.0',
    ],
    entry_points={
        'console_scripts': [
            'skill-safety-check=analyzer:main',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
