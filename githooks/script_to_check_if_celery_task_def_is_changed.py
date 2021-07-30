#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

from __future__ import absolute_import

import ast
import os
import subprocess


def check_celery_task_func_def_changed():
    result = subprocess.run(["git", "diff", "master", "--name-only"], capture_output=True, text=True)
    filenames = result.stdout.split('\n')
    for filename in filenames:
        if not filename.endswith('tasks.py'):
            continue
        if filename.endswith('.py'):
            _check_celery_task_file(filename)


def _check_celery_task_file(filename):
    print(filename)
    r = open(os.path.abspath(filename), 'r')
    tree = ast.parse(r.read())
    func_name_changed = []
    task_def_changed = _get_func_names_which_changed()
    for stmt in ast.walk(tree):
        if not isinstance(stmt, ast.FunctionDef):
            continue
        for decorator in stmt.decorator_list:
            if (
                isinstance(decorator.func, ast.Name)
                and decorator.func.id in ['task', 'periodic_task']
                and stmt.name in task_def_changed
            ):
                func_name_changed.append(stmt.name)

    if func_name_changed:
        return func_name_changed


def _get_func_names_which_changed():
    """
    Command:
        git diff --color=always | grep 'def' | cut -d " " -f2 | cut -d "(" -f1 | sort | uniq
    Output:
        ["func_name_1", "func_name_2"]

    """
    git_diff = subprocess.run(['git', 'diff'], check=True, capture_output=True)
    func_names = subprocess.run(['grep', 'def'], input=git_diff.stdout, capture_output=True)
    git_diff = subprocess.run(['git', 'diff', '--color=always'], check=True, capture_output=True)
    func_names = subprocess.run(['grep', 'def'], input=git_diff.stdout, capture_output=True)
    replace_space = subprocess.run(['cut', '-d', ' ', '-f2'], input=func_names.stdout, capture_output=True)
    replace_bracket = subprocess.run(['cut', '-d', '(', '-f1'], input=replace_space.stdout, capture_output=True)
    sort_names = subprocess.run(['sort'], input=replace_bracket.stdout, capture_output=True)
    uniq_names = subprocess.run(['uniq'], input=sort_names.stdout, capture_output=True)
    return uniq_names.stdout.decode('utf-8').split('\n')


check_celery_task_func_def_changed()
