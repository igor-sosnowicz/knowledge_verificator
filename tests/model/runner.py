"""Module running experiments on language models."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import importlib
import importlib.util
import inspect
import os
from pathlib import Path
from typing import Callable

import numpy as np
from tqdm import tqdm

from knowledge_verificator.utils.filesystem import create_text_file
from knowledge_verificator.io_handler import console


class Metric(Enum):
    """List of metrics available."""

    COSINE_SIMILARITY = 0
    BLEU_4 = 1
    METEOR = 2
    ROUGE_3 = 3


@dataclass
class Result:
    """Dataclass representing a result of a test."""

    model_name: str
    metric: Metric
    data_points: np.ndarray


def generate_test_summary_in_csv(results: list[Result]) -> str:
    """
    Generate an experiment summary report in a CSV format.

    Args:
        results (list[Result]): List of results of experiments.

    Returns:
        str: Formatted CSV file with experiment results.
    """
    report = ''
    report += 'model_name,metric,average_score\n'
    for result in results:
        average_score = round(np.average(result.data_points), 3)
        report += f'{result.model_name},{result.metric.name},{average_score}\n'

    return report


class ExperimentRunner:
    """
    Class discovering experiments on language models, running them,
    and saving their results.
    """

    def __init__(self, directory: Path) -> None:
        self.directory = directory.resolve()
        if not self.directory.exists():
            raise FileNotFoundError(
                f'Non-existent directory with experiments `{self.directory}`.'
            )

    def _collect_experiments(self) -> list[Callable]:
        experiment_functions: list[Callable] = []
        excluded = ('__init__.py', 'results', 'runner.py')
        for file in os.listdir(path=self.directory):
            file_path = self.directory / file

            if file in excluded:
                continue

            if not os.path.isfile(file_path):
                continue

            if not file.endswith('.py'):
                continue

            experiment_functions.extend(
                self._collect_functions_from_file(file_path=file_path)
            )

        return experiment_functions

    def _collect_functions_from_file(self, file_path: Path) -> list[Callable]:
        """
        Call all functions from a give file. These functions must not have
        any arguments.

        Args:
            file_path (Path): Path to a file with functions.

        Returns:
            list[Callable]: List of functions extracted from a file.
        """
        # Get the module name from the file path
        module_name = os.path.splitext(os.path.basename(file_path))[0]

        # Load the module
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            raise ImportError(f'Could not load module from {file_path}')

        module = importlib.util.module_from_spec(spec)
        if spec.loader is None:
            raise ImportError(f'Could not load module loader for {file_path}.')

        spec.loader.exec_module(module)

        # Only function performing experiments: measure_
        return [
            func
            for func_name, func in inspect.getmembers(
                module, inspect.isfunction
            )
            if func_name.startswith('measure_')
        ]

    def run(self) -> None:
        """
        Discover experiments on language models and run them.

        Create a file with results in subdirectory of the provided (in constructor) `directory`.
        """
        results: list[Result] = []
        for experiment in tqdm(
            desc='Running experiments',
            unit='experiment',
            iterable=self._collect_experiments(),
        ):
            console.print(f'Running {experiment.__name__}...')
            result = experiment()
            if isinstance(result, Result):
                results.append(result)
            elif isinstance(result, list):
                results.extend(result)
            else:
                raise TypeError(
                    f'Running an experiment {experiment.__name__} returned '
                    'output of the '
                    f'type {type(result)}. It cannot be handled.'
                )

        experimental_results = generate_test_summary_in_csv(results=results)
        current_datetime = datetime.now().strftime('%H_%M_%S_%Y_%m_%d')
        create_text_file(
            path=f'tests/model/results/qg_{current_datetime}.csv',
            content=experimental_results,
        )
        console.print(
            'The results of the last experiments are stored in the tests/model/results'
            f'/qg_{current_datetime}.csv file.'
        )
