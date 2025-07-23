from setuptools import setup, find_packages

setup(
    name="task-tracker-cli",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "task=task_tracker.cli:run",
        ],
    },
    author="Juan Pablo Martínez",
    description="Una CLI simple para rastrear tareas desde la terminal usando JSON.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)