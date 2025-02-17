#!/usr/bin/env python3

import json
import os
import subprocess
from ingredient_phrase_tagger.training import utils
from .folder_paths import input_folder, output_folder

PACKAGE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MODEL_PATH = os.path.join(PACKAGE_DIRECTORY, "model", "model.crfmodel")


def _exec_crf_test(
    input_text: str,
    model_path: str,
):
    try:
        with open("thefile", mode="w", encoding="utf-8") as input_file:
            # input_text = [safeStr(line) for line in input_text]

            input_file.write(utils.export_data(input_text))
            input_file.flush()
            return subprocess.check_output(
                ["crf_test", "--verbose=1", "--model", model_path, input_file.name]
            ).decode("utf-8")
    finally:
        try:
            os.remove("thefile")
        except:
            pass


def _convert_crf_output_to_json(crf_output: list[str]):
    return utils.import_data(crf_output)


def process_lines(
    ingredient_lines: list[str],
    model_path: str = None,
) -> list[dict[str, str]]:
    path = model_path or DEFAULT_MODEL_PATH
    crf_output = _exec_crf_test(
        input_text=ingredient_lines,
        model_path=path,
    )
    return _convert_crf_output_to_json(crf_output.split("\n"))


def crf_output_from_file(
    file: str,
    model_path: str = None,
):
    with open(os.path.join(input_folder, file), encoding="utf-8") as f:
        raw_ingredient_lines = json.load(f)
    return process_lines(
        ingredient_lines=raw_ingredient_lines,
        model_path=model_path,
    )


def write_crf_output(
    crf_output,
    output_folder: str,
    filename: str,
):
    file_name = os.path.join(output_folder, filename)

    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(crf_output, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
