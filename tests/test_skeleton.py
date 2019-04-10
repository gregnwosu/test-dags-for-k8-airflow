#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from test_dags_for_k8_airflow.skeleton import fib

__author__ = "Gregory Nwosu"
__copyright__ = "Gregory Nwosu"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
