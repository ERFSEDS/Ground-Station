from setuptools import setup

package_name = 'sensor_values'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Paul',
    maintainer_email='CONWAYP2@my.erau.edu',
    description='Distributes sensor values to various topics',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'process_values = sensor_values.values_input:main',
        'test_process = sensor_values.values_output:main'
        ],
    },
)
