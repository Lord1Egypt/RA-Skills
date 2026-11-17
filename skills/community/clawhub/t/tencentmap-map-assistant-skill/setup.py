from setuptools import setup

setup(
    name='tencentmap-map-assistant',
    version='1.5.2',
    py_modules=['tmap_client', 'send_code', 'create_key', 'save_config'],
    package_dir={'': 'scripts'},
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'tmap-send-code=send_code:main',
            'tmap-create-key=create_key:main',
            'tmap-save-config=save_config:main',
        ],
    },
)
